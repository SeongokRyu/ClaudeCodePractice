import time
import random
import string
from typing import Any, Callable, Dict, Optional

import database as db

COLLECTION = "users"

Callback = Callable[[Optional[Exception], Any], None]


def init_user_repo(callback: Callback) -> None:
    db.init_collection(COLLECTION, callback)


def create_user(name: str, email: str, callback: Callback) -> None:
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
    user = {
        "id": f"user_{int(time.time() * 1000)}_{random_suffix}",
        "name": name,
        "email": email,
        "created_at": time.time(),
    }

    def _on_insert(error: Optional[Exception], result: Any) -> None:
        if error:
            callback(error, None)
            return
        callback(None, result)

    db.insert(COLLECTION, user["id"], user, _on_insert)


def get_user_by_id(user_id: str, callback: Callback) -> None:
    def _on_find(error: Optional[Exception], result: Any) -> None:
        if error:
            callback(error, None)
            return
        callback(None, result)

    db.find_by_id(COLLECTION, user_id, _on_find)


def get_all_users(callback: Callback) -> None:
    def _on_find(error: Optional[Exception], result: Any) -> None:
        if error:
            callback(error, None)
            return
        callback(None, result)

    db.find_all(COLLECTION, _on_find)


def update_user(
    user_id: str, data: Dict[str, Any], callback: Callback
) -> None:
    def _on_update(error: Optional[Exception], result: Any) -> None:
        if error:
            callback(error, None)
            return
        callback(None, result)

    db.update(COLLECTION, user_id, data, _on_update)


def delete_user(user_id: str, callback: Callback) -> None:
    def _on_remove(error: Optional[Exception], result: Any) -> None:
        if error:
            callback(error, None)
            return
        callback(None, None)

    db.remove(COLLECTION, user_id, _on_remove)
