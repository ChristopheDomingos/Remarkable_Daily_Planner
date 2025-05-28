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
    
    x_start = pdf.get_x() + indent 
    # If x_start is effectively the left margin due to prior set_x, calculate width relative to that.
    # Or if indent is 0 and pdf.get_x() is already l_margin.
    if abs(x_start - pdf.l_margin) < 0.1 and indent == 0 : 
         x_start = pdf.l_margin 
    
    if column_width == 0: 
        # Full page width from current x_start to right margin
        actual_line_width = pdf.w - x_start - pdf.r_margin
    else: 
        # Use the provided column_width as the actual_line_width if lines are within a column
        actual_line_width = column_width
    
    for _ in range(num_lines):
        current_y_for_line = pdf.get_y()
        # Position line towards bottom of allocated space for better writing feel
        y_pos = current_y_for_line + line_height - (line_height * 0.30) 
        
        line_end_x = min(x_start + actual_line_width, pdf.w - pdf.r_margin)
        pdf.line(x_start, y_pos, line_end_x, y_pos)
        pdf.ln(line_height) 
    pdf.set_draw_color(*COLOR_BLACK) 

def _draw_tally_boxes(pdf: FPDF, num_boxes: int = 15, box_size: float = 3.5, indent: float = 0, color=COLOR_MEDIUM_GRAY):
    pdf.set_draw_color(*color)
    x_start = pdf.get_x() + indent
    y_pos = pdf.get_y() + 1 
    
    page_width = pdf.w - pdf.l_margin - pdf.r_margin - indent
    spacing = box_size / 2.5 
    if (num_boxes * (box_size + spacing) - spacing) > page_width:
        spacing = max(0.5, (page_width - num_boxes * box_size) / (num_boxes -1 if num_boxes > 1 else 1))

    for i in range(num_boxes):
        pdf.rect(x_start + i * (box_size + spacing), y_pos, box_size, box_size, style='D')
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

def create_monthly_overview(pdf: FPDF, year: int, month: int): 
    pdf.add_page()
    month_name = py_calendar.month_name[month]
    
    pdf.set_font(*FONT_TITLE)
    pdf.cell(0, 10, f"{month_name} {year}", ln=True, align='C')
    pdf.ln(4) 

    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_spacing = 8
    col_width = (page_width - col_spacing) / 2

    left_col_x_start = pdf.l_margin
    current_y_col_start = pdf.get_y()

    # --- Left Column: Mini Calendar, Key Dates, Birthdays ---
    pdf.set_xy(left_col_x_start, current_y_col_start)
    pdf.set_font(FONT_BODY[0], 'B', 9) 
    pdf.cell(col_width, 6, "Calendar", border=0, ln=1, align='L') 
    pdf.set_x(left_col_x_start) 
    
    cal = py_calendar.monthcalendar(year, month)
    day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    cell_w = col_width / 7 
    cell_h = 5.5

    pdf.set_font(FONT_BODY[0], 'B', 8) 
    for day_name in day_names:
        pdf.cell(cell_w, cell_h, day_name, border=0, align='C', ln=0)
    pdf.ln(cell_h) 

    pdf.set_font(FONT_BODY[0], '', 8) 
    for week_data in cal:
        pdf.set_x(left_col_x_start) 
        for day in week_data:
            day_str = str(day) if day != 0 else ""
            pdf.cell(cell_w, cell_h, day_str, border=0, align='C', ln=0) 
        pdf.ln(cell_h) 
    pdf.ln(3) 
    
    pdf.set_x(left_col_x_start)
    pdf.set_font(FONT_BODY[0], 'B', 9)
    pdf.cell(col_width, 6, "Key Dates & Deadlines", border=0, ln=1, align='L')
    pdf.set_x(left_col_x_start)
    _draw_horizontal_lines(pdf, 5, 6, column_width=col_width, color=COLOR_DARK_GRAY) 
    pdf.ln(3)

    pdf.set_x(left_col_x_start)
    pdf.set_font(FONT_BODY[0], 'B', 9)
    pdf.cell(col_width, 6, "Birthdays & Anniversaries", border=0, ln=1, align='L')
    pdf.set_x(left_col_x_start)
    _draw_horizontal_lines(pdf, 7, 6, column_width=col_width, color=COLOR_DARK_GRAY) # 7 lines
    left_col_final_y = pdf.get_y()
    
    # --- Right Column: Focus & Notes ---
    right_col_x_start = pdf.l_margin + col_width + col_spacing
    pdf.set_xy(right_col_x_start, current_y_col_start) 
    
    pdf.set_font(FONT_BODY[0], 'B', 9)
    pdf.cell(col_width, 6, "Monthly Focus / Intentions", border=0, ln=1, align='L')
    pdf.set_x(right_col_x_start)
    _draw_horizontal_lines(pdf, 5, 7, column_width=col_width, color=COLOR_DARK_GRAY) # 5 lines
    pdf.ln(4)
    
    pdf.set_font(FONT_BODY[0], 'B', 9)
    pdf.set_x(right_col_x_start)
    pdf.cell(col_width, 6, "Ideas / Notes", border=0, ln=1, align='L')
    pdf.set_x(right_col_x_start)
    
    ideas_notes_lines_start_y = pdf.get_y()
    # Align bottom of "Ideas/Notes" with bottom of "Birthdays" (which is left_col_final_y)
    available_height_for_ideas_notes = left_col_final_y - ideas_notes_lines_start_y
    ideas_notes_line_height = 7 
    num_ideas_notes_lines = 0
    if available_height_for_ideas_notes > ideas_notes_line_height:
        num_ideas_notes_lines = int(available_height_for_ideas_notes / ideas_notes_line_height)
    
    num_ideas_notes_lines = max(0, num_ideas_notes_lines) # Ensure it's not negative
    
    if num_ideas_notes_lines > 0:
        _draw_horizontal_lines(pdf, num_ideas_notes_lines, ideas_notes_line_height, column_width=col_width, color=COLOR_DARK_GRAY)
    
    right_col_final_y = pdf.get_y()

    pdf.set_y(max(left_col_final_y, right_col_final_y)) 
    pdf.ln(5)


