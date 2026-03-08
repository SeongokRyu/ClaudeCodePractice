// Simple REST-like module for subagent practice
// This module provides a basic API structure that agents can work with

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface ApiRequest {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  body?: Record<string, any>;
  headers?: Record<string, string>;
}

export interface ApiResponse {
  status: number;
  body: any;
  headers?: Record<string, string>;
}

// In-memory store
const users: Map<string, User> = new Map();

function generateId(): string {
  return `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

// Route handler
export function handleRequest(request: ApiRequest): ApiResponse {
  const { method, path } = request;

  // GET /users
  if (method === 'GET' && path === '/users') {
    return {
      status: 200,
      body: Array.from(users.values()),
    };
  }

  // GET /users/:id
  const getUserMatch = path.match(/^\/users\/([^/]+)$/);
  if (method === 'GET' && getUserMatch) {
    const userId = getUserMatch[1];
    const user = users.get(userId);
    if (!user) {
      return { status: 404, body: { error: 'User not found' } };
    }
    return { status: 200, body: user };
  }

  // POST /users
  if (method === 'POST' && path === '/users') {
    if (!request.body || !request.body.name || !request.body.email) {
      return { status: 400, body: { error: 'Name and email are required' } };
    }

    const newUser: User = {
      id: generateId(),
      name: request.body.name,
      email: request.body.email,
    };

    users.set(newUser.id, newUser);
    return { status: 201, body: newUser };
  }

  // PUT /users/:id
  const putUserMatch = path.match(/^\/users\/([^/]+)$/);
  if (method === 'PUT' && putUserMatch) {
    const userId = putUserMatch[1];
    const existing = users.get(userId);
    if (!existing) {
      return { status: 404, body: { error: 'User not found' } };
    }

    const updated: User = {
      ...existing,
      name: request.body?.name ?? existing.name,
      email: request.body?.email ?? existing.email,
    };

    users.set(userId, updated);
    return { status: 200, body: updated };
  }

  // DELETE /users/:id
  const deleteUserMatch = path.match(/^\/users\/([^/]+)$/);
  if (method === 'DELETE' && deleteUserMatch) {
    const userId = deleteUserMatch[1];
    if (!users.has(userId)) {
      return { status: 404, body: { error: 'User not found' } };
    }

    users.delete(userId);
    return { status: 204, body: null };
  }

  return { status: 404, body: { error: 'Route not found' } };
}

// Helper to reset state (useful for testing)
export function resetStore(): void {
  users.clear();
}
