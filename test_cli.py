import os

import pytest
from click.testing import CliRunner

from ycombinator_scraper.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_version_command(runner):
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "YCombinator-Scraper CLI Tool v0.7.1" in result.output


def test_login_command(runner, monkeypatch):
    # Mock user input for the login command
    monkeypatch.setattr("builtins.input", lambda _: "username")
    monkeypatch.setattr("getpass.getpass", lambda _: "password")

    result = runner.invoke(cli, ["login"])
    assert result.exit_code == 0
    assert "Successfully logged in" in result.output


def test_scrape_company_command_json_output(runner, tmp_path):
    company_url = "https://www.workatastartup.com/companies/vocode"
    output_path = tmp_path / "output"
    output_path.mkdir()

    result = runner.invoke(
        cli,
        [
            "scrape_company",
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


def test_scrape_job_command_csv_output(runner, tmp_path):
    job_url = "https://www.workatastartup.com/jobs/61924"
    output_path = tmp_path / "output"
    output_path.mkdir()

    result = runner.invoke(
        cli,
        [
            "scrape_job",
            "--job-url",
            job_url,
            "--output-format",
            "csv",
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0

    output_filename = "scraped_job_data.csv"
    assert os.path.exists(output_path / output_filename)


def test_scrape_founders_command_invalid_url(runner):
    invalid_url = "https://www.invalidurl.com"

    result = runner.invoke(cli, ["scrape_founders", "--company-url", invalid_url])
    assert result.exit_code != 0
    assert "Invalid company URL" in result.output
