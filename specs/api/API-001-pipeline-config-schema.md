# API Spec: Pipeline Configuration Schema

## Metadata
- **ID:** API-001
- **Status:** Approved
- **Author:** Platform Team
- **Created:** 2024-01-12

---

## Overview

Defines the full schema for pipeline YAML configuration files. This schema is enforced at runtime via a Pydantic model. Any pipeline config that doesn't conform will be rejected before execution begins.

---

## Top-Level Schema

```yaml
name: string              # Required. Unique pipeline identifier.
description: string       # Optional. Human-readable description.

extractor:                # Required. One extractor block.
  type: csv | postgres | api
  # ...type-specific fields (see below)

transformer:              # Optional. Omit if no transformations needed.
  steps:
    - type: string        # Step type key (see Transformer Steps)
      # ...step-specific fields

loader:                   # Required. One loader block.
  type: postgres | s3
  # ...type-specific fields (see below)

retry:                    # Optional. Defaults apply if omitted.
  max_attempts: int       # Default: 3
  backoff_seconds: int    # Default: 5

dead_letter:              # Optional. Where to send invalid rows.
  type: csv | postgres
  path: string            # CSV path (if type: csv)
  table: string           # DB table (if type: postgres)

dry_run: bool             # Optional. Default: false. Set true to skip loading.
```

---

## Extractor Schemas

### CSV Extractor

```yaml
extractor:
  type: csv
  path: string            # Required. File path. Supports ${ENV_VAR} interpolation.
  delimiter: string       # Optional. Default: ","
  encoding: string        # Optional. Default: "utf-8"
  chunk_size: int         # Optional. Default: 10000
  skip_header: bool       # Optional. Default: true
```

### PostgreSQL Extractor

```yaml
extractor:
  type: postgres
  dsn: string             # Required. PostgreSQL connection string. Use ${DATABASE_URL}.
  query: string           # Required. SQL SELECT query.
  chunk_size: int         # Optional. Default: 1000
  params: dict            # Optional. Query parameters (safe substitution).
```

### API Extractor

```yaml
extractor:
  type: api
  url: string             # Required. Base endpoint URL.
  method: GET | POST      # Optional. Default: GET
  headers: dict           # Optional. Request headers.
  auth:
    type: bearer | api_key | basic
    token: string         # For bearer auth. Use ${ENV_VAR}.
    key_header: string    # For api_key auth. Header name.
    key_value: string     # For api_key auth. Use ${ENV_VAR}.
  pagination:
    type: cursor | page | none
    cursor_field: string  # For cursor pagination. Response field name.
    page_param: string    # For page pagination. Query param name.
    page_size: int        # Default: 100
    max_pages: int        # Optional. Safety limit.
```

---

## Transformer Step Schemas

### drop_nulls
```yaml
- type: drop_nulls
  columns: [string]       # Required. Column names to check.
```

### rename_columns
```yaml
- type: rename_columns
  mapping:
    old_name: new_name    # Key: current name, Value: new name
```

### cast_types
```yaml
- type: cast_types
  columns:
    column_name: int | float | str | datetime | bool
```

### filter_rows
```yaml
- type: filter_rows
  expression: string      # Python expression. Row is dict, access as row['field'].
  # Example: "row['status'] == 'active' and row['amount'] > 0"
```

### deduplicate
```yaml
- type: deduplicate
  keys: [string]          # Required. Columns that define uniqueness.
  keep: first | last      # Optional. Default: first
```

### validate_schema
```yaml
- type: validate_schema
  schema:
    field_name:
      type: str | int | float | bool | datetime
      required: bool      # Default: true
      min: number         # Optional. For numeric fields.
      max: number         # Optional. For numeric fields.
      pattern: string     # Optional. Regex for string fields.
```

---

## Loader Schemas

### PostgreSQL Loader

```yaml
loader:
  type: postgres
  dsn: string             # Required. Use ${DATABASE_URL}.
  table: string           # Required. Schema-qualified table name (e.g. public.sales).
  mode: append | replace | upsert
  conflict_key: string    # Required if mode: upsert. Column name.
  batch_size: int         # Optional. Default: 5000
```

### S3 Loader

```yaml
loader:
  type: s3
  bucket: string          # Required.
  prefix: string          # Required. S3 key prefix.
  format: csv | parquet   # Optional. Default: parquet
  partition_by: [string]  # Optional. Column names for Hive-style partitioning.
  compression: snappy | gzip | none  # Optional. Default: snappy (Parquet only).
```

---

## Full Example

```yaml
name: daily_orders_sync
description: Syncs yesterday's orders from internal DB to S3 as Parquet

extractor:
  type: postgres
  dsn: ${DATABASE_URL}
  query: |
    SELECT order_id, customer_id, amount, status, created_at
    FROM orders
    WHERE created_at::date = current_date - 1
  chunk_size: 5000

transformer:
  steps:
    - type: drop_nulls
      columns: [order_id, amount]
    - type: cast_types
      columns:
        amount: float
        created_at: datetime
    - type: filter_rows
      expression: "row['status'] != 'cancelled'"
    - type: validate_schema
      schema:
        order_id:
          type: str
          required: true
        amount:
          type: float
          required: true
          min: 0

loader:
  type: s3
  bucket: internal-data-lake
  prefix: orders/raw/
  format: parquet
  partition_by: [created_at]

dead_letter:
  type: csv
  path: /tmp/rejected_orders_${RUN_DATE}.csv

retry:
  max_attempts: 3
  backoff_seconds: 10
```

---

## Validation Rules

- `name` must match pattern `^[a-z0-9_-]+$`
- `extractor.type` must be one of `csv`, `postgres`, `api`
- `loader.type` must be one of `postgres`, `s3`
- `mode: upsert` requires `conflict_key` to be set
- `${ENV_VAR}` tokens are resolved at startup; missing env vars cause an immediate error with the variable name in the message

## Related Specs
- [FEAT-001](../features/FEAT-001-pipeline-runner.md) — Pipeline Runner (consumes this schema)
- [ARCH-001](../architecture/ARCH-001-system-overview.md) — System Overview
