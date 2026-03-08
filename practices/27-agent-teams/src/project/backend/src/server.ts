/**
 * Sample Backend Server
 *
 * A minimal Express-like server structure for Agent Teams to work on.
 * Note: This is a structural example — not meant to be run directly without dependencies.
 */

interface Task {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in-progress" | "done";
  assignee?: string;
  createdAt: Date;
}

interface DashboardResponse {
  tasks: Task[];
  totalCount: number;
  completedCount: number;
}

// In-memory task store
const tasks: Map<string, Task> = new Map();

// Seed some sample data
function seedData(): void {
  const sampleTasks: Task[] = [
    {
      id: "1",
      title: "Set up project",
      description: "Initialize the project structure",
      status: "done",
      assignee: "alice",
      createdAt: new Date("2026-01-01"),
    },
    {
      id: "2",
      title: "Implement auth",
      description: "Add user authentication",
      status: "in-progress",
      assignee: "bob",
      createdAt: new Date("2026-01-15"),
    },
    {
      id: "3",
      title: "Write tests",
      description: "Add comprehensive test coverage",
      status: "todo",
      createdAt: new Date("2026-02-01"),
    },
  ];

  sampleTasks.forEach((task) => tasks.set(task.id, task));
}

/**
 * GET /api/dashboard
 * Returns dashboard data with task summary.
 */
function getDashboard(): DashboardResponse {
  const allTasks = Array.from(tasks.values());
  return {
    tasks: allTasks,
    totalCount: allTasks.length,
    completedCount: allTasks.filter((t) => t.status === "done").length,
  };
}

/**
 * GET /api/tasks
 * Returns all tasks, optionally filtered by status.
 */
function getTasks(status?: Task["status"]): Task[] {
  const allTasks = Array.from(tasks.values());
  if (status) {
    return allTasks.filter((t) => t.status === status);
  }
  return allTasks;
}

/**
 * GET /api/tasks/:id
 * Returns a single task by ID.
 */
function getTaskById(id: string): Task | undefined {
  return tasks.get(id);
}

/**
 * POST /api/tasks
 * Creates a new task.
 */
function createTask(
  title: string,
  description: string,
  assignee?: string
): Task {
  const id = Date.now().toString(36);
  const task: Task = {
    id,
    title,
    description,
    status: "todo",
    assignee,
    createdAt: new Date(),
  };
  tasks.set(id, task);
  return task;
}

// Initialize
seedData();

export { getDashboard, getTasks, getTaskById, createTask };
