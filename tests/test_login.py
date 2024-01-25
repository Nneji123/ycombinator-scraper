import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from ycombinator_scraper.config import Settings
from ycombinator_scraper.scraper import login

settings = Settings()


@pytest.fixture
def driver():
    # Set up a WebDriver instance for testing
    chrome_service = ChromeService(executable_path=settings.CHROMEDRIVER_BINARY)
    driver = webdriver.Chrome(service=chrome_service)
    yield driver
    # Close the WebDriver instance after testing
    driver.quit()


def test_successful_login(driver):
    # Mocking user credentials for testing
    username = "test_user"
    password = "test_password"

    # Call the login function with mocked credentials
    result = login(driver, username, password)

    # Assert that the login was successful
    assert result is True


def test_failed_login_timeout(driver):
    # Mocking user credentials for testing
    username = "test_user"
    password = "test_password"

    # Simulate a timeout during login
    with pytest.raises(TimeoutException):
        login(driver, username, password)
