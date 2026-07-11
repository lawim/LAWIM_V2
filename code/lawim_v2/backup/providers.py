from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .models import BackupArtifact, utc_now


class StorageProvider(Protocol):
    identifier: str
    name: str
    kind: str

    def initialize(self) -> None: ...
    def is_available(self) -> bool: ...
    def store(self, artifact: BackupArtifact) -> dict[str, Any]: ...
    def retrieve(self, artifact_id: str) -> dict[str, Any] | None: ...
    def verify(self, artifact_id: str) -> bool: ...
    def delete(self, artifact_id: str) -> bool: ...
    def list(self) -> list[dict[str, Any]]: ...
    def get_free_space(self) -> int: ...
    def health(self) -> dict[str, Any]: ...


@dataclass(slots=True)
class BaseStorageProvider:
    identifier: str
    name: str
    kind: str
    path: Path = Path("")
    uuid: str = ""
    label: str = ""
    mount_point: str = ""
    state: str = "UNKNOWN"
    available: bool = False
    free_space_bytes: int = 0
    read_only: bool = False
    last_checked_at: str = field(default_factory=utc_now)
    _artifacts: dict[str, dict[str, Any]] = field(default_factory=dict, init=False, repr=False)

    def initialize(self) -> None:
        self.last_checked_at = utc_now()

    def is_available(self) -> bool:
        return self.available

    def store(self, artifact: BackupArtifact) -> dict[str, Any]:
        snapshot = artifact.as_dict()
        snapshot.update({"provider": self.identifier, "stored_at": utc_now(), "state": self.state})
        self._artifacts[artifact.identifier] = snapshot
        return snapshot

    def retrieve(self, artifact_id: str) -> dict[str, Any] | None:
        return self._artifacts.get(artifact_id)

    def verify(self, artifact_id: str) -> bool:
        return artifact_id in self._artifacts

    def delete(self, artifact_id: str) -> bool:
        return self._artifacts.pop(artifact_id, None) is not None

    def list(self) -> list[dict[str, Any]]:
        return list(self._artifacts.values())

    def get_free_space(self) -> int:
        return self.free_space_bytes

    def health(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "kind": self.kind,
            "path": str(self.path),
            "uuid": self.uuid,
            "label": self.label,
            "mount_point": self.mount_point,
            "state": self.state,
            "available": self.available,
            "free_space_bytes": self.free_space_bytes,
            "read_only": self.read_only,
            "last_checked_at": self.last_checked_at,
            "artifact_count": len(self._artifacts),
        }


@dataclass(slots=True)
class LocalDiskProvider(BaseStorageProvider):
    kind: str = "local_disk"


@dataclass(slots=True)
class GoogleDriveProvider(BaseStorageProvider):
    kind: str = "google_drive"


@dataclass(slots=True)
class ExternalDiskProvider(BaseStorageProvider):
    kind: str = "external_disk"
