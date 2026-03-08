from datetime import datetime

from user_service import UserService, CreateUserInput, UpdateUserInput


class TestCreateUser:
    def setup_method(self):
        self.service = UserService()

    def test_should_create_a_user_with_generated_id_and_timestamps(self):
        user = self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )

        assert user.id == "1"
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_should_assign_incrementing_ids(self):
        user1 = self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )
        user2 = self.service.create_user(
            CreateUserInput(name="Bob", email="bob@example.com")
        )

        assert user1.id == "1"
        assert user2.id == "2"


class TestGetUser:
    def setup_method(self):
        self.service = UserService()

    def test_should_return_a_user_by_id(self):
        created = self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )
        found = self.service.get_user(created.id)

        assert found is not None
        assert found.name == "Alice"

    def test_should_return_none_for_non_existent_user(self):
        found = self.service.get_user("999")
        assert found is None


class TestUpdateUser:
    def setup_method(self):
        self.service = UserService()

    def test_should_update_user_fields(self):
        created = self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )
        updated = self.service.update_user(
            created.id, UpdateUserInput(name="Alice Updated")
        )

        assert updated.name == "Alice Updated"
        assert updated.email == "alice@example.com"

    def test_should_update_the_updated_at_timestamp(self):
        created = self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )
        original_updated_at = created.updated_at

        updated = self.service.update_user(
            created.id, UpdateUserInput(name="Alice Updated")
        )
        assert updated.updated_at >= original_updated_at

    def test_should_raise_error_when_user_not_found(self):
        import pytest

        with pytest.raises(ValueError, match='User with id "999" not found'):
            self.service.update_user("999", UpdateUserInput(name="Ghost"))


class TestDeleteUser:
    def setup_method(self):
        self.service = UserService()

    def test_should_delete_an_existing_user(self):
        created = self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )
        result = self.service.delete_user(created.id)

        assert result is True
        assert self.service.get_user(created.id) is None

    def test_should_return_false_when_deleting_non_existent_user(self):
        result = self.service.delete_user("999")
        assert result is False


class TestListUsers:
    def setup_method(self):
        self.service = UserService()

    def test_should_return_empty_list_when_no_users_exist(self):
        assert self.service.list_users() == []

    def test_should_return_all_users(self):
        self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )
        self.service.create_user(
            CreateUserInput(name="Bob", email="bob@example.com")
        )

        users = self.service.list_users()
        assert len(users) == 2


class TestCount:
    def setup_method(self):
        self.service = UserService()

    def test_should_return_0_when_no_users_exist(self):
        assert self.service.count() == 0

    def test_should_return_the_correct_count(self):
        self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )
        self.service.create_user(
            CreateUserInput(name="Bob", email="bob@example.com")
        )

        assert self.service.count() == 2


class TestClear:
    def setup_method(self):
        self.service = UserService()

    def test_should_remove_all_users(self):
        self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )
        self.service.create_user(
            CreateUserInput(name="Bob", email="bob@example.com")
        )

        self.service.clear()

        assert self.service.count() == 0
        assert self.service.list_users() == []

    def test_should_reset_id_counter(self):
        self.service.create_user(
            CreateUserInput(name="Alice", email="alice@example.com")
        )
        self.service.clear()

        user = self.service.create_user(
            CreateUserInput(name="Bob", email="bob@example.com")
        )
        assert user.id == "1"
