from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol


class StorageProvider(Protocol):
    name: str
    kind: str
    quota_gb: int
    used_gb: int
    status: str

    def resolve_access(self, *, media_id: int, kind: str) -> dict[str, Any]: ...

    def sync(self, *, media_id: int, direction: str = "outbound") -> dict[str, Any]: ...


@dataclass(slots=True)
class StorageOrchestratorPolicy:
    default_provider: str = "local"
    temporary_access_ttl_seconds: int = 900
    allowed_kinds: tuple[str, ...] = ("image", "video", "audio", "document")
    bandwidth_limit_mbps: int = 100


@dataclass(slots=True)
class ProviderHealth:
    name: str
    status: str = "mock-ready"
    note: str = "placeholder health snapshot"


@dataclass(slots=True)
class DriveBalancingRule:
    name: str
    target_kind: str
    provider_name: str
    max_bytes_per_job: int = 50_000_000


@dataclass(slots=True)
class DriveAssignment:
    provider_name: str
    kind: str
    size_bytes: int
    reason: str


@dataclass(slots=True)
class DriveQuotaManager:
    quotas_gb: dict[str, int] = field(default_factory=lambda: {"drive-1": 1000, "drive-2": 1000, "drive-3": 1000, "drive-4": 1000, "drive-5": 1000, "drive-6": 1000, "drive-7": 1000, "drive-8": 1000, "drive-9": 1000, "drive-10": 1000})

    def assign_drive(self, *, kind: str, size_bytes: int, rule: DriveBalancingRule | None = None) -> DriveAssignment:
        provider_name = rule.provider_name if rule else "drive-1"
        return DriveAssignment(provider_name=provider_name, kind=kind, size_bytes=size_bytes, reason=rule.name if rule else "default")


@dataclass(slots=True)
class CompressionPolicy:
    level: str = "balanced"


@dataclass(slots=True)
class DeduplicationPolicy:
    enabled: bool = True


@dataclass(slots=True)
class BandwidthPolicy:
    limit_mbps: int = 100


@dataclass(slots=True)
class LifecycleStateMachine:
    states: tuple[str, ...] = ("hot", "warm", "cold", "archived")

    def transition(self, current_state: str, target_state: str) -> str:
        if current_state not in self.states or target_state not in self.states:
            raise ValueError("unsupported lifecycle state")
        if current_state == "archived" and target_state != "archived":
            raise ValueError("archived media cannot transition forward")
        return target_state

    def backup_state_for(self, lifecycle_state: str) -> str:
        mapping = {"hot": "fresh", "warm": "queued", "cold": "queued", "archived": "archived"}
        return mapping.get(lifecycle_state, "queued")


@dataclass(slots=True)
class BackupJob:
    media_id: int
    kind: str
    status: str = "scheduled"
    target_provider: str = "backup-center"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(slots=True)
class RestoreJob:
    media_id: int
    reason: str
    status: str = "queued"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(slots=True)
class SyncJob:
    media_id: int
    provider_name: str
    direction: str
    status: str = "queued"


@dataclass(slots=True)
class BackupCenter:
    backup_jobs: list[BackupJob] = field(default_factory=list)
    restore_jobs: list[RestoreJob] = field(default_factory=list)
    sync_jobs: list[SyncJob] = field(default_factory=list)
    alerts: list[str] = field(default_factory=list)

    def add_alert(self, message: str) -> None:
        self.alerts.append(message)


@dataclass(slots=True)
class BackupManager:
    backup_center: BackupCenter

    def create_backup_job(self, *, media_id: int, kind: str) -> BackupJob:
        job = BackupJob(media_id=media_id, kind=kind)
        self.backup_center.backup_jobs.append(job)
        return job

    def create_restore_job(self, *, media_id: int, reason: str) -> RestoreJob:
        job = RestoreJob(media_id=media_id, reason=reason)
        self.backup_center.restore_jobs.append(job)
        return job


@dataclass(slots=True)
class RestorationEngine:
    def build_restore_plan(self, *, media_id: int, reason: str) -> dict[str, Any]:
        return {
            "media_id": media_id,
            "reason": reason,
            "source": "backup-center",
            "status": "ready",
        }


@dataclass(slots=True)
class StorageOptimizer:
    compression: CompressionPolicy = field(default_factory=CompressionPolicy)
    deduplication: DeduplicationPolicy = field(default_factory=DeduplicationPolicy)
    bandwidth: BandwidthPolicy = field(default_factory=BandwidthPolicy)

    def plan(self, *, media_id: int, kind: str) -> dict[str, Any]:
        return {
            "media_id": media_id,
            "kind": kind,
            "compression": self.compression.level,
            "deduplication_enabled": self.deduplication.enabled,
            "bandwidth_limit_mbps": self.bandwidth.limit_mbps,
        }


