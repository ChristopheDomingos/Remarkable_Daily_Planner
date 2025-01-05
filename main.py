from fpdf import FPDF
from planner.templates import (
    create_daily_page,
    create_weekly_overview,
    create_monthly_title
)
from planner.styles import MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT
from datetime import date, timedelta

def generate_planner(start_date, end_date):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(MARGIN_LEFT)
    pdf.set_top_margin(MARGIN_TOP)
    pdf.set_right_margin(MARGIN_RIGHT)

    current_date = start_date

    while current_date <= end_date:
        # Monthly title page
        if current_date.day == 1:
            create_monthly_title(pdf, current_date.strftime("%B %Y"))

        # Weekly overview page
        if current_date.weekday() == 0:  # Monday
            create_weekly_overview(pdf, current_date)

        # Daily page
        create_daily_page(pdf, current_date)

        current_date += timedelta(days=1)

    # Save the generated PDF
    output_file = "Remarkable_Daily_Planner_Output.pdf"
    pdf.output(output_file)
    print(f"PDF generated and saved as {output_file}")

if __name__ == "__main__":
    # Generate planner for the entire year 2025
    generate_planner(date(2025, 1, 1), date(2025, 12, 31))

