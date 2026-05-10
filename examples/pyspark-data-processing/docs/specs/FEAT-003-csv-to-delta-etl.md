# Feature Spec: PySpark CSV to Delta Lake ETL Pipeline

## Metadata
- **ID:** FEAT-003
- **Status:** Implemented
- **Author:** SDD Toolkit Example
- **Created:** 2024-01-10
- **Updated:** 2024-01-15

---

## Overview

Build a production-grade ETL pipeline that reads CSV files (local or S3), validates each row against a Pydantic schema, applies transformations (deduplication, type casting, filtering), and writes clean data to Delta Lake (cloud-native Parquet). Invalid rows go to a dead-letter table. The pipeline is memory-efficient, resumable, and observable.

## Goals
- Process CSV files of any size without exceeding memory budget
- Validate data quality upfront; separate valid from invalid rows
- Write to Delta Lake for ACID guarantees and schema evolution
- Support incremental runs (append or upsert modes)
- Emit structured logs for observability

## Non-Goals (Out of Scope)
- Real-time streaming
- Complex joins (single-table pipelines only in v1)
- Machine learning feature engineering
- Data warehouse orchestration (that's on top of this)

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Reader accepts CSV path (local or s3://...) and chunk size | Must Have |
| FR-2 | Reader yields chunks of records (dict) for memory safety | Must Have |
| FR-3 | Validator accepts Pydantic schema and checks each row | Must Have |
| FR-4 | Invalid rows are routed to dead_letter DataFrame | Must Have |
| FR-5 | Transformer applies steps: dedup, type cast, filter, standardize | Must Have |
| FR-6 | Writer accepts DataFrame and writes to Delta Lake | Must Have |
| FR-7 | Writer supports append, replace, and upsert modes | Should Have |
| FR-8 | Pipeline logs row counts at each stage (read, valid, invalid, written) | Should Have |
| FR-9 | Pipeline retries transient failures up to N times | Should Have |

### Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-1 | Pipeline of 1M rows completes in < 5 minutes | Must Have |
| NFR-2 | Peak memory never exceeds 512MB regardless of file size | Must Have |
| NFR-3 | All code has type hints and spec-aware docstrings | Must Have |
| NFR-4 | 100% test coverage of happy path and error cases | Must Have |

---

## Acceptance Criteria

- [ ] Given a CSV with 1M rows, when pipeline runs, then all valid rows written to Delta Lake within 5 min
- [ ] Given 10K rows with 1K bad rows, when pipeline runs, then bad rows written to dead-letter table
- [ ] Given a pipeline rerun with upsert mode, when duplicate key exists, then row is updated (not duplicated)
- [ ] Given a transient S3 error, when pipeline retries, then it eventually succeeds
- [ ] Given a PySpark DataFrame of 1M rows, when held in memory, then peak memory < 512MB

---

## Architecture

```
Input CSV (s3://bucket/file.csv or /local/file.csv)
    ↓
Reader.read_chunks(path, chunk_size)  [FR-1, FR-2]
    ↓ yields chunks of [dict]
    ↓
for chunk in reader:
    ↓
    Transformer.transform(chunk, schema)  [FR-3, FR-5]
        └─ validate each row (Pydantic)
        └─ route invalid rows to dead_letter
        └─ apply transformations (dedup, type cast, filter)
    ↓
    Writer.write(valid_rows, invalid_rows, table_name)  [FR-6]
        └─ write valid rows to Delta Lake (append/upsert)
        └─ write invalid rows to dead_letter table
        ↓
        ✓ Delta Lake table updated
        ✓ Dead-letter table updated
        ✓ Logs emitted
```

---

## Data Models

### Input Schema (Pydantic)
```python
class SalesRecord(BaseModel):
    sale_id: int
    customer_id: int
    amount: float
    created_at: datetime
    region: str  # enum: NA, EU, APAC
```

### Transformation Steps
1. **Deduplicate** — keep first occurrence of each (sale_id, customer_id)
2. **Type Cast** — ensure amount is float (cast string if needed)
3. **Validate Region** — must be in (NA, EU, APAC)
4. **Filter** — drop rows where amount <= 0

### Output (Delta Lake)
```sql
CREATE TABLE sales_clean (
    sale_id INT,
    customer_id INT,
    amount FLOAT,
    created_at TIMESTAMP,
    region STRING,
    loaded_at TIMESTAMP DEFAULT current_timestamp(),
    PRIMARY KEY (sale_id, customer_id)  -- or just unique constraint
);

CREATE TABLE sales_dead_letter (
    sale_id INT,
    customer_id INT,
    amount STRING,
    created_at STRING,
    region STRING,
    error_reason STRING,
    attempted_at TIMESTAMP DEFAULT current_timestamp()
);
```

---

## Design Notes

- **Chunking**: Reader yields lists of records, not individual records, to reduce function call overhead
- **Memory safety**: Each chunk is ~100KB; held in memory briefly then released after write
- **Pydantic validation**: Each row validated individually; failures are collected, not fatal
- **Idempotency**: Upsert mode with primary key allows reruns without duplication
- **Observability**: Structured logging at every stage (start, chunk processed, summary)

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| File not found | Raise FileNotFoundError immediately |
| S3 permission denied | Raise PermissionError (should be resolved before retry) |
| Transient S3 timeout | Retry with exponential backoff (3 attempts) |
| Invalid CSV format | Log and skip malformed rows, continue |
| Schema validation failure | Route to dead_letter, continue |
| Delta Lake write failure | Fail fast with retry logic at orchestration level |

---

## Performance Targets

- 1M rows in 5 min = 200K rows/min = 3,333 rows/sec
- Chunk size = 10K rows per batch
- 100 chunks total for 1M rows
- Each chunk: read (10ms) + transform (50ms) + write (100ms) = 160ms
- Total: 100 * 160ms = 16 seconds (plenty of headroom for 5-min target)

---

## Open Questions

- [ ] Should we support other input formats (Parquet, JSON)?
- [ ] Should we expose Spark configuration (repartition, shuffle, etc.)?
- [ ] Should pipeline support joins/enrichment from reference tables?
