# planner/styles.py
from planner.config import load_config 
import os

# Assumes main.py is run from project root, where config.yaml is.
# styles.py is in planner/, so config.yaml is in parent directory.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")

config = {} # Initialize with an empty dict for fallback
try:
    config = load_config(CONFIG_PATH)
    if not isinstance(config, dict): # Ensure loaded config is a dictionary
        print(f"[WARN styles.py] Config file at '{CONFIG_PATH}' did not load as a dictionary. Using default styles.")
        config = {}
except FileNotFoundError:
    print(f"[WARN styles.py] Config file '{CONFIG_PATH}' not found. Using default styles.")
    config = {} # Fallback to empty dict
except Exception as e: # Catch any other error during config loading
    print(f"[WARN styles.py] Error loading config file '{CONFIG_PATH}': {e}. Using default styles.")
    config = {} # Fallback to empty dict

def parse_font_string(font_str, default_family='Arial', default_style='', default_size=12):
    """ Safely parses a font string 'Family,Style,Size' into a tuple. """
    if not font_str or not isinstance(font_str, str): 
        return (default_family, default_style, default_size)
    
    parts = font_str.split(',')
    family = parts[0].strip() if len(parts) > 0 and parts[0].strip() else default_family
    
    style = ''
    if len(parts) > 1 and parts[1].strip(): 
        style = parts[1].strip()
    
    size = default_size
    if len(parts) > 2 and parts[2].strip(): 
        try:
            size = int(parts[2].strip())
        except ValueError:
            # If conversion to int fails, use default_size
            # print(f"[WARN styles.py] Invalid size value in font string '{font_str}'. Using default size {default_size}.") # Optional warning
            size = default_size
            
    return (family, style, size)

# --- Main Font Styles ---
FONT_TITLE = parse_font_string(config.get('font_title'), default_family='Arial', default_style='B', default_size=16)
FONT_BODY  = parse_font_string(config.get('font_body'), default_family='Arial', default_style='', default_size=12)

# --- Margin Settings (in mm) ---
margins_config = config.get('margins', {}) 
if not isinstance(margins_config, dict): # Ensure margins_config is a dict
    margins_config = {} 
MARGIN_LEFT  = margins_config.get('left', 10)
MARGIN_TOP   = margins_config.get('top', 15)
MARGIN_RIGHT = margins_config.get('right', 10)

# --- Examen Page Specific Font Styles ---
FONT_EXAMEN_STEP_TITLE = parse_font_string(config.get('font_examen_step_title'), default_family='Arial', default_style='B', default_size=12)
FONT_EXAMEN_PROMPT = parse_font_string(config.get('font_examen_prompt'), default_family='Arial', default_style='I', default_size=10)