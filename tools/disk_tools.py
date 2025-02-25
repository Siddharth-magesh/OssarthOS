import shutil
from langchain_core.tools import tool

@tool(parse_docstring=True)
def get_disk_usage():
    """Retrieves disk usage statistics.

    Returns:
        dict: A dictionary containing disk usage statistics:
            - total (str): Total disk space in GB
            - used (str): Used disk space in GB
            - free (str): Free disk space in GB
    """
    path = "/"
    total, used, free = shutil.disk_usage(path)
    gb = 1024 * 1024 * 1024

    return {
        "total": f"{total / gb:.2f} GB",
        "used": f"{used / gb:.2f} GB",
        "free": f"{free / gb:.2f} GB",
    }