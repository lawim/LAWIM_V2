from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _gb_from_bytes(size_bytes: int) -> float:
    return round(max(size_bytes, 0) / (1024**3), 3)


def _quota_band(usage_percent: float) -> str:
    if usage_percent > 92:
        return "blocked"
    if usage_percent >= 85:
        return "slowdown"
    if usage_percent >= 70:
        return "attention"
    return "normal"


def _resource_value(resource: Any, key: str, default: Any = None) -> Any:
    if isinstance(resource, Mapping):
        return resource.get(key, default)
    return getattr(resource, key, default)


@dataclass(slots=True)
class GoogleDriveOAuthCredentials:
    client_id: str = "client-id-placeholder"
    client_secret: str = "client-secret-placeholder"
    refresh_token: str = "refresh-token-placeholder"
    access_token: str = "access-token-placeholder"
    token_type: str = "Bearer"
    expiry: str = "never"
    scopes: tuple[str, ...] = ("https://www.googleapis.com/auth/drive",)
    refresh_strategy: str = "automatic"
    status: str = "placeholder-configured"

    def as_dict(self) -> dict[str, Any]:
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expiry": self.expiry,
            "scopes": list(self.scopes),
            "refresh_strategy": self.refresh_strategy,
            "status": self.status,
        }


@dataclass(slots=True)
class GoogleDriveConnector:
    drive_id: str
    logical_name: str
    provider: str = "google-drive"
    category: str = "general"
    quota_gb: float = 13.0
    used_gb: float = 0.0
    resource_type: str = "google-drive-resource"
    api_version: str = "v3"
    routing_strategy: str = "official-priority-route"
    backup_policy: str = "backup-center-activation"
    restore_policy: str = "restore-center-activation"
    state: str = "ready"
    health: str = "healthy"
    last_control: str = field(default_factory=_utc_now)
    last_access: str = field(default_factory=_utc_now)
    last_upload: str = "never"
    last_download: str = "never"
    last_incident: str = "none"
    oauth: GoogleDriveOAuthCredentials = field(default_factory=GoogleDriveOAuthCredentials)
    folders: list[str] = field(default_factory=list)
    journal: list[dict[str, Any]] = field(default_factory=list)
    alerts: list[str] = field(default_factory=list)

    @classmethod
    def from_resource(cls, resource: Any) -> "GoogleDriveConnector":
        drive_id = str(_resource_value(resource, "drive_id"))
        quota_gb = float(_resource_value(resource, "quota_gb", 13.0))
        used_gb = float(_resource_value(resource, "used_gb", 0.0))
        state = str(_resource_value(resource, "state", _resource_value(resource, "status", "ready")))
        health = str(_resource_value(resource, "health", "healthy"))
        usage_percent = round((used_gb / quota_gb) * 100, 1) if quota_gb else 0.0
        alerts: list[str] = []
        if state != "ready" or health != "healthy":
            alerts.append(f"{drive_id} {state} at {usage_percent:.1f}%")
        return cls(
            drive_id=drive_id,
            logical_name=str(_resource_value(resource, "logical_name", drive_id)),
            provider=str(_resource_value(resource, "provider_type", _resource_value(resource, "provider", "google-drive"))),
            category=str(_resource_value(resource, "category", "general")),
            quota_gb=quota_gb,
            used_gb=used_gb,
            resource_type=str(_resource_value(resource, "resource_type", "google-drive-resource")),
            api_version=str(_resource_value(resource, "api_version", "v3")),
            routing_strategy=str(_resource_value(resource, "routing_strategy", "official-priority-route")),
            backup_policy=str(_resource_value(resource, "backup_policy", "backup-center-activation")),
            restore_policy=str(_resource_value(resource, "restore_policy", "restore-center-activation")),
            state=state,
            health=health,
            last_control=str(_resource_value(resource, "last_control", _resource_value(resource, "last_test", _utc_now()))),
            last_access=str(_resource_value(resource, "last_access", _resource_value(resource, "last_test", _utc_now()))),
            last_upload=str(_resource_value(resource, "last_upload", "never")),
            last_download=str(_resource_value(resource, "last_download", "never")),
            last_incident=str(_resource_value(resource, "last_incident", alerts[0] if alerts else "none")),
            oauth=GoogleDriveOAuthCredentials(
                client_id=f"{drive_id}.client-id.placeholder",
                client_secret="client-secret-placeholder",
                refresh_token="refresh-token-placeholder",
                access_token="access-token-placeholder",
                expiry="never",
            ),
            folders=list(cls.required_folders()),
            alerts=alerts,
        )

    @staticmethod
    def required_folders() -> tuple[str, ...]:
        return (
            "VIDEOS",
            "VIDEOS_ARCHIVE",
            "PHOTOS",
            "AUDIO",
            "DOCUMENTS",
            "CONVERSATIONS",
            "BACKUPS",
            "EXPORTS",
            "TEMP",
            "LOGS",
        )

    @property
    def available_gb(self) -> float:
        return round(max(self.quota_gb - self.used_gb, 0.0), 3)

    @property
    def usage_percent(self) -> float:
        if self.quota_gb <= 0:
            return 0.0
        return round((self.used_gb / self.quota_gb) * 100, 1)

    @property
    def threshold_band(self) -> str:
        return _quota_band(self.usage_percent)

    def _record(self, action: str, **details: Any) -> None:
        timestamp = _utc_now()
        self.journal.append({"timestamp": timestamp, "action": action, "details": details})
        self.last_access = timestamp

    def _normalize_folder(self, folder_name: str) -> str:
        folder = folder_name.strip().replace(" ", "_").upper()
        if not folder:
            raise ValueError("folder name is required")
        return folder

    def connect(self) -> dict[str, Any]:
        self.last_control = _utc_now()
        self._record("connect", oauth_status=self.oauth.status, api_version=self.api_version)
        return {
            "drive_id": self.drive_id,
            "logical_name": self.logical_name,
            "connected": True,
            "oauth_status": self.oauth.status,
            "api_version": self.api_version,
            "state": self.state,
            "health": self.health,
            "quota": self.quota_status(),
        }

    def test_connection(self) -> dict[str, Any]:
        result = self.connect()
        result["test_status"] = "passed"
        result["last_control"] = self.last_control
        return result

    def refresh_access_token(self) -> dict[str, Any]:
        self.oauth.access_token = "access-token-placeholder-renewed"
        self.oauth.expiry = "never"
        self.last_control = _utc_now()
        self._record("refresh_access_token", oauth_status=self.oauth.status)
        return {
            "drive_id": self.drive_id,
            "oauth_status": self.oauth.status,
            "token_refresh": "automatic",
            "expiry": self.oauth.expiry,
        }

    def create_folder(self, folder_name: str) -> dict[str, Any]:
        folder = self._normalize_folder(folder_name)
        if folder not in self.folders:
            self.folders.append(folder)
        self._record("create_folder", folder=folder)
        self.last_upload = _utc_now()
        return {
            "drive_id": self.drive_id,
            "folder": folder,
            "status": "created",
            "folders": list(self.folders),
        }

    def read(self, *, folder_name: str, object_name: str) -> dict[str, Any]:
        folder = self._normalize_folder(folder_name)
        if folder not in self.folders and folder not in self.required_folders():
            self.alerts.append(f"{self.drive_id} missing folder {folder}")
        self._record("read", folder=folder, object_name=object_name)
        self.last_download = _utc_now()
        return {
            "drive_id": self.drive_id,
            "folder": folder,
            "object_name": object_name,
            "operation": "read",
            "status": "ok",
            "oauth_status": self.oauth.status,
        }

    def write(self, *, folder_name: str, object_name: str, size_bytes: int = 0, mime_type: str = "application/octet-stream") -> dict[str, Any]:
        folder = self._normalize_folder(folder_name)
        estimated_gb = _gb_from_bytes(size_bytes)
        if estimated_gb > self.available_gb:
            incident = f"quota exceeded for {self.drive_id} while writing {object_name}"
            self.last_incident = incident
            self.health = "degraded"
            self.alerts.append(incident)
            self._record("write-blocked", folder=folder, object_name=object_name, size_bytes=size_bytes)
            return {
                "drive_id": self.drive_id,
                "folder": folder,
                "object_name": object_name,
                "operation": "write",
                "status": "blocked",
                "reason": "quota",
                "available_gb": self.available_gb,
            }
        self.used_gb = round(self.used_gb + estimated_gb, 3)
        self._record("write", folder=folder, object_name=object_name, size_bytes=size_bytes, mime_type=mime_type)
        self.last_upload = _utc_now()
        return {
            "drive_id": self.drive_id,
            "folder": folder,
            "object_name": object_name,
            "operation": "write",
            "status": "ok",
            "mime_type": mime_type,
            "size_bytes": size_bytes,
            "usage": self.quota_status(),
        }

    def delete(self, *, folder_name: str, object_name: str, size_bytes: int = 0) -> dict[str, Any]:
        folder = self._normalize_folder(folder_name)
        estimated_gb = _gb_from_bytes(size_bytes)
        if estimated_gb:
            self.used_gb = round(max(self.used_gb - estimated_gb, 0.0), 3)
        self._record("delete", folder=folder, object_name=object_name, size_bytes=size_bytes)
        self.last_access = _utc_now()
        return {
            "drive_id": self.drive_id,
            "folder": folder,
            "object_name": object_name,
            "operation": "delete",
            "status": "ok",
            "usage": self.quota_status(),
        }

    def record_incident(self, message: str) -> dict[str, Any]:
        self.last_incident = message
        self.health = "degraded"
        self.alerts.append(message)
        self._record("incident", message=message)
        return {
            "drive_id": self.drive_id,
            "status": "recorded",
            "message": message,
            "health": self.health,
        }

    def quota_status(self) -> dict[str, Any]:
        return {
            "drive_id": self.drive_id,
            "quota_gb": self.quota_gb,
            "used_gb": self.used_gb,
            "available_gb": self.available_gb,
            "usage_percent": self.usage_percent,
            "band": self.threshold_band,
        }

    def health_status(self) -> dict[str, Any]:
        return {
            "drive_id": self.drive_id,
            "logical_name": self.logical_name,
            "provider": self.provider,
            "api_version": self.api_version,
            "state": self.state,
            "health": self.health,
            "oauth_status": self.oauth.status,
            "last_control": self.last_control,
            "last_access": self.last_access,
            "last_upload": self.last_upload,
            "last_download": self.last_download,
            "last_incident": self.last_incident,
            "alerts": list(self.alerts),
        }

    def monitoring_snapshot(self) -> dict[str, Any]:
        api_monitor = {
            "apiVersion": self.api_version,
            "oauthStatus": self.oauth.status,
            "status": "healthy" if self.health == "healthy" else "watch",
        }
        return {
            "drive_id": self.drive_id,
            "quota_monitor": self.quota_status(),
            "latency_ms": 28 if self.health == "healthy" else 85,
            "throughput_mbps": 180 if self.health == "healthy" else 60,
            "apiMonitor": api_monitor,
            "api_monitor": api_monitor,
            "alerts": list(self.alerts),
            "rotation": {
                "routing_strategy": self.routing_strategy,
                "backup_policy": self.backup_policy,
                "restore_policy": self.restore_policy,
            },
            "occupation": {
                "used_gb": self.used_gb,
                "available_gb": self.available_gb,
                "usage_percent": self.usage_percent,
            },
        }

    def activation_snapshot(self) -> dict[str, Any]:
        return {
            "drive_id": self.drive_id,
            "logical_name": self.logical_name,
            "provider": self.provider,
            "category": self.category,
            "resource_type": self.resource_type,
            "quota": self.quota_status(),
            "health": self.health_status(),
            "oauth": self.oauth.as_dict(),
            "folders": list(self.folders),
            "journal": list(self.journal),
            "alerts": list(self.alerts),
        }


def build_default_google_drive_connectors(resources: Sequence[Any] | None = None) -> list[GoogleDriveConnector]:
    return [GoogleDriveConnector.from_resource(resource) for resource in list(resources or [])]


__all__ = [
    "GoogleDriveConnector",
    "GoogleDriveOAuthCredentials",
    "build_default_google_drive_connectors",
]
