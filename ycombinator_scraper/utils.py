from typing import Dict, List
from pydantic import BaseModel
import pandas as pd


def write_json_to_csv(json_data: List[Dict], csv_filename: str) -> None:
    df = pd.DataFrame(json_data)
    df.to_csv(csv_filename, index=False)


def generate_csv_from_pydantic_data(data: List[BaseModel], file_path: str):
    if not data:
        raise ValueError("Data list is empty")

    data_dicts = [item.dict() for item in data]

    df = pd.DataFrame(data_dicts)

    df.to_csv(file_path, index=False)
