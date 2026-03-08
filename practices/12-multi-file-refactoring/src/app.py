from typing import Any, Callable, Dict, List, Optional

import user_repository as user_repo
import order_repository as order_repo
import notification_service

Callback = Callable[[Optional[Exception], Any], None]


def init_app(callback: Callback) -> None:
    def _on_user_init(error: Optional[Exception], result: Any) -> None:
        if error:
            callback(error, None)
            return

        def _on_order_init(error2: Optional[Exception], result2: Any) -> None:
            if error2:
                callback(error2, None)
                return
            callback(None, None)

        order_repo.init_order_repo(_on_order_init)

    user_repo.init_user_repo(_on_user_init)


# Create a user and send a welcome notification — classic callback chain
def register_user(name: str, email: str, callback: Callback) -> None:
    def _on_create(error: Optional[Exception], user: Any) -> None:
        if error:
            callback(error, None)
            return

        def _on_notify(
            error2: Optional[Exception], notification: Any
        ) -> None:
            if error2:
                callback(error2, None)
                return
            callback(None, {"user": user, "notification": notification})

        notification_service.send_notification(
            user["id"],
            f"Welcome, {user['name']}!",
            "email",
            _on_notify,
        )

    user_repo.create_user(name, email, _on_create)


# Place an order and notify the user — deeper callback chain
def place_order(
    user_id: str, items: List[Dict[str, Any]], callback: Callback
) -> None:
    # First verify the user exists
    def _on_get_user(error: Optional[Exception], user: Any) -> None:
        if error:
            callback(error, None)
            return

        # Then create the order
        def _on_create_order(
            error2: Optional[Exception], order: Any
        ) -> None:
            if error2:
                callback(error2, None)
                return

            # Then send notification
            def _on_notify(
                error3: Optional[Exception], notification: Any
            ) -> None:
                if error3:
                    callback(error3, None)
                    return
                callback(
                    None, {"order": order, "notification": notification}
                )

            notification_service.send_notification(
                user_id,
                f"Order {order['id']} placed successfully. Total: {order['total']}",
                "email",
                _on_notify,
            )

        order_repo.create_order(user_id, items, _on_create_order)

    user_repo.get_user_by_id(user_id, _on_get_user)


# Get user dashboard data — parallel-ish callbacks (but done sequentially)
def get_user_dashboard(user_id: str, callback: Callback) -> None:
    def _on_get_user(error: Optional[Exception], user: Any) -> None:
        if error:
            callback(error, None)
            return

        def _on_get_orders(
            error2: Optional[Exception], orders: Any
        ) -> None:
            if error2:
                callback(error2, None)
                return

            def _on_get_notifications(
                error3: Optional[Exception], notifications: Any
            ) -> None:
                if error3:
                    callback(error3, None)
                    return
                callback(
                    None,
                    {
                        "user": user,
                        "orders": orders,
                        "notifications": notifications,
                    },
                )

            notification_service.get_notifications_by_user_id(
                user_id, _on_get_notifications
            )

        order_repo.get_orders_by_user_id(user_id, _on_get_orders)

    user_repo.get_user_by_id(user_id, _on_get_user)
