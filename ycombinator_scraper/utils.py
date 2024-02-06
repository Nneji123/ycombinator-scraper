import re
from pathlib import Path
from typing import Dict, List

import pandas as pd
from bs4 import BeautifulSoup
from pydantic import BaseModel

from ycombinator_scraper.exceptions import InvalidURLException

OUTPUT_PATH = "output"


def validate_job_url(input_url: str) -> None:
    """Workatastartup.com url validator"""
    url_pattern = re.compile(r"https://www.workatastartup.com/jobs")
    if not url_pattern.match(input_url):
        raise InvalidURLException(input_url)


def validate_company_url(input_url: str) -> None:
    """Workatastartup.com url validator"""
    url_pattern = re.compile(r"https://www.workatastartup.com/companies")
    if not url_pattern.match(input_url):
        raise InvalidURLException(input_url)


def get_output_filename(
    output_path: Path, file_format: str, file_name: str, company_name: str
):
    # Get the current working directory
    current_directory = Path.cwd()

    # Create the output directory (if not exists) in the current working directory
    output_directory = current_directory / "output" / output_path
    output_directory.mkdir(parents=True, exist_ok=True)

    # Append company name to the file name
    modified_file_name = f"{file_name}_{company_name}"

    # Construct the full file path
    return output_directory / f"{modified_file_name}.{file_format}"


def strip_html_tags(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()


def write_json_to_csv(json_data: List[Dict], csv_filename: str) -> None:
    df = pd.DataFrame(json_data)
    df.to_csv(csv_filename, index=False)


def generate_csv_from_pydantic_data(data: List[BaseModel], file_path: str) -> None:
    if not data:
        raise ValueError("Data list is empty")

    data_dicts = [item.model_dump() for item in data]
    df = pd.DataFrame(data_dicts)
    df.to_csv(file_path, index=False)
