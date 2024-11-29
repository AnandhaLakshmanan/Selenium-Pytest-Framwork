from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from page_objects.shopping_page import ShoppingPage
from page_objects.base_page import BasePage


class HomePage(BasePage):
    """
    Represents the Home Page of the application, providing methods to interact
    with various web elements and perform actions.
    """

    # Locators
    SHOP_LINK = (By.LINK_TEXT, "Shop")
    NAME_FIELD = (By.NAME, "name")
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.ID, "exampleInputPassword1")
    LIKES_ICE_CREAM_CHECKBOX = (By.ID, "exampleCheck1")
    GENDER_DROPDOWN = (By.CSS_SELECTOR, "#exampleFormControlSelect1")
    DOB_FIELD = (By.NAME, "bday")
    SUBMIT_BUTTON = (By.XPATH, "//input[@type='submit']")
    SUCCESS_MESSAGE_ALERT = (By.CLASS_NAME, "alert-success")

    EMPLOYMENT_STATUS_RADIOS = {
        "Student": "inlineRadio1",
        "Employed": "inlineRadio2",
        "Entrepreneur": "inlineRadio3",
    }

    def __init__(self, driver: WebDriver):
        """
        Initializes the HomePage class & assigns a driver instance variable.

        :param driver: WebDriver instance used to interact with the page.
        """
        super().__init__(driver)

    def navigate_to_shop_page(self) -> ShoppingPage:
        """
        Navigates to the Shop page.

        :return: An instance of the ShopPage class.
        """
        self.driver.find_element(*self.SHOP_LINK).click()
        return ShoppingPage(self.driver)

    def set_name(self, name: str) -> None:
        """
        Enters a name into the name input field.

        :param name: The name to be entered.
        """
        self.driver.find_element(*self.NAME_FIELD).send_keys(name)

    def set_email(self, email: str) -> None:
        """
        Enters an email into the email input field.

        :param email: The email to be entered.
        """
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)

    def set_password(self, password: str) -> None:
        """
        Enters a password into the password input field.

        :param password: The password to be entered.
        """
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def tick_ice_cream_checkbox(self) -> None:
        """
        Ticks the 'Likes Ice Cream'
        """
        self.driver.find_element(*self.LIKES_ICE_CREAM_CHECKBOX).click()

    def select_employment_status(self, status: str) -> None:
        """
        Selects an employment status radio button.

        :param status: The employment status to select (e.g., "Student", "Employed", "Entrepreneur").
        """
        if status not in self.EMPLOYMENT_STATUS_RADIOS:
            raise ValueError(f"Invalid employment status: {status}")

        radio_button = self.driver.find_element(By.ID, self.EMPLOYMENT_STATUS_RADIOS[status])
        if radio_button.is_enabled():
            radio_button.click()
        else:
            raise Exception(f"Radio button for {status} is disabled")

    def select_gender(self, gender: str) -> None:
        """
        Selects a gender from the dropdown.

        :param gender: The gender to select (e.g., "Male", "Female").
        """
        dropdown = self.driver.find_element(*self.GENDER_DROPDOWN)
        self.select_option_from_static_dropdown_by_text(dropdown, gender)

    def set_date_of_birth(self, dob: str) -> None:
        """
        Enters a date of birth into the DOB field.

        :param dob: The date of birth in format (e.g., "01-01-2000").
        """
        self.driver.find_element(*self.DOB_FIELD).send_keys(dob)

    def click_submit_button(self) -> None:
        """
        Clicks the submit button on the form.
        """
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_success_message(self) -> str:
        """
        Retrieves the success message displayed after form submission.

        :return: success message
        """
        return self.driver.find_element(*self.SUCCESS_MESSAGE_ALERT).text

    def fill_out_form(self, test_data: dict) -> None:
        """
        Completes the entire form with the provided details.

        :param test_data: A dictionary containing the following keys:
                          - name: str
                          - email: str
                          - password: str
                          - likes_ice_cream: bool
                          - gender: str
                          - employment_status: str
                          - dob: str
        """
        self.set_name(test_data["name"])
        self.set_email(test_data["email"])
        self.set_password(test_data["password"])
        if test_data["likes_ice_cream"]:
            self.tick_ice_cream_checkbox()
        self.select_gender(test_data["gender"])
        self.select_employment_status(test_data["employment_status"])
        self.set_date_of_birth(test_data["dob"])
        self.click_submit_button()
