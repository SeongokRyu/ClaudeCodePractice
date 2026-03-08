/**
 * Module C: Notification Service
 * Legacy module using callback patterns — for migration exercise.
 */

interface Notification {
  id: string;
  type: 'email' | 'sms' | 'push';
  recipient: string;
  subject: string;
  body: string;
  sentAt?: Date;
  status: 'pending' | 'sent' | 'failed';
}

interface SendResult {
  notificationId: string;
  status: 'sent' | 'failed';
  error?: string;
  retryAfter?: number;
}

type Callback<T> = (error: Error | null, result?: T) => void;

// Simulated notification queue
const notificationQueue: Notification[] = [];
const sentNotifications: Map<string, Notification> = new Map();

/**
 * Queue a notification for sending.
 * Uses callback pattern (should be migrated to async/await).
 */
export function queueNotification(
  type: Notification['type'],
  recipient: string,
  subject: string,
  body: string,
  callback: Callback<Notification>
): void {
  setTimeout(() => {
    if (!recipient || recipient.trim().length === 0) {
      callback(new Error('Recipient is required'));
      return;
    }

    const notification: Notification = {
      id: `notif-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type,
      recipient,
      subject,
      body,
      status: 'pending',
    };

    notificationQueue.push(notification);
    callback(null, notification);
  }, 50);
}

/**
 * Send a single notification.
 * Uses callback pattern with simulated network delay.
 */
export function sendNotification(
  notificationId: string,
  callback: Callback<SendResult>
): void {
  setTimeout(() => {
    const index = notificationQueue.findIndex(n => n.id === notificationId);
    if (index === -1) {
      callback(new Error(`Notification not found: ${notificationId}`));
      return;
    }

    const notification = notificationQueue[index];

    // Simulate send with 10% failure rate
    const success = Math.random() > 0.1;

    if (success) {
      notification.status = 'sent';
      notification.sentAt = new Date();
      sentNotifications.set(notification.id, notification);
      notificationQueue.splice(index, 1);

      callback(null, {
        notificationId: notification.id,
        status: 'sent',
      });
    } else {
      notification.status = 'failed';

      callback(null, {
        notificationId: notification.id,
        status: 'failed',
        error: 'Network timeout',
        retryAfter: 5000,
      });
    }
  }, 200);
}

/**
 * Send all pending notifications with retry logic.
 * Uses recursive callback pattern (callback hell).
 */
export function sendAllPending(
  maxRetries: number,
  callback: Callback<{ sent: number; failed: number }>
): void {
  const results = { sent: 0, failed: 0 };
  const pending = [...notificationQueue];
  let index = 0;

  function sendNext(): void {
    if (index >= pending.length) {
      callback(null, results);
      return;
    }

    const notification = pending[index];
    let attempts = 0;

    function attemptSend(): void {
      sendNotification(notification.id, (err, result) => {
        if (err) {
          results.failed++;
          index++;
          sendNext();
          return;
        }

        if (result!.status === 'sent') {
          results.sent++;
          index++;
          sendNext();
        } else {
          attempts++;
          if (attempts < maxRetries) {
            // Retry after delay
            setTimeout(attemptSend, result!.retryAfter || 1000);
          } else {
            results.failed++;
            index++;
            sendNext();
          }
        }
      });
    }

    attemptSend();
  }

  sendNext();
}

/**
 * Send a batch of notifications to multiple recipients.
 * Uses nested callbacks for sequential sending.
 */
export function sendBatch(
  type: Notification['type'],
  recipients: string[],
  subject: string,
  body: string,
  callback: Callback<SendResult[]>
): void {
  const results: SendResult[] = [];
  let index = 0;

  function processNext(): void {
    if (index >= recipients.length) {
      callback(null, results);
      return;
    }

    const recipient = recipients[index];
    index++;

    // Queue the notification
    queueNotification(type, recipient, subject, body, (queueErr, notification) => {
      if (queueErr) {
        results.push({
          notificationId: '',
          status: 'failed',
          error: queueErr.message,
        });
        processNext();
        return;
      }

      // Send it
      sendNotification(notification!.id, (sendErr, sendResult) => {
        if (sendErr) {
          results.push({
            notificationId: notification!.id,
            status: 'failed',
            error: sendErr.message,
          });
        } else {
          results.push(sendResult!);
        }

        processNext();
      });
    });
  }

  processNext();
}

/**
 * Get notification statistics.
 * Uses callback pattern (should be migrated to async/await).
 */
export function getStats(
  callback: Callback<{
    pending: number;
    sent: number;
    byType: Record<string, number>;
  }>
): void {
  setTimeout(() => {
    const byType: Record<string, number> = {};

    for (const n of sentNotifications.values()) {
      byType[n.type] = (byType[n.type] || 0) + 1;
    }

    callback(null, {
      pending: notificationQueue.length,
      sent: sentNotifications.size,
      byType,
    });
  }, 10);
}
