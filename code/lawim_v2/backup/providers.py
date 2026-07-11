from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from dataclasses import dataclass, field
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


def _jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    return value


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

    def _root_path(self) -> Path:
        configured = str(self.path).strip()
        if configured in {"", "."}:
            return Path(tempfile.gettempdir()) / "lawim-backup" / self.identifier
        return self.path.expanduser()

    def _artifact_dir(self) -> Path:
        return self._root_path() / "artifacts"

    def _artifact_manifest_path(self, artifact_id: str) -> Path:
        return self._artifact_dir() / f"{artifact_id}.json"

    def initialize(self) -> None:
        self.last_checked_at = utc_now()

    def is_available(self) -> bool:
        return self.available

    def _read_manifest(self, artifact_id: str) -> dict[str, Any] | None:
        manifest_path = self._artifact_manifest_path(artifact_id)
        if not manifest_path.is_file():
            return None
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return payload if isinstance(payload, dict) else None

    def store(self, artifact: BackupArtifact) -> dict[str, Any]:
        root = self._root_path()
        artifact_dir = self._artifact_dir()
        artifact_dir.mkdir(parents=True, exist_ok=True)
        snapshot = artifact.as_dict()
        snapshot.update(
            {
                "provider": self.identifier,
                "stored_at": utc_now(),
                "state": self.state,
                "artifact_root": str(root),
            }
        )
        manifest_path = self._artifact_manifest_path(artifact.identifier)
        manifest_path.write_text(json.dumps(_jsonable(snapshot), ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
        self.last_checked_at = utc_now()
        return snapshot

    def retrieve(self, artifact_id: str) -> dict[str, Any] | None:
        return self._read_manifest(artifact_id)

    def verify(self, artifact_id: str) -> bool:
        manifest = self._read_manifest(artifact_id)
        if manifest is None:
            return False
        artifact_path = manifest.get("path")
        expected_sha256 = str(manifest.get("sha256") or "").strip()
        if not artifact_path:
            return bool(manifest.get("checksum_valid", True))
        path = Path(str(artifact_path))
        if not path.is_file():
            return False
        if not expected_sha256:
            return True
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return digest == expected_sha256

    def delete(self, artifact_id: str) -> bool:
        manifest_path = self._artifact_manifest_path(artifact_id)
        if not manifest_path.exists():
            return False
        manifest_path.unlink(missing_ok=True)
        self.last_checked_at = utc_now()
        return True

    def list(self) -> list[dict[str, Any]]:
        artifact_dir = self._artifact_dir()
        if not artifact_dir.is_dir():
            return []
        items: list[dict[str, Any]] = []
        for manifest_path in sorted(artifact_dir.glob("*.json")):
            try:
                payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(payload, dict):
                items.append(payload)
        return items

    def get_free_space(self) -> int:
        root = self._root_path()
        try:
            usage = shutil.disk_usage(root if root.exists() else root.parent)
            return int(usage.free)
        except OSError:
            return self.free_space_bytes

    def health(self) -> dict[str, Any]:
        root = self._root_path()
        return {
            "identifier": self.identifier,
            "name": self.name,
            "kind": self.kind,
            "path": str(self.path),
            "resolved_path": str(root),
            "uuid": self.uuid,
            "label": self.label,
            "mount_point": self.mount_point,
            "state": self.state,
            "available": self.available,
            "free_space_bytes": self.get_free_space(),
            "read_only": self.read_only,
            "last_checked_at": self.last_checked_at,
            "artifact_count": len(self.list()),
            "filesystem_ready": root.exists(),
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
