import pytest

from ycombinator_scraper import Scraper


@pytest.fixture
def scraper():
    scraper = Scraper()
    yield scraper


@pytest.fixture
def get_test_url():
    url = "https://www.workatastartup.com/companies/vocode/"
    yield url


@pytest.fixture
def get_test_job_url():
    url = "https://www.workatastartup.com/jobs/64444"
    yield url
