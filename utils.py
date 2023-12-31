import re

NUM_OR_DOT_REGEX = re.compile(r"^[0-9.]$")


def is_num_or_dot(string: str) -> bool:
    """
    Check if a string contains only digits or a dot.
    Args:
        string (str): The input string to be checked.
    Returns:
        bool: True if the string contains only digits or a dot, False
        otherwise.
    """
    return NUM_OR_DOT_REGEX.search(string)


def is_valid_number(string: str) -> bool:
    valid = False
    try:
        float(string)
        valid = True
        return valid
    except ValueError:
        valid = False
        return valid


def convert_to_number(string: str):
    if not is_valid_number(string):
        return

    number = float(string)
    if number.is_integer():
        return int(number)
    return number


def is_empty(string: str) -> bool:
    """
    Check if a given string is empty.
    Args:
        string (str): The string to check.
    Returns:
        bool: True if the string is empty, False otherwise.
    """
    return len(string) == 0


def formmat_result(result):
    if isinstance(result, int) or result.is_integer():
        return int(result)
    else:
        return round(result, 2)
