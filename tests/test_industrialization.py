from __future__ import annotations

import importlib.metadata
import tempfile
import unittest
from pathlib import Path

from lawim_v2.db import LawimRepository
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT, validate_manifest_table_alignment
from lawim_v2.schema_migrations import PRODUCTION_MIGRATION_TOOL, apply_sqlite_legacy_migrations, migration_strategy_profile


class UnifiedPersistenceTest(unittest.TestCase):
    def test_manifest_aligns_with_sqlite_and_postgresql_ddl(self) -> None:
        errors = validate_manifest_table_alignment()
        self.assertEqual(errors, [])

    def test_sqlite_init_script_is_canonical(self) -> None:
        self.assertIn("CREATE TABLE IF NOT EXISTS organizations", SQLITE_INIT_SCRIPT)
        self.assertIn("CREATE TABLE IF NOT EXISTS notifications", SQLITE_INIT_SCRIPT)
        self.assertIn("idx_notifications_user_read", SQLITE_INIT_SCRIPT)

    def test_legacy_migrations_are_idempotent_on_fresh_database(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            db_path = Path(tempdir) / "legacy.sqlite3"
            repository = LawimRepository(db_path)
            repository.initialize(seed_demo_data=False)
            with repository._transaction() as conn:  # noqa: SLF001 — migration contract test
                apply_sqlite_legacy_migrations(conn)
            self.assertEqual(repository.schema_version(), APPLICATION_SCHEMA_VERSION)
            repository.close()

    def test_migration_strategy_documents_prisma_for_production(self) -> None:
        profile = migration_strategy_profile()
        self.assertEqual(profile["production_tool"], PRODUCTION_MIGRATION_TOOL)
        self.assertEqual(profile["schema_version"], APPLICATION_SCHEMA_VERSION)


class PackagingMetadataTest(unittest.TestCase):
    def test_pyproject_declares_package_name(self) -> None:
        root = Path(__file__).resolve().parent.parent
        pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('name = "lawim-v2"', pyproject)
        self.assertIn("lawim_v2.__main__:main", pyproject)

    def test_package_version_is_exposed(self) -> None:
        import lawim_v2

        self.assertEqual(lawim_v2.__version__, "0.1.0")

    def test_distribution_metadata_when_installed(self) -> None:
        try:
            version = importlib.metadata.version("lawim-v2")
        except importlib.metadata.PackageNotFoundError:
            raise unittest.SkipTest("lawim-v2 not installed — run validate-packaging.sh")
        self.assertEqual(version, "0.1.0")
