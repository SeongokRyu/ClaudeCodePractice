import { UserService } from './user-service';
import { User } from './types';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  describe('createUser', () => {
    it('should create a user with generated id and timestamps', () => {
      const user = service.createUser({
        name: 'Alice',
        email: 'alice@example.com',
      });

      expect(user.id).toBe('1');
      expect(user.name).toBe('Alice');
      expect(user.email).toBe('alice@example.com');
      expect(user.createdAt).toBeInstanceOf(Date);
      expect(user.updatedAt).toBeInstanceOf(Date);
    });

    it('should assign incrementing IDs', () => {
      const user1 = service.createUser({ name: 'Alice', email: 'alice@example.com' });
      const user2 = service.createUser({ name: 'Bob', email: 'bob@example.com' });

      expect(user1.id).toBe('1');
      expect(user2.id).toBe('2');
    });
  });

  describe('getUser', () => {
    it('should return a user by ID', () => {
      const created = service.createUser({ name: 'Alice', email: 'alice@example.com' });
      const found = service.getUser(created.id);

      expect(found).not.toBeNull();
      expect(found!.name).toBe('Alice');
    });

    it('should return null for non-existent user', () => {
      const found = service.getUser('999');
      expect(found).toBeNull();
    });
  });

  describe('updateUser', () => {
    it('should update user fields', () => {
      const created = service.createUser({ name: 'Alice', email: 'alice@example.com' });
      const updated = service.updateUser(created.id, { name: 'Alice Updated' });

      expect(updated.name).toBe('Alice Updated');
      expect(updated.email).toBe('alice@example.com');
    });

    it('should update the updatedAt timestamp', () => {
      const created = service.createUser({ name: 'Alice', email: 'alice@example.com' });
      const originalUpdatedAt = created.updatedAt;

      // Small delay to ensure different timestamp
      const updated = service.updateUser(created.id, { name: 'Alice Updated' });
      expect(updated.updatedAt.getTime()).toBeGreaterThanOrEqual(originalUpdatedAt.getTime());
    });

    it('should throw an error when user not found', () => {
      expect(() => {
        service.updateUser('999', { name: 'Ghost' });
      }).toThrow('User with id "999" not found');
    });
  });

  describe('deleteUser', () => {
    it('should delete an existing user', () => {
      const created = service.createUser({ name: 'Alice', email: 'alice@example.com' });
      const result = service.deleteUser(created.id);

      expect(result).toBe(true);
      expect(service.getUser(created.id)).toBeNull();
    });

    it('should return false when deleting non-existent user', () => {
      const result = service.deleteUser('999');
      expect(result).toBe(false);
    });
  });

  describe('listUsers', () => {
    it('should return empty array when no users exist', () => {
      expect(service.listUsers()).toEqual([]);
    });

    it('should return all users', () => {
      service.createUser({ name: 'Alice', email: 'alice@example.com' });
      service.createUser({ name: 'Bob', email: 'bob@example.com' });

      const users = service.listUsers();
      expect(users).toHaveLength(2);
    });
  });

  describe('count', () => {
    it('should return 0 when no users exist', () => {
      expect(service.count()).toBe(0);
    });

    it('should return the correct count', () => {
      service.createUser({ name: 'Alice', email: 'alice@example.com' });
      service.createUser({ name: 'Bob', email: 'bob@example.com' });

      expect(service.count()).toBe(2);
    });
  });

  describe('clear', () => {
    it('should remove all users', () => {
      service.createUser({ name: 'Alice', email: 'alice@example.com' });
      service.createUser({ name: 'Bob', email: 'bob@example.com' });

      service.clear();

      expect(service.count()).toBe(0);
      expect(service.listUsers()).toEqual([]);
    });

    it('should reset ID counter', () => {
      service.createUser({ name: 'Alice', email: 'alice@example.com' });
      service.clear();

      const user = service.createUser({ name: 'Bob', email: 'bob@example.com' });
      expect(user.id).toBe('1');
    });
  });
});
