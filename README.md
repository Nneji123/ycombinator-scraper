# YCombinator-Scraper

<div align="center">

<img src="https://raw.githubusercontent.com/nneji123/ycombinator-scraper/main/docs/img/logo.png" alt="Ycombinator_Scraper logo" width="200" height="200" role="img">

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/tests.yml/badge.svg)](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/tests.yml) [![publish-pypi](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/pypi.yml/badge.svg)](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/pypi.yml) [![Coverage](https://codecov.io/gh/Nneji123/ycombinator-scraper/graph/badge.svg?token=37muKJo0SL)](https://codecov.io/gh/Nneji123/ycombinator-scraper)|
| Docs | [![Docs](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/docs.yml/badge.svg)](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/docs.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/ycombinator-scraper.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/ycombinator-scraper/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/ycombinator-scraper.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/ycombinator-scraper/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ycombinator-scraper.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/ycombinator-scraper/) |
| Meta |  [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](./LICENSE) |

</div>

-----

YCombinator-Scraper provides a web scraping tool for extracting data from [Workatastartup](https://www.workatastartup.com/) website. The package uses Selenium and BeautifulSoup to navigate through the pages and extract information.

---

**Documentation**: <a href="https://nneji123.github.io/ycombinator-scraper" target="_blank">https://nneji123.github.io/ycombinator-scraper</a>

**Source Code**: <a href="https://github.com/nneji123/ycombinator-scraper" target="_blank">https://github.com/nneji123/ycombinator-scraper</a>

---

# Sponsor
[Proxycurl APIs](https://nubela.co/proxycurl/?utm_campaign=influencer_marketing&utm_source=github&utm_medium=social&utm_content=ifeanyi_nneji_ycombinator_scraper)


[<img src="https://github.com/Nneji123/ycombinator-scraper/assets/101701760/2f59fe31-f69d-41a8-ab7b-5b66fbe590ed">](https://nubela.co/proxycurl?utm_campaign=influencer_marketing&utm_source=github&utm_medium=social&utm_content=ifeanyi_nneji_ycombinator_scraper)

Scrape public LinkedIn profile data at scale with Proxycurl APIs.

- Scraping Public profiles are battle tested in court in HiQ VS LinkedIn case.
- GDPR, CCPA, SOC2 compliant.
- High rate limit - 300 requests/minute.
- Fast - APIs respond in ~2s.
- Fresh data - 88% of data is scraped real-time, other 12% are not older than 29 days.
- High accuracy.
- Tons of data points returned per profile

Built for developers, by developers.


## Features

- **Web Scraping Capabilities:**
  - Extract detailed information about companies, including name, description, tags, images, job links, and social media links.
  - Scrape job-specific details such as title, salary range, tags, and description.

- **Founder and Company Data Extraction:**
  - Obtain information about company founders, including name, image, description, linkedIn profile, and optional email addresses.

- **Headless Mode:**
  - Run the scraper in headless mode to perform web scraping without displaying a browser window.

- **Configurability:**
  - Easily configure scraper settings such as login credentials, logs directory, automatic install of webdriver based on browser with `webdriver-manager package` and using environment variables or a configuration file.

- **Command-Line Interface (CLI):**
  - Command-line tools to perform various scraping tasks interactively or in batch mode.

- **Data Output Formats:**
  - Save scraped data in JSON or CSV format, providing flexibility for further analysis or integration with other tools.

- **Caching Mechanism:**
  - Implement a caching feature to store function results for a specified duration, reducing redundant web requests and improving performance.

- **Docker Support:**
  - Package the scraper as a Docker image, enabling easy deployment and execution in containerized environments or run the prebuilt docker image `docker pull nneji123/ycombinator_scraper`.

## Requirements

- Python 3.9+
- Chrome or Chromium browser installed.

## Installation

```console
$ pip install ycombinator-scraper
$ ycscraper --help

# Output
YCombinator-Scraper Version 0.7.0
Usage: python -m ycombinator_scraper [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  login
  scrape-company
  scrape-founders
  scrape-job
  version
```

### With Docker
```bash
$ git clone https://github.com/Nneji12/ycombinator-scraper
$ cd ycombinator-scraper
$ docker build -t your_name/scraper_name . # e.g docker build -t nneji123/ycombinator_scraper .
$ docker run nneji123/ycombinator_scraper python -m ycombinator_scraper --help
```

## Dependencies

- **click**: Enables the creation of a command-line interface for interacting with the scraper tool.
- **beautifulsoup4**: Facilitates the parsing and extraction of data from HTML and XML in the web scraping process.
- **loguru**: Provides a robust logging framework to track and manage log messages generated during the scraping process.
- **pandas**: Utilized for the manipulation and organization of data, particularly in generating CSV files from scraped information.
- **pathlib**: Offers an object-oriented approach to handle file system paths, contributing to better file management within the project.
- **pydantic**: Used for data validation and structuring the models that represent various aspects of scraped data.
- **pydantic-settings**: Extends Pydantic to enhance the management of settings in the project.
- **selenium**: Employs browser automation for web scraping, allowing interaction with dynamic web pages and extraction of information.

## Usage

### With CLI
```bash
ycscraper scrape-company --company-url https://www.workatastartup.com/companies/example-inc
```

This command will scrape data for the specified company and save it in the default output format (JSON).

### With Library

```python
from ycombinator_scraper import Scraper

scraper = Scraper()
company_data = scraper.scrape_company_data("https://www.workatastartup.com/companies/example-inc")
print(company_data.model_dump_json(by_alias=True,indent=2))
```
Pydantic is used under the hood so methods like `model_dump_json` are available for all the scraped data.

> **You can view more examples here: [Examples](https://nneji123.github.io/ycombinator-scraper/usage/examples)**


## Contribution

We welcome contributions from the community! To contribute to this project, follow the steps below.

### Setting Up Development Environment

#### Gitpod

You can use Gitpod, a free online VS Code-like environment, to quickly start contributing.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/nneji123/ycombinator-scraper)

#### Local Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/nneji123/ycombinator-scraper.git
    cd ycombinator-scraper
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running Tests

Make sure to run tests before submitting a pull request.

```bash
pip install -r requirements-test.txt
pytest tests
```

### Installing Documentation Requirements

If you make changes to documentation, install the necessary dependencies:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

### Setting Up Pre-Commit Hooks

We use `pre-commit` to ensure code quality. Install it by running:

```bash
pip install pre-commit
pre-commit install
```

Now, `pre-commit` will run automatically before each commit to check for linting and other issues.

### Submitting a Pull Request

1. Fork the repository and create a new branch for your contribution:

    ```bash
    git checkout -b feature-or-fix-branch
    ```

2. Make your changes and commit them:

    ```bash
    git add .
    git commit -am "Your meaningful commit message"
    ```

3. Push the changes to your fork:

    ```bash
    git push origin feature-or-fix-branch
    ```

4. Open a pull request on GitHub. Provide a clear title and description of your changes.


## Documentation

The [documentation](https://nneji123.github.io/ycombinator-scraper/) is made with [Material for MkDocs](https://github.com/squidfunk/mkdocs-material) and is hosted by [GitHub Pages](https://docs.github.com/en/pages).

## License

YCombinator-Scraper is distributed under the terms of the [MIT](./LICENSE) license.
