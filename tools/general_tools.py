import json
import os
import re
from datetime import datetime, timedelta
import dateparser
from langchain_core.tools import tool

ALARM_FILE = "alarms.json"

def parse_date(date_str: str) -> str:
    date_str = date_str.lower().strip()
    if date_str in ["today", "now"]:
        return datetime.now().strftime("%Y-%m-%d")
    if date_str == "tomorrow":
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if date_str == "day after tomorrow":
        return (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    parsed_date = dateparser.parse(date_str)

    if parsed_date:
        return parsed_date.strftime("%Y-%m-%d")

    raise ValueError(f"Invalid date format: {date_str}. Try formats like 'YYYY-MM-DD', 'March 10', 'next Friday', etc.")

def parse_time(time_str: str) -> str:
    time_formats = ["%H:%M", "%I:%M %p", "%I %p", "%H%M"]
    
    for fmt in time_formats:
        try:
            return datetime.strptime(time_str, fmt).strftime("%H:%M")
        except ValueError:
            continue

    raise ValueError(f"Invalid time format: {time_str}. Expected formats: HH:MM, h:mm AM/PM, etc.")

@tool(parse_docstring=True)
def set_alarm(time: str, date: str = None, message: str = "") -> dict:
    """Sets an alarm for a specified time and date.

    Args:
        time (str): The time for the alarm in 24-hour format (e.g., '14:30' for 2:30 PM).
        date (str, optional): The date for the alarm in 'YYYY-MM-DD' format. Defaults to today if not provided.
        message (str, optional): A message to display when the alarm goes off.

    Returns:
        dict: A dictionary containing alarm details:
            - id (int): A unique identifier for the alarm.
            - time (str): The alarm time in 'HH:MM' format.
            - date (str): The alarm date in 'YYYY-MM-DD' format.
            - message (str): The custom message for the alarm.
            - active_status (bool): Whether the alarm is active (always True when set).
    """
    try:
        parsed_time = parse_time(time)
    except ValueError as e:
        return {"error": str(e)}

    if date:
        try:
            parsed_date = parse_date(date)
        except ValueError as e:
            return {"error": str(e)}
    else:
        parsed_date = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(ALARM_FILE):
        with open(ALARM_FILE, "w") as file:
            json.dump([], file)

    with open(ALARM_FILE, "r") as file:
        try:
            alarms = json.load(file)
        except json.JSONDecodeError:
            alarms = []

    alarm_id = len(alarms) + 1

    alarm_entry = {
        "id": alarm_id,
        "time": parsed_time,
        "date": parsed_date,
        "message": message.strip(),
        "active_status": True
    }

    alarms.append(alarm_entry)
    with open(ALARM_FILE, "w") as file:
        json.dump(alarms, file, indent=4)

    return alarm_entry
