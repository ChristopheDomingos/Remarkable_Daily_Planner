# planner/templates.py
from fpdf import FPDF
from planner.styles import (
    FONT_TITLE, FONT_BODY, FONT_EXAMEN_STEP_TITLE, FONT_EXAMEN_PROMPT,
    MARGIN_LEFT, MARGIN_RIGHT
)
import calendar as py_calendar
from datetime import timedelta, date
from planner.utils import load_quotes

# --- Color Definitions ---
COLOR_LIGHT_GRAY = (220, 220, 220)
COLOR_MEDIUM_GRAY = (200, 200, 200)
COLOR_DARK_GRAY = (150, 150, 150)
COLOR_BLACK = (0, 0, 0)

# --- Load Quotes (once when the module is loaded) ---
ALL_CATHOLIC_QUOTES = load_quotes("my_quotes.csv")

# --- Helper Functions ---
def _draw_horizontal_lines(pdf: FPDF, num_lines: int, line_height: float, indent: float = 0, column_width: float = 0, color=COLOR_LIGHT_GRAY):
    pdf.set_draw_color(*color)
    current_x_for_indent_calc = pdf.get_x()
    x_start = current_x_for_indent_calc + indent

    if column_width == 0:
        actual_line_width = pdf.w - x_start - pdf.r_margin
    else:
        actual_line_width = column_width

    if x_start < pdf.l_margin: x_start = pdf.l_margin

    start_y = pdf.get_y()
    for i in range(num_lines):
        current_y_for_line = start_y + (i * line_height)
        y_pos_for_drawing = current_y_for_line + line_height - (line_height * 0.30)
        line_end_x = min(x_start + actual_line_width, pdf.w - pdf.r_margin)
        pdf.line(x_start, y_pos_for_drawing, line_end_x, y_pos_for_drawing)
    pdf.set_y(start_y + (num_lines * line_height))
    pdf.set_draw_color(*COLOR_BLACK)


def _draw_tally_boxes(pdf: FPDF, num_boxes: int = 15, box_size: float = 3.5, indent: float = 0, color=COLOR_MEDIUM_GRAY):
    pdf.set_draw_color(*color)
    current_x_for_indent_calc = pdf.get_x()
    x_start_indent = current_x_for_indent_calc + indent
    y_pos = pdf.get_y() + 1

    if x_start_indent < pdf.l_margin : x_start_indent = pdf.l_margin

    page_width_available_for_boxes = pdf.w - x_start_indent - pdf.r_margin
    spacing = box_size / 2.5
    total_width_needed = num_boxes * box_size + (num_boxes - 1) * spacing
    if total_width_needed > page_width_available_for_boxes:
        if num_boxes > 1:
            spacing = max(0.5, (page_width_available_for_boxes - num_boxes * box_size) / (num_boxes - 1))
        else:
            spacing = 0.5

    for i in range(num_boxes):
        pdf.rect(x_start_indent + i * (box_size + spacing), y_pos, box_size, box_size, style='D')
    pdf.ln(box_size + spacing + 2)
    pdf.set_draw_color(*COLOR_BLACK)


def _draw_section_divider(pdf: FPDF, y_offset: float = 2, color=COLOR_LIGHT_GRAY, thickness=0.2):
    current_y = pdf.get_y() + y_offset
    pdf.set_draw_color(*color)
    pdf.set_line_width(thickness)
    pdf.line(pdf.l_margin, current_y, pdf.w - pdf.r_margin, current_y)
    pdf.set_draw_color(*COLOR_BLACK)
    pdf.set_line_width(0.2)
    pdf.ln(y_offset * 1.5)


# --- Page Template Functions ---

