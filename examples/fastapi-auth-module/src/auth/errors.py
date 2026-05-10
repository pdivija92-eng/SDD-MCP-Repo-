"""
Custom exceptions for authentication module.

Spec: FEAT-001 — Error handling
"""


class AuthError(Exception):
    """Base exception for authentication errors."""
    pass


class InvalidCredentialsError(AuthError):
    """Username or password is incorrect."""
    pass


class UserNotFoundError(AuthError):
    """User with given email does not exist."""
    pass
