"""
JWT Authentication Module for FastAPI.

Spec: FEAT-001 (docs/specs/FEAT-001-jwt-auth.md)
Plan: docs/specs/FEAT-001-plan.md
Status: Implemented 2024-01-15
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ── Request/Response Schemas ──────────────────────────────────────────────────

class TokenRequest(BaseModel):
    """Login endpoint request. Spec: FR-1."""
    email: EmailStr
    password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    """Login endpoint response. Spec: FR-1."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class UserPayload(BaseModel):
    """Decoded JWT token payload. Spec: FR-4."""
    sub: str  # typically email
    user_id: int
    exp: int  # Unix timestamp
    iat: int  # Unix timestamp
    scopes: list[str] = Field(default_factory=list)


class UserInfo(BaseModel):
    """User information decoded from token. Spec: FR-5."""
    email: str
    user_id: int
    scopes: list[str] = Field(default_factory=list)


class RefreshTokenRequest(BaseModel):
    """Refresh endpoint request. Spec: FR-9."""
    refresh_token: str
