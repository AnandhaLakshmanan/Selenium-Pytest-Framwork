import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.checkout_page import CheckoutPage
from page_objects.home_page import HomePage
from utils.base_class import BaseClass


class TestEndToEnd(BaseClass):

    def test_end_to_end(self):
        logger = self.get_logger()

        home_page = HomePage(self.driver)

        logger.info("Getting products")
        checkout_page = home_page.shop_items()
        product_to_buy = "Blackberry"
        products = checkout_page.get_products()
        for product in products:
            product_name = checkout_page.get_product_name(product).text
            logger.info(f"product name: {product_name}")
            if product_name == product_to_buy:
                checkout_page.add_product_to_cart(product).click()
        checkout_page.click_checkout_button().click()

        confirm_page = checkout_page.click_checkout_again()
        logger.info("Entering country name")
        confirm_page.country_name().send_keys("ind")
        self.wait_till_element_is_located((By.LINK_TEXT, "India"))
        confirm_page.select_country().click()
        confirm_page.accept_t_and_c().click()
        confirm_page.select_purchase().click()
        self.wait_till_element_is_located((By.CSS_SELECTOR, ".alert-success"))
        actual_message = confirm_page.get_success_message().text
        logger.info(f"Text on site: {actual_message}")
        assert "Success" in actual_message, f"not getting success message"
