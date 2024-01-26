# import json
# import time

# from loguru import logger
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

# from ycombinator_scraper.models import CompanyData, JobData
# from ycombinator_scraper.scraper import Scraper
# from ycombinator_scraper.utils import strip_html_tags


# def login(driver, username, password):
#     driver.get("https://www.workatastartup.com/companies")

#     login_button = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "/html/body/header/nav/div[3]/div[2]/a")
#         )
#     )
#     login_button.click()

#     username_input = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//*[@id='ycid-input']"))
#     )
#     password_input = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//*[@id='password-input']"))
#     )
#     login_button = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//*[@id='sign-in-card']/div[2]/div[8]/button/span[1]")
#         )
#     )

#     username_input.send_keys(username)
#     password_input.send_keys(password)
#     login_button.click()


# from typing import List


# def scrape_company_links() -> List[dict]:
#     company_links = []

#     try:
#         driver = webdriver.Chrome()
#         login(driver=driver, username="Aboy123", password="linda321")
#         # Navigate to the main page with the list of companies
#         # driver.get("https://www.workatastartup.com/companies/")
#         time.sleep(20)
#         # Wait for the page to load

#         # Find all elements with the specified class name
#         company_name_elements = driver.find_elements(
#             By.CLASS_NAME, "company-name.hover\:underline"
#         )
#         company_url_elements = driver.find_elements(
#             By.CLASS_NAME, "text-blue-600.ellipsis"
#         )

#         print(company_name_elements)
#         # Iterate through each company element and gather details
#         for company_element in company_name_elements:
#             # Extract company name and URL
#             company_name = company_element.text
#             print(company_name)
#             company_url_element = company_element.find_element(By.XPATH, ".//a")
#             company_url = company_url_element.get_attribute("href")

#             # Append company details to the list
#             company_details = {"company_name": company_name, "company_url": company_url}
#             company_links.append(company_details)

#     except Exception as e:
#         logger.error(f"Error scraping company links: {e}")

#     return company_links


# # Example usage
# options = Options()
# options.add_argument("--headless")

# company_links_result = scrape_company_links()
# print("Company Links Result:", company_links_result)

from ycombinator_scraper.scraper import Scraper

# Instantiate the Scraper
scraper = Scraper()

# Login (replace 'your_username' and 'your_password' with actual values)
scraper.login()
scraper.save_cookies()
# # Load or save cookies if needed
# scraper.load_cookies()

# Scrape job data (replace 'job_url' with an actual job URL)
# job_data = scraper.scrape_job_data('https://www.workatastartup.com/jobs/64089')
# print(job_data)

# # Scrape company data (replace 'company_url' with an actual company URL)
# company_data = scraper.scrape_company_data(
#     "https://www.workatastartup.com/companies/eze"
# )
# print(company_data)

# # Scrape founders data (replace 'company_url' with an actual company URL)
# founders_data = scraper.scrape_founders_data(
#     "https://www.workatastartup.com/companies/eze"
# )
# print(founders_data)

# # Close the driver when done
# scraper.driver.quit()
