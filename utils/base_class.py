import inspect
import logging
from pathlib import Path

import pytest


@pytest.mark.usefixtures("setup")
class BaseClass:
    @staticmethod
    def create_logger():
        """
        Sets up and returns a logger instance for the current test.

        :return: Configured logger object.
        """
        test_name = inspect.stack()[1][3]
        logger = logging.getLogger(test_name)
        log_file_path = Path("logs/test_execution.log")

        # Ensure the logs directory exists
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file_path, mode="a")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        file_handler.setFormatter(formatter)

        if not logger.handlers:
            logger.addHandler(file_handler)

        logger.setLevel(logging.INFO)
        return logger
