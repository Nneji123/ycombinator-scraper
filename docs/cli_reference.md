# YCombinator-Scraper CLI Reference

The YCombinator-Scraper CLI provides commands for interacting with the scraping functionality. Below are the available commands along with their descriptions and options.

## Global Options

### `--help`

Displays information about available commands and their usage.

```bash
ycscraper --help
```

## `version`

Displays the version of the YCombinator-Scraper CLI.

```bash
ycscraper version
```

## `login`

Logs in to the Workatastartup platform.

```bash
ycscraper login --username <your_username> --password <your_password>
```

- `--username`: Your Workatastartup username.
- `--password`: Your Workatastartup password.

## `scrape-company`

Scrapes data for a specified company.

```bash
ycscraper scrape-company --company-url <company_url> --output-format <json/csv> --output-path <output_path>
```

- `--company-url`: URL of the company to scrape.
- `--output-format`: Output format (json or csv).
- `--output-path`: Output path for saved files.

## `scrape-job`

Scrapes data for a specified job.

```bash
ycsraper scrape-job --job-url <job_url> --output-format <json/csv> --output-path <output_path>
```

- `--job-url`: URL of the job to scrape.
- `--output-format`: Output format (json or csv).
- `--output-path`: Output path for saved files.

## `scrape-founders`

Scrapes data for the founders of a specified company.

```bash
ycscraper scrape-founders --company-url <company_url> --output-format <json/csv> --output-path <output_path>
```

- `--company-url`: URL of the company to scrape founders data.
- `--output-format`: Output format (json or csv).
- `--output-path`: Output path for saved files.


---

**Note:** Ensure you have configured the necessary settings either in a `.env` file or through environment variables.
