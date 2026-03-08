/**
 * Basic calculator module.
 * Note: This module has intentional bugs and missing edge cases
 * for practice purposes.
 */

export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}

/**
 * Divides a by b.
 * BUG: Does not handle division by zero properly.
 * It returns Infinity instead of throwing an error.
 */
export function divide(a: number, b: number): number {
  return a / b;
}

/**
 * Formats a number with thousand separators.
 * Examples:
 *   format(1234) => "1,234"
 *   format(1000000) => "1,000,000"
 *
 * Edge cases not handled:
 *   - Negative numbers may not format correctly
 *   - Decimal numbers may produce unexpected results
 *   - Very large numbers
 */
export function format(n: number): string {
  const str = String(n);
  const parts = str.split('.');
  const intPart = parts[0];
  const decPart = parts.length > 1 ? '.' + parts[1] : '';

  // Simple regex-based formatting — has issues with negative numbers
  const formatted = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

  return formatted + decPart;
}
