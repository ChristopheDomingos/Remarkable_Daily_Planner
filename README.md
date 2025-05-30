# Remarkable Daily Planner - Version 2.2

**Created by: Christophe Domingos**
**Date: May 30, 2025**

## Overview
This project generates professional-grade PDF planners tailored for use on Remarkable tablets and similar e-ink devices. It creates highly functional daily, weekly, and monthly pages designed for clarity and ease of use. Two types of planners can be generated:
1.  A comprehensive **Daily Planner** including daily tasks/journal, weekly overviews/habit tracking, monthly calendars, and Examen pages.
2.  A focused **St. Ignatius Examen Planner** with daily, weekly, and monthly Examen/reflection pages.

The PDFs are optimized for A4 and A5 formats and include internal navigation links for a seamless experience on your Remarkable device.

## Key Features
-   **Modular Design:** Code is organized into logical modules for configuration, styling, page templates, and utilities.
-   **Configurable:** Key settings like margins and fonts can be easily adjusted via `config.yaml` without modifying the Python code.
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
    -   Centered habit tracker for up to 5 customizable habits.
    -   Space for reflection on accomplishments and challenges of the past week.
-   **Weekly Examen Pages:**
    -   Guided 5-step General Examen of Consciousness for the week.
-   **Monthly Overview Pages:**
    -   Full month calendar with clickable day numbers linking to respective daily pages.
    -   Sections for monthly focus, key dates, birthdays/anniversaries, and general notes.
-   **Monthly Examen Pages:**
    -   Guided 5-step General Examen of Consciousness for the month.
-   **Custom Quotes:** Easily customize daily quotes by editing `my_quotes.csv`.
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
│   ├── init.py                 # Makes 'planner' a Python package
│   ├── config.py                   # Loads configuration from config.yaml
│   ├── styles.py                   # Defines styles (fonts, margins) from config
│   ├── templates.py                # Functions to create PDF page layouts
│   └── utils.py                    # Utility functions (e.g., quote loader)
│
├── generated_planners/             # Default output directory for full planners (add to .gitignore)
└── generated_examen_planners/      # Default output directory for Examen planners (add to .gitignore)


## Installation

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

1.  **To generate the full daily planners:**
    Run the `main.py` script from the project root directory:
    ```bash
    python main.py
    ```
    This will generate planners for the years and formats specified within `main.py` (default: 2025 & 2026, A4 & A5) into the `generated_planners` directory.

2.  **To generate the St. Ignatius Examen planners:**
    Run the `main_generate_examen_sampler.py` script:
    ```bash
    python main_generate_examen_sampler.py
    ```
    This will generate Examen-focused planners for the years and formats specified (default: 2025 & 2026, A4 & A5) into the `generated_examen_planners` directory.

3.  **Customization:**
    * **Fonts & Margins:** Modify `config.yaml`.
    * **Daily Quotes:** Edit `my_quotes.csv`. Ensure the CSV format ("Quote","Author") is maintained.
    * **Years & Formats:** Change the `years_to_generate` and `formats_to_generate` lists directly in `main.py` or `main_generate_examen_sampler.py`.

## GitHub Repository - Best Practices
To make your GitHub repository look top-tier:
* **Repository Description:** Use a concise and informative description for your repository on GitHub. E.g., "Generates customizable PDF daily, weekly, and monthly planners optimized for Remarkable e-ink tablets. Includes Examen pages and Catholic quotes."
* **Topics/Tags:** Add relevant topics like `pdf-generation`, `remarkable`, `planner`, `python`, `fpdf2`, `e-ink`, `digital-planner`, `ignatian-examen`. This improves discoverability.
* **LICENSE File:** Include the `LICENSE` file (MIT recommended, provided below).
* **Pin the Repository:** If it's a key project, pin it to your GitHub profile.

## Project Highlights & Version 2.2 Updates
This version (2.2) focuses on refining the codebase for clarity, maintainability, and ease of use, preparing it for public release.
-   **Code Refinement:** Reviewed and cleaned comments and code structure across all Python modules for professionalism and readability. Removed AI-like artifacts.
-   **Enhanced Documentation:** Updated `README.md` with detailed installation, usage, and project structure. Added `structure.txt` and a `LICENSE` file.
-   **Dependency Management:** Updated `requirements.txt` with necessary packages (`fpdf2`, `PyYAML`, `Pillow`).
-   **Author Attribution:** Added consistent author tagging in file headers and a "Crafted by" notice in main scripts.
-   **Robust Quote Loading:** Improved error handling and feedback in the quote loading utility.
-   **Clearer Output:** Refined console output during PDF generation.
-   **Preserved Functionality:** All original PDF layout and generation logic from version 2.1 remains intact, ensuring consistent output.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.