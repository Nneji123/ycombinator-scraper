import os

import pytest
from click.testing import CliRunner

from ycombinator_scraper.cli import cli
from ycombinator_scraper.scraper import Scraper


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def scraper(monkeypatch):
    scraper = Scraper()

    monkeypatch.setattr(scraper, "load_cookies", lambda: None)
    monkeypatch.setattr(scraper, "scrape_company_data", lambda url: {"dummy": "data"})
    monkeypatch.setattr(scraper, "scrape_job_data", lambda url: {"dummy": "data"})

    yield scraper


def test_version_command(runner):
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "YCombinator-Scraper CLI Tool v0.7.1" in result.output


def test_login_command(runner):
    # Mock user input for the login command
    username = "username"
    password = "password"

    result = runner.invoke(cli, ["login"], input=f"{username}\n{password}\n")
    assert result.exit_code == 1


def test_scrape_company_command_json_output(runner, tmp_path, monkeypatch, scraper):
    company_url = "https://www.workatastartup.com/companies/example"
    output_path = tmp_path / "output"
    output_path.mkdir()

    result = runner.invoke(
        cli,
        [
            "scrape-company",
            "--company-url",
            company_url,
            "--output-format",
            "json",
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0

    output_filename = f"scraped_company_data_{company_url.strip('https://www.workatastartup.com/companies/')}.json"
    assert os.path.exists(output_path / output_filename)


def test_scrape_founders_command_invalid_url(runner, scraper):
    invalid_url = "https://www.invalidurl.com"

    result = runner.invoke(cli, ["scrape-founders", "--company-url", invalid_url])
    assert result.exit_code == 0
