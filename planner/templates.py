from fpdf import FPDF
from planner.styles import FONT_TITLE, FONT_BODY

def create_daily_page(pdf, current_date):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    month = current_date.strftime("%B")
    date_str = current_date.strftime("%d/%m/%Y - %A")
    pdf.cell(0, 10, month, ln=True, align='C')
    pdf.cell(0, 10, date_str, ln=True, align='C')
    pdf.ln(10)

    pdf.set_font(*FONT_BODY)
    pdf.cell(0, 10, "Tasks:", ln=True)
    for _ in range(15):
        pdf.cell(0, 10, "-", ln=True)
    pdf.ln(10)

    pdf.cell(0, 10, "Notes:", ln=True)
    pdf.ln(40)  # Space for freeform notes

def create_weekly_overview(pdf, week_start_date):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    pdf.cell(0, 10, f"Weekly Overview - Starting {week_start_date.strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font(*FONT_BODY)
    pdf.cell(0, 10, "Goals for the Week:", ln=True)
    for _ in range(5):
        pdf.cell(0, 10, "-", ln=True)
    pdf.ln(10)

    pdf.cell(0, 10, "Habit Tracker:", ln=True)
    pdf.cell(0, 10, "Day 1: [ ] | Day 2: [ ] | Day 3: [ ] | Day 4: [ ] | Day 5: [ ] | Day 6: [ ] | Day 7: [ ]", ln=True)

def create_monthly_title(pdf, month_name):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    pdf.cell(0, 10, month_name, ln=True, align='C')
    pdf.ln(20)

    pdf.set_font(*FONT_BODY)
    pdf.cell(0, 10, "Key Highlights for the Month:", ln=True)
    for _ in range(5):
        pdf.cell(0, 10, "-", ln=True)
