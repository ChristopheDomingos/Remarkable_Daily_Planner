from __future__ import annotations

import logging
import os
from datetime import date
from typing import Dict

from fpdf import FPDF

from Remarkable_PDF_Planner_Generator_planner.config import load_config, month_name
from remarkable_planner.rendering.pdf_factory import make_pdf
from remarkable_planner.rendering.links import preallocate_month_links
from remarkable_planner.generate.month_loop import iter_date_range

# Use your existing templates without touching them
from planner.templates import (
    create_daily_page,
    create_daily_reflection_page,
    create_weekly_overview,
    create_monthly_overview,
    create_monthly_examen_page,
)

def _ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def generate_for_format(
    start_date: date,
    end_date: date,
    page_format: str,
    base_output_dir: str,
    cfg: dict,
) -> None:
    """Generate a planner PDF per month for [start_date, end_date]."""
    margins = cfg.get("margins", {})
    locale_code = cfg.get("locale", "en_US")

    year_dir = os.path.join(base_output_dir, str(start_date.year), page_format)
    _ensure_dir(year_dir)
    logging.info("Output dir: %s", os.path.abspath(year_dir))

    # init first month
    current_year = start_date.year
    current_month = start_date.month
    pdf: FPDF = make_pdf(page_format, margins)

    daily_links, calendar_link = preallocate_month_links(pdf, current_year, current_month)
    create_monthly_overview(pdf, current_year, current_month, daily_links, calendar_link)

    for d in iter_date_range(start_date, end_date):
        # month boundary
        if d.month != current_month or d.year != current_year:
            month_label = month_name(locale_code, current_month)
            create_monthly_examen_page(pdf, month_label, current_year)

            out_name = f"{current_month:02d} - {month_label}_{current_year}_{page_format}.pdf"
            out_path = os.path.join(year_dir, out_name)
            try:
                pdf.output(out_path)
                logging.info("Saved %s", out_path)
            except Exception as e:
                logging.error("Failed to save %s: %s", out_path, e)
                raise

            current_month = d.month
            current_year = d.year
            pdf = make_pdf(page_format, margins)
            daily_links, calendar_link = preallocate_month_links(pdf, current_year, current_month)
            create_monthly_overview(pdf, current_year, current_month, daily_links, calendar_link)

        # daily page
        create_daily_page(pdf, d, calendar_link, daily_links[d])

        # weekly overview on Mondays: reuse the SAME link id as the daily page so the
        # monthly calendar Monday cell points to the weekly overview (the weekly call sets the final target).
        if d.weekday() == 0:
            create_weekly_overview(pdf, d, calendar_link, daily_links[d])

        # daily reflection (two-arg signature in your templates)
        create_daily_reflection_page(pdf, d)

    # finalize last month
    month_label = month_name(locale_code, current_month)
    create_monthly_examen_page(pdf, month_label, current_year)
    out_name = f"{current_month:02d} - {month_label}_{current_year}_{page_format}.pdf"
    out_path = os.path.join(year_dir, out_name)
    try:
        pdf.output(out_path)
        logging.info("Saved %s", out_path)
    except Exception as e:
        logging.error("Failed to save %s: %s", out_path, e)
        raise
