from __future__ import annotations
import csv
from functools import lru_cache
from datetime import date

@lru_cache(maxsize=1)
def _load_quotes(path: str) -> list[str]:
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            return [row[0].strip() for row in reader if row and row[0].strip()]
    except FileNotFoundError:
        return []

def quote_for_date(d: date, path: str, seed: int = 0) -> str:
    quotes = _load_quotes(path)
    if not quotes:
        return ""
    idx = (d.toordinal() + int(seed)) % len(quotes)
    return quotes[idx]
