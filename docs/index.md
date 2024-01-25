# YCJobAutomator

This Python script provides a web scraping tool for extracting data from [Workatastartup](https://www.workatastartup.com/) website. The script uses Selenium and BeautifulSoup to navigate through the pages and extract information.

## Prerequisites

- Python 3.x
- Chrome browser installed
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) installed and added to the system path.
- Required Python packages can be installed using `pip install -r requirements.txt`.

## Usage

1. **Initialize Driver**

   ```python
   from src.scraper import initialize_driver

   # Headless option is set to True by default
   driver = initialize_driver(headless=True)
   ```

   The `initialize_driver` function initializes the Chrome WebDriver. Pass `headless=False` if you want to see the browser in action.

2. **Login to Workatastartup**

   ```python
   from src.scraper import login

   username = "your_username"
   password = "your_password"

   if login(driver, username, password):
       # Successfully logged in
       pass
   else:
       # Login failed
       pass
   ```

   The `login` function logs in to the Workatastartup website using the provided username and password.

3. **Load/Save Cookies (Optional)**

   ```python
   from src.scraper import load_cookies, save_cookies

   # Load cookies from file
   load_cookies(driver)

   # Save cookies to file
   save_cookies(driver)
   ```

   These functions allow you to load previously saved cookies or save the current cookies for future use.

4. **Scrape Job Details**

   ```python
   from src.scraper import scrape_job_details

   job_url = "https://www.workatastartup.com/jobs/12345"
   job_data = scrape_job_details(driver, job_url)
   print(job_data)
   ```

   The `scrape_job_details` function extracts details such as job title, tags, salary range, and job description from a specific job page.

5. **Scrape Company Details**

   ```python
   from src.scraper import scrape_company_data

   company_url = "https://www.workatastartup.com/companies/abc"
   company_data = scrape_company_data(driver, company_url)
   print(company_data)
   ```

   The `scrape_company_data` function fetches details about a company, including name, description, tags, job links, and social links.

6. **Scrape Founders Data**

   ```python
   from src.scraper import scrape_founders_data

   founders_url = "https://www.workatastartup.com/companies/abc"
   founders_data = scrape_founders_data(driver, founders_url)
   print(founders_data)
   ```

   The `scrape_founders_data` function retrieves information about the founders of a company, including name, image URL, description, LinkedIn URL, and optional emails.

7. **Scrape Multiple Companies in Parallel**

   ```python
   from src.scraper import scrape_jobs_in_parallel, ScrapedData

   company_urls = ["https://www.workatastartup.com/companies/abc", "https://www.workatastartup.com/companies/xyz"]
   scraped_data = scrape_jobs_in_parallel(username, password, company_urls)
   print(scraped_data)
   ```

   The `scrape_jobs_in_parallel` function allows you to scrape data from multiple companies simultaneously. Provide a list of company URLs, and it will return a list of `CompanyData`.

8. **Run the Script**

   Execute the script to perform a sample scraping operation.

   ```bash
   python script_name.py
   ```

   Replace `script_name.py` with the actual name of your script.

## Notes

- Ensure you have the necessary permissions before scraping any website.
- It is recommended to review and comply with the terms of service of the target website.

Feel free to modify the script according to your specific use case and requirements.
