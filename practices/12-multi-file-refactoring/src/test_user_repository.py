import threading
import database as db
import user_repository as user_repo


def _wait(fn, timeout=5):
    """Helper to run a callback-based function synchronously in tests."""
    result = {"error": None, "data": None}
    event = threading.Event()

    def callback(error, data):
        result["error"] = error
        result["data"] = data
        event.set()

    fn(callback)
    event.wait(timeout)
    return result


class TestCreateUser:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: user_repo.init_user_repo(cb))

    def test_should_create_a_user_with_generated_id(self):
        r = _wait(lambda cb: user_repo.create_user("Alice", "alice@example.com", cb))
        assert r["error"] is None
        user = r["data"]
        assert user is not None
        assert user["name"] == "Alice"
        assert user["email"] == "alice@example.com"
        assert user["id"] is not None
        assert user["created_at"] is not None


class TestGetUserById:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: user_repo.init_user_repo(cb))

    def test_should_retrieve_a_user_by_id(self):
        r = _wait(lambda cb: user_repo.create_user("Alice", "alice@example.com", cb))
        assert r["error"] is None
        user_id = r["data"]["id"]
        r2 = _wait(lambda cb: user_repo.get_user_by_id(user_id, cb))
        assert r2["error"] is None
        assert r2["data"]["name"] == "Alice"

    def test_should_return_error_for_non_existent_user(self):
        r = _wait(lambda cb: user_repo.get_user_by_id("nonexistent", cb))
        assert r["error"] is not None


class TestGetAllUsers:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: user_repo.init_user_repo(cb))

    def test_should_return_all_users(self):
        _wait(lambda cb: user_repo.create_user("Alice", "alice@example.com", cb))
        _wait(lambda cb: user_repo.create_user("Bob", "bob@example.com", cb))
        r = _wait(lambda cb: user_repo.get_all_users(cb))
        assert r["error"] is None
        assert len(r["data"]) == 2


class TestUpdateUser:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: user_repo.init_user_repo(cb))

    def test_should_update_user_data(self):
        r = _wait(lambda cb: user_repo.create_user("Alice", "alice@example.com", cb))
        assert r["error"] is None
        user_id = r["data"]["id"]
        r2 = _wait(
            lambda cb: user_repo.update_user(user_id, {"name": "Alice Updated"}, cb)
        )
        assert r2["error"] is None
        assert r2["data"]["name"] == "Alice Updated"
        assert r2["data"]["email"] == "alice@example.com"


class TestDeleteUser:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: user_repo.init_user_repo(cb))

    def test_should_delete_a_user(self):
        r = _wait(lambda cb: user_repo.create_user("Alice", "alice@example.com", cb))
        assert r["error"] is None
        user_id = r["data"]["id"]
        r2 = _wait(lambda cb: user_repo.delete_user(user_id, cb))
        assert r2["error"] is None
        r3 = _wait(lambda cb: user_repo.get_user_by_id(user_id, cb))
        assert r3["error"] is not None
