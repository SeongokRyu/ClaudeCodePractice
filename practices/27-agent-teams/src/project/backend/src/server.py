"""
Sample Backend Server

A minimal Flask server structure for Agent Teams to work on.
Note: This is a structural example -- install Flask to run it.

Usage:
    pip install flask
    python server.py
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, Literal

from flask import Flask, jsonify, request

# ── Types ────────────────────────────────────────────────────────────────

Status = Literal["todo", "in-progress", "done"]


@dataclass
class Task:
    id: str
    title: str
    description: str
    status: Status
    created_at: str  # ISO format string for JSON serialization
    assignee: Optional[str] = None


@dataclass
class DashboardResponse:
    tasks: list[dict]
    total_count: int
    completed_count: int


# ── In-memory task store ─────────────────────────────────────────────────

tasks: dict[str, Task] = {}


def seed_data() -> None:
    """Seed some sample data."""
    sample_tasks = [
        Task(
            id="1",
            title="Set up project",
            description="Initialize the project structure",
            status="done",
            assignee="alice",
            created_at="2026-01-01T00:00:00",
        ),
        Task(
            id="2",
            title="Implement auth",
            description="Add user authentication",
            status="in-progress",
            assignee="bob",
            created_at="2026-01-15T00:00:00",
        ),
        Task(
            id="3",
            title="Write tests",
            description="Add comprehensive test coverage",
            status="todo",
            created_at="2026-02-01T00:00:00",
        ),
    ]
    for task in sample_tasks:
        tasks[task.id] = task


# ── API Functions (also usable without Flask) ────────────────────────────


def get_dashboard() -> DashboardResponse:
    """GET /api/dashboard -- Returns dashboard data with task summary."""
    all_tasks = list(tasks.values())
    return DashboardResponse(
        tasks=[asdict(t) for t in all_tasks],
        total_count=len(all_tasks),
        completed_count=sum(1 for t in all_tasks if t.status == "done"),
    )


def get_tasks(status: Optional[Status] = None) -> list[Task]:
    """GET /api/tasks -- Returns all tasks, optionally filtered by status."""
    all_tasks = list(tasks.values())
    if status:
        return [t for t in all_tasks if t.status == status]
    return all_tasks


def get_task_by_id(task_id: str) -> Optional[Task]:
    """GET /api/tasks/:id -- Returns a single task by ID."""
    return tasks.get(task_id)


def create_task(
    title: str,
    description: str,
    assignee: Optional[str] = None,
) -> Task:
    """POST /api/tasks -- Creates a new task."""
    task_id = format(int(datetime.now().timestamp() * 1000), "x")
    task = Task(
        id=task_id,
        title=title,
        description=description,
        status="todo",
        assignee=assignee,
        created_at=datetime.now().isoformat(),
    )
    tasks[task.id] = task
    return task


# ── Flask App ────────────────────────────────────────────────────────────

app = Flask(__name__)


@app.route("/api/dashboard", methods=["GET"])
def dashboard_endpoint():
    data = get_dashboard()
    return jsonify(asdict(data))


@app.route("/api/tasks", methods=["GET"])
def tasks_endpoint():
    status = request.args.get("status")
    result = get_tasks(status)
    return jsonify([asdict(t) for t in result])


@app.route("/api/tasks/<task_id>", methods=["GET"])
def task_by_id_endpoint(task_id: str):
    task = get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(asdict(task))


@app.route("/api/tasks", methods=["POST"])
def create_task_endpoint():
    data = request.get_json()
    if not data or "title" not in data or "description" not in data:
        return jsonify({"error": "title and description are required"}), 400
    task = create_task(
        title=data["title"],
        description=data["description"],
        assignee=data.get("assignee"),
    )
    return jsonify(asdict(task)), 201


# ── Initialize ───────────────────────────────────────────────────────────

seed_data()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
