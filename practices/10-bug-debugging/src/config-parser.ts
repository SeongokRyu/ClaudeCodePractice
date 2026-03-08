export interface AppConfig {
  debug: boolean;
  verbose: boolean;
  maxRetries: number;
  timeout: number;
  apiUrl: string;
  features: {
    enableCache: boolean;
    enableLogging: boolean;
    enableMetrics: boolean;
  };
}

type RawConfig = Record<string, string>;

export class ConfigParser {
  // BUG: parseBoolean uses truthy check, which means "false" string becomes true
  // because "false" is a non-empty string and thus truthy
  private parseBoolean(value: string): boolean {
    return Boolean(value);  // BUG: Boolean("false") === true
  }

  private parseNumber(value: string): number {
    const num = Number(value);
    if (isNaN(num)) {
      throw new Error(`Invalid number: ${value}`);
    }
    return num;
  }

  parse(raw: RawConfig): AppConfig {
    return {
      debug: this.parseBoolean(raw['debug'] ?? 'false'),
      verbose: this.parseBoolean(raw['verbose'] ?? 'false'),
      maxRetries: this.parseNumber(raw['maxRetries'] ?? '3'),
      timeout: this.parseNumber(raw['timeout'] ?? '5000'),
      apiUrl: raw['apiUrl'] ?? 'http://localhost:3000',
      features: {
        enableCache: this.parseBoolean(raw['enableCache'] ?? 'true'),
        enableLogging: this.parseBoolean(raw['enableLogging'] ?? 'true'),
        enableMetrics: this.parseBoolean(raw['enableMetrics'] ?? 'false'),
      },
    };
  }

  // Parse from environment-like key=value format
  parseFromString(configString: string): AppConfig {
    const raw: RawConfig = {};
    const lines = configString.split('\n');

    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed === '' || trimmed.startsWith('#')) {
        continue;
      }
      const eqIndex = trimmed.indexOf('=');
      if (eqIndex === -1) {
        throw new Error(`Invalid config line: ${trimmed}`);
      }
      const key = trimmed.substring(0, eqIndex).trim();
      const value = trimmed.substring(eqIndex + 1).trim();
      raw[key] = value;
    }

    return this.parse(raw);
  }
}
