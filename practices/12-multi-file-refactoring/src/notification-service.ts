import { Notification, Callback } from './types';

// In-memory notification log
const sentNotifications: Notification[] = [];

export function sendNotification(
  userId: string,
  message: string,
  type: Notification['type'],
  callback: Callback<Notification>
): void {
  setTimeout(() => {
    const notification: Notification = {
      id: `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      userId,
      message,
      type,
      sentAt: new Date(),
    };

    sentNotifications.push(notification);
    callback(null, notification);
  }, 10);
}

export function getNotificationsByUserId(
  userId: string,
  callback: Callback<Notification[]>
): void {
  setTimeout(() => {
    const userNotifications = sentNotifications.filter(
      (n) => n.userId === userId
    );
    callback(null, userNotifications);
  }, 10);
}

export function clearNotifications(callback: Callback<void>): void {
  setTimeout(() => {
    sentNotifications.length = 0;
    callback(null);
  }, 10);
}
