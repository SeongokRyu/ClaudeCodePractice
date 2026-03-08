/**
 * Vulnerable Application
 *
 * This application contains INTENTIONAL security vulnerabilities
 * for educational purposes. DO NOT use this code in production.
 *
 * Vulnerabilities included:
 * - SQL Injection (A03)
 * - XSS (A03)
 * - Hardcoded Secrets (A02)
 * - Missing Authentication (A01)
 * - No Input Validation (A08)
 * - IDOR (A04/A01)
 * - Sensitive Data in Logs (A09)
 * - Insecure CORS (A05)
 */

import http from "http";

// ============================================================
// VULNERABILITY 1: Hardcoded Secrets (A02: Cryptographic Failures)
// ============================================================
const JWT_SECRET = "super-secret-key-12345";
const DB_PASSWORD = "admin123";
const API_KEY = "sk-prod-abcdef123456789";

// ============================================================
// Simulated Database
// ============================================================
interface User {
  id: number;
  username: string;
  password: string; // VULNERABILITY: Stored in plain text (A02)
  email: string;
  role: "admin" | "user";
}

const users: User[] = [
  { id: 1, username: "admin", password: "admin123", email: "admin@example.com", role: "admin" },
  { id: 2, username: "alice", password: "alice456", email: "alice@example.com", role: "user" },
  { id: 3, username: "bob", password: "bob789", email: "bob@example.com", role: "user" },
];

interface Post {
  id: number;
  userId: number;
  title: string;
  content: string;
}

const posts: Post[] = [
  { id: 1, userId: 1, title: "Admin Post", content: "Secret admin content" },
  { id: 2, userId: 2, title: "Alice's Post", content: "Hello from Alice" },
  { id: 3, userId: 3, title: "Bob's Post", content: "Hello from Bob" },
];

// ============================================================
// VULNERABILITY 2: SQL Injection via String Templates (A03: Injection)
// ============================================================
function findUserByUsername(username: string): User | undefined {
  // Simulating a SQL query with string interpolation
  // In a real app with a real DB, this would be:
  // const query = `SELECT * FROM users WHERE username = '${username}'`;
  // An attacker could input: ' OR '1'='1' --
  const simulatedQuery = `SELECT * FROM users WHERE username = '${username}'`;
  console.log(`Executing query: ${simulatedQuery}`);

  // Simulated execution (the vulnerability is in the query construction)
  // In reality, the string template allows SQL injection
  return users.find((u) => u.username === username);
}

// ============================================================
// VULNERABILITY 3: XSS via Unsanitized Output (A03: Injection)
// ============================================================
function renderUserProfile(user: User): string {
  // User-provided data is directly embedded in HTML without escaping
  return `
    <html>
      <body>
        <h1>Profile: ${user.username}</h1>
        <p>Email: ${user.email}</p>
        <div class="bio">${user.username}'s profile page</div>
      </body>
    </html>
  `;
}

function renderSearchResults(query: string, results: Post[]): string {
  // Search query is reflected in the page without sanitization
  // XSS attack: ?q=<script>alert('xss')</script>
  return `
    <html>
      <body>
        <h1>Search Results for: ${query}</h1>
        <ul>
          ${results.map((p) => `<li>${p.title}: ${p.content}</li>`).join("")}
        </ul>
      </body>
    </html>
  `;
}

// ============================================================
// VULNERABILITY 4: Missing Authentication (A01: Broken Access Control)
// ============================================================
function handleAdminPanel(
  _req: http.IncomingMessage,
  res: http.ServerResponse
): void {
  // No authentication check! Anyone can access the admin panel
  const allUsers = users.map((u) => ({
    id: u.id,
    username: u.username,
    password: u.password, // VULNERABILITY: Exposing passwords! (A02)
    email: u.email,
    role: u.role,
  }));

  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ users: allUsers }));
}

