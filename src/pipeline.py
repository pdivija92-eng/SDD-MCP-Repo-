"""Pipeline Runner — orchestrates Extract → Transform → Load. Spec: FEAT-001."""
from __future__ import annotations

import os
import re
import time
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from src.extractors import CSVExtractor, DBExtractor, APIExtractor, BaseExtractor
from src.loaders import DBLoader, S3Loader, BaseLoader
from src.transformers import (
    TransformerPipeline, STEP_REGISTRY,
    DropNulls, RenameColumns, CastTypes, FilterRows, Deduplicate, SchemaValidator,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class RunSummary:
    pipeline: str
    status: str = "pending"
    rows_extracted: int = 0
    rows_transformed: int = 0
    rows_loaded: int = 0
    rows_rejected: int = 0
    duration_seconds: float = 0.0
    error: str | None = None


def interpolate_env(value: Any) -> Any:
    """Replace ${VAR} tokens in strings with environment variable values."""
    if isinstance(value, str):
        def replace(match):
            var = match.group(1)
            result = os.environ.get(var)
            if result is None:
                raise EnvironmentError(f"Required environment variable not set: ${{{var}}}")
            return result
        return re.sub(r"\$\{([^}]+)\}", replace, value)
    elif isinstance(value, dict):
        return {k: interpolate_env(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [interpolate_env(v) for v in value]
    return value


def build_extractor(config: dict) -> BaseExtractor:
    cfg = interpolate_env(config)
    ext_type = cfg.get("type")
    if ext_type == "csv":
        return CSVExtractor(
            path=cfg["path"],
            delimiter=cfg.get("delimiter", ","),
            encoding=cfg.get("encoding", "utf-8"),
            chunk_size=cfg.get("chunk_size", 10_000),
        )
    elif ext_type == "postgres":
        return DBExtractor(
            dsn=cfg["dsn"],
            query=cfg["query"],
            chunk_size=cfg.get("chunk_size", 1_000),
            params=cfg.get("params"),
        )
    elif ext_type == "api":
        return APIExtractor(
            url=cfg["url"],
            auth=cfg.get("auth"),
            pagination=cfg.get("pagination"),
            page_size=cfg.get("page_size", 100),
            max_pages=cfg.get("max_pages"),
            headers=cfg.get("headers"),
        )
    raise ValueError(f"Unknown extractor type: {ext_type}")


def build_transformer_pipeline(config: dict | None) -> TransformerPipeline:
    if not config:
        return TransformerPipeline(steps=[])
    steps = []
    for step_cfg in config.get("steps", []):
        step_type = step_cfg.get("type")
        cls = STEP_REGISTRY.get(step_type)
        if not cls:
            raise ValueError(f"Unknown transformer step: {step_type}")
        cfg = {k: v for k, v in step_cfg.items() if k != "type"}
        # Map config keys to constructor args
        if step_type == "drop_nulls":
            steps.append(DropNulls(columns=cfg["columns"]))
        elif step_type == "rename_columns":
            steps.append(RenameColumns(mapping=cfg["mapping"]))
        elif step_type == "cast_types":
            steps.append(CastTypes(columns=cfg["columns"]))
        elif step_type == "filter_rows":
            steps.append(FilterRows(expression=cfg["expression"]))
        elif step_type == "deduplicate":
            steps.append(Deduplicate(keys=cfg["keys"], keep=cfg.get("keep", "first")))
        elif step_type == "validate_schema":
            steps.append(SchemaValidator(schema=cfg["schema"]))
    return TransformerPipeline(steps=steps)


def build_loader(config: dict) -> BaseLoader:
    cfg = interpolate_env(config)
    loader_type = cfg.get("type")
    if loader_type == "postgres":
        return DBLoader(
            dsn=cfg["dsn"],
            table=cfg["table"],
            mode=cfg.get("mode", "append"),
            conflict_key=cfg.get("conflict_key"),
            batch_size=cfg.get("batch_size", 5_000),
        )
    elif loader_type == "s3":
        return S3Loader(
            bucket=cfg["bucket"],
            prefix=cfg["prefix"],
            format=cfg.get("format", "parquet"),
            partition_by=cfg.get("partition_by"),
            compression=cfg.get("compression", "snappy"),
        )
    raise ValueError(f"Unknown loader type: {loader_type}")


def run_pipeline(config_path: str, dry_run: bool = False) -> RunSummary:
    """Execute a pipeline from a YAML config file.

    Args:
        config_path: Path to the pipeline YAML config.
        dry_run: If True, skip the load step.

    Returns:
        RunSummary with row counts and status.
    """
    config = yaml.safe_load(Path(config_path).read_text())
    pipeline_name = config.get("name", config_path)
    summary = RunSummary(pipeline=pipeline_name)
    retry_cfg = config.get("retry", {})
    max_attempts = retry_cfg.get("max_attempts", 3)
    backoff = retry_cfg.get("backoff_seconds", 5)

    logger.info(f"Starting pipeline: {pipeline_name}", extra={"dry_run": dry_run})
    start = time.time()

    try:
        extractor = build_extractor(config["extractor"])
        transformer = build_transformer_pipeline(config.get("transformer"))
        loader = build_loader(config["loader"]) if not dry_run else None

        with extractor:
            if loader:
                loader.connect()
            try:
                for chunk in extractor.extract():
                    summary.rows_extracted += len(chunk)
                    valid_chunk = transformer.run(chunk)
                    summary.rows_transformed += len(valid_chunk)
                    summary.rows_rejected += len(transformer.invalid_rows)

                    if loader and valid_chunk:
                        attempt = 0
                        while True:
                            try:
                                loader.load(valid_chunk)
                                break
                            except Exception as e:
                                attempt += 1
                                if attempt >= max_attempts:
                                    raise
                                logger.warning(f"Load attempt {attempt} failed: {e}. Retrying in {backoff}s...")
                                time.sleep(backoff)

                if loader:
                    loader.commit()
                    summary.rows_loaded = loader.rows_loaded
            except Exception:
                if loader:
                    loader._rollback()
                raise
            finally:
                if loader:
                    loader.close()

        summary.status = "dry_run" if dry_run else "success"
        logger.info(
            f"Pipeline complete: {pipeline_name}",
            extra={
                "rows_extracted": summary.rows_extracted,
                "rows_transformed": summary.rows_transformed,
                "rows_loaded": summary.rows_loaded,
                "rows_rejected": summary.rows_rejected,
            }
        )

    except Exception as e:
        summary.status = "failed"
        summary.error = str(e)
        logger.error(f"Pipeline failed: {pipeline_name}: {e}", exc_info=True)

    summary.duration_seconds = round(time.time() - start, 2)
    return summary


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Run an ETL pipeline")
    parser.add_argument("command", choices=["run"])
    parser.add_argument("--config", required=True, help="Path to pipeline YAML config")
    parser.add_argument("--dry-run", action="store_true", help="Skip the load step")
    args = parser.parse_args()

    summary = run_pipeline(args.config, dry_run=args.dry_run)
    print(f"\n{'='*50}")
    print(f"Pipeline:    {summary.pipeline}")
    print(f"Status:      {summary.status}")
    print(f"Extracted:   {summary.rows_extracted}")
    print(f"Transformed: {summary.rows_transformed}")
    print(f"Loaded:      {summary.rows_loaded}")
    print(f"Rejected:    {summary.rows_rejected}")
    print(f"Duration:    {summary.duration_seconds}s")
    if summary.error:
        print(f"Error:       {summary.error}")
    print('='*50)

    sys.exit(0 if summary.status in ("success", "dry_run") else 1)
