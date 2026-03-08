/**
 * Module A: User Service
 * Legacy module using callback patterns — for migration exercise.
 */

import { EventEmitter } from 'events';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

type Callback<T> = (error: Error | null, result?: T) => void;

// Simulated database
const users: Map<string, User> = new Map();

/**
 * Find a user by ID.
 * Uses callback pattern (should be migrated to async/await).
 */
export function findUserById(id: string, callback: Callback<User>): void {
  setTimeout(() => {
    const user = users.get(id);
    if (user) {
      callback(null, user);
    } else {
      callback(new Error(`User not found: ${id}`));
    }
  }, 100);
}

/**
 * Create a new user.
 * Uses callback pattern (should be migrated to async/await).
 */
export function createUser(
  name: string,
  email: string,
  callback: Callback<User>
): void {
  setTimeout(() => {
    // Validate email
    if (!email.includes('@')) {
      callback(new Error('Invalid email address'));
      return;
    }

    // Check for duplicate email
    for (const user of users.values()) {
      if (user.email === email) {
        callback(new Error(`Email already exists: ${email}`));
        return;
      }
    }

    const user: User = {
      id: `user-${Date.now()}`,
      name,
      email,
      role: 'user',
    };

    users.set(user.id, user);
    callback(null, user);
  }, 150);
}

/**
 * Update user role.
 * Uses callback pattern with nested callbacks (callback hell).
 */
export function updateUserRole(
  userId: string,
  newRole: User['role'],
  adminId: string,
  callback: Callback<User>
): void {
  // First verify the admin exists
  findUserById(adminId, (err, admin) => {
    if (err) {
      callback(new Error(`Admin verification failed: ${err.message}`));
      return;
    }

    // Then verify the admin has the right role
    if (admin!.role !== 'admin') {
      callback(new Error('Only admins can change roles'));
      return;
    }

    // Then find the target user
    findUserById(userId, (err2, user) => {
      if (err2) {
        callback(err2);
        return;
      }

      // Finally update the role
      user!.role = newRole;
      users.set(user!.id, user!);
      callback(null, user);
    });
  });
}

/**
 * Delete a user with confirmation.
 * Uses callback with event emitter pattern.
 */
export function deleteUser(
  userId: string,
  callback: Callback<boolean>
): EventEmitter {
  const emitter = new EventEmitter();

  findUserById(userId, (err, user) => {
    if (err) {
      callback(err);
      return;
    }

    emitter.emit('confirm', user);

    // Simulate deletion after confirmation
    emitter.on('confirmed', () => {
      users.delete(userId);
      callback(null, true);
    });

    emitter.on('cancelled', () => {
      callback(null, false);
    });
  });

  return emitter;
}

/**
 * List users with pagination.
 * Uses callback pattern (should be migrated to async/await).
 */
export function listUsers(
  page: number,
  pageSize: number,
  callback: Callback<{ users: User[]; total: number }>
): void {
  setTimeout(() => {
    const allUsers = Array.from(users.values());
    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    const pageUsers = allUsers.slice(start, end);

    callback(null, {
      users: pageUsers,
      total: allUsers.length,
    });
  }, 50);
}