def create_daily_page(pdf: FPDF, current_date):
    pdf.add_page()
    
    month_name = current_date.strftime("%B")
    date_str = current_date.strftime("%A, %B %d, %Y") 
    pdf.set_font(FONT_BODY[0], '', 10) 
    pdf.cell(0, 7, month_name.upper(), ln=True, align='C')
    pdf.set_font(*FONT_TITLE)
    pdf.cell(0, 10, date_str, ln=True, align='C')
    pdf.ln(4)

    day_of_year_idx = current_date.timetuple().tm_yday - 1 
    
    quote = "Focus on the good." 
    author = "Unknown" 
    if ALL_CATHOLIC_QUOTES: 
        quote_index = day_of_year_idx % len(ALL_CATHOLIC_QUOTES)
        quote, author = ALL_CATHOLIC_QUOTES[quote_index]
    
    pdf.set_font(FONT_BODY[0], 'I', 9) 
    pdf.multi_cell(0, 5, f'"{quote}"', align='C')
    pdf.set_font(FONT_BODY[0], '', 8) 
    pdf.multi_cell(0, 4, f"- {author}", align='C') 
    pdf.ln(4) # Removed section divider after quote

    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    line_item_height = 6.5 
    marker_width = 5 

    pdf.set_font(FONT_BODY[0], 'B', 10) 
    pdf.cell(0, 8, "Tasks:", ln=True) 
    
    pdf.set_font(*FONT_BODY)
    line_x_start_for_item = pdf.l_margin + marker_width
    available_width_for_item_line = page_width - marker_width
    for _ in range(10): 
        current_y_before_cell = pdf.get_y()
        pdf.set_x(pdf.l_margin) 
        
        circle_radius = 0.8 
        circle_y = current_y_before_cell + (line_item_height / 2) - circle_radius
        pdf.set_fill_color(*COLOR_DARK_GRAY) 
        pdf.ellipse(pdf.get_x() + circle_radius , circle_y, 
                    circle_radius, circle_radius, style='DF') 
        pdf.set_xy(pdf.get_x() + marker_width, current_y_before_cell) 
        
        line_y = current_y_before_cell + (line_item_height / 2) + 0.5 
        pdf.set_draw_color(*COLOR_LIGHT_GRAY)
        pdf.line(line_x_start_for_item, line_y, line_x_start_for_item + available_width_for_item_line, line_y)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_xy(pdf.l_margin, current_y_before_cell + line_item_height) 
    pdf.ln(2) 
    
    pdf.set_font(FONT_BODY[0], 'B', 10)
    pdf.cell(0, 8, "Journal", ln=True) # Changed title, removed divider before
    pdf.set_font(*FONT_BODY)
    
    current_y_before_journal_lines = pdf.get_y()
    bottom_safe_limit = pdf.h - pdf.b_margin 
    remaining_page_height = bottom_safe_limit - current_y_before_journal_lines - 3 # 3mm conceptual bottom padding
    
    num_journal_lines = 0
    journal_line_height = 7 # Height of each journal line
    if remaining_page_height > journal_line_height:
        num_journal_lines = int(remaining_page_height / journal_line_height)
    
    if num_journal_lines > 0:
        _draw_horizontal_lines(pdf, num_journal_lines, journal_line_height, color=COLOR_LIGHT_GRAY)


