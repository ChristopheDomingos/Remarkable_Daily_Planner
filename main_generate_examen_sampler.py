# generate_examen_planners.py
from fpdf import FPDF
from datetime import date, timedelta
import calendar
import os

from planner.templates import (
    create_daily_reflection_page, 
    create_weekly_examen_page,
    create_monthly_examen_page
)
from planner.styles import MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT

def generate_yearly_examen_planner_for_format(year_to_generate: int, page_format: str, base_output_directory: str = "generated_examen_planners"):
    print(f"\n--- Generating St. Ignatius Examen Planner for {year_to_generate} ({page_format}) ---")

    start_date_obj = date(year_to_generate, 1, 1)
    end_date_obj = date(year_to_generate, 12, 31)
    
    current_date = start_date_obj
    active_pdf = None
    current_pdf_month = -1
    current_pdf_year = -1 # Should be same as year_to_generate

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
        if current_date.month != current_pdf_month or current_date.year != current_pdf_year: # current_pdf_year check is belt-and-suspenders here
            if active_pdf is not None:
                try:
                    month_name_to_save = calendar.month_name[current_pdf_month]
                    output_filename = f"{current_pdf_month:02d} - {month_name_to_save}_Examen_{current_pdf_year}_{page_format}.pdf"
                except IndexError: 
                    output_filename = f"Month_{current_pdf_month}_Examen_{current_pdf_year}_{page_format}.pdf" 
                
                output_filepath = os.path.join(format_specific_dir, output_filename)
                try:
                    active_pdf.output(output_filepath, "F")
                    print(f"Examen PDF for {month_name_to_save} {current_pdf_year} ({page_format}) generated as {output_filepath}")
                except Exception as e:
                    print(f"Error saving Examen PDF {output_filepath}: {e}")

            current_pdf_month = current_date.month
            current_pdf_year = current_date.year 
            month_name_full = current_date.strftime("%B") 

            active_pdf = FPDF(orientation='P', unit='mm', format=page_format) # Set page format
            active_pdf.set_auto_page_break(auto=True, margin=15) 
            active_pdf.set_left_margin(MARGIN_LEFT)
            active_pdf.set_top_margin(MARGIN_TOP)
            active_pdf.set_right_margin(MARGIN_RIGHT)
            
            if current_date.day == 1: 
                create_monthly_examen_page(active_pdf, month_name_full, current_pdf_year)

        if active_pdf and current_date.weekday() == 0: 
            create_weekly_examen_page(active_pdf, current_date)
        
        if active_pdf: 
            create_daily_reflection_page(active_pdf, current_date)
        
        current_date += timedelta(days=1)

    if active_pdf is not None:
        try:
            month_name_to_save = calendar.month_name[current_pdf_month]
            output_filename = f"{current_pdf_month:02d} - {month_name_to_save}_Examen_{current_pdf_year}_{page_format}.pdf"
        except IndexError:
            output_filename = f"Month_{current_pdf_month}_Examen_{current_pdf_year}_{page_format}.pdf"

        output_filepath = os.path.join(format_specific_dir, output_filename)
        try:
            active_pdf.output(output_filepath, "F")
            print(f"Examen PDF for {month_name_to_save} {current_pdf_year} ({page_format}) generated as {output_filepath}")
        except Exception as e:
            print(f"Error saving Examen PDF {output_filepath}: {e}")
    
    print(f"--- Finished generating St. Ignatius Examen Planner for {year_to_generate} ({page_format}) ---")


if __name__ == "__main__":
    print("Starting St. Ignatius Examen Planners generation...")
    
    years_to_generate = [2025, 2026]
    formats_to_generate = ['A4', 'A5'] # A5 is good for Remarkable
    base_output_dir = "generated_examen_planners"

    for year in years_to_generate:
        for fmt in formats_to_generate:
            generate_yearly_examen_planner_for_format(year, fmt, base_output_dir)
    
    print("\nSt. Ignatius Examen Planners generation for all requested years and formats finished.")