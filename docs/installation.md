# YCombinator-Scraper Installation Guide

## Installation from PyPI

### 1. Install the Package

```bash
pip install ycombinator-scraper
```

### 2. Export Configuration Variables (Optional)

Create a `.env` file in your project directory and set the following configuration variables:

```ini
login_username=your_workatastartup_username
login_password=your_workatastartup_password
logs_directory=/path/to/logs
headless_mode=True
```

Replace placeholders (`your_workatastartup_username`, `your_workatastartup_password`, `/path/to/logs`, `/path/to/chromedriver`) with your actual Workatastartup login credentials, desired logs directory, and the path to the ChromeDriver binary.

You can also export the environment variables. E.g `export login_username=/path/to/chromedriver"

**Note:** It's recommended to keep sensitive information like passwords in a secure manner. Do not share your `.env` file publicly.

### 3. Run the Scraper

You can now use the `ycombinator-scraper` command to run the scraper:

```bash
ycombinator-scraper
```

## Installation from Git

### 1. Clone the Repository

```bash
git clone https://github.com/Nneji123/ycombinator-scraper.git
```

### 2. Navigate to the Project Directory

```bash
cd ycombinator-scraper
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Export Configuration Variables (Optional)

Create a `.env` file in your project directory and set the same configuration variables as mentioned in the PyPI installation section.

### 5. Run the Scraper

You can run the `ycombinator-scraper` using the following command:

```bash
python -m ycombinator-scraper
```

## Using Docker

### 1. Build the Docker Image

```bash
docker build -t ycombinator-scraper .
```

### 2. Run the Docker Container

```bash
docker run -v /path/to/logs:/app/logs ycombinator-scraper
```

Replace `/path/to/logs` with the desired logs directory on your host machine.

### 3. Export Configuration Variables (Optional)

Create a `.env` file in the `/path/to/logs` directory on your host machine and set the same configuration variables as mentioned in the PyPI installation section.

Enjoy scraping company, job, and founder data from YCombinator's Workatastartup platform!
