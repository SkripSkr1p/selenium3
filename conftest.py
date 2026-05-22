# conftest.py
import pytest
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

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