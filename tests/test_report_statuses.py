# tests/test_report_statuses.py
import pytest
import allure
from tests.base_test import BaseTest  # Make sure this import path is correct for your structure


@allure.epic("Framework Verification")
@allure.feature("Reporting")
class TestReportStatuses(BaseTest):
    """
    A test class to demonstrate and verify Allure reporting for different test outcomes.
    """

    @allure.story("Passing Test Scenario")
    @allure.title("Test to verify a successful execution")
    def test_pass_scenario(self):
        """
        This test should always pass.
        It navigates to a known page and checks the title.
        """
        with allure.step("Navigate to Google and verify title"):
            self.logger.info("Navigating to https://www.google.com")
            self.driver.get("https://www.google.com")

            self.logger.info("Asserting that the title contains 'Google'")
            assert "Google" in self.driver.title, "The title should contain 'Google'"

        self.logger.info("Pass scenario test completed successfully.")

    @allure.story("Failing Test Scenario")
    @allure.title("Test to verify failure evidence capture")
    def test_fail_scenario(self):
        """
        This test is designed to fail to verify screenshot and log attachment.
        It navigates to a page and asserts an incorrect title.
        """
        with allure.step("Navigate to Google and assert an incorrect title to force a failure"):
            self.logger.info("Navigating to https://www.google.com")
            self.driver.get("https://www.google.com")

            self.logger.error("This assertion will fail, triggering failure evidence capture.")
            assert "SomethingWrong" in self.driver.title, "This assertion is designed to fail"

    @allure.story("Skipped Test Scenario")
    @allure.title("Test to verify skipped test reporting")
    def test_skip_scenario(self):
        """
        This test will be skipped to verify how skipped tests are reported.
        """
        with allure.step("Intentionally skipping this test"):
            self.logger.warning("This test is being intentionally skipped.")
            pytest.skip("Skipping this test as part of the demonstration.")