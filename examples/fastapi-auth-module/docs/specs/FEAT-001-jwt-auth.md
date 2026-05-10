# Feature Spec: FastAPI JWT Authentication Module

## Metadata
- **ID:** FEAT-001
- **Status:** Implemented
- **Author:** SDD Toolkit Example
- **Created:** 2024-01-10
- **Updated:** 2024-01-15

---

## Overview

Implement a JWT-based authentication module for FastAPI applications. This module provides token generation (login), token validation (dependency injection), token refresh, and user scope/role-based access control. Tokens are stateless; validation happens by cryptographic signature verification.

## Goals
- Provide secure, stateless authentication for FastAPI endpoints
- Support refresh tokens for long-lived sessions without storing state
- Enable role-based access control (RBAC) via token scopes
- Make authentication a one-liner: `@app.get("/protected") def protected(user = Depends(get_current_user))`
- Tokens expire to limit the impact of token compromise

## Non-Goals (Out of Scope)
- OAuth 2.0 / third-party integrations
- Multi-factor authentication (MFA)
- Session storage or blacklisting (stateless only)
- LDAP or external identity provider integration

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | User login endpoint accepts email + password, returns access + refresh tokens | Must Have |
| FR-2 | Access tokens are valid for 15 minutes by default (configurable) | Must Have |
| FR-3 | Refresh tokens are valid for 7 days by default (configurable) | Must Have |
| FR-4 | Token validation endpoint checks JWT signature and expiry | Must Have |
| FR-5 | FastAPI dependency `Depends(get_current_user)` decodes token and returns user info | Must Have |
| FR-6 | Expired tokens raise `HTTPException(status_code=401)` | Must Have |
| FR-7 | Invalid signatures raise `HTTPException(status_code=401)` | Must Have |
| FR-8 | Tokens include optional "scopes" field for role-based access | Should Have |
| FR-9 | Refresh endpoint swaps refresh token for new access token | Should Have |

### Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-1 | Token validation completes in < 5ms | Must Have |
| NFR-2 | No external dependencies beyond `fastapi`, `pydantic`, `python-jose` | Must Have |
| NFR-3 | All functions have type hints and docstrings | Must Have |
| NFR-4 | 100% test coverage of happy path + error cases | Must Have |

---

## Acceptance Criteria

- [ ] Given valid credentials, when POST /login is called, then access + refresh tokens are returned
- [ ] Given an access token, when the token is past expiry, then GET with token header returns 401
- [ ] Given an access token, when used in `Depends(get_current_user)`, then user info is decoded from the token
- [ ] Given an invalid token signature, when validation is attempted, then 401 is raised
- [ ] Given a refresh token, when POST /refresh is called, then a new access token is returned
- [ ] Given a token with scopes, when accessing a scope-protected endpoint, then access is granted if scope matches

---

## Architecture

```
POST /login                   (email, password) → {access_token, refresh_token}
     └─ validate credentials
     └─ generate JWT access token (15 min expiry)
     └─ generate JWT refresh token (7 day expiry)
     └─ return both

GET  /user                    (requires Bearer token)
     └─ Depends(get_current_user)
        └─ extract token from Authorization header
        └─ decode JWT signature (verifies authenticity)
        └─ check expiry
        └─ return user info from token payload

POST /refresh                 (refresh_token) → {access_token}
     └─ validate refresh token signature
     └─ if not expired, generate new access token
     └─ return new access token
```

## Token Payload Structure

```json
{
  "sub": "user@example.com",
  "user_id": 42,
  "exp": 1705267200,
  "iat": 1705263600,
  "scopes": ["read", "write"]
}
```

## Configuration

```python
# .env or pydantic settings
SECRET_KEY = "your-secret-key-min-32-chars"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
```

---

## Design Notes

- **Stateless**: No database lookups during token validation (only signature check)
- **Fast**: Token validation is O(1) — pure cryptography, no I/O
- **Secure**: Tokens are signed with a secret; expiry is in the token itself
- **Extensible**: Scopes field enables fine-grained RBAC without database changes
- **FastAPI-native**: Uses `Depends()` for clean, testable dependency injection

## Error Handling

| Scenario | HTTP Status | Error |
|----------|-------------|-------|
| Missing Authorization header | 401 | `Unauthorized: Token missing` |
| Expired token | 401 | `Unauthorized: Token expired` |
| Invalid signature | 401 | `Unauthorized: Invalid token` |
| Malformed token | 401 | `Unauthorized: Invalid token format` |
| Wrong algorithm | 401 | `Unauthorized: Invalid token` |

---

## Security Considerations

- Secret key must be at least 32 characters, random, and never hardcoded
- Tokens should be sent over HTTPS only
- Access tokens are short-lived to limit exposure of compromised tokens
- Refresh tokens must be stored securely (HttpOnly cookie, not localStorage)
- Token payload is visible (base64) — never store passwords or sensitive data in tokens

---

## Open Questions

- [ ] Should we support refresh token rotation (issue new refresh on each use)?
- [ ] Should we store a token blacklist for logout?
- [ ] Should we support multiple auth methods (API keys, OAuth)?
