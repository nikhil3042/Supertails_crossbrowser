# Professional Python Test Automation Framework

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-4.15%2B-green.svg)](https://selenium.dev)
[![Pytest](https://img.shields.io/badge/Pytest-7.4%2B-orange.svg)](https://pytest.org)
[![Allure](https://img.shields.io/badge/Allure-2.13%2B-purple.svg)](https://docs.qameta.io/allure/)

A robust and scalable UI test automation framework built with Python. This framework demonstrates a professional-grade architecture incorporating the Page Object Model, data-driven testing, advanced logging, and rich, multi-format reporting.

---

## ✨ Key Features

### 🏗️ **Architecture & Design Patterns**
- **Page Object Model (POM):** Clean separation of UI elements (`Pages`) and test logic (`Tests`)
- **Centralized `BasePage`:** Contains reusable, robust UI actions with smart waiting mechanisms
- **`BaseTest` Class:** Manages common test setup and teardown, including browser lifecycle and failure capture
- **Modular & Scalable Structure:** Organized into distinct packages for configuration, data, pages, reports, tests, and utilities

### 📊 **Data-Driven Testing**
- **Excel Integration:** Powered by a custom `ExcelDataProvider` for reading and filtering data from `.xlsx` files
- **Advanced Data Filtering:** Supports SQL-like filtering for single or multiple `AND` conditions
- **Parameterized Tests:** Dynamically generates test cases based on data from Excel

### 🌍 **Multi-Environment Support**
- **Dynamic Environment Management:** Easily switch test execution between different environments (`demo`, `dev`, `staging`) using an environment variable
- **YAML Configuration:** All environment details (URLs, credentials) are managed in a clean `config.yaml` file

### 📝 **Advanced Logging**
- **Timestamped Log Directories:** Automatically creates a unique, timestamped folder for each test run
- **Rich Log Format:** Logs include timestamp, filename, and line number for precise debugging
- **Colored Console Output:** Uses `colorlog` for enhanced readability of log levels in the console

### 📈 **Comprehensive Reporting**
- **Allure Reports:** Generates detailed, interactive HTML reports
  - **Automatic Attachments:** Captures and attaches screenshots and test-specific logs on failure
  - **Environment Details:** Displays browser, platform, and URL on the report dashboard
- **`pytest-html` Reports:** Generates a simple, self-contained `.html` report with screenshots embedded on failure

### 🔧 **Automation Features**
- **Automatic WebDriver Management:** Utilizes Selenium Manager to seamlessly download and manage browser drivers
- **Designed for Cross-Browser Support:** Framework is structured to easily extend testing to Firefox, Edge, etc.
- **Parallel Execution Ready:** Supports concurrent test execution via `pytest-xdist` (tests must be independent)

---

## 🛠️ Technology Stack

| Component               | Technology    | Purpose                              |
|-------------------------|---------------|--------------------------------------|
| **Language**            | Python 3.10+  | Core programming language            |
| **Test Runner**         | Pytest        | Test execution and framework         |
| **Browser Automation**  | Selenium      | Web UI interaction                   |
| **Reporting**           | Allure Report | Primary interactive reporting        |
| **Secondary Reporting** | pytest-html   | Self-contained HTML reports          |
| **Data Processing**     | openpyxl      | Excel file reading and manipulation  |
| **Logging**             | colorlog      | Enhanced console logging             |
| **Configuration**       | PyYAML        | Environment configuration management |

---

## 📂 Project Structure

```
Your_Project_Name/
├── 📁 config/                    # Environment configuration management
│   ├── config.yaml               # Multi-environment settings
│   └── environment.py            # Environment configuration handler
│
├── 📁 data/                      # Test data files (place your .xlsx files here)
│   └── TestData_AppName.xlsx     # Example test data file
│
├── 📁 logs/                      # Generated log files
│   └── logs_DD_MM_YYYY_HHMMSS/   # Timestamped folders (auto-created)
│
├── 📁 pages/                     # Page Object Model classes
│   ├── base_page.py              # Reusable UI actions and utilities
│   ├── login_page.py             # Example login page object
│   └── __init__.py               # Package initialization
│
├── 📁 reports/                   # Test execution reports
│   ├── allure-results/           # Raw Allure data (auto-generated)
│   ├── screenshots/              # Failure screenshots (auto-captured)
│   └── html_report.html          # pytest-html report
│
├── 📁 tests/                     # Test scripts and framework setup
│   ├── conftest.py               # Pytest fixtures and hooks
│   ├── base_test.py              # Base test class with setup/teardown
│   ├── test_login.py             # Example test implementation
│   └── __init__.py               # Package initialization
│
├── 📁 utils/                     # Reusable utility modules
│   ├── excel_provider.py         # Excel data reading and filtering
│   ├── data_providers.py         # Bridge functions for parametrization
│   └── logger.py                 # Logging configuration utility
│
├── 📄 pytest.ini                 # Pytest configuration file
├── 📄 requirements.txt           # Python package dependencies
└── 📄 README.md                  # Project documentation


---

## 🏗️ Framework Architecture

This diagram provides a high-level visual overview of the framework's components and their relationships.

![Framework Architecture Diagram](docs_images/framework_architecture.png)

---

---

## 📜 Coding Standards & Best Practices

To ensure consistency, readability, and maintainability across the project, we follow a detailed set of coding standards and best practices. These guidelines cover everything from naming conventions to error handling and Page Object design.

➡️ **[Read the Full Coding Standards Guide](CODING_STANDARDS.md)**

---
---

## 🚀 Setup and Installation

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.10 or higher** - [Download Python](https://python.org)
- **pip** - Python package installer (typically comes with Python)
- **Allure Commandline Tool** - Required for generating HTML reports
  - 📋 [Installation Guide](https://docs.qameta.io/allure/#_installing_a_commandline)

### Installation Guide

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd Your_Project_Name/
   ```

2. **Create and Activate a Virtual Environment** *(Highly Recommended)*
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   pytest --version
   allure --version
   ```

---

## ▶️ Execution Guide

> **Important:** Always run commands from the **project root directory**. Your `pytest.ini` file automates most of the configuration.

### Running Tests

#### Basic Test Execution
```bash
# Run all tests using the default environment (dev)
pytest

# Run specific test file
pytest tests/test_login.py

# Run tests with specific marker
pytest -m smoke

# Run tests with verbose output
pytest -v
```

#### Environment-Specific Execution
```bash
# Windows PowerShell
$env:ENV="staging"; pytest

# macOS/Linux
ENV=staging pytest

# Windows Command Prompt
set ENV=staging && pytest
```

#### Advanced Execution Options
```bash
# Run tests in parallel
pytest -n 4

# Run with live logging
pytest -s

# Run specific test method
pytest tests/test_login.py::TestLogin::test_successful_login

# Run with custom markers
pytest -m "smoke and critical"
```

### Generating and Viewing Reports

The framework generates two types of reports automatically:

#### Allure Report *(Primary)*
Allure provides the most detailed, interactive report. The raw data is generated automatically by pytest.

```bash
# Generate and view the report in a browser
allure serve reports/allure-results

# Generate static HTML report
allure generate reports/allure-results --clean -o reports/allure-html
```

#### pytest-html Report *(Secondary)*
A simple, self-contained HTML file is also generated automatically. You can find it at `reports/html_report.html`.

---

## 📋 Usage Examples

### Data-Driven Test with Excel

This example shows how to run a test for every row in an Excel sheet:

```python
# In your test file (e.g., tests/sample_data_test.py)

from utils.data_providers import get_all_test_data

# Define the data source
WORKBOOK = "TestData_AppName.xlsx"
SHEET = "YourSheetName"

@pytest.mark.parametrize("data_row", get_all_test_data(WORKBOOK, SHEET))
def test_example(data_row):
    """This test runs for each row from the Excel sheet."""
    test_case_id = data_row.get("TESTCASE_ID")
    print(f"Running test for {test_case_id}")
    
    # Your test logic here
    assert data_row is not None
```

### Advanced Data Filtering

```python
# Filter data based on specific criteria
@pytest.mark.parametrize("data_row", 
    get_filtered_test_data(WORKBOOK, SHEET, "EXECUTION_FLAG", "Yes"))
def test_filtered_data(data_row):
    """Run tests only for rows where EXECUTION_FLAG = 'Yes'."""
    # Test implementation
    pass
```

### Page Object Implementation

Page objects should inherit from `BasePage` to use its reusable methods:

```python
# In pages/login_page.py

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure

class LoginPage(BasePage):
    """Login page object with locators and actions."""

    # --- Locators ---
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")

    # --- Actions ---
    @allure.step("Login with credentials")
    def login(self, username: str, password: str):
        """Enters credentials and clicks login."""
        self.send_keys(self.USERNAME_FIELD, username)
        self.send_keys(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Check if login was successful")
    def is_login_successful(self) -> bool:
        """Verify if login was successful."""
        return not self.is_visible(self.ERROR_MESSAGE)
```

### Test Implementation Example

```python
# In tests/test_login.py

import pytest
import allure
from tests.base_test import BaseTest
from pages.login_page import LoginPage
from utils.data_providers import get_login_test_data

@allure.feature("Authentication")
class TestLogin(BaseTest):
    """Test class for login functionality."""
    
    @allure.story("Valid Login")
    @pytest.mark.smoke
    @pytest.mark.parametrize("test_data", get_login_test_data())
    def test_successful_login(self, test_data):
        """Test successful login with valid credentials."""
        
        # Arrange
        login_page = LoginPage(self.driver)
        username = test_data["USERNAME"]
        password = test_data["PASSWORD"]
        
        # Act
        login_page.navigate_to_login()
        login_page.login(username, password)
        
        # Assert
        assert login_page.is_login_successful()
```

---

## 🧪 Best Practices

### Test Organization
- ✅ Use descriptive test names that explain the scenario
- ✅ Follow AAA pattern (Arrange, Act, Assert)
- ✅ Keep tests independent and isolated
- ✅ Use appropriate test markers for categorization

### Page Object Guidelines
- ✅ One page object per web page or component
- ✅ Use descriptive method names for actions
- ✅ Separate locators from actions
- ✅ Return page objects for method chaining where appropriate

### Data Management
- ✅ Store test data in Excel files within the `data/` directory
- ✅ Use meaningful column headers
- ✅ Separate positive and negative test scenarios
- ✅ Keep test data version controlled

### Reporting and Logging
- ✅ Use `@allure.step()` decorators for detailed reporting
- ✅ Add screenshots and logs for debugging failures
- ✅ Include environment information in reports
- ✅ Use meaningful test descriptions and titles

---

## 🔧 Troubleshooting

### Common Issues

#### WebDriver Issues
```bash
# Update Selenium to get the latest WebDriver management
pip install --upgrade selenium

# Clear WebDriver cache if needed
selenium-manager --clear-cache
```

#### Import Errors
```bash
# Ensure you're in the project root directory
pwd  # or cd on Windows

# Verify virtual environment is activated
which python  # or where python on Windows

# Reinstall dependencies if needed
pip install -r requirements.txt
```

#### Report Generation Issues
```bash
# Verify Allure installation
allure --version

# Clean previous results
rm -rf reports/allure-results/*  # or del on Windows

# Regenerate reports
pytest
allure serve reports/allure-results
```

### Debug Mode

```bash
# Run with detailed traceback information
pytest --tb=long

# Run a single test with live console output (disables capturing)
pytest tests/test_login.py::TestLogin::test_successful_login -v -s

# Run with debug logging
pytest --log-cli-level=DEBUG
```

### Performance Optimization

```bash
# Run tests in parallel (adjust number based on your system)
pytest -n 4

# Run only failed tests from last run
pytest --lf

# Run tests that failed or passed in the last run
pytest --ff
```

---

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies
4. Make your changes
5. Run tests and ensure they pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all public methods
- Write unit tests for new utilities
- Update documentation for new features
- Use type hints where appropriate

---

## 📚 Additional Resources

- 📖 [Selenium Documentation](https://selenium-python.readthedocs.io/)
- 📖 [Pytest Documentation](https://docs.pytest.org/)
- 📖 [Allure Documentation](https://docs.qameta.io/allure/)
- 📖 [Page Object Model Guide](https://selenium-python.readthedocs.io/page-objects.html)
- 📖 [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Support & Contact

For questions, issues, or contributions:

- 📧 **Email:** [your-email@example.com]
- 💬 **GitHub Issues:** [Create an Issue](../../issues)
- 📚 **Documentation:** [Wiki](../../wiki)
- 🐛 **Bug Reports:** Use the issue tracker with the bug label

---

**Built with ❤️ for robust and scalable test automation**