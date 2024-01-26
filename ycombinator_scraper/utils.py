import os
import time
from pathlib import Path
from typing import Dict, List

import pandas as pd
from bs4 import BeautifulSoup
from pydantic import BaseModel

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


# TODO: Update Scraper to use functool lru_cache
cache_store = {}


def timed_cache(seconds: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = (func, args, frozenset(kwargs.items()))
            current_time = time.time()

            # Check if the result is in the cache and not expired
            if (
                key in cache_store
                and current_time - cache_store[key]["timestamp"] < seconds
            ):
                return cache_store[key]["value"]

            # If not in cache or expired, compute the result and update the cache
            result = func(*args, **kwargs)
            cache_store[key] = {"value": result, "timestamp": current_time}
            return result

        return wrapper

    return decorator
