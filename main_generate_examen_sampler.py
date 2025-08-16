# -*- coding: utf-8 -*-
"""
St. Ignatius Examen Planner
Keep imports aligned with your existing templates.
"""

from __future__ import annotations

import argparse
import calendar as py_calendar
import logging
import os
from datetime import date, timedelta

import yaml
from fpdf import FPDF

from planner.templates import (
    create_weekly_examen_page,
    create_daily_examen_page,
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

def generate_yearly_examen_planner_for_format(
    year: int, page_format: str, base_output_dir: str, config: dict
) -> None:
    margins = (config.get("margins") or {})
    left = float(margins.get("left", 10))
    top = float(margins.get("top", 15))
    right = float(margins.get("right", 10))
    bottom = float(margins.get("bottom", 15))

    outdir = os.path.join(base_output_dir, str(year), page_format)
    _ensure_outdir(outdir)

    for month in range(1, 13):
        pdf = FPDF(orientation='P', unit='mm', format=page_format)
        pdf.set_left_margin(left)
        pdf.set_top_margin(top)
        pdf.set_right_margin(right)
        pdf.set_auto_page_break(auto=True, margin=bottom)

        month_name = py_calendar.month_name[month]

        # Optional monthly intro
        create_monthly_examen_page(pdf, month_name, year)

        d = date(year, month, 1)
        while d.month == month:
            create_daily_examen_page(pdf, d)
            if d.weekday() == 0:
                create_weekly_examen_page(pdf, d)
            d += timedelta(days=1)

        # Monthly summary at the end
        create_monthly_examen_page(pdf, month_name, year)

        out_name = f"{month:02d} - {month_name}_{year}_{page_format}.pdf"
        out_path = os.path.join(outdir, out_name)
        try:
            pdf.output(out_path)
            logging.info("Saved %s", out_path)
        except Exception as e:
            logging.error("Failed to save %s: %s", out_path, e)
            raise

def parse_args():
    p = argparse.ArgumentParser(description="Generate Examen-only planners.")
    p.add_argument("--years", nargs="+", type=int, default=[date.today().year],
                   help="Years to generate (e.g., --years 2025 2026).")
    p.add_argument("--formats", nargs="+", default=["A4", "A5"],
                   help="Page formats (e.g., --formats A4 A5).")
    p.add_argument("--outdir", default="generated_examen_planners",
                   help="Base output directory.")
    p.add_argument("--config", default="config.yaml",
                   help="Path to YAML configuration.")
    p.add_argument("-v", "--verbose", action="count", default=0,
                   help="Increase verbosity.")
    return p.parse_args()

def main():
    args = parse_args()
    _setup_logging(args.verbose)
    cfg = _load_yaml_config(args.config)

    for y in args.years:
        for fmt in args.formats:
            generate_yearly_examen_planner_for_format(y, fmt, args.outdir, cfg)

    print("\nExamen planner generation complete. Crafted by: Christophe Domingos")

if __name__ == "__main__":
    main()
