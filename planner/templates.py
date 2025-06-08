# -*- coding: utf-8 -*-
# Remarkable Daily Planner
# Version 2.3
#
# Created by: Christophe Domingos
# Date: June 3, 2025 # Updated

from fpdf import FPDF
from planner.styles import (
    FONT_TITLE, FONT_BODY, FONT_EXAMEN_STEP_TITLE, FONT_EXAMEN_PROMPT
)
import calendar as py_calendar
from datetime import timedelta, date
from planner.utils import load_quotes
from planner.data import BIRTHDAYS_ANNIVERSARIES_DATA, SPECIAL_DATES_DATA

COLOR_LIGHT_GRAY = (220, 220, 220)
COLOR_MEDIUM_GRAY = (200, 200, 200)
COLOR_DARK_GRAY = (150, 150, 150)
COLOR_BLACK = (0, 0, 0)

ALL_CATHOLIC_QUOTES = load_quotes("my_quotes.csv")

def _draw_horizontal_lines(pdf: FPDF, num_lines: int, line_height: float, indent: float = 0, column_width: float = 0, color=COLOR_LIGHT_GRAY):
    pdf.set_draw_color(*color)
    x_start = pdf.get_x() + indent
    if column_width == 0:
        actual_line_width = pdf.w - x_start - pdf.r_margin
    else:
        actual_line_width = column_width
    if x_start < pdf.l_margin: x_start = pdf.l_margin
    start_y = pdf.get_y()
    for i in range(num_lines):
        y_pos_for_drawing = start_y + (i * line_height) + line_height - (line_height * 0.30)
        line_end_x = min(x_start + actual_line_width, pdf.w - pdf.r_margin)
        pdf.line(x_start, y_pos_for_drawing, line_end_x, y_pos_for_drawing)
    pdf.set_y(start_y + (num_lines * line_height))
    pdf.set_draw_color(*COLOR_BLACK)

def _draw_tally_boxes(pdf: FPDF, num_boxes: int = 15, box_size: float = 3.5, indent: float = 0, color=COLOR_MEDIUM_GRAY):
    pdf.set_draw_color(*color)
    x_start_indent = pdf.get_x() + indent
    y_pos = pdf.get_y() + 1
    if x_start_indent < pdf.l_margin : x_start_indent = pdf.l_margin
    page_width_available_for_boxes = pdf.w - x_start_indent - pdf.r_margin
    spacing = box_size / 2.5
    total_width_needed = num_boxes * box_size + (num_boxes - 1) * spacing
    if total_width_needed > page_width_available_for_boxes:
        spacing = max(0.5, (page_width_available_for_boxes - num_boxes * box_size) / (num_boxes - 1)) if num_boxes > 1 else 0.5
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

