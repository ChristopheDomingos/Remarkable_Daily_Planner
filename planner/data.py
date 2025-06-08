# -*- coding: utf-8 -*-
# Remarkable Daily Planner
# Version 2.3
#
# Created by: Christophe Domingos
# Date: June 3, 2025 # Updated
#
# Description: Contains data for birthdays, anniversaries, and special dates.
#              Manually edit the lists below to customize your planner.

# BIRTHDAYS_ANNIVERSARIES_DATA
# Structure: {"type": "birthday" or "anniversary", "name": "Name", "day": DD, "month": MM, "year": YYYY (birth year or event year, optional)}
# For anniversaries like memorials, 'year' can be the year of the event if relevant, or None.
# Age for birthdays is calculated if 'year' (birth year) is provided.

BIRTHDAYS_ANNIVERSARIES_DATA = [
    # January
    {"type": "birthday", "name": "Alex Rosa", "day": 2, "month": 1, "year": None},
    {"type": "birthday", "name": "Prima Elodie", "day": 3, "month": 1, "year": None},
    {"type": "birthday", "name": "Fred", "day": 8, "month": 1, "year": None},
    {"type": "birthday", "name": "Prima Jéssica", "day": 18, "month": 1, "year": None},
    {"type": "birthday", "name": "Mãe", "day": 27, "month": 1, "year": None},
    # February
    {"type": "birthday", "name": "Miguel Quina", "day": 1, "month": 2, "year": None},
    {"type": "birthday", "name": "Tio Zé Dias", "day": 2, "month": 2, "year": None},
    {"type": "birthday", "name": "Mariana Silva", "day": 16, "month": 2, "year": None},
    {"type": "birthday", "name": "Prima Vidalina", "day": 21, "month": 2, "year": None},
    {"type": "anniversary", "name": "Avó Maria (Memorial)", "day": 28, "month": 2, "year": None},
    # March
    {"type": "birthday", "name": "Telma", "day": 1, "month": 3, "year": None},
    {"type": "birthday", "name": "Prima Sílvia", "day": 3, "month": 3, "year": None},
    {"type": "birthday", "name": "Francisco Simões", "day": 7, "month": 3, "year": None},
    {"type": "birthday", "name": "Pai", "day": 20, "month": 3, "year": None},
    {"type": "birthday", "name": "Higino", "day": 23, "month": 3, "year": None},
    {"type": "birthday", "name": "Julian", "day": 31, "month": 3, "year": 2024},
    # April
    {"type": "birthday", "name": "Primo Júlio", "day": 8, "month": 4, "year": None},
    {"type": "birthday", "name": "Tio Carlos Rosa", "day": 11, "month": 4, "year": None},
    {"type": "birthday", "name": "Avó Maria", "day": 17, "month": 4, "year": None},
    {"type": "birthday", "name": "Leonor", "day": 19, "month": 4, "year": None},
    {"type": "birthday", "name": "Padre Marco", "day": 24, "month": 4, "year": None},
    {"type": "anniversary", "name": "Klaudia's Dad (Memorial)", "day": 24, "month": 4, "year": None},
    {"type": "birthday", "name": "Catarina Garcia", "day": 27, "month": 4, "year": None},
    # May
    {"type": "birthday", "name": "Inês Carvalho", "day": 3, "month": 5, "year": None},
    {"type": "birthday", "name": "Prima Patrícia", "day": 7, "month": 5, "year": None},
    {"type": "birthday", "name": "Klara", "day": 13, "month": 5, "year": None},
    # June
    {"type": "birthday", "name": "Prima Gabriela", "day": 5, "month": 6, "year": None},
    {"type": "birthday", "name": "Tio Zé Santos", "day": 9, "month": 6, "year": None},
    {"type": "birthday", "name": "Tomé", "day": 12, "month": 6, "year": None},
    {"type": "birthday", "name": "Tia Fátima", "day": 15, "month": 6, "year": None},
    {"type": "birthday", "name": "Tio Fernando Sambento", "day": 15, "month": 6, "year": None},
    {"type": "birthday", "name": "Tola", "day": 19, "month": 6, "year": None},
    {"type": "birthday", "name": "Susana Valente", "day": 20, "month": 6, "year": None},
    # July
    {"type": "birthday", "name": "Romy", "day": 3, "month": 7, "year": None},
    {"type": "birthday", "name": "Kevin", "day": 7, "month": 7, "year": None},
    {"type": "birthday", "name": "Eli", "day": 12, "month": 7, "year": None},
    {"type": "birthday", "name": "Tia Fernanda", "day": 14, "month": 7, "year": None},
    {"type": "birthday", "name": "Alec", "day": 20, "month": 7, "year": None},
    {"type": "birthday", "name": "Cátia Correia", "day": 23, "month": 7, "year": None},
    {"type": "birthday", "name": "João Magalhães", "day": 26, "month": 7, "year": None},
    {"type": "birthday", "name": "Inês Correia", "day": 28, "month": 7, "year": None},
    # August
    {"type": "birthday", "name": "Prima Ilda", "day": 15, "month": 8, "year": None},
    {"type": "birthday", "name": "Mana", "day": 16, "month": 8, "year": None},
    {"type": "birthday", "name": "Clarinha", "day": 17, "month": 8, "year": None},
    {"type": "birthday", "name": "Prima Beatriz", "day": 23, "month": 8, "year": None},
    {"type": "birthday", "name": "Primo Vítor", "day": 24, "month": 8, "year": None},
    {"type": "birthday", "name": "Mathieu", "day": 26, "month": 8, "year": None},
    {"type": "birthday", "name": "Milene Santos", "day": 29, "month": 8, "year": None},
    {"type": "birthday", "name": "Primo Tomas", "day": 29, "month": 8, "year": None},
    # September
    {"type": "birthday", "name": "Elie", "day": 21, "month": 9, "year": None},
    # October
    {"type": "birthday", "name": "Eszter", "day": 2, "month": 10, "year": None},
    {"type": "birthday", "name": "Prima Carla", "day": 5, "month": 10, "year": None},
    {"type": "birthday", "name": "Tia Maria Alíce", "day": 20, "month": 10, "year": None},
    {"type": "birthday", "name": "Prima Inês Morais", "day": 27, "month": 10, "year": None},
    {"type": "birthday", "name": "Primo Alexandre Morais", "day": 31, "month": 10, "year": None},
    # November
    {"type": "birthday", "name": "Ana Perdigão", "day": 18, "month": 11, "year": None},
    {"type": "birthday", "name": "Prima Leslie", "day": 25, "month": 11, "year": None},
    # December
    {"type": "birthday", "name": "Vira", "day": 1, "month": 12, "year": None},
    {"type": "birthday", "name": "Tio Carlos Domingues", "day": 2, "month": 12, "year": None},
    {"type": "birthday", "name": "Tio Fernando Santos", "day": 11, "month": 12, "year": None},
    {"type": "birthday", "name": "Sara Trichet", "day": 17, "month": 12, "year": None},
    {"type": "birthday", "name": "Bianca", "day": 19, "month": 12, "year": 1992},
    {"type": "birthday", "name": "Maria Magano", "day": 25, "month": 12, "year": None},
    {"type": "birthday", "name": "João Magano", "day": 26, "month": 12, "year": None},
    {"type": "birthday", "name": "Klaudia Guderley", "day": 26, "month": 12, "year": None},
    {"type": "birthday", "name": "Tia Natália", "day": 28, "month": 12, "year": None},
]


# SPECIAL_DATES_DATA
# Structure: {"name": "Event Name", "day": DD, "month": MM, "year": YYYY (optional), "type": "holiday/saint/gift/other"}
# Populate this list with bank holidays, special gift dates, Saints' days, etc.
# The 'year' can be omitted if the event occurs annually on the same day/month.
# If 'year' is included, it will only be shown for that specific year.
# Example:
# {"name": "New Year's Day", "day": 1, "month": 1, "type": "holiday"},
# {"name": "St. Patrick's Day", "day": 17, "month": 3, "type": "saint"},
# {"name": "Project Deadline", "day": 15, "month": 6, "year": 2025, "type": "gift"} # A specific one-time event

SPECIAL_DATES_DATA = [
    # Add your special dates here
    # e.g. {"name": "Christmas Day", "day": 25, "month": 12, "type": "holiday"},
]