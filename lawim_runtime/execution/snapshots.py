from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ExecutionSnapshot:
    snapshot_id: str
    execution_id: str
    state: str
    data: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1
    checksum: str = ""


class SnapshotManager:
    def __init__(self) -> None:
        self._snapshots: dict[str, list[ExecutionSnapshot]] = {}

    def take_snapshot(
        self,
        execution_id: str,
        state: str,
        data: dict[str, Any],
    ) -> ExecutionSnapshot:
        snapshots = self._snapshots.setdefault(execution_id, [])
        version = len(snapshots) + 1
        snapshot = ExecutionSnapshot(
            snapshot_id=f"snap-{execution_id}-{version}",
            execution_id=execution_id,
            state=state,
            data=data,
            version=version,
        )
        snapshots.append(snapshot)
        return snapshot

    def get_latest(self, execution_id: str) -> ExecutionSnapshot | None:
        snapshots = self._snapshots.get(execution_id)
        if not snapshots:
            return None
        return snapshots[-1]

    def list_for_execution(self, execution_id: str) -> list[ExecutionSnapshot]:
        return list(self._snapshots.get(execution_id, []))

    def count(self, execution_id: str = "") -> int:
        if execution_id:
            return len(self._snapshots.get(execution_id, []))
        return sum(len(v) for v in self._snapshots.values())

    def clear(self, execution_id: str = "") -> None:
        if execution_id:
            self._snapshots.pop(execution_id, None)
        else:
            self._snapshots.clear()
