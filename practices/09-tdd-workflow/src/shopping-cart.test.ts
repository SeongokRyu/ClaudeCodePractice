import { ShoppingCartImpl } from './shopping-cart';

describe('ShoppingCart', () => {
  let cart: ShoppingCartImpl;

  beforeEach(() => {
    cart = new ShoppingCartImpl();
  });

  describe('addItem', () => {
    it('should add a new item to the cart', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 });
      const items = cart.getItems();
      expect(items).toHaveLength(1);
      expect(items[0]).toEqual({
        id: '1',
        name: 'Apple',
        price: 1000,
        quantity: 1,
      });
    });

    it('should add item with specified quantity', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 3);
      const items = cart.getItems();
      expect(items[0].quantity).toBe(3);
    });

    it('should increase quantity when adding existing item', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 2);
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 3);
      const items = cart.getItems();
      expect(items).toHaveLength(1);
      expect(items[0].quantity).toBe(5);
    });

    it('should throw error for zero or negative quantity', () => {
      expect(() => {
        cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 0);
      }).toThrow();
      expect(() => {
        cart.addItem({ id: '1', name: 'Apple', price: 1000 }, -1);
      }).toThrow();
    });

    it('should throw error for negative price', () => {
      expect(() => {
        cart.addItem({ id: '1', name: 'Apple', price: -100 });
      }).toThrow();
    });
  });

  describe('removeItem', () => {
    it('should remove an item from the cart', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 });
      cart.addItem({ id: '2', name: 'Banana', price: 2000 });
      cart.removeItem('1');
      const items = cart.getItems();
      expect(items).toHaveLength(1);
      expect(items[0].id).toBe('2');
    });

    it('should throw error when removing non-existent item', () => {
      expect(() => {
        cart.removeItem('non-existent');
      }).toThrow();
    });

    it('should handle removing from empty cart', () => {
      expect(() => {
        cart.removeItem('1');
      }).toThrow();
    });
  });

  describe('getTotal', () => {
    it('should return 0 for empty cart', () => {
      expect(cart.getTotal()).toBe(0);
    });

    it('should calculate total correctly', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 2);
      cart.addItem({ id: '2', name: 'Banana', price: 1500 }, 3);
      expect(cart.getTotal()).toBe(2000 + 4500);
    });

    it('should update total after removing item', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 2);
      cart.addItem({ id: '2', name: 'Banana', price: 1500 }, 1);
      cart.removeItem('2');
      expect(cart.getTotal()).toBe(2000);
    });
  });

  describe('applyDiscount', () => {
    it('should apply percentage discount', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 10);
      const discounted = cart.applyDiscount(10);
      expect(discounted).toBe(9000);
    });

    it('should apply 0% discount (no change)', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 5);
      const discounted = cart.applyDiscount(0);
      expect(discounted).toBe(5000);
    });

    it('should apply 100% discount', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 5);
      const discounted = cart.applyDiscount(100);
      expect(discounted).toBe(0);
    });

    it('should throw error for discount > 100%', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 });
      expect(() => {
        cart.applyDiscount(101);
      }).toThrow();
    });

    it('should throw error for negative discount', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 });
      expect(() => {
        cart.applyDiscount(-10);
      }).toThrow();
    });

    it('should return 0 for empty cart regardless of discount', () => {
      const discounted = cart.applyDiscount(50);
      expect(discounted).toBe(0);
    });
  });

  describe('clearCart', () => {
    it('should remove all items', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 });
      cart.addItem({ id: '2', name: 'Banana', price: 2000 });
      cart.clearCart();
      expect(cart.getItems()).toHaveLength(0);
      expect(cart.getTotal()).toBe(0);
    });

    it('should handle clearing empty cart', () => {
      cart.clearCart();
      expect(cart.getItems()).toHaveLength(0);
    });
  });

  describe('getItemCount', () => {
    it('should return 0 for empty cart', () => {
      expect(cart.getItemCount()).toBe(0);
    });

    it('should return total quantity of all items', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 3);
      cart.addItem({ id: '2', name: 'Banana', price: 2000 }, 2);
      expect(cart.getItemCount()).toBe(5);
    });

    it('should update count after operations', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 }, 3);
      cart.addItem({ id: '2', name: 'Banana', price: 2000 }, 2);
      cart.removeItem('1');
      expect(cart.getItemCount()).toBe(2);
      cart.clearCart();
      expect(cart.getItemCount()).toBe(0);
    });
  });

  describe('immutability', () => {
    it('should return a copy of items, not the internal array', () => {
      cart.addItem({ id: '1', name: 'Apple', price: 1000 });
      const items = cart.getItems();
      items.push({ id: '2', name: 'Hack', price: 0, quantity: 1 });
      expect(cart.getItems()).toHaveLength(1);
    });
  });
});
