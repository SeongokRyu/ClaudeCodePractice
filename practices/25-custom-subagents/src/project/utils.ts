/**
 * Utility functions for the Task Manager application.
 */

/**
 * Generate a unique ID.
 * Uses a simple timestamp + random suffix approach.
 */
export function generateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `${timestamp}-${random}`;
}

/**
 * Format a date for display.
 */
export function formatDate(date: Date): string {
  return date.toISOString().split("T")[0];
}

/**
 * Validate that a string input is non-empty.
 * Throws an error if validation fails.
 */
export function validateInput(value: string, fieldName: string): void {
  if (!value || typeof value !== "string") {
    throw new Error(`${fieldName} is required and must be a string`);
  }

  if (value.trim().length === 0) {
    throw new Error(`${fieldName} cannot be empty or whitespace only`);
  }

  if (value.length > 500) {
    throw new Error(`${fieldName} cannot exceed 500 characters`);
  }
}

/**
 * Truncate a string to a maximum length with ellipsis.
 */
export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str;
  return str.substring(0, maxLength - 3) + "...";
}

/**
 * Simple deep clone for plain objects.
 * Note: Does not handle Date objects, functions, etc.
 */
export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}
