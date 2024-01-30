from ycombinator_scraper.config import Settings  # Replace 'your_settings_module' with the actual module name
from pathlib import Path
import pytest
import shutil

@pytest.fixture
def temp_logs_directory(tmp_path):
    logs_path = tmp_path / "logs"
    return logs_path

def test_create_logs_directory(temp_logs_directory):
    # Ensure the logs directory does not exist initially
    assert not temp_logs_directory.exists()

    # Use Settings.create_logs_directory to create the logs directory
    logs_directory_path = Settings.create_logs_directory()

    # Check if the logs directory is created
    assert logs_directory_path.exists()
    assert logs_directory_path.is_dir()

    # Verify that logs_directory_path is the expected path
    expected_path = Path.cwd() / "logs"
    assert logs_directory_path == expected_path

    # Clean up: Remove the created logs directory
    shutil.rmtree(logs_directory_path)
  
