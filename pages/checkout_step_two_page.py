# pages/checkout_step_two_page.py

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class CheckoutStepTwoPage(BasePage):
    """
    Page Object for the second step of the checkout process (order overview).
    """
    # --- Locators ---
    PAGE_TITLE = (By.CLASS_NAME, "title")
    FINISH_BUTTON = (By.ID, "finish")

    def __init__(self, driver):
        super().__init__(driver)

    def is_overview_page_displayed(self):
        """Verifies if the checkout overview page is displayed."""
        if self.is_visible(self.PAGE_TITLE):
            return "OVERVIEW" in self.get_text(self.PAGE_TITLE).upper()
        return False

    def click_finish(self):
        """Clicks the 'Finish' button to complete the purchase."""
        self.click(self.FINISH_BUTTON)
        self.logger.info("Clicked the Finish button.")