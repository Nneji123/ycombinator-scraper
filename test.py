# import json
# import pickle
# import re
# import time
# from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
# from pathlib import Path
# from typing import Dict, List, Union

# from loguru import logger
# from selenium import webdriver
# from selenium.common.exceptions import (
#     NoSuchElementException,
#     TimeoutException,
#     WebDriverException,
# )
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager

# from config.config import Settings
# from src.scraping.models import FounderDetails, JobData, ScrapeResult

# # Get the path of the current Python file
# current_file_path = Path(__file__)
# settings = Settings()


# def initialize_driver(headless: bool = False) -> webdriver.Chrome:
#     chrome_options = Options()
#     chrome_options.headless = headless
#     chrome_options.binary_location = settings.CHROME_BINARY
#     chrome_driver_path = current_file_path.parent / "chromedriver.exe"
#     chrome_service = ChromeService(chrome_driver_path)
#     driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

#     logger.info("WebDriver initialized")
#     return driver


# def login(driver: webdriver.Chrome, username: str, password: str) -> bool:
#     try:
#         driver.get("https://www.workatastartup.com/companies")

#         login_button = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "/html/body/header/nav/div[3]/div[2]/a")
#             )
#         )
#         login_button.click()

#         username_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='ycid-input']"))
#         )
#         password_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//*[@id='password-input']"))
#         )
#         login_button = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//*[@id='sign-in-card']/div[2]/div[8]/button/span[1]")
#             )
#         )

#         username_input.send_keys(username)
#         password_input.send_keys(password)
#         login_button.click()

#         WebDriverWait(driver, 20).until(EC.url_contains("/companies"))

#         return True

#     except TimeoutException:
#         logger.error("Login failed due to timeout")
#         return False


# def load_cookies(driver: webdriver.Chrome) -> None:
#     cookies_path = Path("data") / "cookies.pkl"

#     if cookies_path.exists():
#         with open(cookies_path, "rb") as cookies_file:
#             cookies = pickle.load(cookies_file)
#             for cookie in cookies:
#                 driver.add_cookie(cookie)


# def save_cookies(driver: webdriver.Chrome) -> None:
#     cookies_path = Path("data") / "cookies.pkl"

#     with open(cookies_path, "wb") as cookies_file:
#         pickle.dump(driver.get_cookies(), cookies_file)


# def scrape_job_links(driver: webdriver.Chrome) -> List[str]:
#     try:
#         page_content = driver.page_source
#         job_links = re.findall(
#             r"https://www\.workatastartup\.com/jobs/\d+", page_content
#         )

#     except (TimeoutException, NoSuchElementException, WebDriverException) as e:
#         logger.error(f"Error scraping job links: {e}")
#         job_links = []

#     return job_links


# def scrape_job_data(driver: webdriver.Chrome, job_link: str) -> JobData:
#     job_data = JobData()

#     try:
#         driver.get(job_link)

#         job_description = (
#             WebDriverWait(driver, 10)
#             .until(
#                 EC.presence_of_element_located(
#                     (By.XPATH, "//div[@class='job-description']")
#                 )
#             )
#             .text
#         )

#         company_link = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//a[@class='company-link']"))
#         )
#         company_name = company_link.text

#         company_link.click()

#         founders_names = driver.find_elements(By.XPATH, "//div[@class='founder-name']")
#         profile_images_urls = driver.find_elements(
#             By.XPATH, "//img[@class='founder-profile-image']"
#         )
#         linkedin_urls = driver.find_elements(By.XPATH, "//a[@class='linkedin-profile']")

#         founders_list = []

#         for i in range(len(founders_names)):
#             founder_name = founders_names[i].text
#             profile_image_url = profile_images_urls[i].get_attribute("src")
#             linkedin_url = linkedin_urls[i].get_attribute("href")

#             founder_details = FounderDetails(
#                 founder_name=founder_name,
#                 profile_image_url=profile_image_url,
#                 linkedin_url=linkedin_url,
#             )

#             founders_list.append(founder_details)

#         job_data = JobData(
#             company_name=company_name,
#             job_description=job_description,
#             founders_details=founders_list,
#         )

#         logger.info(job_data)

