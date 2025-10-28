import allure
import pytest
import time
from pages.product_catalog import ProductCatalog
from pages.cart import CartPage
from tests.base_test import BaseTest
from config.environment import Environment

@allure.feature("Integration Flow")
@allure.story("Product Catalog to Cart Integration")
class TestIntegrationCartCatalog(BaseTest):

    @allure.title("TC_INT_001 - Verify product added from catalog appears in cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    @pytest.mark.regression
    def test_add_product_to_cart_from_catalog(self):
        """
        TC_INT_001 - Verify adding a product from catalog reflects correctly in cart.
        """
        env = Environment("supertails")
        base_url = env.get_base_url()
        catalog = ProductCatalog(self.driver)
        cart = CartPage(self.driver)

        with allure.step("Navigate to Supertails home page"):
            self.logger.info(f"Navigating to URL: {base_url}")
            self.driver.get(base_url)
            assert "Supertails" in self.driver.title or "Pet" in self.driver.title,"Page title does not indicate Supertails homepage"  # 🔹 Added assertion for page validation

        with allure.step("Search for a product and add to cart"):
            try:
                catalog.search_product("dog food")
                products = catalog.get_list_products()
                self.logger.info(f"Products found: {products}")

                assert len(products) > 0, "No products found for search term 'dog food'"
                catalog.click_product_by_index(2)  # 🔹 Changed: Open product page first instead of direct add_to_cart_by_index
                self.logger.info("Opened 3rd product from search results successfully.")
                catalog.add_to_cart()
                self.logger.info("Product added to cart successfully.")
                time.sleep(5)
            except Exception as e:
                self.logger.error(f"Error adding product to cart: {e}")
                allure.attach(self.driver.page_source, name="Add to Cart Failure", attachment_type=allure.attachment_type.HTML)
                pytest.fail(f"Failed during add-to-cart: {e}")

        with allure.step("Open cart and verify added product"):
            try:
                cart.open_cart()
                time.sleep(3)
                items = cart.get_items_in_cart()
                self.logger.info(f"Cart contents: {items}")

                assert len(items) > 0, "No items found in cart after adding product."
                allure.attach(str(items), name="Cart Verification", attachment_type=allure.attachment_type.TEXT)

                # 🔹 Optional: Further validation
                added_item_name = items[0].lower()
                assert "dog" in added_item_name or "food" in added_item_name, f"Unexpected product in cart: {added_item_name}"

            except Exception as e:
                self.logger.error(f"Error verifying cart after add: {e}")
                allure.attach(self.driver.page_source, name="Cart Verification Failure",attachment_type=allure.attachment_type.HTML)
                pytest.fail(f"Cart verification failed: {e}")
