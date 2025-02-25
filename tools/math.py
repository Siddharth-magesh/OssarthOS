from langchain_core.tools import tool

@tool(parse_docstring=True)
def addition_tool(num1: int, num2: int):
    """A tool to add two numbers.

    Args:
        num1 (int): The first number.
        num2 (int): The second number.

    Returns:
        int: The sum of num1 and num2.
    """
    return num1 + num2
