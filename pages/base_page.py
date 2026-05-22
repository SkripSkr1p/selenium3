from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, browser, timeout=15):
        self.browser = browser
        self.wait = WebDriverWait(browser, timeout)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def send_keys(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator):
        return self.find(locator).text