"""Ycombinator-Scraper"""
import pickle
import sys
from pathlib import Path
from typing import List

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from ycombinator_scraper.config import Settings
from ycombinator_scraper.exceptions import InvalidURLException
from ycombinator_scraper.models import CompanyData, FounderData, JobData
from ycombinator_scraper.selectors import (
    COMPANY_DESCRIPTION_CLASS_ONE,
    COMPANY_DESCRIPTION_CLASS_TWO,
    COMPANY_IMAGE_CLASS,
    COMPANY_JOB_CLASS,
    COMPANY_NAME_CLASS,
    COMPANY_SOCIAL_CLASS,
    COMPANY_TAGS_CLASS,
    FOUNDER_DESCRIPTION_CLASS_ONE,
    FOUNDER_DESCRIPTION_CLASS_TWO,
    FOUNDER_IMAGE_CLASS,
    FOUNDER_LINKEDIN_CLASS,
    FOUNDER_NAME_CLASS,
    JOB_DESCRIPTION_CLASS,
    JOB_TAGS_CLASS,
    JOB_TITLE_CLASS,
    LOGIN_BUTTON_XPATH,
    PASSWORD_INPUT_XPATH,
    SALARY_RANGE_CLASS,
    SUBMIT_BUTTON_XPATH,
    USERNAME_INPUT_XPATH,
)
from ycombinator_scraper.utils import (
    strip_html_tags,
    timed_cache,
    validate_company_url,
    validate_job_url,
)

settings = Settings()


