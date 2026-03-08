"""
Main Application Module -- Item Manager

A simple item management module that serves as the baseline
for the production pipeline to extend with new features.
"""

import time
import random
import string
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Item:
    id: str
    name: str
    category: str
    created_at: datetime
    updated_at: datetime


# In-memory item store
_items: dict[str, Item] = {}


def _generate_id() -> str:
    """Generate a unique ID."""
    ts_part = format(int(time.time() * 1000), "x")
    random_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{ts_part}-{random_part}"


def _validate_string(value: str, field_name: str) -> None:
    """Validate that a string is non-empty."""
    if not value or not isinstance(value, str) or value.strip() == "":
        raise ValueError(f"{field_name} is required and cannot be empty")
    if len(value) > 200:
        raise ValueError(f"{field_name} cannot exceed 200 characters")


def create_item(name: str, category: str) -> Item:
    """Create a new item."""
    _validate_string(name, "name")
    _validate_string(category, "category")

    now = datetime.now()
    item = Item(
        id=_generate_id(),
        name=name.strip(),
        category=category.strip(),
        created_at=now,
        updated_at=now,
    )
    _items[item.id] = item
    return item


def get_item(item_id: str) -> Optional[Item]:
    """Get an item by ID."""
    return _items.get(item_id)


def update_item(
    item_id: str,
    name: Optional[str] = None,
    category: Optional[str] = None,
) -> Item:
    """Update an item's name or category."""
    item = _items.get(item_id)
    if item is None:
        raise ValueError(f"Item not found: {item_id}")

    if name is not None:
        _validate_string(name, "name")
        item.name = name.strip()

    if category is not None:
        _validate_string(category, "category")
        item.category = category.strip()

    item.updated_at = datetime.now()
    return item


def delete_item(item_id: str) -> bool:
    """Delete an item by ID."""
    if item_id in _items:
        del _items[item_id]
        return True
    return False


def list_items(category: Optional[str] = None) -> list[Item]:
    """List all items, optionally filtered by category."""
    all_items = list(_items.values())
    if category:
        return [item for item in all_items if item.category == category]
    return all_items


def clear_items() -> None:
    """Clear all items (useful for testing)."""
    _items.clear()
