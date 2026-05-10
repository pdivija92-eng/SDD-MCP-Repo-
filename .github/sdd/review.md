# /review

**Usage**: `/review FEAT-XXX` or `/review PR-#`

Perform an AI-assisted review that compares implementation or pull request changes against the related SDD spec.

## Instructions for the assistant

1. Read the feature spec: `docs/specs/FEAT-XXX-*.md`
2. Read the implementation plan: `docs/specs/FEAT-XXX-plan.md` if present
3. Inspect the PR diff or local code changes
4. Check whether:
   - Code changes match functional requirements
   - Acceptance criteria are satisfied
   - Tests cover the expected behavior
   - Security, reliability, or maintainability risks were introduced
   - Implementation deviates from the approved plan
5. Generate a review report at `reviews/FEAT-XXX-review.md`

## Review report structure

```markdown
# Code Review - FEAT-XXX

## Summary
- Spec compliance:
- Implementation completeness:
- Test coverage:
- Merge readiness:

## Requirement checklist
- [ ] FR-1:
- [ ] NFR-1:

## Findings
### Critical
- None

### Major
- None

### Minor
- None

## Missing tests
- None

## Recommendations
1. 

## Sign-off
- Ready to merge:
```

## When to use

- Before opening a PR
- Before merging a PR
- After implementation, before `/update`
- When code changed and the spec may have drifted
