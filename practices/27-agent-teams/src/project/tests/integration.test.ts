/**
 * Integration Tests — Starter File
 *
 * Tests that verify the full-stack flow works correctly.
 * Agent Teams should expand these tests significantly.
 */

import { getDashboard, getTasks, createTask } from "../backend/src/server";

describe("Integration Tests", () => {
  describe("Dashboard API", () => {
    it("should return dashboard data with task counts", () => {
      const dashboard = getDashboard();

      expect(dashboard.tasks).toBeDefined();
      expect(dashboard.totalCount).toBeGreaterThan(0);
      expect(dashboard.completedCount).toBeDefined();
      expect(dashboard.completedCount).toBeLessThanOrEqual(
        dashboard.totalCount
      );
    });

    it("should include all task fields in dashboard response", () => {
      const dashboard = getDashboard();
      const task = dashboard.tasks[0];

      expect(task.id).toBeDefined();
      expect(task.title).toBeDefined();
      expect(task.status).toBeDefined();
      expect(["todo", "in-progress", "done"]).toContain(task.status);
    });
  });

  describe("Tasks API", () => {
    it("should return all tasks", () => {
      const tasks = getTasks();
      expect(tasks.length).toBeGreaterThan(0);
    });

    it("should filter tasks by status", () => {
      const doneTasks = getTasks("done");
      doneTasks.forEach((task) => {
        expect(task.status).toBe("done");
      });
    });

    it("should create a new task", () => {
      const task = createTask("Test task", "Test description", "tester");

      expect(task.id).toBeDefined();
      expect(task.title).toBe("Test task");
      expect(task.status).toBe("todo");
      expect(task.assignee).toBe("tester");
    });
  });
});