#     except (TimeoutException, NoSuchElementException, WebDriverException) as e:
#         logger.error(f"Error scraping job data for {job_link}: {e}")

#     finally:
#         driver.execute_script("window.history.go(-1)")
#         time.sleep(2)  # Adding a pause between requests to mimic human behavior

#     return job_data


# def scrape_jobs_in_parallel(username: str, password: str) -> str:
#     driver = initialize_driver()

#     try:
#         if login(driver, username, password):
#             load_cookies(driver)

#             job_links_to_scrape = scrape_job_links(driver)

#             with ThreadPoolExecutor(max_workers=5) as executor:
#                 futures = [
#                     executor.submit(scrape_job_data, driver, job_link)
#                     for job_link in job_links_to_scrape
#                 ]
#                 wait(futures, timeout=None, return_when=ALL_COMPLETED)

#             scraped_data = [future.result() for future in futures]

#             save_cookies(driver)

#             result = ScrapeResult(
#                 scraped_data=scraped_data, job_links=job_links_to_scrape
#             )

#             return result.model_dump_json(indent=2)

#     except (NoSuchElementException, WebDriverException) as e:
#         logger.error(f"Error: {e}")
#     finally:
#         driver.quit()


# if __name__ == "__main__":
#     scraped_json_data = scrape_job_links(
#         settings.login_username, settings.login_password
#     )
#     print(scraped_json_data)

import re

from bs4 import BeautifulSoup  # Import BeautifulSoup from the 'bs4' package


def strip_html_tags(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()


import json
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login_and_scrape_jobs(username, password):
    # # Initialize the WebDriver
    # options = Options()
    # options.add_extension("src/scraping/chrome_extensions/block_video.crx")
    # options.add_extension("src/scraping/chrome_extensions/block_images_video.crx")

    driver = (
        webdriver.Chrome()
    )  # Make sure to replace with the path to your chromedriver

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
        # WebDriverWait(driver, 20).until(EC.url_contains("/companies"))
        # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        # Get all job links on the page
        page_content = driver.page_source
        job_links = re.findall(
            r"https://www\.workatastartup\.com/jobs/\d+", page_content
        )

        driver.get(
            "https://www.workatastartup.com/companies/picnichealth"
        )  # Open the job link directly

        # Wait for the job page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Find all elements with the specified class name
        job_description_elements = driver.find_elements(By.CLASS_NAME, "prose")
        print(job_description_elements)
        print(job_description_elements[1].get_attribute("outerHTML"))
        # Check if there is at least one element with the specified class name
        if len(job_description_elements) >= 2:
            # Get the outer HTML of the second element
            job_description_html = job_description_elements[1].get_attribute(
                "outerHTML"
            )

            job_title = driver.find_elements(
                By.CSS_SELECTOR, ".company-name.text-2xl.font-bold"
            )
            print(job_title)
            job_title[0].text
            # Strip HTML tags
            job_description_text = strip_html_tags(job_description_html)
            print(job_description_text)

        # Click the link of the company that posted the job
        company_link = driver.find_elements(By.CLASS_NAME, "company-logo")

        company_link[0].click()
        # Get all company details on the page
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
        print(company_name)
        company_description = company_description_elements[0].text
        print(company_description)
        company_tags = [tag.text for tag in company_tags_elements]
        print(company_tags)
        company_links = [
            link.get_attribute("href")
            for link in driver.find_elements(
                By.XPATH, "//a[@class='text-blue-600.ellipsis']"
            )
        ]
        print(company_links)
        company_details = {
            "company_name": company_name,
            "company_description": company_description,
            "company_tags": company_tags,
            "company_links": company_links,
        }
        print(company_details)
        # companies_list.append(company_details)

        # Find all founders' details
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
        # Create a list to store founders' details
        founders_list = []

        # Iterate through each founder and gather details
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
        # Store the job description and founders' details in a dictionary or process them as needed
        job_data = {
            "job_description": job_description_text,
            "job_title": job_title,
            "founders_details": founders_list,
            # 'company_details': company_details
        }

        print(json.dumps(job_data))
    except Exception as e:
        print(e)

    finally:
        # Close the WebDriver
        driver.quit()


# Example usage
login_and_scrape_jobs("Aboy123", "linda321")
