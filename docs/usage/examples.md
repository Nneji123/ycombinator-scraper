# Examples

This section provides some examples of how to use the YCombinator-Scraper tool and package in different scenarios.

## Example 1: Scrape Company Data using CLI

```bash
yc-scraper scrape-company --company-url https://www.workatastartup.com/company/example-inc
```

This command will scrape data for the specified company and save it in the default output format (JSON).

## Example 2: Scrape Job Data using CLI

```bash
yc-scraper scrape-job --job-url https://www.workatastartup.com/job/example-job
```

This command will scrape data for the specified job and save it in the default output format (JSON).

## Example 3: Scrape Founder Data using CLI

```bash
yc-scraper scrape-founders --company-url https://www.workatastartup.com/company/example-inc
```

This command will scrape founder data for the specified company and save it in the default output format (JSON).

## Example 4: Scrape Company Data using Python Package

```python
from ycombinator_scraper.scraper import Scraper

scraper = Scraper()
company_data = scraper.scrape_company_data("https://www.workatastartup.com/company/example-inc")
print(company_data.model_dump_json(indent=2))
```

This Python script demonstrates how to use the YCombinator-Scraper package to scrape company data.
