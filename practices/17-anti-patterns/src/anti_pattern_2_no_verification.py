"""
Currency Formatter

This function compiles and runs correctly for most inputs.
However, it has subtle floating-point issues that only
appear with specific values.

WARNING: This implementation is INTENTIONALLY BUGGY
for educational purposes.
"""

from __future__ import annotations

import math


def format_currency(amount: float) -> str:
    """
    Formats a number as a currency string.

    Examples:
        format_currency(1234567.89)  -> "$1,234,567.89"
        format_currency(-1234)       -> "($1,234.00)"
        format_currency(0)           -> "$0.00"
    """
    is_negative = amount < 0
    absolute_amount = abs(amount)

    # BUG 1: Using round() / format with floating-point numbers
    # This causes rounding errors for certain values
    # Example: round(1.005, 2) gives 1.0 instead of 1.01 in Python
    # because 1.005 in IEEE 754 is actually 1.00499999999999989...
    fixed = f"{absolute_amount:.2f}"

    integer_part, decimal_part = fixed.split(".")

    # Add comma separators
    with_commas = _add_commas(integer_part)

    formatted = f"${with_commas}.{decimal_part}"

    if is_negative:
        return f"({formatted})"

    return formatted


def _add_commas(num_str: str) -> str:
    """
    Adds comma separators to a number string.
    "1234567" -> "1,234,567"
    """
    # BUG 2: This approach works for normal numbers but fails for very large
    # numbers that exceed float precision
    parts: list[str] = []
    remaining = num_str

    while len(remaining) > 3:
        parts.insert(0, remaining[-3:])
        remaining = remaining[:-3]
    parts.insert(0, remaining)

    return ",".join(parts)


def format_total(amounts: list[float]) -> str:
    """
    Calculates the total and formats it.
    BUG 3: Accumulates floating-point errors when summing
    """
    # This naive summation accumulates floating-point errors
    total = 0.0
    for amount in amounts:
        total += amount
    return format_currency(total)


def format_discounted_price(price: float, discount_percent: float) -> str:
    """
    Calculates a percentage discount and formats the result.
    BUG 4: Percentage calculation can produce floating-point artifacts
    """
    discount = price * (discount_percent / 100)
    discounted_price = price - discount
    return format_currency(discounted_price)


# --- Safe version (for comparison after the exercise) ---


def safe_format_currency(amount: float) -> str:
    """
    Safe currency formatter that handles floating-point correctly.
    Uses Decimal for precise rounding, then integer arithmetic.
    """
    if not math.isfinite(amount):
        return "$0.00"

    from decimal import Decimal, ROUND_HALF_UP

    is_negative = amount < 0

    # Use Decimal for precise rounding to 2 decimal places
    # str() conversion preserves the intended value better than float arithmetic
    d = Decimal(str(abs(amount)))
    rounded = d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    cents = int(rounded * 100)
    dollars = cents // 100
    remaining_cents = cents % 100

    with_commas = _add_commas(str(dollars))
    decimal_part = str(remaining_cents).zfill(2)

    formatted = f"${with_commas}.{decimal_part}"

    if is_negative:
        return f"({formatted})"

    return formatted


def safe_format_total(amounts: list[float]) -> str:
    """
    Safe total formatter using Decimal arithmetic.
    """
    from decimal import Decimal, ROUND_HALF_UP

    # Sum using Decimal to avoid floating-point accumulation
    total = sum(Decimal(str(a)) for a in amounts)
    return safe_format_currency(float(total))
