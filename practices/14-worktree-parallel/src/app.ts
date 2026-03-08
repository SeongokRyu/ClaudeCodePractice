import http from "http";

// --- Types ---
interface User {
  id: number;
  name: string;
  email: string;
}

interface Route {
  method: string;
  path: string;
  handler: (req: http.IncomingMessage, res: http.ServerResponse, body?: string) => void;
}

// --- In-memory data ---
const users: User[] = [
  { id: 1, name: "Alice", email: "alice@example.com" },
  { id: 2, name: "Bob", email: "bob@example.com" },
];

let nextId = 3;

// --- Helpers ---
function parseBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", () => resolve(body));
    req.on("error", reject);
  });
}

function sendJson(res: http.ServerResponse, statusCode: number, data: unknown): void {
  res.writeHead(statusCode, { "Content-Type": "application/json" });
  res.end(JSON.stringify(data));
}

function notFound(res: http.ServerResponse): void {
  sendJson(res, 404, { error: "Not found" });
}

// --- Route handlers ---
function getUsers(_req: http.IncomingMessage, res: http.ServerResponse): void {
  sendJson(res, 200, users);
}

function getUserById(req: http.IncomingMessage, res: http.ServerResponse): void {
  const url = req.url || "";
  const match = url.match(/^\/users\/(\d+)$/);
  if (!match) return notFound(res);

  const id = parseInt(match[1], 10);
  const user = users.find((u) => u.id === id);
  if (!user) return notFound(res);

  sendJson(res, 200, user);
}

function createUser(_req: http.IncomingMessage, res: http.ServerResponse, body?: string): void {
  if (!body) {
    return sendJson(res, 400, { error: "Request body is required" });
  }

  try {
    const { name, email } = JSON.parse(body);
    if (!name || !email) {
      return sendJson(res, 400, { error: "name and email are required" });
    }

    const newUser: User = { id: nextId++, name, email };
    users.push(newUser);
    sendJson(res, 201, newUser);
  } catch {
    sendJson(res, 400, { error: "Invalid JSON" });
  }
}

function deleteUser(req: http.IncomingMessage, res: http.ServerResponse): void {
  const url = req.url || "";
  const match = url.match(/^\/users\/(\d+)$/);
  if (!match) return notFound(res);

  const id = parseInt(match[1], 10);
  const index = users.findIndex((u) => u.id === id);
  if (index === -1) return notFound(res);

  users.splice(index, 1);
  sendJson(res, 204, null);
}

function getHealth(_req: http.IncomingMessage, res: http.ServerResponse): void {
  sendJson(res, 200, { status: "ok", uptime: process.uptime() });
}

// --- Router ---
const routes: Route[] = [
  { method: "GET", path: "/health", handler: getHealth },
  { method: "GET", path: "/users", handler: getUsers },
  { method: "GET", path: "/users/:id", handler: getUserById },
  { method: "POST", path: "/users", handler: createUser },
  { method: "DELETE", path: "/users/:id", handler: deleteUser },
];

function matchRoute(method: string, url: string): Route | undefined {
  return routes.find((route) => {
    if (route.method !== method) return false;

    if (route.path.includes(":id")) {
      const pattern = route.path.replace(":id", "\\d+");
      return new RegExp(`^${pattern}$`).test(url);
    }

    return route.path === url;
  });
}

// --- Server ---
export async function handleRequest(
  req: http.IncomingMessage,
  res: http.ServerResponse
): Promise<void> {
  const method = req.method || "GET";
  const url = req.url || "/";

  const route = matchRoute(method, url);
  if (!route) {
    return notFound(res);
  }

  if (method === "POST" || method === "PUT" || method === "PATCH") {
    const body = await parseBody(req);
    route.handler(req, res, body);
  } else {
    route.handler(req, res);
  }
}

export function createApp(): http.Server {
  return http.createServer(handleRequest);
}

// --- Start server ---
if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  const server = createApp();
  server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

// --- Exports for testing ---
export { users, User, sendJson, notFound, matchRoute };
