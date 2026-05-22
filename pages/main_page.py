# pages/main_page.py
from selenium.webdriver.common.by import By

from .base_page import BasePage
from .registration_page import RegistrationPage
from .login_page import LoginPage
from .catalog_page import CatalogPage


class MainPage(BasePage):
    REGISTRATION_LINK = (By.LINK_TEXT, "Регистрация")
    LOGIN_LINK = (By.LINK_TEXT, "Вход")           # ← поменяй, если текст ссылки другой
    CATALOG_LINK = (By.XPATH, "//a[contains(text(), 'Товары и услуги')]")
    LOGOUT_LINK = (By.LINK_TEXT, "Выход")

    def go_to_registration(self):
        self.click(self.REGISTRATION_LINK)
        return RegistrationPage(self.browser)

    def go_to_login(self):
        self.click(self.LOGIN_LINK)
        return LoginPage(self.browser)

    def go_to_catalog(self):
        self.click(self.CATALOG_LINK)
        return CatalogPage(self.browser)

    def logout(self):
        self.click(self.LOGOUT_LINK)