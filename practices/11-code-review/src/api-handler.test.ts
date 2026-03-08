import {
  searchUsers,
  getUserById,
  createUser,
  deleteUser,
  processRequest,
} from './api-handler';

describe('API Handler', () => {
  // Note: These tests pass but intentionally do NOT cover security cases.
  // Part of the exercise is recognizing what's missing from the test suite.

  describe('searchUsers', () => {
    it('should find users by name', () => {
      const result = searchUsers('Alice');
      expect(result.success).toBe(true);
      expect(result.data).toHaveLength(1);
      expect(result.data[0].name).toBe('Alice');
    });

    it('should return empty array for no matches', () => {
      const result = searchUsers('NonExistent');
      expect(result.success).toBe(true);
      expect(result.data).toHaveLength(0);
    });

    it('should be case-insensitive', () => {
      const result = searchUsers('alice');
      expect(result.success).toBe(true);
      expect(result.data).toHaveLength(1);
    });
  });

  describe('getUserById', () => {
    it('should return user by ID', () => {
      const result = getUserById(1);
      expect(result.success).toBe(true);
      expect(result.data.name).toBe('Alice');
    });

    it('should return error for non-existent user', () => {
      const result = getUserById(999);
      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
    });
  });

  describe('createUser', () => {
    it('should create a new user', () => {
      const result = createUser('Dave', 'dave@example.com');
      expect(result.success).toBe(true);
      expect(result.data.name).toBe('Dave');
      expect(result.data.email).toBe('dave@example.com');
    });
  });

  describe('processRequest', () => {
    it('should route to correct handler', () => {
      const result = processRequest('search', { query: 'Bob' });
      expect(result.success).toBe(true);
    });

    it('should handle unknown actions', () => {
      const result = processRequest('unknown', {});
      expect(result.success).toBe(false);
    });
  });
});
