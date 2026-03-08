"""Tests for the Item Manager module."""

import pytest
from datetime import datetime

from app import (
    create_item,
    get_item,
    update_item,
    delete_item,
    list_items,
    clear_items,
)


@pytest.fixture(autouse=True)
def setup() -> None:
    """Clear items before each test."""
    clear_items()


class TestCreateItem:
    def test_create_with_name_and_category(self) -> None:
        item = create_item("Widget", "hardware")
        assert item.name == "Widget"
        assert item.category == "hardware"
        assert item.id is not None
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)

    def test_trim_whitespace(self) -> None:
        item = create_item("  Widget  ", "  hardware  ")
        assert item.name == "Widget"
        assert item.category == "hardware"

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError, match="name is required and cannot be empty"):
            create_item("", "hardware")

    def test_empty_category_raises(self) -> None:
        with pytest.raises(ValueError, match="category is required and cannot be empty"):
            create_item("Widget", "")

    def test_name_exceeding_200_chars_raises(self) -> None:
        long_name = "a" * 201
        with pytest.raises(ValueError, match="name cannot exceed 200 characters"):
            create_item(long_name, "hardware")


class TestGetItem:
    def test_return_item_by_id(self) -> None:
        created = create_item("Widget", "hardware")
        found = get_item(created.id)
        assert found == created

    def test_return_none_for_unknown_id(self) -> None:
        assert get_item("nonexistent") is None


class TestUpdateItem:
    def test_update_name(self) -> None:
        item = create_item("Widget", "hardware")
        updated = update_item(item.id, name="Gadget")
        assert updated.name == "Gadget"

    def test_update_category(self) -> None:
        item = create_item("Widget", "hardware")
        updated = update_item(item.id, category="software")
        assert updated.category == "software"

    def test_unknown_id_raises(self) -> None:
        with pytest.raises(ValueError, match="Item not found: unknown"):
            update_item("unknown", name="X")


class TestDeleteItem:
    def test_delete_existing(self) -> None:
        item = create_item("Widget", "hardware")
        assert delete_item(item.id) is True
        assert get_item(item.id) is None

    def test_delete_nonexistent(self) -> None:
        assert delete_item("nonexistent") is False


class TestListItems:
    def test_list_all(self) -> None:
        create_item("Widget", "hardware")
        create_item("App", "software")
        assert len(list_items()) == 2

    def test_filter_by_category(self) -> None:
        create_item("Widget", "hardware")
        create_item("App", "software")
        create_item("Gadget", "hardware")
        assert len(list_items("hardware")) == 2
        assert len(list_items("software")) == 1

    def test_empty_when_no_match(self) -> None:
        assert len(list_items("nonexistent")) == 0
