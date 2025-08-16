from __future__ import annotations

import argparse
import logging
from datetime import date

from remarkable_planner.config import load_config
from remarkable_planner.logging_setup import setup_logging
from remarkable_planner.generate.daily import generate_for_format as gen_daily
from remarkable_planner.generate.examen import generate_year_for_format as gen_examen

def _add_common_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("--formats", nargs="+", default=["A4", "A5"], help="Page formats (e.g., A4 A5).")
    p.add_argument("--outdir", default="generated_planners", help="Base output directory.")
    p.add_argument("--config", default="config.yaml", help="Path to YAML configuration.")
    p.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (-v, -vv).")
    p.add_argument("--json", action="store_true", help="Emit JSON logs instead of human-readable.")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="planner", description="Remarkable Planner Generator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_daily = sub.add_parser("generate-daily", help="Generate daily planner PDFs.")
    p_daily.add_argument("--years", nargs="+", type=int, default=[date.today().year],
                         help="Years to generate (e.g., 2025 2026).")
    _add_common_flags(p_daily)

    p_examen = sub.add_parser("generate-examen", help="Generate Examen-only planner PDFs.")
    p_examen.add_argument("--years", nargs="+", type=int, default=[date.today().year],
                          help="Years to generate (e.g., 2025 2026).")
    p_examen.add_argument("--outdir", default="generated_examen_planners", help="Base output directory.")
    _add_common_flags(p_examen)

    p_check = sub.add_parser("check", help="Validate config and exit.")
    _add_common_flags(p_check)

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    setup_logging(args.verbose, args.json)
    cfg = load_config(args.config)

    if args.cmd == "check":
        logging.info("Configuration OK.")
        print("OK")
        return

    if args.cmd == "generate-daily":
        for y in args.years:
            for fmt in args.formats:
                gen_daily(date(y,1,1), date(y,12,31), fmt, args.outdir, cfg)
        print("Daily planner generation complete.")
        return

    if args.cmd == "generate-examen":
        for y in args.years:
            for fmt in args.formats:
                gen_examen(y, fmt, args.outdir, cfg)
        print("Examen planner generation complete.")
        return

if __name__ == "__main__":
    main()
