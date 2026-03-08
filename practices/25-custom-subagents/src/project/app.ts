/**
 * Sample Application — Task Manager
 *
 * A simple task management module for subagents to analyze,
 * extend, and review.
 */

import { generateId, formatDate, validateInput } from "./utils";

export interface Task {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in-progress" | "done";
  priority: "low" | "medium" | "high";
  createdAt: Date;
  updatedAt: Date;
  assignee?: string;
}

export class TaskManager {
  private tasks: Map<string, Task> = new Map();

  /**
   * Create a new task.
   */
  createTask(
    title: string,
    description: string,
    priority: Task["priority"] = "medium"
  ): Task {
    validateInput(title, "title");
    validateInput(description, "description");

    const now = new Date();
    const task: Task = {
      id: generateId(),
      title: title.trim(),
      description: description.trim(),
      status: "todo",
      priority,
      createdAt: now,
      updatedAt: now,
    };

    this.tasks.set(task.id, task);
    return task;
  }

  /**
   * Get a task by ID.
   */
  getTask(id: string): Task | undefined {
    return this.tasks.get(id);
  }

  /**
   * Update a task's status.
   */
  updateStatus(id: string, status: Task["status"]): Task {
    const task = this.tasks.get(id);
    if (!task) {
      throw new Error(`Task not found: ${id}`);
    }

    task.status = status;
    task.updatedAt = new Date();
    return task;
  }

  /**
   * Assign a task to someone.
   */
  assignTask(id: string, assignee: string): Task {
    const task = this.tasks.get(id);
    if (!task) {
      throw new Error(`Task not found: ${id}`);
    }

    validateInput(assignee, "assignee");
    task.assignee = assignee.trim();
    task.updatedAt = new Date();
    return task;
  }

  /**
   * List all tasks, optionally filtered by status.
   */
  listTasks(status?: Task["status"]): Task[] {
    const allTasks = Array.from(this.tasks.values());
    if (status) {
      return allTasks.filter((t) => t.status === status);
    }
    return allTasks;
  }

  /**
   * Delete a task.
   */
  deleteTask(id: string): boolean {
    return this.tasks.delete(id);
  }

  /**
   * Get a summary of task counts by status.
   */
  getSummary(): Record<Task["status"], number> {
    const summary: Record<Task["status"], number> = {
      todo: 0,
      "in-progress": 0,
      done: 0,
    };

    for (const task of this.tasks.values()) {
      summary[task.status]++;
    }

    return summary;
  }

  /**
   * Format a task for display.
   */
  formatTask(task: Task): string {
    const assigneeStr = task.assignee ? ` (@${task.assignee})` : "";
    return `[${task.status}] ${task.title}${assigneeStr} (${formatDate(task.createdAt)})`;
  }
}
