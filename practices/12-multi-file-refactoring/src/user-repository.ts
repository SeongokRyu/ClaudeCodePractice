import { User, Callback } from './types';
import * as db from './database';

const COLLECTION = 'users';

export function initUserRepo(callback: Callback<void>): void {
  db.initCollection(COLLECTION, callback);
}

export function createUser(
  name: string,
  email: string,
  callback: Callback<User>
): void {
  const user: User = {
    id: `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    name,
    email,
    createdAt: new Date(),
  };

  db.insert(COLLECTION, user.id, user, (error, result) => {
    if (error) {
      callback(error);
      return;
    }
    callback(null, result as User);
  });
}

export function getUserById(
  userId: string,
  callback: Callback<User>
): void {
  db.findById(COLLECTION, userId, (error, result) => {
    if (error) {
      callback(error);
      return;
    }
    callback(null, result as User);
  });
}

export function getAllUsers(callback: Callback<User[]>): void {
  db.findAll(COLLECTION, (error, result) => {
    if (error) {
      callback(error);
      return;
    }
    callback(null, result as User[]);
  });
}

export function updateUser(
  userId: string,
  data: Partial<Omit<User, 'id' | 'createdAt'>>,
  callback: Callback<User>
): void {
  db.update(COLLECTION, userId, data, (error, result) => {
    if (error) {
      callback(error);
      return;
    }
    callback(null, result as User);
  });
}

export function deleteUser(userId: string, callback: Callback<void>): void {
  db.remove(COLLECTION, userId, (error) => {
    if (error) {
      callback(error);
      return;
    }
    callback(null);
  });
}
