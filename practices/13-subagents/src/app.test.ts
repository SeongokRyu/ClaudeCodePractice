import { handleRequest, resetStore, ApiRequest } from './app';

describe('API Handler', () => {
  beforeEach(() => {
    resetStore();
  });

  describe('POST /users', () => {
    it('should create a new user', () => {
      const request: ApiRequest = {
        method: 'POST',
        path: '/users',
        body: { name: 'Alice', email: 'alice@example.com' },
      };

      const response = handleRequest(request);
      expect(response.status).toBe(201);
      expect(response.body.name).toBe('Alice');
      expect(response.body.email).toBe('alice@example.com');
      expect(response.body.id).toBeDefined();
    });

    it('should return 400 for missing fields', () => {
      const request: ApiRequest = {
        method: 'POST',
        path: '/users',
        body: { name: 'Alice' },
      };

      const response = handleRequest(request);
      expect(response.status).toBe(400);
    });
  });

  describe('GET /users', () => {
    it('should return all users', () => {
      handleRequest({
        method: 'POST',
        path: '/users',
        body: { name: 'Alice', email: 'alice@example.com' },
      });
      handleRequest({
        method: 'POST',
        path: '/users',
        body: { name: 'Bob', email: 'bob@example.com' },
      });

      const response = handleRequest({
        method: 'GET',
        path: '/users',
      });

      expect(response.status).toBe(200);
      expect(response.body).toHaveLength(2);
    });

    it('should return empty array when no users', () => {
      const response = handleRequest({
        method: 'GET',
        path: '/users',
      });

      expect(response.status).toBe(200);
      expect(response.body).toHaveLength(0);
    });
  });

  describe('GET /users/:id', () => {
    it('should return a specific user', () => {
      const createResponse = handleRequest({
        method: 'POST',
        path: '/users',
        body: { name: 'Alice', email: 'alice@example.com' },
      });

      const userId = createResponse.body.id;
      const response = handleRequest({
        method: 'GET',
        path: `/users/${userId}`,
      });

      expect(response.status).toBe(200);
      expect(response.body.name).toBe('Alice');
    });

    it('should return 404 for non-existent user', () => {
      const response = handleRequest({
        method: 'GET',
        path: '/users/nonexistent',
      });

      expect(response.status).toBe(404);
    });
  });

  describe('PUT /users/:id', () => {
    it('should update a user', () => {
      const createResponse = handleRequest({
        method: 'POST',
        path: '/users',
        body: { name: 'Alice', email: 'alice@example.com' },
      });

      const userId = createResponse.body.id;
      const response = handleRequest({
        method: 'PUT',
        path: `/users/${userId}`,
        body: { name: 'Alice Updated' },
      });

      expect(response.status).toBe(200);
      expect(response.body.name).toBe('Alice Updated');
      expect(response.body.email).toBe('alice@example.com');
    });
  });

  describe('DELETE /users/:id', () => {
    it('should delete a user', () => {
      const createResponse = handleRequest({
        method: 'POST',
        path: '/users',
        body: { name: 'Alice', email: 'alice@example.com' },
      });

      const userId = createResponse.body.id;
      const deleteResponse = handleRequest({
        method: 'DELETE',
        path: `/users/${userId}`,
      });

      expect(deleteResponse.status).toBe(204);

      const getResponse = handleRequest({
        method: 'GET',
        path: `/users/${userId}`,
      });

      expect(getResponse.status).toBe(404);
    });

    it('should return 404 for non-existent user', () => {
      const response = handleRequest({
        method: 'DELETE',
        path: '/users/nonexistent',
      });

      expect(response.status).toBe(404);
    });
  });

  describe('Unknown routes', () => {
    it('should return 404 for unknown routes', () => {
      const response = handleRequest({
        method: 'GET',
        path: '/unknown',
      });

      expect(response.status).toBe(404);
    });
  });
});
