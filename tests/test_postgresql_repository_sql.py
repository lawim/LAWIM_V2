from __future__ import annotations

import unittest

from lawim_v2.db import LawimRepository
from lawim_v2.postgresql_repository import _PgConnection, _should_return_postgresql_id
from lawim_v2.repository_introspection import table_exists, tables_present
from lawim_v2.security.repository import SecurityRepositoryMixin


class _FakeNativeConnection:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []
        self.columns: list[dict[str, str]] = []

    def run(self, sql: str, **params: object) -> list[dict[str, object]]:
        self.calls.append((sql, params))
        if "INSERT INTO users" in sql:
            self.columns = [{"name": "id"}]
            return [(42,)]
        self.columns = [{"name": "token"}, {"name": "user_id"}]
        return []


class PostgreSQLRepositorySqlTest(unittest.TestCase):
    def test_returning_id_is_enabled_for_id_tables(self) -> None:
        self.assertTrue(_should_return_postgresql_id("INSERT INTO users (email) VALUES ($1)"))
        self.assertTrue(_should_return_postgresql_id("INSERT INTO organizations (name) VALUES ($1)"))

    def test_returning_id_is_disabled_for_token_primary_key_tables(self) -> None:
        self.assertFalse(_should_return_postgresql_id("INSERT INTO sessions (token, user_id) VALUES ($1, $2)"))

    def test_execute_leaves_sessions_insert_without_returning_clause(self) -> None:
        native = _FakeNativeConnection()
        connection = _PgConnection(native)

        cursor = connection.execute(
            "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
            ("token-1", 1, "2026-07-05T00:00:00Z", "2026-07-06T00:00:00Z"),
        )

        self.assertEqual(native.calls[0][0], "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES ($1, $2, $3, $4)")
        self.assertIsNone(cursor.lastrowid)

    def test_execute_keeps_returning_id_for_users_insert(self) -> None:
        native = _FakeNativeConnection()
        connection = _PgConnection(native)

        cursor = connection.execute(
            "INSERT INTO users (email, full_name, role, organization_id, password_salt, password_hash, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("owner@example.com", "Owner", "owner", None, "salt", "hash", "2026-07-05T00:00:00Z"),
        )

        self.assertIn("RETURNING id", native.calls[0][0])
        self.assertEqual(cursor.lastrowid, 42)


class _FakeIntrospectionRepository:
    def __init__(self, driver: str, rows: list[dict[str, object]]) -> None:
        self.driver = driver
        self.rows = rows
        self.calls: list[tuple[str, tuple[object, ...]]] = []

    def all(self, sql: str, params: tuple[object, ...] = ()) -> list[dict[str, object]]:
        self.calls.append((sql, params))
        return self.rows


class _FakeColumnsCursor:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self._rows = rows

    def fetchall(self) -> list[dict[str, object]]:
        return self._rows


class _FakeColumnsConnection:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self.rows = rows
        self.calls: list[tuple[str, tuple[object, ...]]] = []

    def execute(self, sql: str, params: tuple[object, ...] = ()) -> _FakeColumnsCursor:
        self.calls.append((sql, params))
        return _FakeColumnsCursor(self.rows)


class _SecurityStatsRepository(SecurityRepositoryMixin):
    driver = "postgresql"

    def __init__(self) -> None:
        self.scalar_calls: list[tuple[str, tuple[object, ...]]] = []

    def scalar(self, sql: str, params: tuple[object, ...] = ()) -> int:
        self.scalar_calls.append((sql, params))
        return 0

    def list_audit_trail(self, limit: int = 5) -> list[dict[str, object]]:
        return []

    def list_security_incidents(self, status: str, limit: int = 5) -> list[dict[str, object]]:
        return []

    def list_risk_alerts(self, status: str, limit: int = 5) -> list[dict[str, object]]:
        return []

    def integration_sources(self) -> list[dict[str, object]]:
        return []


class PostgreSQLCompatibilityTest(unittest.TestCase):
    def test_tables_present_uses_information_schema_for_postgresql(self) -> None:
        repository = _FakeIntrospectionRepository(
            "postgresql",
            [{"name": "assistant_sessions"}, {"name": "assistant_agents"}],
        )

        self.assertTrue(tables_present(repository, ("assistant_sessions", "assistant_agents")))
        self.assertIn("information_schema.tables", repository.calls[0][0])
        self.assertEqual(repository.calls[0][1], ("assistant_sessions", "assistant_agents"))

    def test_table_exists_uses_sqlite_catalog_for_sqlite_driver(self) -> None:
        repository = _FakeIntrospectionRepository("sqlite", [{"name": "analytics_events"}])

        self.assertTrue(table_exists(repository, "analytics_events"))
        self.assertIn("sqlite_master", repository.calls[0][0])

    def test_table_columns_switches_to_information_schema_for_postgresql(self) -> None:
        repository = type("FakeRepository", (), {"driver": "postgresql"})()
        connection = _FakeColumnsConnection(
            [{"column_name": "id"}, {"column_name": "provider_name"}, {"column_name": "caption"}]
        )

        columns = LawimRepository._table_columns(repository, connection, "media")

        self.assertEqual(columns, {"id", "provider_name", "caption"})
        self.assertIn("information_schema.columns", connection.calls[0][0])

    def test_security_stats_uses_bound_cutoff_instead_of_sqlite_datetime(self) -> None:
        repository = _SecurityStatsRepository()

        repository.security_stats()

        audit_query, audit_params = next(
            (sql, params) for sql, params in repository.scalar_calls if "audit_trail_entries" in sql
        )
        self.assertIn("created_at >= ?", audit_query)
        self.assertNotIn("datetime(", audit_query)
        self.assertEqual(len(audit_params), 1)
        self.assertRegex(str(audit_params[0]), r"^\d{4}-\d{2}-\d{2}T")
