/**
 * Example application using environment variables for secrets.
 * This is the SAFE version — all secrets come from the environment.
 *
 * This pattern should PASS the pre-commit hook.
 */

interface Config {
  apiUrl: string;
  apiKey: string;
  dbHost: string;
  dbPassword: string;
  jwtSecret: string;
}

/**
 * Load configuration from environment variables.
 * Throws if required variables are missing.
 */
function loadConfig(): Config {
  const required = [
    'API_URL',
    'API_KEY',
    'DB_HOST',
    'DB_PASSWORD',
    'JWT_SECRET',
  ];

  const missing = required.filter(key => !process.env[key]);
  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missing.join(', ')}\n` +
      'Copy .env.example to .env and fill in the values.'
    );
  }

  return {
    apiUrl: process.env.API_URL!,
    apiKey: process.env.API_KEY!,
    dbHost: process.env.DB_HOST!,
    dbPassword: process.env.DB_PASSWORD!,
    jwtSecret: process.env.JWT_SECRET!,
  };
}

export class ApiClient {
  private config: Config;

  constructor() {
    this.config = loadConfig();
  }

  async fetchData(endpoint: string): Promise<any> {
    const response = await fetch(`${this.config.apiUrl}/${endpoint}`, {
      headers: {
        Authorization: `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return response.json();
  }

  async connectDatabase(): Promise<void> {
    // Use connection string from environment — no secrets in code
    console.log(`Connecting to ${this.config.dbHost}...`);
    // Actual connection logic would go here
  }
}

export function generateToken(userId: string): string {
  const config = loadConfig();
  // In real code, use jsonwebtoken package with config.jwtSecret
  const payload = JSON.stringify({ userId, exp: Date.now() + 3600000 });
  return Buffer.from(payload).toString('base64');
}

// .env.example template (commit this, NOT .env)
const ENV_EXAMPLE = `
# API Configuration
API_URL=https://api.example.com/v1
API_KEY=your-api-key-here

# Database
DB_HOST=localhost
DB_PASSWORD=your-db-password-here

# Authentication
JWT_SECRET=your-jwt-secret-here
`.trim();
