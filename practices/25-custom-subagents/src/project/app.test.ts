import { TaskManager, Task } from "./app";

describe("TaskManager", () => {
  let manager: TaskManager;

  beforeEach(() => {
    manager = new TaskManager();
  });

  describe("createTask", () => {
    it("should create a task with default priority", () => {
      const task = manager.createTask("Test task", "A test description");

      expect(task.title).toBe("Test task");
      expect(task.description).toBe("A test description");
      expect(task.status).toBe("todo");
      expect(task.priority).toBe("medium");
      expect(task.id).toBeDefined();
      expect(task.createdAt).toBeInstanceOf(Date);
    });

    it("should create a task with specified priority", () => {
      const task = manager.createTask("Urgent", "Fix now", "high");
      expect(task.priority).toBe("high");
    });

    it("should trim whitespace from title and description", () => {
      const task = manager.createTask("  padded title  ", "  padded desc  ");
      expect(task.title).toBe("padded title");
      expect(task.description).toBe("padded desc");
    });

    it("should throw on empty title", () => {
      expect(() => manager.createTask("", "desc")).toThrow(
        "title cannot be empty"
      );
    });

    it("should throw on empty description", () => {
      expect(() => manager.createTask("title", "")).toThrow(
        "description cannot be empty"
      );
    });
  });

  describe("getTask", () => {
    it("should return a task by ID", () => {
      const created = manager.createTask("Find me", "desc");
      const found = manager.getTask(created.id);
      expect(found).toEqual(created);
    });

    it("should return undefined for unknown ID", () => {
      expect(manager.getTask("nonexistent")).toBeUndefined();
    });
  });

  describe("updateStatus", () => {
    it("should update task status", () => {
      const task = manager.createTask("Status test", "desc");
      const updated = manager.updateStatus(task.id, "in-progress");
      expect(updated.status).toBe("in-progress");
    });

    it("should update the updatedAt timestamp", () => {
      const task = manager.createTask("Timestamp test", "desc");
      const originalUpdatedAt = task.updatedAt;

      // Small delay to ensure different timestamp
      const updated = manager.updateStatus(task.id, "done");
      expect(updated.updatedAt.getTime()).toBeGreaterThanOrEqual(
        originalUpdatedAt.getTime()
      );
    });

    it("should throw for unknown task ID", () => {
      expect(() => manager.updateStatus("unknown", "done")).toThrow(
        "Task not found"
      );
    });
  });

  describe("assignTask", () => {
    it("should assign a task to someone", () => {
      const task = manager.createTask("Assign test", "desc");
      const assigned = manager.assignTask(task.id, "alice");
      expect(assigned.assignee).toBe("alice");
    });

    it("should throw for empty assignee", () => {
      const task = manager.createTask("Assign test", "desc");
      expect(() => manager.assignTask(task.id, "")).toThrow();
    });
  });

  describe("listTasks", () => {
    it("should list all tasks", () => {
      manager.createTask("Task 1", "desc");
      manager.createTask("Task 2", "desc");
      expect(manager.listTasks()).toHaveLength(2);
    });

    it("should filter by status", () => {
      const task1 = manager.createTask("Task 1", "desc");
      manager.createTask("Task 2", "desc");
      manager.updateStatus(task1.id, "done");

      expect(manager.listTasks("done")).toHaveLength(1);
      expect(manager.listTasks("todo")).toHaveLength(1);
    });

    it("should return empty array when no tasks match", () => {
      expect(manager.listTasks("in-progress")).toHaveLength(0);
    });
  });

  describe("deleteTask", () => {
    it("should delete an existing task", () => {
      const task = manager.createTask("Delete me", "desc");
      expect(manager.deleteTask(task.id)).toBe(true);
      expect(manager.getTask(task.id)).toBeUndefined();
    });

    it("should return false for unknown task", () => {
      expect(manager.deleteTask("nonexistent")).toBe(false);
    });
  });

  describe("getSummary", () => {
    it("should return correct counts", () => {
      const t1 = manager.createTask("T1", "d");
      const t2 = manager.createTask("T2", "d");
      manager.createTask("T3", "d");
      manager.updateStatus(t1.id, "in-progress");
      manager.updateStatus(t2.id, "done");

      expect(manager.getSummary()).toEqual({
        todo: 1,
        "in-progress": 1,
        done: 1,
      });
    });
  });
});
