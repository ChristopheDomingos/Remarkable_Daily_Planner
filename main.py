from fpdf import FPDF
from planner.templates import create_daily_page, create_weekly_overview, create_monthly_title

def main():
    # Initialize the PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Example: Generate a daily page
    create_daily_page(pdf, "2025-01-05")

    # Example: Generate a weekly overview
    create_weekly_overview(pdf, "2025-W01")

    # Example: Generate a monthly title page
    create_monthly_title(pdf, "January 2025")

    # Save the generated PDF
    output_file = "Remarkable_Daily_Planner_Output.pdf"
    pdf.output(output_file)
    print(f"PDF generated and saved as {output_file}")

if __name__ == "__main__":
    main()
