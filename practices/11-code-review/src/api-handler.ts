// API Handler — intentionally contains multiple security and quality issues
// This code is for practice purposes. DO NOT use in production!

// BUG: Hardcoded API key
const API_KEY = 'sk-secret-api-key-12345-do-not-share';
const DB_PASSWORD = 'admin123';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

interface ApiResponse {
  success: boolean;
  data?: any;
  error?: string;
}

// Simulated database
const users: User[] = [
  { id: 1, name: 'Alice', email: 'alice@example.com', role: 'admin' },
  { id: 2, name: 'Bob', email: 'bob@example.com', role: 'user' },
  { id: 3, name: 'Charlie', email: 'charlie@example.com', role: 'user' },
];

// BUG: No input validation, SQL-injection-like string interpolation
export function searchUsers(query: string): ApiResponse {
  // Simulating SQL-injection-vulnerable query building
  const sqlQuery = `SELECT * FROM users WHERE name LIKE '%${query}%'`;
  console.log(`Executing query: ${sqlQuery}`);

  // Actually just filter in memory, but the SQL string is still dangerous if logged/sent
  const results = users.filter(
    (u) => u.name.toLowerCase().includes(query.toLowerCase())
  );

  return {
    success: true,
    data: results,
  };
}

// BUG: No authentication check, returns sensitive data
export function getUserById(id: number): ApiResponse {
  const user = users.find((u) => u.id === id);

  if (!user) {
    // BUG: Leaking internal information in error message
    return {
      success: false,
      error: `User not found in database table 'users' at index ${id}. DB connection: ${DB_PASSWORD}`,
    };
  }

  return {
    success: true,
    data: user,
  };
}

// BUG: No input validation, no error handling
export function createUser(name: string, email: string): ApiResponse {
  // No validation of name or email
  // No check for duplicate emails
  // No sanitization

  const newUser: User = {
    id: users.length + 1, // BUG: ID collision if users are deleted
    name: name,
    email: email,
    role: 'user',
  };

  users.push(newUser);

  // BUG: Logging sensitive data
  console.log(`Created user: ${JSON.stringify(newUser)}`);

  return {
    success: true,
    data: newUser,
  };
}

// BUG: No authorization check — any user can delete any user
export function deleteUser(userId: number): ApiResponse {
  const index = users.findIndex((u) => u.id === userId);

  if (index === -1) {
    return { success: false, error: 'User not found' };
  }

  // No check if the requester has permission to delete
  const deleted = users.splice(index, 1);

  return {
    success: true,
    data: deleted[0],
  };
}

// BUG: Hardcoded API key used directly, no rate limiting
export function callExternalApi(endpoint: string, data: any): ApiResponse {
  // Using hardcoded API key
  const headers = {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
  };

  // No timeout setting
  // No retry logic
  // No rate limiting
  console.log(`Calling ${endpoint} with headers: ${JSON.stringify(headers)}`);

  // Simulated response
  return {
    success: true,
    data: { message: 'External API call simulated' },
  };
}

// BUG: Generic catch-all that swallows errors
export function processRequest(action: string, params: any): ApiResponse {
  try {
    switch (action) {
      case 'search':
        return searchUsers(params.query);
      case 'get':
        return getUserById(params.id);
      case 'create':
        return createUser(params.name, params.email);
      case 'delete':
        return deleteUser(params.id);
      case 'external':
        return callExternalApi(params.endpoint, params.data);
      default:
        return { success: false, error: 'Unknown action' };
    }
  } catch (e) {
    // BUG: Swallowing error details, not logging properly
    return { success: false, error: 'Something went wrong' };
  }
}
