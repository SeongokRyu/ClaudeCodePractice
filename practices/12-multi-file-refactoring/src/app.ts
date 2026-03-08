import { User, Order, OrderItem, Notification, Callback } from './types';
import * as userRepo from './user-repository';
import * as orderRepo from './order-repository';
import * as notificationService from './notification-service';

export function initApp(callback: Callback<void>): void {
  userRepo.initUserRepo((error) => {
    if (error) {
      callback(error);
      return;
    }
    orderRepo.initOrderRepo((error2) => {
      if (error2) {
        callback(error2);
        return;
      }
      callback(null);
    });
  });
}

// Create a user and send a welcome notification — classic callback chain
export function registerUser(
  name: string,
  email: string,
  callback: Callback<{ user: User; notification: Notification }>
): void {
  userRepo.createUser(name, email, (error, user) => {
    if (error) {
      callback(error);
      return;
    }

    notificationService.sendNotification(
      user!.id,
      `Welcome, ${user!.name}!`,
      'email',
      (error2, notification) => {
        if (error2) {
          callback(error2);
          return;
        }
        callback(null, { user: user!, notification: notification! });
      }
    );
  });
}

// Place an order and notify the user — deeper callback chain
export function placeOrder(
  userId: string,
  items: OrderItem[],
  callback: Callback<{ order: Order; notification: Notification }>
): void {
  // First verify the user exists
  userRepo.getUserById(userId, (error, user) => {
    if (error) {
      callback(error);
      return;
    }

    // Then create the order
    orderRepo.createOrder(userId, items, (error2, order) => {
      if (error2) {
        callback(error2);
        return;
      }

      // Then send notification
      notificationService.sendNotification(
        userId,
        `Order ${order!.id} placed successfully. Total: ${order!.total}`,
        'email',
        (error3, notification) => {
          if (error3) {
            callback(error3);
            return;
          }
          callback(null, { order: order!, notification: notification! });
        }
      );
    });
  });
}

// Get user dashboard data — parallel-ish callbacks (but done sequentially)
export function getUserDashboard(
  userId: string,
  callback: Callback<{
    user: User;
    orders: Order[];
    notifications: Notification[];
  }>
): void {
  userRepo.getUserById(userId, (error, user) => {
    if (error) {
      callback(error);
      return;
    }

    orderRepo.getOrdersByUserId(userId, (error2, orders) => {
      if (error2) {
        callback(error2);
        return;
      }

      notificationService.getNotificationsByUserId(
        userId,
        (error3, notifications) => {
          if (error3) {
            callback(error3);
            return;
          }

          callback(null, {
            user: user!,
            orders: orders!,
            notifications: notifications!,
          });
        }
      );
    });
  });
}
