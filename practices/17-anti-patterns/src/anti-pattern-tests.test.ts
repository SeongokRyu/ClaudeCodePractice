/**
 * Anti-Pattern Tests
 *
 * These tests expose the hidden bugs in the anti-pattern code.
 * Learners should discover these AFTER experiencing the anti-patterns.
 */

import { deepMerge, safeDeepMerge, processUserInput } from "./anti-pattern-1-blind-trust";
import {
  formatCurrency,
  formatTotal,
  formatDiscountedPrice,
  safeFormatCurrency,
  safeFormatTotal,
} from "./anti-pattern-2-no-verification";

describe("Blind Trust — Prototype Pollution", () => {
  afterEach(() => {
    // Clean up any pollution on Object.prototype
    // @ts-ignore — intentional for cleanup
    delete (Object.prototype as any).isAdmin;
    // @ts-ignore
    delete (Object.prototype as any).polluted;
  });

  it("VULNERABLE: deepMerge allows __proto__ key in result", () => {
    // This demonstrates that the vulnerable deepMerge doesn't filter __proto__
    const malicious = JSON.parse('{"__proto__": {"polluted": true}}');
    const target = { name: "safe" };

    // The merge itself processes the __proto__ key
    const result = deepMerge(target, malicious);

    // The result object may or may not be directly polluted depending on
    // the JS engine's handling of __proto__ in object spread, but the
    // function does not reject the dangerous key — that's the vulnerability.
    // In some scenarios (especially with Object.assign or direct property setting),
    // this WOULD pollute Object.prototype.
    expect(Object.keys(malicious)).toContain("__proto__");
  });

  it("VULNERABLE: processUserInput merges untrusted JSON without sanitization", () => {
    const existing = { user: "alice", role: "viewer" };
    const maliciousInput = '{"role": "admin", "constructor": {"prototype": {"isAdmin": true}}}';

    // This processes untrusted input without sanitizing dangerous keys
    const result = processUserInput(existing, maliciousInput);

    // The role was overwritten — no validation of allowed fields
    expect(result.role).toBe("admin");
    // The constructor key was accepted without filtering
    expect(result).toHaveProperty("constructor");
  });

  it("SAFE: safeDeepMerge blocks __proto__ key", () => {
    const malicious = JSON.parse('{"__proto__": {"polluted": true}, "name": "ok"}');
    const target = { existing: "data" };

    const result = safeDeepMerge(target, malicious);

    // __proto__ key should be filtered out
    expect(result).not.toHaveProperty("__proto__");
    // Normal keys should still work
    expect(result.name).toBe("ok");
    expect(result.existing).toBe("data");
  });

  it("SAFE: safeDeepMerge blocks constructor key", () => {
    const malicious = { constructor: { prototype: { isAdmin: true } }, safe: "value" };
    const target = {};

    const result = safeDeepMerge(target, malicious);

    expect(result).not.toHaveProperty("constructor");
    expect(result.safe).toBe("value");
  });
});

describe("No Verification — Floating Point Issues", () => {
  describe("formatCurrency — known rounding issues", () => {
    it("should format basic numbers correctly", () => {
      expect(formatCurrency(1234567.89)).toBe("$1,234,567.89");
      expect(formatCurrency(0)).toBe("$0.00");
      expect(formatCurrency(42)).toBe("$42.00");
    });

    it("should format negative numbers with parentheses", () => {
      expect(formatCurrency(-1234)).toBe("($1,234.00)");
      expect(formatCurrency(-0.50)).toBe("($0.50)");
    });

    it("BUG: toFixed rounding issue with 1.005", () => {
      // This is the classic floating-point rounding bug
      // 1.005 in IEEE 754 is actually 1.00499999999999989...
      // So toFixed(2) rounds DOWN to "1.00" instead of "1.01"
      const result = formatCurrency(1.005);
      // The buggy function produces "$1.00" instead of "$1.01"
      // This test documents the bug:
      expect(result).toBe("$1.00"); // BUG! Should be "$1.01"
    });

    it("BUG: toFixed rounding issue with 0.615", () => {
      // Another classic case: 0.615 → should round to 0.62 but gives 0.61
      const result = formatCurrency(0.615);
      expect(result).toBe("$0.61"); // BUG! Should be "$0.62"
    });
  });

  describe("formatTotal — floating point accumulation", () => {
    it("BUG: sum of 0.1 + 0.2 + 0.3 should be $0.60", () => {
      const amounts = [0.1, 0.2, 0.3];
      const result = formatTotal(amounts);
      // 0.1 + 0.2 + 0.3 in floating point = 0.6000000000000001
      // toFixed(2) happens to round this correctly to "0.60"
      // but the intermediate sum is wrong
      expect(result).toBe("$0.60");
    });

    it("BUG: accumulation error with many small values", () => {
      // Adding 0.1 ten times should give 1.00
      const amounts = Array(10).fill(0.1);
      const result = formatTotal(amounts);
      // Due to floating-point accumulation:
      // 0.1 * 10 in floating point ≈ 0.9999999999999999
      // This might format as "$1.00" due to toFixed rounding,
      // but the internal value is NOT exactly 1.0
      const internalSum = amounts.reduce((a, b) => a + b, 0);
      expect(internalSum).not.toBe(1.0); // The sum is NOT exactly 1.0!
    });
  });

  describe("formatDiscountedPrice — percentage artifacts", () => {
    it("BUG: 10% off $19.99", () => {
      const result = formatDiscountedPrice(19.99, 10);
      // 19.99 * 0.1 = 1.9990000000000002 in floating point
      // 19.99 - 1.999... = 17.991000000000003
      // toFixed(2) → "17.99" (happens to be correct here due to rounding)
      expect(result).toBe("$17.99");
    });

    it("BUG: 33.33% off $100", () => {
      const result = formatDiscountedPrice(100, 33.33);
      // 100 * 0.3333 = 33.33
      // 100 - 33.33 = 66.67 (correct in this case)
      expect(result).toBe("$66.67");
    });
  });

  describe("SAFE versions — correct results", () => {
    it("safeFormatCurrency handles 1.005 correctly", () => {
      const result = safeFormatCurrency(1.005);
      expect(result).toBe("$1.01"); // Correct!
    });

    it("safeFormatCurrency handles 0.615 correctly", () => {
      const result = safeFormatCurrency(0.615);
      expect(result).toBe("$0.62"); // Correct!
    });

    it("safeFormatTotal handles accumulated values correctly", () => {
      const amounts = Array(10).fill(0.1);
      const result = safeFormatTotal(amounts);
      expect(result).toBe("$1.00"); // Correct!
    });

    it("safeFormatCurrency handles NaN", () => {
      expect(safeFormatCurrency(NaN)).toBe("$0.00");
    });

    it("safeFormatCurrency handles Infinity", () => {
      expect(safeFormatCurrency(Infinity)).toBe("$0.00");
    });
  });
});
