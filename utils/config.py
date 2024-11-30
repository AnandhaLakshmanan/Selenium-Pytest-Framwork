
import os
from pathlib import Path

# Test Website URL
URL = "https://rahulshettyacademy.com/angularpractice/"

# Base directory of the project
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Test data directory, configurable via environment variable
TEST_DATA_DIR: Path = Path(os.getenv("TEST_DATA_DIR", BASE_DIR / "test_data"))

# Temporary directories for logs, screenshots, reports
BASE_TMP_DIR: Path = BASE_DIR / "tmp"
LOG_DIR: Path = BASE_TMP_DIR / "logs"
SCREENSHOT_DIR: Path = BASE_TMP_DIR / "screenshots"
REPORT_DIR: Path = BASE_TMP_DIR / "reports"
