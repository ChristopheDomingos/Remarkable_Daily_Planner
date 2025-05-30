# -*- coding: utf-8 -*-
# Remarkable Daily Planner
# Version 2.2
#
# Created by: Christophe Domingos
# Date: May 30, 2025
#
# Description: Defines and loads style configurations (fonts, margins)
#              for the PDF planner.

from planner.config import load_config
import os

# Determine project root to locate config.yaml relative to this file's location
# Assumes styles.py is in planner/ and config.yaml is in the parent directory (project root).
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")

# --- Load Configuration with Fallbacks ---
config_data = {} # Initialize with an empty dict for fallback
try:
    config_data = load_config(CONFIG_PATH)
    if not isinstance(config_data, dict):
        print(f"[STYLE_CONFIG_WARN] Config file at '{CONFIG_PATH}' did not load as a dictionary. Using default styles.")
        config_data = {} # Fallback to empty if not a dict
except FileNotFoundError:
    print(f"[STYLE_CONFIG_WARN] Config file '{CONFIG_PATH}' not found. Using default styles.")
    # config_data remains an empty dict
except Exception as e:
    print(f"[STYLE_CONFIG_WARN] Error loading config file '{CONFIG_PATH}': {e}. Using default styles.")
    # config_data remains an empty dict

def parse_font_string(font_str: str, default_family: str = 'Helvetica', default_style: str = '', default_size: int = 12) -> tuple:
    """
    Safely parses a font string 'Family,Style,Size' into a (family, style, size) tuple.
    Provides default values if the string is malformed or parts are missing.
    """
    if not font_str or not isinstance(font_str, str):
        return (default_family, default_style, default_size)

    parts = font_str.split(',')
    family = parts[0].strip() if len(parts) > 0 and parts[0].strip() else default_family
    style = ''
    if len(parts) > 1 and parts[1].strip():
        style = parts[1].strip().upper() # Styles like 'B', 'I', 'U'

    size = default_size
    if len(parts) > 2 and parts[2].strip():
        try:
            size = int(parts[2].strip())
        except ValueError:
            # If size conversion fails, use default size. Optional: log this.
            size = default_size
    return (family, style, size)

# --- Font Styles ---
# Default to 'Helvetica' as a safe fallback if specific fonts like 'Arial'
# are not available or properly added to FPDF.
# The config.yaml can specify other fonts (e.g., "Arial"), but FPDF might
# substitute them if not correctly configured with add_font().
FONT_TITLE = parse_font_string(config_data.get('font_title'), default_family='Helvetica', default_style='B', default_size=16)
FONT_BODY  = parse_font_string(config_data.get('font_body'), default_family='Helvetica', default_style='', default_size=12)

# --- Margin Settings (in mm) ---
margins_config = config_data.get('margins', {})
if not isinstance(margins_config, dict): # Ensure margins_config is a dict
    margins_config = {} # Fallback if 'margins' is not a dictionary
MARGIN_LEFT  = margins_config.get('left', 10)
MARGIN_TOP   = margins_config.get('top', 15)
MARGIN_RIGHT = margins_config.get('right', 10)

# --- Examen Page Specific Font Styles ---
# These allow finer control over Examen page appearance via config.yaml.
FONT_EXAMEN_STEP_TITLE = parse_font_string(config_data.get('font_examen_step_title'), default_family='Helvetica', default_style='B', default_size=12)
FONT_EXAMEN_PROMPT = parse_font_string(config_data.get('font_examen_prompt'), default_family='Helvetica', default_style='I', default_size=10)