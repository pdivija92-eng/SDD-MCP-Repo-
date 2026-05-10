#!/usr/bin/env python3
"""
SDD Toolkit - Interactive Demo

Run this to see the full SDD workflow on a sample ETL feature.

Usage:
    python demo/run_demo.py
"""

import sys
import time
from datetime import datetime


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
WHITE = "\033[97m"


def color(style: str, text: str) -> str:
    return f"{style}{text}{RESET}"


def pause(seconds: float = 0.5) -> None:
    time.sleep(seconds)


def typewrite(text: str, delay: float = 0.01) -> None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def section(title: str) -> None:
    print()
    print(color(CYAN, "=" * 64))
    print(color(BOLD + CYAN, f"  {title}"))
    print(color(CYAN, "=" * 64))
    pause()


def command(cmd: str) -> None:
    print()
    print(color(DIM, "  $ "), end="")
    typewrite(color(BOLD + WHITE, cmd), delay=0.02)
    pause()


def thinking(message: str) -> None:
    sys.stdout.write(color(YELLOW, f"  ... {message}"))
    for _ in range(3):
        time.sleep(0.2)
        sys.stdout.write(color(YELLOW, "."))
        sys.stdout.flush()
    print(color(GREEN, " done"))


def created(path: str, detail: str) -> None:
    print(color(GREEN, f"  [ok] {path}") + color(DIM, f" - {detail}"))


def show_file(title: str, content: str, max_lines: int = 18) -> None:
    print()
    print(color(PURPLE, f"  --- {title} ---"))
    lines = content.strip().splitlines()
    for line in lines[:max_lines]:
        print(color(DIM, f"  {line}"))
    if len(lines) > max_lines:
        print(color(DIM, f"  ... {len(lines) - max_lines} more lines"))
    pause()


SPEC = """# Feature Spec: CSV to PostgreSQL Ingestion

## Metadata
- ID: FEAT-001
- Status: Draft
- Created: {date}

## Overview
Read CSV files, validate each row, load valid rows into PostgreSQL,
and route invalid rows to a dead-letter file.

## Functional requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Read local CSV files | Must Have |
| FR-2 | Validate rows against a schema | Must Have |
| FR-3 | Bulk insert valid rows into PostgreSQL | Must Have |
| FR-4 | Write invalid rows to a dead-letter CSV | Must Have |

## Acceptance criteria
- [ ] Given a valid CSV, when ingested, then rows are loaded
- [ ] Given invalid rows, when validated, then they are dead-lettered
"""

PLAN = """# Implementation Plan: FEAT-001

## Files
- src/ingestion/reader.py
- src/ingestion/validator.py
- src/ingestion/loader.py
- tests/test_csv_ingestion.py

## Tasks
- [ ] Implement chunked CSV reader
- [ ] Implement row validation
- [ ] Implement PostgreSQL bulk loader
- [ ] Add tests for acceptance criteria
"""

REVIEW = """# Code Review - FEAT-001

## Summary
- Spec compliance: mostly complete
- Implementation completeness: reader, validator, and loader present
- Test coverage: acceptance criteria covered
- Merge readiness: ready after one minor naming cleanup

## Findings
### Minor
- Rename `bad_rows_path` to `dead_letter_path` for spec language consistency.

## Sign-off
- Ready to merge: yes, after minor cleanup
"""

MEMORY = """# Project Memory - Demo ETL Project

## Current specs

| ID | Feature | Status | Last updated |
|----|---------|--------|--------------|
| FEAT-001 | CSV to PostgreSQL ingestion | Implemented | {date} |

## Key decisions
- Invalid rows are routed to a dead-letter file.
- CSV reading uses chunks to keep memory bounded.
"""


def run_demo() -> None:
    today = datetime.now().strftime("%Y-%m-%d")

    print(color(BOLD + CYAN, "SDD Toolkit - Interactive Demo"))
    print(color(DIM, "A short walkthrough of spec, plan, implement, review, and update."))

    section("Step 0 - Bootstrap")
    command("python sdd-init.py demo-project")
    created("docs/specs/", "feature specs and plans")
    created(".github/sdd/", "slash command instructions")
    created("reviews/", "review artifacts")
    created(".mcp/config.json", "MCP filesystem config")

    section("Step 1 - /specify")
    command("/specify I need a CSV ingestion module for PostgreSQL")
    thinking("creating feature spec")
    created("docs/specs/FEAT-001-csv-ingestion.md", "formal feature spec")
    show_file("FEAT-001-csv-ingestion.md", SPEC.format(date=today))

    section("Step 2 - /clarify")
    command("/clarify FEAT-001")
    print(color(WHITE, "  Question: What should happen when some rows are invalid?"))
    print(color(GREEN, "  Answer: Load valid rows and write invalid rows to a dead-letter CSV."))
    created("FEAT-001", "acceptance criteria tightened")

    section("Step 3 - /plan")
    command("/plan FEAT-001")
    thinking("building implementation plan")
    created("docs/specs/FEAT-001-plan.md", "tasks, files, and tests")
    show_file("FEAT-001-plan.md", PLAN)

    section("Step 4 - /implement")
    command("/implement FEAT-001")
    thinking("generating reader, validator, loader, and tests")
    created("src/ingestion/reader.py", "chunked CSV reader")
    created("src/ingestion/validator.py", "schema validation")
    created("src/ingestion/loader.py", "bulk insert loader")
    created("tests/test_csv_ingestion.py", "acceptance tests")

    section("Step 5 - /review")
    command("/review FEAT-001")
    thinking("checking implementation against the spec")
    created("reviews/FEAT-001-review.md", "spec-based review report")
    show_file("FEAT-001-review.md", REVIEW)

    section("Step 6 - /update")
    command("/update")
    thinking("syncing spec status and project memory")
    created("docs/specs/CLAUDE.md", "current specs and decisions refreshed")
    show_file("CLAUDE.md", MEMORY.format(date=today))

    section("Summary")
    steps = [
        ("sdd-init", "adds SDD folders to an existing project"),
        ("/specify", "turns an idea into a spec"),
        ("/clarify", "makes requirements testable"),
        ("/plan", "turns specs into implementation tasks"),
        ("/implement", "builds code and tests from the plan"),
        ("/review", "checks code against requirements"),
        ("/update", "keeps memory and specs current"),
    ]
    for cmd, description in steps:
        print(f"  {color(GREEN, '[ok]')} {color(BOLD, cmd):<14} {color(DIM, description)}")

    print()
    print(color(WHITE, "Try it on your own project:"))
    print(color(WHITE, "  python sdd-init.py /path/to/your-project"))


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\nDemo interrupted. Run again anytime: python demo/run_demo.py")
