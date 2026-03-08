import threading
import database as db
import user_repository as user_repo
import order_repository as order_repo


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


SAMPLE_ITEMS = [
    {"product_id": "p1", "name": "Widget", "price": 1000, "quantity": 2},
    {"product_id": "p2", "name": "Gadget", "price": 2500, "quantity": 1},
]


class TestCreateOrder:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: user_repo.init_user_repo(cb))
        _wait(lambda cb: order_repo.init_order_repo(cb))
        r = _wait(lambda cb: user_repo.create_user("Alice", "alice@example.com", cb))
        self.test_user_id = r["data"]["id"]

    def test_should_create_an_order_with_calculated_total(self):
        r = _wait(
            lambda cb: order_repo.create_order(self.test_user_id, SAMPLE_ITEMS, cb)
        )
        assert r["error"] is None
        order = r["data"]
        assert order is not None
        assert order["user_id"] == self.test_user_id
        assert len(order["items"]) == 2
        assert order["total"] == 4500  # 1000*2 + 2500*1
        assert order["status"] == "pending"


class TestGetOrderById:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: user_repo.init_user_repo(cb))
        _wait(lambda cb: order_repo.init_order_repo(cb))
        r = _wait(lambda cb: user_repo.create_user("Alice", "alice@example.com", cb))
        self.test_user_id = r["data"]["id"]

    def test_should_retrieve_an_order_by_id(self):
        r = _wait(
            lambda cb: order_repo.create_order(self.test_user_id, SAMPLE_ITEMS, cb)
        )
        assert r["error"] is None
        order_id = r["data"]["id"]
        r2 = _wait(lambda cb: order_repo.get_order_by_id(order_id, cb))
        assert r2["error"] is None
        assert r2["data"]["id"] == order_id
        assert r2["data"]["total"] == 4500


class TestGetOrdersByUserId:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: user_repo.init_user_repo(cb))
        _wait(lambda cb: order_repo.init_order_repo(cb))
        r = _wait(lambda cb: user_repo.create_user("Alice", "alice@example.com", cb))
        self.test_user_id = r["data"]["id"]

    def test_should_return_orders_for_a_specific_user(self):
        _wait(
            lambda cb: order_repo.create_order(self.test_user_id, SAMPLE_ITEMS, cb)
        )
        _wait(
            lambda cb: order_repo.create_order(
                self.test_user_id,
                [{"product_id": "p3", "name": "Doohickey", "price": 500, "quantity": 3}],
                cb,
            )
        )
        r = _wait(
            lambda cb: order_repo.get_orders_by_user_id(self.test_user_id, cb)
        )
        assert r["error"] is None
        assert len(r["data"]) == 2

    def test_should_return_empty_list_for_user_with_no_orders(self):
        r = _wait(
            lambda cb: order_repo.get_orders_by_user_id("other-user", cb)
        )
        assert r["error"] is None
        assert len(r["data"]) == 0


class TestUpdateOrderStatus:
    def setup_method(self):
        _wait(lambda cb: db.clear_all(cb))
        _wait(lambda cb: user_repo.init_user_repo(cb))
        _wait(lambda cb: order_repo.init_order_repo(cb))
        r = _wait(lambda cb: user_repo.create_user("Alice", "alice@example.com", cb))
        self.test_user_id = r["data"]["id"]

    def test_should_update_order_status(self):
        r = _wait(
            lambda cb: order_repo.create_order(self.test_user_id, SAMPLE_ITEMS, cb)
        )
        assert r["error"] is None
        order_id = r["data"]["id"]
        r2 = _wait(
            lambda cb: order_repo.update_order_status(order_id, "confirmed", cb)
        )
        assert r2["error"] is None
        assert r2["data"]["status"] == "confirmed"