def create_monthly_overview(pdf: FPDF, year: int, month: int,
                            daily_page_link_ids: dict, # This dict will be populated
                            calendar_page_target_id):  # INT link ID for this page itself
    pdf.add_page()
    is_a5 = pdf.w < 160
    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    if calendar_page_target_id is not None:
        pdf.set_link(calendar_page_target_id, y=0.0) 

    month_name = py_calendar.month_name[month]
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
        for day_number in week_data:
            day_str = str(day_number) if day_number != 0 else ""
            link_to_daily_page_for_this_day = None
            if day_number != 0:
                current_cal_date = date(year, month, day_number)
                # Original v2.2 style linking: add link ID here, store it, use in cell
                link_id = pdf.add_link() 
                daily_page_link_ids[current_cal_date] = link_id 
                link_to_daily_page_for_this_day = link_id
            
            pdf.cell(cal_cell_w, cal_cell_h, day_str, border=0, align='C', ln=0,
                     link=link_to_daily_page_for_this_day if link_to_daily_page_for_this_day else '')
        pdf.ln(cal_cell_h)
    pdf.ln(5)

    # --- Sections Layout (Birthdays first, then Key Dates, Focus, Ideas) ---
    # (Layout for these sections from v2.4.1 remains the same)
    section_title_font = (FONT_BODY[0], 'B', 9)
    section_line_height = 5.0 if is_a5 else 6.0 
    section_text_font_size = 7 if is_a5 else 8
    section_prompt_h = 6
    section_padding_after_lines = 3 if is_a5 else 4
    
    pdf.set_font(*section_title_font) 
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, section_prompt_h, "Birthdays & Anniversaries", border=0, ln=1, align='L')

    events_this_month = [b for b in BIRTHDAYS_ANNIVERSARIES_DATA if b['month'] == month]
    events_this_month.sort(key=lambda x: x['day'])

    if events_this_month:
        birthday_font_size = 6 if is_a5 else 7 
        pdf.set_font(FONT_BODY[0], '', birthday_font_size) 
        line_h_bday = 3.8 if is_a5 else 4.2 
        num_cols = 3
        col_spacing = 2  
        col_width = (page_width - (num_cols - 1) * col_spacing) / num_cols
        max_entries_per_col = 5
        col_starts_x = [pdf.l_margin + i * (col_width + col_spacing) for i in range(num_cols)]
        initial_y_birthdays_section = pdf.get_y()
        max_y_col_end = initial_y_birthdays_section 
        for c_idx in range(num_cols):
            current_col_y_pos = initial_y_birthdays_section 
            pdf.set_xy(col_starts_x[c_idx], current_col_y_pos)
            for i in range(max_entries_per_col):
                entry_overall_idx = c_idx * max_entries_per_col + i
                if entry_overall_idx < len(events_this_month):
                    event = events_this_month[entry_overall_idx]
                    age_str = ""
                    if event['type'] == 'birthday' and event.get('year'):
                        age = year - event['year']
                        try:
                            bday_this_year_obj = date(year, event['month'], event['day'])
                            if date(year, month, 15).month > event['month']: pass
                            elif date(year, month, 15).month == event['month']:
                                if date(year, month, 15).day < event['day']: age -=1
                            else: age -=1
                        except ValueError: pass 
                        if age < 0: age = 0 
                        age_str = f" ({age})" if age >= 0 else ""
                    display_text = f"{event['day']:02d}: {event['name']}{age_str}"
                    if entry_overall_idx == (num_cols * max_entries_per_col) - 1 and len(events_this_month) > (num_cols * max_entries_per_col):
                        display_text = "..."
                    x_before_multicell = col_starts_x[c_idx]
                    pdf.set_x(x_before_multicell)
                    pdf.multi_cell(col_width, line_h_bday, display_text, border=0, align='L', ln=0) 
                    current_col_y_pos += line_h_bday 
                    pdf.set_xy(x_before_multicell, current_col_y_pos) 
                else: break 
            max_y_col_end = max(max_y_col_end, current_col_y_pos) 
        pdf.set_y(max_y_col_end)
    else: 
        pdf.set_font(FONT_BODY[0], 'I', section_text_font_size) 
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(page_width, section_line_height, "None this month.", align='L', ln=1)
    pdf.ln(section_padding_after_lines / 1.5) 

    pdf.set_font(*section_title_font) 
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, section_prompt_h, "Key Dates & Deadlines", border=0, ln=1, align='L')
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, 3, section_line_height, column_width=page_width, color=COLOR_DARK_GRAY)
    pdf.ln(section_padding_after_lines)

    pdf.set_font(*section_title_font) 
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, section_prompt_h, "Monthly Focus / Intentions", border=0, ln=1, align='L')
    pdf.set_x(pdf.l_margin)
    _draw_horizontal_lines(pdf, 3, section_line_height, column_width=page_width, color=COLOR_DARK_GRAY)
    pdf.ln(section_padding_after_lines)

    pdf.set_font(*section_title_font) 
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, section_prompt_h, "Ideas / Notes", border=0, ln=1, align='L')
    current_y_before_ideas = pdf.get_y()
    page_bottom_margin = pdf.b_margin
    remaining_height_on_page = pdf.h - page_bottom_margin - current_y_before_ideas - section_line_height 
    num_ideas_lines = 0
    if remaining_height_on_page > 0:
        num_ideas_lines = max(1, int(remaining_height_on_page / section_line_height))
        default_max_ideas_a5 = 3 if is_a5 else 4 
        default_max_ideas_a4 = 4 if not is_a5 else 3
        num_ideas_lines = min(num_ideas_lines, default_max_ideas_a5 if is_a5 else default_max_ideas_a4)
    if num_ideas_lines > 0:
        pdf.set_x(pdf.l_margin)
        _draw_horizontal_lines(pdf, num_ideas_lines, section_line_height, column_width=page_width, color=COLOR_DARK_GRAY)
    pdf.ln(5)
    # No return needed for links_to_add_on_calendar_page with this original linking style


