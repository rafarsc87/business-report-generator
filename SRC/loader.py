#loader

import pandas as pd
from typing import Optional


def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Loads data from a CSV file into a pandas DataFrame.

    It expects the CSV to have a 'date' column which will be converted to datetime objects,
    and a 'month' column (YYYY-MM format) will be derived from it.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: The loaded DataFrame with 'date' and 'month' columns,
                                or None if an error occurs during loading.
    """
    try:
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.strftime("%Y-%m")
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None