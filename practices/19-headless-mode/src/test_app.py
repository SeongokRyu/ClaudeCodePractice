"""Tests for the Task Manager application."""

import pytest
import re
from app import TaskManager, Task


@pytest.fixture
def manager() -> TaskManager:
    return TaskManager()


class TestCreateTask:
    def test_create_task_with_title_and_description(self, manager: TaskManager) -> None:
        task = manager.create_task("Test task", "Test description")
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.completed is False
        assert re.match(r"^task-\d+$", task.id)

    def test_create_task_with_only_title(self, manager: TaskManager) -> None:
        task = manager.create_task("Title only")
        assert task.title == "Title only"
        assert task.description == ""

    def test_trim_whitespace(self, manager: TaskManager) -> None:
        task = manager.create_task("  padded title  ", "  padded desc  ")
        assert task.title == "padded title"
        assert task.description == "padded desc"

    def test_empty_title_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            manager.create_task("")

    def test_whitespace_only_title_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            manager.create_task("   ")

    def test_unique_ids(self, manager: TaskManager) -> None:
        task1 = manager.create_task("Task 1")
        task2 = manager.create_task("Task 2")
        assert task1.id != task2.id


class TestGetTask:
    def test_return_task_by_id(self, manager: TaskManager) -> None:
        created = manager.create_task("Find me")
        found = manager.get_task(created.id)
        assert found is not None
        assert found.title == "Find me"

    def test_return_none_for_nonexistent_id(self, manager: TaskManager) -> None:
        assert manager.get_task("task-999") is None


class TestGetAllTasks:
    def test_empty_when_no_tasks(self, manager: TaskManager) -> None:
        assert manager.get_all_tasks() == []

    def test_return_all_tasks(self, manager: TaskManager) -> None:
        manager.create_task("Task 1")
        manager.create_task("Task 2")
        manager.create_task("Task 3")
        assert len(manager.get_all_tasks()) == 3


class TestUpdateTask:
    def test_update_title(self, manager: TaskManager) -> None:
        task = manager.create_task("Original")
        updated = manager.update_task(task.id, title="Updated")
        assert updated.title == "Updated"

    def test_update_description(self, manager: TaskManager) -> None:
        task = manager.create_task("Title", "Old desc")
        updated = manager.update_task(task.id, description="New desc")
        assert updated.description == "New desc"
        assert updated.title == "Title"

    def test_nonexistent_task_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="Task not found"):
            manager.update_task("task-999", title="New")

    def test_empty_title_raises(self, manager: TaskManager) -> None:
        task = manager.create_task("Original")
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            manager.update_task(task.id, title="")


class TestCompleteTask:
    def test_mark_as_completed(self, manager: TaskManager) -> None:
        task = manager.create_task("Complete me")
        completed = manager.complete_task(task.id)
        assert completed.completed is True

    def test_nonexistent_task_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="Task not found"):
            manager.complete_task("task-999")


class TestDeleteTask:
    def test_delete_existing_task(self, manager: TaskManager) -> None:
        task = manager.create_task("Delete me")
        assert manager.delete_task(task.id) is True
        assert manager.get_task(task.id) is None

    def test_nonexistent_task_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="Task not found"):
            manager.delete_task("task-999")


class TestGetStats:
    def test_zeros_when_empty(self, manager: TaskManager) -> None:
        assert manager.get_stats() == {"total": 0, "completed": 0, "pending": 0}

    def test_count_completed_and_pending(self, manager: TaskManager) -> None:
        t1 = manager.create_task("Task 1")
        manager.create_task("Task 2")
        manager.create_task("Task 3")
        manager.complete_task(t1.id)
        assert manager.get_stats() == {"total": 3, "completed": 1, "pending": 2}


class TestSearchTasks:
    @pytest.fixture(autouse=True)
    def setup_tasks(self, manager: TaskManager) -> None:
        manager.create_task("Set up CI/CD")
        manager.create_task("Write unit tests")
        manager.create_task("Set up monitoring")

    def test_find_by_partial_title(self, manager: TaskManager) -> None:
        results = manager.search_tasks("set up")
        assert len(results) == 2

    def test_case_insensitive(self, manager: TaskManager) -> None:
        results = manager.search_tasks("SET UP")
        assert len(results) == 2

    def test_no_matches(self, manager: TaskManager) -> None:
        results = manager.search_tasks("nonexistent")
        assert len(results) == 0


class TestExportImportJson:
    def test_round_trip(self, manager: TaskManager) -> None:
        manager.create_task("Task 1", "Desc 1")
        manager.create_task("Task 2", "Desc 2")

        json_str = manager.export_to_json()
        new_manager = TaskManager()
        imported = new_manager.import_from_json(json_str)

        assert imported == 2
        assert len(new_manager.get_all_tasks()) == 2
