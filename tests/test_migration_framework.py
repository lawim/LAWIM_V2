from __future__ import annotations

import sqlite3
from unittest import TestCase

from lawim_v2.migration import (
    MigrationEngine,
    MigrationHistory,
    MigrationPlanner,
    MigrationRegistry,
    MigrationRunner,
    MigrationState,
    MigrationStep,
    MigrationValidator,
    RollbackManager,
)


class MigrationFrameworkTest(TestCase):
    def test_registry_plans_upgrade_to_current_schema(self) -> None:
        registry = MigrationRegistry(
            (
                MigrationStep(
                    name="legacy-to-v18",
                    from_version=5,
                    to_version=18,
                    target_backend="sqlite",
                    apply=lambda context: None,
                    rollback=lambda context: None,
                ),
            )
        )
        planner = MigrationPlanner(registry)
        plan = planner.plan(current_version=5, target_version=18, backend="sqlite")
        self.assertEqual([entry.name for entry in plan], ["legacy-to-v18"])

    def test_runner_applies_and_records_history(self) -> None:
        connection = sqlite3.connect(":memory:")
        connection.execute("CREATE TABLE demo (id INTEGER PRIMARY KEY)")

        def apply_step(context) -> None:
            connection.execute("CREATE TABLE migration_state (id INTEGER PRIMARY KEY)")
            context.state.current_version = context.target_version

        registry = MigrationRegistry(
            (
                MigrationStep(
                    name="bootstrap-schema",
                    from_version=1,
                    to_version=18,
                    target_backend="sqlite",
                    apply=apply_step,
                    rollback=lambda context: None,
                ),
            )
        )
        runner = MigrationRunner(registry, MigrationValidator())
        result = runner.run(
            current_version=1,
            target_version=18,
            backend="sqlite",
            connection=connection,
            dry_run=False,
            state=MigrationState(current_version=1, target_version=18),
            history=MigrationHistory(),
        )
        self.assertTrue(result.success)
        self.assertEqual(result.state.current_version, 18)
        self.assertEqual(result.history.entries[-1].status, "applied")

    def test_validator_rejects_missing_schema_meta(self) -> None:
        connection = sqlite3.connect(":memory:")
        validator = MigrationValidator()
        with self.assertRaises(ValueError):
            validator.validate(connection=connection, expected_version=18)

    def test_rollback_manager_reports_unsupported_downgrade(self) -> None:
        registry = MigrationRegistry(
            (
                MigrationStep(
                    name="bootstrap-schema",
                    from_version=18,
                    to_version=5,
                    target_backend="sqlite",
                    apply=lambda context: None,
                    rollback=None,
                ),
            )
        )
        manager = RollbackManager(registry)
        result = manager.plan_rollback(current_version=18, target_version=5, backend="sqlite")
        self.assertFalse(result.can_rollback)
        self.assertIn("rollback", result.reason.lower())
