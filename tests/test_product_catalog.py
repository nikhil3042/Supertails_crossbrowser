import allure
import pytest
from pages.product_catalog import ProductCatalog
from tests.base_test import BaseTest
from config.environment import Environment

@allure.feature("Product Catalog")
@allure.story("Product Search and Listing")
class TestProductCatalog(BaseTest):

    @allure.title("TC_PC_001 - Verify user can search for a valid product and see results")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_search_valid_product(self):
        """
        TC_PC_001 - Verify user can search for a valid product and get matching results.
        """
        env = Environment("supertails")
        base_url = env.get_base_url()
        catalog = ProductCatalog(self.driver)

        with allure.step("Navigate to Supertails home page"):
            self.logger.info(f"Navigating to URL: {base_url}")
            self.driver.get(base_url)

        with allure.step("Search for a valid product (dog food)"):
            try:
                catalog.search_product("dog food")
                self.logger.debug("Search executed successfully.")

                products = catalog.get_list_products()
                self.logger.info(f"Products returned: {len(products)}")
                self.logger.debug(f"Product list: {products}")

                assert len(products) > 0, "No products found for a valid search."
                allure.attach(str(products), name="Search Results", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                self.logger.error(f"Error during product search: {e}")
                allure.attach(self.driver.page_source, name="Search Failure Page", attachment_type=allure.attachment_type.HTML)
                pytest.fail(f"Test failed due to exception: {e}")

    @allure.title("TC_PC_002 - Verify 'No Results' message is displayed for invalid product search")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_search_invalid_product(self):
        """
        TC_PC_002 - Verify searching for invalid product displays 'No Results' message.
        """
        env = Environment("supertails")
        base_url = env.get_base_url()
        catalog = ProductCatalog(self.driver)

        with allure.step("Navigate to Supertails home page"):
            self.logger.info(f"Navigating to URL: {base_url}")
            self.driver.get(base_url)

        with allure.step("Search for invalid product"):
            try:
                catalog.search_product("random_invalid_product_xyz")
                self.logger.debug("Search executed with invalid product.")

                message = catalog.no_result()
                self.logger.info(f"No result message: {message}")

                assert "no" in message.lower(), "Expected 'No Results' message not displayed."
            except Exception as e:
                self.logger.error(f"Error during invalid product search: {e}")
                allure.attach(self.driver.page_source, name="Invalid Search Failure", attachment_type=allure.attachment_type.HTML)
                pytest.fail(f"Test failed due to exception: {e}")
