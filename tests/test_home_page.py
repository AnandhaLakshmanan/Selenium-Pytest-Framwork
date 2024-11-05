import pytest
from page_objects.home_page import HomePage
from test_data.home_page_test_data import HomePageTestData
from utils.base_class import BaseClass


class TestHomePage(BaseClass):

    def test_form_submission(self, get_test_data):
        logger = self.get_logger()
        home_page = HomePage(self.driver)
        logger.info(f"first name input data: {get_test_data["name"]}")
        home_page.get_name().send_keys(get_test_data["name"])
        home_page.get_email().send_keys(get_test_data["email"])
        home_page.get_likes_ice_cream_check_box().click()
        self.select_from_static_dropdown_by_text(home_page.get_gender(), get_test_data["gender"])
        home_page.get_submit().click()
        message = home_page.get_message().text
        assert "Success" in message, "Not getting success message"
        self.driver.refresh()

    @pytest.fixture(params=HomePageTestData.get_test_data_from_excel("Testcase2"))
    #@pytest.fixture(params=HomePageTestData.test_home_page_data)
    def get_test_data(self, request):
        return request.param
