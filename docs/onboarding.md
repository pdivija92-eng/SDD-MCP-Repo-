# SDD Toolkit Onboarding

This guide helps a new user clone the toolkit and add Spec-Driven Development to an existing Python project.

## Prerequisites

- Python 3.11+
- Git
- Node.js 18+ if you want to use the generated MCP filesystem config
- An AI assistant or editor that can read Markdown instructions

## Setup

```bash
git clone https://github.com/pdivija92-eng/SDD-MCP-Repo-.git
cd SDD-MCP-Repo-
python sdd-init.py /path/to/your-project
```

The target project will receive:

- `docs/specs/`
- `.github/sdd/`
- `reviews/`
- `.mcp/config.json`
- `.gitignore` additions for SDD cache files

## First Workflow

Open the target project in your editor and run:

```text
/specify I want to build [describe your feature]
/clarify FEAT-001
/plan FEAT-001
/implement FEAT-001
/review FEAT-001
/update
```

## Project Conventions

- Specs live in `docs/specs/`.
- Review reports live in `reviews/`.
- Command instructions live in `.github/sdd/`.
- New features should have a spec before implementation.
- Run `/review` before merging meaningful changes.
- Run `/update` after implementation to refresh spec status and memory.

## Getting Help

- Read [README.md](../README.md) for the public quick start.
- Read [INTEGRATION.md](../INTEGRATION.md) for team rollout guidance.
- Read `.github/sdd/*.md` to see what each SDD command should do.
