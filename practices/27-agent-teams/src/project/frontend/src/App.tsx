/**
 * Sample Frontend Application
 *
 * A minimal React-like application structure for Agent Teams to work on.
 * Note: This is a structural example — not meant to be run directly.
 */

import React, { useState, useEffect } from "react";

interface Task {
  id: string;
  title: string;
  status: "todo" | "in-progress" | "done";
  assignee?: string;
}

interface DashboardData {
  tasks: Task[];
  totalCount: number;
  completedCount: number;
}

/**
 * Main App component.
 */
export function App(): React.ReactElement {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No data</div>;

  return (
    <div className="app">
      <header>
        <h1>Task Dashboard</h1>
        <p>
          {data.completedCount}/{data.totalCount} tasks completed
        </p>
      </header>
      <main>
        <TaskList tasks={data.tasks} />
      </main>
    </div>
  );
}

/**
 * Task list component.
 */
function TaskList({ tasks }: { tasks: Task[] }): React.ReactElement {
  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </ul>
  );
}

/**
 * Individual task item component.
 */
function TaskItem({ task }: { task: Task }): React.ReactElement {
  return (
    <li className={`task-item task-${task.status}`}>
      <span className="task-title">{task.title}</span>
      <span className="task-status">{task.status}</span>
      {task.assignee && <span className="task-assignee">@{task.assignee}</span>}
    </li>
  );
}

/**
 * Fetch dashboard data from the API.
 */
async function fetchDashboard(): Promise<DashboardData> {
  const response = await fetch("/api/dashboard");
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}

export default App;
