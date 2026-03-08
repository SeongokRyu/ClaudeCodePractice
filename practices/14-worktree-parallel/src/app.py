"""
Simple REST API application using Flask-style routing (pure Python).

A lightweight HTTP server with in-memory user storage for practicing
parallel development with git worktrees.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, asdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional


# --- Types ---
@dataclass
class User:
    id: int
    name: str
    email: str


# --- In-memory data ---
users: list[User] = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com"),
]

next_id: int = 3
_start_time: float = time.time()


# --- Helpers ---
def send_json(handler: BaseHTTPRequestHandler, status_code: int, data: object) -> None:
    """Send a JSON response with the given status code."""
    body = json.dumps(data).encode("utf-8")
    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(body)


def not_found(handler: BaseHTTPRequestHandler) -> None:
    """Send a 404 Not Found response."""
    send_json(handler, 404, {"error": "Not found"})


# --- Route handlers ---
def get_users(handler: BaseHTTPRequestHandler, body: Optional[str] = None) -> None:
    send_json(handler, 200, [asdict(u) for u in users])


def get_user_by_id(handler: BaseHTTPRequestHandler, body: Optional[str] = None) -> None:
    path = handler.path or ""
    match = re.match(r"^/users/(\d+)$", path)
    if not match:
        return not_found(handler)

    user_id = int(match.group(1))
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        return not_found(handler)

    send_json(handler, 200, asdict(user))


def create_user(handler: BaseHTTPRequestHandler, body: Optional[str] = None) -> None:
    global next_id

    if not body:
        return send_json(handler, 400, {"error": "Request body is required"})

    try:
        data = json.loads(body)
        name = data.get("name")
        email = data.get("email")
        if not name or not email:
            return send_json(handler, 400, {"error": "name and email are required"})

        new_user = User(id=next_id, name=name, email=email)
        next_id += 1
        users.append(new_user)
        send_json(handler, 201, asdict(new_user))
    except json.JSONDecodeError:
        send_json(handler, 400, {"error": "Invalid JSON"})


def delete_user(handler: BaseHTTPRequestHandler, body: Optional[str] = None) -> None:
    path = handler.path or ""
    match = re.match(r"^/users/(\d+)$", path)
    if not match:
        return not_found(handler)

    user_id = int(match.group(1))
    index = next((i for i, u in enumerate(users) if u.id == user_id), -1)
    if index == -1:
        return not_found(handler)

    users.pop(index)
    send_json(handler, 204, None)


def get_health(handler: BaseHTTPRequestHandler, body: Optional[str] = None) -> None:
    uptime = time.time() - _start_time
    send_json(handler, 200, {"status": "ok", "uptime": uptime})


# --- Router ---
@dataclass
class Route:
    method: str
    path: str
    handler: object  # callable


routes: list[Route] = [
    Route(method="GET", path="/health", handler=get_health),
    Route(method="GET", path="/users", handler=get_users),
    Route(method="GET", path="/users/:id", handler=get_user_by_id),
    Route(method="POST", path="/users", handler=create_user),
    Route(method="DELETE", path="/users/:id", handler=delete_user),
]


def match_route(method: str, url: str) -> Optional[Route]:
    """Find the first route matching the given method and URL."""
    for route in routes:
        if route.method != method:
            continue

        if ":id" in route.path:
            pattern = route.path.replace(":id", r"\d+")
            if re.match(f"^{pattern}$", url):
                return route
        else:
            if route.path == url:
                return route

    return None


# --- Request Handler ---
class AppRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the app."""

    def do_GET(self) -> None:
        self._handle_request("GET")

    def do_POST(self) -> None:
        self._handle_request("POST")

    def do_PUT(self) -> None:
        self._handle_request("PUT")

    def do_PATCH(self) -> None:
        self._handle_request("PATCH")

    def do_DELETE(self) -> None:
        self._handle_request("DELETE")

    def _handle_request(self, method: str) -> None:
        url = self.path or "/"
        route = match_route(method, url)
        if not route:
            return not_found(self)

        if method in ("POST", "PUT", "PATCH"):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length else ""
            route.handler(self, body)
        else:
            route.handler(self)

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default logging."""
        pass


def create_app(port: int = 0) -> HTTPServer:
    """Create and return an HTTPServer instance."""
    server = HTTPServer(("localhost", port), AppRequestHandler)
    return server


# --- Start server ---
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 3000))
    server = create_app(port)
    print(f"Server running on http://localhost:{port}")
    server.serve_forever()
