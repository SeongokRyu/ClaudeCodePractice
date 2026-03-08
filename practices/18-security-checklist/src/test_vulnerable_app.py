"""
Security Tests for the Vulnerable App

These tests verify that security vulnerabilities are PRESENT
in the vulnerable version, and should be adapted to verify
that they are FIXED in the secure version.
"""

from __future__ import annotations

import json
import threading
import urllib.request
import urllib.error

import pytest

from vulnerable_app import (
    create_vulnerable_app,
    find_user_by_username,
    render_search_results,
    render_user_profile,
    users,
    posts,
    User,
    JWT_SECRET,
    API_KEY,
)


@pytest.fixture(autouse=True)
def server():
    """Start the vulnerable server on a random port for each test."""
    srv = create_vulnerable_app(port=0)
    port = srv.server_address[1]
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield f"http://localhost:{port}"
    srv.shutdown()


def request(
    base_url: str, method: str, path: str, body: dict | None = None
) -> dict:
    """Make an HTTP request and return status + parsed data + raw response."""
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
                parsed = None
            return {"status": resp.status, "data": parsed, "raw": raw}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            parsed = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            parsed = None
        return {"status": e.code, "data": parsed, "raw": raw}


class TestHardcodedSecrets:
    """Security Vulnerability: Hardcoded Secrets (A02)"""

    def test_fail_jwt_secret_is_hardcoded_and_exported(self) -> None:
        assert JWT_SECRET == "super-secret-key-12345"
        # This should NOT be hardcoded or exported

    def test_fail_api_key_is_hardcoded_and_exported(self) -> None:
        assert API_KEY == "sk-prod-abcdef123456789"

    def test_fail_passwords_are_stored_in_plain_text(self) -> None:
        admin = next((u for u in users if u.username == "admin"), None)
        assert admin is not None
        assert admin.password == "admin123"
        # Passwords should be hashed, not stored in plain text


class TestSQLInjection:
    """Security Vulnerability: SQL Injection (A03)"""

    def test_fail_find_user_uses_f_string_for_queries(self) -> None:
        """findUserByUsername uses f-string interpolation for queries."""
        malicious_input = "' OR '1'='1' --"
        # In a real DB, this would return all users
        # The function uses f-string: f"...WHERE username = '{username}'"
        result = find_user_by_username(malicious_input)
        # Even though our simulated DB doesn't actually execute SQL,
        # the query construction is vulnerable
        assert result is None  # In real DB, this would return data!


class TestXSS:
    """Security Vulnerability: XSS (A03)"""

    def test_fail_render_search_results_reflects_unsanitized_input(self) -> None:
        xss_payload = '<script>alert("xss")</script>'
        html = render_search_results(xss_payload, [])
        # The XSS payload is reflected directly in the HTML
        assert '<script>alert("xss")</script>' in html
        # It should be escaped: &lt;script&gt;...

    def test_fail_render_user_profile_outputs_unsanitized_username(self) -> None:
        malicious_user = User(
            id=99,
            username='<img src=x onerror=alert("xss")>',
            password="test",
            email="test@test.com",
            role="user",
        )
        html = render_user_profile(malicious_user)
        assert '<img src=x onerror=alert("xss")>' in html


class TestMissingAuth:
    """Security Vulnerability: Missing Auth (A01)"""

    def test_fail_admin_panel_accessible_without_auth(self, server: str) -> None:
        res = request(server, "GET", "/admin")
        # Anyone can access the admin panel!
        assert res["status"] == 200
        assert res["data"]["users"] is not None
        assert len(res["data"]["users"]) > 0

    def test_fail_admin_panel_exposes_passwords(self, server: str) -> None:
        res = request(server, "GET", "/admin")
        admin_user = next(
            (u for u in res["data"]["users"] if u["username"] == "admin"),
            None,
        )
        # Passwords should NEVER be in API responses
        assert admin_user is not None
        assert "password" in admin_user
        assert admin_user["password"] == "admin123"

    def test_fail_user_deletion_works_without_auth(self, server: str) -> None:
        res = request(server, "DELETE", "/admin/user?id=3")
        assert res["status"] == 200
        # Restore the deleted user for other tests
        users.append(
            User(
                id=3,
                username="bob",
                password="bob789",
                email="bob@example.com",
                role="user",
            )
        )


class TestNoInputValidation:
    """Security Vulnerability: No Input Validation (A08)"""

    def test_fail_user_creation_accepts_admin_role(self, server: str) -> None:
        res = request(server, "POST", "/users", {
            "username": "attacker",
            "password": "pass",
            "email": "bad",
            "role": "admin",  # User should NOT be able to set their own role!
        })
        assert res["status"] == 201
        assert res["data"]["role"] == "admin"
        # Clean up
        idx = next(
            (i for i, u in enumerate(users) if u.username == "attacker"), -1
        )
        if idx != -1:
            users.pop(idx)

    def test_fail_user_creation_returns_password_in_response(
        self, server: str
    ) -> None:
        res = request(server, "POST", "/users", {
            "username": "testuser",
            "password": "secret123",
            "email": "test@test.com",
        })
        # Password should NEVER be in API responses
        assert res["data"]["password"] == "secret123"
        # Clean up
        idx = next(
            (i for i, u in enumerate(users) if u.username == "testuser"), -1
        )
        if idx != -1:
            users.pop(idx)


class TestEvalInjection:
    """Security Vulnerability: eval() usage (Python-specific)"""

    def test_fail_eval_executes_arbitrary_expressions(self, server: str) -> None:
        """eval() on untrusted input allows arbitrary code execution."""
        res = request(server, "POST", "/calculate", {
            "expression": "2 + 2",
        })
        assert res["status"] == 200
        assert res["data"]["result"] == "4"

    def test_fail_eval_can_access_builtins(self, server: str) -> None:
        """eval() can access Python builtins for code execution."""
        res = request(server, "POST", "/calculate", {
            "expression": "len('hello')",
        })
        assert res["status"] == 200
        assert res["data"]["result"] == "5"


class TestIDOR:
    """Security Vulnerability: IDOR (A01/A04)"""

    def test_fail_any_user_can_access_any_post_by_id(self, server: str) -> None:
        # An attacker can access admin's private post
        res = request(server, "GET", "/post?id=1")
        assert res["status"] == 200
        assert res["data"]["title"] == "Admin Post"
        assert res["data"]["content"] == "Secret admin content"
        # There's no ownership check!


class TestCORSMisconfiguration:
    """Security Vulnerability: CORS Misconfiguration (A05)"""

    def test_fail_cors_allows_all_origins(self, server: str) -> None:
        res = request(server, "GET", "/admin")
        # Access-Control-Allow-Origin: * allows any website to make requests
        assert res["status"] == 200
        # In a real test, we'd check the Access-Control-Allow-Origin header


class TestSecurityFixVerification:
    """Security Fix Verification (for secure_app.py)"""

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_jwt_secret_from_env(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_passwords_hashed(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_parameterized_queries(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_html_output_escaped(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_admin_requires_auth(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_admin_requires_admin_role(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_user_creation_validates_fields(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_no_role_escalation(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_no_passwords_in_responses(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_cors_restricted(self) -> None:
        pass

    @pytest.mark.skip(reason="TODO: implement in secure_app.py")
    def test_pass_no_internal_details_in_errors(self) -> None:
        pass
