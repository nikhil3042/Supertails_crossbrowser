"""
Base Page class containing common, reusable methods for all page objects.
This class is the foundation of the Page Object Model pattern.
"""

import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import get_logger  # Import our central logger utility


class BasePage:
    """
    Base class for all page objects. Contains common methods that can be used
    across all page objects to maintain the DRY (Don't Repeat Yourself) principle.
    """

    def __init__(self, driver):
        """
        Initialize BasePage with the WebDriver instance and our central logger.
        """
        self.driver = driver
        # Explicit wait timeout can be configured here
        self.wait = WebDriverWait(driver, 20)
        # Use our central logger, already configured in conftest.py
        self.logger = get_logger()

    @allure.step("Clicking Element: {locator}")
    def click(self, locator):
        """
        Waits for an element to be clickable and then clicks it.
        Fails the test immediately if the element is not clickable within the timeout.
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Successfully clicked element: {locator}")
        except TimeoutException:
            self.logger.error(f"Timeout: Element not clickable: {locator}")
            # Re-raise the exception to fail the test and trigger failure evidence capture
            raise

    @allure.step("Entering text '{text}' into Element: {locator}")
    def send_keys(self, locator, text, clear_first=True):
        """
        Sends keys to an element after waiting for it to be visible.
        Fails the test immediately if the element is not found within the timeout.
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Successfully entered text into element: {locator}")
        except TimeoutException:
            self.logger.error(f"Timeout: Element not visible for text entry: {locator}")
            raise

    @allure.step("Checking if Element is visible: {locator}")
    def is_visible(self, locator, timeout=10):
        """
        Checks if an element is visible on the page within a given timeout.
        Returns True or False. Does not fail the test.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            self.logger.info(f"Element is not visible within {timeout}s: {locator}")
            return False

    @allure.step("Getting text from Element: {locator}")
    def get_text(self, locator):
        """
        Gets text from an element. Fails test if element not found.
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            self.logger.info(f"Retrieved text '{text}' from element: {locator}")
            return text
        except TimeoutException:
            self.logger.error(f"Timeout: Could not get text from element as it was not visible: {locator}")
            raise

    @allure.step("Getting page title")
    def get_title(self):
        """Gets the title of the current page."""
        title = self.driver.title
        self.logger.info(f"Current page title: {title}")
        return title

    @allure.step("Navigating to URL: {url}")
    def navigate_to(self, url):
        """Navigates to a specific URL."""
        try:
            self.driver.get(url)
            self.logger.info(f"Successfully navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}. Error: {e}")
            raise
