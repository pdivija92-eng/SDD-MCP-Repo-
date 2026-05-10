#!/usr/bin/env python3
"""
sdd-init.py - Bootstrap Spec-Driven Development into any Python project.

Usage:
    python sdd-init.py .
    python sdd-init.py /path/to/your-project
    python sdd-init.py . --name "My ETL Project"
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


BANNER = """
============================================================
 SDD Toolkit - sdd-init v1.0
 Spec-Driven Development for Python projects
============================================================
"""

MEMORY_TEMPLATE = """# Project Memory - {project_name}

> This file is the AI-readable memory for this project.
> Update it using `/update` after meaningful code or spec changes.

## Project overview
- **Name**: {project_name}
- **Type**: Python project
- **SDD initialized**: {date}
- **Spec folder**: `docs/specs/`
- **Review folder**: `reviews/`

## What this project does
<!-- Fill this in after /specify your first feature -->

## Current specs

| ID | Feature | Status |
|----|---------|--------|
| - | No specs yet - run /specify to create your first | - |

## Key decisions
<!-- Important architectural or design decisions go here -->

## Tech stack
- Language: Python 3.11+
- <!-- Add your stack: FastAPI, PySpark, SQLAlchemy, etc. -->

## Conventions
- All new features require a spec in `docs/specs/` before code is written
- Spec status: Draft -> Review -> Approved -> Implemented
- Run `/review` before merging meaningful changes
- Commit format: `feat(FEAT-XXX): description`

## Slash commands
- `/specify <description>` - create a new feature spec
- `/clarify [FEAT-XXX]` - refine an existing spec
- `/plan FEAT-XXX` - break a spec into implementation tasks
- `/implement FEAT-XXX` - generate code from a spec and plan
- `/review FEAT-XXX` - review implementation or PR changes against the spec
- `/update` - sync specs and this memory file after code changes
"""

GITIGNORE_ADDITIONS = """

# SDD Toolkit
.sdd-cache/
"""

COMMANDS = ["specify", "clarify", "plan", "implement", "review", "update"]


def print_step(message: str) -> None:
    print(f"  [ok] {message}")


def print_header(message: str) -> None:
    print(f"\n{message}")
    print("  " + "-" * len(message))


def create_folder_structure(target: Path) -> None:
    """Create SDD folders inside the target project."""
    for folder in ["docs/specs", ".github/sdd", "reviews"]:
        path = target / folder
        path.mkdir(parents=True, exist_ok=True)
        print_step(f"Created {folder}/")


def write_memory_file(target: Path, project_name: str) -> None:
    """Write the AI memory file."""
    content = MEMORY_TEMPLATE.format(
        project_name=project_name,
        date=datetime.now().strftime("%Y-%m-%d"),
    )
    path = target / "docs" / "specs" / "CLAUDE.md"
    path.write_text(content, encoding="utf-8")
    print_step("Created docs/specs/CLAUDE.md")


def write_slash_commands(target: Path) -> None:
    """Copy slash command definitions into .github/sdd/."""
    toolkit_dir = Path(__file__).parent
    commands_src = toolkit_dir / ".github" / "sdd"
    commands_dst = target / ".github" / "sdd"

    for command in COMMANDS:
        src = commands_src / f"{command}.md"
        dst = commands_dst / f"{command}.md"
        if src.exists():
            shutil.copy(src, dst)
            print_step(f"Installed /{command} command")
        else:
            dst.write_text(FALLBACK_COMMANDS[command], encoding="utf-8")
            print_step(f"Installed /{command} command from fallback")


def write_mcp_config(target: Path) -> None:
    """Write MCP config for compatible tools."""
    mcp_dir = target / ".mcp"
    mcp_dir.mkdir(exist_ok=True)
    config = {
        "mcpServers": {
            "sdd-specs": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "./docs/specs",
                ],
                "description": "Expose project specs to MCP-compatible AI tools",
            }
        }
    }
    config_path = mcp_dir / "config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print_step("Created .mcp/config.json")


def update_gitignore(target: Path) -> None:
    """Add SDD cache entries to .gitignore."""
    gitignore = target / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8")
        if ".sdd-cache" not in content:
            gitignore.write_text(content.rstrip() + GITIGNORE_ADDITIONS, encoding="utf-8")
            print_step("Updated .gitignore")
        return

    gitignore.write_text(GITIGNORE_ADDITIONS.strip() + "\n", encoding="utf-8")
    print_step("Created .gitignore")


def print_next_steps(target: Path) -> None:
    print(
        f"""
