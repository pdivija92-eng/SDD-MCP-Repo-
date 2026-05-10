"""Tests for transformer steps. References: FEAT-003."""
import pytest
from src.transformers import (
    DropNulls, RenameColumns, CastTypes, FilterRows,
    Deduplicate, SchemaValidator, TransformerPipeline,
)


SAMPLE = [
    {"id": "1", "name": "Alice", "amount": "10.5", "status": "active"},
    {"id": "2", "name": None,    "amount": "20.0", "status": "inactive"},
    {"id": "3", "name": "Carol", "amount": None,   "status": "active"},
    {"id": "1", "name": "Alice", "amount": "10.5", "status": "active"},  # duplicate
]


class TestDropNulls:
    def test_drops_null_rows(self):
        result = DropNulls(columns=["name"]).transform(SAMPLE)
        assert len(result) == 3
        assert all(r["name"] is not None for r in result)

    def test_does_not_mutate_input(self):
        original = [dict(r) for r in SAMPLE]
        DropNulls(columns=["name"]).transform(SAMPLE)
        assert SAMPLE == original


class TestRenameColumns:
    def test_renames(self):
        chunk = [{"old_name": "x", "keep": "y"}]
        result = RenameColumns({"old_name": "new_name"}).transform(chunk)
        assert "new_name" in result[0]
        assert "old_name" not in result[0]
        assert result[0]["keep"] == "y"


class TestCastTypes:
    def test_casts_float(self):
        chunk = [{"amount": "19.99"}]
        result = CastTypes({"amount": "float"}).transform(chunk)
        assert result[0]["amount"] == 19.99

    def test_casts_int(self):
        chunk = [{"count": "42"}]
        result = CastTypes({"count": "int"}).transform(chunk)
        assert result[0]["count"] == 42

    def test_invalid_cast_returns_none(self):
        chunk = [{"amount": "not_a_number"}]
        result = CastTypes({"amount": "float"}).transform(chunk)
        assert result[0]["amount"] is None


class TestFilterRows:
    def test_filters(self):
        chunk = [{"status": "active"}, {"status": "inactive"}, {"status": "active"}]
        result = FilterRows("row['status'] == 'active'").transform(chunk)
        assert len(result) == 2

    def test_numeric_filter(self):
        chunk = [{"amount": 5}, {"amount": 15}, {"amount": 25}]
        result = FilterRows("row['amount'] > 10").transform(chunk)
        assert len(result) == 2


class TestDeduplicate:
    def test_deduplicates(self):
        result = Deduplicate(keys=["id", "name"]).transform(SAMPLE)
        ids = [r["id"] for r in result]
        assert ids.count("1") == 1

    def test_keep_last(self):
        chunk = [{"id": "1", "val": "first"}, {"id": "1", "val": "last"}]
        result = Deduplicate(keys=["id"], keep="last").transform(chunk)
        assert result[0]["val"] == "last"


class TestSchemaValidator:
    def test_valid_rows_pass(self):
        schema = {"id": {"type": "str", "required": True}}
        chunk = [{"id": "1"}, {"id": "2"}]
        validator = SchemaValidator(schema)
        result = validator.transform(chunk)
        assert len(result) == 2
        assert len(validator.last_invalid_rows) == 0

    def test_missing_required_goes_to_dead_letter(self):
        schema = {"id": {"type": "str", "required": True}}
        chunk = [{"id": "1"}, {"name": "no_id"}]
        validator = SchemaValidator(schema)
        result = validator.transform(chunk)
        assert len(result) == 1
        assert len(validator.last_invalid_rows) == 1

    def test_min_max_validation(self):
        schema = {"amount": {"type": "float", "required": True, "min": 0, "max": 100}}
        chunk = [{"amount": 50.0}, {"amount": -1.0}, {"amount": 200.0}]
        validator = SchemaValidator(schema)
        result = validator.transform(chunk)
        assert len(result) == 1
        assert len(validator.last_invalid_rows) == 2


class TestTransformerPipeline:
    def test_pipeline_applies_steps_in_order(self):
        """FEAT-003 FR-2: Steps are applied sequentially."""
        chunk = [
            {"sale_id": "1", "sale_amount": "10.5", "status": "active"},
            {"sale_id": None, "sale_amount": "5.0", "status": "active"},
        ]
        pipeline = TransformerPipeline(steps=[
            DropNulls(columns=["sale_id"]),
            RenameColumns({"sale_amount": "amount"}),
            CastTypes({"amount": "float"}),
        ])
        result = pipeline.run(chunk)
        assert len(result) == 1
        assert result[0]["amount"] == 10.5
        assert "sale_amount" not in result[0]
