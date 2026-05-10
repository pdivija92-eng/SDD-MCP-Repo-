# Implementation Plan: FEAT-001 — FastAPI JWT Authentication

## Metadata
- **Spec**: [FEAT-001-jwt-auth.md](./FEAT-001-jwt-auth.md)
- **Estimated total**: 3 hours
- **Created**: 2024-01-10

---

## File Structure

Files to create:
- `src/auth/__init__.py` — module exports
- `src/auth/schemas.py` — Pydantic models (TokenRequest, TokenResponse, UserInfo)
- `src/auth/service.py` — business logic (token generation, validation)
- `src/auth/dependencies.py` — FastAPI Depends() compatible functions
- `src/auth/errors.py` — custom exceptions
- `src/auth/config.py` — settings from environment
- `tests/conftest.py` — pytest fixtures
- `tests/test_auth_unit.py` — unit tests for auth logic
- `tests/test_auth_integration.py` — FastAPI integration tests

---

## Tasks (in order)

- [ ] **Task 1**: Define Pydantic schemas — _30 min_
  - What: Create `schemas.py` with TokenRequest, TokenResponse, UserPayload, UserInfo
  - Acceptance: Schema validation works for valid/invalid inputs
  - Spec refs: FR-1

- [ ] **Task 2**: Implement token service — _1 hr_
  - What: Create `service.py` with `create_access_token()`, `create_refresh_token()`, `validate_token()`
  - Acceptance: Tokens are created correctly; expired tokens raise ValueError; signatures are verified
  - Spec refs: FR-2, FR-3, FR-4, NFR-1

- [ ] **Task 3**: Create FastAPI dependencies — _45 min_
  - What: Create `dependencies.py` with `get_current_user`, `get_current_user_with_scope`
  - Acceptance: Can be used in `Depends()` syntax; returns user info; raises HTTPException on invalid token
  - Spec refs: FR-5, FR-6, FR-7, FR-8

- [ ] **Task 4**: Create config and errors — _15 min_
  - What: Create `config.py` (settings), `errors.py` (custom exceptions), `__init__.py` (exports)
  - Acceptance: Imports work cleanly; settings load from environment
  - Spec refs: FR-1

- [ ] **Task 5**: Write unit tests — _1 hr_
  - What: Create `tests/test_auth_unit.py` with tests for each function
  - Acceptance: Tests cover happy path, expiry, invalid signatures, malformed tokens
  - Spec refs: All FR, NFR-4

- [ ] **Task 6**: Write integration tests — _45 min_
  - What: Create `tests/test_auth_integration.py` with FastAPI TestClient
  - Acceptance: Test /login, /refresh, protected endpoints with valid/invalid tokens
  - Spec refs: FR-1, FR-9, all error cases

---

## Test Plan

| Test | Type | Covers |
|------|------|--------|
| `test_create_access_token` | unit | FR-2, token payload structure |
| `test_token_expiry` | unit | FR-2, tokens expire correctly |
| `test_validate_token_success` | unit | FR-4, valid tokens are accepted |
| `test_validate_token_expired` | unit | FR-6, expired tokens raise error |
| `test_validate_token_invalid_signature` | unit | FR-7, tampered tokens are rejected |
| `test_get_current_user_dependency` | unit | FR-5, dependency returns user info |
| `test_scope_validation` | unit | FR-8, scope checking works |
| `test_login_endpoint` | integration | FR-1, POST /login returns tokens |
| `test_protected_endpoint_success` | integration | FR-5, valid token grants access |
| `test_protected_endpoint_expired_token` | integration | FR-6, expired tokens denied |
| `test_refresh_endpoint` | integration | FR-9, refresh produces new access token |
| `test_missing_authorization_header` | integration | FR-6, missing token returns 401 |

---

## Dependencies

- Must complete: None (this is foundational)
- Blocked by: None
- Requires: `fastapi`, `pydantic`, `python-jose`

---

## Implementation Notes

- Use `HS256` (HMAC with SHA-256) for signing; it's simple and standard
- Store SECRET_KEY in environment; never hardcode
- Use `datetime.utcnow()` consistently (or `datetime.now(timezone.utc)` in Python 3.11+)
- `python-jose` library handles all JWT operations; don't implement JWT manually
- Token validation is O(1) — only signature check + expiry check, no database
