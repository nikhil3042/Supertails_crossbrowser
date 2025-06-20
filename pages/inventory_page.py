# pages/inventory_page.py
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class InventoryPage(BasePage):
    """
    Page Object for the Sauce Labs Demo Inventory/Products page.
    """
    # --- Locators ---
    PAGE_TITLE = (By.CLASS_NAME, "title")
    SHOPPING_CART_ICON = (By.ID, "shopping_cart_container")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    # Using a dynamic locator for a specific product's add-to-cart button
    # We can use .format() to insert the product name later.
    ADD_TO_CART_BUTTON = (By.XPATH, "//div[text()='{}']/ancestor::div[@class='inventory_item']//button")

    # Locators for the menu and logout link
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        super().__init__(driver)

    def is_inventory_page_displayed(self):
        """Verifies if the inventory page is displayed by checking for the title."""
        if self.is_visible(self.PAGE_TITLE):
            return "PRODUCTS" in self.get_text(self.PAGE_TITLE).upper()
        return False

    def add_item_to_cart(self, item_name):
        """
        Adds a specific item to the cart by its name.
        Example: add_item_to_cart("Sauce Labs Backpack")
        """
        # Create a specific locator for the item by formatting our template
        item_locator = (self.ADD_TO_CART_BUTTON[0], self.ADD_TO_CART_BUTTON[1].format(item_name))
        self.click(item_locator)
        self.logger.info(f"Clicked 'Add to Cart' for item: {item_name}")

    def wait_for_cart_badge_to_update(self, expected_count_str, timeout=5):
        """
        Waits for the shopping cart badge to be visible and contain the expected number.

        Args:
            expected_count_str (str): The text expected inside the badge (e.g., "1").
            timeout (int): Maximum time to wait.

        Returns:
            bool: True if the condition is met, False if it times out.
        """
        try:
            self.logger.info(f"Waiting for cart badge to show '{expected_count_str}'...")
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(self.SHOPPING_CART_BADGE, expected_count_str)
            )
            self.logger.info("Cart badge updated correctly.")
            return True
        except:
            self.logger.error("Timeout: Cart badge did not update to the expected value.")
            return False

    def click_shopping_cart(self):
        """Navigates to the shopping cart page."""
        self.click(self.SHOPPING_CART_ICON)

    def logout(self):
        """Logs out of the application."""
        self.click(self.MENU_BUTTON)
        # It's good practice to wait for the logout link to be clickable
        self.click(self.LOGOUT_LINK)
        self.logger.info("User logged out successfully.")