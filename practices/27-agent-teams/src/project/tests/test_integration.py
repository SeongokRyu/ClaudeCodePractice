"""
Integration Tests -- Starter File

Tests that verify the full-stack flow works correctly.
Agent Teams should expand these tests significantly.
"""

import sys
import os

# Add backend to path for direct imports
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "backend", "src")
)

from server import get_dashboard, get_tasks, create_task


class TestDashboardAPI:
    def test_returns_dashboard_data_with_task_counts(self) -> None:
        dashboard = get_dashboard()
        assert dashboard.tasks is not None
        assert dashboard.total_count > 0
        assert dashboard.completed_count is not None
        assert dashboard.completed_count <= dashboard.total_count

    def test_includes_all_task_fields(self) -> None:
        dashboard = get_dashboard()
        task = dashboard.tasks[0]
        assert "id" in task
        assert "title" in task
        assert "status" in task
        assert task["status"] in ("todo", "in-progress", "done")


class TestTasksAPI:
    def test_returns_all_tasks(self) -> None:
        tasks = get_tasks()
        assert len(tasks) > 0

    def test_filters_by_status(self) -> None:
        done_tasks = get_tasks("done")
        for task in done_tasks:
            assert task.status == "done"

    def test_creates_new_task(self) -> None:
        task = create_task("Test task", "Test description", "tester")
        assert task.id is not None
        assert task.title == "Test task"
        assert task.status == "todo"
        assert task.assignee == "tester"
