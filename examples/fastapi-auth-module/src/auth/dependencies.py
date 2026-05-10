"""
FastAPI dependencies for JWT authentication.

Use in your routes with Depends():
    @app.get("/user")
    async def get_user(user = Depends(get_current_user)):
        return user

Spec: FEAT-001 FR-5 — FastAPI dependency Depends(get_current_user)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from .service import validate_token, extract_user_info, InvalidTokenError, ExpiredTokenError
from .schemas import UserInfo


# Use FastAPI's HTTPBearer scheme for automatic Swagger documentation
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> UserInfo:
    """
    FastAPI dependency that validates token and returns user info.

    Usage:
        @app.get("/protected")
        async def protected(user = Depends(get_current_user)):
            return {"user": user}

    Raises:
        HTTPException(401) if token is missing, expired, or invalid

    Spec: FR-5 — Token validation endpoint
    Spec: FR-6, FR-7 — Expired/invalid tokens raise 401
    """
    token = credentials.credentials
    try:
        payload = validate_token(token)
        user_info = extract_user_info(payload)
        return user_info
    except ExpiredTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_with_scope(required_scopes: list[str]):
    """
    Factory for scope-protected endpoints.

    Usage:
        @app.get("/admin")
        async def admin_only(user = Depends(get_current_user_with_scope(["admin"]))):
            return {"data": "secret"}

    Spec: FR-8 — Role-based access control via scopes
    """
    async def scope_verifier(user: UserInfo = Depends(get_current_user)) -> UserInfo:
        if not any(scope in user.scopes for scope in required_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user
    return scope_verifier
