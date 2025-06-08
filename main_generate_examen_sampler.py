# -*- coding: utf-8 -*-
# Remarkable Daily Planner
# Version 2.3
#
# Created by: Christophe Domingos
# Date: June 3, 2025 # Updated
#
# Description: Script to generate yearly St. Ignatius Examen planners,
#              focusing on daily, weekly, and monthly reflection pages.
#              Monthly Examen page is now at the end of the month.

from fpdf import FPDF
from datetime import date, timedelta
import calendar as py_calendar # Renamed
import os

from planner.templates import (
    create_daily_reflection_page,
    create_weekly_examen_page,
    create_monthly_examen_page
)
from planner.styles import MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT

def generate_yearly_examen_planner_for_format(year_to_generate: int, page_format: str, base_output_directory: str = "generated_examen_planners"):
    """
    Generates a set of monthly St. Ignatius Examen PDF planners for a given year and page format.
    """
    print(f"\n--- Generating St. Ignatius Examen Planner for {year_to_generate} ({page_format}) ---")

    start_date_obj = date(year_to_generate, 1, 1)
    end_date_obj = date(year_to_generate, 12, 31)

    current_date = start_date_obj
    active_pdf = None
    current_pdf_month = -1
    current_pdf_year = -1

    year_dir = os.path.join(base_output_directory, str(year_to_generate))
    format_specific_dir = os.path.join(year_dir, page_format)

    if not os.path.exists(format_specific_dir):
        try:
            os.makedirs(format_specific_dir)
            print(f"Created output directory: {os.path.abspath(format_specific_dir)}")
        except OSError as e:
            print(f"Error creating output directory {format_specific_dir}: {e}")
            return

    print(f"Examen PDFs for {year_to_generate} ({page_format}) will be saved in: {os.path.abspath(format_specific_dir)}")

    while current_date <= end_date_obj:
        if current_date.month != current_pdf_month or current_date.year != current_pdf_year:
            if active_pdf is not None:
                # Add Monthly Examen for the completed month BEFORE saving
                completed_month_name = py_calendar.month_name[current_pdf_month]
                create_monthly_examen_page(active_pdf, completed_month_name, current_pdf_year) # Moved here
                
                try:
                    output_filename = f"{current_pdf_month:02d} - {completed_month_name}_Examen_{current_pdf_year}_{page_format}.pdf"
                except IndexError:
                    output_filename = f"Month_{current_pdf_month}_Examen_{current_pdf_year}_{page_format}.pdf"

                output_filepath = os.path.join(format_specific_dir, output_filename)
                try:
                    active_pdf.output(output_filepath)
                    print(f"Examen PDF for {completed_month_name} {current_pdf_year} ({page_format}) generated as {output_filepath}")
                except Exception as e:
                    print(f"Error saving Examen PDF {output_filepath}: {e}")

            current_pdf_month = current_date.month
            current_pdf_year = current_date.year
            # month_name_full = current_date.strftime("%B") # Not needed here for initial setup

            active_pdf = FPDF(orientation='P', unit='mm', format=page_format)
            active_pdf.set_auto_page_break(auto=True, margin=15)
            active_pdf.set_left_margin(MARGIN_LEFT)
            active_pdf.set_top_margin(MARGIN_TOP)
            active_pdf.set_right_margin(MARGIN_RIGHT)

            # First page in Examen sampler is a daily reflection page,
            # or weekly if it's a Monday. Monthly Examen is now at the end.
            # No specific first page like monthly overview needed here.

        if active_pdf and current_date.weekday() == 0: # Monday
            create_weekly_examen_page(active_pdf, current_date)

        if active_pdf:
            create_daily_reflection_page(active_pdf, current_date)

        current_date += timedelta(days=1)

    if active_pdf is not None:
        # Add Monthly Examen for the final completed month BEFORE saving
        final_month_name = py_calendar.month_name[current_pdf_month]
        create_monthly_examen_page(active_pdf, final_month_name, current_pdf_year) # Moved here

        try:
            output_filename = f"{current_pdf_month:02d} - {final_month_name}_Examen_{current_pdf_year}_{page_format}.pdf"
        except IndexError:
            output_filename = f"Month_{current_pdf_month}_Examen_{current_pdf_year}_{page_format}.pdf"

        output_filepath = os.path.join(format_specific_dir, output_filename)
        try:
            active_pdf.output(output_filepath)
            print(f"Examen PDF for {final_month_name} {current_pdf_year} ({page_format}) generated as {output_filepath}")
        except Exception as e:
            print(f"Error saving Examen PDF {output_filepath}: {e}")

    print(f"--- Finished generating St. Ignatius Examen Planner for {year_to_generate} ({page_format}) ---")


if __name__ == "__main__":
    print("Starting St. Ignatius Examen Planners generation (v2.3)...")

    years_to_generate = [2025, 2026]
    formats_to_generate = ['A4', 'A5']
    base_output_dir = "generated_examen_planners"

    for year in years_to_generate:
        for fmt in formats_to_generate:
            generate_yearly_examen_planner_for_format(year, fmt, base_output_dir)

    print("\nSt. Ignatius Examen Planners generation for all requested years and formats finished.")
    print("\nCrafted by: Christophe Domingos")