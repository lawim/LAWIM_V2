from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_backup_id(prefix: str = "LAWIM", suffix: str | None = None) -> str:
    base = f"{prefix}-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}"
    if suffix:
        safe_suffix = suffix.replace(" ", "-").replace("/", "-")
        return f"{base}-{safe_suffix}"
    return base


BackupJobState = Literal["PENDING", "RUNNING", "VERIFYING", "UPLOADING", "COMPLETED", "FAILED", "CANCELLED"]
RestoreJobState = Literal["PENDING", "RUNNING", "VERIFYING", "RESTORING", "COMPLETED", "FAILED", "CANCELLED"]
BackupDestinationState = Literal["UNKNOWN", "CONFIGURED", "AVAILABLE", "DEGRADED", "UNAVAILABLE"]
AlertLevel = Literal["INFO", "WARNING", "CRITICAL"]


@dataclass(slots=True)
class BackupDestination:
    identifier: str
    name: str
    kind: str
    path: str = ""
    uuid: str = ""
    label: str = ""
    mount_point: str = ""
    state: BackupDestinationState = "UNKNOWN"
    free_space_bytes: int = 0
    read_only: bool = False
    last_checked_at: str = field(default_factory=utc_now)

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class BackupArtifact:
    identifier: str
    backup_id: str
    kind: str
    filename: str
    path: str = ""
    size_bytes: int = 0
    sha256: str = ""
    encrypted: bool = False
    checksum_algorithm: str = "sha256"
    verified_at: str | None = None
    version: str = ""
    git_commit: str = ""

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class BackupJob:
    identifier: str
    backup_id: str
    kind: str
    state: BackupJobState = "PENDING"
    destination: str = ""
    size_bytes: int = 0
    trigger: str = "scheduler"
    git_commit: str = ""
    version: str = ""
    created_at: str = field(default_factory=utc_now)
    started_at: str | None = None
    finished_at: str | None = None
    duration_seconds: float | None = None
    checksum: str = ""
    encrypted: bool = False
    validation_result: str = "pending"

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class BackupManifest:
    identifier: str
    backup_id: str
    version: str
    git_commit: str
    timezone: str
    generated_at: str = field(default_factory=utc_now)
    checksum_algorithm: str = "sha256"
    status: str = "PENDING"
    total_size_bytes: int = 0
    destination_ids: tuple[str, ...] = ()
    artifact_ids: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["destination_ids"] = list(self.destination_ids)
        payload["artifact_ids"] = list(self.artifact_ids)
        return payload


@dataclass(slots=True)
class BackupEvent:
    identifier: str
    backup_id: str
    kind: str
    level: AlertLevel
    message: str
    created_at: str = field(default_factory=utc_now)
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class BackupAlert:
    identifier: str
    level: AlertLevel
    title: str
    message: str
    status: str = "NEW"
    created_at: str = field(default_factory=utc_now)
    acknowledged_by: str | None = None
    acknowledged_at: str | None = None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class BackupSchedule:
    identifier: str
    name: str
    calendar: str
    timezone: str
    source: str
    enabled: bool = True
    status: str = "TARGET"
    next_run_at: str | None = None
    last_run_at: str | None = None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class BackupMetrics:
    total_jobs: int = 0
    successful_jobs: int = 0
    failed_jobs: int = 0
    mean_duration_seconds: float = 0.0
    max_duration_seconds: float = 0.0
    bytes_stored: int = 0
    storage_usage_percent: float = 0.0
    last_success_at: str | None = None
    last_failed_at: str | None = None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class RestoreJob:
    identifier: str
    backup_id: str
    kind: str
    state: RestoreJobState = "PENDING"
    target_environment: str = "isolated"
    created_at: str = field(default_factory=utc_now)
    started_at: str | None = None
    finished_at: str | None = None
    duration_seconds: float | None = None
    checksum_verified: bool = False
    decrypted: bool = False
    validation_result: str = "pending"

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class BackupSettings:
    enabled: bool = True
    timezone: str = "Africa/Douala"
    backup_root: Path = Path("/var/backups/lawim")
    state_root: Path = Path("/var/lib/lawim-backup")
    logs_root: Path = Path("/var/log/lawim-backup")
    temp_root: Path = Path("/var/tmp/lawim-backup")
    google_drive_schedule: tuple[str, str] = ("02:00", "14:30")
    local_replication_interval_minutes: int = 5
    external_backup_weekday: str = "sunday"
    retention_local_days: int = 2
    retention_google_drive_days: int = 30
    retention_external_months: int = 12
    retry_count: int = 3
    timeout_seconds: int = 3600
    verify_after_upload: bool = True
    automated_restore_tests: bool = True

    def as_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["backup_root"] = str(self.backup_root)
        payload["state_root"] = str(self.state_root)
        payload["logs_root"] = str(self.logs_root)
        payload["temp_root"] = str(self.temp_root)
        payload["google_drive_schedule"] = list(self.google_drive_schedule)
        return payload

    def schedules(self) -> tuple[BackupSchedule, ...]:
        base = (
            BackupSchedule(
                identifier="google-drive-0200",
                name="Google Drive backup",
                calendar="TZ=Africa/Douala *-*-* 02:00:00",
                timezone=self.timezone,
                source="systemd",
            ),
            BackupSchedule(
                identifier="google-drive-1430",
                name="Google Drive backup",
                calendar="TZ=Africa/Douala *-*-* 14:30:00",
                timezone=self.timezone,
                source="systemd",
            ),
            BackupSchedule(
                identifier="local-replication",
                name="Local replication",
                calendar="PT5M",
                timezone=self.timezone,
                source="scheduler",
            ),
            BackupSchedule(
                identifier="external-backup-weekly",
                name="External disk copy",
                calendar="P1W",
                timezone=self.timezone,
                source="systemd",
            ),
            BackupSchedule(
                identifier="checksum-daily",
                name="Checksum verification",
                calendar="P1D",
                timezone=self.timezone,
                source="scheduler",
            ),
            BackupSchedule(
                identifier="restore-tests",
                name="Restore tests",
                calendar="P1W / P1M / P3M",
                timezone=self.timezone,
                source="scheduler",
            ),
        )
        return base
