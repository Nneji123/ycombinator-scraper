import pytest

from ycombinator_scraper.config import Settings
from ycombinator_scraper.models import FounderData
from ycombinator_scraper.scraper import Scraper

settings = Settings()


@pytest.fixture
def scraper():
    # Set up a WebDriver instance for testing
    scraper = Scraper()
    yield scraper


def test_scrape_founders_data(scraper):
    # Mocking company URL for testing
    company_url = "https://www.workatastartup.com/companies/vocode"

    # Call the scrape_founders_data function with mocked company URL
    founders_list = scraper.scrape_founders_data(company_url)

    # Assert that the founders_list is a list of FounderData
    assert all(isinstance(founder, FounderData) for founder in founders_list)

    # Add more assertions based on the structure of FounderData and the expected HTML elements

    # Example assertions:
    for founder in founders_list:
        assert isinstance(founder.founder_name, str)
        assert isinstance(founder.founder_image_url, str)
        assert isinstance(founder.founder_description, str)
        assert isinstance(founder.founder_linkedin_url, str)

    scraper.shutdown_driver()
