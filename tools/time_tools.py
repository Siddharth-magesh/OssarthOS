from datetime import datetime
from zoneinfo import ZoneInfo
from langchain_core.tools import tool

@tool(parse_docstring=True)
def get_time_in_timezone(timezone_name: str) -> str:
    """Returns the current time for a given timezone. 

    Args:
        timezone_name: IANA timezone name (e.g., 'America/New_York')

    Returns:
        str: Current time in the specified timezone
    """
    try:
        current_time = datetime.now(ZoneInfo(timezone_name))
        return current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception as e:
        return f"Error: Invalid timezone: {str(e)}"
