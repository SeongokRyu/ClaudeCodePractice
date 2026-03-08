import threading
import database as db


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


class TestDatabaseInsert:
    def setup_method(self):
        r = _wait(lambda cb: db.clear_all(cb))
        r = _wait(lambda cb: db.init_collection("test", cb))

    def test_should_insert_a_document(self):
        r = _wait(lambda cb: db.insert("test", "1", {"name": "Alice"}, cb))
        assert r["error"] is None
        assert r["data"] == {"name": "Alice"}

    def test_should_reject_duplicate_ids(self):
        _wait(lambda cb: db.insert("test", "1", {"name": "Alice"}, cb))
        r = _wait(lambda cb: db.insert("test", "1", {"name": "Bob"}, cb))
        assert r["error"] is not None
        assert "already exists" in str(r["error"])

    def test_should_reject_insert_to_non_existent_collection(self):
        r = _wait(lambda cb: db.insert("nonexistent", "1", {"name": "Alice"}, cb))
        assert r["error"] is not None
        assert "does not exist" in str(r["error"])


class TestDatabaseFindById:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: db.init_collection("test", cb))

    def test_should_find_a_document_by_id(self):
        _wait(lambda cb: db.insert("test", "1", {"name": "Alice"}, cb))
        r = _wait(lambda cb: db.find_by_id("test", "1", cb))
        assert r["error"] is None
        assert r["data"] == {"name": "Alice"}

    def test_should_return_error_for_non_existent_document(self):
        r = _wait(lambda cb: db.find_by_id("test", "nonexistent", cb))
        assert r["error"] is not None
        assert "not found" in str(r["error"])


class TestDatabaseFindAll:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: db.init_collection("test", cb))

    def test_should_return_all_documents(self):
        _wait(lambda cb: db.insert("test", "1", {"name": "Alice"}, cb))
        _wait(lambda cb: db.insert("test", "2", {"name": "Bob"}, cb))
        r = _wait(lambda cb: db.find_all("test", cb))
        assert r["error"] is None
        assert len(r["data"]) == 2


class TestDatabaseUpdate:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: db.init_collection("test", cb))

    def test_should_update_a_document(self):
        _wait(lambda cb: db.insert("test", "1", {"name": "Alice", "age": 25}, cb))
        r = _wait(lambda cb: db.update("test", "1", {"age": 26}, cb))
        assert r["error"] is None
        assert r["data"] == {"name": "Alice", "age": 26}

    def test_should_return_error_for_non_existent_document(self):
        r = _wait(lambda cb: db.update("test", "nonexistent", {"name": "New"}, cb))
        assert r["error"] is not None


class TestDatabaseRemove:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: db.init_collection("test", cb))

    def test_should_remove_a_document(self):
        _wait(lambda cb: db.insert("test", "1", {"name": "Alice"}, cb))
        r = _wait(lambda cb: db.remove("test", "1", cb))
        assert r["error"] is None
        r2 = _wait(lambda cb: db.find_by_id("test", "1", cb))
        assert r2["error"] is not None
