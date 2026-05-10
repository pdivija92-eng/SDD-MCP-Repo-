# Example 2: Django ORM User Model with Signal Handlers

## What this shows

Using SDD for a **typical Django backend feature**: building a User model with post-save signals that auto-create a profile and sync to cache.

Shows:
- How SDD works for **Django projects** (not just APIs)
- How to specify **database constraints** and **Django signals**
- How specifications improve code review on complex interactions

## The workflow

```
Spec: FEAT-002-user-model.md
  ├─ User model with email/password
  ├─ Auto-create profile on user creation
  ├─ Update profile last_login on each login
  ├─ Sync to Redis cache for fast lookups
  ├─ Cascade delete signals

Plan: FEAT-002-plan.md
  ├─ Task 1: Create models (User, Profile)
  ├─ Task 2: Create signals.py
  ├─ Task 3: Register signals in apps.py
  ├─ Task 4: Add tests

Implementation:
  ├─ src/users/models.py
  ├─ src/users/signals.py
  ├─ src/users/apps.py
  ├─ tests/test_user_model.py
  └─ tests/test_user_signals.py
```

## Why this matters for your skills

- ✅ Shows you understand **database design** (constraints, indices)
- ✅ Proves **Django expertise** (signals, model lifecycle)
- ✅ Demonstrates **testing complex interactions** (signals + cache)
- ✅ Shows **ops thinking** (cache invalidation, cascade behavior)
- ✅ Proves specs catch real issues (signal ordering, race conditions)

## Files

```
django-orm-task/
├── README.md
├── docs/specs/
│   ├── FEAT-002-user-model.md
│   ├── FEAT-002-plan.md
│   └── CLAUDE.md
├── src/users/
│   ├── models.py
│   ├── signals.py
│   ├── apps.py
│   └── __init__.py
└── tests/
    ├── test_user_model.py
    └── test_user_signals.py
```

## Key insight

SDD isn't just for APIs. It works for:
- Database schema design
- Signal/event handling
- Cache invalidation logic
- Celery tasks
- CLI commands

Any feature complex enough to need thought → gets a spec first.
