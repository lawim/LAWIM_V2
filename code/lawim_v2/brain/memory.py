from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

MemoryKind = Literal["confirmed_fact", "preference", "constraint", "decision", "hypothesis", "temporary"]
MemoryStatus = Literal["active", "pending_confirmation", "expired", "superseded"]


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


MEMORY_KINDS: tuple[MemoryKind, ...] = (
    "confirmed_fact", "preference", "constraint", "decision", "hypothesis", "temporary"
)

MEMORY_KIND_PRIORITY: dict[MemoryKind, int] = {
    "decision": 100,
    "constraint": 90,
    "confirmed_fact": 80,
    "preference": 60,
    "hypothesis": 30,
    "temporary": 10,
}


class BrainMemory:
    def __init__(self, repository) -> None:
        self.repository = repository

    def add_item(
        self,
        *,
        project_id: int,
        kind: MemoryKind,
        key: str,
        label: str,
        value: str,
        source_table: str | None = None,
        source_id: int | None = None,
        confidence: int = 50,
        is_global: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        now = _utcnow()
        status: MemoryStatus = "active" if kind != "hypothesis" else "pending_confirmation"
        row = self.repository.create_brain_memory(
            project_id=project_id,
            kind=kind,
            memory_key=key,
            label=label,
            value=value,
            source_table=source_table,
            source_id=source_id,
            confidence=confidence,
            status=status,
            is_global=is_global,
            metadata_json=metadata or {},
            created_at=now,
        )
        return dict(row)

    def add_temporary(self, project_id: int, key: str, label: str, value: str) -> dict[str, Any]:
        return self.add_item(
            project_id=project_id,
            kind="temporary",
            key=f"tmp-{key}",
            label=label,
            value=value,
            confidence=20,
        )

    def add_hypothesis(self, project_id: int, key: str, label: str, value: str) -> dict[str, Any]:
        return self.add_item(
            project_id=project_id,
            kind="hypothesis",
            key=f"hyp-{key}",
            label=label,
            value=value,
            confidence=30,
            status="pending_confirmation",
        )

    def confirm(self, project_id: int, memory_key: str) -> dict[str, Any] | None:
        existing = self.repository.get_brain_memory(project_id, memory_key)
        if existing is None:
            return None
        now = _utcnow()
        if existing["kind"] == "temporary" or existing["status"] == "pending_confirmation":
            updated = self.repository.update_brain_memory(
                project_id=project_id,
                memory_key=memory_key,
                kind="confirmed_fact",
                status="active",
                confidence=90,
                updated_at=now,
            )
            return dict(updated) if updated else None
        updated = self.repository.update_brain_memory(
            project_id=project_id,
            memory_key=memory_key,
            status="active",
            confidence=80,
            updated_at=now,
        )
        return dict(updated) if updated else None

    def reject(self, project_id: int, memory_key: str) -> dict[str, Any] | None:
        existing = self.repository.get_brain_memory(project_id, memory_key)
        if existing is None:
            return None
        now = _utcnow()
        updated = self.repository.update_brain_memory(
            project_id=project_id,
            memory_key=memory_key,
            status="superseded",
            confidence=0,
            updated_at=now,
        )
        return dict(updated) if updated else None

    def get_active(self, project_id: int, kind: MemoryKind | None = None) -> list[dict[str, Any]]:
        return self.repository.list_brain_memory(project_id, kind=kind, status="active")

    def get_pending(self, project_id: int) -> list[dict[str, Any]]:
        return self.repository.list_brain_memory(project_id, status="pending_confirmation")

    def get_by_key(self, project_id: int, key: str) -> dict[str, Any] | None:
        return self.repository.get_brain_memory(project_id, key)

    def get_summary(self, project_id: int) -> dict[str, Any]:
        items = self.repository.list_brain_memory(project_id, status="active")
        by_kind: dict[str, list[dict[str, Any]]] = {}
        for item in items:
            kind = str(item.get("kind", "temporary"))
            by_kind.setdefault(kind, []).append(item)
        return {
            "total": len(items),
            "by_kind": {k: len(v) for k, v in by_kind.items()},
            "confirmed_facts": by_kind.get("confirmed_fact", []),
            "preferences": by_kind.get("preference", []),
            "constraints": by_kind.get("constraint", []),
            "decisions": by_kind.get("decision", []),
            "hypotheses": by_kind.get("hypothesis", []),
            "temporary": by_kind.get("temporary", []),
        }

    def expire_temporary(self, project_id: int, older_than_minutes: int = 60) -> int:
        return self.repository.expire_brain_memory(project_id, older_than_minutes)

    def promote_hypothesis(self, project_id: int, memory_key: str) -> dict[str, Any] | None:
        existing = self.repository.get_brain_memory(project_id, memory_key)
        if existing is None or existing["kind"] != "hypothesis":
            return None
        now = _utcnow()
        updated = self.repository.update_brain_memory(
            project_id=project_id,
            memory_key=memory_key,
            kind="confirmed_fact",
            status="active",
            confidence=75,
            updated_at=now,
        )
        return dict(updated) if updated else None
