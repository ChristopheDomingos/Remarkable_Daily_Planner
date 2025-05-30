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
    current_date = start_date_obj
    active_pdf = None
    current_pdf_month = -1
    current_pdf_year = -1

    # Link management variables for the current monthly PDF
    daily_page_link_ids_for_current_month = {}
    calendar_page_internal_link_id = None

    # Create year-specific and format-specific output directory
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
        if current_date.month != current_pdf_month or current_date.year != current_pdf_year:
            if active_pdf is not None:
                try:
                    month_name_to_save = calendar.month_name[current_pdf_month]
                    output_filename = f"{current_pdf_month:02d} - {month_name_to_save}_{current_pdf_year}_{page_format}.pdf"
                except IndexError:
                    output_filename = f"Month_{current_pdf_month}_{current_pdf_year}_{page_format}.pdf"

                output_filepath = os.path.join(format_specific_dir, output_filename)
                try:
                    active_pdf.output(output_filepath, "F")
                    print(f"PDF for {month_name_to_save} {current_pdf_year} ({page_format}) generated as {output_filepath}")
                except Exception as e:
                    print(f"Error saving PDF {output_filepath}: {e}")

            # Reset for new month
            current_pdf_month = current_date.month
            current_pdf_year = current_date.year
            month_name_full = current_date.strftime("%B")
            daily_page_link_ids_for_current_month = {} # Reset for the new PDF

            active_pdf = FPDF(orientation='P', unit='mm', format=page_format)
            active_pdf.set_auto_page_break(auto=True, margin=15)
            active_pdf.set_left_margin(MARGIN_LEFT)
            active_pdf.set_top_margin(MARGIN_TOP)
            active_pdf.set_right_margin(MARGIN_RIGHT)

            # Create a link target for the calendar page (it's usually the first content page)
            calendar_page_internal_link_id = active_pdf.add_link()

            # Pass the link dict and the calendar link ID to the monthly overview
            create_monthly_overview(active_pdf, current_pdf_year, current_pdf_month,
                                    daily_page_link_ids_for_current_month,
                                    calendar_page_internal_link_id)
            create_monthly_examen_page(active_pdf, month_name_full, current_pdf_year)

        # --- Page Generation within the current month's PDF ---
        if active_pdf and current_date.weekday() == 0:
            create_weekly_overview(active_pdf, current_date)
            create_weekly_examen_page(active_pdf, current_date)

        if active_pdf:
            # Get the link_id that the calendar created *for this specific daily page*
            target_id_for_this_daily_page = daily_page_link_ids_for_current_month.get(current_date)

            create_daily_page(active_pdf, current_date,
                              calendar_page_internal_link_id, # Link to navigate *back to* calendar
                              target_id_for_this_daily_page)  # Link target *for this* daily page

            create_daily_reflection_page(active_pdf, current_date)

        current_date += timedelta(days=1)

    # Save the last PDF
    if active_pdf is not None:
        try:
            month_name_to_save = calendar.month_name[current_pdf_month]
            output_filename = f"{current_pdf_month:02d} - {month_name_to_save}_{current_pdf_year}_{page_format}.pdf"
        except IndexError:
            output_filename = f"Month_{current_pdf_month}_{current_pdf_year}_{page_format}.pdf"

        output_filepath = os.path.join(format_specific_dir, output_filename)
        try:
            active_pdf.output(output_filepath, "F")
            print(f"PDF for {month_name_to_save} {current_pdf_year} ({page_format}) generated as {output_filepath}")
        except Exception as e:
            print(f"Error saving PDF {output_filepath}: {e}")

if __name__ == "__main__":
    print("Starting PDF planner generation...")

    years_to_generate = [2025, 2026]
    formats_to_generate = ['A4','A5'] # Changed to A5 for Remarkable focus, add 'A4' if needed
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