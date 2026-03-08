# Skill: Coding Conventions

## Description
This skill defines the coding conventions for this project. Load this skill before implementing any new code.

## Naming Conventions
- **Variables & functions**: snake_case (`get_user_by_id`, `is_valid`)
- **Classes**: PascalCase (`UserProfile`, `AuthToken`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Files**: snake_case (`user_preferences.py`)
- **Test files**: `test_` prefix (`test_user_preferences.py`)

## File Structure
```python
"""Module docstring describing purpose."""

# 1. Standard library imports
import os
from datetime import datetime

# 2. Third-party imports
import requests

# 3. Local imports
from utils import local_util

# 4. Types and dataclasses
@dataclass
class MyType:
    field: str

# 5. Constants
MAX_ITEMS = 100

# 6. Main exports (functions/classes)
def my_function() -> None:
    """Docstring."""
    ...

# 7. Helper functions (private, prefixed with _)
def _helper_function() -> None:
    ...
```

## Error Handling
- Always raise `ValueError` or custom exceptions with descriptive messages
- Include the failing value in error messages: `raise ValueError(f"User not found: {user_id}")`
- Validate inputs at function boundaries
- Use early returns for guard clauses

## Python Rules
- **Type hints on all functions** -- parameters and return types
- **Use `dataclasses`** for structured data
- **Use `Optional[T]`** instead of `T | None` for compatibility
- **Prefer explicit imports** over wildcard imports

## Comments
- Docstrings on all public functions and classes
- Inline comments explain "why", not "what"
- No commented-out code

## Function Size
- Target: under 30 lines per function
- If a function is longer, extract helper functions
- Each function should do one thing well
