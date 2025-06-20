# tests/test_logging_only.py
import allure
from utils.logger import get_logger

# Get the logger instance. It's already been configured by the fixture in conftest.py
# before this test even starts.
logger = get_logger()

@allure.story("Framework Utilities")
@allure.feature("Logging")
def test_log_messages():
    """
    A simple test to verify that the logging setup is working correctly.
    It does not use BaseTest and does not launch a browser.
    """
    with allure.step("Log messages at various levels"):
        logger.info("This is an informational message.")
        logger.debug("This is a detailed debug message for tracing.")
        logger.warning("This is a warning message about a potential issue.")
        logger.error("This is an error message indicating something failed.")
        logger.critical("This is a critical message for a major failure.")

    with allure.step("Verify test completion"):
        print("\nTest finished. Check console output and the 'logs' folder.")
        assert True