from selenium.webdriver.common.by import By


class ConfirmPage:
    country_input_box = (By.ID, "country")
    country = (By.LINK_TEXT, "India")
    terms_and_conditions = (By.XPATH, "//label[@for='checkbox2']")
    purchase = (By.CSS_SELECTOR, "input[value*='Pur']")
    success_message = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver):
        self.driver = driver

    def country_name(self):
        return self.driver.find_element(*ConfirmPage.country_input_box)

    def select_country(self):
        return self.driver.find_element(*ConfirmPage.country)

    def accept_t_and_c(self):
        return  self.driver.find_element(*ConfirmPage.terms_and_conditions)

    def select_purchase(self):
        return self.driver.find_element(*ConfirmPage.purchase)

    def get_success_message(self):
        return self.driver.find_element(*ConfirmPage.success_message)
