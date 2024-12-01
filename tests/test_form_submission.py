import logging
from typing import Any, Dict

import pytest

from page_objects.home_page import HomePage
from utils.test_utilities import TestUtilities


class TestFormSubmission(TestUtilities):
    """
    Test class for validating form submissions on the homepage.
    """

    @pytest.mark.parametrize(
        "test_data", TestUtilities.load_test_data("form_submission.json")
    )
    def test_form_submission(self, test_data: Dict[str, Any]):
        """
        Validates the form submission process using parameterized test data.

        :param test_data: A dictionary containing the test data for form fields.
        """
        logger: logging.Logger = self.create_logger()
        home_page: HomePage = HomePage(self.driver)
        logger.info(f"Starting form submission test with data: {test_data}")

        # Fill out the form
        home_page.fill_out_form(test_data)

        # Validate success message
        actual_message: str = home_page.get_success_message()
        logger.info(f"Alert message: {actual_message}")
        expected_message: str = "The Form has been submitted successfully"
        assert (
            expected_message in actual_message
        ), f"Expected '{expected_message}' but got '{actual_message}' for {test_data['name']}"

        # Refresh the page to reset the form
        self.driver.refresh()
