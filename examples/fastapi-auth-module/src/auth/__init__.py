"""
Auth module exports.

Usage:
    from auth import create_access_token, get_current_user, TokenResponse
"""

from .schemas import (
    TokenRequest,
    TokenResponse,
    UserInfo,
    RefreshTokenRequest,
)
from .service import (
    create_access_token,
    create_refresh_token,
    validate_token,
    TokenError,
    InvalidTokenError,
    ExpiredTokenError,
)
from .dependencies import (
    get_current_user,
    get_current_user_with_scope,
)
from .errors import (
    AuthError,
    InvalidCredentialsError,
    UserNotFoundError,
)

__all__ = [
    # Schemas
    "TokenRequest",
    "TokenResponse",
    "UserInfo",
    "RefreshTokenRequest",
    # Service
    "create_access_token",
    "create_refresh_token",
    "validate_token",
    "TokenError",
    "InvalidTokenError",
    "ExpiredTokenError",
    # Dependencies
    "get_current_user",
    "get_current_user_with_scope",
    # Errors
    "AuthError",
    "InvalidCredentialsError",
    "UserNotFoundError",
]
