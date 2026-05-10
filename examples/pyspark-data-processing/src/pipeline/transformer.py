"""
Data transformer with validation and cleaning.

Spec: FEAT-003 FR-3, FR-4, FR-5
Validates records, routes invalid ones to dead-letter, applies transformations.
"""

from typing import Any
from pydantic import ValidationError
from .models import SalesRecord


class DataTransformer:
    """
    Validate and transform records. Spec: FR-3, FR-4, FR-5.

    Handles:
    - Schema validation (Pydantic)
    - Dead-letter routing (invalid records)
    - Transformations (dedup, type cast, filter)
    """

    def __init__(self):
        self.validated_count = 0
        self.invalid_count = 0
        self._seen_keys = set()  # for deduplication

    def transform_chunk(
        self,
        chunk: list[dict],
        schema: type = SalesRecord,
    ) -> tuple[list[dict], list[dict], list[str]]:
        """
        Validate and transform a chunk of records.

        Args:
            chunk: List of record dicts from CSV
            schema: Pydantic model for validation

        Returns:
            (valid_records, invalid_records, errors)

        Spec: FR-3 — Pydantic validation
        Spec: FR-4 — Invalid rows collected separately
        Spec: FR-5 — Transformations applied
        """
        valid: list[dict] = []
        invalid: list[dict] = []
        errors: list[str] = []

        for i, row in enumerate(chunk):
            try:
                # Validate schema
                record = schema(**row)

                # Deduplication (FR-5)
                key = (record.sale_id, record.customer_id)
                if key in self._seen_keys:
                    continue  # skip duplicate
                self._seen_keys.add(key)

                # Convert back to dict (type-cast applied by Pydantic)
                valid.append(record.dict())
                self.validated_count += 1

            except ValidationError as e:
                invalid.append(row)
                error_msg = f"Row {i}: {e.errors()[0]['msg']}"
                errors.append(error_msg)
                self.invalid_count += 1

        return valid, invalid, errors

    def reset_dedup(self):
        """Reset deduplication state between runs."""
        self._seen_keys.clear()
