"""
Main pipeline orchestrator.

Spec: FEAT-003 — Full ETL workflow
"""

import time
import logging
from .models import PipelineConfig, PipelineStats
from .reader import CSVReader
from .transformer import DataTransformer
from .writer import DeltaWriter


logger = logging.getLogger(__name__)


class Pipeline:
    """
    Main ETL orchestrator. Spec: FEAT-003 FR-8, FR-9.

    Coordinates:
    1. Read CSV in chunks
    2. Validate and transform each chunk
    3. Write valid to Delta, invalid to dead-letter
    4. Log statistics
    """

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.stats = PipelineStats()

    def run(self) -> PipelineStats:
        """
        Execute the pipeline end-to-end.

        Spec: FR-8 — Logs row counts at each stage
        Spec: FR-9 — Retries on transient failures
        NFR-1 — Targets 1M rows in <5 min
        NFR-2 — Memory bounded
        """
        start_time = time.time()
        self.stats.status = "running"

        try:
            reader = CSVReader(self.config.input_path, self.config.chunk_size)
            transformer = DataTransformer()
            writer = DeltaWriter(
                self.config.output_table,
                self.config.dead_letter_table,
                self.config.write_mode,
                self.config.upsert_key,
            )

            # Process chunks
            for i, chunk in enumerate(reader.read_chunks()):
                self.stats.rows_read += len(chunk)

                # Validate and transform
                valid, invalid, errors = transformer.transform_chunk(chunk)
                self.stats.rows_validated += len(valid)
                self.stats.rows_rejected += len(invalid)
                self.stats.errors.extend(errors)

                # Write
                writer.write(valid, invalid)
                self.stats.rows_written += writer.total_written

                if i % 10 == 0:
                    logger.info(
                        f"Chunk {i}: read={len(chunk)}, "
                        f"valid={len(valid)}, invalid={len(invalid)}"
                    )

            self.stats.status = "success"

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self.stats.status = "failed"
            self.stats.errors.append(str(e))
            raise

        finally:
            self.stats.duration_seconds = time.time() - start_time
            self._log_summary()

        return self.stats

    def _log_summary(self):
        """Log pipeline summary. Spec: FR-8."""
        logger.info(
            f"Pipeline {self.stats.status}: "
            f"read={self.stats.rows_read}, "
            f"valid={self.stats.rows_validated}, "
            f"invalid={self.stats.rows_rejected}, "
            f"written={self.stats.rows_written}, "
            f"duration={self.stats.duration_seconds:.1f}s"
        )
