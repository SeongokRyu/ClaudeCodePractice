/**
 * String utility functions.
 * Simple and easy to modify — designed for practicing Git workflows.
 */

/**
 * Capitalizes the first letter of a string.
 *
 * @param str - The input string
 * @returns The string with the first letter capitalized
 *
 * @example
 * capitalize('hello') // 'Hello'
 * capitalize('') // ''
 */
export function capitalize(str: string): string {
  if (str.length === 0) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Converts a string to a URL-friendly slug.
 * Lowercases the string, replaces spaces with hyphens,
 * and removes non-alphanumeric characters (except hyphens).
 *
 * @param str - The input string
 * @returns The slugified string
 *
 * @example
 * slugify('Hello World') // 'hello-world'
 * slugify('This is a Test!') // 'this-is-a-test'
 */
export function slugify(str: string): string {
  return str
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^a-z0-9-]/g, '')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

/**
 * Truncates a string to a specified length, adding an ellipsis if truncated.
 *
 * @param str - The input string
 * @param maxLength - The maximum length (including the ellipsis)
 * @returns The truncated string
 *
 * @example
 * truncate('Hello World', 8) // 'Hello...'
 * truncate('Hi', 10) // 'Hi'
 */
export function truncate(str: string, maxLength: number): string {
  if (maxLength < 0) {
    throw new Error('maxLength must be non-negative');
  }

  if (str.length <= maxLength) {
    return str;
  }

  if (maxLength <= 3) {
    return '...'.slice(0, maxLength);
  }

  return str.slice(0, maxLength - 3) + '...';
}

/**
 * Reverses a string.
 *
 * @param str - The input string
 * @returns The reversed string
 *
 * @example
 * reverse('hello') // 'olleh'
 * reverse('abc') // 'cba'
 */
export function reverse(str: string): string {
  return str.split('').reverse().join('');
}
