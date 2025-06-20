# pages/checkout_step_one_page.py

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class CheckoutStepOnePage(BasePage):
    """
    Page Object for the first step of the checkout process (entering user info).
    """
    # --- Locators ---
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    def __init__(self, driver):
        super().__init__(driver)

    def fill_checkout_information(self, first_name, last_name, postal_code):
        """
        Fills the first name, last name, and postal code fields.
        """
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.POSTAL_CODE_INPUT, postal_code)
        self.logger.info(f"Filled checkout information for {first_name} {last_name}.")

    def click_continue(self):
        """Clicks the 'Continue' button to proceed to the next step."""
        self.click(self.CONTINUE_BUTTON)
        self.logger.info("Clicked the Continue button on checkout page.")