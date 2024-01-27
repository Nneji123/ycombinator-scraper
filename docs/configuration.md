# YCombinator-Scraper Configuration

## Overview

The `YCombinator-Scraper` configuration file (`config.py`) allows you to customize various settings for the scraper. This file uses Pydantic for configuration validation and allows you to define settings such as login credentials, logs directory, headless mode, and the path to the ChromeDriver binary.

## Configuration Options

### 1. `login_username` (str)

Your Workatastartup username.

### 2. `login_password` (str)

Your Workatastartup password.

### 3. `logs_directory` (Path)

The directory where log files will be stored. Default is "./logs".

## Example Configuration

```ini
# .env

login_username=your_username
login_password=your_password
```

**Note:** Replace `"your_username"` and `"your_password"` with your actual Workatastartup username and password. Adjust other settings as needed.

## Configuration Validation

The configuration file uses Pydantic to validate and parse the settings. If there are any issues with the configuration, an error will be raised, providing information on the problem.

Ensure that you configure the settings correctly to avoid any disruptions in the scraping process.

For more information on Pydantic configuration and validation, refer to the [official documentation](https://pydantic-docs.helpmanual.io/).

**Note:** Do not share your login credentials or sensitive information publicly. Keep your configuration files secure.
