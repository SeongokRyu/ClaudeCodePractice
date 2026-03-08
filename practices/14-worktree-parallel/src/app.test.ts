import http from "http";
import { createApp } from "./app";

let server: http.Server;
let baseUrl: string;

function request(
  method: string,
  path: string,
  body?: object
): Promise<{ status: number; data: any }> {
  return new Promise((resolve, reject) => {
    const url = new URL(path, baseUrl);
    const options: http.RequestOptions = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
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
            data: data ? JSON.parse(data) : null,
          });
        } catch {
          resolve({ status: res.statusCode || 500, data });
        }
      });
    });

    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

beforeAll((done) => {
  server = createApp();
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

describe("Health Check", () => {
  it("should return health status", async () => {
    const res = await request("GET", "/health");
    expect(res.status).toBe(200);
    expect(res.data.status).toBe("ok");
    expect(res.data.uptime).toBeGreaterThanOrEqual(0);
  });
});

describe("Users API", () => {
  it("should list all users", async () => {
    const res = await request("GET", "/users");
    expect(res.status).toBe(200);
    expect(Array.isArray(res.data)).toBe(true);
    expect(res.data.length).toBeGreaterThanOrEqual(2);
  });

  it("should get a user by id", async () => {
    const res = await request("GET", "/users/1");
    expect(res.status).toBe(200);
    expect(res.data.name).toBe("Alice");
    expect(res.data.email).toBe("alice@example.com");
  });

  it("should return 404 for non-existent user", async () => {
    const res = await request("GET", "/users/999");
    expect(res.status).toBe(404);
  });

  it("should create a new user", async () => {
    const res = await request("POST", "/users", {
      name: "Charlie",
      email: "charlie@example.com",
    });
    expect(res.status).toBe(201);
    expect(res.data.name).toBe("Charlie");
    expect(res.data.id).toBeDefined();
  });

  it("should return 400 for invalid create request", async () => {
    const res = await request("POST", "/users", { name: "NoEmail" });
    expect(res.status).toBe(400);
  });

  it("should return 404 for unknown routes", async () => {
    const res = await request("GET", "/unknown");
    expect(res.status).toBe(404);
  });
});
