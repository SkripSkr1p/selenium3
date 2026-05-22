from selenium.webdriver.common.by import By
from .base_page import BasePage


class CatalogPage(BasePage):
    BYTOVAYA_TECH = (By.PARTIAL_LINK_TEXT, "Бытовая техника")
    AUDIO_TECH = (By.PARTIAL_LINK_TEXT, "Аудиотехника")

    def go_to_bytovaya(self):
        self.click(self.BYTOVAYA_TECH)
        return self

    def go_to_audio(self):
        self.click(self.AUDIO_TECH)
        return self

    def add_mikrofon_mb7k_to_cart(self):
        """Добавляет Микрофон MB-7K в корзину прямо из списка"""
        locator = (By.XPATH, '//a[contains(@onclick, "ChangeBasket(553196")]')
        self.click(locator)
        return self