from fpdf import FPDF
from planner.styles import FONT_TITLE, FONT_BODY

def create_daily_page(pdf, date):
    pdf.add_page()
    pdf.set_font(*FONT_BODY)
    pdf.cell(0, 10, f"Daily Planner - {date}", ln=True, align='C')
    pdf.ln(10)  # Add spacing

    # Add sections
    pdf.cell(0, 10, "Top Priorities:", ln=True, align='L')
    pdf.cell(0, 10, "- [ ] Task 1", ln=True, align='L')
    pdf.cell(0, 10, "- [ ] Task 2", ln=True, align='L')
    pdf.cell(0, 10, "- [ ] Task 3", ln=True, align='L')

    pdf.ln(10)
    pdf.cell(0, 10, "Notes:", ln=True, align='L')
    pdf.ln(20)  # Leave space for notes

def create_weekly_overview(pdf, week_start_date):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    pdf.cell(0, 10, f"Weekly Overview - Starting {week_start_date}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font(*FONT_BODY)
    pdf.cell(0, 10, "Goals for the Week:", ln=True, align='L')
    pdf.cell(0, 10, "- [ ] Goal 1", ln=True, align='L')
    pdf.cell(0, 10, "- [ ] Goal 2", ln=True, align='L')

    pdf.ln(10)
    pdf.cell(0, 10, "Habit Tracker:", ln=True, align='L')
    pdf.cell(0, 10, "Day 1: [ ] | Day 2: [ ] | Day 3: [ ] | Day 4: [ ] | Day 5: [ ] | Day 6: [ ] | Day 7: [ ]", ln=True, align='L')

def create_monthly_title(pdf, month_name):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    pdf.cell(0, 10, f"{month_name}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font(*FONT_BODY)
    pdf.cell(0, 10, "Key Highlights for the Month:", ln=True, align='L')
    pdf.cell(0, 10, "- Highlight 1", ln=True, align='L')
    pdf.cell(0, 10, "- Highlight 2", ln=True, align='L')
    pdf.cell(0, 10, "- Highlight 3", ln=True, align='L')
