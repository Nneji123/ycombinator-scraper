# YCombinator-Scraper API Reference

## `Scraper` Class

### `__init__(self) -> None`

- **Description:**
  Initializes the `Scraper` class.

### `initialize_driver(self) -> webdriver.Chrome`

- **Returns:**
  - `webdriver.Chrome`: Initialized ChromeDriver instance.

- **Description:**
  Initializes the ChromeDriver.

### `shutdown_driver(self) -> None`

- **Description:**
  Ends the chromedriver instance.

### `login(self, username: str, password: str) -> bool`

- **Parameters:**
  - `username` (str): Workatastartup username.
  - `password` (str): Workatastartup password.

- **Returns:**
  - `bool`: True if login is successful, False otherwise.

- **Description:**
  Logs in to the Workatastartup platform using the provided credentials.

### `load_cookies(self) -> None`

- **Description:**
  Loads cookies from the saved file.

### `save_cookies(self) -> None`

- **Description:**
  Saves cookies to a file.

### `scrape_job_data(self, job_url: str) -> JobData`

- **Parameters:**
  - `job_url` (str): URL of the job to scrape.

- **Returns:**
  - `JobData`: Scraped job data.

- **Description:**
  Scrapes job data from the specified job URL.

### `scrape_company_data(self, company_url: str) -> CompanyData`

- **Parameters:**
  - `company_url` (str): URL of the company to scrape.

- **Returns:**
  - `CompanyData`: Scraped company data.

- **Description:**
  Scrapes company data from the specified company URL.

### `scrape_founders_data(self, company_url: str) -> List[FounderData]`

- **Parameters:**
  - `company_url` (str): URL of the company to scrape founders data.

- **Returns:**
  - `List[FounderData]`: List of scraped founder data.

- **Description:**
  Scrapes founders data from the specified company URL.

---

## `JobData` Class

### `__init__(self, job_url: str) -> None`

- **Parameters:**
  - `job_url` (str): URL of the job.

- **Description:**
  Initializes the `JobData` class.

### `model_dump(self) -> dict`

- **Returns:**
  - `dict`: Dictionary representation of the job data.

- **Description:**
  Returns a dictionary representation of the job data.

### `model_dump_json(self, **kwargs) -> str`

- **Returns:**
  - `str`: JSON representation of the job data.

- **Description:**
  Returns a JSON representation of the job data.

---

## `CompanyData` Class

### `__init__(self, company_url: str) -> None`

- **Parameters:**
  - `company_url` (str): URL of the company.

- **Description:**
  Initializes the `CompanyData` class.

### `model_dump(self) -> dict`

- **Returns:**
  - `dict`: Dictionary representation of the company data.

- **Description:**
  Returns a dictionary representation of the company data.

### `model_dump_json(self, **kwargs) -> str`

- **Returns:**
  - `str`: JSON representation of the company data.

- **Description:**
  Returns a JSON representation of the company data.

---

## `FounderData` Class

### `__init__(self, founder_name: str, founder_image_url: str, founder_description: str, founder_linkedin_url: str, founder_emails: Optional[List[str]] = None) -> None`

- **Parameters:**
  - `founder_name` (str): Founder's name.
  - `founder_image_url` (str): URL of the founder's image.
  - `founder_description` (str): Description of the founder.
  - `founder_linkedin_url` (str): LinkedIn URL of the founder.
  - `founder_emails` (Optional[List[str]]): List of founder's email addresses.

- **Description:**
  Initializes the `FounderData` class.

### `model_dump(self) -> dict`

- **Returns:**
  - `dict`: Dictionary representation of the founder data.

- **Description:**
  Returns a dictionary representation of the founder data.

### `model_dump_json(self, **kwargs) -> str`

- **Returns:**
  - `str`: JSON representation of the founder data.

- **Description:**
  Returns a JSON representation of the founder data.

---

**Note:** All classes and methods in this API reference are part of the `ycombinator_scraper` package.
