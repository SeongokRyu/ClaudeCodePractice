/**
 * Example application WITH hardcoded secrets.
 * THIS FILE IS INTENTIONALLY INSECURE — for testing the pre-commit hook.
 *
 * DO NOT use this pattern in real code!
 */

// WARNING: Hardcoded API keys (this should be caught by the pre-commit hook)
const API_KEY = "sk-proj-abc123def456ghi789jkl012mno345pqr678";
const DATABASE_PASSWORD = "SuperSecret123!@#";
const AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE";
const AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

// Private key embedded in code (critical security issue)
const PRIVATE_KEY = `-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF0PbnGcY5unA67hqxnfZoEapMPBP
nLmkMzKMkMjK8EXAMPLE_NOT_REAL_KEY_DATA_HERE
-----END RSA PRIVATE KEY-----`;

interface Config {
  apiUrl: string;
  apiKey: string;
  dbHost: string;
  dbPassword: string;
}

// Hardcoded configuration (should use environment variables)
const config: Config = {
  apiUrl: "https://api.example.com/v1",
  apiKey: API_KEY,
  dbHost: "db.production.internal",
  dbPassword: DATABASE_PASSWORD,
};

export class ApiClient {
  private config: Config;

  constructor() {
    this.config = config;
  }

  async fetchData(endpoint: string): Promise<any> {
    const response = await fetch(`${this.config.apiUrl}/${endpoint}`, {
      headers: {
        Authorization: `Bearer ${this.config.apiKey}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return response.json();
  }

  async connectDatabase(): Promise<void> {
    // Simulated database connection with hardcoded credentials
    console.log(`Connecting to ${this.config.dbHost} with password ${this.config.dbPassword}`);
  }
}

// JWT secret hardcoded
const JWT_SECRET = "my-super-secret-jwt-key-do-not-share";

export function generateToken(userId: string): string {
  // Simplified — in real code, use jsonwebtoken package
  const payload = JSON.stringify({ userId, exp: Date.now() + 3600000 });
  return Buffer.from(payload).toString("base64");
}
