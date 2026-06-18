import os
from loader import load_data
from report_builder import build_report_data
from report_generator import generate_report
from input_handler import get_report_request, get_file_format
from exporter import export_report

import pandas as pd
from typing import Tuple, Dict, Any, Optional

# --- TERMINAL INTERFACE (CLI) ---


def terminal_entry_menu() -> Optional[Tuple[pd.DataFrame, Dict[str, Any], str]]:
    """
    Presents a terminal menu to the user for input and report configuration.

    Prompts for CSV file path, report sections, filters, and export format.

    Returns:
        Optional[Tuple[pd.DataFrame, Dict[str, Any], str]]: A tuple containing
        the loaded DataFrame, report request dictionary, and export format string,
        or None if an error occurs or file is not found.
    """
    print("\n" + "="*50)
    print("      BUSINESS REPORT GENERATOR - TERMINAL")
    print("="*50 + "\n")
    
    file_path = input("Enter the path of the CSV file (e.g., data/sample_data.csv): ").strip()
    
    if not os.path.exists(file_path):
        terminal_exit_menu(False, f"File '{file_path}' not found.")
        return None

    df = load_data(file_path)
    if df is None:
        return None

    print("\n--- Report Configuration ---")
    report_request = get_report_request(df)
    
    print("\n--- Export Configuration ---")
    export_format = get_file_format()
    
    return df, report_request, export_format


def terminal_exit_menu(success: bool, message: str = "") -> None:
    """
    Displays an exit message in the terminal indicating success or failure.

    Args:
        success (bool): True if the operation was successful, False otherwise.
        message (str): A descriptive message to display to the user.
    """
    if success:
        print(f"\n✅ SUCCESS: {message}")
    else:
        print(f"\n❌ ERROR: {message}")
    print("\n" + "="*50 + "\n")


def run_terminal_interface() -> None:
    """
    Runs the complete business report generation flow through the terminal interface.

    This function orchestrates the process from user input to report generation
    and export, handling potential exceptions.
    """
    data = terminal_entry_menu()
    if data:
        df, report_request, export_format = data
        try:
            report_data = build_report_data(df, report_request)
            report_string = generate_report(report_data)
            export_report(report_data, report_string, export_format)
            terminal_exit_menu(True, f"Report generated in 'Reports/' as {export_format}.")
        except Exception as e:
            terminal_exit_menu(False, str(e))