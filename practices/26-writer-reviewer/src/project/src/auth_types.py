"""Shared types for the authentication module."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: str
    email: str
    password_hash: str
    created_at: datetime


@dataclass
class AuthToken:
    token: str
    user_id: str
    expires_at: datetime


@dataclass
class LoginResult:
    success: bool
    token: Optional[str] = None
    error: Optional[str] = None


@dataclass
class TokenValidation:
    valid: bool
    user_id: Optional[str] = None
    error: Optional[str] = None
