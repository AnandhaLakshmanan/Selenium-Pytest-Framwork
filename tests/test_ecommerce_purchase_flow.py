import logging
from typing import List

import pytest
from selenium.webdriver.remote.webelement import WebElement

from page_objects.home_page import HomePage
from page_objects.shopping_page import ShoppingPage
from page_objects.checkout_page import CheckoutPage
from page_objects.purchase_page import PurchasePage
from utils.test_utilities import TestUtilities


class TestECommercePurchaseFlow(TestUtilities):
    """
    Tests for the e-commerce purchase flow.
    """

    def test_add_two_products_and_verify_cart_items_in_checkout(self):
        """
        Verifies that two products can be added to the cart and checked out successfully.
        """
        logger: logging.Logger = self.create_logger()
        products_to_buy: List[str] = ["Nokia Edge", "Samsung Note 8"]

        # Navigate to shop page and add products
        shopping_page: ShoppingPage = self._navigate_to_shop_page(logger)
        self._add_products_to_cart(shopping_page, products_to_buy, logger)

        # Proceed to checkout and verify cart
        logger.info("Proceeding to checkout.")
        checkout_page: CheckoutPage = shopping_page.click_checkout()
        self._verify_cart_items(checkout_page, products_to_buy, logger)
        self.driver.refresh()

    def test_add_two_products_remove_one_and_verify_cart(self):
        """
        Verifies that one of two added products can be removed from the cart.
        """
        logger: logging.Logger = self.create_logger()
        products_to_buy: List[str] = ["Nokia Edge", "Blackberry"]
        product_to_remove: str = "Blackberry"

        # Navigate to shop page and add products
        shopping_page: ShoppingPage = self._navigate_to_shop_page(logger)
        self._add_products_to_cart(shopping_page, products_to_buy, logger)

        # Proceed to checkout and verify cart
        logger.info("Proceeding to checkout.")
        checkout_page: CheckoutPage = shopping_page.click_checkout()
        self._verify_cart_items(checkout_page, products_to_buy, logger)

        # Remove a product and verify the cart again
        logger.info(f"Removing product '{product_to_remove}' from the cart.")
        checkout_page.remove_product_from_cart(product_to_remove)

        # Verify the remaining cart
        remaining_products: List[str] = [product for product in products_to_buy if product != product_to_remove]
        self._verify_cart_items(checkout_page, remaining_products, logger)
        self.driver.refresh()

    @pytest.mark.parametrize("product_to_buy, quantity", [("Blackberry", 1), ("Blackberry", 2)])
    def test_product_purchase_flow(self, product_to_buy: str, quantity: int):
        """
        Verifies the successful purchase process for a specific product.

        :param product_to_buy: Name of the product to be purchased.
        :param quantity: Quantity of the product to purchase.
        """
        logger: logging.Logger = self.create_logger()

        # Constants
        country_code: str = "ind"
        expected_success_keyword: str = "Success"

        logger.info(f"Starting test for product '{product_to_buy}' with quantity {quantity}.")

        # Navigate to shop page and add product
        shopping_page: ShoppingPage = self._navigate_to_shop_page(logger)
        self._add_products_to_cart(shopping_page, [product_to_buy], logger)

        # Proceed to checkout
        logger.info("Proceeding to checkout.")
        checkout_page: CheckoutPage = shopping_page.click_checkout()
        self._verify_cart_items(checkout_page, [product_to_buy], logger)

        # Update quantity if applicable
        if quantity > 1:
            logger.info(f"Updating quantity to {quantity} for product '{product_to_buy}'.")
            checkout_page.enter_quantity(quantity)
        actual_quantity: int = int(checkout_page.get_quantity())
        assert actual_quantity == quantity, f"Expected quantity {quantity}, but got {actual_quantity}."

        # Complete the purchase
        purchase_page: PurchasePage = checkout_page.proceed_to_purchase()
        logger.info("Completing the purchase process.")
        purchase_page.select_delivery_location(country_code)
        purchase_page.accept_terms_and_conditions()
        purchase_page.complete_purchase()

        # Verify success message
        actual_message: str = purchase_page.get_success_message()
        logger.info(f"Purchase Alert message: {actual_message}")
        assert expected_success_keyword in actual_message, (
            f"Expected success message to contain '{expected_success_keyword}', but got: {actual_message}"
        )
        logger.info("Purchase successful. Test passed.")

        self.driver.refresh()

    def _navigate_to_shop_page(self, logger: logging.Logger):
        """
        Navigates to the shop page and returns the shopping page object.

        :param logger: Logger instance for logging the navigation step.
        :return: ShoppingPage instance.
        """
        home_page: HomePage = HomePage(self.driver)
        logger.info("Navigating to the shop page.")
        return home_page.navigate_to_shop_page()

    @staticmethod
    def _add_products_to_cart(shopping_page, products: List[str], logger: logging.Logger):
        """
        Adds a list of products to the cart.

        :param shopping_page: The shopping page object.
        :param products: List of product names to add to the cart.
        :param logger: Logger instance for logging the addition process.
        """
        for product in products:
            assert shopping_page.find_and_add_product_to_cart(product), (
                f"Product '{product}' not found on the shop page."
            )
            logger.info(f"Added '{product}' to the cart.")

    @staticmethod
    def _verify_cart_items(checkout_page: CheckoutPage, expected_products: List[str], logger: logging.Logger):
        """
        Verifies the cart contains the expected products.

        :param checkout_page: The checkout page object.
        :param expected_products: List of expected product names.
        :param logger: Logger instance for logging the verification process.
        """
        cart_items: List[WebElement] = checkout_page.get_cart_items()
        assert len(cart_items) == len(expected_products), (
            f"Expected {len(expected_products)} products in cart but got: {len(cart_items)}"
        )
        cart_item_names: List[str] = [item.text for item in cart_items]
        assert sorted(cart_item_names) == sorted(expected_products), (
            f"Cart items mismatch. Expected {expected_products}, but got {cart_item_names}."
        )
        logger.info("Cart items verified successfully.")
