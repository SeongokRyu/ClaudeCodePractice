import {
  createItem,
  getItem,
  updateItem,
  deleteItem,
  listItems,
  clearItems,
} from "./app";

describe("Item Manager", () => {
  beforeEach(() => {
    clearItems();
  });

  describe("createItem", () => {
    it("should create an item with name and category", () => {
      const item = createItem("Widget", "hardware");

      expect(item.name).toBe("Widget");
      expect(item.category).toBe("hardware");
      expect(item.id).toBeDefined();
      expect(item.createdAt).toBeInstanceOf(Date);
      expect(item.updatedAt).toBeInstanceOf(Date);
    });

    it("should trim whitespace from inputs", () => {
      const item = createItem("  Widget  ", "  hardware  ");

      expect(item.name).toBe("Widget");
      expect(item.category).toBe("hardware");
    });

    it("should throw on empty name", () => {
      expect(() => createItem("", "hardware")).toThrow(
        "name is required and cannot be empty"
      );
    });

    it("should throw on empty category", () => {
      expect(() => createItem("Widget", "")).toThrow(
        "category is required and cannot be empty"
      );
    });

    it("should throw on name exceeding 200 characters", () => {
      const longName = "a".repeat(201);
      expect(() => createItem(longName, "hardware")).toThrow(
        "name cannot exceed 200 characters"
      );
    });
  });

  describe("getItem", () => {
    it("should return item by ID", () => {
      const created = createItem("Widget", "hardware");
      const found = getItem(created.id);
      expect(found).toEqual(created);
    });

    it("should return undefined for unknown ID", () => {
      expect(getItem("nonexistent")).toBeUndefined();
    });
  });

  describe("updateItem", () => {
    it("should update item name", () => {
      const item = createItem("Widget", "hardware");
      const updated = updateItem(item.id, { name: "Gadget" });
      expect(updated.name).toBe("Gadget");
    });

    it("should update item category", () => {
      const item = createItem("Widget", "hardware");
      const updated = updateItem(item.id, { category: "software" });
      expect(updated.category).toBe("software");
    });

    it("should throw for unknown ID", () => {
      expect(() => updateItem("unknown", { name: "X" })).toThrow(
        "Item not found: unknown"
      );
    });
  });

  describe("deleteItem", () => {
    it("should delete existing item", () => {
      const item = createItem("Widget", "hardware");
      expect(deleteItem(item.id)).toBe(true);
      expect(getItem(item.id)).toBeUndefined();
    });

    it("should return false for unknown ID", () => {
      expect(deleteItem("nonexistent")).toBe(false);
    });
  });

  describe("listItems", () => {
    it("should list all items", () => {
      createItem("Widget", "hardware");
      createItem("App", "software");
      expect(listItems()).toHaveLength(2);
    });

    it("should filter by category", () => {
      createItem("Widget", "hardware");
      createItem("App", "software");
      createItem("Gadget", "hardware");

      expect(listItems("hardware")).toHaveLength(2);
      expect(listItems("software")).toHaveLength(1);
    });

    it("should return empty array when no items match", () => {
      expect(listItems("nonexistent")).toHaveLength(0);
    });
  });
});