def create_monthly_overview(pdf: FPDF, year: int, month: int,
                            daily_page_link_ids: dict, calendar_page_target_id):
    pdf.add_page()
    is_a5 = pdf.w < 160

    if calendar_page_target_id is not None:
        pdf.set_link(calendar_page_target_id, y=0.0)

    month_name = py_calendar.month_name[month]
    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font(*FONT_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, 10, f"{month_name} {year}", ln=True, align='C')
    pdf.ln(6)

    pdf.set_font(FONT_BODY[0], 'B', 9)
    num_days_in_week = 7
    cal_cell_w = page_width / (num_days_in_week + 2)
    cal_cell_w = min(cal_cell_w, 12)
    cal_total_width = num_days_in_week * cal_cell_w
    cal_x_start = pdf.l_margin + (page_width - cal_total_width) / 2
    cal_cell_h = 5.5

    pdf.set_xy(cal_x_start, pdf.get_y())
    pdf.set_font(FONT_BODY[0], 'B', 8)
    day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for day_name in day_names:
        pdf.cell(cal_cell_w, cal_cell_h, day_name, border=0, align='C', ln=0)
    pdf.ln(cal_cell_h)

    cal_data = py_calendar.monthcalendar(year, month)
    pdf.set_font(FONT_BODY[0], '', 8)
    for week_data in cal_data:
        pdf.set_x(cal_x_start)
        for day in week_data:
            day_str = str(day) if day != 0 else ""
            link_to_daily_page_for_this_day = None
            if day != 0:
                current_cal_date = date(year, month, day)
                link_id = pdf.add_link()
                daily_page_link_ids[current_cal_date] = link_id
                link_to_daily_page_for_this_day = link_id
            pdf.cell(cal_cell_w, cal_cell_h, day_str, border=0, align='C', ln=0,
                     link=link_to_daily_page_for_this_day if link_to_daily_page_for_this_day else '')
        pdf.ln(cal_cell_h)
    pdf.ln(5)

    section_title_font = (FONT_BODY[0], 'B', 9)
    section_line_height = 6.5
    section_prompt_h = 6
    section_padding_after_lines = 3 if is_a5 else 4


    num_focus_lines = 3 # Changed from: 3 if is_a5 else 5
    pdf.set_x(pdf.l_margin)
    pdf.set_font(*section_title_font)
    pdf.cell(page_width, section_prompt_h, "Monthly Focus / Intentions", border=0, ln=1, align='L')
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, num_focus_lines, section_line_height, column_width=page_width, color=COLOR_DARK_GRAY)
    pdf.ln(section_padding_after_lines)

    if is_a5:
        col_width_a5 = page_width / 2 - 2 
        lines_for_a5_columns = 5 # Same number of lines for both

        key_dates_y_start = pdf.get_y()
        pdf.set_x(pdf.l_margin)
        pdf.set_font(*section_title_font)
        pdf.multi_cell(col_width_a5, section_prompt_h, "Key Dates & Deadlines", border=0, align='L', ln=1) # Use multi_cell for potential wrapping
        pdf.set_x(pdf.l_margin)
        _draw_horizontal_lines(pdf, lines_for_a5_columns, section_line_height, column_width=col_width_a5, color=COLOR_DARK_GRAY)
        left_col_end_y = pdf.get_y()

        pdf.set_xy(pdf.l_margin + col_width_a5 + 4, key_dates_y_start) 
        pdf.set_font(*section_title_font)
        pdf.multi_cell(col_width_a5, section_prompt_h, "Birthdays & Anniversaries", border=0, align='L', ln=1)
        pdf.set_x(pdf.l_margin + col_width_a5 + 4)
        _draw_horizontal_lines(pdf, lines_for_a5_columns, section_line_height, column_width=col_width_a5, color=COLOR_DARK_GRAY)
        right_col_end_y = pdf.get_y()

        pdf.set_y(max(left_col_end_y, right_col_end_y))
        pdf.ln(section_padding_after_lines)
    else: 
        pdf.set_x(pdf.l_margin)
        pdf.set_font(*section_title_font)
        pdf.cell(page_width, section_prompt_h, "Key Dates & Deadlines", border=0, ln=1, align='L')
        pdf.set_x(pdf.l_margin)
        _draw_horizontal_lines(pdf, 5, section_line_height, column_width=page_width, color=COLOR_DARK_GRAY)
        pdf.ln(section_padding_after_lines)

        pdf.set_x(pdf.l_margin)
        pdf.set_font(*section_title_font)
        pdf.cell(page_width, section_prompt_h, "Birthdays & Anniversaries", border=0, ln=1, align='L')
        pdf.set_x(pdf.l_margin)
        _draw_horizontal_lines(pdf, 7, section_line_height, column_width=page_width, color=COLOR_DARK_GRAY)
        pdf.ln(section_padding_after_lines)

    pdf.set_x(pdf.l_margin)
    pdf.set_font(*section_title_font)
    pdf.cell(page_width, section_prompt_h, "Ideas / Notes", border=0, ln=1, align='L')
    
    current_y_before_ideas = pdf.get_y()
    page_bottom_margin = pdf.b_margin 
    remaining_height_on_page = pdf.h - page_bottom_margin - current_y_before_ideas - section_line_height 
    
    num_ideas_lines = 0
    if remaining_height_on_page > 0:
        num_ideas_lines = max(1, int(remaining_height_on_page / section_line_height))
        default_max_ideas_a5 = 6 # Try to give more space for ideas on A5 now
        default_max_ideas_a4 = 6 
        if is_a5:
            num_ideas_lines = min(num_ideas_lines, default_max_ideas_a5) 
        else:
            num_ideas_lines = min(num_ideas_lines, default_max_ideas_a4)

    if num_ideas_lines > 0:
        pdf.set_x(pdf.l_margin)
        _draw_horizontal_lines(pdf, num_ideas_lines, section_line_height, column_width=page_width, color=COLOR_DARK_GRAY)
    pdf.ln(5)


