"""CSV extractor — reads local CSV/TSV files in chunks. Spec: FEAT-002."""
import csv
from pathlib import Path
from typing import Iterator

from .base import BaseExtractor, ExtractorConnectionError, ExtractorError


class CSVExtractor(BaseExtractor):
    """Reads a CSV file in chunks. Memory-safe for files of any size.

    Args:
        path: Path to the CSV file.
        delimiter: Column delimiter. Default: ','
        encoding: File encoding. Default: 'utf-8'
        chunk_size: Number of rows per chunk. Default: 10000
        skip_header: Whether the first row is a header. Default: True
    """

    def __init__(
        self,
        path: str,
        delimiter: str = ",",
        encoding: str = "utf-8",
        chunk_size: int = 10_000,
        skip_header: bool = True,
    ):
        super().__init__()
        self.path = Path(path)
        self.delimiter = delimiter
        self.encoding = encoding
        self.chunk_size = chunk_size
        self.skip_header = skip_header
        self._file = None
        self._reader = None

    def connect(self) -> None:
        if not self.path.exists():
            raise ExtractorConnectionError(f"CSV file not found: {self.path}")
        if not self.path.is_file():
            raise ExtractorConnectionError(f"Path is not a file: {self.path}")

    def extract(self) -> Iterator[list[dict]]:
        try:
            with open(self.path, encoding=self.encoding, newline="") as f:
                reader = csv.DictReader(f, delimiter=self.delimiter)
                chunk: list[dict] = []
                for row in reader:
                    chunk.append(dict(row))
                    self._row_count += 1
                    if len(chunk) >= self.chunk_size:
                        yield chunk
                        chunk = []
                if chunk:
                    yield chunk
        except (OSError, csv.Error) as e:
            raise ExtractorError(f"Error reading CSV {self.path}: {e}") from e

    def close(self) -> None:
        pass  # File is opened/closed per-extract call
