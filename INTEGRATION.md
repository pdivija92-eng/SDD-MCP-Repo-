# Integration Guide - Add SDD to Your Project

This guide shows how to adopt Spec-Driven Development in an existing Python project using this toolkit.

## Quick Start

### 1. Clone the toolkit

```bash
git clone https://github.com/pdivija92-eng/SDD-MCP-Repo-.git
cd SDD-MCP-Repo-
```

### 2. Bootstrap SDD into your project

```bash
# Into a new or existing project
python sdd-init.py /path/to/your/project

# Or from inside the target project
python /path/to/SDD-MCP-Repo-/sdd-init.py .
```

This creates:

```text
your-project/
+-- docs/
|   +-- specs/
|       +-- CLAUDE.md
|       +-- FEAT-XXX specs and plans
+-- reviews/
|   +-- review reports created by /review
+-- .github/
|   +-- sdd/
|       +-- specify.md
|       +-- clarify.md
|       +-- plan.md
|       +-- implement.md
|       +-- review.md
|       +-- update.md
+-- .mcp/
    +-- config.json
```

The toolkit uses `.github/sdd/` for reusable command definitions.

### 3. Start the workflow

Open the project in your editor and use the slash commands with your AI assistant:

```text
/specify I need a user authentication module with JWT tokens
/clarify FEAT-001
/plan FEAT-001
/implement FEAT-001
/review FEAT-001
/update
```

## The SDD Workflow

1. `/specify` creates a requirement spec in `docs/specs/`.
2. `/clarify` resolves ambiguity and makes acceptance criteria testable.
3. `/plan` creates an implementation plan tied to the spec.
4. `/implement` builds code and tests from the approved plan.
5. `/review` compares the implementation or PR diff against the spec and stores the report in `reviews/`.
6. `/update` refreshes spec status, acceptance criteria, and project memory.

## PR Review Agent

The `/review` command is the PR review agent. It should:

- Read the related feature spec and implementation plan.
- Inspect the PR diff or local code changes.
- Check whether functional requirements, non-functional requirements, and acceptance criteria are satisfied.
- Identify missing tests, behavior gaps, security concerns, and maintainability risks.
- Write a review artifact to `reviews/FEAT-XXX-review.md`.

Use it before opening a PR or before merging a feature branch.

## Team Adoption

### Solo or small project

```bash
python sdd-init.py .
```

Create a spec before each meaningful feature and run `/review` before merging.

### Team project

Add these checks to your PR template:

```markdown
- [ ] Spec exists in `docs/specs/`
- [ ] Implementation plan exists for feature work
- [ ] `/review` report exists in `reviews/`
- [ ] `/update` has refreshed specs and project memory
```

### Organization rollout

1. Fork this toolkit into your organization.
2. Customize `.github/sdd/` command instructions for your stack.
3. Add `sdd-init.py` to internal project scaffolding.
4. Use `reviews/` artifacts as part of engineering review history.

## FAQ

**Do we need a specific AI tool?**  
No. Specs are plain Markdown. Any assistant or developer can read them.

**Can this work without slash commands?**  
Yes. The command files are reusable instructions. You can paste the relevant command file into any AI chat.

**Does this replace Jira, Linear, or GitHub Issues?**  
No. Tickets describe the business need. SDD specs describe the technical contract and acceptance criteria.

**How often should `/update` run?**  
After implementation, before opening a PR, and whenever code behavior changes in a way specs should record.
