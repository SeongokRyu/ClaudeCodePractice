"""
Basic calculator module.
Note: This module has intentional bugs and missing edge cases
for practice purposes.
"""

import re


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    """
    Divides a by b.
    BUG: Does not handle division by zero properly.
    It returns float('inf') instead of raising an error.
    """
    return a / b if b != 0 else float("inf")


def format_number(n: float) -> str:
    """
    Formats a number with thousand separators.

    Examples:
        format_number(1234) => "1,234"
        format_number(1000000) => "1,000,000"

    Edge cases not handled:
        - Negative numbers may not format correctly
        - Decimal numbers may produce unexpected results
        - Very large numbers
    """
    s = str(n)
    parts = s.split(".")
    int_part = parts[0]
    dec_part = "." + parts[1] if len(parts) > 1 else ""

    # Simple regex-based formatting -- has issues with negative numbers
    formatted = re.sub(r"\B(?=(\d{3})+(?!\d))", ",", int_part)

    return formatted + dec_part
