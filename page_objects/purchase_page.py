from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from page_objects.base_page import BasePage


class PurchasePage(BasePage):
    """
    Represents the purchase page of the application. Provides methods to handle
    delivery location input, accept terms and conditions, complete a purchase,
    and retrieve the success message.
    """

    # Locators
    DELIVERY_LOCATION_INPUT_BOX = (By.ID, "country")
    COUNTRY_OPTION = (By.LINK_TEXT, "India")
    TERMS_AND_CONDITIONS_CHECKBOX = (By.XPATH, "//label[@for='checkbox2']")
    PURCHASE_BUTTON = (By.CSS_SELECTOR, "input[value*='Pur']")
    SUCCESS_MESSAGE_ALERT = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver: WebDriver):
        """
        Initializes the PurchasePage class.

        :param driver: WebDriver instance used to interact with the page.
        """
        super().__init__(driver)

    def select_delivery_location(self, location: str) -> None:
        """
        Enters the delivery location in the input box and selects the corresponding country.

        :param location: The delivery location to be entered.
        """
        self.driver.find_element(*self.DELIVERY_LOCATION_INPUT_BOX).send_keys(location)
        self.wait_for_element_to_be_present(self.COUNTRY_OPTION).click()

    def accept_terms_and_conditions(self) -> None:
        """
        Accepts the terms and conditions by selecting the checkbox.
        """
        terms_checkbox = self.driver.find_element(*self.TERMS_AND_CONDITIONS_CHECKBOX)
        if not terms_checkbox.is_selected():
            terms_checkbox.click()

    def complete_purchase(self) -> None:
        """
        Clicks the purchase button to finalize the order.
        """
        self.driver.find_element(*self.PURCHASE_BUTTON).click()

    def get_success_message(self) -> str:
        """
        Retrieves the success message displayed after completing a purchase.

        :return: The success message as a string.
        """
        return self.wait_for_element_to_be_present(self.SUCCESS_MESSAGE_ALERT).text
