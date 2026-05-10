# Feature Spec: Pipeline Runner

## Metadata
- **ID:** FEAT-001
- **Status:** Approved
- **Author:** Platform Team
- **Created:** 2024-01-10
- **Updated:** 2024-01-15

---

## Overview

The Pipeline Runner is the central orchestrator of the ETL framework. It reads a pipeline configuration (YAML), resolves the extractor, transformer, and loader components, and executes them in sequence. It manages execution context, error handling, retries, and run logging.

## Goals
- Provide a single entry point to execute any configured pipeline
- Support sequential and parallelizable pipeline steps
- Emit structured logs for every run (start, success, failure, row counts)
- Support dry-run mode for validation without side effects

## Non-Goals (Out of Scope)
- Distributed execution (handled by Airflow integration layer, not this runner)
- Real-time / streaming pipelines (batch only)
- UI dashboard for run history

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Runner accepts a YAML config file path as input | Must Have |
| FR-2 | Runner resolves and instantiates extractor, transformer, loader from config | Must Have |
| FR-3 | Runner passes extracted data through transformer, then to loader | Must Have |
| FR-4 | Runner supports `--dry-run` flag: extract + transform only, skip load | Must Have |
| FR-5 | Runner retries failed steps up to N times (configurable, default 3) | Must Have |
| FR-6 | Runner logs row counts at each stage (extracted, transformed, loaded) | Should Have |
| FR-7 | Runner emits a structured run summary to stdout and optionally to a log file | Should Have |
| FR-8 | Runner supports environment variable interpolation in config values | Should Have |

### Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-1 | A pipeline of 1M rows must complete within 10 minutes on standard hardware | Must Have |
| NFR-2 | Runner must not hold more than 100MB of data in memory at once (use chunking) | Must Have |
| NFR-3 | All run errors must be logged with full tracebacks | Must Have |

---

## Acceptance Criteria

- [ ] Given a valid YAML config, when `pipeline run --config <path>` is called, then the pipeline executes all three stages
- [ ] Given `--dry-run` flag, when pipeline is run, then no data is written to the loader destination
- [ ] Given a stage failure, when retries are exhausted, then the runner exits with code 1 and logs the error
- [ ] Given a 1M-row CSV input, when the pipeline runs, then peak memory usage stays below 100MB
- [ ] Given a config with `${ENV_VAR}` syntax, when runner starts, then the value is resolved from the environment

---

## Pipeline Config Format

```yaml
name: daily_sales_sync
description: Syncs daily sales data from CSV to PostgreSQL

extractor:
  type: csv
  path: /data/sales_${RUN_DATE}.csv
  chunk_size: 10000

transformer:
  steps:
    - type: drop_nulls
      columns: [sale_id, amount]
    - type: rename_columns
      mapping:
        sale_id: id
        sale_amount: amount
    - type: cast_types
      columns:
        amount: float
        created_at: datetime

loader:
  type: postgres
  table: public.sales
  mode: upsert
  conflict_key: id

retry:
  max_attempts: 3
  backoff_seconds: 5
```

---

## Design Notes

- Use Python generators / chunked iteration to keep memory bounded
- Each stage (extract, transform, load) is a Python class implementing the base interface
- Config is validated with Pydantic before execution begins
- Run metadata (start time, duration, row counts, status) is written to a `pipeline_runs` table if a DB loader is configured

## Dependencies
- [FEAT-002](./FEAT-002-extractor-base.md) — Extractor base class
- [FEAT-003](./FEAT-003-transformer-base.md) — Transformer base class
- [FEAT-004](./FEAT-004-loader-base.md) — Loader base class
- [ARCH-001](../architecture/ARCH-001-system-overview.md) — System overview

## Open Questions
- [ ] Should the runner support parallel execution of independent pipeline steps in v1?
