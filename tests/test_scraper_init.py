import pickle
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from ycombinator_scraper.scraper import Scraper
import pytest

@pytest.fixture
def scraper_instance():
    return Scraper()

def test_initialize_driver(scraper_instance):
    driver = scraper_instance.initialize_driver()

    # Check if the returned object is an instance of webdriver.Chrome
    assert isinstance(driver, webdriver.Chrome)

    # Verify that headless mode options are set
    assert any(arg.startswith("--headless") for arg in driver.capabilities['goog:chromeOptions']['args'])

def test_load_cookies(scraper_instance, tmp_path):
    # Create a temporary directory for testing
    temp_dir = tmp_path / "test_data"
    temp_dir.mkdir()

    # Create a sample cookies file with dummy data
    cookies_path = temp_dir / "cookies.pkl"
    dummy_cookies = [{"name": "test_cookie", "value": "test_value"}]
    with open(cookies_path, "wb") as cookies_file:
        pickle.dump(dummy_cookies, cookies_file)

    # Set the script_directory to the temporary directory
    scraper_instance.script_directory = temp_dir

    # Load cookies using the method
    scraper_instance.load_cookies()

    # Check if the cookies are loaded into the driver
    loaded_cookies = scraper_instance.driver.get_cookies()
    assert loaded_cookies == dummy_cookies

def test_save_cookies(scraper_instance, tmp_path):
    # Create a temporary directory for testing
    temp_dir = tmp_path / "test_data"
    temp_dir.mkdir()

    # Set the script_directory to the temporary directory
    scraper_instance.script_directory = temp_dir

    # Save cookies using the method
    scraper_instance.save_cookies()

    # Check if the cookies file is created
    cookies_path = temp_dir / "data" / "cookies.pkl"
    assert cookies_path.exists()

    # Check if the saved cookies match the driver's cookies
    with open(cookies_path, "rb") as cookies_file:
        saved_cookies = pickle.load(cookies_file)
        assert saved_cookies == scraper_instance.driver.get_cookies()
      
