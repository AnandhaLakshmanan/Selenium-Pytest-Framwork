import inspect
import json
import logging
from .config import TEST_DATA_DIR, LOG_DIR
from pathlib import Path
from typing import List, Dict, Any

import pytest


@pytest.mark.usefixtures("setup")
class TestUtilities:
    """
    A utility class for common test functionalities such as Webdriver & logging setup, test data management.
    """

    @staticmethod
    def create_logger() -> logging.Logger:
        """
        Sets up and returns a logger instance for the current test.

        :return: Configured logger object.
        """
        test_name: str = inspect.stack()[1][3]
        logger: logging.Logger = logging.getLogger(test_name)
        file_path: Path = LOG_DIR / "test_execution.log"

        if not logger.handlers:
            file_handler: logging.FileHandler = logging.FileHandler(file_path, mode="a")
            formatter: logging.Formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        logger.setLevel(logging.INFO)
        return logger

    @staticmethod
    def get_test_data_file_path(file_name: str) -> Path:
        """
        Get the full path to a test data file.

        :param file_name: Name of the file in the test_data directory.
        :return: Path object pointing to the file.
        """
        file_path: Path = TEST_DATA_DIR / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"File '{file_name}' not found in '{TEST_DATA_DIR}'.")
        return file_path

    @staticmethod
    def load_test_data(file_name: str) -> List[Dict[str, Any]]:
        """
        Loads test data from a JSON file located in the 'test_data' directory.

        :param file_name: Name of the JSON file to load.
        :return: Parsed JSON content as a Python object.
        :raises Exception: If the file is not found or has invalid JSON.
        """
        file_path: Path = TestUtilities.get_test_data_file_path(file_name)
        try:
            with file_path.open(mode="r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Test data file '{file_name}' not found in 'test_data' directory.")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON format in file '{file_name}'.")
