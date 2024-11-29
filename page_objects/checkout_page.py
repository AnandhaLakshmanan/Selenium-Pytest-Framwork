from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from page_objects.purchase_page import PurchasePage
from page_objects.base_page import BasePage


class CheckoutPage(BasePage):
    """
    Represents the checkout page of the application. Provides methods to interact
    with checkout-related elements and navigate to the purchase page.
    """
    # Locators
    PROCEED_TO_PURCHASE_BUTTON = (By.CSS_SELECTOR, ".btn.btn-success")
    PRODUCTS_IN_CART = (By.XPATH, "//div/h4[@class='media-heading']")
    QUANTITY = (By.ID, "exampleInputEmail1")
    REMOVE_BUTTON = (By.XPATH, "ancestor::tr[1]/td[last()]/button")

    def __init__(self, driver: WebDriver):
        """
        Initializes the CheckoutPage class.

        :param driver: WebDriver instance used to interact with the page.
        """
        super().__init__(driver)

    def get_cart_items(self) -> List[WebElement]:
        """
        Retrieves products added to cart on checkout page

        :return: A list of WebElement objects representing the products.
        """
        return self.driver.find_elements(*self.PRODUCTS_IN_CART)

    def get_quantity(self) -> str:
        """
        Retrieves the current value of the quantity input field.

        :return: The quantity as a string.
        """
        return self.driver.find_element(*self.QUANTITY).get_attribute('value')

    def enter_quantity(self, quantity: int) -> None:
        """
        Clears and enters a new value into the quantity input field.

        :param quantity: The quantity to set as a string.
        """
        quantity_input_box = self.driver.find_element(*self.QUANTITY)
        quantity_input_box.clear()
        quantity_input_box.send_keys(str(quantity))

    def remove_product_from_cart(self, product: str) -> None:
        """
        Removes a specified product from the cart by clicking the corresponding remove button.

        :param product: The name of the product to remove from the cart.
        :raises ValueError: If the specified product is not found in the cart.
        """
        cart_items = self.get_cart_items()
        for item in cart_items:
            if item.text.strip() == product.strip():
                remove_button = item.find_element(*self.REMOVE_BUTTON)
                remove_button.click()
                return
        raise ValueError(f"Product '{product}' not found in the cart.")

    def proceed_to_purchase(self) -> PurchasePage:
        """
        Clicks the checkout button to proceed to the purchase page.

        :return: An instance of the PurchasePage class.
        """
        self.driver.find_element(*self.PROCEED_TO_PURCHASE_BUTTON).click()
        return PurchasePage(self.driver)
