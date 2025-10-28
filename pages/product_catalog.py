from selenium.common import ElementClickInterceptedException

from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ProductCatalog(BasePage):
    SEARCH_TEXTFIELD = (By.CSS_SELECTOR,'input#mainfrm')
    SEARCH_BUTTON = (By.XPATH,'(//span[contains(text(),"Search")])[5]')
    PRODUCT_CARDS = (By.XPATH,'//div[@id="searchResultsWrapper"]//li')
    ADD_TO_CART= (By.XPATH,'//span[contains(text(),"Add to Cart")]/..')
    NO_RESULT = (By.XPATH,'//div[@class="search-not-found noResult"]')

    def __init__(self,driver):
        super().__init__(driver)

    def search_product(self,name):
        self.logger.info(f'searching for product f{name}')
        self.send_keys(self.SEARCH_TEXTFIELD,name)
        try:
            self.click(self.SEARCH_BUTTON)
        except ElementClickInterceptedException:
            self.logger.warning("Search button click intercepted, retrying with JS click")
            btn = self.driver.find_element(*self.SEARCH_BUTTON)
            self.driver.execute_script("arguments[0].click();", btn)

    def get_list_products(self):
        self.logger.info(f'getting for products')
        products_list = self.driver.find_elements(*self.PRODUCT_CARDS)
        products = [product.text for product in products_list]
        return products

    def click_product_by_index(self,index=0):
        self.logger.info('clicking the product')
        products_list = self.driver.find_elements(*self.PRODUCT_CARDS)
        if index<len(products_list):
            products_list[index].click()
        else:
            raise IndexError(f"Product index {index} not found. Only {len(products_list)} products available.")

    def add_to_cart(self):
        """Clicks the Add to Cart button on the product detail page."""
        self.logger.info("Clicking Add to Cart button on product detail page")
        try:
            self.click(self.ADD_TO_CART)
            self.logger.info("Add to Cart button clicked successfully")
        except Exception:
            self.logger.warning("Normal click failed, retrying with JS click")
            add_button = self.wait_for_element(self.ADD_TO_CART)
            self.driver.execute_script("arguments[0].scrollIntoView();",add_button)
            self.driver.execute_script("arguments[0].click();", add_button)

    def no_result(self):
        self.logger.info('no result is found')
        return self.get_text(self.NO_RESULT)