from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.persistence_adapter import resolve_persistence_adapter
from lawim_v2.repository_contract import LawimRepositoryContract


def _postgres_dsn() -> str:
    return os.getenv("LAWIM_TEST_POSTGRES_URL", "").strip()


class PostgreSQLReleaseCandidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dsn = _postgres_dsn()
        if not cls.dsn:
            raise unittest.SkipTest("LAWIM_TEST_POSTGRES_URL not set — PostgreSQL RC tests skipped")
        try:
            import pg8000  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("pg8000 not installed — pip install -r requirements-postgresql.txt") from exc

    def _open_repository(self):
        tempdir = tempfile.TemporaryDirectory()
        fallback = Path(tempdir.name) / "fallback.sqlite3"
        adapter = resolve_persistence_adapter(
            fallback,
            db_driver="postgresql",
            database_url=self.dsn,
            allow_sqlite_fallback=False,
        )
        repository = adapter.create_repository()
        self.addCleanup(repository.close)
        self.addCleanup(tempdir.cleanup)
        return repository

    def test_postgresql_schema_version_matches_application(self) -> None:
        repository = self._open_repository()
        repository.initialize(seed_demo_data=False)
        self.assertEqual(repository.schema_version(), APPLICATION_SCHEMA_VERSION)

    def test_postgresql_seeded_summary_counts(self) -> None:
        repository = self._open_repository()
        repository.initialize(seed_demo_data=True)
        summary = repository.summary()
        self.assertGreaterEqual(summary["organizations"], 3)
        self.assertGreaterEqual(summary["published_properties"], 1)

    def test_postgresql_authenticates_seeded_admin(self) -> None:
        repository = self._open_repository()
        repository.initialize(seed_demo_data=True)
        user = repository.authenticate(email="admin@lawim.local", password="lawim-demo")
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "admin")  # type: ignore[index]

    def test_postgresql_syncs_standard_demo_accounts_without_seed(self) -> None:
        repository = self._open_repository()
        repository.initialize(seed_demo_data=False)
        synced = repository.sync_standard_demo_accounts()
        self.assertEqual(len(synced), 5)
        self.assertIsNotNone(repository.authenticate(identifier="admin", password="LAWIM@Demo2026µ"))
        self.assertIsNotNone(repository.authenticate(identifier="+237686822668", password="LAWIM@Demo2026µ"))
        self.assertIsNotNone(repository.authenticate(identifier="investor@lawim.app", password="LAWIM@Demo2026µ"))

    def test_postgresql_lists_properties_with_pagination(self) -> None:
        repository = self._open_repository()
        repository.initialize(seed_demo_data=True)
        payload = repository.list_properties(page=1, limit=5)
        items = payload.get("items") or []
        pagination = payload.get("pagination") or {}
        self.assertIsInstance(items, list)
        self.assertGreaterEqual(int(pagination.get("total", 0)), 1)
        self.assertLessEqual(len(items), 5)

    def test_postgresql_repository_satisfies_contract(self) -> None:
        repository = self._open_repository()
        self.assertIsInstance(repository, LawimRepositoryContract)
