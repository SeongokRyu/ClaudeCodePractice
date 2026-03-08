import { Callback } from './types';

// In-memory database simulation using callbacks
const store: Map<string, Map<string, any>> = new Map();

export function initCollection(collectionName: string, callback: Callback<void>): void {
  setTimeout(() => {
    store.set(collectionName, new Map());
    callback(null);
  }, 10);
}

export function insert(
  collectionName: string,
  id: string,
  data: any,
  callback: Callback<any>
): void {
  setTimeout(() => {
    const collection = store.get(collectionName);
    if (!collection) {
      callback(new Error(`Collection '${collectionName}' does not exist`));
      return;
    }
    if (collection.has(id)) {
      callback(new Error(`Document with id '${id}' already exists`));
      return;
    }
    collection.set(id, { ...data });
    callback(null, { ...data });
  }, 10);
}

export function findById(
  collectionName: string,
  id: string,
  callback: Callback<any>
): void {
  setTimeout(() => {
    const collection = store.get(collectionName);
    if (!collection) {
      callback(new Error(`Collection '${collectionName}' does not exist`));
      return;
    }
    const doc = collection.get(id);
    if (!doc) {
      callback(new Error(`Document with id '${id}' not found`));
      return;
    }
    callback(null, { ...doc });
  }, 10);
}

export function findAll(
  collectionName: string,
  callback: Callback<any[]>
): void {
  setTimeout(() => {
    const collection = store.get(collectionName);
    if (!collection) {
      callback(new Error(`Collection '${collectionName}' does not exist`));
      return;
    }
    const docs = Array.from(collection.values()).map((doc) => ({ ...doc }));
    callback(null, docs);
  }, 10);
}

export function update(
  collectionName: string,
  id: string,
  data: Partial<any>,
  callback: Callback<any>
): void {
  setTimeout(() => {
    const collection = store.get(collectionName);
    if (!collection) {
      callback(new Error(`Collection '${collectionName}' does not exist`));
      return;
    }
    const existing = collection.get(id);
    if (!existing) {
      callback(new Error(`Document with id '${id}' not found`));
      return;
    }
    const updated = { ...existing, ...data };
    collection.set(id, updated);
    callback(null, { ...updated });
  }, 10);
}

export function remove(
  collectionName: string,
  id: string,
  callback: Callback<void>
): void {
  setTimeout(() => {
    const collection = store.get(collectionName);
    if (!collection) {
      callback(new Error(`Collection '${collectionName}' does not exist`));
      return;
    }
    if (!collection.has(id)) {
      callback(new Error(`Document with id '${id}' not found`));
      return;
    }
    collection.delete(id);
    callback(null);
  }, 10);
}

export function clearAll(callback: Callback<void>): void {
  setTimeout(() => {
    store.clear();
    callback(null);
  }, 10);
}
