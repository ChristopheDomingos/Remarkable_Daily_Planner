from __future__ import annotations

import logging
import os
from datetime import date, timedelta

from fpdf import FPDF

from planner.config import month_name
from planner.rendering.pdf_factory import make_pdf

# Import the templates module and feature-detect available functions.
# This lets the generator work even if some examen helpers are not implemented.
import planner.templates as T  # type: ignore

# Soft capabilities
HAS_DAILY_EXAMEN = hasattr(T, "create_daily_examen_page")
HAS_WEEKLY_EXAMEN = hasattr(T, "create_weekly_examen_page")
HAS_MONTHLY_EXAMEN = hasattr(T, "create_monthly_examen_page")

if not HAS_MONTHLY_EXAMEN:
    raise ImportError(
        "planner.templates must define 'create_monthly_examen_page' for the examen generator."
    )

def _ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def generate_year_for_format(
    year: int,
    page_format: str,
    base_output_dir: str,
    cfg: dict,
) -> None:
    """Generate an Examen-only planner for the given year and page format.

    Behavior adapts to available template functions:
      - If T.create_daily_examen_page exists -> add a daily examen page for each day.
      - If T.create_weekly_examen_page exists -> add a weekly examen page on Mondays.
      - Always add a monthly examen page at the start and end of each month.
    """
    margins = cfg.get("margins", {})
    locale_code = cfg.get("locale", "en_US")

    outdir = os.path.join(base_output_dir, str(year), page_format)
    _ensure_dir(outdir)

    for month in range(1, 13):
        pdf: FPDF = make_pdf(page_format, margins)
        month_label = month_name(locale_code, month)

        # Monthly Examen intro/overview (required)
        T.create_monthly_examen_page(pdf, month_label, year)

        d = date(year, month, 1)
        while d.month == month:
            # Optional daily examen
            if HAS_DAILY_EXAMEN:
                T.create_daily_examen_page(pdf, d)

            # Optional weekly examen (Mondays)
            if HAS_WEEKLY_EXAMEN and d.weekday() == 0:
                T.create_weekly_examen_page(pdf, d)

            d += timedelta(days=1)

        # Monthly Examen summary/end (required)
        T.create_monthly_examen_page(pdf, month_label, year)

        out_name = f"{month:02d} - {month_label}_{year}_{page_format}.pdf"
        out_path = os.path.join(outdir, out_name)
        try:
            pdf.output(out_path)
            logging.info("Saved %s", out_path)
        except Exception as e:
            logging.error("Failed to save %s: %s", out_path, e)
            raise
