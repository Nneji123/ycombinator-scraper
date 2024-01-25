import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from ycombinator_scraper.config import Settings
from ycombinator_scraper.scraper import scrape_founders_data, FounderData

settings = Settings()


@pytest.fixture
def driver():
    # Set up a WebDriver instance for testing
    chrome_service = ChromeService(executable_path=settings.CHROMEDRIVER_BINARY)
    driver = webdriver.Chrome(service=chrome_service)
    yield driver
    # Close the WebDriver instance after testing
    driver.quit()


def test_scrape_founders_data(driver):
    # Mocking company URL for testing
    company_url = "https://www.workatastartup.com/companies/vocode"

    # Call the scrape_founders_data function with mocked company URL
    founders_list = scrape_founders_data(driver, company_url)

    # Assert that the founders_list is a list of FounderData
    assert all(isinstance(founder, FounderData) for founder in founders_list)

    # Add more assertions based on the structure of FounderData and the expected HTML elements

    # Example assertions:
    for founder in founders_list:
        assert isinstance(founder.founder_name, str)
        assert isinstance(founder.founder_image_url, str)
        assert isinstance(founder.founder_description, str)
        assert isinstance(founder.founder_linkedin_url, str)
