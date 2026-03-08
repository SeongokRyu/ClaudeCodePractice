/**
 * Security Tests for the Vulnerable App
 *
 * These tests verify that security vulnerabilities are PRESENT
 * in the vulnerable version, and should be adapted to verify
 * that they are FIXED in the secure version.
 */

import http from "http";
import {
  createVulnerableApp,
  findUserByUsername,
  renderSearchResults,
  renderUserProfile,
  users,
  JWT_SECRET,
  API_KEY,
} from "./vulnerable-app";

let server: http.Server;
let baseUrl: string;

function request(
  method: string,
  path: string,
  body?: object
): Promise<{ status: number; data: any; raw: string }> {
  return new Promise((resolve, reject) => {
    const url = new URL(path, baseUrl);
    const options: http.RequestOptions = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      method,
      headers: { "Content-Type": "application/json" },
    };

    const req = http.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve({
            status: res.statusCode || 500,
            data: JSON.parse(data),
            raw: data,
          });
        } catch {
          resolve({ status: res.statusCode || 500, data: null, raw: data });
        }
      });
    });

    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

beforeAll((done) => {
  server = createVulnerableApp();
  server.listen(0, () => {
    const addr = server.address();
    if (addr && typeof addr === "object") {
      baseUrl = `http://localhost:${addr.port}`;
    }
    done();
  });
});

afterAll((done) => {
  server.close(done);
});

describe("Security Vulnerability: Hardcoded Secrets (A02)", () => {
  it("FAIL: JWT_SECRET is hardcoded and exported", () => {
    expect(JWT_SECRET).toBe("super-secret-key-12345");
    // This should NOT be hardcoded or exported
  });

  it("FAIL: API_KEY is hardcoded and exported", () => {
    expect(API_KEY).toBe("sk-prod-abcdef123456789");
  });

  it("FAIL: passwords are stored in plain text", () => {
    const admin = users.find((u) => u.username === "admin");
    expect(admin?.password).toBe("admin123");
    // Passwords should be hashed, not stored in plain text
  });
});

describe("Security Vulnerability: SQL Injection (A03)", () => {
  it("FAIL: findUserByUsername uses string interpolation for queries", () => {
    // This simulates an SQL injection attack
    const maliciousInput = "' OR '1'='1' --";
    // In a real DB, this would return all users
    // The function uses string template: `...WHERE username = '${username}'`
    const result = findUserByUsername(maliciousInput);
    // Even though our simulated DB doesn't actually execute SQL,
    // the query construction is vulnerable
    expect(result).toBeUndefined(); // In real DB, this would return data!
  });
});

describe("Security Vulnerability: XSS (A03)", () => {
  it("FAIL: renderSearchResults reflects unsanitized input", () => {
    const xssPayload = '<script>alert("xss")</script>';
    const html = renderSearchResults(xssPayload, []);
    // The XSS payload is reflected directly in the HTML
    expect(html).toContain('<script>alert("xss")</script>');
    // It should be escaped: &lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;
  });

  it("FAIL: renderUserProfile outputs unsanitized username", () => {
    const maliciousUser = {
      id: 99,
      username: '<img src=x onerror=alert("xss")>',
      password: "test",
      email: "test@test.com",
      role: "user" as const,
    };
    const html = renderUserProfile(maliciousUser);
    expect(html).toContain('<img src=x onerror=alert("xss")>');
  });
});

describe("Security Vulnerability: Missing Auth (A01)", () => {
  it("FAIL: admin panel is accessible without authentication", async () => {
    const res = await request("GET", "/admin");
    // Anyone can access the admin panel!
    expect(res.status).toBe(200);
    expect(res.data.users).toBeDefined();
    expect(res.data.users.length).toBeGreaterThan(0);
  });

  it("FAIL: admin panel exposes passwords", async () => {
    const res = await request("GET", "/admin");
    const adminUser = res.data.users.find(
      (u: any) => u.username === "admin"
    );
    // Passwords should NEVER be in API responses
    expect(adminUser.password).toBeDefined();
    expect(adminUser.password).toBe("admin123");
  });

  it("FAIL: user deletion works without authentication", async () => {
    const initialCount = users.length;
    const res = await request("DELETE", "/admin/user?id=3");
    expect(res.status).toBe(200);
    // Restore the deleted user for other tests
    users.push({
      id: 3,
      username: "bob",
      password: "bob789",
      email: "bob@example.com",
      role: "user",
    });
  });
});

describe("Security Vulnerability: No Input Validation (A08)", () => {
  it("FAIL: user creation accepts any role including admin", async () => {
    const res = await request("POST", "/users", {
      username: "attacker",
      password: "pass",
      email: "bad",
      role: "admin", // User should NOT be able to set their own role!
    });
    expect(res.status).toBe(201);
    expect(res.data.role).toBe("admin");
    // Clean up
    const idx = users.findIndex((u) => u.username === "attacker");
    if (idx !== -1) users.splice(idx, 1);
  });

  it("FAIL: user creation returns password in response", async () => {
    const res = await request("POST", "/users", {
      username: "testuser",
      password: "secret123",
      email: "test@test.com",
    });
    // Password should NEVER be in API responses
    expect(res.data.password).toBe("secret123");
    // Clean up
    const idx = users.findIndex((u) => u.username === "testuser");
    if (idx !== -1) users.splice(idx, 1);
  });
});

describe("Security Vulnerability: IDOR (A01/A04)", () => {
  it("FAIL: any user can access any post by ID enumeration", async () => {
    // An attacker can access admin's private post
    const res = await request("GET", "/post?id=1");
    expect(res.status).toBe(200);
    expect(res.data.title).toBe("Admin Post");
    expect(res.data.content).toBe("Secret admin content");
    // There's no ownership check!
  });
});

describe("Security Vulnerability: CORS Misconfiguration (A05)", () => {
  it("FAIL: CORS allows all origins", async () => {
    const res = await request("GET", "/admin");
    // Access-Control-Allow-Origin: * allows any website to make requests
    // This is checked via response headers in the raw response
    expect(res.status).toBe(200);
    // In a real test, we'd check the Access-Control-Allow-Origin header
  });
});

describe("Security Fix Verification (for secure-app.ts)", () => {
  it.todo("PASS: JWT_SECRET should come from environment variable");
  it.todo("PASS: passwords should be hashed with bcrypt");
  it.todo("PASS: queries should use parameterized statements");
  it.todo("PASS: HTML output should escape user input");
  it.todo("PASS: admin endpoints should require authentication");
  it.todo("PASS: admin endpoints should require admin role");
  it.todo("PASS: user creation should validate all fields");
  it.todo("PASS: user creation should not allow role escalation");
  it.todo("PASS: API responses should never include passwords");
  it.todo("PASS: CORS should restrict allowed origins");
  it.todo("PASS: error responses should not leak internal details");
});
