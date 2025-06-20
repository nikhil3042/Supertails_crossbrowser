# pages/checkout_complete_page.py

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class CheckoutCompletePage(BasePage):
    """
    Page Object for the final "Checkout: Complete!" page.
    """
    # --- Locators ---
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        super().__init__(driver)

    def get_confirmation_message(self):
        """Gets the text of the final confirmation message."""
        if self.is_visible(self.COMPLETE_HEADER):
            return self.get_text(self.COMPLETE_HEADER)
        return "Confirmation message not found."