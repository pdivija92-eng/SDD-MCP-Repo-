# SDD Toolkit - Spec-Driven Development for Python Projects

> Drop spec-driven development into any Python project in one command.

SDD helps teams write the spec first, let AI-assisted tools build from that shared context, and keep specs, implementation plans, reviews, and project memory in sync as the code evolves.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple.svg)](https://modelcontextprotocol.io)
[![Works with](https://img.shields.io/badge/works%20with-Claude%20%7C%20Cursor%20%7C%20Copilot-orange.svg)]()

## What This Gives You

- A one-command bootstrap script: `python sdd-init.py /path/to/project`
- Reusable slash command instructions in `.github/sdd/`
- A living `docs/specs/` folder for feature specs and implementation plans
- An AI memory file at `docs/specs/CLAUDE.md`
- A `reviews/` folder for PR and implementation review reports
- Examples for APIs, Django models, and data pipelines

## Why SDD Matters

| Without SDD | With SDD |
|---|---|
| Requirements live in chat threads | Specs live in version-controlled Markdown |
| New contributors reverse-engineer the codebase | Contributors read specs and start with context |
| AI output drifts from requirements | AI reads specs before generating code |
| Code and docs drift apart | `/update` keeps them aligned |
| PR reviews miss requirement gaps | `/review` checks changes against the spec |

## Quick Start

```bash
# 1. Clone this toolkit
git clone https://github.com/pdivija92-eng/SDD-MCP-Repo-.git
cd SDD-MCP-Repo-

# 2. Bootstrap SDD into any Python project
python sdd-init.py /path/to/your-project

# 3. Open the target project in VS Code or Cursor
code /path/to/your-project

# 4. Start with a spec
/specify I want a user authentication module with JWT tokens
```

Your project now has `docs/specs/`, `.github/sdd/`, MCP config, and `reviews/`.

## Slash Commands

| Command | What it does | Output |
|---|---|---|
| `/specify` | Turns a feature idea into a formal spec | `docs/specs/FEAT-XXX-name.md` |
| `/clarify` | Refines an incomplete spec through focused questions | Updated spec |
| `/plan` | Breaks a spec into implementation tasks | `docs/specs/FEAT-XXX-plan.md` |
| `/implement` | Generates code from an approved spec and plan | Source and test files |
| `/review` | Reviews code or PR changes against the spec | `reviews/FEAT-XXX-review.md` |
| `/update` | Syncs specs and memory after code changes | Updated spec and memory files |

## Repository Layout Added to Your Project

```text
your-project/
+-- docs/
|   +-- specs/
|       +-- CLAUDE.md
|       +-- FEAT-001-example.md
|       +-- FEAT-001-plan.md
+-- reviews/
|   +-- FEAT-001-review.md
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

Nothing in your existing application code changes. SDD lives alongside it.

## Try the Demo

```bash
cd demo/
python run_demo.py
```

The demo walks through a complete SDD cycle using a sample ETL pipeline: spec, plan, implementation, review, and update.

## Examples

- `examples/fastapi-auth-module/` - JWT authentication with FastAPI
- `examples/django-orm-task/` - Django model and signal workflow
- `examples/pyspark-data-processing/` - CSV-to-Delta data pipeline

## Who This Is For

This toolkit is useful for teams and individual developers who want a lightweight, repeatable way to align requirements, implementation plans, code, tests, and reviews.

It works well for backend services, data engineering pipelines, automation projects, and Python templates where long-lived context matters.

## Connect

- LinkedIn: [linkedin.com/in/divija-p-a61b42252](https://linkedin.com/in/divija-p-a61b42252)
- GitHub: [pdivija92-eng](https://github.com/pdivija92-eng)
