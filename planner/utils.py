# -*- coding: utf-8 -*-
# Remarkable Daily Planner
# Version 2.2
#
# Created by: Christophe Domingos
# Date: May 30, 2025
#
# Description: Utility functions for the planner, such as loading quotes.

import csv
import os

# Default quotes to use if the CSV file is not found or is invalid.
DEFAULT_QUOTES = [
    ("To begin, begin.", "William Wordsworth (Default)"),
    ("An unexamined life is not worth living.", "Socrates (Default)"),
    ("The only way to do great work is to love what you do.", "Steve Jobs (Default)")
]

def load_quotes(file_path: str = "my_quotes.csv") -> list[tuple[str, str]]:
    """
    Loads quotes from a CSV file.

    The CSV file is expected to be in the project root directory.
    Each row should be in the format: "Quote","Author"

    Args:
        file_path: The name of the CSV file (e.g., "my_quotes.csv").

    Returns:
        A list of (quote, author) tuples. Returns default quotes on error.
    """
    quotes = []
    
    # Construct the absolute path to the quotes file, assuming it's in the project root.
    # utils.py is in planner/, so project_root is its parent's parent.
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    actual_file_path = os.path.join(project_root, file_path)

    if not os.path.exists(actual_file_path):
        print(f"[QUOTES_LOADER_WARN] Quotes file '{os.path.abspath(actual_file_path)}' not found. Using default quotes.")
        return DEFAULT_QUOTES.copy() # Return a copy to prevent modification of defaults

    try:
        with open(actual_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            # csv.QUOTE_ALL handles quotes that might contain commas.
            reader = csv.reader(csvfile, quotechar='"', delimiter=',', 
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)
            for i, row in enumerate(reader):
                if len(row) == 2:
                    quote, author = row[0].strip(), row[1].strip()
                    if quote and author: # Ensure neither quote nor author is empty
                        quotes.append((quote, author))
                    else:
                        print(f"[QUOTES_LOADER_WARN] Skipping malformed row {i+1} in '{actual_file_path}': Empty quote or author.")
                elif row: # Row exists but doesn't have exactly two elements
                    print(f"[QUOTES_LOADER_WARN] Skipping malformed row {i+1} in '{actual_file_path}': Expected 2 columns, got {len(row)}.")
        
        if not quotes:
            print(f"[QUOTES_LOADER_WARN] No valid quotes found in '{os.path.abspath(actual_file_path)}'. Using default quotes.")
            return DEFAULT_QUOTES.copy()
        
        print(f"[QUOTES_LOADER_INFO] Successfully loaded {len(quotes)} quotes from '{os.path.abspath(actual_file_path)}'.")
        return quotes

    except FileNotFoundError: # Should be caught by os.path.exists, but as a fallback.
        print(f"[QUOTES_LOADER_ERROR] Quotes file '{os.path.abspath(actual_file_path)}' not found during open attempt. Using default quotes.")
        return DEFAULT_QUOTES.copy()
    except csv.Error as e:
        print(f"[QUOTES_LOADER_ERROR] CSV parsing error in '{os.path.abspath(actual_file_path)}': {e}. Using default quotes.")
        return DEFAULT_QUOTES.copy()
    except Exception as e: # Catch-all for other unexpected errors
        print(f"[QUOTES_LOADER_ERROR] An unexpected error occurred loading quotes from '{os.path.abspath(actual_file_path)}': {e}. Using default quotes.")
        return DEFAULT_QUOTES.copy()

if __name__ == '__main__':
    # Test function for loading quotes directly
    print("Testing quote loading utility...")
    loaded_quotes = load_quotes()
    if loaded_quotes and loaded_quotes != DEFAULT_QUOTES:
        print(f"\nSuccessfully loaded {len(loaded_quotes)} custom quotes. First 5:")
        for i, (q, a) in enumerate(loaded_quotes[:5]):
            print(f"{i+1}. \"{q}\" - {a}")
    elif loaded_quotes == DEFAULT_QUOTES:
        print("\nLoaded default quotes as custom file was not found or was empty/invalid.")
        for i, (q, a) in enumerate(loaded_quotes[:3]):
             print(f"{i+1}. \"{q}\" - {a}")
    else: # Should not happen if DEFAULT_QUOTES is always returned on failure
        print("\nNo quotes were loaded, and defaults were not returned. Check logic.")