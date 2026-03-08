"""
In-memory user service with CRUD operations.

This service uses a dictionary to store users in memory.
It provides create, read, update, delete operations
along with listing and searching capabilities.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User type definition for the user service."""

    id: str
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class CreateUserInput:
    """
    Input type for creating a new user.
    The id, created_at, and updated_at fields are generated automatically.
    """

    name: str
    email: str


@dataclass
class UpdateUserInput:
    """
    Input type for updating an existing user.
    All fields are optional -- only provided fields will be updated.
    """

    name: Optional[str] = None
    email: Optional[str] = None


class UserService:
    """In-memory user service with CRUD operations."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._next_id: int = 1

    def create_user(self, input: CreateUserInput) -> User:
        """
        Creates a new user.
        Generates a unique ID and timestamps automatically.
        """
        user_id = str(self._next_id)
        self._next_id += 1
        now = datetime.now()

        user = User(
            id=user_id,
            name=input.name,
            email=input.email,
            created_at=now,
            updated_at=now,
        )

        self._users[user_id] = user
        return user

    def get_user(self, id: str) -> Optional[User]:
        """
        Retrieves a user by ID.
        Returns None if the user is not found.
        """
        return self._users.get(id, None)

    def update_user(self, id: str, input: UpdateUserInput) -> User:
        """
        Updates an existing user.
        Only the provided fields in the input will be updated.
        Raises an error if the user is not found.
        """
        user = self._users.get(id)
        if user is None:
            raise ValueError(f'User with id "{id}" not found')

        if input.name is not None:
            user.name = input.name
        if input.email is not None:
            user.email = input.email
        user.updated_at = datetime.now()

        self._users[id] = user
        return user

    def delete_user(self, id: str) -> bool:
        """
        Deletes a user by ID.
        Returns True if the user was deleted, False if not found.
        """
        if id in self._users:
            del self._users[id]
            return True
        return False

    def list_users(self) -> list[User]:
        """Returns all users as a list."""
        return list(self._users.values())

    def count(self) -> int:
        """Returns the total number of users."""
        return len(self._users)

    def clear(self) -> None:
        """
        Clears all users from the store.
        Useful for testing.
        """
        self._users.clear()
        self._next_id = 1