SDD is ready in: {target}

Next steps:

  1. Open your project:
     code {target}

  2. Start with a spec:
     /specify I want to build [describe your first feature]

  3. Continue the workflow:
     /clarify FEAT-001
     /plan FEAT-001
     /implement FEAT-001
     /review FEAT-001
     /update

Review reports will be stored in:
     reviews/

MCP config was written to:
     .mcp/config.json
"""
    )


FALLBACK_COMMANDS = {
    "specify": """# /specify

**Usage**: `/specify <feature description>`

Turn a plain English description into a structured spec file.

## What the assistant should do
1. Ask clarifying questions if the description is ambiguous
2. Generate a spec file at `docs/specs/FEAT-XXX-<name>.md`
3. Update `docs/specs/CLAUDE.md` with the new spec entry

## Spec file structure
- Metadata
- Overview and goals
- Functional requirements
- Non-functional requirements
- Acceptance criteria
- Design notes and open questions
""",
    "clarify": """# /clarify

**Usage**: `/clarify [FEAT-XXX]`

Refine an existing spec through structured Q&A.

## What the assistant should do
1. Read the current or specified spec
2. Identify ambiguities and missing acceptance criteria
3. Ask targeted questions
4. Update the spec with the answers
""",
    "plan": """# /plan

**Usage**: `/plan FEAT-XXX`

Break an approved spec into concrete implementation tasks.

## What the assistant should do
1. Read `docs/specs/FEAT-XXX-*.md`
2. Create `docs/specs/FEAT-XXX-plan.md`
3. Include tasks, file structure, tests, dependencies, and risks
""",
    "implement": """# /implement

**Usage**: `/implement FEAT-XXX`

Generate code that conforms to a spec and implementation plan.

## What the assistant should do
1. Read the spec, plan, and project memory
2. Implement the planned files
3. Add tests for acceptance criteria
4. Update the spec status when complete
""",
    "review": """# /review

**Usage**: `/review FEAT-XXX` or `/review PR-#`

Review implementation or pull request changes against the related SDD spec.

## What the assistant should do
1. Read the feature spec and implementation plan
2. Inspect the PR diff or local changes
3. Check requirement coverage and acceptance criteria
4. Identify bugs, missing tests, risks, and spec drift
5. Write a report to `reviews/FEAT-XXX-review.md`
""",
    "update": """# /update

**Usage**: `/update`

Keep specs and project memory in sync with code changes.

## What the assistant should do
1. Inspect recent code changes
2. Map changed files to affected specs
3. Update spec status and acceptance criteria
4. Refresh `docs/specs/CLAUDE.md`
5. Summarize what changed
""",
}


def main() -> None:
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="Bootstrap Spec-Driven Development into any Python project"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Path to your Python project (default: current directory)",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Project name (default: folder name)",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"Error: target path does not exist: {target}")
        sys.exit(1)

    project_name = args.name or target.name.replace("-", " ").replace("_", " ").title()

    print(f"Project: {project_name}")
    print(f"Target:  {target}")

    print_header("Creating folder structure")
    create_folder_structure(target)

    print_header("Writing AI memory file")
    write_memory_file(target, project_name)

    print_header("Installing slash commands")
    write_slash_commands(target)

    print_header("Configuring MCP")
    write_mcp_config(target)

    print_header("Updating .gitignore")
    update_gitignore(target)

    print_next_steps(target)


if __name__ == "__main__":
    main()
