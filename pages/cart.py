from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class CartPage(BasePage):
    CART_ICON = (By.XPATH,'(//a[@id="HeaderCartTrigger"])[2]')
    CART_ITEMS = (By.XPATH,'//div[@class="cart__item"]')
    TRASH_BUTTON_XPATH = './/div[@class="cart__remove"]'
    REMOVE_BUTTON = (By.XPATH,'//span[contains(text(),"Remove")]')
    EMPTY_CART = (By.CSS_SELECTOR,'div[class="rte text-spacing"]')

    def __init__(self,driver):
        super().__init__(driver)

    def open_cart(self):
        self.logger.info('opening cart')
        self.click(self.CART_ICON)

    def get_items_in_cart(self):
        self.logger.info('getting items in cart')
        cart_items_list = self.driver.find_elements(*self.CART_ITEMS)
        cart_items = [item.text for item in cart_items_list]
        return cart_items

    def remove_cart_item_by_index(self,index=0):
        self.logger.info('removing the product to cart')
        cart_items_list = self.driver.find_elements(*self.CART_ITEMS)
        if index<len(cart_items_list):
            remove_button = cart_items_list[index].find_element(By.XPATH,self.TRASH_BUTTON_XPATH)
            remove_button.click()
            self.click(self.REMOVE_BUTTON)
        else:
            raise IndexError(f"Product index {index} not found. Only {len(cart_items_list)} products available.")

    def no_item_in_cart(self):
        self.logger.info('no result is found')
        self.get_text(self.EMPTY_CART)