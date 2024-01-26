import pytest

from ycombinator_scraper.config import Settings
from ycombinator_scraper.models import JobData
from ycombinator_scraper.scraper import Scraper

settings = Settings()


@pytest.fixture
def scraper():
    # Set up a WebDriver instance for testing
    scraper = Scraper()
    yield scraper


def test_scrape_job_data(scraper):
    # Mocking job URL for testing
    job_url = "https://www.workatastartup.com/companies/vocode"

    # Call the scrape_job_data function with mocked job URL
    job_data = scraper.scrape_job_data(job_url)

    # Assert that the job_data is an instance of JobData
    assert isinstance(job_data, JobData)

    # Add more assertions based on the structure of JobData and the expected HTML elements

    # Example assertions:
    assert job_data.job_url == job_url
    assert isinstance(job_data.job_title, str)
    assert isinstance(job_data.job_tags, list)
    assert isinstance(job_data.job_salary_range, str)
    assert isinstance(job_data.job_description, str)
    scraper.shutdown_driver()
