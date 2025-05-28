# planner/utils.py
import csv
import os

DEFAULT_QUOTES = [
    ("To begin, begin.", "William Wordsworth (Placeholder)"),
    ("An unexamined life is not worth living.", "Socrates (Placeholder)"),
    ("The only way to do great work is to love what you do.", "Steve Jobs (Placeholder)")
]

def load_quotes(file_path: str = "my_quotes.csv") -> list:
    """
    Loads quotes from a CSV file located in the project root.
    Expected CSV format: "Quote","Author"
    Returns a list of (quote, author) tuples.
    If the file is not found or is empty/invalid, returns a default list.
    """
    quotes = []
    
    # Determine project root to reliably find my_quotes.csv
    # This assumes utils.py is in planner/ and my_quotes.csv is in the parent directory (project root)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    actual_file_path = os.path.join(project_root, file_path) # Construct path relative to project root

    if not os.path.exists(actual_file_path):
        print(f"[WARN utils.py] Quotes file '{os.path.abspath(actual_file_path)}' not found. Using default quotes.")
        return DEFAULT_QUOTES

    try:
        with open(actual_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, quotechar='"', delimiter=',', 
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)
            for i, row in enumerate(reader):
                if len(row) == 2:
                    quote, author = row[0].strip(), row[1].strip()
                    if quote and author: # Ensure neither is empty
                        quotes.append((quote, author))
                    else:
                        print(f"[WARN utils.py] Skipping malformed row {i+1} in '{actual_file_path}': Empty quote or author.")
                elif row: # Row is not empty but doesn't have 2 elements
                    print(f"[WARN utils.py] Skipping malformed row {i+1} in '{actual_file_path}': Expected 2 columns, got {len(row)}.")
        
        if not quotes:
            print(f"[WARN utils.py] No valid quotes found in '{os.path.abspath(actual_file_path)}'. Using default quotes.")
            return DEFAULT_QUOTES
        
        print(f"[INFO utils.py] Successfully loaded {len(quotes)} quotes from '{os.path.abspath(actual_file_path)}'.")
        return quotes

    except FileNotFoundError: 
        print(f"[WARN utils.py] Quotes file '{os.path.abspath(actual_file_path)}' not found during open. Using default quotes.")
        return DEFAULT_QUOTES
    except csv.Error as e:
        print(f"[WARN utils.py] Error reading CSV file '{os.path.abspath(actual_file_path)}': {e}. Using default quotes.")
        return DEFAULT_QUOTES
    except Exception as e:
        print(f"[WARN utils.py] An unexpected error occurred loading quotes from '{os.path.abspath(actual_file_path)}': {e}. Using default quotes.")
        return DEFAULT_QUOTES

if __name__ == '__main__':
    # For testing the function directly
    loaded_quotes = load_quotes()
    if loaded_quotes:
        print(f"\nFirst few loaded quotes (total: {len(loaded_quotes)}):")
        for i, (q, a) in enumerate(loaded_quotes[:5]):
            print(f"{i+1}. \"{q}\" - {a}")
    else:
        print("No quotes were loaded.")