function handleDeleteUser(
  req: http.IncomingMessage,
  res: http.ServerResponse
): void {
  // No authentication or authorization check!
  const url = new URL(req.url || "", `http://${req.headers.host}`);
  const userId = parseInt(url.searchParams.get("id") || "0", 10);

  const index = users.findIndex((u) => u.id === userId);
  if (index !== -1) {
    users.splice(index, 1);
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ message: "User deleted" }));
  } else {
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "User not found" }));
  }
}

// ============================================================
// VULNERABILITY 5: No Input Validation (A08: Data Integrity Failures)
// ============================================================
function handleCreateUser(body: string, res: http.ServerResponse): void {
  // No validation at all — accepts any input
  const data = JSON.parse(body);

  // No check for required fields
  // No check for field types
  // No check for field lengths
  // No check for malicious content
  const newUser: User = {
    id: users.length + 1,
    username: data.username, // Could be empty, null, or malicious
    password: data.password, // Stored in plain text
    email: data.email, // No email format validation
    role: data.role || "user", // User can set their own role to "admin"!
  };

  users.push(newUser);

  // VULNERABILITY 6: Sensitive data in logs (A09: Logging Failures)
  console.log(
    `New user created: ${JSON.stringify(newUser)}` // Logs password in plain text!
  );

  res.writeHead(201, { "Content-Type": "application/json" });
  res.end(JSON.stringify(newUser)); // Returns password in response!
}

// ============================================================
// VULNERABILITY 7: IDOR - Insecure Direct Object Reference (A01/A04)
// ============================================================
function handleGetPost(
  req: http.IncomingMessage,
  res: http.ServerResponse
): void {
  const url = new URL(req.url || "", `http://${req.headers.host}`);
  const postId = parseInt(url.searchParams.get("id") || "0", 10);

  // No ownership check — any user can view any post
  // An attacker can enumerate all posts by incrementing the ID
  const post = posts.find((p) => p.id === postId);

  if (post) {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(post));
  } else {
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Post not found" }));
  }
}

// ============================================================
// Server Setup
// ============================================================
export function createVulnerableApp(): http.Server {
  return http.createServer(async (req, res) => {
    // VULNERABILITY 8: Insecure CORS (A05: Security Misconfiguration)
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "*");
    res.setHeader("Access-Control-Allow-Headers", "*");

    const url = req.url || "";
    const method = req.method || "GET";

    try {
      // Routes
      if (method === "GET" && url === "/admin") {
        return handleAdminPanel(req, res);
      }

      if (method === "DELETE" && url.startsWith("/admin/user")) {
        return handleDeleteUser(req, res);
      }

      if (method === "POST" && url === "/users") {
        let body = "";
        req.on("data", (chunk) => (body += chunk));
        req.on("end", () => handleCreateUser(body, res));
        return;
      }

      if (method === "GET" && url.startsWith("/post")) {
        return handleGetPost(req, res);
      }

      if (method === "GET" && url.startsWith("/search")) {
        const searchUrl = new URL(url, `http://${req.headers.host}`);
        const query = searchUrl.searchParams.get("q") || "";
        const results = posts.filter(
          (p) =>
            p.title.includes(query) || p.content.includes(query)
        );
        const html = renderSearchResults(query, results);
        res.writeHead(200, { "Content-Type": "text/html" });
        res.end(html);
        return;
      }

      if (method === "GET" && url.startsWith("/user/")) {
        const username = url.split("/user/")[1];
        const user = findUserByUsername(decodeURIComponent(username || ""));
        if (user) {
          const html = renderUserProfile(user);
          res.writeHead(200, { "Content-Type": "text/html" });
          res.end(html);
        } else {
          res.writeHead(404, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ error: "User not found" }));
        }
        return;
      }

      // Default
      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Not found" }));
    } catch (error) {
      // VULNERABILITY: Exposing internal error details
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(
        JSON.stringify({
          error: "Internal server error",
          details: String(error), // Leaks stack trace / internal info
          dbPassword: DB_PASSWORD, // Accidentally leaks secret!
        })
      );
    }
  });
}

// Exports for testing
export {
  findUserByUsername,
  renderUserProfile,
  renderSearchResults,
  handleAdminPanel,
  users,
  posts,
  JWT_SECRET,
  API_KEY,
};
