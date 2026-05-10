"""
Delta Lake writer with append/upsert support.

Spec: FEAT-003 FR-6, FR-7
Writes validated records and dead-letter rows to Delta Lake.
"""

from typing import Any
from datetime import datetime


class DeltaWriter:
    """
    Write to Delta Lake. Spec: FR-6, FR-7.

    Args:
        output_table: Delta Lake table name (e.g. 'sales_clean')
        dead_letter_table: Dead-letter table name
        write_mode: 'append', 'replace', or 'upsert'
        upsert_key: Column name for upsert matching (if mode='upsert')
    """

    def __init__(
        self,
        output_table: str,
        dead_letter_table: str,
        write_mode: str = "append",
        upsert_key: str | None = None,
    ):
        self.output_table = output_table
        self.dead_letter_table = dead_letter_table
        self.write_mode = write_mode
        self.upsert_key = upsert_key
        self.written_count = 0
        self.dead_letter_count = 0

    def write(self, valid_rows: list[dict], invalid_rows: list[dict]) -> None:
        """
        Write valid rows to output table, invalid to dead-letter.

        Spec: FR-6 — Write to Delta Lake
        Spec: FR-7 — Supports append/upsert modes
        Spec: FR-4 — Dead-letter routing

        Args:
            valid_rows: Records that passed validation
            invalid_rows: Records that failed validation
        """
        if valid_rows:
            self._write_valid(valid_rows)

        if invalid_rows:
            self._write_dead_letter(invalid_rows)

    def _write_valid(self, rows: list[dict]) -> None:
        """Write valid rows based on write_mode. Spec: FR-6, FR-7."""
        # In production, would use PySpark SQL:
        # spark.createDataFrame(rows, schema).write \
        #     .format("delta") \
        #     .mode(self.write_mode) \
        #     .option("mergeSchema", "true") \
        #     .saveAsTable(self.output_table)

        # For demo, just count
        self.written_count += len(rows)

    def _write_dead_letter(self, rows: list[dict]) -> None:
        """Write dead-letter rows. Spec: FR-4."""
        # Add metadata to dead-letter records
        for row in rows:
            row["attempted_at"] = datetime.utcnow().isoformat()
            row["error_reason"] = "Schema validation failed"

        # In production, would use PySpark SQL
        self.dead_letter_count += len(rows)

    @property
    def total_written(self) -> int:
        """Total rows written (valid + dead-letter)."""
        return self.written_count + self.dead_letter_count
