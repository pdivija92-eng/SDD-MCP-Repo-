# Feature Spec: Django User Model with Auto-Profile Creation

## Metadata
- **ID:** FEAT-002
- **Status:** Implemented
- **Author:** SDD Toolkit Example
- **Created:** 2024-01-10
- **Updated:** 2024-01-15

---

## Overview

Create a Django User model with automatic profile creation via post-save signal. When a user is created, a Profile object is instantly available. When a user logs in, their profile's `last_login` is updated. When a user is deleted, their profile cascades. Profile data is cached in Redis for fast API lookups.

## Goals
- User model with email as unique identifier (not username)
- Auto-create Profile on user creation (no "profile does not exist" errors)
- Track user login timestamps in Profile
- Cache Profile in Redis to avoid N+1 queries in APIs
- Handle cascade deletion correctly

## Non-Goals (Out of Scope)
- Multi-tenancy or organization scoping
- Social auth integrations
- Profile image storage
- Soft deletes

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | User model has email (unique), password, created_at, updated_at | Must Have |
| FR-2 | Profile model auto-created on user creation | Must Have |
| FR-3 | Profile has fields: bio, avatar_url, last_login, updated_at | Must Have |
| FR-4 | Deleting a User deletes its Profile | Must Have |
| FR-5 | User login updates Profile.last_login | Should Have |
| FR-6 | Profile is cached in Redis with 1-hour TTL | Should Have |
| FR-7 | Cache is invalidated on Profile save | Should Have |

### Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-1 | Model creation (<1s single-threaded) | Must Have |
| NFR-2 | Cache lookups complete in <5ms | Should Have |
| NFR-3 | Signals don't create N+1 queries | Should Have |

---

## Acceptance Criteria

- [ ] Given a new User, when saved, then a Profile is created in same transaction
- [ ] Given a User with a Profile, when deleted, then Profile is also deleted
- [ ] Given a Profile, when saved, then Redis cache is invalidated
- [ ] Given a User with a cached Profile, when Profile updated, then cache reflects change
- [ ] Given 1000 users, when they login, then signal processing < 100ms

---

## Database Schema

```sql
-- User table
CREATE TABLE users_user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(254) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Profile table
CREATE TABLE users_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users_user(id) ON DELETE CASCADE,
    bio TEXT,
    avatar_url VARCHAR(500),
    last_login TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_profile_user_id ON users_profile(user_id);
```

## Signal Flow

```
1. User.objects.create(email="alice@example.com", password="...")
   └─ pre_save signal (validation)
   └─ save() → INSERT into users_user
   └─ post_save signal → auto-create Profile
      └─ Profile.objects.create(user_id=1)
      └─ pre_save signal
      └─ save() → INSERT into users_profile
      └─ post_save signal → cache_set("profile:1", {...})

2. user.save()  # update
   └─ post_save signal
   └─ cache_invalidate("profile:{user_id}")
```

---

## Design Notes

- Signals are registered in `apps.py` ready_signal to avoid double registration
- Cache key is `profile:{user_id}` with 1-hour TTL
- Profile is created in same transaction as User (atomicity)
- Cascade is handled by database foreign key, not Django signal
- last_login signal only fires if explicitly set during login flow

---

## Security Considerations

- Password is always hashed (not stored plain)
- Profile.bio and avatar_url are user-controlled (XSS considerations for display)
- Cache expiry prevents stale data affecting authorization
