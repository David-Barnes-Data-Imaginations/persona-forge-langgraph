
from datetime import datetime
from langchain_core.tools.structured import StructuredTool


def get_now_datetime() -> datetime:
    """Wrapper for easier mocking in unit test."""
    return datetime.now()

def get_current_time() -> str:
    """Get the current time in format HH:MM AM/PM"""
    return get_now_datetime().strftime("%I:%M%p")

def _convert_date_to_words(dt: datetime):
    """Change date values represented in YYYY-mm-dd format to word values as they would be pronounced."""
    day = dt.day
    if day == 1 or day == 21 or day == 31:
        day_word = f"{day}st"
    elif day == 2 or day == 22:
        day_word = f"{day}nd"
    elif day == 3 or day == 23:
        day_word = f"{day}rd"
    else:
        day_word = f"{day}th"

    date_obj = dt.strftime(f"%B {day_word}, %Y")
    return date_obj

def get_current_date() -> str:
    """Get the current date in format YYYY-MM-DD"""
    dt = get_now_datetime()
    dt_str = _convert_date_to_words(dt)
    return dt_str

def get_tools():
    """Get a list of tools for the agent.

    Returns:
        A list of tool functions available to the agent.
    """
    return [
        StructuredTool.from_function(get_current_time),
        StructuredTool.from_function(get_current_date),
    ]