# Example 1: FastAPI JWT Authentication Module

## What this shows

This example demonstrates the complete SDD workflow on a **typical FastAPI backend feature**: user authentication with JWT tokens.

- **Spec**: `docs/specs/FEAT-001-jwt-auth.md` (4KB, written first)
- **Plan**: `docs/specs/FEAT-001-plan.md` (tasks, estimates, file structure)
- **Implementation**: Full Python code in `src/` (generated from spec + plan)
- **Tests**: Unit and integration tests

## The SDD workflow

```
1. /specify "I need JWT authentication for FastAPI"
   └─ FEAT-001-jwt-auth.md created

2. /clarify
   └─ Questions refined: expiry times, refresh tokens, scope?

3. /plan FEAT-001
   └─ FEAT-001-plan.md created (4 implementation tasks, 3 hours total)

4. /implement FEAT-001
   └─ Full code generated:
      ✓ src/auth/schemas.py (Pydantic models)
      ✓ src/auth/service.py (token generation/validation)
      ✓ src/auth/dependencies.py (FastAPI dependency)
      ✓ tests/test_auth.py (unit tests)
      ✓ tests/test_auth_integration.py (integration tests)

5. /update
   └─ Status: Approved → Implemented
      CLAUDE.md updated with implementation notes
```

## How it positions your skills

- ✅ Shows you can write **clear, testable requirements**
- ✅ Demonstrates **API design thinking** (schemas, error handling)
- ✅ Proves **security awareness** (JWT best practices, token expiry)
- ✅ Shows **TDD mindset** (tests written before code)
- ✅ Proves **code quality** (type hints, docstrings, error handling)

## Files in this example

```
fastapi-auth-module/
├── README.md                          ← you are here
├── docs/
│   └── specs/
│       ├── FEAT-001-jwt-auth.md       ← spec (written first)
│       ├── FEAT-001-plan.md           ← implementation plan
│       └── CLAUDE.md                  ← project memory
├── src/
│   └── auth/
│       ├── __init__.py
│       ├── schemas.py                 ← Pydantic models
│       ├── service.py                 ← business logic
│       ├── dependencies.py            ← FastAPI integration
│       └── errors.py                  ← custom exceptions
├── tests/
│   ├── conftest.py
│   ├── test_auth_unit.py              ← unit tests
│   └── test_auth_integration.py       ← integration tests
└── requirements.txt                   ← dependencies

Key: This is a **complete, working example** you can copy into your projects.
```

## To use this as a template

```bash
# 1. Copy this entire folder into your project
cp -r examples/fastapi-auth-module/src/auth ./your-project/src/

# 2. Copy the spec and plan to learn from them
cp examples/fastapi-auth-module/docs/specs/FEAT-001-* ./your-project/docs/specs/

# 3. Adapt to your needs (different token expiry? Different scopes?)
/clarify  # Refine the spec for your use case

# 4. Regenerate code with your customizations
/implement FEAT-001

# Done. Your JWT auth is ready.
```

## What makes this impressive to hiring managers

1. **You wrote the spec first** — not reverse-engineering requirements from code
2. **Clear acceptance criteria** — they can test if it works as promised
3. **Complete test coverage** — unit + integration tests
4. **Security-conscious** — discusses token expiry, refresh tokens, scope
5. **Production-ready** — error handling, logging, type hints
