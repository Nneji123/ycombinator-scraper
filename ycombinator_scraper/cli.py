from datetime import datetime

import click
import pandas as pd
from loguru import logger

from .config import Settings
from .scraper import Scraper
from .utils import get_output_filename

settings = Settings()
scraper = Scraper()

# Create a 'logs' directory if it doesn't exist
log_directory = settings.logs_directory
log_directory.mkdir(exist_ok=True)
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = log_directory / f"log_{timestamp_str}.log"
logger.add(log_file_path, rotation="1 day", level="INFO")


@click.group()
def cli():
    pass


@cli.command()
def version():
    click.echo("YCombinator-Scraper CLI Tool v0.5.0")


@cli.command()
@click.option("--username", prompt=True, help="Your Workatastartup username")
@click.option(
    "--password", prompt=True, hide_input=True, help="Your Workatastartup password"
)
def login(username, password):
    if scraper.login(username, password):
        scraper.save_cookies()


@cli.command()
@click.option("--company-url", prompt=True, help="URL of the company to scrape")
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format (json or csv)",
)
@click.option(
    "--output-path", type=click.Path(), default=".", help="Output path for saved files"
)
def scrape_company(company_url, output_format, output_path):
    scraper.load_cookies()
    company_data = scraper.scrape_company_data(company_url)

    output_filename = get_output_filename(
        output_path, output_format, "scraped_company_data"
    )

    if output_format == "json":
        with open(output_filename, "w") as json_file:
            json_file.write(company_data.model_dump_json(indent=2))
    elif output_format == "csv":
        df = pd.DataFrame([company_data.model_dump()])
        df.to_csv(output_filename, index=False)

    logger.success(f"Data saved as {output_format.upper()}: {output_filename}")


@cli.command()
@click.option("--job-url", prompt=True, help="URL of the job to scrape")
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format (json or csv)",
)
@click.option(
    "--output-path", type=click.Path(), default=".", help="Output path for saved files"
)
def scrape_job(job_url, output_format, output_path):
    scraper.load_cookies()
    job_data = scraper.scrape_job_data(job_url)

    output_filename = get_output_filename(
        output_path, output_format, "scraped_job_data"
    )

    if output_format == "json":
        with open(output_filename, "w") as json_file:
            json_file.write(job_data.model_dump_json(indent=2))
    elif output_format == "csv":
        df = pd.DataFrame([job_data.model_dump()])
        df.to_csv(output_filename, index=False)

    logger.success(f"Data saved as {output_format.upper()}: {output_filename}")


@cli.command()
@click.option(
    "--company-url", prompt=True, help="URL of the company to scrape founders data"
)
@click.option(
    "--output-format",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Output format (json or csv)",
)
@click.option(
    "--output-path", type=click.Path(), default=".", help="Output path for saved files"
)
def scrape_founders(company_url, output_format, output_path):
    scraper.load_cookies()
    founders_data = scraper.scrape_founders_data(company_url)

    all_founders_data = []  # Accumulate all founders' data in this list

    for i, founder in enumerate(founders_data):
        all_founders_data.append(founder.model_dump())

    output_filename = get_output_filename(
        output_path, output_format, "scraped_founder_data"
    )

    if output_format == "json":
        with open(output_filename, "w") as json_file:
            json_file.write(all_founders_data)

    elif output_format == "csv":
        df = pd.DataFrame(all_founders_data)
        df.to_csv(output_filename, index=False)

    logger.success(f"Data saved as {output_format.upper()}: {output_filename}")


if __name__ == "__main__":
    cli()
