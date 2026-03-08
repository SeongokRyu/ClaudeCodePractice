from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, List, Literal, Optional, TypeVar

T = TypeVar("T")


@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: datetime


@dataclass
class OrderItem:
    product_id: str
    name: str
    price: float
    quantity: int


@dataclass
class Order:
    id: str
    user_id: str
    items: List[OrderItem]
    total: float
    status: Literal["pending", "confirmed", "shipped", "delivered"]
    created_at: datetime


@dataclass
class Notification:
    id: str
    user_id: str
    message: str
    type: Literal["email", "sms", "push"]
    sent_at: datetime


# Callback type: callback(error, result)
Callback = Callable[[Optional[Exception], Optional[T]], None]
