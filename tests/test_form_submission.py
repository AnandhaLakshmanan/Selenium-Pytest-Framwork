import json
import logging
import os

import pytest
from page_objects.home_page import HomePage
from utils.base_class import BaseClass
from typing import List, Dict, Any


def load_test_data(file_name: str) -> List[Dict[str, Any]]:
    """
    Loads test data from a JSON file located in the 'test_data' directory.

    :param file_name: Name of the JSON file to load.
    :return: Parsed JSON content as a Python object.
    :raises Exception: If the file is not found or has invalid JSON.
    """
    try:
        # Construct the file path relative to the 'test_data' folder
        data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data")
        file_path = os.path.join(data_folder, file_name)
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"Test data file '{file_name}' not found in 'test_data' directory.")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON format in file '{file_name}'.")


class TestFormSubmission(BaseClass):
    """
    Test class for validating form submissions on the homepage.
    """

    @pytest.mark.parametrize("test_data", load_test_data("form_submission.json"))
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
        assert expected_message in actual_message, \
            f"Expected '{expected_message}' but got '{actual_message}' for {test_data['name']}"

        # Refresh the page to reset the form
        self.driver.refresh()
