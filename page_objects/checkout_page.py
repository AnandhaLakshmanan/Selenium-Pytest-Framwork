from selenium.webdriver.common.by import By

from page_objects.order_confirmation_page import ConfirmPage


class CheckoutPage:
    products = (By.XPATH, "//app-card/div")
    product_name = (By.XPATH, "div[@class='card-body']/h4")
    product_name_full_path = (By.XPATH, "//app-card/div/div[@class='card-body']/h4")
    add_to_cart = (By.XPATH, "div[@class='card-footer']/button")
    checkout = (By.XPATH, "//a[@class='nav-link btn btn-primary']")
    checkout_to_purchase = (By.CSS_SELECTOR, ".btn.btn-success")

    def __init__(self, driver):
        self.driver = driver

    def get_products(self):
        return self.driver.find_elements(*CheckoutPage.products)

    def get_product_name(self, product):
        # return self.driver.find_element(*CheckoutPage.product_name_full_path)
        return product.find_element(*CheckoutPage.product_name)

    def add_product_to_cart(self, product):
        return product.find_element(*CheckoutPage.add_to_cart)

    def click_checkout_button(self):
        return self.driver.find_element(*CheckoutPage.checkout)

    def click_checkout_again(self):
        self.driver.find_element(*CheckoutPage.checkout_to_purchase).click()
        confirm_page = ConfirmPage(self.driver)
        return confirm_page
