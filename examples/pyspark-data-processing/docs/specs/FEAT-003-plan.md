# Implementation Plan: FEAT-003 — PySpark CSV to Delta Lake Pipeline

## Metadata
- **Spec**: [FEAT-003-csv-to-delta-etl.md](./FEAT-003-csv-to-delta-etl.md)
- **Estimated total**: 4 hours
- **Created**: 2024-01-10

---

## File Structure

Files to create:
- `src/pipeline/__init__.py` — module exports
- `src/pipeline/models.py` — Pydantic schema, configuration
- `src/pipeline/reader.py` — CSV reader with chunking
- `src/pipeline/transformer.py` — data validation and transformation
- `src/pipeline/writer.py` — Delta Lake writer
- `src/pipeline/pipeline.py` — main orchestrator
- `src/pipeline/utils.py` — logging, retry logic
- `tests/conftest.py` — fixtures, sample CSV
- `tests/test_reader.py` — reader tests
- `tests/test_transformer.py` — transformer tests
- `tests/test_pipeline.py` — end-to-end tests

---

## Tasks (in order)

- [ ] **Task 1**: Define schemas and config — _30 min_
  - What: Pydantic BaseModel for input schema, PipelineConfig for settings
  - Acceptance: Can instantiate models; validation works for valid/invalid inputs
  - Spec refs: FR-3, NFR-3

- [ ] **Task 2**: Implement CSV reader — _1 hr_
  - What: CSVReader class with read_chunks() generator
  - Acceptance: Reads local and S3 CSVs in chunks; memory bounded
  - Spec refs: FR-1, FR-2, NFR-2

- [ ] **Task 3**: Implement transformer — _1 hr_
  - What: TransformerPipeline class with validate() and transform()
  - Acceptance: Routes valid rows and invalid rows correctly; deduplication works
  - Spec refs: FR-3, FR-4, FR-5

- [ ] **Task 4**: Implement Delta Lake writer — _45 min_
  - What: DeltaWriter class with write() method supporting modes
  - Acceptance: Writes to Delta Lake; append/upsert modes work
  - Spec refs: FR-6, FR-7

- [ ] **Task 5**: Implement main pipeline orchestrator — _45 min_
  - What: Pipeline.run() method that coordinates reader → transformer → writer
  - Acceptance: Full pipeline executes; logs emitted; summary statistics collected
  - Spec refs: FR-8, FR-9

- [ ] **Task 6**: Write comprehensive tests — _1 hr_
  - What: Unit tests for each component; integration test for full pipeline
  - Acceptance: 100% coverage; performance tests verify 1M row target
  - Spec refs: NFR-4

---

## Test Plan

| Test | Type | Covers |
|------|------|--------|
| `test_schema_validation_happy_path` | unit | FR-3 |
| `test_schema_validation_invalid_row` | unit | FR-3, FR-4 |
| `test_csv_reader_chunking` | unit | FR-1, FR-2 |
| `test_csv_reader_s3` | unit | FR-1 |
| `test_transformer_deduplication` | unit | FR-5 |
| `test_transformer_type_casting` | unit | FR-5 |
| `test_dead_letter_routing` | unit | FR-4 |
| `test_delta_writer_append` | unit | FR-6, FR-7 |
| `test_delta_writer_upsert` | unit | FR-7 |
| `test_full_pipeline_happy_path` | integration | FR-1 through FR-9 |
| `test_pipeline_1m_rows_performance` | performance | NFR-1, NFR-2 |
| `test_retry_on_transient_error` | integration | FR-9 |

---

## Performance Benchmarks

After Task 6, measure:
- **Throughput**: 1M rows in <5 min (target: 200K rows/min)
- **Memory**: Peak RSS < 512MB for 1M row pipeline
- **Latency**: Per-chunk processing (target: <200ms/10K rows)

---

## Dependencies

- Must complete before: Data warehouse ETL orchestration built on top
- Blocked by: Delta Lake cluster availability
- Requires: PySpark 3.3+, Pydantic 2.0+, pytest-cov
