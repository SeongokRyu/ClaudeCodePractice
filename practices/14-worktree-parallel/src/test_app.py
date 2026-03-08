"""
Tests for the REST API application.
"""

import json
import threading
import urllib.request
import urllib.error

import pytest

from app import create_app, users, User


@pytest.fixture(autouse=True)
def server():
    """Start the server on a random port before each test, stop after."""
    srv = create_app(port=0)
    port = srv.server_address[1]
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield f"http://localhost:{port}"
    srv.shutdown()


def request(base_url: str, method: str, path: str, body: dict | None = None) -> dict:
    """Make an HTTP request and return status + parsed JSON data."""
    url = f"{base_url}{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            try:
                parsed = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                parsed = raw
            return {"status": resp.status, "data": parsed}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            parsed = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            parsed = raw
        return {"status": e.code, "data": parsed}


# --- Health Check ---
class TestHealthCheck:
    def test_should_return_health_status(self, server: str) -> None:
        res = request(server, "GET", "/health")
        assert res["status"] == 200
        assert res["data"]["status"] == "ok"
        assert res["data"]["uptime"] >= 0


# --- Users API ---
class TestUsersAPI:
    def test_should_list_all_users(self, server: str) -> None:
        res = request(server, "GET", "/users")
        assert res["status"] == 200
        assert isinstance(res["data"], list)
        assert len(res["data"]) >= 2

    def test_should_get_a_user_by_id(self, server: str) -> None:
        res = request(server, "GET", "/users/1")
        assert res["status"] == 200
        assert res["data"]["name"] == "Alice"
        assert res["data"]["email"] == "alice@example.com"

    def test_should_return_404_for_non_existent_user(self, server: str) -> None:
        res = request(server, "GET", "/users/999")
        assert res["status"] == 404

    def test_should_create_a_new_user(self, server: str) -> None:
        res = request(server, "POST", "/users", {
            "name": "Charlie",
            "email": "charlie@example.com",
        })
        assert res["status"] == 201
        assert res["data"]["name"] == "Charlie"
        assert "id" in res["data"]

    def test_should_return_400_for_invalid_create_request(self, server: str) -> None:
        res = request(server, "POST", "/users", {"name": "NoEmail"})
        assert res["status"] == 400

    def test_should_return_404_for_unknown_routes(self, server: str) -> None:
        res = request(server, "GET", "/unknown")
        assert res["status"] == 404
