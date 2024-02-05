# YCombinator-Scraper Package

## Usage

The `YCombinator-Scraper` package provides a simple and convenient Python interface for scraping data from the [Workatastartup](https://www.workatastartup.com/companies) website.

### 1. Initialization

```python
from ycombinator_scraper import Scraper

# Initialize the scraper with optional headless mode (default: True)
scraper = Scraper()
```

### 2. Logging In

```python
# Log in to Workatastartup
scraper.login(username="your_username", password="your_password")
```

### 3. Loading and Saving Cookies

```python
# Load saved cookies
scraper.load_cookies()

# Save cookies for later use
scraper.save_cookies()
```

### 4. Scraping Job Data

```python
# Scrape job data
job_data = scraper.scrape_job_data(job_url="https://www.workatastartup.com/joba/1234")

# Print job data
print(job_data)
```

**Example Output:**
```plaintext
JobData(job_url='https://www.workatastartup.com/job/1234', job_title='Software Engineer', job_salary_range='$120k - $150k', job_tags=['Python', 'JavaScript', 'React'], job_description='Exciting opportunity for a skilled software engineer...')
```

### 5. Scraping Company Data

```python
# Scrape company data
company_data = scraper.scrape_company_data(company_url="https://www.workatastartup.com/companies/example-inc")

# Print company data
print(company_data)
```

**Example Output:**
```plaintext
CompanyData(
    company_name='Tech Innovators Inc.',
    company_url='https://www.workatastartup.com/company/5678',
    company_description='Tech Innovators is a leading tech company focused on innovation and cutting-edge solutions...',
    company_tags=['Technology', 'Innovation', 'Startup'],
    company_image='https://www.workatastartup.com/images/logo.png',
    company_social_links=['https://twitter.com/techinnovators', 'https://linkedin.com/company/techinnovators']
)
```

### 6. Scraping Founders Data

```python
# Scrape founders data
founders_data = scraper.scrape_founders_data(company_url="https://www.workatastartup.com/companies/example-inc")

# Print founders data
for i, founder in enumerate(founders_data):
    print(f"Founder {i + 1}:", founder)
```

**Example Output:**
```plaintext
Founder 1: FounderData(
    founder_name='John Doe',
    founder_image_url='https://www.workatastartup.com/images/founder1.png',
    founder_description='Experienced entrepreneur with a passion for technology...',
    founder_linkedin_url='https://www.linkedin.com/in/johndoe',
    founder_emails=None
)
```

**Note:** Replace `"your_username"` and `"your_password"` with your actual Workatastartup username and password. Ensure you handle sensitive information securely.