@dataclass(slots=True)
class SetupWizardConfiguration:
    architecture: str
    backup_center_enabled: bool
    external_disk_enabled: bool
    google_drive_count: int = 10
    placeholder_notes: tuple[str, ...] = ("mock configuration", "no secrets stored")


@dataclass(slots=True)
class LocalStorageProvider:
    name: str = "local"
    kind: str = "local"
    quota_gb: int = 1000
    used_gb: int = 0
    status: str = "mock-ready"

    def resolve_access(self, *, media_id: int, kind: str) -> dict[str, Any]:
        return {
            "media_id": media_id,
            "kind": kind,
            "provider": self.name,
            "temporary_access_url": f"https://mock.example/{self.name}/{media_id}",
            "ttl_seconds": 900,
        }

    def sync(self, *, media_id: int, direction: str = "outbound") -> dict[str, Any]:
        return {"media_id": media_id, "provider": self.name, "direction": direction, "status": "mock-synced"}


@dataclass(slots=True)
class GoogleDriveProvider:
    name: str
    quota_gb: int = 1000
    used_gb: int = 0
    status: str = "mock-ready"
    kind: str = "google-drive"

    def resolve_access(self, *, media_id: int, kind: str) -> dict[str, Any]:
        return {
            "media_id": media_id,
            "kind": kind,
            "provider": self.name,
            "temporary_access_url": f"https://mock.example/{self.name}/{media_id}",
            "ttl_seconds": 900,
        }

    def sync(self, *, media_id: int, direction: str = "outbound") -> dict[str, Any]:
        return {"media_id": media_id, "provider": self.name, "direction": direction, "status": "mock-synced"}


@dataclass(slots=True)
class BackupCenterProvider:
    name: str = "backup-center"
    kind: str = "backup"
    quota_gb: int = 5000
    used_gb: int = 0
    status: str = "mock-ready"

    def resolve_access(self, *, media_id: int, kind: str) -> dict[str, Any]:
        return {"media_id": media_id, "kind": kind, "provider": self.name, "temporary_access_url": f"https://mock.example/{self.name}/{media_id}", "ttl_seconds": 900}

    def sync(self, *, media_id: int, direction: str = "outbound") -> dict[str, Any]:
        return {"media_id": media_id, "provider": self.name, "direction": direction, "status": "mock-synced"}


@dataclass(slots=True)
class ExternalDiskProvider:
    name: str
    capacity_gb: int = 200
    used_gb: int = 0
    status: str = "mock-ready"
    kind: str = "external-disk"

    def resolve_access(self, *, media_id: int, kind: str) -> dict[str, Any]:
        return {"media_id": media_id, "kind": kind, "provider": self.name, "temporary_access_url": f"https://mock.example/{self.name}/{media_id}", "ttl_seconds": 900}

    def sync(self, *, media_id: int, direction: str = "outbound") -> dict[str, Any]:
        return {"media_id": media_id, "provider": self.name, "direction": direction, "status": "mock-synced"}


@dataclass(slots=True)
class StorageOrchestrator:
    providers: list[StorageProvider]
    policy: StorageOrchestratorPolicy = field(default_factory=StorageOrchestratorPolicy)

    def __post_init__(self) -> None:
        provider_names = {provider.name for provider in self.providers}
        if self.policy.default_provider not in provider_names:
            self.providers.append(LocalStorageProvider(name=self.policy.default_provider))

    def resolve_media_access(self, *, media_id: int, kind: str, provider_name: str | None = None) -> dict[str, Any]:
        provider = next((item for item in self.providers if item.name == (provider_name or self.policy.default_provider)), None)
        if provider is None:
            raise ValueError("unknown provider")
        resolved = provider.resolve_access(media_id=media_id, kind=kind)
        resolved["lifecycle_state"] = "hot"
        resolved["policy"] = {
            "temporary_access_ttl_seconds": self.policy.temporary_access_ttl_seconds,
            "bandwidth_limit_mbps": self.policy.bandwidth_limit_mbps,
        }
        return resolved

    def register_provider(self, provider: StorageProvider) -> None:
        self.providers.append(provider)


__all__ = [
    "BackupCenter",
    "BackupCenterProvider",
    "BackupJob",
    "BackupManager",
    "BandwidthPolicy",
    "CompressionPolicy",
    "DeduplicationPolicy",
    "DriveAssignment",
    "DriveBalancingRule",
    "DriveQuotaManager",
    "ExternalDiskProvider",
    "GoogleDriveProvider",
    "LifecycleStateMachine",
    "LocalStorageProvider",
    "ProviderHealth",
    "RestoreJob",
    "RestorationEngine",
    "SetupWizardConfiguration",
    "StorageOptimizer",
    "StorageOrchestrator",
    "StorageOrchestratorPolicy",
    "StorageProvider",
    "SyncJob",
]
