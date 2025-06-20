# tests/test_smoke_journey.py

import pytest
import allure
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.checkout_complete_page import CheckoutCompletePage
from config.environment import Environment


@allure.epic("End-to-End Tests")
@allure.feature("Purchase Journey")
class TestSmokePurchase(BaseTest):
    """
    Contains smoke tests for the main user journeys.
    """

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Happy Path Purchase")
    @allure.title("Test End-to-End Purchase for a Standard User")
    @allure.description(
        "This test verifies the complete purchase cycle: Login > Add Item > Checkout > Finish > Logout.")
    def test_end_to_end_purchase_happy_path(self):
        """
        Verifies the full, successful purchase journey.
        """
        # --- ARRANGE ---
        login_page = LoginPage(self.driver)
        inventory_page = InventoryPage(self.driver)
        cart_page = CartPage(self.driver)
        checkout_step_one_page = CheckoutStepOnePage(self.driver)
        checkout_step_two_page = CheckoutStepTwoPage(self.driver)
        checkout_complete_page = CheckoutCompletePage(self.driver)
        env = Environment()
        base_url = env.get_base_url()

        # --- ACT & ASSERT ---

        with allure.step("1. Login to Application"):
            login_page.navigate_to(base_url)
            login_page.login(env.get_username(), env.get_password())
            assert inventory_page.is_inventory_page_displayed(), "Did not land on inventory page."
            self.logger.info("Login successful and inventory page is displayed.")

        with allure.step("2. Add Item to Cart and Verify Badge"):
            inventory_page.add_item_to_cart("Sauce Labs Backpack")
            assert inventory_page.wait_for_cart_badge_to_update("1"), "Cart badge did not update to 1."
            self.logger.info("Item added to cart and badge count is correct.")

        with allure.step("3. Navigate to Cart and Verify Item"):
            inventory_page.click_shopping_cart()
            assert cart_page.is_item_in_cart("Sauce Labs Backpack"), "Correct item was not found in the cart."
            self.logger.info("Successfully navigated to cart and verified the item.")

        with allure.step("4. Proceed to Checkout and Fill Information"):
            cart_page.click_checkout()
            checkout_step_one_page.fill_checkout_information("Test", "User", "560001")
            checkout_step_one_page.click_continue()
            self.logger.info("Filled checkout info and continued to the overview page.")

        with allure.step("5. Verify Overview and Finish Purchase"):
            assert checkout_step_two_page.is_overview_page_displayed(), "Did not land on checkout overview page."
            checkout_step_two_page.click_finish()
            self.logger.info("Verified overview and finished the purchase.")

        with allure.step("6. Verify Order Confirmation"):
            confirmation_message = checkout_complete_page.get_confirmation_message()
            assert "THANK YOU FOR YOUR ORDER" in confirmation_message.upper(), "Confirmation message was not found or incorrect."
            self.logger.info(f"Order confirmed with message: {confirmation_message}")

        with allure.step("7. Logout"):
            # The logout function is on the inventory page object, accessible via the menu
            inventory_page.logout()
            assert login_page.is_visible(login_page.LOGIN_BUTTON), "User was not logged out successfully."
            self.logger.info("Logout was successful.")