def create_daily_page(pdf: FPDF, current_date,
                        calendar_link_id_for_nav_back,
                        target_id_for_this_page):
    pdf.add_page()
    is_a5 = pdf.w < 160

    if target_id_for_this_page is not None:
        pdf.set_link(target_id_for_this_page, y=0.0)

    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    
    month_name = current_date.strftime("%B")
    date_str = current_date.strftime("%A, %B %d, %Y")

    pdf.set_font(FONT_BODY[0], '', 10)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, 7, month_name.upper(), ln=True, align='C')

    pdf.set_font(*FONT_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, 10, date_str, ln=True, align='C', link=calendar_link_id_for_nav_back)
    pdf.ln(2) 

    day_of_year_idx = current_date.timetuple().tm_yday - 1
    quote = "Focus on the good."
    author = "Unknown"
    if ALL_CATHOLIC_QUOTES:
        quote_index = day_of_year_idx % len(ALL_CATHOLIC_QUOTES)
        quote, author = ALL_CATHOLIC_QUOTES[quote_index]

    pdf.set_font(FONT_BODY[0], 'I', 9)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, 4.5, f'"{quote}"', align='C', ln=1)

    pdf.set_font(FONT_BODY[0], '', 8)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, 4, f"- {author}", align='C', ln=1)
    pdf.ln(3)
    
    # Task lines: 10 for both A5 and A4 as per new request for A5.
    num_task_lines = 10

    line_item_height = 6.5 
    marker_width = 5
    tasks_title_height = 8
    tasks_padding_after = 2

    pdf.set_font(FONT_BODY[0], 'B', 10)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, tasks_title_height, "Tasks:", ln=True)

    pdf.set_font(*FONT_BODY)
    line_x_start_for_item = pdf.l_margin + marker_width
    available_width_for_item_line = page_width - marker_width
    for _ in range(num_task_lines):
        current_y_before_cell = pdf.get_y()
        # Ensure we don't draw tasks if we are too close to the bottom margin
        if current_y_before_cell + line_item_height > pdf.h - pdf.b_margin:
            break # Stop adding tasks if no space
        pdf.set_x(pdf.l_margin)
        circle_radius = 0.8
        circle_y = current_y_before_cell + (line_item_height / 2) - circle_radius
        pdf.set_fill_color(*COLOR_DARK_GRAY)
        pdf.ellipse(pdf.get_x() + circle_radius , circle_y, circle_radius, circle_radius, style='DF')
        pdf.set_xy(pdf.l_margin + marker_width, current_y_before_cell)
        line_y = current_y_before_cell + (line_item_height / 2) + 0.5
        pdf.set_draw_color(*COLOR_LIGHT_GRAY)
        pdf.line(line_x_start_for_item, line_y, line_x_start_for_item + available_width_for_item_line, line_y)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_xy(pdf.l_margin, current_y_before_cell + line_item_height)
    pdf.ln(tasks_padding_after)

    journal_title_height = 8
    journal_line_height = 7 # Keep journal line height standard
    
    pdf.set_font(FONT_BODY[0], 'B', 10)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, journal_title_height, "Journal", ln=True)
    
    # Calculate remaining space for journal lines dynamically
    current_y_before_journal_lines = pdf.get_y()
    # pdf.b_margin is where auto-page-break would occur.
    # Space available from current_y to where content should stop before hitting b_margin.
    # Subtract a small buffer (e.g., half a line height) to avoid lines touching the very edge of drawable area.
    remaining_height_for_journal_actual = (pdf.h - pdf.b_margin) - current_y_before_journal_lines - (journal_line_height * 0.3)
    
    actual_journal_lines = 0
    if remaining_height_for_journal_actual > 0:
         actual_journal_lines = max(0, int(remaining_height_for_journal_actual / journal_line_height))
    
    # For A4, the user requested 20 journal lines if tasks are 10
    if not is_a5:
        actual_journal_lines = 20 # Override calculation for A4 target

    pdf.set_font(*FONT_BODY)
    pdf.set_x(pdf.l_margin)
    if actual_journal_lines > 0:
        _draw_horizontal_lines(pdf, actual_journal_lines, journal_line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)


