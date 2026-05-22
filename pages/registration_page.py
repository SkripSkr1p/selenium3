from selenium.webdriver.common.by import By
from .base_page import BasePage


class RegistrationPage(BasePage):
    NAME_FIELD = (By.NAME, "_name")
    FIO_FIELD = (By.NAME, "_fio")
    LOGIN_FIELD = (By.NAME, "_login")
    PASSWORD_FIELD = (By.NAME, "_password")
    PASSWORD2_FIELD = (By.NAME, "_password2")
    SUBMIT_BUTTON = (By.NAME, "form_reg")
    REG_SUBMIT_IMG = (By.CSS_SELECTOR, 'input[src="/imgs/but_reg.gif"]')

    def register(self, name, fio, email, password="123123"):
        self.send_keys(self.NAME_FIELD, name)
        self.send_keys(self.FIO_FIELD, fio)
        self.send_keys(self.LOGIN_FIELD, email)
        self.send_keys(self.PASSWORD_FIELD, password)
        self.send_keys(self.PASSWORD2_FIELD, password)
        self.click(self.SUBMIT_BUTTON)
        return self