def create_daily_reflection_page(pdf: FPDF, current_date): 
    pdf.add_page()
    # original_font_settings removed

    pdf.set_font(FONT_TITLE[0], FONT_TITLE[1], 14) 
    page_title = f"Daily Particular Examen"
    pdf.cell(0, 8, page_title, ln=True, align='C')
    # Date subtitle removed as per user request in previous iterations
    pdf.ln(5)

    section_line_height = 6.5 
    prompt_line_height = 5 
    notes_lines = 2
    tally_box_indent = 8 
    line_indent = 0 

    pdf.set_font(*FONT_EXAMEN_STEP_TITLE)
    pdf.multi_cell(w=0, h=6, txt="MORNING: Resolve & Grace", align='L')
    
    pdf.set_font(*FONT_EXAMEN_PROMPT)
    pdf.multi_cell(w=0, h=prompt_line_height, txt="Specific fault to avoid / virtue to cultivate today:", align='L')
    _draw_horizontal_lines(pdf, 1, section_line_height + 1, indent=line_indent, color=COLOR_DARK_GRAY)
    
    pdf.multi_cell(w=0, h=prompt_line_height, txt="Grace I ask for (e.g., 'for patience,' 'to be more attentive,' 'strength against [my focus area]'):", align='L')
    _draw_horizontal_lines(pdf, 1, section_line_height, indent=line_indent, color=COLOR_DARK_GRAY)
    _draw_section_divider(pdf, y_offset=3, color=COLOR_MEDIUM_GRAY, thickness=0.1)

    pdf.set_font(*FONT_EXAMEN_STEP_TITLE)
    pdf.multi_cell(w=0, h=6, txt="MIDDAY: Examination & Tally (since waking)", align='L')

    pdf.set_font(*FONT_EXAMEN_PROMPT)
    pdf.multi_cell(w=0, h=prompt_line_height, txt="Instances of [focus area] this period:", align='L')
    _draw_tally_boxes(pdf, num_boxes=12, box_size=3, indent=tally_box_indent, color=COLOR_DARK_GRAY) 
    
    pdf.multi_cell(w=0, h=prompt_line_height, txt="Brief reflection/observation:", align='L')
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, color=COLOR_LIGHT_GRAY)
    _draw_section_divider(pdf, y_offset=3, color=COLOR_MEDIUM_GRAY, thickness=0.1)

    pdf.set_font(*FONT_EXAMEN_STEP_TITLE)
    pdf.multi_cell(w=0, h=6, txt="EVENING: Examination & Tally (since midday)", align='L')

    pdf.set_font(*FONT_EXAMEN_PROMPT)
    pdf.multi_cell(w=0, h=prompt_line_height, txt="Instances of [focus area] this period:", align='L')
    _draw_tally_boxes(pdf, num_boxes=12, box_size=3, indent=tally_box_indent, color=COLOR_DARK_GRAY)

    pdf.multi_cell(w=0, h=prompt_line_height, txt="Brief reflection/observation:", align='L')
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, color=COLOR_LIGHT_GRAY)
    _draw_section_divider(pdf, y_offset=3, color=COLOR_MEDIUM_GRAY, thickness=0.1)

    pdf.set_font(*FONT_EXAMEN_STEP_TITLE)
    pdf.multi_cell(w=0, h=6, txt="NIGHT: Overall Reflection & Gratitude", align='L')

    pdf.set_font(*FONT_EXAMEN_PROMPT)
    pdf.multi_cell(w=0, h=prompt_line_height, txt="Comparing midday and evening, what have I learned?", align='L')
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, color=COLOR_LIGHT_GRAY)

    pdf.multi_cell(w=0, h=prompt_line_height, txt="For what am I grateful regarding this effort today?", align='L')
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, color=COLOR_LIGHT_GRAY)

    pdf.multi_cell(w=0, h=prompt_line_height, txt="Resolve for tomorrow concerning this point (continue, adjust, new focus?):", align='L')
    _draw_horizontal_lines(pdf, notes_lines, section_line_height, indent=line_indent, color=COLOR_LIGHT_GRAY)
    # original_font_settings removed from here too

