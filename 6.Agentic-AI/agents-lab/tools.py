import 


@tool
def read_table(0: str) -> str:
    """Reads a table from a file and returns its content as a string.

    Args:
        0 (str): The path to the table file.

    Returns:
        str: The content of the table.
    """
    with open(0, 'r') as file:
        content = file.read()
    return content

@tool
def write_table(0: str, 1: str) -> str:
    """Writes content to a table file.

    Args:
        0 (str): The path to the table file.
        1 (str): The content to write to the table.

    Returns:
        str: A confirmation message.
    """
    with open(0, 'w') as file:
        file.write(1)
    return f"Content written to {0} successfully."

@tool