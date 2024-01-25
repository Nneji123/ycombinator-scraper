import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.ycombinator_scraper.scraper import scrape_company_data, CompanyData

@pytest.fixture
def driver():
    # Set up a WebDriver instance for testing
    chrome_service = ChromeService("chromedriver.exe")
    driver = webdriver.Chrome(service=chrome_service)
    yield driver
    # Close the WebDriver instance after testing
    driver.quit()

def test_scrape_company_data(driver):
    # Mocking company URL for testing
    company_url = "https://www.workatastartup.com/companies/vocode"

    # Call the scrape_company_data function with mocked company URL
    company_data = scrape_company_data(driver, company_url)

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
