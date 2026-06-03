# main_test.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.main_page import MainPage
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from conftest import generate_a_email


# ПОЗИТИВНЫЕ ТЕСТЫ

@pytest.mark.registration
@pytest.mark.smoke
def test_successful_registration(go_to_registration):
    reg_page = go_to_registration
    email = generate_a_email()

    reg_page.register("Test User", "Test FIO", email)

    assert MainPage(reg_page.browser).is_element_present((By.LINK_TEXT, "Выход"))


@pytest.mark.authorization
@pytest.mark.smoke
def test_successful_authorization(main_page):
    email = generate_a_email()

    reg_page = main_page.go_to_registration()
    reg_page.register("Test User", "Test Full Name", email)
    main_page.logout()

    login_page = main_page.go_to_login()
    login_page.login(email)

    assert main_page.is_element_present(main_page.LOGOUT_LINK)


@pytest.mark.e2e
@pytest.mark.smoke
def test_successful_registration_and_purchase(main_page):
    email = generate_a_email()

    reg_page = main_page.go_to_registration()
    reg_page.register("Buyer Test", "Buyer Full Name", email)

    catalog = main_page.go_to_catalog()
    catalog.go_to_bytovaya()
    catalog.go_to_audio()
    catalog.add_mikrofon_mb7k_to_cart()

    WebDriverWait(main_page.browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Оформить заказ"))
    ).click()

    assert any(word in main_page.browser.page_source.lower() 
               for word in ["заказ", "оформлен", "корзина"])


# НЕГАТИВНЫЕ ТЕСТЫ

@pytest.mark.registration
@pytest.mark.negative
def test_failed_registration(go_to_registration):
    reg_page = go_to_registration

    # Некорректные данные
    reg_page.send_keys(reg_page.NAME_FIELD, "aaaa11111")
    reg_page.send_keys(reg_page.FIO_FIELD, "aaaaaa111111")
    reg_page.send_keys(reg_page.LOGIN_FIELD, "invalid_email.com")   # без @
    reg_page.send_keys(reg_page.PASSWORD_FIELD, "12345")
    reg_page.send_keys(reg_page.PASSWORD2_FIELD, "12345")
    reg_page.click(reg_page.SUBMIT_BUTTON)

    # Проверка ошибки
    try:
        error = WebDriverWait(reg_page.browser, 8).until(
            EC.presence_of_element_located((By.XPATH, "//font[@color='red' or contains(text(),'Ошибка') or contains(text(),'E-mail')]"))
        )
        assert error.is_displayed()
    except TimeoutException:
        pytest.fail("Не отобразилось сообщение об ошибке при некорректной регистрации")


@pytest.mark.authorization
@pytest.mark.negative
def test_failed_authorization(main_page):
    login_page = main_page.go_to_login()

    login_page.send_keys(login_page.LOGIN_FIELD, "wrong@email.com")
    login_page.send_keys(login_page.PASSWORD_FIELD, "wrongpassword123")
    login_page.click(login_page.SUBMIT_BUTTON)

    # Проверка ошибки авторизации
    try:
        error = WebDriverWait(login_page.browser, 8).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Неверный') or contains(text(),'ошибка') or contains(text(),'Ошибка')]")),
                EC.presence_of_element_located((By.TAG_NAME, "font"))
            )
        )
        assert error.is_displayed()
    except TimeoutException:
        pytest.fail("Не отобразилось сообщение об ошибке при неудачной авторизации")
@pytest.mark.taiga
def test_taiga(main_page):
    assert False