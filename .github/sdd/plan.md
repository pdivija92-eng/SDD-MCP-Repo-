# /plan

Break an approved spec into ordered, estimable implementation tasks with a clear file structure.

## Instructions for Claude

When the user runs `/plan FEAT-XXX`:

1. Read `docs/specs/FEAT-XXX-*.md` — if status is not `Approved`, warn the user
2. Read `docs/specs/CLAUDE.md` for tech stack and conventions
3. Generate `docs/specs/FEAT-XXX-plan.md` using the plan template below
4. Print a short summary of the plan to chat

## Plan template

```markdown
# Implementation Plan: FEAT-XXX — [Feature Name]

## Metadata
- **Spec**: [FEAT-XXX-name.md](./FEAT-XXX-name.md)
- **Estimated total**: X hours
- **Created**: YYYY-MM-DD

---

## File structure

Files to create:
- `src/<module>/base.py` — base class / interface
- `src/<module>/<impl>.py` — implementation
- `tests/test_<module>.py` — unit tests

Files to modify:
- `src/__init__.py` — add export

---

## Tasks (in order)

- [ ] **Task 1**: [name] — _[estimate]_
  - What: [one line description]
  - Acceptance: [how to verify it's done]
  - Spec refs: FR-1, NFR-1

- [ ] **Task 2**: [name] — _[estimate]_
  - What: 
  - Acceptance: 
  - Spec refs: 

---

## Test plan

| Test | Type | Covers |
|------|------|--------|
| test_happy_path | unit | FR-1, FR-2 |
| test_invalid_input | unit | FR-3 |
| test_performance | integration | NFR-1 |

---

## Dependencies
- Must complete before: [other FEAT-XXX if any]
- Blocked by: [nothing / list blockers]
```

## Planning principles Claude follows

- Tasks are ordered so each one is buildable on its own
- Base classes and interfaces come before implementations
- Tests are written as a task, not an afterthought
- Each task maps to at least one spec requirement (FR-X or NFR-X)
- Estimates are realistic: "write tests" is always at least 1 hour
