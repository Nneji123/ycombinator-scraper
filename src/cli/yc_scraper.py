import os
import click
from src.scraping import (
    scrape_company_data,
    scrape_founders_data,
    scrape_job_data,
    initialize_driver,
    login,
    save_cookies,
    load_cookies,
)
from config.config import Settings
import pandas as pd
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

settings = Settings()

# Configure logging with loguru
logger.add("logs/{time:YYYY-MM-DD}.log", rotation="1 day", level="INFO")

OUTPUT_PATH = "output"

@click.group()
def cli():
    pass

def get_output_filename(output_path, file_format, file_name):
    output_directory = os.path.join(OUTPUT_PATH, output_path)
    os.makedirs(output_directory, exist_ok=True)
    return os.path.join(output_directory, f"{file_name}.{file_format}")

@cli.command()
def version():
    click.echo("Your CLI Tool v1.0.0")


@cli.command()
@click.option('--username', prompt=True, help='Your Workatastartup username')
@click.option('--password', prompt=True, hide_input=True, help='Your Workatastartup password')
def login_command(username, password):
    driver = initialize_driver()
    if login(driver, username, password):
        save_cookies(driver)
        logger.success("Successfully logged in!")
    driver.quit()

@cli.command()
@click.option('--company-url', prompt=True, help='URL of the company to scrape')
@click.option('--output-format', type=click.Choice(['json', 'csv']), default='json', help='Output format (json or csv)')
@click.option('--output-path', type=click.Path(), default='.', help='Output path for saved files')
def scrape_company_command(company_url, output_format, output_path):
    driver = initialize_driver()
    load_cookies(driver)
    company_data = scrape_company_data(driver, company_url)

    output_filename = get_output_filename(output_path, output_format, "scraped_company_data")
    
    if output_format == 'json':
        with open(output_filename, 'w') as json_file:
            json_file.write(company_data.json(indent=2))
    elif output_format == 'csv':
        df = pd.DataFrame([company_data.dict()])
        df.to_csv(output_filename, index=False)
    
    logger.success(f'Data saved as {output_format.upper()}: {output_filename}')
    driver.quit()

@cli.command()
@click.option('--job-url', prompt=True, help='URL of the job to scrape')
@click.option('--output-format', type=click.Choice(['json', 'csv']), default='json', help='Output format (json or csv)')
@click.option('--output-path', type=click.Path(), default='.', help='Output path for saved files')
def scrape_job_command(job_url, output_format, output_path):
    driver = initialize_driver()
    load_cookies(driver)
    job_data = scrape_job_data(driver, job_url)

    output_filename = get_output_filename(output_path, output_format, "scraped_job_data")
    
    if output_format == 'json':
        with open(output_filename, 'w') as json_file:
            json_file.write(job_data.json(indent=2))
    elif output_format == 'csv':
        df = pd.DataFrame([job_data.dict()])
        df.to_csv(output_filename, index=False)
    
    logger.success(f'Data saved as {output_format.upper()}: {output_filename}')
    driver.quit()

@cli.command()
@click.option('--company-url', prompt=True, help='URL of the company to scrape founders data')
@click.option('--output-format', type=click.Choice(['json', 'csv']), default='json', help='Output format (json or csv)')
@click.option('--output-path', type=click.Path(), default='.', help='Output path for saved files')
def scrape_founders_command(company_url, output_format, output_path):
    driver = initialize_driver()
    load_cookies(driver)
    founders_data = scrape_founders_data(driver, company_url)

    for i, founder in enumerate(founders_data):
        output_filename = get_output_filename(output_path, output_format, f"scraped_founder_data_{i+1}")
        
        if output_format == 'json':
            with open(output_filename, 'w') as json_file:
                json_file.write(founder.json(indent=2))
        elif output_format == 'csv':
            df = pd.DataFrame([founder.dict()])
            df.to_csv(output_filename, index=False)
        
        logger.success(f'Data saved as {output_format.upper()}: {output_filename}')

    driver.quit()

@cli.command()
@click.option('--username', prompt=True, help='Your Workatastartup username')
@click.option('--password', prompt=True, hide_input=True, help='Your Workatastartup password')
@click.option('--output-format', type=click.Choice(['json', 'csv']), default='json', help='Output format (json or csv)')
@click.option('--output-path', type=click.Path(), default='.', help='Output path for saved files')
def scrape_all_command(username, password, output_format, output_path):
    driver = initialize_driver()
    if login(driver, username, password):
        save_cookies(driver)

        company_urls = ["company_url_1", "company_url_2"]  # Add actual URLs
        job_urls = ["job_url_1", "job_url_2"]  # Add actual URLs
        founders_urls = ["founders_url_1", "founders_url_2"]  # Add actual URLs

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(scrape_company_data, driver, company_urls, output_format, output_path))
            results += list(executor.map(scrape_job_data, driver, job_urls, output_format, output_path))
            results += list(executor.map(scrape_founders_data, driver, founders_urls, output_format, output_path))

        logger.success("Scraping completed successfully!")

    driver.quit()
@cli.command()
def interactive():
    click.echo("Entering interactive mode. Type 'exit' to leave.")
    while True:
        command = click.prompt("Enter a command", type=str)
        if command.lower() == 'exit':
            click.echo("Exiting interactive mode.")
            break
        else:
            click.echo(f"Invalid command: {command}")

if __name__ == '__main__':
    cli()
              
