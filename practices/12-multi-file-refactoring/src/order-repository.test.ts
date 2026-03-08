import * as db from './database';
import * as userRepo from './user-repository';
import * as orderRepo from './order-repository';
import { OrderItem } from './types';

describe('OrderRepository', () => {
  let testUserId: string;

  const sampleItems: OrderItem[] = [
    { productId: 'p1', name: 'Widget', price: 1000, quantity: 2 },
    { productId: 'p2', name: 'Gadget', price: 2500, quantity: 1 },
  ];

  beforeEach((done) => {
    db.clearAll(() => {
      userRepo.initUserRepo(() => {
        orderRepo.initOrderRepo(() => {
          userRepo.createUser('Alice', 'alice@example.com', (error, user) => {
            if (error) return done(error);
            testUserId = user!.id;
            done();
          });
        });
      });
    });
  });

  describe('createOrder', () => {
    it('should create an order with calculated total', (done) => {
      orderRepo.createOrder(testUserId, sampleItems, (error, order) => {
        expect(error).toBeNull();
        expect(order).toBeDefined();
        expect(order!.userId).toBe(testUserId);
        expect(order!.items).toHaveLength(2);
        expect(order!.total).toBe(4500); // 1000*2 + 2500*1
        expect(order!.status).toBe('pending');
        done();
      });
    });
  });

  describe('getOrderById', () => {
    it('should retrieve an order by ID', (done) => {
      orderRepo.createOrder(testUserId, sampleItems, (error, order) => {
        expect(error).toBeNull();
        orderRepo.getOrderById(order!.id, (error2, found) => {
          expect(error2).toBeNull();
          expect(found!.id).toBe(order!.id);
          expect(found!.total).toBe(4500);
          done();
        });
      });
    });
  });

  describe('getOrdersByUserId', () => {
    it('should return orders for a specific user', (done) => {
      orderRepo.createOrder(testUserId, sampleItems, () => {
        orderRepo.createOrder(
          testUserId,
          [{ productId: 'p3', name: 'Doohickey', price: 500, quantity: 3 }],
          () => {
            orderRepo.getOrdersByUserId(testUserId, (error, orders) => {
              expect(error).toBeNull();
              expect(orders).toHaveLength(2);
              done();
            });
          }
        );
      });
    });

    it('should return empty array for user with no orders', (done) => {
      orderRepo.getOrdersByUserId('other-user', (error, orders) => {
        expect(error).toBeNull();
        expect(orders).toHaveLength(0);
        done();
      });
    });
  });

  describe('updateOrderStatus', () => {
    it('should update order status', (done) => {
      orderRepo.createOrder(testUserId, sampleItems, (error, order) => {
        expect(error).toBeNull();
        orderRepo.updateOrderStatus(order!.id, 'confirmed', (error2, updated) => {
          expect(error2).toBeNull();
          expect(updated!.status).toBe('confirmed');
          done();
        });
      });
    });
  });
});
