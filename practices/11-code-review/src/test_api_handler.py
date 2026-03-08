from api_handler import (
    search_users,
    get_user_by_id,
    create_user,
    delete_user,
    process_request,
)


# Note: These tests pass but intentionally do NOT cover security cases.
# Part of the exercise is recognizing what's missing from the test suite.


class TestSearchUsers:
    def test_should_find_users_by_name(self):
        result = search_users("Alice")
        assert result.success is True
        assert len(result.data) == 1
        assert result.data[0]["name"] == "Alice"

    def test_should_return_empty_list_for_no_matches(self):
        result = search_users("NonExistent")
        assert result.success is True
        assert len(result.data) == 0

    def test_should_be_case_insensitive(self):
        result = search_users("alice")
        assert result.success is True
        assert len(result.data) == 1


class TestGetUserById:
    def test_should_return_user_by_id(self):
        result = get_user_by_id(1)
        assert result.success is True
        assert result.data["name"] == "Alice"

    def test_should_return_error_for_non_existent_user(self):
        result = get_user_by_id(999)
        assert result.success is False
        assert result.error is not None


class TestCreateUser:
    def test_should_create_a_new_user(self):
        result = create_user("Dave", "dave@example.com")
        assert result.success is True
        assert result.data["name"] == "Dave"
        assert result.data["email"] == "dave@example.com"


class TestProcessRequest:
    def test_should_route_to_correct_handler(self):
        result = process_request("search", {"query": "Bob"})
        assert result.success is True

    def test_should_handle_unknown_actions(self):
        result = process_request("unknown", {})
        assert result.success is False