class Scraper:
    def __init__(self):
        self.driver = None
        self.script_directory = Path(__file__).resolve().parent

    def initialize_driver(self) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_experimental_option(
            "prefs",
            {
                "profile.managed_default_content_settings.images": 2,
                "profile.managed_default_content_settings.stylesheet": 2,
                "profile.managed_default_content_settings.fonts": 2,
            },
        )
        logger.info("Running Scraper in headless mode!")
        if sys.platform == "linux":
            logger.info("Running Scraper in Linux environment!")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
        chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        logger.info("WebDriver initialized")
        return driver

    def login(
        self,
        username: str = settings.login_username,
        password: str = settings.login_password,
    ) -> bool:
        try:
            if self.driver is None:
                self.driver = self.initialize_driver()
            # Open the WorkForStartups website
            self.driver.get("https://www.workatastartup.com/companies")

            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            login_button.click()

            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, USERNAME_INPUT_XPATH))
            )
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, PASSWORD_INPUT_XPATH))
            )
            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, SUBMIT_BUTTON_XPATH))
            )

            username_input.send_keys(username)
            password_input.send_keys(password)
            login_button.click()
            logger.success("Successfully logged in!")
            return True

        except TimeoutException:
            logger.error("Login failed due to timeout")
            return False

    def load_cookies(self) -> None:
        cookies_path = self.script_directory / "data" / "cookies.pkl"
        if cookies_path.exists():
            with open(cookies_path, "rb") as cookies_file:
                cookies = pickle.load(cookies_file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

    def save_cookies(self) -> None:
        cookies_path = self.script_directory / "data" / "cookies.pkl"
        with open(cookies_path, "wb") as cookies_file:
            pickle.dump(self.driver.get_cookies(), cookies_file)

    def validate_and_set_job_url(self, input_url: str) -> None:
        try:
            validate_job_url(input_url)
        except InvalidURLException as e:
            logger.error(f"Error: {e}")

    def validate_and_set_company_url(self, input_url: str) -> None:
        try:
            validate_company_url(input_url)
        except InvalidURLException as e:
            logger.error(f"Error: {e}")

    @timed_cache(seconds=30)
    def scrape_job_data(self, job_url: str) -> JobData:
        try:
            if self.driver is None:
                self.driver = self.initialize_driver()
            self.validate_and_set_job_url(job_url)
            job_data = JobData(job_url=job_url)
            self.driver.get(job_url)
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Scraping job title
            job_title_elements = self.driver.find_elements(
                By.CLASS_NAME, JOB_TITLE_CLASS
            )
            if job_title_elements:
                job_data.job_title = job_title_elements[0].text

            # Scraping job tags
            job_tags_elements = self.driver.find_elements(By.CLASS_NAME, JOB_TAGS_CLASS)
            if job_tags_elements:
                job_data.job_tags = [tag.text.split("\n") for tag in job_tags_elements]

            # Scraping salary range (if present)
            try:
                salary_range_element = self.driver.find_element(
                    By.CLASS_NAME, SALARY_RANGE_CLASS
                )
                cleaned_string = salary_range_element.text.strip("")

                # Remove the " • " symbol
                cleaned_string = cleaned_string.replace("•", "").strip(" ")
                job_data.job_salary_range = cleaned_string
            except Exception:
                pass  # Will return None

            # Scraping job description
            job_description_elements = self.driver.find_elements(
                By.CLASS_NAME, JOB_DESCRIPTION_CLASS
            )
            if len(job_description_elements) >= 2:
                job_description_html = job_description_elements[1].get_attribute(
                    "outerHTML"
                )
                job_data.job_description = strip_html_tags(job_description_html)

            logger.success(f"Successfully scraped job data for: {job_data.job_url}")

        except Exception as e:
            logger.error(f"Error scraping job data for: {job_data.job_url}. {e}")

        return job_data

    @timed_cache(seconds=30)
    def scrape_company_data(self, company_url: str) -> CompanyData:
        company_details = CompanyData()
        try:
            if self.driver is None:
                self.driver = self.initialize_driver()
            self.validate_and_set_company_url(company_url)
            company_details = CompanyData(company_url=company_url)
            self.driver.get(company_url)
            company_link = self.driver.find_elements(By.CLASS_NAME, COMPANY_IMAGE_CLASS)
            company_details.company_image = company_link[0].get_attribute("src")

            company_name_elements = self.driver.find_elements(
                By.CLASS_NAME, COMPANY_NAME_CLASS
            )
            company_description_elements = self.driver.find_elements(
                By.CLASS_NAME, COMPANY_DESCRIPTION_CLASS_ONE
            ) or self.driver.find_elements(By.CLASS_NAME, COMPANY_DESCRIPTION_CLASS_TWO)
            company_tags_elements = self.driver.find_elements(
                By.CLASS_NAME, COMPANY_TAGS_CLASS
            )
            company_job_elements = self.driver.find_elements(
                By.CLASS_NAME, COMPANY_JOB_CLASS
            )
            company_social_elements = self.driver.find_elements(
                By.CLASS_NAME, COMPANY_SOCIAL_CLASS
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
                    company_details.company_social_links.append(
                        f"{prefix}{social_link}"
                    )
            company_details.company_founders = self.scrape_founders_data(
                company_url=company_url
            )
            job_data_list = []
            for job_url in company_details.company_job_links:
                job_data = self.scrape_job_data(job_url)
                job_data_list.append(job_data)
            company_details.job_data = job_data_list
            logger.success(
                f"Successfully scraped Data For Company: {company_details.company_name}"
            )

        except Exception as e:
            logger.error(f"Error Scraping Company Data: {e}")

        return company_details

    @timed_cache(seconds=30)
    def scrape_founders_data(self, company_url: str) -> List[FounderData]:
        founders_list = []

        try:
            if self.driver is None:
                self.initialize_driver()
            self.validate_and_set_company_url(company_url)
            founders_names = self.driver.find_elements(
                By.CLASS_NAME, FOUNDER_NAME_CLASS
            )
            founders_images = self.driver.find_elements(
                By.CLASS_NAME, FOUNDER_IMAGE_CLASS
            )
            founders_descriptions = self.driver.find_elements(
                By.CLASS_NAME, FOUNDER_DESCRIPTION_CLASS_ONE
            ) or self.driver.find_elements(By.CLASS_NAME, FOUNDER_DESCRIPTION_CLASS_TWO)
            founders_linkedins = self.driver.find_elements(
                By.CLASS_NAME, FOUNDER_LINKEDIN_CLASS
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

            logger.success(
                f"Successfully scraped founder's details from: {company_url}"
            )

        except Exception as e:
            logger.error(f"Error scraping founders details: {e}")

        return founders_list

    def shutdown_driver(self) -> None:
        if self.driver is not None:
            self.driver.quit()
