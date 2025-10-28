import allure
import pytest
from pages.cart import CartPage
from tests.base_test import BaseTest
from config.environment import Environment

@allure.feature("Cart Management")
@allure.story("View and Modify Cart")
class TestCart(BaseTest):

    @allure.title("TC_CART_001 - Verify user can open cart and view added items")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_open_cart(self):
        """
        TC_CART_001 - Verify user can open cart and see items if any exist.
        """
        env = Environment("supertails")
        base_url = env.get_base_url()
        cart = CartPage(self.driver)

        with allure.step("Navigate to Supertails home page"):
            self.logger.info(f"Navigating to: {base_url}")
            self.driver.get(base_url)

        with allure.step("Open the cart and verify contents"):
            try:
                cart.open_cart()
                self.logger.debug("Cart opened successfully.")

                items = cart.get_items_in_cart()
                self.logger.info(f"Items found in cart: {len(items)}")
                self.logger.debug(f"Cart contents: {items}")

                assert isinstance(items, list), "Cart items not retrieved correctly."
                allure.attach(str(items), name="Cart Items", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                self.logger.error(f"Error opening or reading cart: {e}")
                allure.attach(self.driver.page_source, name="Cart Failure Page", attachment_type=allure.attachment_type.HTML)
                pytest.fail(f"Test failed: {e}")

    @allure.title("TC_CART_002 - Verify user can remove an item from the cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_remove_item_from_cart(self):
        """
        TC_CART_002 - Verify removing an item from cart works properly.
        """
        env = Environment("supertails")
        base_url = env.get_base_url()
        cart = CartPage(self.driver)

        with allure.step("Navigate to Supertails home page"):
            self.logger.info(f"Navigating to: {base_url}")
            self.driver.get(base_url)

        with allure.step("Remove an item from the cart"):
            try:
                cart.open_cart()
                items_before = cart.get_items_in_cart()
                self.logger.debug(f"Items before removal: {items_before}")

                if len(items_before) > 0:
                    cart.remove_cart_item_by_index(0)
                    self.logger.info("Removed first item from cart successfully.")

                    empty_msg = cart.no_item_in_cart()
                    self.logger.info(f"Empty cart message: {empty_msg}")
                    assert "empty" in empty_msg.lower(), "Cart not empty after removal."
                else:
                    self.logger.warning("Cart already empty; skipping removal check.")
            except Exception as e:
                self.logger.error(f"Error while removing cart item: {e}")
                allure.attach(self.driver.page_source, name="Cart Remove Failure", attachment_type=allure.attachment_type.HTML)
                pytest.fail(f"Test failed due to exception: {e}")
