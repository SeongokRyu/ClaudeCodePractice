import { add, subtract, multiply, divide, format } from './calculator';

describe('Calculator', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should add a positive and a negative number', () => {
      expect(add(5, -3)).toBe(2);
    });
  });

  describe('subtract', () => {
    it('should subtract two numbers', () => {
      expect(subtract(10, 4)).toBe(6);
    });
  });

  describe('multiply', () => {
    it('should multiply two numbers', () => {
      expect(multiply(3, 4)).toBe(12);
    });

    it('should return zero when multiplied by zero', () => {
      expect(multiply(5, 0)).toBe(0);
    });
  });

  describe('divide', () => {
    it('should divide two numbers', () => {
      expect(divide(10, 2)).toBe(5);
    });

    it('should handle decimal results', () => {
      expect(divide(7, 2)).toBe(3.5);
    });

    // NOTE: There is no test for division by zero!
    // The challenge is for the learner to discover this gap
    // and ask Claude to fix the bug + add tests.
  });

  describe('format', () => {
    it('should format a number with thousand separators', () => {
      expect(format(1234)).toBe('1,234');
    });

    it('should format a large number', () => {
      expect(format(1000000)).toBe('1,000,000');
    });

    it('should handle small numbers without separators', () => {
      expect(format(42)).toBe('42');
    });

    // NOTE: Missing tests for:
    // - Negative numbers
    // - Decimal numbers
    // - Zero
    // - Very large numbers
    // The challenge is for the learner to ask Claude to add these.
  });
});
