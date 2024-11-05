from selenium.webdriver.common.by import By

from page_objects.checkout_page import CheckoutPage


class HomePage:
    shop = (By.LINK_TEXT, "Shop")
    name = (By.NAME, "name")
    email = (By.NAME, "email")
    likes_ice_Cream = (By.ID, "exampleCheck1")
    gender = (By.CSS_SELECTOR, "#exampleFormControlSelect1")
    submit = (By.XPATH, "//input[@type='submit']")
    message = (By.CLASS_NAME, "alert-success")

    def __init__(self, driver):
        self.driver = driver

    def shop_items(self):
        self.driver.find_element(*HomePage.shop).click()
        checkout_page = CheckoutPage(self.driver)
        return checkout_page

    def get_name(self):
        return self.driver.find_element(*HomePage.name)

    def get_email(self):
        return self.driver.find_element(*HomePage.email)

    def get_likes_ice_cream_check_box(self):
        return self.driver.find_element(*HomePage.likes_ice_Cream)

    def get_gender(self):
        return self.driver.find_element(*HomePage.gender)

    def get_submit(self):
        return self.driver.find_element(*HomePage.submit)

    def get_message(self):
        return self.driver.find_element(*HomePage.message)
