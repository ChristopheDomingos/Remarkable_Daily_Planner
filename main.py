# -*- coding: utf-8 -*-
"""
Wrapper entrypoint for VS Code "Run" button.
Generates the DAILY planner for the current year in A4 and A5 by default.

You can tweak the defaults below (YEARS, FORMATS, OUTDIR, CONFIG).
"""

from __future__ import annotations
import sys
from datetime import date

# === Defaults you can change ===
YEARS = [date.today().year]       # e.g., [2025, 2026]
FORMATS = ["A4", "A5"]            # e.g., ["A5"]
OUTDIR = "generated_planners"
CONFIG = "config.yaml"
VERBOSITY = 1                     # 0=warnings only, 1=info, 2=debug
JSON_LOGS = False                 # True to emit JSON logs

def _argv_for_daily():
    argv = [
        "planner", "generate-daily",
        "--years", *(str(y) for y in YEARS),
        "--formats", *FORMATS,
        "--outdir", OUTDIR,
        "--config", CONFIG,
    ]
    if VERBOSITY >= 1:
        argv += ["-" + "v" * VERBOSITY]  # -v or -vv
    if JSON_LOGS:
        argv += ["--json"]
    return argv

if __name__ == "__main__":
    # Route through the unified CLI with our defaults
    from planner.cli import main as planner_cli_main
    sys.argv = _argv_for_daily()
    planner_cli_main()
