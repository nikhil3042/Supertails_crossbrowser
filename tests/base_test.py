"""
Base Test class containing common setup and teardown methods.
This class implements the foundation for all test classes.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import allure
import io
import logging
import time
from pathlib import Path

from utils.logger import get_logger
from config.environment import Environment

# --- NEW: Define Project Root as a Global Constant ---
# This is a robust way to get your project's root directory.
# It assumes this file (base_test.py) is inside a 'tests' folder,
# which is inside your project root.
PROJECT_ROOT = Path(__file__).parent.parent


class BaseTest:
    logger = get_logger()

    @pytest.fixture(scope="function", autouse=True)
    def setup_and_teardown(self, request, browser):
        """
        Setup/teardown fixture that supports multiple browsers dynamically.
        """
        self.logger.info(f"--- Starting test: {request.node.name} on {browser.upper()} ---")

        # --- Setup logging for this test ---
        log_stream = io.StringIO()
        stream_handler = logging.StreamHandler(log_stream)
        log_format = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        stream_handler.setFormatter(log_format)
        self.logger.addHandler(stream_handler)

        # --- Setup environment and browser ---
        self.env = Environment("supertails")
        self.env.set_browser(browser)
        self.logger.info(f"Running test on browser: {browser.upper()}")

        self.driver = self._setup_driver()
        request.cls.driver = self.driver

        with allure.step("Browser Setup"):
            self.driver.maximize_window()
            self.driver.implicitly_wait(self.env.config['browser']['implicit_wait'])
            self.driver.set_page_load_timeout(60)

        # --- Yield to test execution ---
        yield

        # --- Teardown section ---
        with allure.step("Test Teardown"):
            if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                self._capture_allure_screenshot(request)

            log_content = log_stream.getvalue()
            allure.attach(
                log_content,
                name=f"Execution Log for {request.node.name} ({browser.upper()})",
                attachment_type=allure.attachment_type.TEXT
            )

            self.logger.removeHandler(stream_handler)
            self.logger.info(f"--- Finished test: {request.node.name} on {browser.upper()} ---")

            if self.driver:
                self.driver.quit()

    def _setup_driver(self):
        """Sets up WebDriver. No longer needs arguments passed to it."""
        browser = self.env.config['browser']['default'].lower()
        headless = self.env.config['browser']['headless']
        self.logger.info(f"Setting up '{browser}' browser (Headless: {headless})")
        if browser == 'chrome':
            return self._setup_chrome_driver(headless)
        elif browser == 'edge':
            return self._setup_edge_driver(headless)
        else:
            self.logger.error(f"Unsupported browser: {browser}")
            raise ValueError(f"Unsupported browser: {browser}")

    def _setup_chrome_driver(self, headless=False):
        """
        Sets up Chrome WebDriver using your comprehensive list of options.
        """
        options = ChromeOptions()

        # Use the PROJECT_ROOT constant defined at the top of the file
        profile_path = PROJECT_ROOT / "automation_chrome_profile"
        options.add_argument(f"--user-data-dir={profile_path}")
        self.logger.info(f"Using dedicated Chrome profile: {profile_path}")

        # --- ADDING YOUR SUGGESTED OPTIONS TO SUPPRESS POPUPS ---
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        options.add_experimental_option("prefs", prefs)

        if headless:
            options.add_argument('--headless')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-renderer-backgrounding')
        options.page_load_strategy = "eager"  # Waits for DOMContentLoaded, not full resources

        service = ChromeService()
        driver = webdriver.Chrome(service=service, options=options)
        self.logger.info("Chrome WebDriver initialized with dedicated profile and popup suppression.")
        return driver

    def _setup_edge_driver(self, headless=False):
        """Sets up Edge WebDriver."""
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.page_load_strategy = "eager"  # Waits for DOMContentLoaded, not full resources

        service = EdgeService()
        driver = webdriver.Edge(service=service, options=options)
        self.logger.info("Edge WebDriver initialized successfully.")
        return driver

    def _capture_allure_screenshot(self, request):
        """Captures a unique, timestamped screenshot for the Allure report."""
        test_name = request.node.name
        self.logger.error(f"Test '{test_name}' failed. Capturing Allure screenshot.")

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        # Use the PROJECT_ROOT constant to build the absolute path
        screenshot_folder = PROJECT_ROOT / "reports" / "screenshots"
        screenshot_folder.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_folder / f"failed_{test_name}_{timestamp}.png"

        try:
            time.sleep(1) # Short delay before screenshot
            self.driver.save_screenshot(str(screenshot_path))
            allure.attach.file(str(screenshot_path), name=f"Failure Screenshot: {test_name}",
                             attachment_type=allure.attachment_type.PNG)
            self.logger.info(f"Screenshot for Allure saved to: {screenshot_path}")
        except Exception as e:
            self.logger.error(f"Failed to capture Allure screenshot: {e}")