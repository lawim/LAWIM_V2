from __future__ import annotations

import os
import unittest
from pathlib import Path

from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.persistence_adapter import resolve_persistence_adapter
from lawim_v2.repository_contract import LawimRepositoryContract
from lawim_v2.schema_ddl import normalized_ddl_fingerprint


class ProductizationContractTest(unittest.TestCase):
    def test_repository_satisfies_runtime_contract(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tempdir:
            db_path = Path(tempdir) / "lawim.sqlite3"
            adapter = resolve_persistence_adapter(
                db_path,
                db_driver="sqlite",
                database_url="postgresql://lawim:lawim@localhost:5432/lawim_v2",
                allow_sqlite_fallback=True,
            )
            repository = adapter.create_repository()
            self.assertIsInstance(repository, LawimRepositoryContract)
            repository.initialize(seed_demo_data=True)
            summary = repository.summary()
            self.assertEqual(summary["organizations"], 3)
            repository.close()

    def test_schema_ddl_fingerprint_is_stable(self) -> None:
        fingerprint = normalized_ddl_fingerprint()
        self.assertEqual(len(fingerprint), 64)
        self.assertEqual(APPLICATION_SCHEMA_VERSION, 16)

    def test_compose_alias_tree_points_to_canonical_compose(self) -> None:
        root = Path(__file__).resolve().parent.parent
        alias_dir = root / "docker" / "compose"
        expected = {
            "docker-compose.base.yml": "../../compose/docker-compose.base.yml",
            "docker-compose.development.yml": "../../compose/docker-compose.dev.yml",
            "docker-compose.staging.yml": "../../compose/docker-compose.staging.yml",
            "docker-compose.production.yml": "../../compose/docker-compose.prod.yml",
            "docker-compose.postgres.yml": "../../compose/docker-compose.postgres.yml",
        }
        for filename, target in expected.items():
            link = alias_dir / filename
            self.assertTrue(link.is_symlink(), msg=filename)
            self.assertEqual(os.readlink(link), target, msg=filename)
            self.assertTrue((alias_dir / target).resolve().is_file(), msg=filename)


class PostgreSQLIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dsn = os.getenv("LAWIM_TEST_POSTGRES_URL", "").strip()
        if not cls.dsn:
            raise unittest.SkipTest("LAWIM_TEST_POSTGRES_URL not set — PostgreSQL integration skipped")

        try:
            import pg8000  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("pg8000 not installed — pip install -r requirements-postgresql.txt") from exc

    def test_postgresql_repository_initializes_and_seeds(self) -> None:
        import tempfile

        tempdir = tempfile.TemporaryDirectory()
        fallback = Path(tempdir.name) / "fallback.sqlite3"
        adapter = resolve_persistence_adapter(
            fallback,
            db_driver="postgresql",
            database_url=self.dsn,
            allow_sqlite_fallback=False,
        )
        repository = adapter.create_repository()
        self.assertIsInstance(repository, LawimRepositoryContract)
        try:
            repository.initialize(seed_demo_data=True)
            profile = repository.backend_profile()
            self.assertEqual(profile["driver"], "postgresql")
            self.assertEqual(repository.schema_version(), APPLICATION_SCHEMA_VERSION)
            summary = repository.summary()
            self.assertGreaterEqual(summary["organizations"], 3)
        finally:
            repository.close()
            tempdir.cleanup()
