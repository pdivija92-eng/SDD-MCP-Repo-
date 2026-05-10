"""PostgreSQL loader with append, replace, and upsert modes. Spec: FEAT-004."""
from .base import BaseLoader, LoaderConnectionError, LoaderError


class DBLoader(BaseLoader):
    """Writes records to PostgreSQL using batch inserts.

    Args:
        dsn: PostgreSQL connection string.
        table: Schema-qualified table name (e.g. 'public.sales').
        mode: 'append', 'replace', or 'upsert'.
        conflict_key: Column name for upsert conflict resolution.
        batch_size: Rows per INSERT statement. Default: 5000
    """

    def __init__(
        self,
        dsn: str,
        table: str,
        mode: str = "append",
        conflict_key: str | None = None,
        batch_size: int = 5_000,
    ):
        super().__init__()
        self.dsn = dsn
        self.table = table
        self.mode = mode
        self.conflict_key = conflict_key
        self.batch_size = batch_size
        self._conn = None
        self._replaced = False

    def connect(self) -> None:
        try:
            import psycopg2
            self._conn = psycopg2.connect(self.dsn)
            self._conn.autocommit = False
        except Exception as e:
            raise LoaderConnectionError(
                f"Failed to connect to database: {e}"
            ) from e

    def load(self, chunk: list[dict]) -> None:
        if not chunk:
            return
        if self._conn is None:
            raise LoaderError("Not connected.")
        try:
            import psycopg2.extras
            cursor = self._conn.cursor()

            if self.mode == "replace" and not self._replaced:
                cursor.execute(f"TRUNCATE TABLE {self.table}")
                self._replaced = True

            columns = list(chunk[0].keys())
            col_str = ", ".join(f'"{c}"' for c in columns)
            placeholders = ", ".join(["%s"] * len(columns))

            if self.mode == "upsert" and self.conflict_key:
                updates = ", ".join(
                    f'"{c}" = EXCLUDED."{c}"'
                    for c in columns if c != self.conflict_key
                )
                sql = (
                    f'INSERT INTO {self.table} ({col_str}) VALUES ({placeholders}) '
                    f'ON CONFLICT ("{self.conflict_key}") DO UPDATE SET {updates}'
                )
            else:
                sql = f"INSERT INTO {self.table} ({col_str}) VALUES ({placeholders})"

            rows = [tuple(row[c] for c in columns) for row in chunk]
            psycopg2.extras.execute_batch(cursor, sql, rows, page_size=self.batch_size)
            cursor.close()
            self._rows_loaded += len(chunk)
        except Exception as e:
            raise LoaderError(f"Error writing to {self.table}: {e}") from e

    def commit(self) -> None:
        if self._conn:
            self._conn.commit()

    def _rollback(self) -> None:
        if self._conn:
            try:
                self._conn.rollback()
            except Exception:
                pass

    def close(self) -> None:
        if self._conn:
            self._conn.close()
        self._conn = None
