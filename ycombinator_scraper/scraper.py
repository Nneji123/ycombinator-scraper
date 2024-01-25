"""Workatastartup.com WebScraper"""

import os
import pickle
from typing import List

from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from config.config import Settings
from src.ycombinator_scraper.models import CompanyData, FounderData, JobData

settings = Settings()

# Create a 'logs' directory if it doesn't exist
log_directory = settings.logs_directory
log_directory.mkdir(exist_ok=True)
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = log_directory / f"log_{timestamp_str}.log"
logger.add(log_file_path, rotation="1 day", level="INFO")


def strip_html_tags(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()


def initialize_driver(headless: bool = settings.headless_mode) -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.headless = headless
    if headless:
        logger.info("Running Scraper in headless mode!")

    chrome_service = ChromeService(executable_path=settings.CHROMEDRIVER_BINARY)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    logger.info("WebDriver initialized")
    return driver


def login(driver: webdriver.Chrome, username: str, password: str) -> bool:
    try:
        # Open the WorkForStartups website
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
        logger.success("Successfully logged in!")
        return True

    except TimeoutException:
        logger.error("Login failed due to timeout")
        return False


def load_cookies(driver: webdriver.Chrome) -> None:
    if os.path.exists("cookies.pkl"):
        with open("cookies.pkl", "rb") as cookies_file:
            cookies = pickle.load(cookies_file)
            for cookie in cookies:
                driver.add_cookie(cookie)


def save_cookies(driver: webdriver.Chrome) -> None:
    with open("cookies.pkl", "wb") as cookies_file:
        pickle.dump(driver.get_cookies(), cookies_file)


def scrape_job_data(driver: webdriver.Chrome, job_url: str) -> JobData:
    try:
        job_data = JobData(job_url=job_url)
        driver.get(job_data.job_url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Scraping job title
        job_title_elements = driver.find_elements(
            By.CLASS_NAME, "company-name.text-2xl.font-bold"
        )
        if job_title_elements:
            job_data.job_title = job_title_elements[0].text

        # Scraping job tags
        job_tags_elements = driver.find_elements(
            By.CLASS_NAME, "company-details.my-2.flex.flex-wrap.md\:my-0"
        )
        if job_tags_elements:
            job_data.job_tags = [tag.text for tag in job_tags_elements]

        # Scraping salary range (if present)
        try:
            salary_range_element = driver.find_element(
                By.CLASS_NAME, "text-gray-500.my-2"
            )
            job_data.job_salary_range = salary_range_element.text
        except Exception:
            pass  # Will return None

        # Scraping job description
        job_description_elements = driver.find_elements(By.CLASS_NAME, "prose")
        if len(job_description_elements) >= 2:
            job_description_html = job_description_elements[1].get_attribute(
                "outerHTML"
            )
            job_data.job_description = strip_html_tags(job_description_html)

    except Exception as e:
        logger.error(f"Error scraping job data for: {job_data.job_url}. {e}")

    logger.success(f"Successfully scraped job data for: {job_data.job_url}")
    return job_data


def scrape_company_data(driver: webdriver.Chrome, company_url: str) -> CompanyData:
    company_details = CompanyData(company_url=company_url)
    try:
        driver.get(company_url)
        company_link = driver.find_elements(By.CLASS_NAME, "mt-2.sm\:w-28")
        company_details.company_image = company_link[0].get_attribute("src")

        company_name_elements = driver.find_elements(
            By.CLASS_NAME, "company-name.hover\:underline"
        )
        company_description_elements = driver.find_elements(
            By.CLASS_NAME, "sm\:text-md.prose.col-span-11.mx-5.max-w-none.text-sm"
        ) or driver.find_elements(By.CLASS_NAME, "mt-3.text-gray-700")
        company_tags_elements = driver.find_elements(
            By.CLASS_NAME, "detail-label.text-sm"
        )
        company_job_elements = driver.find_elements(
            By.CLASS_NAME, "font-medium.text-gray-900.hover\:underline.sm\:text-lg"
        )
        company_social_elements = driver.find_elements(
            By.CLASS_NAME, "text-blue-600.ellipsis"
        )

        company_details.company_name = company_name_elements[0].text
        company_details.company_description = company_description_elements[0].text
        company_details.company_tags = [tag.text for tag in company_tags_elements]
        company_details.company_job_links = [
            link.get_attribute("href") for link in company_job_elements
        ]
        social_prefixes = {
            0: "https://",
            1: "https://twitter.com/",
            2: "https://facebook.com/",
        }

        for i, link in enumerate(company_social_elements):
            social_link = link.text.strip()
            if social_link:  # Check if the link is not an empty string
                prefix = social_prefixes.get(
                    i, ""
                )  # Get the prefix from the dictionary
                company_details.company_social_links.append(f"{prefix}{social_link}")
    except Exception as e:
        logger.error(f"Error Scraping Company Data: {e}")

    logger.success(
        f"Successfully scraped Data For Company: {company_details.company_name}"
    )
    return company_details


def scrape_founders_data(
    driver: webdriver.Chrome, company_url: str
) -> List[FounderData]:
    founders_list = []

    try:
        driver.get(company_url)
        founders_names = driver.find_elements(By.CLASS_NAME, "mb-1.font-medium")
        founders_images = driver.find_elements(
            By.CLASS_NAME, "ml-2.mr-2.h-20.w-20.rounded-full.sm\:ml-5"
        )
        founders_descriptions = driver.find_elements(
            By.CLASS_NAME, "sm\:text-md.text-sm"
        ) or driver.find_elements(By.CLASS_NAME, "sm\:text-md.w-full.text-sm")
        founders_linkedins = driver.find_elements(
            By.CLASS_NAME, "fa.fa-linkedin.ml-4.p-1.text-blue-600"
        )

        for i in range(len(founders_names)):
            founder_name = founders_names[i].text
            founder_image_url = founders_images[i].get_attribute("src")
            founder_description = founders_descriptions[i].text
            founder_linkedin_url = founders_linkedins[i].get_attribute("href")

            founder_data = FounderData(
                founder_name=founder_name,
                founder_image_url=founder_image_url,
                founder_description=founder_description,
                founder_linkedin_url=founder_linkedin_url,
                founder_emails=None,
            )
            founders_list.append(founder_data)

    except Exception as e:
        logger.error(f"Error scraping founders details: {e}")

    logger.success(f"Successfully scraped founder's details from: {company_url}")
    return founders_list
