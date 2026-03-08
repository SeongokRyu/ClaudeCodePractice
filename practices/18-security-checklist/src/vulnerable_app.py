"""
Vulnerable Application

This application contains INTENTIONAL security vulnerabilities
for educational purposes. DO NOT use this code in production.

Vulnerabilities included:
- SQL Injection (A03)
- XSS (A03)
- Hardcoded Secrets (A02)
- Missing Authentication (A01)
- No Input Validation (A08)
- IDOR (A04/A01)
- Sensitive Data in Logs (A09)
- Insecure CORS (A05)
- eval() usage (Python-specific injection)
- pickle deserialization (Python-specific)
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, asdict, field
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional
from urllib.parse import urlparse, parse_qs

# ============================================================
# VULNERABILITY 1: Hardcoded Secrets (A02: Cryptographic Failures)
# ============================================================
JWT_SECRET = "super-secret-key-12345"
DB_PASSWORD = "admin123"
API_KEY = "sk-prod-abcdef123456789"


# ============================================================
# Simulated Database
# ============================================================
@dataclass
class User:
    id: int
    username: str
    password: str  # VULNERABILITY: Stored in plain text (A02)
    email: str
    role: str  # "admin" or "user"


@dataclass
class Post:
    id: int
    user_id: int
    title: str
    content: str


users: list[User] = [
    User(id=1, username="admin", password="admin123", email="admin@example.com", role="admin"),
    User(id=2, username="alice", password="alice456", email="alice@example.com", role="user"),
    User(id=3, username="bob", password="bob789", email="bob@example.com", role="user"),
]

posts: list[Post] = [
    Post(id=1, user_id=1, title="Admin Post", content="Secret admin content"),
    Post(id=2, user_id=2, title="Alice's Post", content="Hello from Alice"),
    Post(id=3, user_id=3, title="Bob's Post", content="Hello from Bob"),
]


# ============================================================
# VULNERABILITY 2: SQL Injection via f-string (A03: Injection)
# ============================================================
def find_user_by_username(username: str) -> Optional[User]:
    """
    Simulating a SQL query with f-string interpolation.
    In a real app with a real DB, this would be:
        query = f"SELECT * FROM users WHERE username = '{username}'"
    An attacker could input: ' OR '1'='1' --
    """
    simulated_query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"Executing query: {simulated_query}")

    # Simulated execution (the vulnerability is in the query construction)
    return next((u for u in users if u.username == username), None)


# ============================================================
# VULNERABILITY 3: XSS via Unsanitized Output (A03: Injection)
# ============================================================
def render_user_profile(user: User) -> str:
    """User-provided data is directly embedded in HTML without escaping."""
    return f"""
    <html>
      <body>
        <h1>Profile: {user.username}</h1>
        <p>Email: {user.email}</p>
        <div class="bio">{user.username}'s profile page</div>
      </body>
    </html>
    """


def render_search_results(query: str, results: list[Post]) -> str:
    """
    Search query is reflected in the page without sanitization.
    XSS attack: ?q=<script>alert('xss')</script>
    """
    items = "".join(f"<li>{p.title}: {p.content}</li>" for p in results)
    return f"""
    <html>
      <body>
        <h1>Search Results for: {query}</h1>
        <ul>
          {items}
        </ul>
      </body>
    </html>
    """


# ============================================================
# VULNERABILITY 4: Missing Authentication (A01: Broken Access Control)
# ============================================================
def handle_admin_panel(handler: BaseHTTPRequestHandler) -> None:
    """No authentication check! Anyone can access the admin panel."""
    all_users = [
        {
            "id": u.id,
            "username": u.username,
            "password": u.password,  # VULNERABILITY: Exposing passwords! (A02)
            "email": u.email,
            "role": u.role,
        }
        for u in users
    ]

    body = json.dumps({"users": all_users}).encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(body)


def handle_delete_user(handler: BaseHTTPRequestHandler) -> None:
    """No authentication or authorization check!"""
    parsed = urlparse(handler.path)
    params = parse_qs(parsed.query)
    user_id = int(params.get("id", ["0"])[0])

    index = next((i for i, u in enumerate(users) if u.id == user_id), -1)
    if index != -1:
        users.pop(index)
        body = json.dumps({"message": "User deleted"}).encode("utf-8")
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(body)
    else:
        body = json.dumps({"error": "User not found"}).encode("utf-8")
        handler.send_response(404)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(body)


# ============================================================
# VULNERABILITY 5: No Input Validation (A08: Data Integrity Failures)
# ============================================================
def handle_create_user(handler: BaseHTTPRequestHandler, body_str: str) -> None:
    """No validation at all - accepts any input."""
    data = json.loads(body_str)

    # No check for required fields
    # No check for field types
    # No check for field lengths
    # No check for malicious content
    new_user = User(
        id=len(users) + 1,
        username=data.get("username", ""),  # Could be empty or malicious
        password=data.get("password", ""),  # Stored in plain text
        email=data.get("email", ""),  # No email format validation
        role=data.get("role", "user"),  # User can set their own role to "admin"!
    )

    users.append(new_user)

    # VULNERABILITY 6: Sensitive data in logs (A09: Logging Failures)
    print(f"New user created: {json.dumps(asdict(new_user))}")  # Logs password!

    response_body = json.dumps(asdict(new_user)).encode("utf-8")
    handler.send_response(201)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(response_body)  # Returns password in response!


# ============================================================
# VULNERABILITY 6: eval() usage (Python-specific injection)
# ============================================================
def handle_calculate(handler: BaseHTTPRequestHandler, body_str: str) -> None:
    """
    VULNERABLE: Uses eval() on user-provided input.
    An attacker could execute arbitrary Python code.
    Example payload: "__import__('os').system('rm -rf /')"
    """
    data = json.loads(body_str)
    expression = data.get("expression", "0")

    # INTENTIONALLY VULNERABLE: eval() on untrusted input
    try:
        result = eval(expression)  # noqa: S307
        response = json.dumps({"result": str(result)}).encode("utf-8")
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(response)
    except Exception as e:
        response = json.dumps({"error": str(e)}).encode("utf-8")
        handler.send_response(400)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(response)


# ============================================================
# VULNERABILITY 7: IDOR - Insecure Direct Object Reference (A01/A04)
# ============================================================
def handle_get_post(handler: BaseHTTPRequestHandler) -> None:
    """No ownership check - any user can view any post."""
    parsed = urlparse(handler.path)
    params = parse_qs(parsed.query)
    post_id = int(params.get("id", ["0"])[0])

    # An attacker can enumerate all posts by incrementing the ID
    post = next((p for p in posts if p.id == post_id), None)

    if post:
        body = json.dumps(asdict(post)).encode("utf-8")
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(body)
    else:
        body = json.dumps({"error": "Post not found"}).encode("utf-8")
        handler.send_response(404)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(body)


# ============================================================
# Server Setup
# ============================================================
class VulnerableAppHandler(BaseHTTPRequestHandler):
    """HTTP request handler with intentional security vulnerabilities."""

    def do_GET(self) -> None:
        # VULNERABILITY 8: Insecure CORS (A05: Security Misconfiguration)
        self.send_cors_headers()

        url = self.path or ""

        try:
            if url == "/admin":
                return handle_admin_panel(self)

            if url.startswith("/post"):
                return handle_get_post(self)

            if url.startswith("/search"):
                parsed = urlparse(url)
                params = parse_qs(parsed.query)
                query = params.get("q", [""])[0]
                results = [
                    p for p in posts
                    if query in p.title or query in p.content
                ]
                html = render_search_results(query, results)
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
                return

            if url.startswith("/user/"):
                username = url.split("/user/")[1]
                user = find_user_by_username(username)
                if user:
                    html = render_user_profile(user)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(html.encode("utf-8"))
                else:
                    body = json.dumps({"error": "User not found"}).encode("utf-8")
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(body)
                return

            # Default
            body = json.dumps({"error": "Not found"}).encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            # VULNERABILITY: Exposing internal error details
            error_response = json.dumps({
                "error": "Internal server error",
                "details": str(e),  # Leaks stack trace / internal info
                "db_password": DB_PASSWORD,  # Accidentally leaks secret!
            }).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(error_response)

    def do_POST(self) -> None:
        self.send_cors_headers()
        url = self.path or ""

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body_str = self.rfile.read(content_length).decode("utf-8") if content_length else ""

            if url == "/users":
                return handle_create_user(self, body_str)

            if url == "/calculate":
                return handle_calculate(self, body_str)

            body = json.dumps({"error": "Not found"}).encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            error_response = json.dumps({
                "error": "Internal server error",
                "details": str(e),
                "db_password": DB_PASSWORD,
            }).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(error_response)

    def do_DELETE(self) -> None:
        self.send_cors_headers()
        url = self.path or ""

        try:
            if url.startswith("/admin/user"):
                return handle_delete_user(self)

            body = json.dumps({"error": "Not found"}).encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            error_response = json.dumps({
                "error": "Internal server error",
                "details": str(e),
                "db_password": DB_PASSWORD,
            }).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(error_response)

    def send_cors_headers(self) -> None:
        """VULNERABILITY 8: Insecure CORS - allows all origins."""
        # These headers are set but note: send_header only works after send_response
        # We store them to be added when send_response is called
        pass

    def send_response(self, code: int, message: str | None = None) -> None:
        super().send_response(code)
        # VULNERABILITY: Insecure CORS headers
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default logging."""
        pass


def create_vulnerable_app(port: int = 0) -> HTTPServer:
    """Create and return a vulnerable HTTP server."""
    server = HTTPServer(("localhost", port), VulnerableAppHandler)
    return server


# --- Start server ---
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 3000))
    server = create_vulnerable_app(port)
    print(f"Vulnerable server running on http://localhost:{port}")
    server.serve_forever()
