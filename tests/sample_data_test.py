# tests/sample_data_test.py
import pytest
import allure

# Import the helper functions from your utility file
from utils.data_providers import get_all_test_data, get_filtered_test_data

# tests/sample_data_test.py (The Consumer / Your Test)
# Purpose: This is an example of a clean test file that uses the library. It doesn't know how the data is read; it just asks for it and runs the tests. You will use this pattern to build your main test_employeelogin and other test files.
# Analogy: This is the driver of the car, focused only on the journey (the test logic).

# --- Test Setup ---
# Define the source of our data here
WORKBOOK = "TestData_AppName.xlsx"
SHEET = "GAURANTEEDASSUREDINCOME"

# --- Test 1: Runs for ALL rows ---

@pytest.mark.parametrize("data_row", get_all_test_data(WORKBOOK, SHEET))
def test_each_row_from_excel(data_row):
    """
    This test will be executed once for each row in the Excel sheet.
    """
    test_case_id = data_row.get("TESTCASE_ID", "Unknown_ID")

    with allure.step(f"Running test for {test_case_id}"):
        print(f"\n--- Executing for {test_case_id} ---")
        print(f"Received Data: {data_row}")

        assert test_case_id != "Unknown_ID" and test_case_id is not None, "TESTCASE_ID should not be empty"
        assert data_row.get(
            "FIRST_NAME") == "Harsha", f"Expected FIRST_NAME to be 'Harsha' but got {data_row.get('FIRST_NAME')}"


# --- Test 2: Runs for ONLY ONE filtered row ---
# This function is now defined separately at the main level of the file.

@pytest.mark.parametrize("data_row", get_filtered_test_data(WORKBOOK, SHEET, "TESTCASE_ID", "TC_001"))
def test_single_row_from_excel(data_row):
    """
    This test will only be executed for the row where TESTCASE_ID is 'TC_001'.
    """
    test_case_id = data_row.get("TESTCASE_ID")

    with allure.step(f"Running specific test for {test_case_id}"):
        print(f"\n--- Executing ONLY for {test_case_id} ---")
        print(f"Received Filtered Data: {data_row}")

        # Assert that the filter worked correctly
        assert test_case_id == "TC_001"
        assert str(data_row.get("PR_AGE")) == "37"