def create_daily_page(pdf: FPDF, current_date_obj: date,
                        calendar_link_id_for_nav_back, 
                        target_id_for_this_page: int): # target_id is an INT
    pdf.add_page()
    if target_id_for_this_page is not None:
        pdf.set_link(target_id_for_this_page, y=0.0) # Define this page as the target for the ID

    is_a5 = pdf.w < 160
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    month_name = current_date_obj.strftime("%B")
    date_str = current_date_obj.strftime("%A, %B %d, %Y")
    pdf.set_font(FONT_BODY[0], '', 10)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, 7, month_name.upper(), ln=True, align='C')
    pdf.set_font(*FONT_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, 10, date_str, ln=True, align='C', link=calendar_link_id_for_nav_back) 
    pdf.ln(2) 
    day_of_year_idx = current_date_obj.timetuple().tm_yday - 1
    quote_text = "Focus on the good."
    author_text = "Unknown"
    if ALL_CATHOLIC_QUOTES:
        quote_index = day_of_year_idx % len(ALL_CATHOLIC_QUOTES)
        quote_text, author_text = ALL_CATHOLIC_QUOTES[quote_index]
    pdf.set_font(FONT_BODY[0], 'I', 9)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, 4.5, f'"{quote_text}"', align='C', ln=1)
    pdf.set_font(FONT_BODY[0], '', 8)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, 4, f"- {author_text}", align='C', ln=1)
    pdf.ln(3)
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
        if current_y_before_cell + line_item_height > pdf.h - pdf.b_margin: break 
        pdf.set_x(pdf.l_margin)
        circle_radius = 0.8
        circle_y = current_y_before_cell + (line_item_height / 2) - circle_radius 
        pdf.set_fill_color(*COLOR_DARK_GRAY)
        pdf.ellipse(pdf.get_x() + circle_radius, circle_y, circle_radius, circle_radius, style='DF')
        pdf.set_xy(pdf.l_margin + marker_width, current_y_before_cell)
        line_y_pos = current_y_before_cell + (line_item_height / 2) + 0.5 
        pdf.set_draw_color(*COLOR_LIGHT_GRAY)
        pdf.line(line_x_start_for_item, line_y_pos, line_x_start_for_item + available_width_for_item_line, line_y_pos)
        pdf.set_draw_color(*COLOR_BLACK)
        pdf.set_xy(pdf.l_margin, current_y_before_cell + line_item_height)
    pdf.ln(tasks_padding_after)
    journal_title_height = 8
    journal_line_height = 7
    pdf.set_font(FONT_BODY[0], 'B', 10)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, journal_title_height, "Journal", ln=True)
    current_y_before_journal_lines = pdf.get_y()
    remaining_height_for_journal = (pdf.h - pdf.b_margin) - current_y_before_journal_lines - (journal_line_height * 0.3)
    actual_journal_lines = 0
    if remaining_height_for_journal > 0:
         actual_journal_lines = max(0, int(remaining_height_for_journal / journal_line_height))
    if not is_a5: 
        target_a4_lines = (pdf.h - pdf.b_margin - current_y_before_journal_lines - (journal_line_height*0.3) ) // journal_line_height
        actual_journal_lines = max(0, int(target_a4_lines))
    pdf.set_font(*FONT_BODY)
    pdf.set_x(pdf.l_margin)
    if actual_journal_lines > 0:
        _draw_horizontal_lines(pdf, actual_journal_lines, journal_line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)

