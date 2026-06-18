#report_builder.py

"""Main module to build the report by integrating data loading, processing, and exporting."""

import pandas as pd
from processor import total_by_category, total_by_month, filter_by_category, filter_by_month, calculate_total
from typing import Dict, Any, List


def build_report_data(df: pd.DataFrame, report_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Builds the report data based on the selected sections and filters.

    Args:
        df (pd.DataFrame): The input DataFrame containing the business data.
        report_request (Dict[str, Any]): A dictionary specifying the requested
                                         report sections and filter criteria.

    Returns:
        Dict[str, Any]: A dictionary containing the processed data for the report.
    """
    report_data: Dict[str, Any] = {}
    selected_sections = report_request["sections"]
    
    if "categories" in selected_sections:
        report_data["categories"] = total_by_category(df)

    if "months" in selected_sections:
        report_data["months"] = total_by_month(df)

    if "total" in selected_sections:
        report_data["total"] = calculate_total(df)

    if "filtered_category" in selected_sections:
        category = report_request["category"]
        report_data["filtered_category"] = filter_by_category(df, category)
        report_data["selected_category"] = category

    if "filtered_month" in selected_sections:
        month = report_request["month"]
        report_data["filtered_month"] = filter_by_month(df, month)
        report_data["selected_month"] = month
    
    return report_data