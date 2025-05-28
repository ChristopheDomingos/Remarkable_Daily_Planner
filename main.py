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

def generate_planner(start_date_obj: date, end_date_obj: date, output_directory: str = "generated_planners"):
    current_date = start_date_obj
    active_pdf = None
    current_pdf_month = -1
    current_pdf_year = -1

    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
            print(f"Created output directory: {os.path.abspath(output_directory)}")
        except OSError as e:
            print(f"Error creating output directory {output_directory}: {e}")
            return 

    print(f"PDFs will be saved in: {os.path.abspath(output_directory)}")

    while current_date <= end_date_obj:
        if current_date.month != current_pdf_month or current_date.year != current_pdf_year:
            if active_pdf is not None:
                try:
                    month_name_to_save = calendar.month_name[current_pdf_month]
                    # MODIFIED: Add month number to filename
                    output_filename = f"{current_pdf_month} - {month_name_to_save}_{current_pdf_year}.pdf"
                except IndexError: 
                    # Fallback if current_pdf_month is somehow invalid (e.g. 0 or >12)
                    # Though this should not happen with correct logic.
                    output_filename = f"Month_{current_pdf_month}_{current_pdf_year}.pdf" 
                
                output_filepath = os.path.join(output_directory, output_filename)
                try:
                    active_pdf.output(output_filepath, "F")
                    print(f"PDF for {month_name_to_save} {current_pdf_year} generated as {output_filepath}")
                except Exception as e:
                    print(f"Error saving PDF {output_filepath}: {e}")

            current_pdf_month = current_date.month
            current_pdf_year = current_date.year
            month_name_full = current_date.strftime("%B") 

            active_pdf = FPDF()
            active_pdf.set_auto_page_break(auto=True, margin=15) 
            active_pdf.set_left_margin(MARGIN_LEFT)
            active_pdf.set_top_margin(MARGIN_TOP)
            active_pdf.set_right_margin(MARGIN_RIGHT)
            
            create_monthly_overview(active_pdf, current_pdf_year, current_pdf_month) 
            create_monthly_examen_page(active_pdf, month_name_full, current_pdf_year)

        if active_pdf and current_date.weekday() == 0: 
            create_weekly_overview(active_pdf, current_date)
            create_weekly_examen_page(active_pdf, current_date)
        
        if active_pdf: 
            create_daily_page(active_pdf, current_date)
            create_daily_reflection_page(active_pdf, current_date)
        
        current_date += timedelta(days=1)

    if active_pdf is not None:
        try:
            month_name_to_save = calendar.month_name[current_pdf_month]
            # MODIFIED: Add month number to filename for the last PDF
            output_filename = f"{current_pdf_month} - {month_name_to_save}_{current_pdf_year}.pdf"
        except IndexError:
            output_filename = f"Month_{current_pdf_month}_{current_pdf_year}.pdf"

        output_filepath = os.path.join(output_directory, output_filename)
        try:
            active_pdf.output(output_filepath, "F")
            print(f"PDF for {month_name_to_save} {current_pdf_year} generated as {output_filepath}")
        except Exception as e:
            print(f"Error saving PDF {output_filepath}: {e}")

if __name__ == "__main__":
    print("Starting PDF planner generation...")
    
    planner_start_date = date(2025, 1, 1)
    planner_end_date = date(2025, 12, 31) 

    generate_planner(planner_start_date, planner_end_date, output_directory="generated_planners")
    print("PDF planner generation finished.")