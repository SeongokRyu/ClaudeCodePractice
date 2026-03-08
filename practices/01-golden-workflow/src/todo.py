"""Todo management app - Practice 01 hands-on code"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Todo:
    id: int
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)


_todos: list[Todo] = []
_next_id: int = 1


def add_todo(title: str) -> Todo:
    global _next_id
    todo = Todo(id=_next_id, title=title)
    _next_id += 1
    _todos.append(todo)
    return todo


def complete_todo(id: int) -> Optional[Todo]:
    for todo in _todos:
        if todo.id == id:
            todo.completed = True
            return todo
    return None


def delete_todo(id: int) -> bool:
    for i, todo in enumerate(_todos):
        if todo.id == id:
            _todos.pop(i)
            return True
    return False


def list_todos() -> list[Todo]:
    return list(_todos)


def list_completed() -> list[Todo]:
    return [t for t in _todos if t.completed]


def list_pending() -> list[Todo]:
    return [t for t in _todos if not t.completed]


def clear_all() -> None:
    global _next_id
    _todos.clear()
    _next_id = 1
