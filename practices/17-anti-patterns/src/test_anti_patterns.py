"""
Anti-Pattern Tests

These tests expose the hidden bugs in the anti-pattern code.
Learners should discover these AFTER experiencing the anti-patterns.
"""

from __future__ import annotations

import json
import math

import pytest

from anti_pattern_1_blind_trust import (
    deep_merge,
    safe_deep_merge,
    process_user_input,
    create_user_profile,
    safe_create_user_profile,
)
from anti_pattern_2_no_verification import (
    format_currency,
    format_total,
    format_discounted_price,
    safe_format_currency,
    safe_format_total,
)


class TestBlindTrustDangerousKeys:
    """Blind Trust - Dangerous key injection (Python equivalent of Prototype Pollution)"""

    def test_vulnerable_deep_merge_allows_dunder_keys_in_result(self) -> None:
        """deepMerge doesn't filter dangerous dunder keys."""
        malicious = {"__class__": {"overridden": True}, "name": "ok"}

        target = {"name": "safe"}
        result = deep_merge(target, malicious)

        # The vulnerable deep_merge does not reject the dangerous key
        assert "__class__" in result

    def test_vulnerable_process_user_input_merges_untrusted_json(self) -> None:
        """processUserInput merges untrusted JSON without sanitization."""
        existing = {"user": "alice", "role": "viewer"}
        malicious_input = json.dumps({
            "role": "admin",
            "__init__": {"compromised": True},
        })

        result = process_user_input(existing, malicious_input)

        # The role was overwritten - no validation of allowed fields
        assert result["role"] == "admin"
        # The __init__ key was accepted without filtering
        assert "__init__" in result

    def test_safe_deep_merge_blocks_dunder_keys(self) -> None:
        """safeDeepMerge blocks dangerous dunder keys."""
        malicious = {"__class__": {"overridden": True}, "name": "ok"}
        target = {"existing": "data"}

        result = safe_deep_merge(target, malicious)

        # __class__ key should be filtered out
        assert "__class__" not in result
        # Normal keys should still work
        assert result["name"] == "ok"
        assert result["existing"] == "data"

    def test_safe_deep_merge_blocks_init_key(self) -> None:
        """safeDeepMerge blocks __init__ key."""
        malicious = {"__init__": {"compromised": True}, "safe": "value"}
        target = {}

        result = safe_deep_merge(target, malicious)

        assert "__init__" not in result
        assert result["safe"] == "value"


class TestBlindTrustMutableDefaults:
    """Blind Trust - Mutable default argument (Python-specific anti-pattern)"""

    def test_vulnerable_mutable_default_shares_state(self) -> None:
        """Mutable default argument causes shared state between calls."""
        # Reset the default list by reloading (or call with fresh import)
        # This test demonstrates the bug: permissions accumulate across calls
        from anti_pattern_1_blind_trust import create_user_profile

        user1 = create_user_profile("Alice")
        user2 = create_user_profile("Bob")

        # BUG: user2's permissions contain "read" twice because the default
        # list is shared and mutated across calls
        assert len(user2["permissions"]) > 1  # Should be 1 but is 2+

    def test_safe_version_does_not_share_state(self) -> None:
        """Safe version creates independent permission lists."""
        user1 = safe_create_user_profile("Alice")
        user2 = safe_create_user_profile("Bob")

        assert user1["permissions"] == ["read"]
        assert user2["permissions"] == ["read"]
        assert user1["permissions"] is not user2["permissions"]


class TestNoVerificationFloatingPoint:
    """No Verification - Floating Point Issues"""

    class TestFormatCurrencyKnownRoundingIssues:
        def test_should_format_basic_numbers_correctly(self) -> None:
            assert format_currency(1234567.89) == "$1,234,567.89"
            assert format_currency(0) == "$0.00"
            assert format_currency(42) == "$42.00"

        def test_should_format_negative_numbers_with_parentheses(self) -> None:
            assert format_currency(-1234) == "($1,234.00)"
            assert format_currency(-0.50) == "($0.50)"

        def test_bug_rounding_issue_with_1_005(self) -> None:
            """
            Classic floating-point rounding bug.
            1.005 in IEEE 754 is actually 1.00499999999999989...
            So f"{1.005:.2f}" rounds DOWN to "1.00" instead of "1.01"
            """
            result = format_currency(1.005)
            # The buggy function produces "$1.00" instead of "$1.01"
            assert result == "$1.00"  # BUG! Should be "$1.01"

        def test_bug_rounding_issue_with_0_615(self) -> None:
            """Another classic case: 0.615 should round to 0.62 but gives 0.61"""
            result = format_currency(0.615)
            assert result == "$0.61"  # BUG! Should be "$0.62"

    class TestFormatTotalFloatingPointAccumulation:
        def test_bug_sum_of_0_1_0_2_0_3_should_be_0_60(self) -> None:
            amounts = [0.1, 0.2, 0.3]
            result = format_total(amounts)
            # 0.1 + 0.2 + 0.3 in floating point = 0.6000000000000001
            # f-string formatting happens to round this correctly to "0.60"
            # but the intermediate sum is wrong
            assert result == "$0.60"

        def test_bug_accumulation_error_with_many_small_values(self) -> None:
            """Adding 0.1 ten times should give 1.00"""
            amounts = [0.1] * 10
            # Due to floating-point accumulation:
            # sum of 0.1 * 10 in floating point != exactly 1.0
            internal_sum = 0.0
            for a in amounts:
                internal_sum += a
            assert internal_sum != 1.0  # The sum is NOT exactly 1.0!

    class TestFormatDiscountedPricePercentageArtifacts:
        def test_bug_10_percent_off_19_99(self) -> None:
            result = format_discounted_price(19.99, 10)
            # 19.99 * 0.1 = 1.9990000000000002 in floating point
            # 19.99 - 1.999... = 17.991000000000003
            # f"{:.2f}" -> "17.99" (happens to be correct due to rounding)
            assert result == "$17.99"

        def test_bug_33_33_percent_off_100(self) -> None:
            result = format_discounted_price(100, 33.33)
            # 100 * 0.3333 = 33.33
            # 100 - 33.33 = 66.67 (correct in this case)
            assert result == "$66.67"

    class TestSafeVersionsCorrectResults:
        def test_safe_format_currency_handles_1_005_correctly(self) -> None:
            result = safe_format_currency(1.005)
            assert result == "$1.01"  # Correct!

        def test_safe_format_currency_handles_0_615_correctly(self) -> None:
            result = safe_format_currency(0.615)
            assert result == "$0.62"  # Correct!

        def test_safe_format_total_handles_accumulated_values(self) -> None:
            amounts = [0.1] * 10
            result = safe_format_total(amounts)
            assert result == "$1.00"  # Correct!

        def test_safe_format_currency_handles_nan(self) -> None:
            assert safe_format_currency(float("nan")) == "$0.00"

        def test_safe_format_currency_handles_infinity(self) -> None:
            assert safe_format_currency(float("inf")) == "$0.00"
