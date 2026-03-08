import { ConfigParser } from './config-parser';

describe('ConfigParser', () => {
  let parser: ConfigParser;

  beforeEach(() => {
    parser = new ConfigParser();
  });

  describe('parse', () => {
    it('should parse number values correctly', () => {
      const config = parser.parse({
        maxRetries: '5',
        timeout: '10000',
      });
      expect(config.maxRetries).toBe(5);
      expect(config.timeout).toBe(10000);
    });

    it('should parse string values correctly', () => {
      const config = parser.parse({
        apiUrl: 'https://api.production.com',
      });
      expect(config.apiUrl).toBe('https://api.production.com');
    });

    it('should use defaults for missing values', () => {
      const config = parser.parse({});
      expect(config.maxRetries).toBe(3);
      expect(config.timeout).toBe(5000);
      expect(config.apiUrl).toBe('http://localhost:3000');
    });

    // This test FAILS due to the Boolean("false") === true bug
    it('should parse "false" string as boolean false', () => {
      const config = parser.parse({
        debug: 'false',
        verbose: 'false',
      });
      // BUG: Boolean("false") returns true because "false" is a non-empty string
      expect(config.debug).toBe(false);
      expect(config.verbose).toBe(false);
    });

    it('should parse "true" string as boolean true', () => {
      const config = parser.parse({
        debug: 'true',
        verbose: 'true',
      });
      expect(config.debug).toBe(true);
      expect(config.verbose).toBe(true);
    });

    // This test FAILS due to the same bug in nested features
    it('should handle feature flags correctly', () => {
      const config = parser.parse({
        enableCache: 'false',
        enableLogging: 'true',
        enableMetrics: 'false',
      });
      expect(config.features.enableCache).toBe(false);
      expect(config.features.enableLogging).toBe(true);
      expect(config.features.enableMetrics).toBe(false);
    });

    it('should throw for invalid number values', () => {
      expect(() => {
        parser.parse({ maxRetries: 'not-a-number' });
      }).toThrow('Invalid number');
    });
  });

  describe('parseFromString', () => {
    it('should parse key=value format', () => {
      const configString = `
debug=true
maxRetries=5
apiUrl=https://api.example.com
      `;
      const config = parser.parseFromString(configString);
      expect(config.debug).toBe(true);
      expect(config.maxRetries).toBe(5);
      expect(config.apiUrl).toBe('https://api.example.com');
    });

    it('should skip comments and empty lines', () => {
      const configString = `
# This is a comment
debug=true

# Another comment
maxRetries=5
      `;
      const config = parser.parseFromString(configString);
      expect(config.debug).toBe(true);
      expect(config.maxRetries).toBe(5);
    });

    it('should throw for invalid format', () => {
      expect(() => {
        parser.parseFromString('invalidline');
      }).toThrow('Invalid config line');
    });
  });
});
