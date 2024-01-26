# YCombinator-Scraper CLI Tool

## Version

```bash
yc_scraper version
```

Display the version of the YCombinator-Scraper CLI tool.

## Login

```bash
yc_scraper login
```

Log in to Workatastartup. You will be prompted to enter your username and password.

## Scrape Company Data

```bash
yc_scraper scrape-company --company-url <company-url> --output-format <json/csv> --output-path <output-path>
```

Scrape data for a specific company.

- `--company-url`: URL of the company to scrape.
- `--output-format`: Output format (json or csv).
- `--output-path`: Output path for saved files.

## Scrape Job Data

```bash
yc_scraper scrape-job --job-url <job-url> --output-format <json/csv> --output-path <output-path>
```

Scrape data for a specific job.

- `--job-url`: URL of the job to scrape.
- `--output-format`: Output format (json or csv).
- `--output-path`: Output path for saved files.

## Scrape Founders Data

```bash
yc_scraper scrape-founders --company-url <company-url> --output-format <json/csv> --output-path <output-path>
```

Scrape founders data for a specific company.

- `--company-url`: URL of the company to scrape founders data.
- `--output-format`: Output format (json or csv).
- `--output-path`: Output path for saved files.

## Interactive Mode

```bash
yc_scraper interactive
```

Enter interactive mode to manually input commands. Type 'exit' to leave the interactive mode.
