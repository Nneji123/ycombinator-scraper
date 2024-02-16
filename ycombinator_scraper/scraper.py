"""Ycombinator-Scraper"""
import concurrent.futures
import pickle
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from loguru import logger
from rich.console import Console
from rich.progress import Progress
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from ycombinator_scraper.config import Settings
from ycombinator_scraper.exceptions import InvalidURLException
from ycombinator_scraper.models import CompanyData, FounderData, JobData, ScrapedData
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
    validate_company_url,
    validate_job_url,
)

settings = Settings()

MAX_WORKERS = 5
SCROLL_PAUSE_TIME = 0.5


class Scraper:
    def __init__(self):
        self.driver = None
        self.console = Console()
        self.script_directory = Path(__file__).resolve().parent

    def _initialize_driver(self) -> webdriver.Chrome:
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
                self.driver = self._initialize_driver()
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

    def _validate_and_set_job_url(self, input_url: str) -> None:
        try:
            validate_job_url(input_url)
        except InvalidURLException as e:
            logger.error(f"Error: {e}")

    def _validate_and_set_company_url(self, input_url: str) -> None:
        try:
            validate_company_url(input_url)
        except InvalidURLException as e:
            logger.error(f"Error: {e}")

    def scrape_job_data(self, job_url: str) -> JobData:
        try:
            if self.driver is None:
                self.driver = self._initialize_driver()
            self._validate_and_set_job_url(job_url)
            job_data = JobData(job_url=job_url)
            self.driver.get(job_url)

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            job_data.job_title = self._get_job_element_text(
                By.CLASS_NAME, JOB_TITLE_CLASS
            )

            job_tags_elements = self.driver.find_elements(By.CLASS_NAME, JOB_TAGS_CLASS)
            job_data.job_tags = [tag.text.split("\n") for tag in job_tags_elements]

            job_data.job_salary_range = self._get_job_salary_range()

            job_description_elements = self.driver.find_elements(
                By.CLASS_NAME, JOB_DESCRIPTION_CLASS
            )
            job_data.job_description = self._get_job_description(
                job_description_elements
            )

            logger.success(f"Successfully scraped job data for: {job_data.job_url}")

        except Exception as e:
            logger.error(f"Error scraping job data for: {job_data.job_url}. {e}")

        return job_data

    def _get_job_element_text(self, by, selector):
        try:
            element = self.driver.find_element(by, selector)
            return element.text if element else None
        except NoSuchElementException:
            return None

    def _get_job_salary_range(self):
        try:
            salary_range_element = self.driver.find_element(
                By.CLASS_NAME, SALARY_RANGE_CLASS
            )
            cleaned_string = (
                salary_range_element.text.strip("").replace("•", "").strip(" ")
            )
            return cleaned_string if cleaned_string else None
        except NoSuchElementException:
            return None

    def _get_job_description(self, description_elements):
        if len(description_elements) >= 2:
            job_description_html = description_elements[1].get_attribute("outerHTML")
            return strip_html_tags(job_description_html)
        return None

    def scrape_company_data(self, company_url: str) -> CompanyData:
        try:
            if self.driver is None:
                self.driver = self._initialize_driver()

            self._validate_and_set_company_url(company_url)
            company_details = CompanyData(company_url=company_url)

            self.driver.get(company_url)

            company_details.company_image = self._get_company_element_attribute(
                By.CLASS_NAME, COMPANY_IMAGE_CLASS, "src"
            )

            company_details.company_name = self._get_company_element_text(
                By.CLASS_NAME, COMPANY_NAME_CLASS
            )

            company_description_elements = self.driver.find_elements(
                By.CLASS_NAME, COMPANY_DESCRIPTION_CLASS_ONE
            ) or self.driver.find_elements(By.CLASS_NAME, COMPANY_DESCRIPTION_CLASS_TWO)
            company_details.company_description = (
                self._get_company_element_text(
                    By.CLASS_NAME, COMPANY_DESCRIPTION_CLASS_ONE
                )
                if company_description_elements
                else None
            )

            company_details.company_tags = self._get_company_element_texts(
                By.CLASS_NAME, COMPANY_TAGS_CLASS
            )

            company_details.company_job_links = self._get_company_element_attributes(
                By.CLASS_NAME, COMPANY_JOB_CLASS, "href"
            )

            social_prefixes = {
                0: "https://",
                1: "https://twitter.com/",
                2: "https://facebook.com/",
            }

            company_details.company_social_links = [
                f"{social_prefixes.get(i, '')}{link.text.strip()}"
                for i, link in enumerate(
                    self.driver.find_elements(By.CLASS_NAME, COMPANY_SOCIAL_CLASS)
                )
                if link.text.strip()
            ]

            company_details.company_founders = self.scrape_founders_data(
                company_url=company_url
            )

            company_details.job_data = [
                self.scrape_job_data(job_url)
                for job_url in company_details.company_job_links
            ]

            logger.success(
                f"Successfully scraped Data For Company: {company_details.company_name}"
            )

        except Exception as e:
            logger.error(f"Error Scraping Company Data: {e}")

        return company_details

    def _get_company_element_text(self, by, selector):
        try:
            element = self.driver.find_element(by, selector)
            return element.text.strip() if element else None
        except NoSuchElementException:
            return None

    def _get_company_element_texts(self, by, selector):
        elements = self.driver.find_elements(by, selector)
        return [element.text.strip() for element in elements]

    def _get_company_element_attribute(self, by, selector, attribute):
        try:
            element = self.driver.find_element(by, selector)
            return element.get_attribute(attribute) if element else None
        except NoSuchElementException:
            return None

    def _get_company_element_attributes(self, by, selector, attribute):
        elements = self.driver.find_elements(by, selector)
        return [element.get_attribute(attribute) for element in elements]

    def scrape_founders_data(self, company_url: str) -> List[FounderData]:
        founders_list = []

        try:
            if self.driver is None:
                self.driver = self._initialize_driver()
            self._validate_and_set_company_url(company_url)
            self.driver.get(company_url)
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

    # TODO: Fix Multiple company scraper
    def _scroll_down(self) -> None:
        try:
            # Get scroll height
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            while True:
                # Scroll down to bottom
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if new_height == last_height:
                    break
                last_height = new_height

        except Exception as e:
            logger.error(f"Error while scrolling down: {e}")

    def scrape_company_urls(self, target_companies: int) -> List[str]:
        company_urls = set()

        try:
            if self.driver is None:
                self.driver = self._initialize_driver()
            self.login()
            time.sleep(10)
            while len(company_urls) < target_companies:
                self._scroll_down()

                elements = self.driver.find_elements(By.CSS_SELECTOR, ".company-name")
                new_company_urls = [
                    element.find_element(By.XPATH, "..").get_attribute("href")
                    for element in elements
                ]
                company_urls.update(new_company_urls)

        except Exception as e:
            logger.error(f"Error scraping company URLs: {e}")

        return list(company_urls)[:target_companies]

    def scrape_multiple_companies(self, no_of_companies: int) -> ScrapedData:
        scraped_data = []
        company_urls = self.scrape_company_urls(target_companies=no_of_companies)
        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Scraping Companies...\n", total=len(company_urls)
            )
            max_retries = 3  # Set the maximum number of retries
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(self.scrape_company_data, url)
                    for url in company_urls
                ]

                for future in concurrent.futures.as_completed(futures):
                    retries = 0
                    while retries < max_retries:
                        try:
                            result = future.result()
                            scraped_data.append(result)
                            progress.update(task, advance=1)
                            break  # Break out of the retry loop if successful
                        except Exception as e:
                            retries += 1
                            self.console.log(
                                f"[bold red]Error scraping company data: {e}[/bold red]"
                            )
                            time.sleep(2)  # Add a delay before retrying
                    time.sleep(5)
        return ScrapedData(scraped_data=scraped_data)

    def shutdown_driver(self) -> None:
        if self.driver is not None:
            self.driver.quit()
