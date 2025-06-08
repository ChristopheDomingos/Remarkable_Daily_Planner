# -*- coding: utf-8 -*-
# Remarkable Daily Planner
# Version 2.3
#
# Created by: Christophe Domingos
# Date: June 3, 2025 # Updated

import calendar as py_calendar
from datetime import date, timedelta
from fpdf import FPDF
import os

from planner.templates import (
    create_daily_page,
    create_daily_reflection_page,
    create_weekly_overview,
    create_monthly_overview,
    create_weekly_examen_page,
    create_monthly_examen_page,
    ALL_CATHOLIC_QUOTES 
)
from planner.styles import MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT

# No apply_calendar_links function needed with direct linking in create_monthly_overview

def generate_planner_for_format(start_date_obj: date, end_date_obj: date, page_format: str, base_output_directory: str):
    current_date = start_date_obj
    active_pdf = None
    current_pdf_month = -1
    current_pdf_year = -1
    
    daily_page_link_ids_for_current_month = {} 
    weekly_page_link_ids_for_current_month = {} 
    calendar_page_internal_link_id = None 

    year_dir = os.path.join(base_output_directory, str(start_date_obj.year))
    format_specific_dir = os.path.join(year_dir, page_format)
    if not os.path.exists(format_specific_dir):
        try:
            os.makedirs(format_specific_dir)
        except OSError as e:
            print(f"Error creating output directory {format_specific_dir}: {e}")
            return
    print(f"PDFs for {page_format} will be saved in: {os.path.abspath(format_specific_dir)}")

    while current_date <= end_date_obj:
        if current_date.month != current_pdf_month or current_date.year != current_pdf_year:
            if active_pdf is not None:
                completed_month_name = py_calendar.month_name[current_pdf_month]
                create_monthly_examen_page(active_pdf, completed_month_name, current_pdf_year)
                output_filename = f"{current_pdf_month:02d} - {completed_month_name}_{current_pdf_year}_{page_format}.pdf"
                output_filepath = os.path.join(format_specific_dir, output_filename)
                try:
                    active_pdf.output(output_filepath)
                    print(f"PDF for {completed_month_name} {current_pdf_year} ({page_format}) generated as {output_filepath}")
                except Exception as e:
                    print(f"Error saving PDF {output_filepath}: {e}")

            current_pdf_month = current_date.month
            current_pdf_year = current_date.year
            daily_page_link_ids_for_current_month = {} 
            weekly_page_link_ids_for_current_month = {} 

            active_pdf = FPDF(orientation='P', unit='mm', format=page_format)
            active_pdf.set_left_margin(MARGIN_LEFT)
            active_pdf.set_top_margin(MARGIN_TOP)
            active_pdf.set_right_margin(MARGIN_RIGHT)
            active_pdf.set_auto_page_break(auto=True, margin= getattr(active_pdf, 'b_margin', 15) if getattr(active_pdf, 'b_margin', 15) > 0 else 15)
            
            calendar_page_internal_link_id = active_pdf.add_link() 
            
            create_monthly_overview(active_pdf, current_pdf_year, current_pdf_month,
                                    daily_page_link_ids_for_current_month, 
                                    calendar_page_internal_link_id)

        if active_pdf:
            if current_date.weekday() == 0: 
                weekly_link_id = active_pdf.add_link()
                weekly_page_link_ids_for_current_month[current_date] = weekly_link_id
                create_weekly_overview(active_pdf, current_date, 
                                       calendar_page_internal_link_id, 
                                       weekly_link_id)    
                create_weekly_examen_page(active_pdf, current_date)

            daily_link_target_id = daily_page_link_ids_for_current_month.get(current_date)
            create_daily_page(active_pdf, current_date,
                              calendar_page_internal_link_id, 
                              daily_link_target_id) 
            create_daily_reflection_page(active_pdf, current_date)
        else: 
            print(f"CRITICAL Error: active_pdf is None at date {current_date}. Aborting.")
            return

        current_date += timedelta(days=1)

    if active_pdf is not None:
        final_month_name = py_calendar.month_name[current_pdf_month]
        create_monthly_examen_page(active_pdf, final_month_name, current_pdf_year)
        output_filename = f"{current_pdf_month:02d} - {final_month_name}_{current_pdf_year}_{page_format}.pdf"
        output_filepath = os.path.join(format_specific_dir, output_filename)
        try:
            active_pdf.output(output_filepath)
            print(f"PDF for {final_month_name} {current_pdf_year} ({page_format}) generated as {output_filepath}")
        except Exception as e:
            print(f"Error saving PDF {output_filepath}: {e}")

if __name__ == "__main__":
    print("Starting PDF planner generation (v2.5.1 - Extended Year/Format Config)...") # Version updated
    
    # Updated years and formats to generate
    years_to_generate = [2025, 2026] 
    formats_to_generate = ['A4', 'A5'] 
    
    base_output_dir = "generated_planners"

    for year in years_to_generate:
        print(f"\n--- Generating Planner for {year} ---")
        for fmt in formats_to_generate:
            print(f"\n-- Generating {fmt} format --")
            start_date_val = date(year, 1, 1) 
            end_date_val = date(year, 12, 31) # Ensure full year generation 
            generate_planner_for_format(start_date_val, end_date_val, fmt, base_output_dir)
        print(f"--- Finished generating for {year} ---")

    print("\nPDF planner generation for all requested years and formats finished.")
    print("\nCrafted by: Christophe Domingos")