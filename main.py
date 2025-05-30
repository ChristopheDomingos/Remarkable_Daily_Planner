# -*- coding: utf-8 -*-
# Remarkable Daily Planner
# Version 2.2
#
# Created by: Christophe Domingos
# Date: May 30, 2025
#
# Description: Main script to generate monthly PDF planners with daily, weekly,
#              and monthly overview pages.

import calendar
from datetime import date, timedelta
from fpdf import FPDF
import os

from planner.templates import (
    create_daily_page,
    create_daily_reflection_page,
    create_weekly_overview,
    create_monthly_overview,
    create_weekly_examen_page,
    create_monthly_examen_page
)
from planner.styles import MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT

def generate_planner_for_format(start_date_obj: date, end_date_obj: date, page_format: str, base_output_directory: str):
    """
    Generates a set of monthly PDF planners for a given date range and page format.

    Each monthly PDF includes:
    - A monthly overview calendar with links to daily pages.
    - A monthly Examen page.
    - Weekly overview and Examen pages at the start of each week.
    - Daily planning and reflection pages for each day.
    """
    current_date = start_date_obj
    active_pdf = None
    current_pdf_month = -1
    current_pdf_year = -1

    daily_page_link_ids_for_current_month = {}
    calendar_page_internal_link_id = None

    year_dir = os.path.join(base_output_directory, str(start_date_obj.year))
    format_specific_dir = os.path.join(year_dir, page_format)

    if not os.path.exists(format_specific_dir):
        try:
            os.makedirs(format_specific_dir)
            print(f"Created output directory: {os.path.abspath(format_specific_dir)}")
        except OSError as e:
            print(f"Error creating output directory {format_specific_dir}: {e}")
            return

    print(f"PDFs for {page_format} will be saved in: {os.path.abspath(format_specific_dir)}")

    while current_date <= end_date_obj:
        # Start a new PDF if month or year changes
        if current_date.month != current_pdf_month or current_date.year != current_pdf_year:
            if active_pdf is not None:
                # Save the previously active PDF
                try:
                    month_name_to_save = calendar.month_name[current_pdf_month]
                    output_filename = f"{current_pdf_month:02d} - {month_name_to_save}_{current_pdf_year}_{page_format}.pdf"
                except IndexError:
                    output_filename = f"Month_{current_pdf_month}_{current_pdf_year}_{page_format}.pdf"

                output_filepath = os.path.join(format_specific_dir, output_filename)
                try:
                    active_pdf.output(output_filepath)
                    print(f"PDF for {month_name_to_save} {current_pdf_year} ({page_format}) generated as {output_filepath}")
                except Exception as e:
                    print(f"Error saving PDF {output_filepath}: {e}")

            # Initialize new PDF for the new month
            current_pdf_month = current_date.month
            current_pdf_year = current_date.year
            month_name_full = current_date.strftime("%B")
            daily_page_link_ids_for_current_month = {} # Reset links for the new month

            active_pdf = FPDF(orientation='P', unit='mm', format=page_format)
            active_pdf.set_auto_page_break(auto=True, margin=15)
            active_pdf.set_left_margin(MARGIN_LEFT)
            active_pdf.set_top_margin(MARGIN_TOP)
            active_pdf.set_right_margin(MARGIN_RIGHT)

            # Add link target for the calendar page itself for navigation
            calendar_page_internal_link_id = active_pdf.add_link()

            # Create initial pages for the month
            create_monthly_overview(active_pdf, current_pdf_year, current_pdf_month,
                                    daily_page_link_ids_for_current_month,
                                    calendar_page_internal_link_id)
            create_monthly_examen_page(active_pdf, month_name_full, current_pdf_year)

        # Add weekly pages at the start of each week (Monday)
        if active_pdf and current_date.weekday() == 0: # Monday
            create_weekly_overview(active_pdf, current_date)
            create_weekly_examen_page(active_pdf, current_date)

        # Add daily pages
        if active_pdf:
            target_id_for_this_daily_page = daily_page_link_ids_for_current_month.get(current_date)
            create_daily_page(active_pdf, current_date,
                              calendar_page_internal_link_id, # Link back to month calendar
                              target_id_for_this_daily_page)   # Link from calendar to this page
            create_daily_reflection_page(active_pdf, current_date)

        current_date += timedelta(days=1)

    # Save the last active PDF after the loop finishes
    if active_pdf is not None:
        try:
            month_name_to_save = calendar.month_name[current_pdf_month]
            output_filename = f"{current_pdf_month:02d} - {month_name_to_save}_{current_pdf_year}_{page_format}.pdf"
        except IndexError:
            output_filename = f"Month_{current_pdf_month}_{current_pdf_year}_{page_format}.pdf"

        output_filepath = os.path.join(format_specific_dir, output_filename)
        try:
            active_pdf.output(output_filepath)
            print(f"PDF for {month_name_to_save} {current_pdf_year} ({page_format}) generated as {output_filepath}")
        except Exception as e:
            print(f"Error saving PDF {output_filepath}: {e}")

if __name__ == "__main__":
    print("Starting PDF planner generation...")

    years_to_generate = [2025, 2026]  # Example: Generate for 2025 and 2026
    formats_to_generate = ['A4', 'A5'] # Supported page formats
    base_output_dir = "generated_planners"

    for year in years_to_generate:
        print(f"\n--- Generating Planner for {year} ---")
        for fmt in formats_to_generate:
            print(f"\n-- Generating {fmt} format --")
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)
            generate_planner_for_format(start_date, end_date, fmt, base_output_dir)
        print(f"--- Finished generating for {year} ---")

    print("\nPDF planner generation for all requested years and formats finished.")
    print("\nCrafted by: Christophe Domingos")