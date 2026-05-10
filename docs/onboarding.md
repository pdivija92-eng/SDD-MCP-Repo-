# Onboarding Guide — Internal ETL Pipeline

Welcome to the internal ETL pipeline project. This guide gets you from zero to running your first pipeline in under 15 minutes.

---

## Prerequisites

- Python 3.11+
- Access to the internal PostgreSQL database
- AWS credentials (for S3 loaders)
- Node.js 18+ (for MCP server)

---

## Setup

### 1. Install dependencies

```bash
git clone <repo-url>
cd sdd-etl-repo
pip install -e ".[dev]"
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Verify setup

```bash
pytest tests/ -v
```

All tests should pass. They use mocks, so no real DB or S3 access needed.

---

## Running a Pipeline

```bash
# Dry run — extract and transform only, no loading
python -m src.pipeline run --config pipelines/example.yaml --dry-run

# Full run
python -m src.pipeline run --config pipelines/example.yaml
```

The runner prints a summary table at the end showing rows extracted, transformed, loaded, and rejected.

---

## Creating a New Pipeline

1. Copy an existing config or use `specs/api/API-001-pipeline-config-schema.md` as a reference
2. Create `pipelines/your_pipeline_name.yaml`
3. Test with `--dry-run` first
4. Write a spec in `specs/features/FEAT-XXX-your-pipeline.md` before going to production

---

## Connecting to Claude via MCP

MCP lets Claude read your specs as context, so it understands the contracts before helping you write code.

```bash
# Start the MCP filesystem server
npx @modelcontextprotocol/server-filesystem ./specs

# In Claude Desktop: Settings → MCP → Add Server → point to the running server
```

Once connected, Claude will read specs from `specs/` automatically when you ask it to help with the ETL pipeline.

---

## Project Conventions

- All new pipeline features need a spec in `specs/features/` before code is written
- Spec status must be `Approved` before implementation begins
- Commit messages must reference the spec ID: `feat(FEAT-005): add Excel extractor`
- Tests live in `tests/` and mirror the `src/` structure
- Never hardcode credentials — use `${ENV_VAR}` in YAML configs

---

## Getting Help

- Read the specs in `specs/` — they are the source of truth
- Check `docs/runbook.md` for troubleshooting common issues
- Ask Claude — it has full context on the project via MCP
