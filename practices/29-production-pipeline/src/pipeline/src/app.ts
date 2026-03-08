/**
 * Main Application Module — Item Manager
 *
 * A simple item management module that serves as the baseline
 * for the production pipeline to extend with new features.
 */

export interface Item {
  id: string;
  name: string;
  category: string;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * In-memory item store.
 */
const items: Map<string, Item> = new Map();

/**
 * Generate a unique ID.
 */
function generateId(): string {
  return `${Date.now().toString(36)}-${Math.random().toString(36).substring(2, 8)}`;
}

/**
 * Validate that a string is non-empty.
 */
function validateString(value: string, fieldName: string): void {
  if (!value || typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`${fieldName} is required and cannot be empty`);
  }
  if (value.length > 200) {
    throw new Error(`${fieldName} cannot exceed 200 characters`);
  }
}

/**
 * Create a new item.
 */
export function createItem(name: string, category: string): Item {
  validateString(name, "name");
  validateString(category, "category");

  const now = new Date();
  const item: Item = {
    id: generateId(),
    name: name.trim(),
    category: category.trim(),
    createdAt: now,
    updatedAt: now,
  };

  items.set(item.id, item);
  return item;
}

/**
 * Get an item by ID.
 */
export function getItem(id: string): Item | undefined {
  return items.get(id);
}

/**
 * Update an item's name or category.
 */
export function updateItem(
  id: string,
  updates: { name?: string; category?: string }
): Item {
  const item = items.get(id);
  if (!item) {
    throw new Error(`Item not found: ${id}`);
  }

  if (updates.name !== undefined) {
    validateString(updates.name, "name");
    item.name = updates.name.trim();
  }

  if (updates.category !== undefined) {
    validateString(updates.category, "category");
    item.category = updates.category.trim();
  }

  item.updatedAt = new Date();
  return item;
}

/**
 * Delete an item by ID.
 */
export function deleteItem(id: string): boolean {
  return items.delete(id);
}

/**
 * List all items, optionally filtered by category.
 */
export function listItems(category?: string): Item[] {
  const allItems = Array.from(items.values());
  if (category) {
    return allItems.filter((item) => item.category === category);
  }
  return allItems;
}

/**
 * Clear all items (useful for testing).
 */
export function clearItems(): void {
  items.clear();
}
