"""Built-in transformer steps. Spec: FEAT-003."""
from datetime import datetime
from .base import BaseTransformer


class DropNulls(BaseTransformer):
    """Remove rows where any of the specified columns are null/empty."""

    def __init__(self, columns: list[str]):
        self.columns = columns

    def transform(self, chunk: list[dict]) -> list[dict]:
        return [
            row for row in chunk
            if all(row.get(col) not in (None, "", "null") for col in self.columns)
        ]


class RenameColumns(BaseTransformer):
    """Rename columns according to a mapping dict."""

    def __init__(self, mapping: dict[str, str]):
        self.mapping = mapping

    def transform(self, chunk: list[dict]) -> list[dict]:
        result = []
        for row in chunk:
            new_row = {}
            for k, v in row.items():
                new_row[self.mapping.get(k, k)] = v
            result.append(new_row)
        return result


class CastTypes(BaseTransformer):
    """Cast column values to specified Python types.

    Supported types: int, float, str, bool, datetime
    """

    TYPE_MAP = {
        "int": int,
        "float": float,
        "str": str,
        "bool": lambda v: str(v).lower() in ("1", "true", "yes"),
        "datetime": lambda v: datetime.fromisoformat(str(v)) if v else None,
    }

    def __init__(self, columns: dict[str, str]):
        self.columns = columns

    def transform(self, chunk: list[dict]) -> list[dict]:
        result = []
        for row in chunk:
            new_row = dict(row)
            for col, type_name in self.columns.items():
                if col in new_row and new_row[col] is not None:
                    caster = self.TYPE_MAP.get(type_name)
                    if caster:
                        try:
                            new_row[col] = caster(new_row[col])
                        except (ValueError, TypeError):
                            new_row[col] = None
            result.append(new_row)
        return result


class FilterRows(BaseTransformer):
    """Keep only rows matching a Python expression.

    The expression has access to `row` as a dict.
    Example: "row['status'] == 'active' and row['amount'] > 0"
    """

    def __init__(self, expression: str):
        self.expression = expression
        self._compiled = compile(expression, "<filter>", "eval")

    def transform(self, chunk: list[dict]) -> list[dict]:
        result = []
        for row in chunk:
            try:
                if eval(self._compiled, {"__builtins__": {}}, {"row": row}):
                    result.append(row)
            except Exception:
                pass  # Skip rows that cause eval errors
        return result


class Deduplicate(BaseTransformer):
    """Remove duplicate rows based on key columns.

    Args:
        keys: Column names that define uniqueness.
        keep: 'first' or 'last'. Default: 'first'
    """

    def __init__(self, keys: list[str], keep: str = "first"):
        self.keys = keys
        self.keep = keep

    def transform(self, chunk: list[dict]) -> list[dict]:
        seen: dict = {}
        for row in chunk:
            key = tuple(row.get(k) for k in self.keys)
            if self.keep == "last" or key not in seen:
                seen[key] = row
        return list(seen.values())


class SchemaValidator(BaseTransformer):
    """Validate rows against a field schema. Invalid rows go to dead-letter.

    Schema format:
        {
            "field_name": {
                "type": "str" | "int" | "float" | "bool" | "datetime",
                "required": True,
                "min": 0,       # optional, numeric fields
                "max": 100,     # optional, numeric fields
                "pattern": "^[A-Z]"  # optional, string fields
            }
        }
    """

    PYTHON_TYPES = {"str": str, "int": int, "float": float, "bool": bool}

    def __init__(self, schema: dict):
        self.schema = schema
        self.last_invalid_rows: list[dict] = []

    def transform(self, chunk: list[dict]) -> list[dict]:
        import re
        valid = []
        self.last_invalid_rows = []
        for row in chunk:
            errors = []
            for field, rules in self.schema.items():
                value = row.get(field)
                required = rules.get("required", True)
                if value is None or value == "":
                    if required:
                        errors.append(f"Missing required field: {field}")
                    continue
                expected_type = self.PYTHON_TYPES.get(rules.get("type", "str"))
                if expected_type and not isinstance(value, expected_type):
                    try:
                        value = expected_type(value)
                        row = {**row, field: value}
                    except (ValueError, TypeError):
                        errors.append(f"Cannot cast {field} to {rules['type']}")
                        continue
                if "min" in rules and isinstance(value, (int, float)) and value < rules["min"]:
                    errors.append(f"{field} below minimum {rules['min']}")
                if "max" in rules and isinstance(value, (int, float)) and value > rules["max"]:
                    errors.append(f"{field} above maximum {rules['max']}")
                if "pattern" in rules and isinstance(value, str):
                    if not re.match(rules["pattern"], value):
                        errors.append(f"{field} does not match pattern")
            if errors:
                self.last_invalid_rows.append({**row, "_errors": errors})
            else:
                valid.append(row)
        return valid
