#data_helpers

import pandas as pd
from typing import List


def get_categories(df: pd.DataFrame) -> List[str]:
    """
    Extracts and returns a sorted list of unique categories from the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing a 'category' column.

    Returns:
        List[str]: A sorted list of unique category names.
    """
    return sorted(df["category"].unique().tolist())


def get_months(df: pd.DataFrame) -> List[str]:
    """
    Extracts and returns a sorted list of unique months (YYYY-MM format) from the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing a 'month' column.

    Returns:
        List[str]: A sorted list of unique month strings.
    """
    months = sorted(df["month"].unique().tolist())
    return months
