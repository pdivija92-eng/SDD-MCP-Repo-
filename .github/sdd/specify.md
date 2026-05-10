# /specify

Turn a plain English description into a structured, version-controlled spec file.

## Instructions for Claude

When the user runs `/specify <description>`:

1. If the description is under 20 words or vague, ask up to 3 clarifying questions before proceeding
2. Auto-assign the next available FEAT-XXX ID by scanning `docs/specs/` for existing files
3. Create `docs/specs/FEAT-XXX-<slug>.md` using the spec template below
4. Update the "Current specs" table in `docs/specs/CLAUDE.md`
5. Confirm what was created and suggest running `/plan FEAT-XXX` next

## Spec template

```markdown
# Feature Spec: [Feature Name]

## Metadata
- **ID:** FEAT-XXX
- **Status:** Draft
- **Author:** [from CLAUDE.md or ask]
- **Created:** YYYY-MM-DD
- **Updated:** YYYY-MM-DD

---

## Overview
[One paragraph: what this feature does and why it exists]

## Goals
- 
- 

## Non-goals (out of scope)
- 

---

## Requirements

### Functional requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | | Must Have |

### Non-functional requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-1 | | Must Have |

---

## Acceptance criteria
- [ ] Given [context], when [action], then [outcome]

---

## Design notes
[Key decisions, constraints, or technical considerations]

## Open questions
- [ ] 
```

## Example usage

```
/specify  I need a module that reads CSV files from an S3 bucket,
          validates each row against a Pydantic schema, and
          bulk-inserts valid rows into PostgreSQL. Invalid rows
          go to a dead-letter CSV file.
```
