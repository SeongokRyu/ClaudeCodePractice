# Simple REST-like module for subagent practice
# This module provides a basic API structure that agents can work with

import re
import time
import random
import string
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class User:
    id: str
    name: str
    email: str


@dataclass
class ApiRequest:
    method: str  # 'GET', 'POST', 'PUT', 'DELETE'
    path: str
    body: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None


@dataclass
class ApiResponse:
    status: int
    body: Any
    headers: Optional[Dict[str, str]] = None


# In-memory store
_users: Dict[str, User] = {}


def _generate_id() -> str:
    random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
    return f"user_{int(time.time() * 1000)}_{random_suffix}"


def handle_request(request: ApiRequest) -> ApiResponse:
    """Route handler."""
    method = request.method
    path = request.path

    # GET /users
    if method == "GET" and path == "/users":
        return ApiResponse(
            status=200,
            body=list({"id": u.id, "name": u.name, "email": u.email} for u in _users.values()),
        )

    # GET /users/:id
    get_user_match = re.match(r"^/users/([^/]+)$", path)
    if method == "GET" and get_user_match:
        user_id = get_user_match.group(1)
        user = _users.get(user_id)
        if not user:
            return ApiResponse(status=404, body={"error": "User not found"})
        return ApiResponse(
            status=200,
            body={"id": user.id, "name": user.name, "email": user.email},
        )

    # POST /users
    if method == "POST" and path == "/users":
        if not request.body or not request.body.get("name") or not request.body.get("email"):
            return ApiResponse(
                status=400, body={"error": "Name and email are required"}
            )

        new_user = User(
            id=_generate_id(),
            name=request.body["name"],
            email=request.body["email"],
        )

        _users[new_user.id] = new_user
        return ApiResponse(
            status=201,
            body={"id": new_user.id, "name": new_user.name, "email": new_user.email},
        )

    # PUT /users/:id
    put_user_match = re.match(r"^/users/([^/]+)$", path)
    if method == "PUT" and put_user_match:
        user_id = put_user_match.group(1)
        existing = _users.get(user_id)
        if not existing:
            return ApiResponse(status=404, body={"error": "User not found"})

        updated = User(
            id=existing.id,
            name=request.body.get("name", existing.name) if request.body else existing.name,
            email=request.body.get("email", existing.email) if request.body else existing.email,
        )

        _users[user_id] = updated
        return ApiResponse(
            status=200,
            body={"id": updated.id, "name": updated.name, "email": updated.email},
        )

    # DELETE /users/:id
    delete_user_match = re.match(r"^/users/([^/]+)$", path)
    if method == "DELETE" and delete_user_match:
        user_id = delete_user_match.group(1)
        if user_id not in _users:
            return ApiResponse(status=404, body={"error": "User not found"})

        del _users[user_id]
        return ApiResponse(status=204, body=None)

    return ApiResponse(status=404, body={"error": "Route not found"})


def reset_store() -> None:
    """Helper to reset state (useful for testing)."""
    _users.clear()
