"""Tests for the TaskManager application."""

import pytest
from app import TaskManager, Task


@pytest.fixture
def manager() -> TaskManager:
    return TaskManager()


class TestCreateTask:
    def test_create_with_default_priority(self, manager: TaskManager) -> None:
        task = manager.create_task("Test task", "A test description")
        assert task.title == "Test task"
        assert task.description == "A test description"
        assert task.status == "todo"
        assert task.priority == "medium"
        assert task.id is not None
        assert task.created_at is not None

    def test_create_with_specified_priority(self, manager: TaskManager) -> None:
        task = manager.create_task("Urgent", "Fix now", "high")
        assert task.priority == "high"

    def test_trim_whitespace(self, manager: TaskManager) -> None:
        task = manager.create_task("  padded title  ", "  padded desc  ")
        assert task.title == "padded title"
        assert task.description == "padded desc"

    def test_empty_title_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="title cannot be empty"):
            manager.create_task("", "desc")

    def test_empty_description_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="description cannot be empty"):
            manager.create_task("title", "")


class TestGetTask:
    def test_return_task_by_id(self, manager: TaskManager) -> None:
        created = manager.create_task("Find me", "desc")
        found = manager.get_task(created.id)
        assert found == created

    def test_return_none_for_unknown_id(self, manager: TaskManager) -> None:
        assert manager.get_task("nonexistent") is None


class TestUpdateStatus:
    def test_update_status(self, manager: TaskManager) -> None:
        task = manager.create_task("Status test", "desc")
        updated = manager.update_status(task.id, "in-progress")
        assert updated.status == "in-progress"

    def test_update_timestamp(self, manager: TaskManager) -> None:
        task = manager.create_task("Timestamp test", "desc")
        original_updated_at = task.updated_at
        updated = manager.update_status(task.id, "done")
        assert updated.updated_at >= original_updated_at

    def test_unknown_task_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="Task not found"):
            manager.update_status("unknown", "done")


class TestAssignTask:
    def test_assign_task(self, manager: TaskManager) -> None:
        task = manager.create_task("Assign test", "desc")
        assigned = manager.assign_task(task.id, "alice")
        assert assigned.assignee == "alice"

    def test_empty_assignee_raises(self, manager: TaskManager) -> None:
        task = manager.create_task("Assign test", "desc")
        with pytest.raises(ValueError):
            manager.assign_task(task.id, "")


class TestListTasks:
    def test_list_all(self, manager: TaskManager) -> None:
        manager.create_task("Task 1", "desc")
        manager.create_task("Task 2", "desc")
        assert len(manager.list_tasks()) == 2

    def test_filter_by_status(self, manager: TaskManager) -> None:
        task1 = manager.create_task("Task 1", "desc")
        manager.create_task("Task 2", "desc")
        manager.update_status(task1.id, "done")
        assert len(manager.list_tasks("done")) == 1
        assert len(manager.list_tasks("todo")) == 1

    def test_empty_when_no_match(self, manager: TaskManager) -> None:
        assert len(manager.list_tasks("in-progress")) == 0


class TestDeleteTask:
    def test_delete_existing(self, manager: TaskManager) -> None:
        task = manager.create_task("Delete me", "desc")
        assert manager.delete_task(task.id) is True
        assert manager.get_task(task.id) is None

    def test_delete_nonexistent(self, manager: TaskManager) -> None:
        assert manager.delete_task("nonexistent") is False


class TestGetSummary:
    def test_correct_counts(self, manager: TaskManager) -> None:
        t1 = manager.create_task("T1", "d")
        t2 = manager.create_task("T2", "d")
        manager.create_task("T3", "d")
        manager.update_status(t1.id, "in-progress")
        manager.update_status(t2.id, "done")

        assert manager.get_summary() == {
            "todo": 1,
            "in-progress": 1,
            "done": 1,
        }
