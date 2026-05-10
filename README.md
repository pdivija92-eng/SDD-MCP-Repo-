# Internal ETL Data Pipeline

A spec-driven Python ETL framework for internal data tooling. Built to extract data from multiple internal sources, transform and validate it, and load it into target destinations reliably.

---

## Project Overview

| Property | Value |
|----------|-------|
| Language | Python 3.11+ |
| Framework | Custom ETL runner + Apache Airflow (optional) |
| Storage targets | PostgreSQL, S3, local filesystem |
| Source systems | REST APIs, PostgreSQL, CSV/Excel files |
| Spec format | Markdown (SDD) |
| MCP integration | `@modelcontextprotocol/server-filesystem` |

---

## Repository Structure

```
sdd-etl-repo/
├── .mcp/
│   └── config.json                  # MCP server config
├── specs/
│   ├── features/
│   │   ├── FEAT-001-pipeline-runner.md
│   │   ├── FEAT-002-extractor-base.md
│   │   ├── FEAT-003-transformer-base.md
│   │   └── FEAT-004-loader-base.md
│   ├── architecture/
│   │   ├── ARCH-001-system-overview.md
│   │   └── ARCH-002-data-flow.md
│   └── api/
│       └── API-001-pipeline-config-schema.md
├── docs/
│   ├── onboarding.md
│   └── runbook.md
├── templates/
│   ├── feature-spec.md
│   ├── architecture-spec.md
│   └── api-spec.md
├── src/
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── csv_extractor.py
│   │   ├── db_extractor.py
│   │   └── api_extractor.py
│   ├── transformers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── cleaner.py
│   │   └── validator.py
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── db_loader.py
│   │   └── s3_loader.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── config.py
│   └── pipeline.py
├── tests/
│   ├── test_extractors.py
│   ├── test_transformers.py
│   └── test_loaders.py
├── pyproject.toml
├── .env.example
└── .gitignore
```

---

## Quick Start

```bash
# 1. Clone and install
git clone <repo-url> && cd sdd-etl-repo
pip install -e ".[dev]"

# 2. Configure environment
cp .env.example .env
# Edit .env with your DB credentials and API keys

# 3. Run a pipeline
python -m src.pipeline run --config pipelines/example.yaml

# 4. Run tests
pytest tests/
```

---

## MCP Integration

AI tools (Claude, Cursor, etc.) can read specs directly via MCP:

```bash
npx @modelcontextprotocol/server-filesystem ./specs
```

The specs folder exposes all feature, architecture, and API specs as context for AI-assisted development. When Claude reads the specs, it understands the full contract before generating any code.

---

## Spec-Driven Workflow

1. **Write spec first** — define inputs, outputs, and transformations in `specs/features/`
2. **Get AI review** — Claude reads the spec via MCP and validates completeness
3. **Generate implementation** — AI generates code conforming to the spec
4. **Validate against spec** — tests reference acceptance criteria from specs
5. **Update spec on change** — spec is the source of truth, code follows

---

## Contributing

- All new features require a spec in `specs/features/` before any code is written
- Specs must have status `Approved` before implementation begins
- PRs must reference the spec ID (e.g. `FEAT-005`) in the commit message