def create_weekly_overview(pdf: FPDF, week_start_date: date,
                             calendar_link_id_for_nav_back, 
                             target_id_for_this_page: int): # target_id is an INT for this page
    pdf.add_page()
    if target_id_for_this_page is not None:
        pdf.set_link(target_id_for_this_page, y=0.0) # Define this page as the target
    
    page_width = pdf.w - pdf.l_margin - pdf.r_margin
    is_a5 = pdf.w < 160
    pdf.set_font(*FONT_TITLE)
    week_end_date = week_start_date + timedelta(days=6)
    title_str = f"Weekly Plan & Review: {week_start_date.strftime('%b %d')} - {week_end_date.strftime('%b %d, %Y')}"
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, 10, title_str, ln=True, align='C', link=calendar_link_id_for_nav_back) 
    pdf.ln(1 if is_a5 else 2)
    # ... (Rest of weekly overview content from v2.4.1/2.5.0 - it doesn't change with this linking revert)
    section_title_font = (FONT_BODY[0], 'B', 10)
    prompt_font_family, _, _ = FONT_BODY
    prompt_style = 'B'
    prompt_font_size = 9
    line_height = 5.0 if is_a5 else 6.0
    prompt_h = 4.0 if is_a5 else 5.0
    section_spacing = 1.0 if is_a5 else 2.0
    inter_title_spacing = 0.5 if is_a5 else 1.0
    lines_top_3 = 3
    lines_appointments = 3 if is_a5 else 5
    lines_skills = 2 if is_a5 else 3
    lines_gratitude = 2
    lines_accomplishments = 3 if is_a5 else 5
    lines_challenges = 2 if is_a5 else 3
    pdf.set_font(*section_title_font)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width, 7, "Plan for the Week", ln=1, align='L')
    pdf.ln(inter_title_spacing)
    pdf.set_font(FONT_BODY[0], 'B', 8) 
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Habit Tracker", align='L', ln=1)
    pdf.set_font(FONT_BODY[0], 'I', 7) 
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, 3, "Fill this tracker daily to monitor your progress.", align='L', ln=1)
    pdf.ln(0.5 if is_a5 else 1)
    suggested_habits = ["Prayer", "Exercise", "Reading", "Focus Virtue", "Act of Service"]
    day_labels = ["M", "T", "W", "T", "F", "S", "S"]
    habit_label_width = 35 if is_a5 else 40
    day_cell_fixed_width = (page_width * 0.7 - habit_label_width) / 7 
    day_cell_fixed_width = max(6, day_cell_fixed_width)
    tracker_total_width = habit_label_width + (7 * day_cell_fixed_width)
    tracker_x_start = pdf.l_margin + (page_width - tracker_total_width) / 2
    table_cell_h = 3.5 if is_a5 else 4.0
    pdf.set_xy(tracker_x_start, pdf.get_y())
    pdf.set_font(FONT_BODY[0], 'B', 7)
    pdf.set_fill_color(*COLOR_LIGHT_GRAY)
    pdf.cell(habit_label_width, table_cell_h, "Habit", border='LTRB', align="L", ln=0, fill=True)
    for day in day_labels:
        pdf.cell(day_cell_fixed_width, table_cell_h, day, border='LTRB', align="C", ln=0, fill=True)
    pdf.ln(table_cell_h)
    pdf.set_font(FONT_BODY[0], '', 7)
    for i, habit in enumerate(suggested_habits):
        pdf.set_x(tracker_x_start)
        pdf.set_draw_color(*COLOR_MEDIUM_GRAY)
        border_style = 'LRB' if i < len(suggested_habits) - 1 else 'LTRB'
        pdf.cell(habit_label_width, table_cell_h, habit, border=border_style, align="L", ln=0)
        for k_day in range(len(day_labels)):
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
    pdf.set_font(prompt_font_family, prompt_style, prompt_font_size)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Top 3 Priorities:", align='L', ln=1)
    _draw_horizontal_lines(pdf, lines_top_3, line_height, column_width=page_width, color=COLOR_DARK_GRAY)
    pdf.ln(section_spacing)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Appointments & Key Dates:", align='L', ln=1)
    _draw_horizontal_lines(pdf, lines_appointments, line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(section_spacing)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Skills / Learning Focus:", align='L', ln=1)
    _draw_horizontal_lines(pdf, lines_skills, line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(section_spacing)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Weekly Gratitude:", align='L', ln=1)
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
    _draw_horizontal_lines(pdf, lines_accomplishments, line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(section_spacing)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(page_width, prompt_h, "Challenges & Lessons Learned:", align='L', ln=1)
    _draw_horizontal_lines(pdf, lines_challenges, line_height, column_width=page_width, color=COLOR_LIGHT_GRAY)
    pdf.ln(section_spacing)


# create_daily_reflection_page (A5 sizing adjustments from v2.4.1)
# create_weekly_examen_page, create_monthly_examen_page (unchanged from v2.4.1)
def create_daily_reflection_page(pdf: FPDF, current_date_obj: date):
    pdf.add_page()
    page_width_content = pdf.w - pdf.l_margin - pdf.r_margin
    is_a5 = pdf.w < 160
    font_fam_step, font_sty_step, font_siz_step = FONT_EXAMEN_STEP_TITLE
    font_fam_prompt, font_sty_prompt, font_siz_prompt = FONT_EXAMEN_PROMPT
    local_font_size_step = max(8, font_siz_step - (1 if is_a5 else 1)) 
    local_font_size_prompt = max(7, font_siz_prompt - (1 if is_a5 else 1)) 
    CURRENT_FONT_EXAMEN_STEP_TITLE = (font_fam_step, font_sty_step, local_font_size_step)
    CURRENT_FONT_EXAMEN_PROMPT = (font_fam_prompt, font_sty_prompt, local_font_size_prompt)
    pdf.set_font(FONT_TITLE[0], FONT_TITLE[1], 12 if is_a5 else 14) 
    page_title = "Daily Particular Examen"
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width_content, 6 if is_a5 else 8, page_title, ln=True, align='C')
    pdf.ln(2 if is_a5 else 3) 
    section_line_height = 5.0 if is_a5 else 6.0  
    prompt_cell_h = 4.0 if is_a5 else 4.5        
    notes_lines_per_section = 3 if is_a5 else 2  
    tally_box_indent = 6 if is_a5 else 8      
    line_indent = 0           
    y_offset_divider = 1.0 if is_a5 else 1.5 
    ln_after_prompt_group = 0.2 if is_a5 else 0.5 
    pdf.set_font(*CURRENT_FONT_EXAMEN_STEP_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h + (1 if is_a5 else 1.5), txt="MORNING: Resolve & Grace", align='L', ln=1) 
    pdf.set_font(*CURRENT_FONT_EXAMEN_PROMPT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h, txt="Specific fault to avoid / virtue to cultivate today:", align='L', ln=1)
    _draw_horizontal_lines(pdf, 1, section_line_height + (0 if is_a5 else 0.5) , indent=line_indent, column_width=page_width_content, color=COLOR_DARK_GRAY) 
    pdf.ln(ln_after_prompt_group)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h, txt="Grace I ask for (e.g., 'for patience,' 'to be more attentive,' 'strength against [my focus area]'):", align='L', ln=1)
    _draw_horizontal_lines(pdf, 1, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_DARK_GRAY)
    _draw_section_divider(pdf, y_offset=y_offset_divider, color=COLOR_MEDIUM_GRAY, thickness=0.1)
    pdf.set_font(*CURRENT_FONT_EXAMEN_STEP_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h + (1 if is_a5 else 1.5), txt="MIDDAY: Examination & Tally (since waking)", align='L', ln=1)
    pdf.set_font(*CURRENT_FONT_EXAMEN_PROMPT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h, txt="Instances of [focus area] this period:", align='L', ln=1)
    pdf.set_x(pdf.l_margin) 
    _draw_tally_boxes(pdf, num_boxes=10 if is_a5 else 12, box_size=2.5 if is_a5 else 3, indent=tally_box_indent, color=COLOR_DARK_GRAY)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h, txt="Brief reflection/observation:", align='L', ln=1)
    _draw_horizontal_lines(pdf, notes_lines_per_section, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)
    _draw_section_divider(pdf, y_offset=y_offset_divider, color=COLOR_MEDIUM_GRAY, thickness=0.1)
    pdf.set_font(*CURRENT_FONT_EXAMEN_STEP_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h + (1 if is_a5 else 1.5), txt="EVENING: Examination & Tally (since midday)", align='L', ln=1)
    pdf.set_font(*CURRENT_FONT_EXAMEN_PROMPT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h, txt="Instances of [focus area] this period:", align='L', ln=1)
    pdf.set_x(pdf.l_margin)
    _draw_tally_boxes(pdf, num_boxes=10 if is_a5 else 12, box_size=2.5 if is_a5 else 3, indent=tally_box_indent, color=COLOR_DARK_GRAY)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h, txt="Brief reflection/observation:", align='L', ln=1)
    _draw_horizontal_lines(pdf, notes_lines_per_section, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)
    _draw_section_divider(pdf, y_offset=y_offset_divider, color=COLOR_MEDIUM_GRAY, thickness=0.1)
    pdf.set_font(*CURRENT_FONT_EXAMEN_STEP_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h + (1 if is_a5 else 1.5), txt="NIGHT: Overall Reflection & Gratitude", align='L', ln=1)
    pdf.set_font(*CURRENT_FONT_EXAMEN_PROMPT)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h, txt="Comparing midday and evening, what have I learned?", align='L', ln=1)
    _draw_horizontal_lines(pdf, notes_lines_per_section, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)
    pdf.ln(ln_after_prompt_group)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h, txt="For what am I grateful regarding this effort today?", align='L', ln=1)
    _draw_horizontal_lines(pdf, notes_lines_per_section, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)
    pdf.ln(ln_after_prompt_group)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=page_width_content, h=prompt_cell_h, txt="Resolve for tomorrow concerning this point (continue, adjust, new focus?):", align='L', ln=1)
    _draw_horizontal_lines(pdf, notes_lines_per_section, section_line_height, indent=line_indent, column_width=page_width_content, color=COLOR_LIGHT_GRAY)

