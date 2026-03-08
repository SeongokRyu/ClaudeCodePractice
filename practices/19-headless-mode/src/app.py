"""
Simple Task Manager Application
Used as sample code for headless mode practice scripts.
"""

# TODO: Add task priority levels (high, medium, low)
# TODO: Implement task categories/tags
# FIXME: Task ID generation could collide in concurrent scenarios

import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    # TODO: Add due_date field
    # TODO: Add assignee field


class TaskManager:
    def __init__(self) -> None:
        # TODO: Accept initial tasks in constructor
        self._tasks: dict[str, Task] = {}
        self._next_id: int = 1

    def _generate_id(self) -> str:
        """
        Generate a unique task ID.
        FIXME: This is not safe for concurrent use -- consider UUID
        """
        task_id = f"task-{self._next_id}"
        self._next_id += 1
        return task_id

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task."""
        if not title or title.strip() == "":
            raise ValueError("Task title cannot be empty")

        now = datetime.now()
        task = Task(
            id=self._generate_id(),
            title=title.strip(),
            description=description.strip(),
            completed=False,
            created_at=now,
            updated_at=now,
        )
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """
        Get all tasks.
        TODO: Add filtering options (by status, date range, etc.)
        """
        return list(self._tasks.values())

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Task:
        """
        Update a task's title and/or description.
        TODO: Support partial updates with a patch object
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")

        if title is not None:
            if title.strip() == "":
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()

        task.updated_at = datetime.now()
        return task

    def complete_task(self, task_id: str) -> Task:
        """Mark a task as completed."""
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")

        task.completed = True
        task.updated_at = datetime.now()
        return task

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.
        TODO: Add soft delete option
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task not found: {task_id}")
        del self._tasks[task_id]
        return True

    def get_stats(self) -> dict[str, int]:
        """
        Get task statistics.
        FIXME: This recalculates every time -- consider caching
        """
        tasks = self.get_all_tasks()
        completed = sum(1 for t in tasks if t.completed)
        return {
            "total": len(tasks),
            "completed": completed,
            "pending": len(tasks) - completed,
        }

    def search_tasks(self, query: str) -> list[Task]:
        """
        Search tasks by title.
        TODO: Add full-text search across title and description
        TODO: Add regex search support
        """
        lower_query = query.lower()
        return [
            task
            for task in self.get_all_tasks()
            if lower_query in task.title.lower()
        ]

    def export_to_json(self) -> str:
        """Export tasks to JSON string."""
        tasks_data = []
        for task in self.get_all_tasks():
            d = asdict(task)
            d["created_at"] = task.created_at.isoformat()
            d["updated_at"] = task.updated_at.isoformat()
            tasks_data.append(d)
        return json.dumps(tasks_data, indent=2)

    def import_from_json(self, json_str: str) -> int:
        """
        Import tasks from JSON string.
        TODO: Add validation for imported data
        FIXME: This doesn't handle duplicate IDs
        """
        tasks_data: list[dict] = json.loads(json_str)
        imported = 0

        for data in tasks_data:
            if data.get("id") and data.get("title"):
                task = Task(
                    id=data["id"],
                    title=data["title"],
                    description=data.get("description", ""),
                    completed=data.get("completed", False),
                    created_at=datetime.fromisoformat(data["created_at"]),
                    updated_at=datetime.fromisoformat(data["updated_at"]),
                )
                self._tasks[task.id] = task
                imported += 1

        return imported


# Main entry point for CLI usage
if __name__ == "__main__":
    manager = TaskManager()

    # Demo usage
    task1 = manager.create_task("Set up CI/CD pipeline", "Configure GitHub Actions")
    task2 = manager.create_task("Write unit tests", "Cover all edge cases")
    task3 = manager.create_task("Review PR #42", "Security-sensitive change")

    manager.complete_task(task1.id)

    print("Tasks:", manager.export_to_json())
    print("Stats:", manager.get_stats())