def create_daily_reflection_page(pdf: FPDF, current_date):
    pdf.add_page()
    page_width_content = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font(FONT_TITLE[0], FONT_TITLE[1], 14)
    page_title = f"Daily Particular Examen"
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width_content, 8, page_title, ln=True, align='C')
    pdf.ln(5)

    section_line_height = 6.5
    prompt_line_height = 5
    notes_lines = 2
    tally_box_indent = 8
    line_indent = 0

    pdf.set_font(*FONT_EXAMEN_STEP_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=6, txt="MORNING: Resolve & Grace", align='L', ln=1)

    pdf.set_font(*FONT_EXAMEN_PROMPT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_line_height, txt="Specific fault to avoid / virtue to cultivate today:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, 1, section_line_height + 1, indent=line_indent, column_width=page_width_content, color=COLOR_DARK_GRAY)

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_line_height, txt="Grace I ask for (e.g., 'for patience,' 'to be more attentive,' 'strength against [my focus area]'):", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, 1, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_DARK_GRAY)
    _draw_section_divider(pdf, y_offset=3, color=COLOR_MEDIUM_GRAY, thickness=0.1)

    pdf.set_font(*FONT_EXAMEN_STEP_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=6, txt="MIDDAY: Examination & Tally (since waking)", align='L', ln=1)

    pdf.set_font(*FONT_EXAMEN_PROMPT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_line_height, txt="Instances of [focus area] this period:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_tally_boxes(pdf, num_boxes=12, box_size=3, indent=tally_box_indent, color=COLOR_DARK_GRAY)

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_line_height, txt="Brief reflection/observation:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)
    _draw_section_divider(pdf, y_offset=3, color=COLOR_MEDIUM_GRAY, thickness=0.1)

    pdf.set_font(*FONT_EXAMEN_STEP_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=6, txt="EVENING: Examination & Tally (since midday)", align='L', ln=1)

    pdf.set_font(*FONT_EXAMEN_PROMPT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_line_height, txt="Instances of [focus area] this period:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_tally_boxes(pdf, num_boxes=12, box_size=3, indent=tally_box_indent, color=COLOR_DARK_GRAY)

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_line_height, txt="Brief reflection/observation:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)
    _draw_section_divider(pdf, y_offset=3, color=COLOR_MEDIUM_GRAY, thickness=0.1)

    pdf.set_font(*FONT_EXAMEN_STEP_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=6, txt="NIGHT: Overall Reflection & Gratitude", align='L', ln=1)

    pdf.set_font(*FONT_EXAMEN_PROMPT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_line_height, txt="Comparing midday and evening, what have I learned?", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_line_height, txt="For what am I grateful regarding this effort today?", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_line_height, txt="Resolve for tomorrow concerning this point (continue, adjust, new focus?):", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)


def create_weekly_overview(pdf: FPDF, week_start_date):
    pdf.add_page()
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    is_a5 = pdf.w < 160

    pdf.set_font(*FONT_TITLE)
    week_end_date = week_start_date + timedelta(days=6)
    title = f"Weekly Plan & Review: {week_start_date.strftime('%b %d')} - {week_end_date.strftime('%b %d, %Y')}"
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, 10, title, ln=True, align='C')
    pdf.ln(1 if is_a5 else 2) # Reduced more for A5

    section_title_font = (FONT_BODY[0], 'B', 10)
    prompt_font_family = FONT_BODY[0]
    prompt_style = 'B'
    prompt_font_size = 9

    line_height = 5.0 if is_a5 else 6.0
    prompt_h = 4.0 if is_a5 else 5.0
    section_spacing = 1.0 if is_a5 else 2.0 # Reduced spacing for A5
    inter_title_spacing = 0.5 if is_a5 else 1.0 # Reduced spacing for A5

    lines_top_3 = 3
    lines_appointments = 3 if is_a5 else 5
    lines_skills = 2 if is_a5 else 3
    lines_gratitude = 2
    lines_accomplishments = 3 if is_a5 else 5
    lines_challenges = 2 if is_a5 else 3

    # --- "Plan for the Week" Title ---
    pdf.set_font(*section_title_font)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, 7, "Plan for the Week", ln=1, align='L')
    pdf.ln(inter_title_spacing)

    # --- Centered Habit Tracker (Moved Up) ---
    pdf.set_font(FONT_BODY[0], '', 7)
    suggested_habits = ["Prayer", "Exercise", "Reading", "Focus Virtue", "Act of Service"]
    day_labels = ["M", "T", "W", "T", "F", "S", "S"]
    
    habit_label_width = 35 if is_a5 else 40 # Adjusted for A5
    day_cell_fixed_width = (page_width * 0.7 - habit_label_width) / 7 # Make tracker take ~70% of page width
    day_cell_fixed_width = max(6, day_cell_fixed_width) # Ensure min width for day cells
    
    tracker_total_width = habit_label_width + (7 * day_cell_fixed_width)
    tracker_x_start = pdf.l_margin + (page_width - tracker_total_width) / 2
    table_cell_h = 3.5 if is_a5 else 4.0 # Reduced for A5

    pdf.set_x(tracker_x_start)
    pdf.set_font(FONT_BODY[0], 'B', 7)
    pdf.set_fill_color(*COLOR_LIGHT_GRAY)
    pdf.cell(habit_label_width, table_cell_h, "Habit", border='LTRB', align="L", ln=0, fill=True)
    for day in day_labels:
        pdf.cell(day_cell_fixed_width, table_cell_h, day, border='LTRB', align="C", ln=0, fill=True)
    pdf.ln(table_cell_h)
    pdf.set_fill_color(*COLOR_BLACK)

    pdf.set_font(FONT_BODY[0], '', 7)
    for i, habit in enumerate(suggested_habits):
        pdf.set_x(tracker_x_start)
        pdf.set_draw_color(*COLOR_MEDIUM_GRAY)
        border_style = 'LRB' if i < len(suggested_habits) - 1 else 'LTRB'
        pdf.cell(habit_label_width, table_cell_h, habit, border=border_style, align="L", ln=0)
        for k_day in range(len(day_labels)):
            pdf.set_draw_color(*COLOR_MEDIUM_GRAY)
            current_cell_border = border_style
            if k_day == len(day_labels) -1 and 'R' not in border_style : current_cell_border += 'R'
            pdf.cell(day_cell_fixed_width, table_cell_h, "", border=current_cell_border, align="C", ln=0)
            box_x_offset = (day_cell_fixed_width - 3) / 2
            box_y_offset = (table_cell_h - 3) / 2
            pdf.set_draw_color(*COLOR_DARK_GRAY)
            pdf.rect(pdf.get_x() - day_cell_fixed_width + box_x_offset, pdf.get_y() + box_y_offset, 3, 3, style='D')
        pdf.ln(table_cell_h)
    pdf.set_draw_color(*COLOR_BLACK)
    pdf.ln(section_spacing + (0.5 if is_a5 else 1.0))

    # --- Planning Subsections ---
    pdf.set_font(prompt_font_family, prompt_style, prompt_font_size)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Top 3 Priorities:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, lines_top_3, line_height, column_width=page_width, color=COLOR_DARK_GRAY)
    pdf.ln(section_spacing)

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Appointments & Key Dates:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, lines_appointments, line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(section_spacing)

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Skills / Learning Focus:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, lines_skills, line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(section_spacing)

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Weekly Gratitude:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, lines_gratitude, line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(section_spacing)

    _draw_section_divider(pdf, y_offset= (0 if is_a5 else 0.5), thickness=0.1, color=COLOR_MEDIUM_GRAY)

    pdf.set_font(*section_title_font)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, 7, "Reflection on the Past Week", align='L', ln=1)
    pdf.ln(inter_title_spacing)
    
    pdf.set_font(prompt_font_family, prompt_style, prompt_font_size)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Key Accomplishments / Wins:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, lines_accomplishments, line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(section_spacing)

    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Challenges & Lessons Learned:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, lines_challenges, line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(section_spacing)


