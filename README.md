# Test Automation Framework Using Selenium and Pytest
A robust and scalable test automation framework leveraging **Selenium** and **Pytest** to validate web applications. This framework follows best practices such as **Page Object Model (POM)** for maintaining code scalability, **data-driven testing** using JSON for form submissions, parameterized tests for running the same test case with different inputs, and type hinting to ensure code quality and readability. It specifically tests the functionality of the [Practice Application](https://rahulshettyacademy.com/angularpractice/).

## Key features
- **Page Object Model (POM)**: Ensures maintainable and scalable test scripts by encapsulating web elements and actions.
- **Data-Driven Testing**: Utilizes JSON files for managing test input data, enhancing flexibility and reducing redundancy.
- **Logging & Reporting**: Provides debug logs and HTML reports with screenshots for failed test cases.
- **Cross-Browser Testing**: Supports Firefox and Chrome, with automatic WebDriver management via an external library.
- **CI/CD Integration**: Automates test execution and uploads logs, reports, and screenshots as artifacts via GitHub Actions workflow.

## Prerequisites
- Python Installation: Ensure Python 3.12 is installed on your system. [Download Python](https://www.python.org/downloads/).
- Clone Repository:
```bash
git clone https://github.com/AnandhaLakshmanan/Selenium-Pytest-Framwork.git
cd Selenium-Pytest-Framwork
```
- Install Dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests
- Run All Tests
```bash
pytest tests/
```
- Run Specific Test Case
```bash
pytest tests/<test_file_name>::<test_class_name>::<test_case_name>
```
Check the ```tmp``` directory for logs, HTML reports, and screenshots of failed test cases.

## Configuration options
- Browser Selection:
  By default, tests run on Chrome. To use Firefox, run:
```
pytest --browser=firefox
```
- Headless Mode:
Disabled by default. Enable it for running tests in CI/CD environments:
```
pytest --headless
```
- HTML Reports:
Enabled by default. Modify or disable settings in the pytest.ini file.
