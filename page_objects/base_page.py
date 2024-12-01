from typing import Tuple

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    """
    Base class for all page objects. Provides common utility methods for interacting with web elements
    and waiting for conditions.
    """

    def __init__(self, driver: WebDriver):
        """
        Initializes the BasePage class with a WebDriver instance.

        :param driver: WebDriver instance used to interact with the web page.
        """
        self.driver = driver

    @staticmethod
    def select_option_from_static_dropdown_by_text(
        element: WebElement, text: str
    ) -> None:
        """
        Selects an option from a static dropdown menu by its visible text.

        :param element: The WebElement representing the dropdown menu.
        :param text: The visible text of the option to select.
        """
        Select(element).select_by_visible_text(text)

    def wait_for_element_to_be_present(
        self, locator: Tuple[str, str], timeout: int = 10
    ) -> WebElement:
        """
        Waits until an element is present in the DOM and returns it.

        :param locator: A tuple containing the locator strategy and value (e.g., (By.ID, "example")).
        :param timeout: Maximum time to wait for the element (default: 10 seconds).
        :return: The WebElement once it is located.
        """
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator)
        )
