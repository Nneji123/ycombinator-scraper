import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from ycombinator_scraper.config import Settings
from ycombinator_scraper.scraper import scrape_job_data, JobData

settings = Settings()


@pytest.fixture
def driver():
    # Set up a WebDriver instance for testing
    chrome_service = ChromeService(executable_path=settings.CHROMEDRIVER_BINARY)
    driver = webdriver.Chrome(service=chrome_service)
    yield driver
    # Close the WebDriver instance after testing
    driver.quit()


def test_scrape_job_data(driver):
    # Mocking job URL for testing
    job_url = "https://www.workatastartup.com/companies/vocode"

    # Call the scrape_job_data function with mocked job URL
    job_data = scrape_job_data(driver, job_url)

    # Assert that the job_data is an instance of JobData
    assert isinstance(job_data, JobData)

    # Add more assertions based on the structure of JobData and the expected HTML elements

    # Example assertions:
    assert job_data.job_url == job_url
    assert isinstance(job_data.job_title, str)
    assert isinstance(job_data.job_tags, list)
    assert isinstance(job_data.job_salary_range, str)
    assert isinstance(job_data.job_description, str)