import { User, CreateUserInput, UpdateUserInput } from './types';

/**
 * In-memory user service with CRUD operations.
 *
 * This service uses a Map to store users in memory.
 * It provides create, read, update, delete operations
 * along with listing and searching capabilities.
 */
export class UserService {
  private users: Map<string, User> = new Map();
  private nextId: number = 1;

  /**
   * Creates a new user.
   * Generates a unique ID and timestamps automatically.
   */
  createUser(input: CreateUserInput): User {
    const id = String(this.nextId++);
    const now = new Date();

    const user: User = {
      id,
      name: input.name,
      email: input.email,
      createdAt: now,
      updatedAt: now,
    };

    this.users.set(id, user);
    return user;
  }

  /**
   * Retrieves a user by ID.
   * Returns null if the user is not found.
   */
  getUser(id: string): User | null {
    return this.users.get(id) ?? null;
  }

  /**
   * Updates an existing user.
   * Only the provided fields in the input will be updated.
   * Throws an error if the user is not found.
   */
  updateUser(id: string, input: UpdateUserInput): User {
    const user = this.users.get(id);
    if (!user) {
      throw new Error(`User with id "${id}" not found`);
    }

    const updatedUser: User = {
      ...user,
      ...input,
      updatedAt: new Date(),
    };

    this.users.set(id, updatedUser);
    return updatedUser;
  }

  /**
   * Deletes a user by ID.
   * Returns true if the user was deleted, false if not found.
   */
  deleteUser(id: string): boolean {
    return this.users.delete(id);
  }

  /**
   * Returns all users as an array.
   */
  listUsers(): User[] {
    return Array.from(this.users.values());
  }

  /**
   * Returns the total number of users.
   */
  count(): number {
    return this.users.size;
  }

  /**
   * Clears all users from the store.
   * Useful for testing.
   */
  clear(): void {
    this.users.clear();
    this.nextId = 1;
  }
}
