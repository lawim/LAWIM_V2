"""KnowledgeVersion model — computed version identity for the loaded knowledge graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


@dataclass(frozen=True, slots=True)
class KnowledgeVersion:
    """Immutable version descriptor for the currently loaded knowledge graph."""

    knowledge_version: str
    schema_version: str
    build_commit: str
    loaded_at: datetime
    source_checksums: dict[str, str] = field(default_factory=dict)
    source_record_counts: dict[str, int] = field(default_factory=dict)
    validation_status: str = "UNKNOWN"
    validation_issue_count: int = 0

    @classmethod
    def compute(
        cls,
        *,
        schema_version: str,
        build_commit: str,
        source_checksums: dict[str, str],
        source_record_counts: dict[str, int],
        loaded_at: datetime | None = None,
    ) -> KnowledgeVersion:
        """Compute a KnowledgeVersion from source metadata and the git commit hash."""
        loaded_at = loaded_at or datetime.now(timezone.utc)
        digest = sha256()
        for path in sorted(source_checksums):
            digest.update(f"{path}:{source_checksums[path]}\n".encode("utf-8"))
        digest.update(f"schema:{schema_version}\n".encode("utf-8"))
        digest.update(f"commit:{build_commit}\n".encode("utf-8"))
        knowledge_version = digest.hexdigest()[:16]
        return cls(
            knowledge_version=knowledge_version,
            schema_version=schema_version,
            build_commit=build_commit,
            loaded_at=loaded_at,
            source_checksums=source_checksums,
            source_record_counts=source_record_counts,
        )

    def dict(self) -> dict[str, Any]:
        return {
            "knowledge_version": self.knowledge_version,
            "schema_version": self.schema_version,
            "build_commit": self.build_commit,
            "loaded_at": self.loaded_at.isoformat(),
            "source_checksums": dict(self.source_checksums),
            "source_record_counts": dict(self.source_record_counts),
            "validation_status": self.validation_status,
            "validation_issue_count": self.validation_issue_count,
        }
