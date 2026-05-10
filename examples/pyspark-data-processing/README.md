# Example 3: PySpark Data Pipeline - CSV to Delta Lake

## What This Shows

This example uses SDD for a practical data engineering workflow:

- Read CSV files from S3 or local storage
- Validate schemas and row-level data quality
- Transform records with deduplication, type casting, and quality checks
- Write curated output to Delta Lake-compatible storage
- Route invalid rows to a dead-letter output

## The Workflow

```text
Spec: FEAT-003-csv-to-delta-etl.md
+-- Functional: read CSV, validate, transform, write
+-- Non-functional: 1M rows in under 5 min, bounded memory
+-- Acceptance: handle bad rows and retry on failure

Plan: FEAT-003-plan.md
+-- Task 1: Base classes
+-- Task 2: CSV reader with chunking
+-- Task 3: Schema validation and data cleaner
+-- Task 4: Delta writer
+-- Task 5: Pipeline runner
+-- Task 6: Unit and integration tests
```

## Why This Example Is Useful

- Covers common data engineering patterns: PySpark, data pipelines, and SQL
- Shows scale thinking: 1M+ row pipelines and memory constraints
- Demonstrates data quality: validation, dead-letter patterns, and retries
- Connects SDD to production-style data workflows
- Gives teams a realistic template they can adapt

## Files

```text
pyspark-data-processing/
+-- README.md
+-- docs/specs/
|   +-- FEAT-003-csv-to-delta-etl.md
|   +-- FEAT-003-plan.md
|   +-- CLAUDE.md
+-- src/pipeline/
|   +-- __init__.py
|   +-- reader.py
|   +-- transformer.py
|   +-- writer.py
|   +-- pipeline.py
+-- tests/
|   +-- conftest.py
|   +-- test_reader.py
|   +-- test_transformer.py
|   +-- test_pipeline.py
+-- requirements.txt
```

## Key Insight

SDD is not limited to web apps. It works for batch data pipelines, Spark workloads, ETL orchestration, data quality checks, and schema evolution.

Any transformation pipeline that should be production-ready benefits from a clear spec before implementation.
