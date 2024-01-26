import os
from typing import Dict, List
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup

OUTPUT_PATH = Path("./output")


def get_output_filename(output_path, file_format, file_name):
    output_directory = os.path.join(OUTPUT_PATH, output_path)
    os.makedirs(output_directory, exist_ok=True)
    return os.path.join(output_directory, f"{file_name}.{file_format}")


def strip_html_tags(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()


def write_json_to_csv(json_data: List[Dict], csv_filename: str) -> None:
    df = pd.DataFrame(json_data)
    df.to_csv(csv_filename, index=False)


def generate_csv_from_pydantic_data(data: List[BaseModel], file_path: str):
    if not data:
        raise ValueError("Data list is empty")

    data_dicts = [item.model_dump() for item in data]

    df = pd.DataFrame(data_dicts)

    df.to_csv(file_path, index=False)
