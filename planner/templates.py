from fpdf import FPDF
from planner.styles import FONT_TITLE, FONT_BODY

def create_daily_page(pdf, current_date):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)

    # Header: Month and Date
    month = current_date.strftime("%B")
    date_str = current_date.strftime("%d/%m/%Y - %A")
    pdf.cell(0, 10, month, ln=True, align='C')
    pdf.cell(0, 10, date_str, ln=True, align='C')
    pdf.ln(5)

    # Tasks Section
    pdf.set_font(*FONT_BODY)
    pdf.cell(0, 8, "Tasks:", ln=True)
    for _ in range(15):  # Adjusted to fit 15 tasks
        pdf.cell(5, 6, "-")  # Add "-" marker
        pdf.ln(3)  # Compact space for writing
        x_start = pdf.get_x() + 10
        y = pdf.get_y()
        pdf.line(x_start, y + 2, x_start + 180, y + 2)  # Line below the writing space
        pdf.ln(6)  # Compact space between lines

    # Notes Section
    pdf.cell(0, 8, "Notes:", ln=True)
    pdf.ln(8)  # Increased space below "Notes:" heading
    for _ in range(5):  # Adjusted to fit 5 lines of notes
        y = pdf.get_y()
        pdf.line(pdf.get_x(), y + 2, pdf.get_x() + 180, y + 2)
        pdf.ln(10)  # Space between notes lines

def create_weekly_overview(pdf, week_start_date):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    pdf.cell(0, 10, f"Weekly Overview - Starting {week_start_date.strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font(*FONT_BODY)
    pdf.cell(0, 10, "Goals for the Week:", ln=True)
    for _ in range(5):  # Fit 5 goals per weekly overview
        pdf.cell(5, 6, "-")  # Add "-" marker
        pdf.ln(3)  # Compact space for writing
        x_start = pdf.get_x() + 10
        y = pdf.get_y()
        pdf.line(x_start, y + 2, x_start + 180, y + 2)  # Line below the writing space
        pdf.ln(6)

    pdf.cell(0, 10, "Habit Tracker:", ln=True)
    pdf.cell(0, 10, "Day 1: [ ] | Day 2: [ ] | Day 3: [ ] | Day 4: [ ] | Day 5: [ ] | Day 6: [ ] | Day 7: [ ]", ln=True)

def create_monthly_title(pdf, month_name):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    pdf.cell(0, 10, month_name, ln=True, align='C')
    pdf.ln(20)

    pdf.set_font(*FONT_BODY)
    pdf.cell(0, 10, "Key Highlights for the Month:", ln=True)
    for _ in range(5):  # Fit 5 highlights per monthly overview
        pdf.cell(5, 6, "-")  # Add "-" marker
        pdf.ln(3)  # Compact space for writing
        x_start = pdf.get_x() + 10
        y = pdf.get_y()
        pdf.line(x_start, y + 2, x_start + 180, y + 2)  # Line below the writing space
        pdf.ln(6)




