# Shopping Cart Module
# This file only defines the interface.
# Follow the TDD workflow and ask Claude to implement it.

from dataclasses import dataclass
from typing import List


@dataclass
class CartItem:
    id: str
    name: str
    price: float
    quantity: int


class ShoppingCartImpl:
    """
    TODO: Ask Claude to implement the ShoppingCartImpl class.
    Example: "Implement ShoppingCartImpl so it passes the tests in src/test_shopping_cart.py"
    """
    pass
