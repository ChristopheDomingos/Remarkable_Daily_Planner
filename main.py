import calendar
from datetime import date, timedelta
from fpdf import FPDF
from planner.templates import (
    create_daily_page,
    create_weekly_overview,
    create_monthly_title
)
from planner.styles import MARGIN_LEFT, MARGIN_TOP, MARGIN_RIGHT

def generate_planner(start_date: date, end_date: date) -> None:
    current_date = start_date
    while current_date <= end_date:
        month_name = current_date.strftime("%B")
        year = current_date.year
        month = current_date.month
        _, last_day = calendar.monthrange(year, month)

        # Create a new PDF for the current month
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_left_margin(MARGIN_LEFT)
        pdf.set_top_margin(MARGIN_TOP)
        pdf.set_right_margin(MARGIN_RIGHT)
        pdf.set_font('Arial', size=12)

        # Generate pages for the current month
        while current_date.day <= last_day and current_date.month == month:
            if current_date.day == 1:
                create_monthly_title(pdf, f"{month_name} {year}")
            if current_date.weekday() == 0:  # Monday
                create_weekly_overview(pdf, current_date)
            create_daily_page(pdf, current_date)
            current_date += timedelta(days=1)
            if current_date > end_date:
                break

        output_file = f"{month_name}_{year}.pdf"
        pdf.output(output_file)
        print(f"PDF for {month_name} {year} generated as {output_file}")

if __name__ == "__main__":
    generate_planner(date(2025, 1, 1), date(2025, 12, 31))