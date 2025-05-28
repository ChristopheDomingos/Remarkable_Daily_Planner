# generate_examen_planners.py
from fpdf import FPDF
from datetime import date, timedelta
import calendar
import os

# Ensure your planner package is accessible
from planner.templates import (
    create_daily_reflection_page, # This is the Daily Particular Examen
    create_weekly_examen_page,
    create_monthly_examen_page
)
from planner.styles import MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT

def generate_yearly_examen_planner(year_to_generate: int, base_output_directory: str = "generated_examen_planners"):
    """
    Generates a yearly planner containing only the St. Ignatius Examen pages.
    Each month will be a separate PDF file saved in a year-specific subdirectory.
    """
    print(f"\n--- Generating St. Ignatius Examen Planner for {year_to_generate} ---")

    start_date_obj = date(year_to_generate, 1, 1)
    end_date_obj = date(year_to_generate, 12, 31)
    
    current_date = start_date_obj
    active_pdf = None
    current_pdf_month = -1
    current_pdf_year = -1

    # Create year-specific output directory
    year_output_directory = os.path.join(base_output_directory, str(year_to_generate))
    if not os.path.exists(year_output_directory):
        try:
            os.makedirs(year_output_directory)
            print(f"Created output directory: {os.path.abspath(year_output_directory)}")
        except OSError as e:
            print(f"Error creating output directory {year_output_directory}: {e}")
            return 

    print(f"Examen PDFs for {year_to_generate} will be saved in: {os.path.abspath(year_output_directory)}")

    while current_date <= end_date_obj:
        if current_date.month != current_pdf_month or current_date.year != current_pdf_year:
            # Save the previous month's PDF if it exists
            if active_pdf is not None:
                try:
                    month_name_to_save = calendar.month_name[current_pdf_month]
                    output_filename = f"{current_pdf_month:02d} - {month_name_to_save}_Examen_{current_pdf_year}.pdf"
                except IndexError: 
                    output_filename = f"Month_{current_pdf_month}_Examen_{current_pdf_year}.pdf" 
                
                output_filepath = os.path.join(year_output_directory, output_filename)
                try:
                    active_pdf.output(output_filepath, "F")
                    print(f"Examen PDF for {month_name_to_save} {current_pdf_year} generated as {output_filepath}")
                except Exception as e:
                    print(f"Error saving Examen PDF {output_filepath}: {e}")

            # Start a new PDF for the new month
            current_pdf_month = current_date.month
            current_pdf_year = current_date.year # Should always be year_to_generate
            month_name_full = current_date.strftime("%B") 

            active_pdf = FPDF()
            active_pdf.set_auto_page_break(auto=True, margin=15) 
            active_pdf.set_left_margin(MARGIN_LEFT)
            active_pdf.set_top_margin(MARGIN_TOP)
            active_pdf.set_right_margin(MARGIN_RIGHT)
            
            # Add Monthly General Examen Page at the start of the month's PDF
            if current_date.day == 1: # Ensure it's added only once per month
                create_monthly_examen_page(active_pdf, month_name_full, current_pdf_year)

        # Add Weekly General Examen on Mondays
        if active_pdf and current_date.weekday() == 0: # 0 is Monday
            create_weekly_examen_page(active_pdf, current_date)
        
        # Add Daily Particular Examen Page
        if active_pdf: 
            create_daily_reflection_page(active_pdf, current_date)
        
        current_date += timedelta(days=1)

    # Save the very last PDF if it exists
    if active_pdf is not None:
        try:
            month_name_to_save = calendar.month_name[current_pdf_month]
            output_filename = f"{current_pdf_month:02d} - {month_name_to_save}_Examen_{current_pdf_year}.pdf"
        except IndexError:
            output_filename = f"Month_{current_pdf_month}_Examen_{current_pdf_year}.pdf"

        output_filepath = os.path.join(year_output_directory, output_filename)
        try:
            active_pdf.output(output_filepath, "F")
            print(f"Examen PDF for {month_name_to_save} {current_pdf_year} generated as {output_filepath}")
        except Exception as e:
            print(f"Error saving Examen PDF {output_filepath}: {e}")
    
    print(f"--- Finished generating St. Ignatius Examen Planner for {year_to_generate} ---")


if __name__ == "__main__":
    print("Starting St. Ignatius Examen Planners generation...")
    
    generate_yearly_examen_planner(2025)
    generate_yearly_examen_planner(2026)
    
    print("\nSt. Ignatius Examen Planners generation for all requested years finished.")