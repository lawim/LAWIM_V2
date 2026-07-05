from __future__ import annotations

import unittest

from lawim_v2.postgresql_repository import _PgConnection, _should_return_postgresql_id


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
