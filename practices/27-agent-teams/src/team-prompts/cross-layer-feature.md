# Cross-Layer Feature Prompt

Implement a real-time notifications feature that spans frontend, backend, and testing.

## Feature Requirements
Users should receive real-time notifications when:
- A task is assigned to them
- A task they're watching is updated
- A comment is added to their task

## Teammates

### 1. Backend Developer
Working directory: `src/project/backend/src/`

Implement:
- Notification data model (id, userId, type, message, read, createdAt)
- `POST /api/notifications` — create a notification
- `GET /api/notifications/:userId` — get user's notifications
- `PATCH /api/notifications/:id/read` — mark as read
- `GET /api/notifications/:userId/unread-count` — get unread count
- WebSocket or SSE endpoint for real-time delivery

### 2. Frontend Developer
Working directory: `src/project/frontend/src/`

Implement:
- NotificationBell component (shows unread count badge)
- NotificationList component (dropdown list of notifications)
- NotificationItem component (individual notification)
- Real-time connection (WebSocket/SSE client)
- Mark-as-read on click
- Toast notification for new items

### 3. Test Engineer
Working directory: `src/project/tests/`

Implement:
- Unit tests for notification API endpoints
- Component tests for NotificationBell, NotificationList
- Integration test: create notification → appears in UI
- Test real-time delivery
- Test mark-as-read flow
- Test edge cases: empty state, many notifications, rapid updates

## Coordination Points
- Backend must define the API contract FIRST
- Frontend depends on the API contract
- Tester can start writing test scaffolds while waiting
- All should agree on the notification data shape

## Shared Task List
- [ ] Define notification data model and API contract
- [ ] Implement notification CRUD endpoints
- [ ] Implement real-time delivery (WebSocket/SSE)
- [ ] Create NotificationBell component
- [ ] Create NotificationList component
- [ ] Connect frontend to real-time endpoint
- [ ] Write API unit tests
- [ ] Write component tests
- [ ] Write integration tests
- [ ] End-to-end verification
