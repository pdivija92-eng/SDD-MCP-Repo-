# Implementation Plan: FEAT-002 — Django User Model with Auto-Profile

## Metadata
- **Spec**: [FEAT-002-user-model.md](./FEAT-002-user-model.md)
- **Estimated total**: 2.5 hours
- **Created**: 2024-01-10

---

## File Structure

Files to create:
- `src/users/models.py` — User and Profile models
- `src/users/signals.py` — post_save signal handlers
- `src/users/apps.py` — app config (register signals)
- `tests/test_user_model.py` — model tests
- `tests/test_user_signals.py` — signal tests

Files to modify:
- `settings.py` → add `'users'` to INSTALLED_APPS
- `requirements.txt` → add redis client

---

## Tasks

- [ ] **Task 1**: Define User model — _30 min_
  - What: Create User with email (unique), password_hash, timestamps
  - Acceptance: Can create/update/delete user; email is unique; timestamps auto-set
  - Spec refs: FR-1

- [ ] **Task 2**: Define Profile model — _30 min_
  - What: Create Profile with bio, avatar_url, last_login, FK to User
  - Acceptance: Profile creation works; on_delete=CASCADE is configured
  - Spec refs: FR-3, FR-4

- [ ] **Task 3**: Write signals — _45 min_
  - What: post_save(User) → create Profile; post_save(Profile) → invalidate cache
  - Acceptance: Profile auto-created; cache invalidation tested
  - Spec refs: FR-2, FR-5, FR-6, FR-7

- [ ] **Task 4**: Register signals in apps.py — _15 min_
  - What: Import signals in `ready()` method to avoid double registration
  - Acceptance: Signal imports don't duplicate on reload
  - Spec refs: FR-2

- [ ] **Task 5**: Write model tests — _45 min_
  - What: Test user creation, profile cascade, timestamp behavior
  - Acceptance: All model-level acceptance criteria covered
  - Spec refs: FR-1, FR-3, FR-4

- [ ] **Task 6**: Write signal tests — _30 min_
  - What: Test signal firing, cascade delete, cache invalidation
  - Acceptance: Signals fire in correct order; no N+1 queries
  - Spec refs: FR-2, FR-5, FR-6, NFR-3

---

## Test Plan

| Test | Type | Covers |
|------|------|--------|
| `test_user_creation` | unit | FR-1 |
| `test_user_email_unique` | unit | FR-1 |
| `test_user_timestamps` | unit | FR-1 |
| `test_profile_creation` | unit | FR-2 |
| `test_profile_fields` | unit | FR-3 |
| `test_cascade_delete` | unit | FR-4 |
| `test_profile_auto_created_on_user_save` | integration | FR-2 |
| `test_cache_invalidation_on_profile_update` | integration | FR-6, FR-7 |
| `test_bulk_user_creation_performance` | performance | NFR-1 |

---

## Dependencies
- Must complete before: Any endpoints that access user.profile
- Blocked by: Database migration support
- Requires: Django ORM, pytest-django, redis-py
