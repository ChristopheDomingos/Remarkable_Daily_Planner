# Remarkable Daily Planner - Version 2.3

**Created by: Christophe Domingos**
**Date: June 3, 2025**

## Overview
This project generates professional-grade PDF planners tailored for use on Remarkable tablets and similar e-ink devices. It creates highly functional daily, weekly, and monthly pages designed for clarity and ease of use. Two types of planners can be generated:
1.  A comprehensive **Daily Planner** including daily tasks/journal, weekly overviews/habit tracking, monthly calendars with integrated birthdays/anniversaries, and Examen pages.
2.  A focused **St. Ignatius Examen Planner** with daily, weekly, and monthly Examen/reflection pages.

The PDFs are optimized for A4 and A5 formats and include enhanced internal navigation links for a seamless experience on your Remarkable device.

## Key Features
-   **Modular Design:** Code is organized into logical modules for configuration, styling, page templates, data, and utilities.
-   **Configurable:** Key settings like margins and fonts can be easily adjusted via `config.yaml`. Birthdays, anniversaries, and special dates are managed in `planner/data.py`.
-   **Daily Pages:**
    -   Clear headers with month, full date, and day of the week.
    -   Clickable date navigates back to the monthly calendar overview.
    -   Inspirational daily quote.
    -   Structured task list with markers and lined writing areas.
    -   Generous lined journal section.
-   **Daily Reflection Pages (Particular Examen):**
    -   Guided sections for morning resolve, midday tally/reflection, evening tally/reflection, and night review.
-   **Weekly Overview Pages:**
    -   Sections for top priorities, appointments, skills/learning, and gratitude.
    -   Centered habit tracker with an instructional note.
    -   Space for reflection on accomplishments and challenges of the past week.
    -   **New:** Title links back to the monthly calendar overview.
-   **Weekly Examen Pages:**
    -   Guided 5-step General Examen of Consciousness for the week.
-   **Monthly Overview Pages:**
    -   Full month calendar with clickable day numbers linking to respective daily pages.
    -   **New:** Mondays on the calendar link to the respective weekly overview page.
    -   Sections for monthly focus, key dates (can include special dates from `planner/data.py`), and general notes.
    -   **New:** "Birthdays & Anniversaries" section dynamically lists events for the month from `planner/data.py`, including calculated age for birthdays with a known birth year.
-   **Monthly Examen Pages:**
    -   Guided 5-step General Examen of Consciousness for the month.
    -   **New:** This page is now placed at the end of each month's PDF content.
-   **Custom Quotes:** Easily customize daily quotes by editing `my_quotes.csv`.
-   **Custom Dates:** Manage birthdays, anniversaries, and other special dates by editing the Python lists in `planner/data.py`.
-   **Output:** Generates separate PDF files for each month, organized by year and format (A4/A5).

## Project Structure
Remarkable_Daily_Planner/
├── config.yaml                     # Main configuration for styles (fonts, margins)
├── main.py                         # Main script to generate full daily planners
├── main_generate_examen_sampler.py # Script to generate Examen-focused planners
├── my_quotes.csv                   # CSV file for custom daily quotes
├── README.md                       # This file
├── requirements.txt                # Python package dependencies
├── structure.txt                   # Overview of the project directory structure
├── LICENSE                         # Project license (MIT License)
│
├── planner/                        # Core planner generation package
│   ├── __init__.py                 # Makes 'planner' a Python package
│   ├── config.py                   # Loads configuration from config.yaml
│   ├── data.py                     # Stores birthday, anniversary, and special date data (NEW)
│   ├── styles.py                   # Defines styles (fonts, margins) from config
│   ├── templates.py                # Functions to create PDF page layouts
│   └── utils.py                    # Utility functions (e.g., quote loader)
│
├── generated_planners/             # Default output directory for full planners (add to .gitignore)
└── generated_examen_planners/      # Default output directory for Examen planners (add to .gitignore)


## Installation
(Installation steps remain the same as v2.2)
1.  **Clone the repository:**
    ```bash
    git clone <your_repository_url_here>
    cd Remarkable_Daily_Planner
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    Activate it:
    -   Windows: `.\venv\Scripts\activate`
    -   macOS/Linux: `source venv/bin/activate`
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1.  **Customize Dates (Optional but Recommended):**
    * Edit `planner/data.py` to include your personal birthdays, anniversaries, and any special dates you want to track.
2.  **To generate the full daily planners:**
    Run the `main.py` script from the project root directory:
    ```bash
    python main.py
    ```
    This will generate planners for the years and formats specified within `main.py` (default: 2025 & 2026, A4 & A5) into the `generated_planners` directory.
3.  **To generate the St. Ignatius Examen planners:**
    Run the `main_generate_examen_sampler.py` script:
    ```bash
    python main_generate_examen_sampler.py
    ```
    This will generate Examen-focused planners for the years and formats specified (default: 2025 & 2026, A4 & A5) into the `generated_examen_planners` directory.
4.  **Further Customization:**
    * **Fonts & Margins:** Modify `config.yaml`.
    * **Daily Quotes:** Edit `my_quotes.csv`. Ensure the CSV format ("Quote","Author") is maintained.
    * **Years & Formats:** Change the `years_to_generate` and `formats_to_generate` lists directly in `main.py` or `main_generate_examen_sampler.py`.

## GitHub Repository - Best Practices
* **Repository Description:** Use a concise and informative description for your repository on GitHub. E.g., "Generates customizable PDF daily, weekly, and monthly planners optimized for Remarkable e-ink tablets. Features birthday/anniversary tracking, Examen pages, Catholic quotes, and enhanced navigation."
* **Topics/Tags:** Add relevant topics like `pdf-generation`, `remarkable`, `planner`, `python`, `fpdf2`, `e-ink`, `digital-planner`, `ignatian-examen`, `productivity`, `journaling`. This improves discoverability.
* **LICENSE File:** Include the `LICENSE` file (MIT recommended, provided).
* **Pin the Repository:** If it's a key project, pin it to your GitHub profile.

## Project Highlights & Version 2.3 Updates
This version (2.3) introduces several enhancements for personalization and navigation:
-   **Birthday & Anniversary Tracking:** Monthly overview now displays birthdays and anniversaries from `planner/data.py`, with automatic age calculation.
-   **Relocated Monthly Examen:** The Monthly Examen page is now positioned at the end of each month's content for a more natural reflection flow.
-   **Enhanced Hypernavigation:**
    -   Monthly calendar Mondays link directly to their corresponding weekly overview page.
    -   Weekly overview titles link back to the monthly calendar.
-   **Special Dates Framework:** Added `planner/data.py` to manage special dates (e.g., holidays, gift dates), with basic integration into the monthly "Key Dates" section. Users can populate this data.
-   **Weekly Habit Tracker Note:** Added an instructional prompt to the weekly habit tracker.
-   **Data Management:** Centralized user-specific date information (birthdays, special dates) into `planner/data.py`.
-   **Code Refinements:** Updated relevant modules to support these new features and improve internal linking logic.
-   **Documentation Update:** `README.md` and `structure.txt` updated to reflect changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.