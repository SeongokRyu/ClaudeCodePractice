"""
Deep Merge Utility

This function looks correct and handles nested dicts well.
However, it contains a subtle security vulnerability:
it doesn't guard against overwriting dunder attributes or
merging untrusted keys that could alter class behavior.

In Python, the equivalent of JS prototype pollution manifests as:
- Mutating class-level __dict__ or __class__ attributes
- Accepting arbitrary keys from untrusted input without validation
- Mutable default arguments leading to shared state
"""

from __future__ import annotations

from typing import Any


NestedDict = dict[str, Any]


def deep_merge(target: NestedDict, source: NestedDict) -> NestedDict:
    """
    Deep merges two dicts together.
    Properties from source override those in target.

    WARNING: This implementation is INTENTIONALLY VULNERABLE
    for educational purposes. It does not filter dangerous keys
    like __class__, __dict__, __init__, etc.
    """
    result: NestedDict = {**target}

    for key in source:
        source_val = source[key]
        target_val = result.get(key)

        # This looks reasonable - recursively merge nested dicts
        if (
            isinstance(source_val, dict)
            and isinstance(target_val, dict)
        ):
            result[key] = deep_merge(target_val, source_val)
        else:
            # BUG: No check for dangerous keys like "__class__", "__dict__",
            # "__init__", "__module__", etc.
            # This allows injection of arbitrary attributes!
            result[key] = source_val

    return result


def apply_config(
    defaults: NestedDict,
    user_config: NestedDict,
) -> NestedDict:
    """
    Applies user-provided configuration on top of defaults.
    Uses deep_merge internally - inherits the vulnerability.
    """
    return deep_merge(defaults, user_config)


def process_user_input(
    existing_data: NestedDict,
    user_input: str,
) -> NestedDict:
    """
    Processes user input and merges it with existing data.
    In a real app, this might process API request bodies.
    """
    import json

    try:
        parsed = json.loads(user_input)
        return deep_merge(existing_data, parsed)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON input")


# --- Mutable default argument vulnerability (Python-specific) ---

def create_user_profile(
    name: str,
    permissions: list[str] = [],  # BUG: Mutable default argument!
) -> dict[str, Any]:
    """
    WARNING: INTENTIONALLY VULNERABLE - mutable default argument.

    All calls that don't pass permissions will SHARE the same list.
    Adding to one user's permissions modifies the default for all future calls.
    """
    permissions.append("read")  # This modifies the shared default list!
    return {"name": name, "permissions": permissions}


# --- Safe version (for comparison after the exercise) ---

DANGEROUS_KEYS = frozenset({
    "__class__", "__dict__", "__init__", "__module__",
    "__setattr__", "__getattr__", "__delattr__",
    "__slots__", "__bases__", "__subclasses__",
})


def safe_deep_merge(target: NestedDict, source: NestedDict) -> NestedDict:
    """
    Safe deep merge that prevents dangerous key injection.
    This is the CORRECT way to implement deep merge.
    """
    result: NestedDict = {**target}

    for key in source:
        # Guard against dangerous key injection
        if key in DANGEROUS_KEYS:
            continue

        # Additional check: skip dunder attributes
        if key.startswith("__") and key.endswith("__"):
            continue

        source_val = source[key]
        target_val = result.get(key)

        if isinstance(source_val, dict) and isinstance(target_val, dict):
            result[key] = safe_deep_merge(target_val, source_val)
        else:
            result[key] = source_val

    return result


def safe_create_user_profile(
    name: str,
    permissions: list[str] | None = None,
) -> dict[str, Any]:
    """
    Safe version - uses None as default and creates a new list each time.
    """
    if permissions is None:
        permissions = []
    permissions = permissions.copy()  # Don't mutate the caller's list
    permissions.append("read")
    return {"name": name, "permissions": permissions}
