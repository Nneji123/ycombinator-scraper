# Examples

This section provides some examples of how to use the YCombinator-Scraper tool and package in different scenarios.

## Using CLI
### Scrape Company Data

```bash
ycscraper scrape-company --company-url https://www.workatastartup.com/companies/example-inc
```

This command will scrape data for the specified company and save it in the default output format (JSON).

### Scrape Job Data

```bash
ycscraper scrape-job --job-url https://www.workatastartup.com/jobs/32131
```

This command will scrape data for the specified job and save it in the default output format (JSON).

### Scrape Founder Data

```bash
ycscraper scrape-founders --company-url https://www.workatastartup.com/companies/example-inc
```

This command will scrape founder data for the specified company and save it in the default output format (JSON).

## With library

Below are examples demonstrating how to use the `Scraper` class to perform various actions such as login, save and load cookies, scrape founder data, scrape company data, and scrape job data.

### Initialize Scraper
```python
scraper = Scraper()
```

### Login
```python
login_successful = scraper.login(username="your_username", password="your_password")
if login_successful:
    print("Login successful!")
else:
    print("Login failed. Check credentials.")
```

### Save Cookies
```python
scraper.save_cookies()
print("Cookies saved successfully.")
```

### Load Cookies
```python
scraper.load_cookies()
print("Cookies loaded successfully.")
```

### Scrape Founder Data
```python
company_url = "https://www.workatastartup.com/companies/example"
founders_data = scraper.scrape_founders_data(company_url)
for founder_data in founders_data:
    print(f"Founder: {founder_data.founder_name}, LinkedIn: {founder_data.founder_linkedin_url}")
```

### Scrape Company Data
```python
company_url = "https://www.workatastartup.com/companies/example"
company_data = scraper.scrape_company_data(company_url)
print(f"Company: {company_data.company_name}, Description: {company_data.company_description}")
```

### Scrape Job Data
```python
job_url = "https://www.workatastartup.com/jobs/321321"
job_data = scraper.scrape_job_data(job_url)
print(f"Job Title: {job_data.job_title}, Salary Range: {job_data.job_salary_range}")
```

### Shutdown Scraper
```python
scraper.shutdown_driver()
print("Scraper shut down successfully.")
```

Make sure to replace placeholder values with your actual credentials, URLs, and other details. Customize the usage according to your specific needs.
