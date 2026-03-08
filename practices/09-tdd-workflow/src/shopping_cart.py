# Shopping Cart Module
# 이 파일은 인터페이스만 정의되어 있습니다.
# TDD 워크플로우에 따라 Claude에게 구현을 요청하세요.

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
    TODO: Claude에게 ShoppingCartImpl 클래스를 구현해달라고 요청하세요.
    예: "src/test_shopping_cart.py의 테스트를 통과하도록 ShoppingCartImpl을 구현해줘"
    """
    pass
