#constants.py
"""Module containing constants used across the Business Report Generator application."""

SECTIONS_INTERFACE = [
            ("categories", "Total by Category"),
            ("months", "Total by Month"),
            ("total", "Grand Total"),
            ("filtered_category", "Filter by Category"),
            ("filtered_month", "Filter by Month")
        ]

SECTIONS = ["categories", "months", "total", "filtered_category", "filtered_month"]

FORMATS = ["PDF", "Excel", "TXT", "CSV", "HTML"]