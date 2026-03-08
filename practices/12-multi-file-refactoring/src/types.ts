export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

export interface Order {
  id: string;
  userId: string;
  items: OrderItem[];
  total: number;
  status: 'pending' | 'confirmed' | 'shipped' | 'delivered';
  createdAt: Date;
}

export interface OrderItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
}

export interface Notification {
  id: string;
  userId: string;
  message: string;
  type: 'email' | 'sms' | 'push';
  sentAt: Date;
}

export type Callback<T> = (error: Error | null, result?: T) => void;
