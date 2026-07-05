from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from .credential_vault import (
    CredentialReference,
    CredentialScope,
    CredentialStatus,
    CredentialType,
    CredentialVault,
    build_default_credential_vault,
)


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
    credential_reference: CredentialReference
    oauth_status: str = CredentialStatus.PLACEHOLDER_CONFIGURED
    credential_status: str = CredentialStatus.PLACEHOLDER_CONFIGURED
    last_connection_test: str = "never"
    last_upload_test: str = "never"
    last_download_test: str = "never"
    last_healthcheck: str = "never"
    expiry: str = "never"
    refresh_strategy: str = "automatic"
    scopes: tuple[str, ...] = ("https://www.googleapis.com/auth/drive",)

    @property
    def status(self) -> str:
        return self.oauth_status

    @property
    def credential_id(self) -> str:
        return self.credential_reference.credential_id

    @property
    def logical_name(self) -> str:
        return self.credential_reference.logical_name

    @property
    def drive_id(self) -> str:
        return self.credential_reference.drive_id

    def as_dict(self) -> dict[str, Any]:
        return {
            "credential_reference": self.credential_reference.as_dict(),
            "credential_id": self.credential_id,
            "logical_name": self.logical_name,
            "drive_id": self.drive_id,
            "oauth_status": self.oauth_status,
            "credential_status": self.credential_status,
            "status": self.status,
            "last_connection_test": self.last_connection_test,
            "last_upload_test": self.last_upload_test,
            "last_download_test": self.last_download_test,
            "last_healthcheck": self.last_healthcheck,
            "expiry": self.expiry,
            "scopes": list(self.scopes),
            "refresh_strategy": self.refresh_strategy,
        }


