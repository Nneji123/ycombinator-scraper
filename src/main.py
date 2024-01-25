from dotenv import load_dotenv

from config.config import Settings
from src.ycombinator_scraper.scraper import login


def main():
    # Load environment variables from .env
    load_dotenv()

    # Load settings using Pydantic
    settings = Settings()

    login("Nneji123", "linda321")
    # Scrape job data
    # json_data = scrape_jobs_in_parallel(settings.username, settings.password)

    # # Write JSON data to a CSV file
    # write_json_to_csv(json_data, settings.csv_filename)

    # # Generate emails
    # emails = generate_emails(json_data)

    # # Send emails
    # send_emails(emails, settings.smtp_server, settings.smtp_port, settings.smtp_username, settings.smtp_password)


if __name__ == "__main__":
    main()
