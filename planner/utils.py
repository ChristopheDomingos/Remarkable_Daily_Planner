# -*- coding: utf-8 -*-
# Remarkable Daily Planner
# Utilities for loading quotes (with logging, no import-time prints)

import csv
import os
import logging

logger = logging.getLogger(__name__)

# Default quotes to use if the CSV file is not found or invalid.
DEFAULT_QUOTES = [
    ("To begin, begin.", "William Wordsworth (Default)"),
    ("Small deeds done are better than great deeds planned.", "Peter Marshall (Default)"),
    ("What we do every day matters more than what we do once in a while.", "Gretchen Rubin (Default)"),
]

def _project_root() -> str:
    # styles.py and templates.py live in planner/, config and CSV live at repo root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_quotes(csv_filename: str = "my_quotes.csv"):
    """Load quotes from CSV (quote, author). Falls back to DEFAULT_QUOTES.

    Returns:
        list[tuple[str, str]]: list of (quote, author)
    """
    root = _project_root()
    path = os.path.join(root, csv_filename)

    if not os.path.exists(path):
        logger.warning("Quotes file '%s' not found. Using default quotes.", os.path.abspath(path))
        return DEFAULT_QUOTES.copy()

    quotes = []
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if not row:
                    continue
                # Accept 1 or 2 columns: (quote) or (quote, author)
                quote = row[0].strip()
                author = row[1].strip() if len(row) > 1 and row[1] else "Unknown"
                if not quote:
                    logger.warning("Skipping empty quote at row %d in '%s'.", i+1, path)
                    continue
                quotes.append((quote, author))
    except csv.Error as e:
        logger.error("CSV parsing error in '%s': %s. Using default quotes.", os.path.abspath(path), e)
        return DEFAULT_QUOTES.copy()
    except Exception as e:
        logger.error("Unexpected error while loading '%s': %s. Using default quotes.", os.path.abspath(path), e)
        return DEFAULT_QUOTES.copy()

    if not quotes:
        logger.warning("No valid quotes found in '%s'. Using default quotes.", os.path.abspath(path))
        return DEFAULT_QUOTES.copy()

    logger.info("Loaded %d quotes from '%s'.", len(quotes), os.path.abspath(path))
    return quotes

if __name__ == '__main__':
    logger.info("Testing quote loading utility...")
    loaded = load_quotes()
    if loaded and loaded != DEFAULT_QUOTES:
        logger.info("Successfully loaded %d custom quotes. First 3:", len(loaded))
        for i, (q, a) in enumerate(loaded[:3], start=1):
            logger.info("%d. \"%s\" - %s", i, q, a)
    elif loaded == DEFAULT_QUOTES:
        logger.info("Loaded default quotes as custom file was not found or invalid.")
        for i, (q, a) in enumerate(loaded[:3], start=1):
            logger.info("%d. \"%s\" - %s", i, q, a)
    else:
        logger.error("No quotes were loaded. Check logic.")