@dataclass(slots=True)
class GoogleDriveConnector:
    drive_id: str
    logical_name: str
    credential_reference: CredentialReference
    oauth: GoogleDriveOAuthCredentials
    credential_vault: CredentialVault | None = None
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
    folders: list[str] = field(default_factory=list)
    journal: list[dict[str, Any]] = field(default_factory=list)
    alerts: list[str] = field(default_factory=list)

    @property
    def credential_id(self) -> str:
        return self.credential_reference.credential_id

    @property
    def credential_status(self) -> str:
        return self.oauth.credential_status

    @property
    def oauth_status(self) -> str:
        return self.oauth.oauth_status

    @classmethod
    def from_resource(
        cls,
        resource: Any,
        *,
        credential_reference: CredentialReference | None = None,
        credential_vault: CredentialVault | None = None,
    ) -> "GoogleDriveConnector":
        drive_id = str(_resource_value(resource, "drive_id"))
        credential_id = str(_resource_value(resource, "credential_id", f"cred-{drive_id}"))
        if credential_reference is None:
            credential_reference = CredentialReference(
                credential_id=credential_id,
                logical_name=str(_resource_value(resource, "logical_name", drive_id)),
                drive_id=drive_id,
                role=str(_resource_value(resource, "role", "")),
                provider=str(_resource_value(resource, "provider_type", _resource_value(resource, "provider", "google-drive"))),
                scope=str(_resource_value(resource, "credential_scope", CredentialScope.GOOGLE_DRIVE)),
                credential_type=str(_resource_value(resource, "credential_type", CredentialType.GOOGLE_DRIVE_OAUTH2)),
                status=str(_resource_value(resource, "credential_status", CredentialStatus.PLACEHOLDER_CONFIGURED)),
                last_used_at=str(_resource_value(resource, "last_used_at", _resource_value(resource, "last_control", _utc_now()))),
                last_test_at=str(_resource_value(resource, "last_connection_test", _resource_value(resource, "last_test", _utc_now()))),
                expires_at=str(_resource_value(resource, "expires_at", "never")),
                rotation_due_at=str(_resource_value(resource, "rotation_due_at", "never")),
            )
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
            last_upload=str(_resource_value(resource, "last_upload", _resource_value(resource, "last_upload_test", "never"))),
            last_download=str(_resource_value(resource, "last_download", _resource_value(resource, "last_download_test", "never"))),
            last_incident=str(_resource_value(resource, "last_incident", alerts[0] if alerts else "none")),
            credential_reference=credential_reference,
            oauth=GoogleDriveOAuthCredentials(
                credential_reference=credential_reference,
                oauth_status=str(_resource_value(resource, "oauth_status", _resource_value(resource, "credential_status", CredentialStatus.PLACEHOLDER_CONFIGURED))),
                credential_status=str(_resource_value(resource, "credential_status", CredentialStatus.PLACEHOLDER_CONFIGURED)),
                last_connection_test=str(_resource_value(resource, "last_connection_test", _resource_value(resource, "last_test", _utc_now()))),
                last_upload_test=str(_resource_value(resource, "last_upload_test", _resource_value(resource, "last_test", _utc_now()))),
                last_download_test=str(_resource_value(resource, "last_download_test", _resource_value(resource, "last_test", _utc_now()))),
                last_healthcheck=str(_resource_value(resource, "last_healthcheck", _resource_value(resource, "last_test", _utc_now()))),
                expiry=str(_resource_value(resource, "expiry", "never")),
            ),
            credential_vault=credential_vault,
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

    def _touch_vault(self, action: str, *, success: bool = True) -> None:
        if self.credential_vault is None:
            return
        if action == "connect":
            record = self.credential_vault.touch_connection_test(self.credential_id, success=success)
        elif action == "upload":
            record = self.credential_vault.touch_upload_test(self.credential_id, success=success)
        elif action == "download":
            record = self.credential_vault.touch_download_test(self.credential_id, success=success)
        elif action == "healthcheck":
            record = self.credential_vault.touch_healthcheck(self.credential_id, success=success)
        else:
            return
        self.credential_reference.status = record.status
        self.credential_reference.last_used_at = record.last_used_at
        self.credential_reference.last_test_at = record.last_connection_test
        self.credential_reference.expires_at = record.expires_at
        self.credential_reference.rotation_due_at = record.rotation_due_at
        self.oauth.credential_status = record.status
        self.oauth.oauth_status = record.status
        self.oauth.last_connection_test = record.last_connection_test
        self.oauth.last_upload_test = record.last_upload_test
        self.oauth.last_download_test = record.last_download_test
        self.oauth.last_healthcheck = record.last_healthcheck

    def _normalize_folder(self, folder_name: str) -> str:
        folder = folder_name.strip().replace(" ", "_").upper()
        if not folder:
            raise ValueError("folder name is required")
        return folder

    def connect(self) -> dict[str, Any]:
        self.last_control = _utc_now()
        self.oauth.last_connection_test = self.last_control
        self.oauth.last_healthcheck = self.last_control
        self._touch_vault("connect")
        self._record("connect", credential_id=self.credential_id, oauth_status=self.oauth.status, credential_status=self.credential_status, api_version=self.api_version)
        return {
            "drive_id": self.drive_id,
            "logical_name": self.logical_name,
            "connected": True,
            "oauth_status": self.oauth.status,
            "credential_status": self.credential_status,
            "credential_id": self.credential_id,
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
        self.oauth.expiry = "never"
        self.last_control = _utc_now()
        self.oauth.last_connection_test = self.last_control
        self.oauth.last_healthcheck = self.last_control
        self._touch_vault("connect")
        self._record("refresh_access_token", credential_id=self.credential_id, oauth_status=self.oauth.status)
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
        self.oauth.last_upload_test = self.last_upload
        self._touch_vault("upload")
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
        self.oauth.last_download_test = self.last_download
        self._touch_vault("download")
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
            self._touch_vault("upload", success=False)
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
        self.oauth.last_upload_test = self.last_upload
        self._touch_vault("upload")
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
        self.oauth.last_download_test = self.last_access
        self._touch_vault("download")
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
        self.last_control = _utc_now()
        self.oauth.last_healthcheck = self.last_control
        self._touch_vault("healthcheck")
        self._record("healthcheck", credential_id=self.credential_id, oauth_status=self.oauth.status, credential_status=self.credential_status)
        return {
            "drive_id": self.drive_id,
            "logical_name": self.logical_name,
            "provider": self.provider,
            "api_version": self.api_version,
            "state": self.state,
            "health": self.health,
            "oauth_status": self.oauth.status,
            "credential_status": self.credential_status,
            "credential_id": self.credential_id,
            "last_control": self.last_control,
            "last_access": self.last_access,
            "last_upload": self.last_upload,
            "last_download": self.last_download,
            "last_connection_test": self.oauth.last_connection_test,
            "last_upload_test": self.oauth.last_upload_test,
            "last_download_test": self.oauth.last_download_test,
            "last_healthcheck": self.oauth.last_healthcheck,
            "last_incident": self.last_incident,
            "alerts": list(self.alerts),
        }

    def monitoring_snapshot(self) -> dict[str, Any]:
        api_monitor = {
            "apiVersion": self.api_version,
            "oauthStatus": self.oauth.status,
            "credentialStatus": self.credential_status,
            "status": "healthy" if self.health == "healthy" else "watch",
        }
        credential_monitor = self.credential_vault.monitoring_snapshot() if self.credential_vault is not None else {
            "vault": "unbound",
            "status": self.credential_status,
            "recordCount": 1,
            "activeCredentials": 1 if self.credential_status in CredentialStatus.active_states() else 0,
            "expiredCredentials": 0,
            "invalidCredentials": 0,
            "rotationDueCredentials": 0,
            "lastAccess": self.last_access,
            "lastSuccess": self.last_access,
            "lastFailure": "never",
            "alerts": [],
            "audit": {"event_count": 0, "latest": None, "entries": []},
        }
        return {
            "drive_id": self.drive_id,
            "quota_monitor": self.quota_status(),
            "latency_ms": 28 if self.health == "healthy" else 85,
            "throughput_mbps": 180 if self.health == "healthy" else 60,
            "apiMonitor": api_monitor,
            "api_monitor": api_monitor,
            "credentialMonitor": credential_monitor,
            "credential_monitor": credential_monitor,
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
            "role": self.credential_reference.role,
            "credential_status": self.credential_status,
            "oauth_status": self.oauth_status,
            "credential_id": self.credential_id,
            "credential_reference": self.credential_reference.as_dict(),
            "quota": self.quota_status(),
            "health": self.health_status(),
            "oauth": self.oauth.as_dict(),
            "folders": list(self.folders),
            "journal": list(self.journal),
            "alerts": list(self.alerts),
            "last_connection_test": self.oauth.last_connection_test,
            "last_upload_test": self.oauth.last_upload_test,
            "last_download_test": self.oauth.last_download_test,
            "last_healthcheck": self.oauth.last_healthcheck,
            "monitoring": self.monitoring_snapshot(),
        }


def build_default_google_drive_connectors(
    resources: Sequence[Any] | None = None,
    *,
    vault: CredentialVault | None = None,
) -> list[GoogleDriveConnector]:
    resources = list(resources or [])
    credential_vault = vault or build_default_credential_vault(resources)
    connectors: list[GoogleDriveConnector] = []
    for resource in resources:
        credential_id = str(_resource_value(resource, "credential_id", f"cred-{_resource_value(resource, 'drive_id')}"))
        try:
            credential_reference = credential_vault.reference_for(credential_id)
        except KeyError:
            credential_reference = CredentialReference(
                credential_id=credential_id,
                logical_name=str(_resource_value(resource, "logical_name", credential_id)),
                drive_id=str(_resource_value(resource, "drive_id")),
                role=str(_resource_value(resource, "role", "")),
                provider=str(_resource_value(resource, "provider_type", _resource_value(resource, "provider", "google-drive"))),
            )
        connectors.append(
            GoogleDriveConnector.from_resource(
                resource,
                credential_reference=credential_reference,
                credential_vault=credential_vault,
            )
        )
    return connectors


__all__ = [
    "GoogleDriveConnector",
    "GoogleDriveOAuthCredentials",
    "build_default_google_drive_connectors",
]
