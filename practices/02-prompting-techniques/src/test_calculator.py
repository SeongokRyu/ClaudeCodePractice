from calculator import add, subtract, multiply, divide, format_number


class TestAdd:
    def test_should_add_two_positive_numbers(self):
        assert add(2, 3) == 5

    def test_should_add_a_positive_and_a_negative_number(self):
        assert add(5, -3) == 2


class TestSubtract:
    def test_should_subtract_two_numbers(self):
        assert subtract(10, 4) == 6


class TestMultiply:
    def test_should_multiply_two_numbers(self):
        assert multiply(3, 4) == 12

    def test_should_return_zero_when_multiplied_by_zero(self):
        assert multiply(5, 0) == 0


class TestDivide:
    def test_should_divide_two_numbers(self):
        assert divide(10, 2) == 5

    def test_should_handle_decimal_results(self):
        assert divide(7, 2) == 3.5

    # NOTE: There is no test for division by zero!
    # The challenge is for the learner to discover this gap
    # and ask Claude to fix the bug + add tests.


class TestFormatNumber:
    def test_should_format_a_number_with_thousand_separators(self):
        assert format_number(1234) == "1,234"

    def test_should_format_a_large_number(self):
        assert format_number(1000000) == "1,000,000"

    def test_should_handle_small_numbers_without_separators(self):
        assert format_number(42) == "42"

    # NOTE: Missing tests for:
    # - Negative numbers
    # - Decimal numbers
    # - Zero
    # - Very large numbers
    # The challenge is for the learner to ask Claude to add these.
