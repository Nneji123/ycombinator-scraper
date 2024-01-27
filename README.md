# YCombinator-Scraper

<div align="center">

<img src="./docs/img/logo.svg" alt="Ycombinator_Scraper logo" width="200" height="200" role="img">

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/tests.yml/badge.svg)](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/tests.yml) [![CI - Codecov](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/codecov.yml/badge.svg)](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/codecov.yml) [![CD - Build and Push Docker Image](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/docker-image.yml) [![Bump and Release](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/release.yml/badge.svg)](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/release.yml) |
| Docs | [![Docs](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/docs.yml/badge.svg)](https://github.com/Nneji123/ycombinator-scraper/actions/workflows/docs.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/ycombinator-scraper.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/ycombinator-scraper/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/ycombinator-scraper.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/ycombinator-scraper/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ycombinator-scraper.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/ycombinator-scraper/) |
| Meta |  [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](./LICENSE) |

</div>

-----

YCombinator-Scraper provides a web scraping tool for extracting data from [Workatastartup](https://www.workatastartup.com/) website. The package uses Selenium and BeautifulSoup to navigate through the pages and extract information.

---

**Documentation**: <a href="https://nneji123.github.io/ycombinator_scraper" target="_blank">https://nneji123.github.io/ycombinator_scraper</a>

**Source Code**: <a href="https://github.com/nneji123/ycombinator_scraper" target="_blank">https://github.com/nneji123/ycombinator_scraper</a>

---

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
$ ycombinator_scraper --help

# Output
YCombinator-Scraper Version 0.6.0
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

```bash
ycscraper scrape-company --company-url https://www.workatastartup.com/company/example-inc
```

This command will scrape data for the specified company and save it in the default output format (JSON).

## Example 2: Scrape Job Data using CLI

```bash
ycscraper scrape-job --job-url https://www.workatastartup.com/job/example-job
```

This command will scrape data for the specified job and save it in the default output format (JSON).

## Example 3: Scrape Founder Data using CLI

```bash
ycscraper scrape-founders --company-url https://www.workatastartup.com/company/example-inc
```

This command will scrape founder data for the specified company and save it in the default output format (JSON).

## Example 4: Scrape Company Data using Python Package

```python
from ycombinator_scraper import Scraper

scraper = Scraper()
company_data = scraper.scrape_company_data("https://www.workatastartup.com/company/example-inc")
print(company_data.model_dump_json(indent=2))
```

Pydantic is used under the hood so methods like `model_dump_json` are available for all the scraped data.

## Documentation

The [documentation](https://nneji123.github.io/ycombinator_scraper/) is made with [Material for MkDocs](https://github.com/squidfunk/mkdocs-material) and is hosted by [GitHub Pages](https://docs.github.com/en/pages).

## License

YCombinator-Scraper is distributed under the terms of the [MIT](./LICENSE) license.
