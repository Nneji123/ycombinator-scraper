import pytest

from ycombinator_scraper.scraper import Scraper


@pytest.fixture
def scraper():
    scraper = Scraper()
    yield scraper


@pytest.fixture
def get_test_url():
    url = "https://www.workatastartup.com/companies/vocode"
    yield url
