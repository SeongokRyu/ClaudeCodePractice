// Shopping Cart Module
// 이 파일은 인터페이스만 정의되어 있습니다.
// TDD 워크플로우에 따라 Claude에게 구현을 요청하세요.

export interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

export interface ShoppingCart {
  addItem(item: Omit<CartItem, 'quantity'>, quantity?: number): void;
  removeItem(itemId: string): void;
  getItems(): CartItem[];
  getTotal(): number;
  applyDiscount(percent: number): number;
  clearCart(): void;
  getItemCount(): number;
}

// TODO: Claude에게 ShoppingCart 인터페이스를 구현하는 클래스를 만들어달라고 요청하세요.
// 예: "src/shopping-cart.test.ts의 테스트를 통과하도록 ShoppingCart를 구현해줘"
