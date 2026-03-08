# Specialist Team Prompt

Create a specialist team to implement a user dashboard feature:

## Teammates

### 1. UX Specialist
Focus on component structure, styling, and user experience.
Working directory: `src/project/frontend/src/`

Tasks:
- Design the dashboard layout
- Create DashboardView component
- Create DashboardWidget component
- Add loading states and error handling in the UI
- Ensure responsive design

### 2. Backend Specialist
Focus on API design, data models, and business logic.
Working directory: `src/project/backend/src/`

Tasks:
- Design the dashboard data model
- Create `GET /api/dashboard` endpoint
- Create `GET /api/dashboard/widgets` endpoint
- Add proper error responses and validation
- Implement data aggregation logic

### 3. Testing Specialist
Focus on test coverage, edge cases, and integration.
Working directory: `src/project/tests/`

Tasks:
- Write unit tests for dashboard API endpoints
- Write component tests for DashboardView
- Write integration test for the full dashboard flow
- Test error states and edge cases
- Verify API response contracts

## Shared Task List
- [ ] Design dashboard data model
- [ ] Create GET /api/dashboard endpoint
- [ ] Create GET /api/dashboard/widgets endpoint
- [ ] Create DashboardView component
- [ ] Create DashboardWidget component
- [ ] Add loading and error states
- [ ] Write API unit tests
- [ ] Write component tests
- [ ] Write integration tests
- [ ] Final review and cleanup
