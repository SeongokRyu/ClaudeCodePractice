import time
import random
import string
import threading
from typing import Any, Callable, List, Optional

Callback = Callable[[Optional[Exception], Any], None]

# In-memory notification log
_sent_notifications: List[dict] = []


def send_notification(
    user_id: str, message: str, notif_type: str, callback: Callback
) -> None:
    def _run():
        random_suffix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=9)
        )
        notification = {
            "id": f"notif_{int(time.time() * 1000)}_{random_suffix}",
            "user_id": user_id,
            "message": message,
            "type": notif_type,
            "sent_at": time.time(),
        }
        _sent_notifications.append(notification)
        callback(None, notification)

    timer = threading.Timer(0.01, _run)
    timer.start()


def get_notifications_by_user_id(
    user_id: str, callback: Callback
) -> None:
    def _run():
        user_notifications = [
            n for n in _sent_notifications if n.get("user_id") == user_id
        ]
        callback(None, user_notifications)

    timer = threading.Timer(0.01, _run)
    timer.start()


def clear_notifications(callback: Callback) -> None:
    def _run():
        _sent_notifications.clear()
        callback(None, None)

    timer = threading.Timer(0.01, _run)
    timer.start()
