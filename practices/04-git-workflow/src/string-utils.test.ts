import { capitalize, slugify, truncate, reverse } from './string-utils';

describe('String Utils', () => {
  describe('capitalize', () => {
    it('should capitalize the first letter', () => {
      expect(capitalize('hello')).toBe('Hello');
    });

    it('should handle empty string', () => {
      expect(capitalize('')).toBe('');
    });

    it('should handle already capitalized string', () => {
      expect(capitalize('Hello')).toBe('Hello');
    });

    it('should handle single character', () => {
      expect(capitalize('a')).toBe('A');
    });
  });

  describe('slugify', () => {
    it('should convert to lowercase and replace spaces with hyphens', () => {
      expect(slugify('Hello World')).toBe('hello-world');
    });

    it('should remove special characters', () => {
      expect(slugify('This is a Test!')).toBe('this-is-a-test');
    });

    it('should handle multiple spaces', () => {
      expect(slugify('hello   world')).toBe('hello-world');
    });

    it('should handle leading and trailing spaces', () => {
      expect(slugify('  hello world  ')).toBe('hello-world');
    });

    it('should handle empty string', () => {
      expect(slugify('')).toBe('');
    });
  });

  describe('truncate', () => {
    it('should truncate long strings with ellipsis', () => {
      expect(truncate('Hello World', 8)).toBe('Hello...');
    });

    it('should not truncate short strings', () => {
      expect(truncate('Hi', 10)).toBe('Hi');
    });

    it('should handle exact length', () => {
      expect(truncate('Hello', 5)).toBe('Hello');
    });

    it('should handle maxLength of 3', () => {
      expect(truncate('Hello', 3)).toBe('...');
    });

    it('should handle maxLength of 0', () => {
      expect(truncate('Hello', 0)).toBe('');
    });

    it('should throw on negative maxLength', () => {
      expect(() => truncate('Hello', -1)).toThrow('maxLength must be non-negative');
    });
  });

  describe('reverse', () => {
    it('should reverse a string', () => {
      expect(reverse('hello')).toBe('olleh');
    });

    it('should handle empty string', () => {
      expect(reverse('')).toBe('');
    });

    it('should handle single character', () => {
      expect(reverse('a')).toBe('a');
    });

    it('should handle palindrome', () => {
      expect(reverse('racecar')).toBe('racecar');
    });
  });
});
