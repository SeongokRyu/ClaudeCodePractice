"""
String utility functions.
Simple and easy to modify -- designed for practicing Git workflows.
"""

import re


def capitalize(s: str) -> str:
    """
    Capitalizes the first letter of a string.

    Args:
        s: The input string

    Returns:
        The string with the first letter capitalized

    Examples:
        >>> capitalize('hello')
        'Hello'
        >>> capitalize('')
        ''
    """
    if len(s) == 0:
        return ""
    return s[0].upper() + s[1:]


def slugify(s: str) -> str:
    """
    Converts a string to a URL-friendly slug.
    Lowercases the string, replaces spaces with hyphens,
    and removes non-alphanumeric characters (except hyphens).

    Args:
        s: The input string

    Returns:
        The slugified string

    Examples:
        >>> slugify('Hello World')
        'hello-world'
        >>> slugify('This is a Test!')
        'this-is-a-test'
    """
    result = s.lower().strip()
    result = re.sub(r"\s+", "-", result)
    result = re.sub(r"[^a-z0-9-]", "", result)
    result = re.sub(r"-+", "-", result)
    result = re.sub(r"^-|-$", "", result)
    return result


def truncate(s: str, max_length: int) -> str:
    """
    Truncates a string to a specified length, adding an ellipsis if truncated.

    Args:
        s: The input string
        max_length: The maximum length (including the ellipsis)

    Returns:
        The truncated string

    Examples:
        >>> truncate('Hello World', 8)
        'Hello...'
        >>> truncate('Hi', 10)
        'Hi'
    """
    if max_length < 0:
        raise ValueError("max_length must be non-negative")

    if len(s) <= max_length:
        return s

    if max_length <= 3:
        return "..."[:max_length]

    return s[: max_length - 3] + "..."


def reverse(s: str) -> str:
    """
    Reverses a string.

    Args:
        s: The input string

    Returns:
        The reversed string

    Examples:
        >>> reverse('hello')
        'olleh'
        >>> reverse('abc')
        'cba'
    """
    return s[::-1]
