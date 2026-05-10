# /update

Keep specs and AI memory in sync with the actual codebase. Run after any meaningful code change.

## Instructions for Claude

When the user runs `/update`:

1. Run `git diff HEAD~1 --name-only` (or ask user what changed if no git)
2. For each changed file, identify which FEAT-XXX it belongs to
3. For each affected spec:
   - Update `Status` field if code matches all acceptance criteria
   - Add implementation notes to `Design notes` section
   - Check off acceptance criteria that are now satisfied
4. Rewrite the "Current specs" table in `docs/specs/CLAUDE.md`
5. Add a new entry to "Key decisions" if any important architectural choice was made
6. Print a summary of what was updated

## CLAUDE.md update format

After `/update`, the CLAUDE.md specs table should look like:

```markdown
## Current specs

| ID | Feature | Status | Last updated |
|----|---------|--------|--------------|
| FEAT-001 | CSV ingestion | ✅ Implemented | 2024-01-15 |
| FEAT-002 | Schema validator | 🔄 In progress | 2024-01-16 |
| FEAT-003 | S3 loader | 📋 Approved | 2024-01-14 |
| FEAT-004 | Dead-letter output | 📝 Draft | 2024-01-16 |
```

Status emoji guide:
- 📝 Draft — spec written, not yet reviewed
- 📋 Approved — spec approved, not yet implemented
- 🔄 In progress — implementation started
- ✅ Implemented — code matches spec + tests pass
- ⚠️ Diverged — code changed but spec not updated (needs /update)

## When to run /update

- After `git commit` on a feature branch
- Before opening a PR
- When onboarding a new team member (run once to refresh context)
- When the codebase diverges from specs

## Example output

```
/update complete. Changes detected in:
  - src/ingestion/csv_extractor.py → FEAT-001

Updates made:
  ✓ FEAT-001 status: In progress → Implemented
  ✓ Checked off 3 acceptance criteria in FEAT-001
  ✓ CLAUDE.md specs table refreshed
  ✓ Added to Key decisions: "CSV extractor uses generator-based chunking
    to keep memory under 100MB for files of any size"

Next: run /specify to define your next feature, or /plan FEAT-002 to continue.
```
