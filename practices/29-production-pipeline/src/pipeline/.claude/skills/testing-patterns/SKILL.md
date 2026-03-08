# Skill: Testing Patterns

## Description
This skill defines how to write tests in this project. Load this skill before writing any test code.

## Framework
- **pytest** for testing
- Test files live next to source files: `module.py` -> `test_module.py`

## Test Structure

```python
"""Tests for module_name."""

import pytest
from module import function_under_test


class TestFunctionName:
    """Tests grouped by function or behavior."""

    def test_happy_path(self) -> None:
        """Should do X when given valid input."""
        result = function_under_test("valid")
        assert result == expected

    def test_error_case(self) -> None:
        """Should raise when given empty string."""
        with pytest.raises(ValueError, match="descriptive message"):
            function_under_test("")

    def test_edge_case(self) -> None:
        """Should handle very long input."""
        long_input = "a" * 10000
        result = function_under_test(long_input)
        assert result is not None
```

## What to Test

### Always Test
1. **Happy path**: Normal, expected usage
2. **Error cases**: Invalid input, missing data, network failures
3. **Edge cases**: Empty strings, zero, None, very large inputs
4. **Boundary conditions**: Off-by-one, max values, min values

### Test Categories per Function
- At least 1 happy path test
- At least 1 error/raise test
- At least 1 edge case test
- Total: minimum 3 tests per public function

## Assertions
```python
# Equality
assert value == expected
assert value != other

# Truthiness
assert value is True
assert value is None
assert value is not None

# Comparisons
assert value > 3
assert value <= 10

# Strings
assert "substring" in value
import re
assert re.match(r"pattern", value)

# Collections
assert len(array) == 3
assert item in array

# Errors
with pytest.raises(ValueError):
    fn()
with pytest.raises(ValueError, match="message"):
    fn()
```

## Fixtures
```python
import pytest

@pytest.fixture
def instance():
    """Create a fresh instance for each test."""
    obj = MyClass()
    yield obj
    obj.cleanup()

@pytest.fixture(autouse=True)
def reset_state():
    """Reset state before each test."""
    clear_items()
```

## Avoid
- Tests that depend on execution order
- Tests that depend on external state (network, filesystem)
- Tests that only check `is not None` (test actual behavior)
- Flaky tests with timeouts or race conditions
- Testing implementation details (private methods)
