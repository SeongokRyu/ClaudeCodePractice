import { Order, OrderItem, Callback } from './types';
import * as db from './database';

const COLLECTION = 'orders';

export function initOrderRepo(callback: Callback<void>): void {
  db.initCollection(COLLECTION, callback);
}

export function createOrder(
  userId: string,
  items: OrderItem[],
  callback: Callback<Order>
): void {
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const order: Order = {
    id: `order_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    userId,
    items,
    total,
    status: 'pending',
    createdAt: new Date(),
  };

  db.insert(COLLECTION, order.id, order, (error, result) => {
    if (error) {
      callback(error);
      return;
    }
    callback(null, result as Order);
  });
}

export function getOrderById(
  orderId: string,
  callback: Callback<Order>
): void {
  db.findById(COLLECTION, orderId, (error, result) => {
    if (error) {
      callback(error);
      return;
    }
    callback(null, result as Order);
  });
}

export function getOrdersByUserId(
  userId: string,
  callback: Callback<Order[]>
): void {
  db.findAll(COLLECTION, (error, results) => {
    if (error) {
      callback(error);
      return;
    }
    const userOrders = (results as Order[]).filter((o) => o.userId === userId);
    callback(null, userOrders);
  });
}

export function updateOrderStatus(
  orderId: string,
  status: Order['status'],
  callback: Callback<Order>
): void {
  db.update(COLLECTION, orderId, { status }, (error, result) => {
    if (error) {
      callback(error);
      return;
    }
    callback(null, result as Order);
  });
}
