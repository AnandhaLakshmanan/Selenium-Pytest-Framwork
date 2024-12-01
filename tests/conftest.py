from datetime import datetime
from pathlib import Path
from typing import Any, Generator, List, Optional

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.config import LOG_DIR, REPORT_DIR, SCREENSHOT_DIR, URL


@pytest.fixture(scope="session", autouse=True)
def create_directories() -> None:
    """
    Ensure the required directories (logs, screenshots, reports) are created before tests run.
    This fixture runs once per session and creates directories if they don't exist already.
    """
    for directory in [LOG_DIR, SCREENSHOT_DIR, REPORT_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add custom command-line options for pytest.

    :param parser: The pytest parser to add custom options to.
    """
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="Specify the browser to use",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=None,
        help="Run tests in headless mode",
    )


def pytest_html_report_title(report: pytest.TestReport) -> None:
    """
    Set the title of the HTML report.

    :param report: The report object to modify the title.
    """
    report.title = "Selenium Test Automation Summary"  # type: ignore


@pytest.fixture(scope="class")
def setup(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    """
    Set up the browser and start the test session.

    :param request: The pytest fixture request object containing the test's configuration.
    """
    browser_name: str = request.config.getoption("browser_name")
    headless: str = request.config.getoption("headless")
    driver: Optional[webdriver.Chrome | webdriver.Firefox] = None

    if browser_name == "chrome":
        chrome_service = ChromeService(ChromeDriverManager().install())
        chrome_options: ChromeOptions = ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    elif browser_name == "firefox":
        firefox_options: FirefoxOptions = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        firefox_options.add_argument("--window-size=1920,1080")
        firefox_service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    driver.get(URL)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item) -> Generator[None, None, None]:
    """
    Take a screenshot and attach it to the HTML report if the test fails.

    :param item: The pytest item (test) that is being executed.
    """
    pytest_html: Optional[Any] = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report: Optional[pytest.TestReport] = None
    if outcome:
        report = outcome.get_result()
    extras: List[Any] = getattr(report, "extras", []) if report else []

    # Proceed only if report is not None
    if report:
        if report.when == "call" or report.when == "setup":
            xfail = hasattr(report, "wasxfail")
            # Ensure the test failed or was expected to fail
            if (report.skipped and xfail) or (report.failed and not xfail):
                # Get the driver from the class level
                driver: Optional[webdriver.Remote] = getattr(item.cls, "driver", None)  # type: ignore
                if driver:
                    # Generate a unique file name using test name, status, and timestamp
                    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    test_case_name: str = report.nodeid.split("::")[-1]
                    file_name: str = f"{test_case_name}_failed_{timestamp}.png"
                    screenshot_path: Path = SCREENSHOT_DIR / file_name
                    # Take the screenshot
                    driver.save_screenshot(str(screenshot_path))
                    if screenshot_path.exists():
                        html = (
                            f'<div><img src="{screenshot_path}" alt="screenshot" style="width:304px;height:228px;" '
                            'onclick="window.open(this.src)" align="right"/></div>'
                        )
                        if pytest_html:
                            extras.append(pytest_html.extras.url(driver.current_url))
                            extras.append(pytest_html.extras.html(html))

            report.extras = extras  # type: ignore