def create_weekly_examen_page(pdf: FPDF, week_start_date):
    pdf.add_page()
    is_a5 = pdf.w < 160
    page_width_content = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font(*FONT_TITLE)
    week_str = week_start_date.strftime("%d/%m/%Y")
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width_content, 10, "Weekly General Examen of Consciousness", ln=True, align='C')
    pdf.set_font(*FONT_BODY)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width_content, 7, f"Week Starting {week_str}", ln=True, align='C')
    pdf.ln(4 if is_a5 else 7) # Reduced padding for A5

    # A5 specific adjustments to fit on one page
    line_height_for_writing = 5.5 if is_a5 else 7.0
    space_after_prompt_text = 1.0 if is_a5 else 1.5
    extra_space_between_steps = 1.0 if is_a5 else 2.0 # Reduced significantly for A5
    step_title_h = 5 if is_a5 else 6
    prompt_text_h = 4 if is_a5 else 5
    
    # Adjusted line counts for A5
    lines_step1 = 2 if is_a5 else 4
    lines_step2 = 2 if is_a5 else 3
    lines_step3 = 3 if is_a5 else 7 # Significantly reduced for A5
    lines_step4 = 2 if is_a5 else 4
    lines_step5 = 2 if is_a5 else 4


    prompts_config = [
        ("Step 1: Presence & Gratitude",
         "Where did I feel most aware of God's presence (or deep peace/connection) this week? For what specific gifts, moments, or insights am I most grateful?", lines_step1),
        ("Step 2: Pray for Light & Insight",
         "I ask for the light to see this past week as God sees it, with honesty and compassion. What specific insights or understanding do I seek about my experiences?", lines_step2),
        ("Step 3: Review the Week",
         "Looking back over the week, what were the significant events, my thoughts, feelings, and actions?\n"
         "  - Moments of Consolation (Joy, peace, love, faith, connection, energy):\n"
         "  - Moments of Desolation (Sadness, anxiety, fear, disconnection, dryness):\n"
         "  - My Dominant Feelings & Interior Movements:\n"
         "  - Key Decisions & My Responses:", lines_step3),
        ("Step 4: Seek Reconciliation & Healing",
         "Where did I miss the mark, act unlovingly, or fail to respond to God's invitations? What do I need to ask forgiveness for (from God, others, myself)? Where do I need healing?", lines_step4),
        ("Step 5: Resolve & Look Forward with Hope",
         "How is God inviting me to respond to what I've reviewed? With hope and reliance on grace, what is one concrete way I can cooperate more fully with God's love and plan in the week ahead?", lines_step5)
    ]
    
    temp_font_step_title = (FONT_EXAMEN_STEP_TITLE[0], FONT_EXAMEN_STEP_TITLE[1], 11 if is_a5 else FONT_EXAMEN_STEP_TITLE[2])
    temp_font_prompt = (FONT_EXAMEN_PROMPT[0], FONT_EXAMEN_PROMPT[1], 9 if is_a5 else FONT_EXAMEN_PROMPT[2])


    for step_title_text, prompt_text, num_lines in prompts_config:
        pdf.set_font(*temp_font_step_title) # Use potentially smaller font for A5
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=page_width_content, h=step_title_h, txt=step_title_text, align='L', ln=1)

        pdf.set_font(*temp_font_prompt) # Use potentially smaller font for A5
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=page_width_content, h=prompt_text_h, txt=prompt_text, align='L', ln=1)

        pdf.set_x(pdf.l_margin)
        if space_after_prompt_text > 0:
            pdf.ln(space_after_prompt_text)
        else:
            pdf.ln(1) # Ensure some space
        pdf.set_x(pdf.l_margin)
        _draw_horizontal_lines(pdf, num_lines, line_height_for_writing, column_width=page_width_content, color=COLOR_LIGHT_GRAY)

        if extra_space_between_steps > 0:
            pdf.ln(extra_space_between_steps)

