import time
import random
import string
from typing import Any, Callable, Dict, List, Optional

import database as db

COLLECTION = "orders"

Callback = Callable[[Optional[Exception], Any], None]


def init_order_repo(callback: Callback) -> None:
    db.init_collection(COLLECTION, callback)


def create_order(
    user_id: str, items: List[Dict[str, Any]], callback: Callback
) -> None:
    total = sum(item["price"] * item["quantity"] for item in items)
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=9))

    order = {
        "id": f"order_{int(time.time() * 1000)}_{random_suffix}",
        "user_id": user_id,
        "items": items,
        "total": total,
        "status": "pending",
        "created_at": time.time(),
    }

    def _on_insert(error: Optional[Exception], result: Any) -> None:
        if error:
            callback(error, None)
            return
        callback(None, result)

    db.insert(COLLECTION, order["id"], order, _on_insert)


def get_order_by_id(order_id: str, callback: Callback) -> None:
    def _on_find(error: Optional[Exception], result: Any) -> None:
        if error:
            callback(error, None)
            return
        callback(None, result)

    db.find_by_id(COLLECTION, order_id, _on_find)


def get_orders_by_user_id(user_id: str, callback: Callback) -> None:
    def _on_find(error: Optional[Exception], results: Any) -> None:
        if error:
            callback(error, None)
            return
        user_orders = [o for o in results if o.get("user_id") == user_id]
        callback(None, user_orders)

    db.find_all(COLLECTION, _on_find)


def update_order_status(
    order_id: str, status: str, callback: Callback
) -> None:
    def _on_update(error: Optional[Exception], result: Any) -> None:
        if error:
            callback(error, None)
            return
        callback(None, result)

    db.update(COLLECTION, order_id, {"status": status}, _on_update)