def create_weekly_overview(pdf: FPDF, week_start_date): 
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    week_end_date = week_start_date + timedelta(days=6) 
    title = f"Weekly Plan & Review: {week_start_date.strftime('%b %d')} - {week_end_date.strftime('%b %d, %Y')}" 
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(4)

    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_width = page_width / 2 - 4 
    col_spacing = 8
    
    line_height = 6
    prompt_h = 5
    section_title_font = (FONT_BODY[0], 'B', 10)
    prompt_font = FONT_EXAMEN_PROMPT

    current_y_left_start = pdf.get_y()
    pdf.set_font(*section_title_font)
    pdf.set_x(pdf.l_margin)
    pdf.cell(col_width, 7, "Plan for the Week", ln=1)
    
    pdf.set_font(FONT_BODY[0], 'B', 9) 
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(col_width, prompt_h, "Top 3 Priorities:", align='L') 
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, 3, line_height, column_width=col_width, color=COLOR_DARK_GRAY) 
    pdf.ln(3)

    pdf.set_font(FONT_BODY[0], 'B', 9)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(col_width, prompt_h, "Appointments & Key Dates:", align='L')
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, 4, line_height, column_width=col_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(3)

    pdf.set_font(FONT_BODY[0], 'B', 9)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(col_width, prompt_h, "Skills / Learning Focus:", align='L')
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, 2, line_height, column_width=col_width, color=COLOR_LIGHT_GRAY)
    left_col_end_y = pdf.get_y()

    pdf.set_xy(pdf.l_margin + col_width + col_spacing, current_y_left_start) 
    pdf.set_font(*section_title_font)
    pdf.cell(col_width, 7, "Habit Tracker", ln=1) 
    
    pdf.set_font(FONT_BODY[0], '', 7) 
    suggested_habits = ["Prayer", "Exercise", "Reading", "Focus Virtue", "Act of Service"] 
    day_labels = ["M", "T", "W", "T", "F", "S", "S"] 
    
    habit_header_width = col_width * 0.45 
    day_cell_width = (col_width * 0.55) / 7
    table_cell_h = 4.5 

    current_x_right_col = pdf.l_margin + col_width + col_spacing
    pdf.set_x(current_x_right_col)
    pdf.set_font(FONT_BODY[0], 'B', 7)
    pdf.set_fill_color(*COLOR_LIGHT_GRAY) 
    pdf.cell(habit_header_width, table_cell_h, "Habit", border='B', align="L", ln=0, fill=True) 
    for day in day_labels:
        pdf.cell(day_cell_width, table_cell_h, day, border='B', align="C", ln=0, fill=True) 
    pdf.ln(table_cell_h)
    pdf.set_fill_color(*COLOR_BLACK) 

    pdf.set_font(FONT_BODY[0], '', 7)
    for i, habit in enumerate(suggested_habits):
        pdf.set_x(current_x_right_col)
        pdf.set_draw_color(*COLOR_MEDIUM_GRAY) 
        pdf.cell(habit_header_width, table_cell_h, habit, border='B', align="L", ln=0) 
        for _ in day_labels:
            box_x = pdf.get_x() + (day_cell_width / 2) - 1.5
            box_y = pdf.get_y() + (table_cell_h / 2) - 1.5
            pdf.set_draw_color(*COLOR_DARK_GRAY) 
            pdf.rect(box_x, box_y, 3, 3, style='D') 
            pdf.set_x(pdf.get_x() + day_cell_width) 
        pdf.ln(table_cell_h)
    pdf.set_draw_color(*COLOR_BLACK) 
    pdf.ln(4) 
    
    pdf.set_font(FONT_BODY[0], 'B', 9)
    pdf.set_x(current_x_right_col)
    pdf.multi_cell(col_width, prompt_h, "Weekly Gratitude:", align='L')
    pdf.set_x(current_x_right_col)
    _draw_horizontal_lines(pdf, 2, line_height, column_width=col_width, color=COLOR_LIGHT_GRAY)
    right_col_end_y = pdf.get_y()


    pdf.set_y(max(left_col_end_y, right_col_end_y) + 5)
    _draw_section_divider(pdf, y_offset=1, thickness=0.1, color=COLOR_MEDIUM_GRAY)

    pdf.set_font(*section_title_font)
    pdf.set_x(pdf.l_margin) 
    pdf.multi_cell(0, 7, "Reflection on the Past Week", align='L') 
    
    pdf.set_font(*prompt_font)
    current_y_review_start = pdf.get_y()
    
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(col_width, prompt_h, "Key Accomplishments / Wins:", align='L')
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, 2, line_height, column_width=col_width, color=COLOR_LIGHT_GRAY)
    left_review_end_y = pdf.get_y()
    
    pdf.set_xy(pdf.l_margin + col_width + col_spacing, current_y_review_start)
    pdf.multi_cell(col_width, prompt_h, "Challenges & Lessons Learned:", align='L')
    pdf.set_x(pdf.l_margin + col_width + col_spacing)
    _draw_horizontal_lines(pdf, 2, line_height, column_width=col_width, color=COLOR_LIGHT_GRAY)
    right_review_end_y = pdf.get_y()

    pdf.set_y(max(left_review_end_y, right_review_end_y) + 2) 


