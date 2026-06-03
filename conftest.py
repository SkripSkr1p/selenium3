# conftest.py
import pytest
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import time
import requests

from pages.main_page import MainPage
from pages.registration_page import RegistrationPage


# ---------- Pytest command-line options ----------
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome or firefox")
    parser.addoption("--language", action="store", default="ru", help="User language")


# ---------- Helper functions ----------
def generate_a_email(min_a=1, max_a=30, domain="gmail.com"):
    name = 'g' * random.randint(min_a, max_a)
    return f"{name}@{domain}"

TOKEN = "token"
PROJECT_ID = 1794247
PRIORITY_ID = 5386321
SEVERITY_ID = 8965835
STATUS_ID = 12560224
TYPE_ID = 5398771

def upload_attachment(issue_id, file_path):
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    with open(file_path, "rb") as f:
        files = {
            "attached_file": (
                os.path.basename(file_path),
                f,
                "image/png"
            )
        }

        data = {
            "object_id": issue_id,
            "content_type": "issues.issue"
        }

        r = requests.post(
            "https://api.taiga.io/api/v1/attachments",
            headers=headers,
            files=files,
            data=data
        )

    print("UPLOAD STATUS:", r.status_code)
    print("UPLOAD RESPONSE:", r.text)

    return r

def create_taiga_issue(subject, description, screenshot=None):

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "project": PROJECT_ID,
        "subject": subject,
        "description": description,
        "priority": PRIORITY_ID,
        "severity": SEVERITY_ID,
        "status": STATUS_ID,
        "type": TYPE_ID
    }

    r = requests.post(
        "https://api.taiga.io/api/v1/issues",
        headers=headers,
        json=payload
    )

    print("TAIGA STATUS:", r.status_code)
    print("TAIGA RESPONSE:", r.text)

    data = r.json()

    # ❗ защита от краша
    if "id" not in data:
        print("❌ Issue not created, skipping attachment")
        return data

    if screenshot:
        upload_attachment(data["id"], screenshot)

    return data

# ---------- Fixtures ----------
@pytest.fixture(scope="function")
def browser(request):
    """Основная фикстура браузера"""
    browser_name = request.config.getoption("--browser")
    language = request.config.getoption("--language")

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        if language:
            options.add_experimental_option('prefs', {'intl.accept_languages': language})

    elif browser_name == "firefox":
        options = FirefoxOptions()
        if language:
            options.set_preference("intl.accept_languages", language)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver = webdriver.Remote(
        command_executor="http://localhost:4444",
        options=options,
        )
    driver.get("https://www.regtorg.ru/")
    # driver.maximize_window()  # уже в ChromeOptions

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def main_page(browser):
    """Главная страница — самая используемая фикстура"""
    return MainPage(browser)


@pytest.fixture(scope="function")
def go_to_registration(browser):
    """Переход на страницу регистрации (совместимость со старыми тестами)"""
    main_page = MainPage(browser)
    registration_page = main_page.go_to_registration()
    return registration_page


@pytest.fixture(scope="function")
def authorized_user(browser):
    """Фикстура: зарегистрированный и авторизованный пользователь"""
    email = generate_a_email()
    main_page = MainPage(browser)

    # Регистрация
    reg_page = main_page.go_to_registration()
    reg_page.register("Auto Test", "Auto Test User", email)

    # Выход и вход
    main_page.logout()
    login_page = main_page.go_to_login()
    login_page.login(email)

    return main_page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("browser")

    if browser is None:
        print("❌ NO BROWSER IN FUNCARGS")
        return

    try:
        os.makedirs("screenshots", exist_ok=True)

        screenshot = f"screenshots/{item.name}_{time.strftime('%Y%m%d-%H%M%S')}.png"

        # 🔥 ДОБАВЬ ЖЁСТКИЙ ФОКУС НА СТАБИЛЬНЫЙ СКРИН
        browser.save_screenshot(screenshot)

        print("📸 SCREENSHOT SAVED:", screenshot)

        create_taiga_issue(
            subject=f"FAILED: {item.name}",
            description=report.longreprtext,
            screenshot=screenshot
        )

    except Exception as e:
        print("❌ SCREENSHOT ERROR:", str(e))