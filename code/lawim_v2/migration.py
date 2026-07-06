from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from typing import Callable


@dataclass(slots=True)
class MigrationContext:
    connection: sqlite3.Connection
    current_version: int
    target_version: int
    backend: str
    state: "MigrationState"
    history: "MigrationHistory"


@dataclass(slots=True)
class MigrationState:
    current_version: int
    target_version: int
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class MigrationHistoryEntry:
    name: str
    from_version: int
    to_version: int
    backend: str
    status: str
    detail: str = ""


@dataclass(slots=True)
class MigrationHistory:
    entries: list[MigrationHistoryEntry] = field(default_factory=list)

    def add(self, entry: MigrationHistoryEntry) -> None:
        self.entries.append(entry)


@dataclass(slots=True)
class MigrationStep:
    name: str
    from_version: int
    to_version: int
    target_backend: str
    apply: Callable[[MigrationContext], None]
    rollback: Callable[[MigrationContext], None] | None = None


@dataclass(slots=True)
class MigrationRegistry:
    steps: tuple[MigrationStep, ...]

    def matching(self, *, current_version: int, target_version: int, backend: str) -> list[MigrationStep]:
        return [
            step
            for step in self.steps
            if step.target_backend in {backend, "all"}
            and step.from_version >= current_version
            and step.to_version <= target_version
            and step.from_version < step.to_version
        ]


@dataclass(slots=True)
class MigrationPlanEntry:
    name: str
    from_version: int
    to_version: int
    backend: str


@dataclass(slots=True)
class MigrationPlan:
    entries: list[MigrationPlanEntry]


@dataclass(slots=True)
class MigrationPlanner:
    registry: MigrationRegistry

    def plan(self, *, current_version: int, target_version: int, backend: str) -> list[MigrationPlanEntry]:
        steps = self.registry.matching(current_version=current_version, target_version=target_version, backend=backend)
        return [
            MigrationPlanEntry(
                name=step.name,
                from_version=step.from_version,
                to_version=step.to_version,
                backend=step.target_backend,
            )
            for step in steps
        ]


@dataclass(slots=True)
class MigrationRunResult:
    success: bool
    state: MigrationState
    history: MigrationHistory
    plan: list[MigrationPlanEntry]


@dataclass(slots=True)
class MigrationValidator:
    def validate(self, *, connection: sqlite3.Connection, expected_version: int) -> None:
        try:
            metadata = connection.execute("SELECT value FROM schema_meta WHERE key = 'schema_version'").fetchone()
        except Exception as exc:
            raise ValueError("schema metadata table is missing") from exc
        if metadata is None:
            raise ValueError("schema metadata row is missing")
        try:
            value = metadata["value"]  # type: ignore[index]
        except Exception:
            value = metadata[0]
        if str(value) != str(expected_version):
            raise ValueError(f"expected schema version {expected_version}, got {value}")


@dataclass(slots=True)
class MigrationRunner:
    registry: MigrationRegistry
    validator: MigrationValidator

    def _ensure_schema_metadata(self, connection: sqlite3.Connection, version: int) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT INTO schema_meta (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = EXCLUDED.value",
            ("schema_version", str(version)),
        )

    def run(
        self,
        *,
        current_version: int,
        target_version: int,
        backend: str,
        connection: sqlite3.Connection,
        dry_run: bool,
        state: MigrationState,
        history: MigrationHistory,
    ) -> MigrationRunResult:
        plan = MigrationPlanner(self.registry).plan(
            current_version=current_version,
            target_version=target_version,
            backend=backend,
        )
        if dry_run:
            return MigrationRunResult(success=True, state=state, history=history, plan=plan)

        self._ensure_schema_metadata(connection, current_version)
        for entry in plan:
            step = next(step for step in self.registry.steps if step.name == entry.name)
            context = MigrationContext(
                connection=connection,
                current_version=current_version,
                target_version=target_version,
                backend=backend,
                state=state,
                history=history,
            )
            step.apply(context)
            history.add(
                MigrationHistoryEntry(
                    name=step.name,
                    from_version=step.from_version,
                    to_version=step.to_version,
                    backend=backend,
                    status="applied",
                )
            )
            current_version = step.to_version
            state.current_version = current_version
            self._ensure_schema_metadata(connection, current_version)

        self.validator.validate(connection=connection, expected_version=target_version)
        return MigrationRunResult(success=True, state=state, history=history, plan=plan)


@dataclass(slots=True)
class RollbackPlan:
    can_rollback: bool
    reason: str
    target_version: int | None = None


@dataclass(slots=True)
class RollbackManager:
    registry: MigrationRegistry

    def plan_rollback(self, *, current_version: int, target_version: int, backend: str) -> RollbackPlan:
        if current_version <= target_version:
            return RollbackPlan(can_rollback=False, reason="rollback target is not lower than current version")
        steps = [
            step
            for step in self.registry.steps
            if step.target_backend in {backend, "all"}
            and step.to_version <= current_version
            and step.to_version > target_version
        ]
        if not steps:
            return RollbackPlan(can_rollback=False, reason="no rollback step is available")
        return RollbackPlan(can_rollback=True, reason="rollback plan available", target_version=target_version)


__all__ = [
    "MigrationContext",
    "MigrationEngine",
    "MigrationHistory",
    "MigrationHistoryEntry",
    "MigrationPlanner",
    "MigrationPlan",
    "MigrationPlanEntry",
    "MigrationRegistry",
    "MigrationRunner",
    "MigrationRunResult",
    "MigrationState",
    "MigrationStep",
    "MigrationValidator",
    "RollbackManager",
    "RollbackPlan",
]


class MigrationEngine(MigrationRunner):
    pass
