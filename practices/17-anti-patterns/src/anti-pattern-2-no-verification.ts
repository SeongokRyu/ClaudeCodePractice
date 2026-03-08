/**
 * Currency Formatter
 *
 * This function compiles and runs correctly for most inputs.
 * However, it has subtle floating-point issues that only
 * appear with specific values.
 *
 * WARNING: This implementation is INTENTIONALLY BUGGY
 * for educational purposes.
 */

/**
 * Formats a number as a currency string.
 *
 * Examples:
 *   formatCurrency(1234567.89)  → "$1,234,567.89"
 *   formatCurrency(-1234)       → "($1,234.00)"
 *   formatCurrency(0)           → "$0.00"
 */
export function formatCurrency(amount: number): string {
  const isNegative = amount < 0;
  const absoluteAmount = Math.abs(amount);

  // BUG 1: Using toFixed(2) on floating-point numbers
  // This causes rounding errors for certain values
  // Example: (0.1 + 0.2).toFixed(2) might give unexpected results
  // More critically: 1.005.toFixed(2) gives "1.00" instead of "1.01"
  const fixed = absoluteAmount.toFixed(2);

  const [integerPart, decimalPart] = fixed.split(".");

  // Add comma separators
  const withCommas = addCommas(integerPart);

  const formatted = `$${withCommas}.${decimalPart}`;

  if (isNegative) {
    return `(${formatted})`;
  }

  return formatted;
}

/**
 * Adds comma separators to a number string.
 * "1234567" → "1,234,567"
 */
function addCommas(numStr: string): string {
  // BUG 2: This regex-based approach fails for very large numbers
  // that exceed Number.MAX_SAFE_INTEGER when originally passed as numbers
  const parts: string[] = [];
  let remaining = numStr;

  while (remaining.length > 3) {
    parts.unshift(remaining.slice(-3));
    remaining = remaining.slice(0, -3);
  }
  parts.unshift(remaining);

  return parts.join(",");
}

/**
 * Calculates the total and formats it.
 * BUG 3: Accumulates floating-point errors when summing
 */
export function formatTotal(amounts: number[]): string {
  // This naive summation accumulates floating-point errors
  let total = 0;
  for (const amount of amounts) {
    total += amount;
  }
  return formatCurrency(total);
}

/**
 * Calculates a percentage discount and formats the result.
 * BUG 4: Percentage calculation can produce floating-point artifacts
 */
export function formatDiscountedPrice(
  price: number,
  discountPercent: number
): string {
  const discount = price * (discountPercent / 100);
  const discountedPrice = price - discount;
  return formatCurrency(discountedPrice);
}

// --- Safe version (for comparison after the exercise) ---

/**
 * Safe currency formatter that handles floating-point correctly.
 * Uses integer arithmetic internally to avoid precision issues.
 */
export function safeFormatCurrency(amount: number): string {
  if (!Number.isFinite(amount)) {
    return "$0.00";
  }

  const isNegative = amount < 0;

  // Convert to cents (integer) to avoid floating-point issues
  const cents = Math.round(Math.abs(amount) * 100);
  const dollars = Math.floor(cents / 100);
  const remainingCents = cents % 100;

  const withCommas = addCommas(dollars.toString());
  const decimalPart = remainingCents.toString().padStart(2, "0");

  const formatted = `$${withCommas}.${decimalPart}`;

  if (isNegative) {
    return `(${formatted})`;
  }

  return formatted;
}

/**
 * Safe total formatter using integer arithmetic.
 */
export function safeFormatTotal(amounts: number[]): string {
  // Sum in cents to avoid floating-point accumulation
  const totalCents = amounts.reduce(
    (sum, amount) => sum + Math.round(amount * 100),
    0
  );
  return safeFormatCurrency(totalCents / 100);
}
