"""Utility functions for the Task Manager application."""

import time
import random
import string
from datetime import date


def generate_id() -> str:
    """
    Generate a unique ID.
    Uses a simple timestamp + random suffix approach.
    """
    timestamp = int(time.time() * 1000)
    ts_part = format(timestamp, "x")  # base-16 for compactness
    random_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{ts_part}-{random_part}"


def format_date(d: date) -> str:
    """Format a date for display (YYYY-MM-DD)."""
    return d.isoformat()[:10]


def validate_input(value: str, field_name: str) -> None:
    """
    Validate that a string input is non-empty.
    Raises ValueError if validation fails.
    """
    if not value or not isinstance(value, str):
        raise ValueError(f"{field_name} is required and must be a string")

    if value.strip() == "":
        raise ValueError(f"{field_name} cannot be empty or whitespace only")

    if len(value) > 500:
        raise ValueError(f"{field_name} cannot exceed 500 characters")


def truncate(s: str, max_length: int) -> str:
    """Truncate a string to a maximum length with ellipsis."""
    if len(s) <= max_length:
        return s
    return s[: max_length - 3] + "..."


def deep_clone(obj: dict) -> dict:
    """
    Simple deep clone for plain dicts/lists.
    Note: Does not handle datetime objects, functions, etc.
    """
    import json

    return json.loads(json.dumps(obj, default=str))