def create_monthly_examen_page(pdf: FPDF, month_name_full: str, year: int):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    page_width_content = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width_content, 10, "Monthly General Examen of Consciousness", ln=True, align='C')
    pdf.set_font(FONT_BODY[0],'',9)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width_content, 7, f"{month_name_full} {year}", ln=True, align='C')
    pdf.ln(4)

    line_height_for_writing = 6.5
    space_after_prompt_text = 1
    extra_space_between_steps = 1.5

    prompts_config = [
        ("Step 1: Presence & Gratitude",
         "Overarching themes of God's presence and significant blessings this month:", 3),
        ("Step 2: Pray for Light & Insight",
         "Key insights about myself, my relationship with God, or my path that emerged this month:", 3),
        ("Step 3: Review the Month",
         "Dominant patterns of consolation/desolation; significant spiritual movements, events, and responses:", 3),
        ("Step 4: Seek Reconciliation & Healing",
         "Ongoing areas requiring forgiveness, healing, and transformation as I move forward:", 3),
        ("Step 5: Resolve & Hope for Next Month",
         "Primary resolution or focus for living more consciously next month? Sources of hope & strength:", 3)
    ]

    for step_title_text, prompt_text, num_lines in prompts_config:
        pdf.set_font(*FONT_EXAMEN_STEP_TITLE)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=page_width_content, h=5, txt=step_title_text, align='L', ln=1)

        pdf.set_font(*FONT_EXAMEN_PROMPT)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=page_width_content, h=4.5, txt=prompt_text, align='L', ln=1)

        pdf.set_x(pdf.l_margin)
        if space_after_prompt_text > 0:
            pdf.ln(space_after_prompt_text)
        else:
            pdf.ln(0.5)
        pdf.set_x(pdf.l_margin)
        _draw_horizontal_lines(pdf, num_lines, line_height_for_writing, column_width=page_width_content, color=COLOR_LIGHT_GRAY)

        if extra_space_between_steps > 0:
            pdf.ln(extra_space_between_steps)