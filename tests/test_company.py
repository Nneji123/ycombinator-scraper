import pytest

from ycombinator_scraper.config import Settings
from ycombinator_scraper.models import CompanyData
from ycombinator_scraper.scraper import Scraper

settings = Settings()


@pytest.fixture
def scraper():
    # Set up a WebDriver instance for testing
    scraper = Scraper()
    yield scraper


def test_scrape_company_data(scraper):
    # Mocking company URL for testing
    company_url = "https://www.workatastartup.com/companies/vocode"

    # Call the scrape_company_data function with mocked company URL
    company_data = scraper.scrape_company_data(company_url)

    # Assert that the company_data is an instance of CompanyData
    assert isinstance(company_data, CompanyData)

    # Add more assertions based on the structure of CompanyData and the expected HTML elements

    # Example assertions:
    assert company_data.company_url == company_url
    assert isinstance(company_data.company_image, str)
    assert isinstance(company_data.company_name, str)
    assert isinstance(company_data.company_description, str)
    assert isinstance(company_data.company_tags, list)
    assert isinstance(company_data.company_job_links, list)
    assert isinstance(company_data.company_social_links, list)

    scraper.shutdown_driver()
