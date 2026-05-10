"""
PySpark ETL Pipeline — CSV to Delta Lake.

Spec: FEAT-003 (docs/specs/FEAT-003-csv-to-delta-etl.md)
Plan: docs/specs/FEAT-003-plan.md
Status: Implemented 2024-01-15
"""

from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


class Region(str, Enum):
    """Valid regions. Spec: FR-5 data quality."""
    NA = "NA"
    EU = "EU"
    APAC = "APAC"


class SalesRecord(BaseModel):
    """
    Input schema for sales data.

    Spec: FR-3 — Pydantic schema validation
    """
    sale_id: int
    customer_id: int
    amount: float = Field(..., gt=0)  # amount must be > 0
    created_at: datetime
    region: Region

    class Config:
        use_enum_values = False  # Keep as Enum, not string


class PipelineConfig(BaseModel):
    """Pipeline configuration."""
    input_path: str  # local path or s3://bucket/path
    output_table: str  # Delta Lake table name
    dead_letter_table: str
    chunk_size: int = 10_000  # records per batch
    write_mode: str = "append"  # append, replace, upsert
    upsert_key: str | None = None  # column for upsert
    max_retries: int = 3
    retry_backoff_seconds: int = 5


class PipelineStats(BaseModel):
    """Pipeline execution statistics. Spec: FR-8."""
    rows_read: int = 0
    rows_validated: int = 0
    rows_transformed: int = 0
    rows_written: int = 0
    rows_rejected: int = 0
    errors: list[str] = Field(default_factory=list)
    duration_seconds: float = 0.0
    status: str = "pending"  # pending, success, failed
