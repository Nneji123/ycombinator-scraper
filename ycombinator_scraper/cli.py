import click
from datetime import datetime
from . import scraper, utils, config
import pandas as pd
from loguru import logger


settings = config.Settings()
cli_scraper = scraper.Scraper()

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
    click.echo("YCombinator-Scraper CLI Tool v0.2.0")


@cli.command()
@click.option("--username", prompt=True, help="Your Workatastartup username")
@click.option(
    "--password", prompt=True, hide_input=True, help="Your Workatastartup password"
)
def login_command(username, password):
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
def scrape_company_command(company_url, output_format, output_path):
    scraper.load_cookies()
    company_data = scraper.scrape_company_data(company_url)

    output_filename = utils.get_output_filename(
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
def scrape_job_command(job_url, output_format, output_path):
    scraper.load_cookies()
    job_data = scraper.scrape_job_data(job_url)

    output_filename = utils.get_output_filename(
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
def scrape_founders_command(company_url, output_format, output_path):
    scraper.load_cookies()
    founders_data = scraper.scrape_founders_data(company_url)

    for i, founder in enumerate(founders_data):
        output_filename = utils.get_output_filename(
            output_path, output_format, f"scraped_founder_data_{i+1}"
        )

        if output_format == "json":
            with open(output_filename, "w") as json_file:
                json_file.write(founder.model_dump_json(indent=2))
        elif output_format == "csv":
            df = pd.DataFrame([founder.model_dump()])
            df.to_csv(output_filename, index=False)

        logger.success(f"Data saved as {output_format.upper()}: {output_filename}")


@cli.command()
def interactive():
    click.echo("Entering interactive mode. Type 'exit' to leave.")
    while True:
        command = click.prompt("Enter a command", type=str)
        if command.lower() == "exit":
            click.echo("Exiting interactive mode.")
            break
        else:
            click.echo(f"Invalid command: {command}")


if __name__ == "__main__":
    print("YCombinator-Scraper Version 0.2.0")
    cli()
