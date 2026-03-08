from todo import (
    add_todo,
    complete_todo,
    delete_todo,
    list_todos,
    list_completed,
    list_pending,
    clear_all,
)


class TestAddTodo:
    def setup_method(self):
        clear_all()

    def test_should_add_a_todo_with_incremental_id(self):
        todo1 = add_todo("Buy groceries")
        todo2 = add_todo("Walk the dog")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo1.title == "Buy groceries"
        assert todo1.completed is False


class TestCompleteTodo:
    def setup_method(self):
        clear_all()

    def test_should_mark_a_todo_as_completed(self):
        todo = add_todo("Read a book")
        completed = complete_todo(todo.id)

        assert completed is not None
        assert completed.completed is True

    def test_should_return_none_for_non_existent_id(self):
        result = complete_todo(999)
        assert result is None


class TestDeleteTodo:
    def setup_method(self):
        clear_all()

    def test_should_remove_a_todo(self):
        todo = add_todo("Clean house")
        assert delete_todo(todo.id) is True
        assert len(list_todos()) == 0

    def test_should_return_false_for_non_existent_id(self):
        assert delete_todo(999) is False


class TestListTodos:
    def setup_method(self):
        clear_all()

    def test_should_return_all_todos(self):
        add_todo("Task 1")
        add_todo("Task 2")
        add_todo("Task 3")

        assert len(list_todos()) == 3

    def test_should_return_a_copy_not_a_reference(self):
        add_todo("Task 1")
        result = list_todos()
        result.pop()

        assert len(list_todos()) == 1


class TestFiltering:
    def setup_method(self):
        clear_all()

    def test_should_filter_completed_and_pending(self):
        todo1 = add_todo("Done task")
        add_todo("Pending task")
        complete_todo(todo1.id)

        assert len(list_completed()) == 1
        assert len(list_pending()) == 1