def create_weekly_examen_page(pdf: FPDF, week_start_date):
    pdf.add_page()
    pdf.set_font(*FONT_TITLE) 
    week_str = week_start_date.strftime("%d/%m/%Y")
    pdf.cell(0, 10, "Weekly General Examen of Consciousness", ln=True, align='C') 
    pdf.set_font(*FONT_BODY) 
    pdf.cell(0, 7, f"Week Starting {week_str}", ln=True, align='C')
    pdf.ln(7)

    line_height_for_writing = 7 
    space_after_prompt_text = 1.5 
    extra_space_between_steps = 3
    
    prompts_config = [
        ("Step 1: Presence & Gratitude",
         "Where did I feel most aware of God's presence (or deep peace/connection) this week? For what specific gifts, moments, or insights am I most grateful?", 4),
        ("Step 2: Pray for Light & Insight",
         "I ask for the light to see this past week as God sees it, with honesty and compassion. What specific insights or understanding do I seek about my experiences?", 3),
        ("Step 3: Review the Week",
         "Looking back over the week, what were the significant events, my thoughts, feelings, and actions?\n"
         "  - Moments of Consolation (Joy, peace, love, faith, connection, energy):\n" 
         "  - Moments of Desolation (Sadness, anxiety, fear, disconnection, dryness):\n"
         "  - My Dominant Feelings & Interior Movements:\n"                               
         "  - Key Decisions & My Responses:", 7),                                        
        ("Step 4: Seek Reconciliation & Healing",
         "Where did I miss the mark, act unlovingly, or fail to respond to God's invitations? What do I need to ask forgiveness for (from God, others, myself)? Where do I need healing?", 4),
        ("Step 5: Resolve & Look Forward with Hope",
         "How is God inviting me to respond to what I've reviewed? With hope and reliance on grace, what is one concrete way I can cooperate more fully with God's love and plan in the week ahead?", 4)
    ]

    for step_title_text, prompt_text, num_lines in prompts_config:
        pdf.set_font(*FONT_EXAMEN_STEP_TITLE) 
        pdf.multi_cell(w=0, h=6, txt=step_title_text, align='L', border=0)

        pdf.set_font(*FONT_EXAMEN_PROMPT)
        pdf.multi_cell(w=0, h=5, txt=prompt_text, align='L', border=0)
        
        pdf.set_x(pdf.l_margin) 
        if space_after_prompt_text > 0:
            pdf.ln(space_after_prompt_text) 
        else: 
            pdf.ln(2) 

        _draw_horizontal_lines(pdf, num_lines, line_height_for_writing, color=COLOR_LIGHT_GRAY)
        
        if extra_space_between_steps > 0:
            pdf.ln(extra_space_between_steps)

def create_monthly_examen_page(pdf: FPDF, month_name_full: str, year: int): 
    pdf.add_page()
    pdf.set_font(*FONT_TITLE)
    pdf.cell(0, 10, "Monthly General Examen of Consciousness", ln=True, align='C') 
    pdf.set_font(FONT_BODY[0],'',9) 
    pdf.cell(0, 7, f"{month_name_full} {year}", ln=True, align='C')
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
        pdf.multi_cell(w=0, h=5, txt=step_title_text, align='L', border=0) 

        pdf.set_font(*FONT_EXAMEN_PROMPT)
        pdf.multi_cell(w=0, h=4.5, txt=prompt_text, align='L', border=0) 
        
        pdf.set_x(pdf.l_margin)
        if space_after_prompt_text > 0:
            pdf.ln(space_after_prompt_text)
        else:
            pdf.ln(0.5) 

        _draw_horizontal_lines(pdf, num_lines, line_height_for_writing, color=COLOR_LIGHT_GRAY)
        
        if extra_space_between_steps > 0:
            pdf.ln(extra_space_between_steps)