def create_weekly_examen_page(pdf: FPDF, week_start_date: date):
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
    pdf.ln(4 if is_a5 else 7) 
    line_height_for_writing = 5.5 if is_a5 else 7.0
    space_after_prompt_text = 1.0 if is_a5 else 1.5
    extra_space_between_steps = 1.0 if is_a5 else 2.0 
    step_title_h = 5 if is_a5 else 6 
    prompt_text_h = 4 if is_a5 else 5 
    lines_step1 = 2 if is_a5 else 4
    lines_step2 = 2 if is_a5 else 3
    lines_step3 = 3 if is_a5 else 7
    lines_step4 = 2 if is_a5 else 4
    lines_step5 = 2 if is_a5 else 4
    prompts_config = [
        ("Step 1: Presence & Gratitude", "Where did I feel most aware of God's presence (or deep peace/connection) this week? For what specific gifts, moments, or insights am I most grateful?", lines_step1),
        ("Step 2: Pray for Light & Insight", "I ask for the light to see this past week as God sees it, with honesty and compassion. What specific insights or understanding do I seek about my experiences?", lines_step2),
        ("Step 3: Review the Week", "Looking back over the week, what were the significant events, my thoughts, feelings, and actions?\n  - Moments of Consolation (Joy, peace, love, faith, connection, energy):\n  - Moments of Desolation (Sadness, anxiety, fear, disconnection, dryness):\n  - My Dominant Feelings & Interior Movements:\n  - Key Decisions & My Responses:", lines_step3),
        ("Step 4: Seek Reconciliation & Healing", "Where did I miss the mark, act unlovingly, or fail to respond to God's invitations? What do I need to ask forgiveness for (from God, others, myself)? Where do I need healing?", lines_step4),
        ("Step 5: Resolve & Look Forward with Hope", "How is God inviting me to respond to what I've reviewed? With hope and reliance on grace, what is one concrete way I can cooperate more fully with God's love and plan in the week ahead?", lines_step5)
    ]
    font_fam_step, font_sty_step, font_siz_step = FONT_EXAMEN_STEP_TITLE
    font_fam_prompt, font_sty_prompt, font_siz_prompt = FONT_EXAMEN_PROMPT
    current_font_step_title = (font_fam_step, font_sty_step, 11 if is_a5 else font_siz_step)
    current_font_prompt = (font_fam_prompt, font_sty_prompt, 9 if is_a5 else font_siz_prompt)
    for step_title_text, prompt_text, num_lines in prompts_config:
        pdf.set_font(*current_font_step_title)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=page_width_content, h=step_title_h, txt=step_title_text, align='L', ln=1)
        pdf.set_font(*current_font_prompt)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=page_width_content, h=prompt_text_h, txt=prompt_text, align='L', ln=1)
        pdf.set_x(pdf.l_margin) 
        if space_after_prompt_text > 0: pdf.ln(space_after_prompt_text)
        else: pdf.ln(1)
        _draw_horizontal_lines(pdf, num_lines, line_height_for_writing, column_width=page_width_content, color=COLOR_LIGHT_GRAY)
        if extra_space_between_steps > 0: pdf.ln(extra_space_between_steps)

