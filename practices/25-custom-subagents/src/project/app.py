"""
Sample Application -- Task Manager

A simple task management module for subagents to analyze,
extend, and review.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Literal

from utils import generate_id, format_date, validate_input


Status = Literal["todo", "in-progress", "done"]
Priority = Literal["low", "medium", "high"]


@dataclass
class Task:
    id: str
    title: str
    description: str
    status: Status
    priority: Priority
    created_at: datetime
    updated_at: datetime
    assignee: Optional[str] = None


class TaskManager:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def create_task(
        self,
        title: str,
        description: str,
        priority: Priority = "medium",
    ) -> Task:
        """Create a new task."""
        validate_input(title, "title")
        validate_input(description, "description")

        now = datetime.now()
        task = Task(
            id=generate_id(),
            title=title.strip(),
            description=description.strip(),
            status="todo",
            priority=priority,
            created_at=now,
            updated_at=now,
        )
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def update_status(self, task_id: str, status: Status) -> Task:
        """Update a task's status."""
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")

        task.status = status
        task.updated_at = datetime.now()
        return task

    def assign_task(self, task_id: str, assignee: str) -> Task:
        """Assign a task to someone."""
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")

        validate_input(assignee, "assignee")
        task.assignee = assignee.strip()
        task.updated_at = datetime.now()
        return task

    def list_tasks(self, status: Optional[Status] = None) -> list[Task]:
        """List all tasks, optionally filtered by status."""
        all_tasks = list(self._tasks.values())
        if status:
            return [t for t in all_tasks if t.status == status]
        return all_tasks

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def get_summary(self) -> dict[str, int]:
        """Get a summary of task counts by status."""
        summary: dict[str, int] = {
            "todo": 0,
            "in-progress": 0,
            "done": 0,
        }
        for task in self._tasks.values():
            summary[task.status] += 1
        return summary

    def format_task(self, task: Task) -> str:
        """Format a task for display."""
        assignee_str = f" (@{task.assignee})" if task.assignee else ""
        return f"[{task.status}] {task.title}{assignee_str} ({format_date(task.created_at)})"
