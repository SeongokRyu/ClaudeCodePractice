/**
 * Shared types for the authentication module.
 */

export interface User {
  id: string;
  email: string;
  passwordHash: string;
  createdAt: Date;
}

export interface AuthToken {
  token: string;
  userId: string;
  expiresAt: Date;
}

export interface LoginResult {
  success: boolean;
  token?: string;
  error?: string;
}

export interface TokenValidation {
  valid: boolean;
  userId?: string;
  error?: string;
}