def create_monthly_examen_page(pdf: FPDF, month_name_full: str, year: int):
    pdf.add_page()
    page_width_content = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_font(*FONT_TITLE)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width_content, 10, "Monthly General Examen of Consciousness", ln=True, align='C')
    pdf.set_font(FONT_BODY[0],'',9)
    pdf.set_x(pdf.l_margin)
    pdf.cell(page_width_content, 7, f"{month_name_full} {year}", ln=True, align='C')
    pdf.ln(4) 
    line_height_for_writing = 6.5
    space_after_prompt_text = 1.0
    extra_space_between_steps = 1.5
    step_title_h = 5 
    prompt_text_h = 4.5
    prompts_config = [
        ("Step 1: Presence & Gratitude", "Overarching themes of God's presence and significant blessings this month:", 3),
        ("Step 2: Pray for Light & Insight", "Key insights about myself, my relationship with God, or my path that emerged this month:", 3),
        ("Step 3: Review the Month", "Dominant patterns of consolation/desolation; significant spiritual movements, events, and responses:", 3),
        ("Step 4: Seek Reconciliation & Healing", "Ongoing areas requiring forgiveness, healing, and transformation as I move forward:", 3),
        ("Step 5: Resolve & Hope for Next Month", "Primary resolution or focus for living more consciously next month? Sources of hope & strength:", 3)
    ]
    for step_title_text, prompt_text, num_lines in prompts_config:
        pdf.set_font(*FONT_EXAMEN_STEP_TITLE) 
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=page_width_content, h=step_title_h, txt=step_title_text, align='L', ln=1)
        pdf.set_font(*FONT_EXAMEN_PROMPT) 
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=page_width_content, h=prompt_text_h, txt=prompt_text, align='L', ln=1)
        pdf.set_x(pdf.l_margin)
        if space_after_prompt_text > 0: pdf.ln(space_after_prompt_text)
        else: pdf.ln(0.5)
        _draw_horizontal_lines(pdf, num_lines, line_height_for_writing, column_width=page_width_content, color=COLOR_LIGHT_GRAY)
        if extra_space_between_steps > 0: pdf.ln(extra_space_between_steps)