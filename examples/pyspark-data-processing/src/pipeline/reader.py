"""
CSV Reader with chunked iteration for memory safety.

Spec: FEAT-003 FR-1, FR-2
Memory-efficient reading of large CSV files.
"""

import csv
from pathlib import Path
from typing import Iterator
from .models import SalesRecord


class CSVReader:
    """
    Read CSV in chunks. Spec: FR-1, FR-2 — memory safe for any file size.

    Args:
        path: Local file path or s3://bucket/key
        chunk_size: Records per chunk (default 10,000)
        encoding: File encoding (default utf-8)
    """

    def __init__(self, path: str, chunk_size: int = 10_000, encoding: str = "utf-8"):
        self.path = path
        self.chunk_size = chunk_size
        self.encoding = encoding
        self._row_count = 0

    def read_chunks(self) -> Iterator[list[dict]]:
        """
        Yield chunks of records as dicts.

        Spec: FR-2 — yields list[dict] for memory safety
        NFR-2 — each chunk ~100KB, then released

        Yields:
            List of record dicts
        """
        chunk: list[dict] = []

        try:
            if self.path.startswith("s3://"):
                # S3 reading (requires boto3 + Spark, simplified here)
                yield from self._read_s3_chunks()
            else:
                # Local file reading
                with open(self.path, encoding=self.encoding, newline="") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        chunk.append(dict(row))
                        self._row_count += 1

                        if len(chunk) >= self.chunk_size:
                            yield chunk
                            chunk = []

                    # Yield remaining
                    if chunk:
                        yield chunk

        except FileNotFoundError as e:
            raise FileNotFoundError(f"CSV file not found: {self.path}") from e

    def _read_s3_chunks(self) -> Iterator[list[dict]]:
        """Read from S3. Spec: FR-1 — s3:// support."""
        # Simplified; would use boto3 + S3 select in production
        raise NotImplementedError("S3 reading requires PySpark or s3fs setup")

    @property
    def row_count(self) -> int:
        """Total rows read."""
        return self._row_count
