import pytest

from string_utils import capitalize, slugify, truncate, reverse


class TestCapitalize:
    def test_should_capitalize_the_first_letter(self):
        assert capitalize("hello") == "Hello"

    def test_should_handle_empty_string(self):
        assert capitalize("") == ""

    def test_should_handle_already_capitalized_string(self):
        assert capitalize("Hello") == "Hello"

    def test_should_handle_single_character(self):
        assert capitalize("a") == "A"


class TestSlugify:
    def test_should_convert_to_lowercase_and_replace_spaces_with_hyphens(self):
        assert slugify("Hello World") == "hello-world"

    def test_should_remove_special_characters(self):
        assert slugify("This is a Test!") == "this-is-a-test"

    def test_should_handle_multiple_spaces(self):
        assert slugify("hello   world") == "hello-world"

    def test_should_handle_leading_and_trailing_spaces(self):
        assert slugify("  hello world  ") == "hello-world"

    def test_should_handle_empty_string(self):
        assert slugify("") == ""


class TestTruncate:
    def test_should_truncate_long_strings_with_ellipsis(self):
        assert truncate("Hello World", 8) == "Hello..."

    def test_should_not_truncate_short_strings(self):
        assert truncate("Hi", 10) == "Hi"

    def test_should_handle_exact_length(self):
        assert truncate("Hello", 5) == "Hello"

    def test_should_handle_max_length_of_3(self):
        assert truncate("Hello", 3) == "..."

    def test_should_handle_max_length_of_0(self):
        assert truncate("Hello", 0) == ""

    def test_should_raise_on_negative_max_length(self):
        with pytest.raises(ValueError, match="max_length must be non-negative"):
            truncate("Hello", -1)


class TestReverse:
    def test_should_reverse_a_string(self):
        assert reverse("hello") == "olleh"

    def test_should_handle_empty_string(self):
        assert reverse("") == ""

    def test_should_handle_single_character(self):
        assert reverse("a") == "a"

    def test_should_handle_palindrome(self):
        assert reverse("racecar") == "racecar"
