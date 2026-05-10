"""
Token generation and validation service.

Spec: FEAT-001
Handles JWT creation with configurable expiry and cryptographic validation.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from jose import JWTError, jwt
from .schemas import UserPayload, UserInfo


# ── Configuration (read from environment) ─────────────────────────────────────

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-min-32-chars-long!!!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


# ── Custom Exceptions ─────────────────────────────────────────────────────────

class TokenError(Exception):
    """Base exception for token-related errors."""
    pass


class InvalidTokenError(TokenError):
    """Token signature is invalid."""
    pass


class ExpiredTokenError(TokenError):
    """Token has expired."""
    pass


# ── Service Functions ─────────────────────────────────────────────────────────

def create_access_token(
    subject: str,
    user_id: int,
    scopes: list[str] | None = None,
    expires_delta: timedelta | None = None,
) -> tuple[str, int]:
    """
    Generate a JWT access token.

    Args:
        subject: Typically the user's email (goes in 'sub' claim)
        user_id: Numeric user ID
        scopes: Optional list of permission scopes (e.g., ['read', 'write'])
        expires_delta: Custom expiry time; uses default if None

    Returns:
        (token_string, expires_in_seconds)

    Spec: FR-2 — Access tokens valid for 15 minutes by default
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    now = datetime.now(timezone.utc)
    expires = now + expires_delta

    payload = {
        "sub": subject,
        "user_id": user_id,
        "iat": int(now.timestamp()),
        "exp": int(expires.timestamp()),
        "scopes": scopes or [],
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, int(expires_delta.total_seconds())


def create_refresh_token(
    subject: str,
    user_id: int,
    expires_delta: timedelta | None = None,
) -> tuple[str, int]:
    """
    Generate a JWT refresh token.

    Args:
        subject: User's email
        user_id: Numeric user ID
        expires_delta: Custom expiry; uses default 7 days if None

    Returns:
        (token_string, expires_in_seconds)

    Spec: FR-3 — Refresh tokens valid for 7 days by default
    """
    if expires_delta is None:
        expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    now = datetime.now(timezone.utc)
    expires = now + expires_delta

    payload = {
        "sub": subject,
        "user_id": user_id,
        "iat": int(now.timestamp()),
        "exp": int(expires.timestamp()),
        "type": "refresh",
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, int(expires_delta.total_seconds())


def validate_token(token: str) -> UserPayload:
    """
    Validate a JWT token and return its decoded payload.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        InvalidTokenError: Signature is invalid or token is malformed
        ExpiredTokenError: Token has expired

    Spec: FR-4 — Token validation checks JWT signature and expiry
    Spec: NFR-1 — Validation completes in < 5ms (pure crypto, O(1))
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return UserPayload(**payload)
    except JWTError as e:
        if "expired" in str(e).lower():
            raise ExpiredTokenError("Token has expired") from e
        raise InvalidTokenError(f"Invalid token: {e}") from e


def extract_user_info(payload: UserPayload) -> UserInfo:
    """
    Convert token payload to user info (strip exp, iat, type).

    Spec: FR-5 — Extract user info for Depends()
    """
    return UserInfo(
        email=payload.sub,
        user_id=payload.user_id,
        scopes=payload.scopes,
    )
