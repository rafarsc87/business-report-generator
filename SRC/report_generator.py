#report_generator

"""Generates the final report based on the processed data."""
import pandas as pd
from typing import Dict, Any, List


def generate_report(report_data: Dict[str, Any]) -> str:
    """
    Generates the report as a human-readable, formatted string based on the processed report data.

    Args:
        report_data (Dict[str, Any]): A dictionary containing the processed data
                                      for various report sections (e.g., totals,
                                      filtered dataframes).

    Returns:
        str: A multi-line string representing the complete business report.
    """
    
    report_lines = []

    report_lines.append("=" * 40)
    report_lines.append("BUSINESS REPORT")
    report_lines.append("=" * 40)
    report_lines.append("") # Empty line

    if "total" in report_data:
        report_lines.append("GRAND TOTAL")
        report_lines.append("-" * 40)
        report_lines.append(f"{report_data['total']:.2f}")
        report_lines.append("") # Empty line
        report_lines.append("") # Empty line

    if "categories" in report_data:
        report_lines.append("TOTAL BY CATEGORY")
        report_lines.append("-" * 40)
        for category, amount in report_data["categories"].items():
            report_lines.append(f"{category:<14} : {amount:.2f}")
        report_lines.append("") # Empty line
        report_lines.append("") # Empty line

    if "months" in report_data:
        report_lines.append("TOTAL BY MONTH")
        report_lines.append("-" * 40)
        for month, amount in report_data["months"].items():
            report_lines.append(f"{month:<14} : {amount:.2f}")
        report_lines.append("") # Empty line
        report_lines.append("") # Empty line

    if "filtered_category" in report_data:
        report_lines.append(f"FILTERED BY CATEGORY: {report_data.get('selected_category', 'N/A')}")
        report_lines.append("-" * 40)
        df: pd.DataFrame = report_data["filtered_category"]
        report_lines.append(f"{'DATE':<12} | {'CATEGORY':<14} | {'AMOUNT':<10} | {'DESCRIPTION'}")
        for _, row in df.iterrows():
            report_lines.append(f"{row['date'].strftime('%Y-%m-%d'):<12} | {row['category']:<14} | {row['amount']:<10.2f} | {row['description']}")
        report_lines.append("") # Empty line
        report_lines.append("") # Empty line

    if "filtered_month" in report_data:
        report_lines.append(f"FILTERED BY MONTH: {report_data.get('selected_month', 'N/A')}")
        report_lines.append("-" * 40)
        df: pd.DataFrame = report_data["filtered_month"]
        report_lines.append(f"{'DATE':<12} | {'CATEGORY':<14} | {'AMOUNT':<10} | {'DESCRIPTION'}")
        for _, row in df.iterrows():
            report_lines.append(f"{row['date'].strftime('%Y-%m-%d'):<12} | {row['category']:<14} | {row['amount']:<10.2f} | {row['description']}")
        report_lines.append("") # Empty line
        report_lines.append("") # Empty line

    return "\n".join(report_lines)