import json
import time

from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.scraping.models import CompanyData, JobData
from src.scraping.scraper import strip_html_tags


def login(driver, username, password):
    driver.get("https://www.workatastartup.com/companies")

    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/header/nav/div[3]/div[2]/a")
        )
    )
    login_button.click()

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ycid-input']"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='password-input']"))
    )
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='sign-in-card']/div[2]/div[8]/button/span[1]")
        )
    )

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()


from typing import List


def scrape_company_links() -> List[dict]:
    company_links = []

    try:
        driver = webdriver.Chrome()
        login(driver=driver, username="Aboy123", password="linda321")
        # Navigate to the main page with the list of companies
        # driver.get("https://www.workatastartup.com/companies/")
        time.sleep(20)
        # Wait for the page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text-2xl.font-medium"))
        )

        # Find all elements with the specified class name
        company_elements = driver.find_elements(By.CLASS_NAME, "text-2xl.font-medium")

        # Iterate through each company element and gather details
        for company_element in company_elements:
            # Extract company name and URL
            company_name = company_element.text
            print(company_name)
            company_url_element = company_element.find_element(By.XPATH, ".//a")
            company_url = company_url_element.get_attribute("href")

            # Append company details to the list
            company_details = {"company_name": company_name, "company_url": company_url}
            company_links.append(company_details)

    except Exception as e:
        logger.error(f"Error scraping company links: {e}")

    return company_links


# Example usage
options = Options()
options.add_argument("--headless")

company_links_result = scrape_company_links()
print("Company Links Result:", company_links_result)
