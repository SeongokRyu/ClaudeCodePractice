/**
 * Simple Task Manager Application
 * Used as sample code for headless mode practice scripts.
 */

// TODO: Add task priority levels (high, medium, low)
// TODO: Implement task categories/tags
// FIXME: Task ID generation could collide in concurrent scenarios

export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  // TODO: Add dueDate field
  // TODO: Add assignee field
}

export class TaskManager {
  private tasks: Map<string, Task> = new Map();
  private nextId = 1;

  // TODO: Accept initial tasks in constructor
  constructor() {}

  /**
   * Generate a unique task ID.
   * FIXME: This is not safe for concurrent use — consider UUID
   */
  private generateId(): string {
    return `task-${this.nextId++}`;
  }

  /**
   * Create a new task.
   */
  createTask(title: string, description: string = ''): Task {
    if (!title || title.trim().length === 0) {
      throw new Error('Task title cannot be empty');
    }

    const now = new Date();
    const task: Task = {
      id: this.generateId(),
      title: title.trim(),
      description: description.trim(),
      completed: false,
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
   * Get all tasks.
   * TODO: Add filtering options (by status, date range, etc.)
   */
  getAllTasks(): Task[] {
    return Array.from(this.tasks.values());
  }

  /**
   * Update a task's title and/or description.
   * TODO: Support partial updates with a patch object
   */
  updateTask(id: string, title?: string, description?: string): Task {
    const task = this.tasks.get(id);
    if (!task) {
      throw new Error(`Task not found: ${id}`);
    }

    if (title !== undefined) {
      if (title.trim().length === 0) {
        throw new Error('Task title cannot be empty');
      }
      task.title = title.trim();
    }

    if (description !== undefined) {
      task.description = description.trim();
    }

    task.updatedAt = new Date();
    return task;
  }

  /**
   * Mark a task as completed.
   */
  completeTask(id: string): Task {
    const task = this.tasks.get(id);
    if (!task) {
      throw new Error(`Task not found: ${id}`);
    }

    task.completed = true;
    task.updatedAt = new Date();
    return task;
  }

  /**
   * Delete a task.
   * TODO: Add soft delete option
   */
  deleteTask(id: string): boolean {
    if (!this.tasks.has(id)) {
      throw new Error(`Task not found: ${id}`);
    }
    return this.tasks.delete(id);
  }

  /**
   * Get task statistics.
   * FIXME: This recalculates every time — consider caching
   */
  getStats(): { total: number; completed: number; pending: number } {
    const tasks = this.getAllTasks();
    const completed = tasks.filter(t => t.completed).length;
    return {
      total: tasks.length,
      completed,
      pending: tasks.length - completed,
    };
  }

  /**
   * Search tasks by title.
   * TODO: Add full-text search across title and description
   * TODO: Add regex search support
   */
  searchTasks(query: string): Task[] {
    const lowerQuery = query.toLowerCase();
    return this.getAllTasks().filter(task =>
      task.title.toLowerCase().includes(lowerQuery)
    );
  }

  /**
   * Export tasks to JSON string.
   */
  exportToJson(): string {
    return JSON.stringify(this.getAllTasks(), null, 2);
  }

  /**
   * Import tasks from JSON string.
   * TODO: Add validation for imported data
   * FIXME: This doesn't handle duplicate IDs
   */
  importFromJson(json: string): number {
    const tasks: Task[] = JSON.parse(json);
    let imported = 0;

    for (const task of tasks) {
      if (task.id && task.title) {
        this.tasks.set(task.id, {
          ...task,
          createdAt: new Date(task.createdAt),
          updatedAt: new Date(task.updatedAt),
        });
        imported++;
      }
    }

    return imported;
  }
}

// Main entry point for CLI usage
if (require.main === module) {
  const manager = new TaskManager();

  // Demo usage
  const task1 = manager.createTask('Set up CI/CD pipeline', 'Configure GitHub Actions');
  const task2 = manager.createTask('Write unit tests', 'Cover all edge cases');
  const task3 = manager.createTask('Review PR #42', 'Security-sensitive change');

  manager.completeTask(task1.id);

  console.log('Tasks:', JSON.stringify(manager.getAllTasks(), null, 2));
  console.log('Stats:', manager.getStats());
}
