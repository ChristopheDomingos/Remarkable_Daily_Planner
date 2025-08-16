from __future__ import annotations
from datetime import date, timedelta

def iter_date_range(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)
