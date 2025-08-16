from __future__ import annotations
from datetime import date, timedelta
from typing import Dict
from fpdf import FPDF

def iter_month_days(y: int, m: int):
    d = date(y, m, 1)
    while d.month == m:
        yield d
        d += timedelta(days=1)

def preallocate_month_links(pdf: FPDF, y: int, m: int) -> tuple[Dict[date,int], int]:
    daily = {d: pdf.add_link() for d in iter_month_days(y, m)}
    calendar_link = pdf.add_link()
    return daily, calendar_link
