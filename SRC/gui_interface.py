# gui_interface.py

"""Graphical User Interface (GUI) for the Business Report Generator application."""

import os
import re
import sys
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from loader import load_data
from report_builder import build_report_data
from report_generator import generate_report
from exporter import export_report
from constants import SECTIONS_INTERFACE, FORMATS #, CATEGORIES
from data_helpers import get_categories, get_months



# --- GRAPHICAL INTERFACE (GUI) ---


class BusinessReportGUI:
    """
    Graphical User Interface (GUI) for the Business Report Generator application.

    Manages user interactions, file selection, report configuration,
    and triggering report generation and export.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initializes the BusinessReportGUI.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("BUSINESS REPORT GENERATOR - PROFESSIONAL PANEL")
        self.root.geometry("600x550")
        self.file_path = tk.StringVar()

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the user interface elements and their layout."""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # 1. File Selection
        ttk.Label(main_frame, text="1. Select CSV File", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Entry(file_frame, textvariable=self.file_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Open", command=self.browse_file).pack(side=tk.RIGHT)

        # 2. Sections Selection
        ttk.Label(main_frame, text="2. Report Sections", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
        self.section_vars = {}
        for key, label in SECTIONS_INTERFACE:
            var = tk.BooleanVar()
            ttk.Checkbutton(main_frame, text=label, variable=var).pack(anchor=tk.W, padx=10)
            self.section_vars[key] = var
        # 3. Filters
        ttk.Label(main_frame, text="3. Filter Values (Optional)", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W, pady=(15, 5))
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Category:").grid(row=0, column=0, sticky=tk.W)
        self.cat_combo = ttk.Combobox(filter_frame, values=[], state="readonly")
        self.cat_combo.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        ttk.Label(filter_frame, text="Month (YYYY-MM):").grid(row=1, column=0, sticky=tk.W)
        self.month_entry = ttk.Combobox(filter_frame, values=[], state="readonly")
        self.month_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        filter_frame.columnconfigure(1, weight=1)

        # 4. Export Format
        ttk.Label(main_frame, text="4. Export Format", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.format_combo = ttk.Combobox(main_frame, values=FORMATS, state="readonly")
        self.format_combo.set("PDF")
        self.format_combo.pack(fill=tk.X, pady=(0, 20))
        # 5. Action Button
        self.gen_button = ttk.Button(main_frame, text="GENERATE REPORT", command=self.run_process)
        self.gen_button.pack(fill=tk.X, ipady=10)

    def browse_file(self) -> None:
        """
        Opens a file dialog for the user to select a CSV file.
        If a file is selected, it loads the data, extracts categories and months,
        and populates the respective comboboxes.
        """
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename: 
            self.file_path.set(filename)
            df = load_data(filename)
            if df is None:
                return
            # Populate category and month comboboxes
            categories = get_categories(df)
            months = get_months(df)
            self.cat_combo["values"] = categories
            self.month_entry["values"] = months

            if categories:
                self.cat_combo.set(categories[0])
            if months:
                self.month_entry.set(months[0])

    def run_process(self) -> None:
        """
        Executes the report generation process.

        This method performs the following steps:
        1. Validates if a file has been selected.
        2. Loads data from the selected CSV file.
        3. Gathers selected report sections and filter values from the GUI.
        4. Performs validation for month input if a month filter is selected.
        5. Builds the report data using `report_builder`.
        6. Generates the report string using `report_generator`.
        7. Exports the report to the chosen format using `exporter`.
        8. Displays success or error messages to the user.
        9. Attempts to open the 'Reports' directory after successful generation.
        """
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file.")
            return
        try:
            df = load_data(self.file_path.get())
            if df is None:
                return
            selected_sections = [k for k, v in self.section_vars.items() if v.get()]
            month_input = self.month_entry.get().strip()

            # Month validation
            if "filtered_month" in selected_sections and month_input:
                if not re.match(r"^\d{4}-\d{2}$", month_input):
                    messagebox.showerror("Validation Error", "Invalid month format. Please use YYYY-MM (e.g., 2023-01).")
                    return
                try:
                    datetime.strptime(month_input, "%Y-%m")
                except ValueError:
                    messagebox.showerror("Validation Error", "Invalid month. Please enter a valid month (e.g., 2023-01).")
                    return
                unique_months = df['month'].unique()
                if month_input not in unique_months:
                    messagebox.showerror("Validation Error", f"Month '{month_input}' not found in the data.")
                    return
            report_request = {"sections": selected_sections, "category": self.cat_combo.get(), "month": month_input}
            report_data = build_report_data(df, report_request)
            report_string = generate_report(report_data)
            fmt = self.format_combo.get()
            export_report(report_data, report_string, fmt)
            messagebox.showinfo("Success", f"Report exported as {fmt}!")
            reports_path = os.path.abspath("Reports") # Open the folder cross-platform
            try:
                if sys.platform == "win32":
                    os.startfile(reports_path)
                elif sys.platform == "darwin":      # macOS
                    subprocess.run(["open", reports_path], check=False)
                else:                               # Linux and others
                    subprocess.run(["xdg-open", reports_path], check=False)
            except Exception:
                messagebox.showinfo("Report Generated", f"Report saved in:\n{reports_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))