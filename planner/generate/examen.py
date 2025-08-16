from __future__ import annotations

import logging
import os
from datetime import date, timedelta

from fpdf import FPDF

from remarkable_planner.config import load_config, month_name
from remarkable_planner.rendering.pdf_factory import make_pdf

from planner.templates import (
    create_weekly_examen_page,
    create_daily_examen_page,
    create_monthly_examen_page,
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
    margins = cfg.get("margins", {})
    locale_code = cfg.get("locale", "en_US")

    outdir = os.path.join(base_output_dir, str(year), page_format)
    _ensure_dir(outdir)

    for month in range(1, 13):
        pdf: FPDF = make_pdf(page_format, margins)
        month_label = month_name(locale_code, month)

        # intro/overview
        create_monthly_examen_page(pdf, month_label, year)

        d = date(year, month, 1)
        while d.month == month:
            create_daily_examen_page(pdf, d)
            if d.weekday() == 0:
                create_weekly_examen_page(pdf, d)
            d += timedelta(days=1)

        # monthly summary at the end
        create_monthly_examen_page(pdf, month_label, year)

        out_name = f"{month:02d} - {month_label}_{year}_{page_format}.pdf"
        out_path = os.path.join(outdir, out_name)
        try:
            pdf.output(out_path)
            logging.info("Saved %s", out_path)
        except Exception as e:
            logging.error("Failed to save %s: %s", out_path, e)
            raise
