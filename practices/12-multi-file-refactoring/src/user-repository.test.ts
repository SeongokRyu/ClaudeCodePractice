import * as db from './database';
import * as userRepo from './user-repository';

describe('UserRepository', () => {
  beforeEach((done) => {
    db.clearAll(() => {
      userRepo.initUserRepo((error) => {
        if (error) return done(error);
        done();
      });
    });
  });

  describe('createUser', () => {
    it('should create a user with generated ID', (done) => {
      userRepo.createUser('Alice', 'alice@example.com', (error, user) => {
        expect(error).toBeNull();
        expect(user).toBeDefined();
        expect(user!.name).toBe('Alice');
        expect(user!.email).toBe('alice@example.com');
        expect(user!.id).toBeDefined();
        expect(user!.createdAt).toBeDefined();
        done();
      });
    });
  });

  describe('getUserById', () => {
    it('should retrieve a user by ID', (done) => {
      userRepo.createUser('Alice', 'alice@example.com', (error, user) => {
        expect(error).toBeNull();
        userRepo.getUserById(user!.id, (error2, found) => {
          expect(error2).toBeNull();
          expect(found!.name).toBe('Alice');
          done();
        });
      });
    });

    it('should return error for non-existent user', (done) => {
      userRepo.getUserById('nonexistent', (error) => {
        expect(error).not.toBeNull();
        done();
      });
    });
  });

  describe('getAllUsers', () => {
    it('should return all users', (done) => {
      userRepo.createUser('Alice', 'alice@example.com', () => {
        userRepo.createUser('Bob', 'bob@example.com', () => {
          userRepo.getAllUsers((error, users) => {
            expect(error).toBeNull();
            expect(users).toHaveLength(2);
            done();
          });
        });
      });
    });
  });

  describe('updateUser', () => {
    it('should update user data', (done) => {
      userRepo.createUser('Alice', 'alice@example.com', (error, user) => {
        expect(error).toBeNull();
        userRepo.updateUser(
          user!.id,
          { name: 'Alice Updated' },
          (error2, updated) => {
            expect(error2).toBeNull();
            expect(updated!.name).toBe('Alice Updated');
            expect(updated!.email).toBe('alice@example.com');
            done();
          }
        );
      });
    });
  });

  describe('deleteUser', () => {
    it('should delete a user', (done) => {
      userRepo.createUser('Alice', 'alice@example.com', (error, user) => {
        expect(error).toBeNull();
        userRepo.deleteUser(user!.id, (error2) => {
          expect(error2).toBeNull();
          userRepo.getUserById(user!.id, (error3) => {
            expect(error3).not.toBeNull();
            done();
          });
        });
      });
    });
  });
});
