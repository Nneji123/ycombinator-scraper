import pytest

from ycombinator_scraper.config import Settings
from ycombinator_scraper.scraper import Scraper

settings = Settings()


@pytest.fixture
def scraper():
    # Set up a WebDriver instance for testing
    scraper = Scraper()
    yield scraper


def test_successful_login(scraper):
    # Mocking user credentials for testing
    username = "test_user"
    password = "test_password"
    result = scraper.login(username, password)
    assert result is True
    scraper.shutdown_driver()
