#input_handler

"""Responsible for showing the user options and prompting for a choice."""

import pandas as pd
from constants import SECTIONS, FORMATS
from data_helpers import get_categories, get_months
from loader import load_data
from typing import Dict, Any, Optional, List


def get_report_request(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Prompts the user in the terminal to select which sections to include in the report
    and any necessary filters (category or month).

    Args:
        df (pd.DataFrame): The DataFrame containing the data, used to retrieve
                           available categories and months for filtering.

    Returns:
        Dict[str, Any]: A dictionary containing:
                        - "sections": A list of selected section keys (e.g., "total", "categories").
                        - "category": The chosen category string for filtering, or None.
                        - "month": The chosen month string (YYYY-MM) for filtering, or None.
    """
    category = None
    month = None 

    print("Select sections to include in the report (comma separated):")
    for i, section in enumerate(SECTIONS, 1):
        print(f"{i}. {section.replace('_', ' ').title()}")

    while True:
        choices = input("Enter the numbers corresponding to your choices (e.g., 1,3,5): ")
        selected = choices.split(",")
        if all(choice.strip() in [str(i) for i in range(1, len(SECTIONS) + 1)] for choice in selected):
            break
        else:
            print("Invalid input. Please enter valid numbers separated by commas.")
        
    if "4" in selected:
        categories = get_categories(df)
        print("Available categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        category = input("Enter the category to filter by: ")
        # Basic validation for category input (can be enhanced)
        if category not in categories:
            print(f"Warning: Category '{category}' not found in data. Filter may yield no results.")

    if "5" in selected:
        months = get_months(df)
        print("Available months:")
        for i, month in enumerate(months, 1):
            print(f"{i}. {month}")
        month = input("Enter the month to filter by (YYYY-MM format): ")
        # Basic validation for month input (can be enhanced)
        if month not in months:
            print(f"Warning: Month '{month}' not found in data. Filter may yield no results.")

    return {
        "sections": [SECTIONS[int(choice.strip()) - 1] for choice in selected],
        "category": category,
        "month": month
    }


def get_file_format() -> str:
    """
    Prompts the user in the terminal to select a file format for the report.

    Returns:
        str: The selected file format (e.g., "PDF", "Excel").
    """
    formats = FORMATS
    print("Select a file format for the report:")
    for i, fmt in enumerate(formats, 1):
        print(f"{i}. {fmt}")
    
    while True:
        choice = input("Enter the number corresponding to your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(formats):
            return formats[int(choice) - 1]
        else:
            print("Invalid choice. Please try again.")