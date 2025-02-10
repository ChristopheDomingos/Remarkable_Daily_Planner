# Remarkable Daily Planner

## Overview
This project generates a professional-grade PDF planner tailored for use on the Remarkable tablet. It includes:
- Daily pages for every day of the year.
- Weekly overview pages for setting weekly goals and tracking habits.
- Monthly title pages for key highlights and goals.

## Features
- **Daily Pages**:
  - Header with the month, date (`DD/MM/YYYY`), and day of the week.
  - Writable task list with `-` markers and aligned horizontal lines for guided handwriting.
  - Notes section with faint dotted lines for structured writing.
- **Weekly Overview**:
  - Weekly goals section.
  - Habit tracker for daily habits.
- **Monthly Title Pages**:
  - Month name prominently displayed.
  - Space for monthly goals or key highlights.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>

## Modifications Log - 10/02/2025

This project has been refactored to improve modularity, maintainability, and future extensibility while preserving the original PDF layout for reMarkable tablets. Key modifications include:

- **Preservation of Your Layout:**  
  All original cells, lines, and spacing remain unchanged. The functions in `planner/templates.py` still generate daily pages, weekly overviews, and monthly titles exactly as before, ensuring the PDF output is identical to your initial design.

- **Modularity & Configuration:**  
  - Font and margin settings have been centralized in `planner/styles.py`.  
  - A new configuration system (using `config.yaml` and `planner/config.py`) has been added so that key parameters can be tweaked without altering the code.
  
- **Maintainability:**  
  - Type hints and detailed docstrings have been added across modules for clarity.  
  - The project is now split into clear modules (for templates, configuration, and planner generation), making future modifications easier to manage.
  
- **Future Enhancements (Optional):**  
  The current structure is designed to allow the addition of features like internal hyperlinks or bookmarks later on, which can improve navigation on the reMarkable without altering the basic appearance of the PDF.

Each commit will build upon these improvements to further enhance functionality while ensuring the PDF remains optimized for reMarkable devices.
