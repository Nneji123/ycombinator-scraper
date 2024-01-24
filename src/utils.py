from typing import Dict, List

import pandas as pd


def write_json_to_csv(json_data: List[Dict], csv_filename: str) -> None:
    """
    Write JSON data to a CSV file using pandas.

    Parameters:
        json_data (List[Dict]): List of dictionaries representing the JSON data.
        csv_filename (str): Name of the CSV file to be created.

    Returns:
        None
    """
    df = pd.DataFrame(json_data)
    df.to_csv(csv_filename, index=False)
