# /implement

Generate Python code that conforms exactly to a spec and its plan.

## Instructions for Claude

When the user runs `/implement FEAT-XXX`:

1. Read `docs/specs/FEAT-XXX-*.md` (the spec)
2. Read `docs/specs/FEAT-XXX-plan.md` (the plan) — if missing, offer to run `/plan` first
3. Read `docs/specs/CLAUDE.md` for conventions, tech stack, and existing patterns
4. Generate all files listed in the plan's "File structure" section
5. After generating, update the spec status to `Implemented`
6. Remind the user to run `/update` after reviewing the code

## Code generation rules

- Every function gets a docstring referencing the spec requirement it satisfies
  ```python
  def extract(self) -> Iterator[list[dict]]:
      """Yield data in chunks. Spec: FEAT-001 FR-2."""
  ```
- Acceptance criteria from the spec become test function names
  ```python
  def test_given_invalid_row_when_loaded_then_goes_to_dead_letter():
      ...
  ```
- Non-functional requirements (NFR) become pytest markers or inline comments
  ```python
  @pytest.mark.performance  # NFR-1: process 1M rows in < 10 min
  def test_large_file_performance():
      ...
  ```
- Follow the tech stack from CLAUDE.md (don't introduce new dependencies without asking)
- Use Python type hints on all functions
- No hardcoded credentials — use environment variables

## What gets generated

For a typical feature:

```
src/
  <module>/
    __init__.py       ← exports
    base.py           ← abstract base class
    <impl>.py         ← concrete implementation
tests/
  test_<module>.py    ← unit tests, one per acceptance criterion
```

## Example output header

```python
"""
CSV Extractor — reads local and S3 CSV files in chunks.

Spec: FEAT-001 (docs/specs/FEAT-001-csv-ingestion.md)
Plan: docs/specs/FEAT-001-plan.md
Status: Implemented 2024-01-15
"""
```
