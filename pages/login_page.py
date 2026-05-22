from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    LOGIN_FIELD = (By.NAME, "login")
    PASSWORD_FIELD = (By.NAME, "passwd")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'input[src="/imgs/but_in.gif"]')

    def login(self, email, password="123123"):
        self.send_keys(self.LOGIN_FIELD, email)
        self.send_keys(self.PASSWORD_FIELD, password)
        self.click(self.SUBMIT_BUTTON)
        return self