#processor

"""Process the data based on the configuration and prepare it for report generation"""
import pandas as pd
from typing import Union


def calculate_total(df: pd.DataFrame) -> float:
    """
    Calculates the sum of the 'amount' column in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing an 'amount' column.

    Returns:
        float: The grand total of all amounts.
    """
    return df["amount"].sum()


def total_by_category(df: pd.DataFrame) -> pd.Series:
    """
    Calculates the total amount for each category.

    Args:
        df (pd.DataFrame): The input DataFrame containing 'category' and 'amount' columns.

    Returns:
        pd.Series: A Series where the index is the category and values are the total amounts.
    """
    return df.groupby("category")["amount"].sum()


def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    Filters the DataFrame to include only rows belonging to a specific category.

    Args:
        df (pd.DataFrame): The input DataFrame containing a 'category' column.
        category (str): The category name to filter by.

    Returns:
        pd.DataFrame: A new DataFrame containing only the rows for the specified category.
    """
    return df[df["category"] == category]


def filter_by_month(df: pd.DataFrame, month: str) -> pd.DataFrame:
    """
    Filters the DataFrame to include only rows belonging to a specific month.

    Args:
        df (pd.DataFrame): The input DataFrame containing a 'month' column (YYYY-MM format).
        month (str): The month string (YYYY-MM) to filter by.

    Returns:
        pd.DataFrame: A new DataFrame containing only the rows for the specified month.
    """
    return df[df["month"] == month]


def total_by_month(df: pd.DataFrame) -> pd.Series:
    """
    Calculates the total amount for each month.

    Args:
        df (pd.DataFrame): The input DataFrame containing 'month' and 'amount' columns.

    Returns:
        pd.Series: A Series where the index is the month (YYYY-MM) and values are the total amounts.
    """
    return df.groupby("month")["amount"].sum()