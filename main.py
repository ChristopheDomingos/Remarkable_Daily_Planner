# -*- coding: utf-8 -*-
"""
Remarkable Daily Planner
Single-source version is optional; keeping inline for compatibility.
"""

from __future__ import annotations

import argparse
import calendar as py_calendar
import logging
import os
from datetime import date, timedelta
from typing import Dict

import yaml
from fpdf import FPDF

# Import the template functions that exist in your repo
from planner.templates import (
    create_daily_page,
    create_daily_reflection_page,
    create_weekly_overview,
    create_monthly_overview,
    create_monthly_examen_page,
)

def _load_yaml_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def _setup_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s")

def _ensure_outdir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def _iter_month_days(y: int, m: int):
    d = date(y, m, 1)
    while d.month == m:
        yield d
        d += timedelta(days=1)

def _preallocate_links_for_month(pdf: FPDF, y: int, m: int):
    """Return (daily_links, calendar_link).
    Monday daily links are aliased to their weekly overview target:
    we reuse the same link id for Monday's daily and weekly pages.
    The weekly page is created after the daily page, so the final
    target becomes the weekly overview as promised in README.
    """
    daily: Dict[date, int] = {}
    for d in _iter_month_days(y, m):
        daily[d] = pdf.add_link()
    calendar_link = pdf.add_link()
    return daily, calendar_link

def generate_planner_for_format(
    start_date: date,
    end_date: date,
    page_format: str,
    base_output_dir: str,
    config: dict,
) -> None:
    # Margins from config (with sane defaults)
    margins = (config.get("margins") or {})
    left = float(margins.get("left", 10))
    top = float(margins.get("top", 15))
    right = float(margins.get("right", 10))
    bottom = float(margins.get("bottom", 15))

    # Output directories: base/year/format
    year_dir = os.path.join(base_output_dir, str(start_date.year))
    fmt_dir = os.path.join(year_dir, page_format)
    _ensure_outdir(fmt_dir)
    logging.info("Output dir: %s", os.path.abspath(fmt_dir))

    # Create first month's PDF
    active_pdf: FPDF | None = None
    current_pdf_year = start_date.year
    current_pdf_month = start_date.month

    def _new_month_pdf(y: int, m: int) -> FPDF:
        pdf = FPDF(orientation='P', unit='mm', format=page_format)
        # Respect config-driven margins including bottom
        pdf.set_left_margin(left)
        pdf.set_top_margin(top)
        pdf.set_right_margin(right)
        pdf.set_auto_page_break(auto=True, margin=bottom)
        return pdf

    active_pdf = _new_month_pdf(current_pdf_year, current_pdf_month)

    # Pre-allocate link IDs and render the monthly overview first
    daily_links, calendar_link = _preallocate_links_for_month(active_pdf, current_pdf_year, current_pdf_month)
    create_monthly_overview(
        active_pdf,
        current_pdf_year,
        current_pdf_month,
        daily_links,
        calendar_link,
    )

    current_date = start_date
    while current_date <= end_date:
        # Month boundary? finalize previous, start new
        if current_date.month != current_pdf_month or current_date.year != current_pdf_year:
            completed_month_name = py_calendar.month_name[current_pdf_month]
            create_monthly_examen_page(active_pdf, completed_month_name, current_pdf_year)

            out_name = f"{current_pdf_month:02d} - {completed_month_name}_{current_pdf_year}_{page_format}.pdf"
            out_path = os.path.join(fmt_dir, out_name)
            try:
                active_pdf.output(out_path)
                logging.info("Saved %s", out_path)
            except Exception as e:
                logging.error("Failed to save %s: %s", out_path, e)
                raise

            # Start new month
            current_pdf_month = current_date.month
            current_pdf_year = current_date.year
            active_pdf = _new_month_pdf(current_pdf_year, current_pdf_month)

            daily_links, calendar_link = _preallocate_links_for_month(active_pdf, current_pdf_year, current_pdf_month)
            create_monthly_overview(
                active_pdf,
                current_pdf_year,
                current_pdf_month,
                daily_links,
                calendar_link,
            )

        # Daily page
        create_daily_page(
            active_pdf,
            current_date,
            calendar_link,                # back to monthly calendar
            daily_links[current_date],     # anchor id used by monthly calendar
        )

        # Weekly overview on Mondays: reuse the SAME link id as the daily page
        # so the calendar Monday cell ends up pointing to the weekly overview.
        if current_date.weekday() == 0:
            create_weekly_overview(
                active_pdf,
                current_date,
                calendar_link,                 # back to calendar
                daily_links[current_date],     # alias link id
            )

        # Daily reflection page (no calendar_link arg in your template signature)
        create_daily_reflection_page(active_pdf, current_date)

        current_date += timedelta(days=1)

    # Finalize the last month
    last_month_name = py_calendar.month_name[current_pdf_month]
    create_monthly_examen_page(active_pdf, last_month_name, current_pdf_year)
    out_name = f"{current_pdf_month:02d} - {last_month_name}_{current_pdf_year}_{page_format}.pdf"
    out_path = os.path.join(fmt_dir, out_name)
    try:
        active_pdf.output(out_path)
        logging.info("Saved %s", out_path)
    except Exception as e:
        logging.error("Failed to save %s: %s", out_path, e)
        raise

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate Remarkable Daily Planner PDFs (one per month).")
    p.add_argument("--years", nargs="+", type=int, default=[date.today().year], help="Years to generate (e.g., --years 2025 2026).")
    p.add_argument("--formats", nargs="+", default=["A4", "A5"], help="Page formats to generate (e.g., --formats A4 A5).")
    p.add_argument("--outdir", default="generated_planners", help="Base output directory.")
    p.add_argument("--config", default="config.yaml", help="Path to YAML configuration.")
    p.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (-v, -vv).")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    _setup_logging(args.verbose)
    cfg = _load_yaml_config(args.config)

    logging.info("Years=%s Formats=%s OutDir=%s", args.years, args.formats, args.outdir)

    for y in args.years:
        logging.info("--- Generating planner for %d ---", y)
        for fmt in args.formats:
            logging.info("-- %s --", fmt)
            start = date(y, 1, 1)
            end = date(y, 12, 31)
            generate_planner_for_format(start, end, fmt, args.outdir, cfg)
        logging.info("--- Finished %d ---", y)

    print("\nPDF planner generation complete. Crafted by: Christophe Domingos")

if __name__ == "__main__":
    main()
