import json
import os
import pickle
import re
import time
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from typing import Dict, List, Union

from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from config.config import Settings
from src.scraping.models import FounderDetails, JobData, ScrapeResult

settings = Settings()


def strip_html_tags(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()


def initialize_driver(headless: bool = True) -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.headless = headless

    chrome_service = ChromeService(ChromeDriverManager().install())
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

        # Wait for the login to complete
        driver.get("https://www.workatastartup.com/companies")

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


def scrape_job_links(driver: webdriver.Chrome, jobs_url: str) -> List[str]:
    job_links = []

    try:
        driver.get(job_url)
        job_link_elements = driver.find_elements(
            By.XPATH, "//a[contains(@href, '/job/')]"
        )
        job_links = [job_link.get_attribute("href") for job_link in job_link_elements]

    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error(f"Error scraping job links: {e}")

    return job_links


def scrape_company_data(driver: webdriver.Chrome, company_link: str):
    pass

def scrape_founders_data(driver: webdriver.Chrome):
    pass

def scrape_job_data(driver: webdriver.Chrome, job_link: str) -> JobData:
    job_data = JobData()

    try:
        driver.get(job_link)

        job_description_elements = driver.find_elements(By.CLASS_NAME, "prose")
        if len(job_description_elements) >= 2:
            job_description_html = job_description_elements[1].get_attribute(
                "outerHTML"
            )

            job_title = driver.find_elements(
                By.CSS_SELECTOR, ".company-name.text-2xl.font-bold"
            )
            job_title[0].text
            job_description_text = strip_html_tags(job_description_html)
        company_link = driver.find_elements(By.CLASS_NAME, "company-logo")

        company_link[0].click()
        company_name_elements = driver.find_elements(
            By.CLASS_NAME, "company-name.hover\:underline"
        )
        company_description_elements = driver.find_elements(
            By.CLASS_NAME, "sm\:text-md.prose.col-span-11.mx-5.max-w-none.text-sm"
        )
        company_tags_elements = driver.find_elements(
            By.CLASS_NAME, "detail-label.text-sm"
        )

        company_name = company_name_elements[0].text
        company_description = company_description_elements[0].text
        company_tags = [tag.text for tag in company_tags_elements]
        company_links = [
            link.get_attribute("href")
            for link in driver.find_elements(
                By.XPATH, "//a[@class='text-blue-600.ellipsis']"
            )
        ]
        company_details = {
            "company_name": company_name,
            "company_description": company_description,
            "company_tags": company_tags,
            "company_links": company_links,
        }
        founders_names = driver.find_elements(By.CLASS_NAME, "mb-1.font-medium")
        print(founders_names[0].text)
        founders_images = driver.find_elements(
            By.CLASS_NAME, "ml-2.mr-2.h-20.w-20.rounded-full.sm\:ml-5"
        )
        print(founders_images[0].get_attribute("href"))
        founders_descriptions = driver.find_elements(
            By.CLASS_NAME, "sm\:text-md.text-sm"
        ) or driver.find_elements(By.CLASS_NAME, "sm\:text-md.w-full.text-sm")
        print(founders_descriptions[0].text)
        founders_linkedins = driver.find_elements(
            By.CLASS_NAME, "fa.fa-linkedin.ml-4.p-1.text-blue-600"
        )
        print(founders_linkedins[0].get_attribute("href"))
        founders_list = []

        for i in range(len(founders_names)):
            founder_name = founders_names[i].text
            founder_image_url = founders_images[i].get_attribute("src")
            founder_description = founders_descriptions[i].text
            founder_linkedin_url = founders_linkedins[i].get_attribute("href")

            founder_details = {
                "founder_name": founder_name,
                "founder_image_url": founder_image_url,
                "founder_description": founder_description,
                "founder_linkedin_url": founder_linkedin_url,
            }
            founders_list.append(founder_details)
        job_data = {
            "job_description": job_description_text,
            "job_title": job_title,
            "founders_details": founders_list,
            "company_details": company_details,
        }

        logger.info(job_data)

    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error(f"Error scraping job data for {job_link}: {e}")

    finally:
        driver.execute_script("window.history.go(-1)")
        time.sleep(2)  # Adding a pause between requests to mimic human behavior

    return job_data


def scrape_jobs_in_parallel(username: str, password: str) -> str:
    driver = initialize_driver()

    try:
        if login(driver, username, password):
            load_cookies(driver)

            job_links_to_scrape = scrape_job_links(driver)

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(scrape_job_data, driver, job_link)
                    for job_link in job_links_to_scrape
                ]
                wait(futures, timeout=None, return_when=ALL_COMPLETED)

            scraped_data = [future.result() for future in futures]

            save_cookies(driver)

            result = ScrapeResult(
                scraped_data=scraped_data, job_links=job_links_to_scrape
            )

            return result.json(indent=2)

    except (NoSuchElementException, WebDriverException) as e:
        logger.error(f"Error: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    scraped_json_data = scrape_jobs_in_parallel(
        settings.login_username, settings.login_password
    )
    print(scraped_json_data)
