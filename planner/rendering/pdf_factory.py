from __future__ import annotations
from typing import Dict, Any
from fpdf import FPDF

def make_pdf(fmt: str, margins: Dict[str, Any]) -> FPDF:
    left   = float(margins.get("left", 10))
    top    = float(margins.get("top", 15))
    right  = float(margins.get("right", 10))
    bottom = float(margins.get("bottom", 15))

    pdf = FPDF(orientation="P", unit="mm", format=fmt)
    pdf.set_left_margin(left)
    pdf.set_top_margin(top)
    pdf.set_right_margin(right)
    pdf.set_auto_page_break(auto=True, margin=bottom)

    # If/when you switch to a Unicode TTF (e.g., Noto Sans), register it here once.
    # pdf.add_font("NotoSans", "", "NotoSans-Regular.ttf", uni=True)
    # pdf.set_font("NotoSans", size=12)

    return pdf
