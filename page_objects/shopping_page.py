from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List
from page_objects.base_page import BasePage
from page_objects.checkout_page import CheckoutPage


class ShoppingPage(BasePage):
    """
    Represents the shopping page of the application. Provides methods to interact
    with product elements, add products to the cart, and proceed to checkout.
    """
    # Locators
    PRODUCT_CARDS = (By.XPATH, "//app-card/div")
    PRODUCT_NAME = (By.XPATH, "div[@class='card-body']/h4")
    ADD_TO_CART_BUTTON = (By.XPATH, "div[@class='card-footer']/button")
    CHECKOUT_BUTTON = (By.XPATH, "//a[@class='nav-link btn btn-primary']")

    def __init__(self, driver: WebDriver):
        """
        Initializes the ShopPage class.

        :param driver: WebDriver instance used to interact with the page.
        """
        super().__init__(driver)

    def get_all_products(self) -> List[WebElement]:
        """
        Retrieves all product cards on the shop page.

        :return: A list of WebElement objects representing the product cards.
        """
        return self.driver.find_elements(*self.PRODUCT_CARDS)

    def get_product_name(self, product: WebElement) -> str:
        """
        Retrieves the name of a specific product.

        :param product: The WebElement representing the product card.
        :return: The name of the product as a string.
        """
        return product.find_element(*self.PRODUCT_NAME).text

    def add_product_to_cart(self, product: WebElement) -> None:
        """
        Clicks the 'Add to Cart' button for a specific product.

        :param product: The WebElement representing the product card.
        """
        product.find_element(*self.ADD_TO_CART_BUTTON).click()

    def find_and_add_product_to_cart(self, product_name: str) -> bool:
        """
        Finds a specific product by name and clicks the 'Add to Cart' button.

        :param product_name: The name of the product to add to the cart.
        :return: True if the product was found and added to the cart, False otherwise.
        """
        all_products = self.get_all_products()
        for product in all_products:
            if self.get_product_name(product) == product_name:
                self.add_product_to_cart(product)
                return True
        return False

    def click_checkout(self) -> CheckoutPage:
        """
        Clicks the checkout button to proceed to the next page.
        """
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()
        return CheckoutPage(self.driver)
