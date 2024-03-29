# YCombinator-Scraper CLI Tool

## Version

```bash
ycscraper version
```

Display the version of the YCombinator-Scraper CLI tool.

## Login

```bash
ycscraper login
```

Log in to Workatastartup. You will be prompted to enter your username and password.

## Scrape Company Data

```bash
ycscraper scrape-company --company-url <company-url> --output-format <json/csv> --output-path <output-path>
```

Scrape data for a specific company.

- `--company-url`: URL of the company to scrape.
- `--output-format`: Output format (json or csv).
- `--output-path`: Output path for saved files.

## Scrape Job Data

```bash
ycscraper scrape-job --job-url <job-url> --output-format <json/csv> --output-path <output-path>
```

Scrape data for a specific job.

- `--job-url`: URL of the job to scrape.
- `--output-format`: Output format (json or csv).
- `--output-path`: Output path for saved files.

## Scrape Founders Data

```bash
ycscraper scrape-founders --company-url <company-url> --output-format <json/csv> --output-path <output-path>
```

Scrape founders data for a specific company.

- `--company-url`: URL of the company to scrape founders data.
- `--output-format`: Output format (json or csv).
- `--output-path`: Output path for saved files.
