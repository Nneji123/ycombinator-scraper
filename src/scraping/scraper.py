import json
import os
import pickle
import time
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from typing import Dict, List, Union

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

from src.scraping.models import FounderDetails, JobData, ScrapeResult


def initialize_driver(headless: bool = True) -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.headless = headless

    chrome_service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    logger.info("WebDriver initialized")
    return driver


def login(driver: webdriver.Chrome, username: str, password: str) -> bool:
    try:
        driver.get("https://www.workatastartup.com/")

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

        WebDriverWait(driver, 10).until(EC.url_contains("/jobs"))

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


def scrape_job_links(driver: webdriver.Chrome) -> List[str]:
    job_links = []

    try:
        job_link_elements = driver.find_elements(
            By.XPATH, "//a[contains(@href, '/job/')]"
        )
        job_links = [job_link.get_attribute("href") for job_link in job_link_elements]

    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        logger.error(f"Error scraping job links: {e}")

    return job_links


def scrape_job_data(driver: webdriver.Chrome, job_link: str) -> JobData:
    job_data = JobData()

    try:
        driver.get(job_link)

        job_description = (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='job-description']")
                )
            )
            .text
        )

        company_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='company-link']"))
        )
        company_name = company_link.text

        company_link.click()

        founders_names = driver.find_elements(By.XPATH, "//div[@class='founder-name']")
        profile_images_urls = driver.find_elements(
            By.XPATH, "//img[@class='founder-profile-image']"
        )
        linkedin_urls = driver.find_elements(By.XPATH, "//a[@class='linkedin-profile']")

        founders_list = []

        for i in range(len(founders_names)):
            founder_name = founders_names[i].text
            profile_image_url = profile_images_urls[i].get_attribute("src")
            linkedin_url = linkedin_urls[i].get_attribute("href")

            founder_details = FounderDetails(
                founder_name=founder_name,
                profile_image_url=profile_image_url,
                linkedin_url=linkedin_url,
            )

            founders_list.append(founder_details)

        job_data = JobData(
            company_name=company_name,
            job_description=job_description,
            founders_details=founders_list,
        )

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


# if __name__ == "__main__":
#     # scraped_json_data = scrape_jobs_in_parallel("your_username", "your_password")
#     # print(scraped_json_data)

#     login("Nneji123", "linda321")
