from __future__ import annotations

import os
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


def _jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, set):
        return sorted(_jsonable(item) for item in value)
    return value


def _as_str(value: object, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _as_int(value: object, default: int = 0) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_float(value: object, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if parsed != parsed or parsed in {float("inf"), float("-inf")}:
        return default
    return parsed


def _as_bool(value: object, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    if value is None:
        return default
    return bool(value)


def _as_path(value: object, default: Path) -> Path:
    if value is None:
        return default
    text = str(value).strip()
    if not text:
        return default
    return Path(text).expanduser()


def _as_sequence(value: object, default: tuple[str, ...]) -> tuple[str, ...]:
    if value is None:
        return default
    if isinstance(value, (list, tuple)):
        items = tuple(_as_str(item) for item in value if _as_str(item))
        return items or default
    if isinstance(value, str):
        parts = tuple(part.strip() for part in value.split(",") if part.strip())
        return parts or default
    return default


def _as_dict(value: object, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return dict(default or {})


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
    quota_bytes: int = 0
    used_bytes: int = 0
    available_bytes: int = 0
    health: str = "unknown"
    provider_version: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BackupDestination":
        return cls(
            identifier=_as_str(data.get("identifier")),
            name=_as_str(data.get("name")),
            kind=_as_str(data.get("kind")),
            path=_as_str(data.get("path")),
            uuid=_as_str(data.get("uuid")),
            label=_as_str(data.get("label")),
            mount_point=_as_str(data.get("mount_point")),
            state=_as_str(data.get("state"), "UNKNOWN"),  # type: ignore[arg-type]
            free_space_bytes=_as_int(data.get("free_space_bytes")),
            read_only=_as_bool(data.get("read_only")),
            last_checked_at=_as_str(data.get("last_checked_at"), utc_now()),
            quota_bytes=_as_int(data.get("quota_bytes")),
            used_bytes=_as_int(data.get("used_bytes")),
            available_bytes=_as_int(data.get("available_bytes")),
            health=_as_str(data.get("health"), "unknown"),
            provider_version=_as_str(data.get("provider_version")),
            details=_as_dict(data.get("details")),
        )


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
    job_id: str = ""
    destination_id: str = ""
    provider: str = ""
    storage_uri: str = ""
    checksum_valid: bool = True
    uploaded_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BackupArtifact":
        return cls(
            identifier=_as_str(data.get("identifier")),
            backup_id=_as_str(data.get("backup_id")),
            kind=_as_str(data.get("kind")),
            filename=_as_str(data.get("filename")),
            path=_as_str(data.get("path")),
            size_bytes=_as_int(data.get("size_bytes")),
            sha256=_as_str(data.get("sha256")),
            encrypted=_as_bool(data.get("encrypted")),
            checksum_algorithm=_as_str(data.get("checksum_algorithm"), "sha256"),
            verified_at=data.get("verified_at") if data.get("verified_at") not in {"", None} else None,
            version=_as_str(data.get("version")),
            git_commit=_as_str(data.get("git_commit")),
            job_id=_as_str(data.get("job_id")),
            destination_id=_as_str(data.get("destination_id")),
            provider=_as_str(data.get("provider")),
            storage_uri=_as_str(data.get("storage_uri")),
            checksum_valid=_as_bool(data.get("checksum_valid"), True),
            uploaded_at=data.get("uploaded_at") if data.get("uploaded_at") not in {"", None} else None,
            metadata=_as_dict(data.get("metadata")),
        )


@dataclass(slots=True)
class BackupJob:
    identifier: str
    backup_id: str
    kind: str
    state: BackupJobState = "PENDING"
    destination: str = ""
    provider: str = ""
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
    systemd_unit: str = "lawim-backup.service"
    attempt: int = 1
    notes: str = ""
    source: str = "app"
    artifact_count: int = 0
    alert_count: int = 0

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BackupJob":
        return cls(
            identifier=_as_str(data.get("identifier")),
            backup_id=_as_str(data.get("backup_id")),
            kind=_as_str(data.get("kind")),
            state=_as_str(data.get("state"), "PENDING"),  # type: ignore[arg-type]
            destination=_as_str(data.get("destination")),
            provider=_as_str(data.get("provider")),
            size_bytes=_as_int(data.get("size_bytes")),
            trigger=_as_str(data.get("trigger"), "scheduler"),
            git_commit=_as_str(data.get("git_commit")),
            version=_as_str(data.get("version")),
            created_at=_as_str(data.get("created_at"), utc_now()),
            started_at=data.get("started_at") if data.get("started_at") not in {"", None} else None,
            finished_at=data.get("finished_at") if data.get("finished_at") not in {"", None} else None,
            duration_seconds=_as_float(data.get("duration_seconds")) if data.get("duration_seconds") is not None else None,
            checksum=_as_str(data.get("checksum")),
            encrypted=_as_bool(data.get("encrypted")),
            validation_result=_as_str(data.get("validation_result"), "pending"),
            systemd_unit=_as_str(data.get("systemd_unit"), "lawim-backup.service"),
            attempt=max(1, _as_int(data.get("attempt"), 1)),
            notes=_as_str(data.get("notes")),
            source=_as_str(data.get("source"), "app"),
            artifact_count=_as_int(data.get("artifact_count")),
            alert_count=_as_int(data.get("alert_count")),
        )


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
    job_id: str = ""
    restore_job_id: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        payload = _jsonable(asdict(self))
        payload["destination_ids"] = list(self.destination_ids)
        payload["artifact_ids"] = list(self.artifact_ids)
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BackupManifest":
        return cls(
            identifier=_as_str(data.get("identifier")),
            backup_id=_as_str(data.get("backup_id")),
            version=_as_str(data.get("version")),
            git_commit=_as_str(data.get("git_commit")),
            timezone=_as_str(data.get("timezone")),
            generated_at=_as_str(data.get("generated_at"), utc_now()),
            checksum_algorithm=_as_str(data.get("checksum_algorithm"), "sha256"),
            status=_as_str(data.get("status"), "PENDING"),
            total_size_bytes=_as_int(data.get("total_size_bytes")),
            destination_ids=_as_sequence(data.get("destination_ids"), ()),
            artifact_ids=_as_sequence(data.get("artifact_ids"), ()),
            job_id=_as_str(data.get("job_id")),
            restore_job_id=_as_str(data.get("restore_job_id")),
            details=_as_dict(data.get("details")),
        )


@dataclass(slots=True)
class BackupEvent:
    identifier: str
    backup_id: str
    kind: str
    level: AlertLevel
    message: str
    created_at: str = field(default_factory=utc_now)
    details: dict[str, Any] = field(default_factory=dict)
    source: str = "backup"
    job_id: str = ""
    restore_id: str = ""
    alert_id: str = ""

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BackupEvent":
        return cls(
            identifier=_as_str(data.get("identifier")),
            backup_id=_as_str(data.get("backup_id")),
            kind=_as_str(data.get("kind")),
            level=_as_str(data.get("level"), "INFO"),  # type: ignore[arg-type]
            message=_as_str(data.get("message")),
            created_at=_as_str(data.get("created_at"), utc_now()),
            details=_as_dict(data.get("details")),
            source=_as_str(data.get("source"), "backup"),
            job_id=_as_str(data.get("job_id")),
            restore_id=_as_str(data.get("restore_id")),
            alert_id=_as_str(data.get("alert_id")),
        )


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
    code: str = ""
    category: str = "backup"
    source: str = "backup"
    target: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BackupAlert":
        return cls(
            identifier=_as_str(data.get("identifier")),
            level=_as_str(data.get("level"), "INFO"),  # type: ignore[arg-type]
            title=_as_str(data.get("title")),
            message=_as_str(data.get("message")),
            status=_as_str(data.get("status"), "NEW"),
            created_at=_as_str(data.get("created_at"), utc_now()),
            acknowledged_by=data.get("acknowledged_by") if data.get("acknowledged_by") not in {"", None} else None,
            acknowledged_at=data.get("acknowledged_at") if data.get("acknowledged_at") not in {"", None} else None,
            code=_as_str(data.get("code")),
            category=_as_str(data.get("category"), "backup"),
            source=_as_str(data.get("source"), "backup"),
            target=_as_str(data.get("target")),
            details=_as_dict(data.get("details")),
        )


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
    provider: str = "systemd"
    description: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BackupSchedule":
        return cls(
            identifier=_as_str(data.get("identifier")),
            name=_as_str(data.get("name")),
            calendar=_as_str(data.get("calendar")),
            timezone=_as_str(data.get("timezone")),
            source=_as_str(data.get("source")),
            enabled=_as_bool(data.get("enabled"), True),
            status=_as_str(data.get("status"), "TARGET"),
            next_run_at=data.get("next_run_at") if data.get("next_run_at") not in {"", None} else None,
            last_run_at=data.get("last_run_at") if data.get("last_run_at") not in {"", None} else None,
            provider=_as_str(data.get("provider"), "systemd"),
            description=_as_str(data.get("description")),
            details=_as_dict(data.get("details")),
        )


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
    average_size_bytes: float = 0.0
    total_size_bytes: int = 0
    transferred_bytes: int = 0
    upload_time_seconds: float = 0.0
    restore_time_seconds: float = 0.0
    alert_count: int = 0
    checksum_validations: int = 0
    checksum_failures: int = 0
    availability_percent: float = 0.0
    rpo_seconds: float = 0.0
    rto_seconds: float = 0.0
    last_backup_age_seconds: float = 0.0
    calculated_at: str = field(default_factory=utc_now)

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BackupMetrics":
        return cls(
            total_jobs=_as_int(data.get("total_jobs")),
            successful_jobs=_as_int(data.get("successful_jobs")),
            failed_jobs=_as_int(data.get("failed_jobs")),
            mean_duration_seconds=_as_float(data.get("mean_duration_seconds")),
            max_duration_seconds=_as_float(data.get("max_duration_seconds")),
            bytes_stored=_as_int(data.get("bytes_stored")),
            storage_usage_percent=_as_float(data.get("storage_usage_percent")),
            last_success_at=data.get("last_success_at") if data.get("last_success_at") not in {"", None} else None,
            last_failed_at=data.get("last_failed_at") if data.get("last_failed_at") not in {"", None} else None,
            average_size_bytes=_as_float(data.get("average_size_bytes")),
            total_size_bytes=_as_int(data.get("total_size_bytes")),
            transferred_bytes=_as_int(data.get("transferred_bytes")),
            upload_time_seconds=_as_float(data.get("upload_time_seconds")),
            restore_time_seconds=_as_float(data.get("restore_time_seconds")),
            alert_count=_as_int(data.get("alert_count")),
            checksum_validations=_as_int(data.get("checksum_validations")),
            checksum_failures=_as_int(data.get("checksum_failures")),
            availability_percent=_as_float(data.get("availability_percent")),
            rpo_seconds=_as_float(data.get("rpo_seconds")),
            rto_seconds=_as_float(data.get("rto_seconds")),
            last_backup_age_seconds=_as_float(data.get("last_backup_age_seconds")),
            calculated_at=_as_str(data.get("calculated_at"), utc_now()),
        )


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
    artifact_id: str = ""
    systemd_unit: str = "lawim-backup.service"
    report: dict[str, Any] = field(default_factory=dict)
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "RestoreJob":
        return cls(
            identifier=_as_str(data.get("identifier")),
            backup_id=_as_str(data.get("backup_id")),
            kind=_as_str(data.get("kind")),
            state=_as_str(data.get("state"), "PENDING"),  # type: ignore[arg-type]
            target_environment=_as_str(data.get("target_environment"), "isolated"),
            created_at=_as_str(data.get("created_at"), utc_now()),
            started_at=data.get("started_at") if data.get("started_at") not in {"", None} else None,
            finished_at=data.get("finished_at") if data.get("finished_at") not in {"", None} else None,
            duration_seconds=_as_float(data.get("duration_seconds")) if data.get("duration_seconds") is not None else None,
            checksum_verified=_as_bool(data.get("checksum_verified")),
            decrypted=_as_bool(data.get("decrypted")),
            validation_result=_as_str(data.get("validation_result"), "pending"),
            artifact_id=_as_str(data.get("artifact_id")),
            systemd_unit=_as_str(data.get("systemd_unit"), "lawim-backup.service"),
            report=_as_dict(data.get("report")),
            details=_as_dict(data.get("details")),
        )


@dataclass(slots=True)
class RestoreResult:
    identifier: str
    restore_job_id: str
    backup_id: str
    kind: str
    state: RestoreJobState = "COMPLETED"
    success: bool = True
    created_at: str = field(default_factory=utc_now)
    completed_at: str | None = None
    duration_seconds: float | None = None
    checksum_verified: bool = False
    media_restored: bool = False
    database_restored: bool = False
    report: dict[str, Any] = field(default_factory=dict)
    notes: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "RestoreResult":
        return cls(
            identifier=_as_str(data.get("identifier")),
            restore_job_id=_as_str(data.get("restore_job_id")),
            backup_id=_as_str(data.get("backup_id")),
            kind=_as_str(data.get("kind")),
            state=_as_str(data.get("state"), "COMPLETED"),  # type: ignore[arg-type]
            success=_as_bool(data.get("success"), True),
            created_at=_as_str(data.get("created_at"), utc_now()),
            completed_at=data.get("completed_at") if data.get("completed_at") not in {"", None} else None,
            duration_seconds=_as_float(data.get("duration_seconds")) if data.get("duration_seconds") is not None else None,
            checksum_verified=_as_bool(data.get("checksum_verified")),
            media_restored=_as_bool(data.get("media_restored")),
            database_restored=_as_bool(data.get("database_restored")),
            report=_as_dict(data.get("report")),
            notes=_as_str(data.get("notes")),
            details=_as_dict(data.get("details")),
        )


@dataclass(slots=True)
class BackupConfiguration:
    identifier: str = "current"
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
    systemd_service: str = "lawim-backup.service"
    systemd_timer: str = "lawim-backup.timer"
    lawim_version: str = ""
    git_commit: str = ""
    last_checked_at: str = field(default_factory=utc_now)
    alerts_enabled: bool = True
    restore_isolation_required: bool = True

    def as_dict(self) -> dict[str, object]:
        payload = _jsonable(asdict(self))
        payload["backup_root"] = str(self.backup_root)
        payload["state_root"] = str(self.state_root)
        payload["logs_root"] = str(self.logs_root)
        payload["temp_root"] = str(self.temp_root)
        payload["google_drive_schedule"] = list(self.google_drive_schedule)
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "BackupConfiguration":
        schedule = _as_sequence(data.get("google_drive_schedule"), ("02:00", "14:30"))
        if len(schedule) < 2:
            schedule = (schedule[0] if schedule else "02:00", "14:30")
        return cls(
            identifier=_as_str(data.get("identifier"), "current"),
            enabled=_as_bool(data.get("enabled"), True),
            timezone=_as_str(data.get("timezone"), "Africa/Douala"),
            backup_root=_as_path(data.get("backup_root"), Path("/var/backups/lawim")),
            state_root=_as_path(data.get("state_root"), Path("/var/lib/lawim-backup")),
            logs_root=_as_path(data.get("logs_root"), Path("/var/log/lawim-backup")),
            temp_root=_as_path(data.get("temp_root"), Path("/var/tmp/lawim-backup")),
            google_drive_schedule=(schedule[0], schedule[1]),
            local_replication_interval_minutes=_as_int(data.get("local_replication_interval_minutes"), 5),
            external_backup_weekday=_as_str(data.get("external_backup_weekday"), "sunday"),
            retention_local_days=_as_int(data.get("retention_local_days"), 2),
            retention_google_drive_days=_as_int(data.get("retention_google_drive_days"), 30),
            retention_external_months=_as_int(data.get("retention_external_months"), 12),
            retry_count=_as_int(data.get("retry_count"), 3),
            timeout_seconds=_as_int(data.get("timeout_seconds"), 3600),
            verify_after_upload=_as_bool(data.get("verify_after_upload"), True),
            automated_restore_tests=_as_bool(data.get("automated_restore_tests"), True),
            systemd_service=_as_str(data.get("systemd_service"), "lawim-backup.service"),
            systemd_timer=_as_str(data.get("systemd_timer"), "lawim-backup.timer"),
            lawim_version=_as_str(data.get("lawim_version")),
            git_commit=_as_str(data.get("git_commit")),
            last_checked_at=_as_str(data.get("last_checked_at"), utc_now()),
            alerts_enabled=_as_bool(data.get("alerts_enabled"), True),
            restore_isolation_required=_as_bool(data.get("restore_isolation_required"), True),
        )

    @classmethod
    def from_env(
        cls,
        *,
        workspace_root: Path | None = None,
        app_env: str | None = None,
    ) -> "BackupConfiguration":
        runtime_env = _as_str(app_env or os.getenv("APP_ENV"), "").lower()

        def _env_path(name: str, default: Path) -> Path:
            raw = os.getenv(name)
            return Path(raw).expanduser() if raw and raw.strip() else default

        if runtime_env == "test":
            base = workspace_root or Path(os.getenv("TMPDIR", "/tmp")) / "lawim-backup"
            return cls(
                backup_root=_env_path("BACKUP_LOCAL_PATH", base / "backups"),
                state_root=_env_path("BACKUP_STATE_PATH", base / "state"),
                logs_root=_env_path("BACKUP_LOGS_PATH", base / "logs"),
                temp_root=_env_path("BACKUP_TEMP_PATH", base / "tmp"),
                timezone=os.getenv("BACKUP_TIMEZONE", "Africa/Douala"),
                google_drive_schedule=_as_sequence(os.getenv("BACKUP_GOOGLE_DRIVE_SCHEDULE"), ("02:00", "14:30")),
                local_replication_interval_minutes=int(os.getenv("BACKUP_LOCAL_REPLICATION_INTERVAL_MINUTES", "5")),
                external_backup_weekday=os.getenv("BACKUP_EXTERNAL_WEEKDAY", "sunday"),
                retention_local_days=int(os.getenv("BACKUP_RETENTION_LOCAL_DAYS", "2")),
                retention_google_drive_days=int(os.getenv("BACKUP_RETENTION_GOOGLE_DRIVE_DAYS", "30")),
                retention_external_months=int(os.getenv("BACKUP_RETENTION_EXTERNAL_MONTHS", "12")),
                retry_count=int(os.getenv("BACKUP_RETRY_COUNT", "3")),
                timeout_seconds=int(os.getenv("BACKUP_TIMEOUT_SECONDS", "3600")),
                verify_after_upload=_as_bool(os.getenv("BACKUP_VERIFY_AFTER_UPLOAD"), True),
                automated_restore_tests=_as_bool(os.getenv("BACKUP_AUTOMATED_RESTORE_TESTS"), True),
                systemd_service=os.getenv("BACKUP_SYSTEMD_SERVICE", "lawim-backup.service"),
                systemd_timer=os.getenv("BACKUP_SYSTEMD_TIMER", "lawim-backup.timer"),
            )

        return cls(
            backup_root=_env_path("BACKUP_LOCAL_PATH", Path("/var/backups/lawim")),
            state_root=_env_path("BACKUP_STATE_PATH", Path("/var/lib/lawim-backup")),
            logs_root=_env_path("BACKUP_LOGS_PATH", Path("/var/log/lawim-backup")),
            temp_root=_env_path("BACKUP_TEMP_PATH", Path("/var/tmp/lawim-backup")),
            timezone=os.getenv("BACKUP_TIMEZONE", "Africa/Douala"),
            google_drive_schedule=_as_sequence(os.getenv("BACKUP_GOOGLE_DRIVE_SCHEDULE"), ("02:00", "14:30")),
            local_replication_interval_minutes=int(os.getenv("BACKUP_LOCAL_REPLICATION_INTERVAL_MINUTES", "5")),
            external_backup_weekday=os.getenv("BACKUP_EXTERNAL_WEEKDAY", "sunday"),
            retention_local_days=int(os.getenv("BACKUP_RETENTION_LOCAL_DAYS", "2")),
            retention_google_drive_days=int(os.getenv("BACKUP_RETENTION_GOOGLE_DRIVE_DAYS", "30")),
            retention_external_months=int(os.getenv("BACKUP_RETENTION_EXTERNAL_MONTHS", "12")),
            retry_count=int(os.getenv("BACKUP_RETRY_COUNT", "3")),
            timeout_seconds=int(os.getenv("BACKUP_TIMEOUT_SECONDS", "3600")),
            verify_after_upload=_as_bool(os.getenv("BACKUP_VERIFY_AFTER_UPLOAD"), True),
            automated_restore_tests=_as_bool(os.getenv("BACKUP_AUTOMATED_RESTORE_TESTS"), True),
            systemd_service=os.getenv("BACKUP_SYSTEMD_SERVICE", "lawim-backup.service"),
            systemd_timer=os.getenv("BACKUP_SYSTEMD_TIMER", "lawim-backup.timer"),
        )

    def policy(self) -> dict[str, object]:
        return {
            "google_drive": {"time": list(self.google_drive_schedule), "timezone": self.timezone},
            "local_replication_interval_minutes": self.local_replication_interval_minutes,
            "external_backup_weekday": self.external_backup_weekday,
            "retention": {
                "local_days": self.retention_local_days,
                "google_drive_days": self.retention_google_drive_days,
                "external_months": self.retention_external_months,
            },
            "retry_count": self.retry_count,
            "timeout_seconds": self.timeout_seconds,
            "verify_after_upload": self.verify_after_upload,
            "automated_restore_tests": self.automated_restore_tests,
        }

    def schedules(self) -> tuple[BackupSchedule, ...]:
        base = (
            BackupSchedule(
                identifier="google-drive-0200",
                name="Google Drive backup",
                calendar=f"TZ={self.timezone} *-*-* {self.google_drive_schedule[0]}:00",
                timezone=self.timezone,
                source="google-drive",
            ),
            BackupSchedule(
                identifier="google-drive-1430",
                name="Google Drive backup",
                calendar=f"TZ={self.timezone} *-*-* {self.google_drive_schedule[1]}:00",
                timezone=self.timezone,
                source="google-drive",
            ),
            BackupSchedule(
                identifier="local-replication",
                name="Local replication",
                calendar=f"every {self.local_replication_interval_minutes} minutes",
                timezone=self.timezone,
                source="local",
            ),
            BackupSchedule(
                identifier="external-offline",
                name="External offline copy",
                calendar=f"weekly on {self.external_backup_weekday}",
                timezone=self.timezone,
                source="external",
            ),
        )
        return base

    def destinations(self) -> tuple[BackupDestination, ...]:
        return (
            BackupDestination(
                identifier="local",
                name="Local disk",
                kind="local_disk",
                path=str(self.backup_root),
                mount_point=str(self.state_root),
                state="CONFIGURED",
                health="watch" if not self.backup_root.exists() else "ready",
                details={"role": "primary-local"},
            ),
            BackupDestination(
                identifier="google-drive",
                name="Google Drive",
                kind="google_drive",
                state="CONFIGURED",
                health="configured",
                details={"role": "cloud-offsite"},
            ),
            BackupDestination(
                identifier="external-disk",
                name="External disk",
                kind="external_disk",
                state="UNKNOWN",
                health="watch",
                details={"role": "offline-offsite"},
            ),
        )


BackupSettings = BackupConfiguration


@dataclass(slots=True)
class RestoreResultBundle:
    restore_job: RestoreJob
    restore_result: RestoreResult


__all__ = [
    "AlertLevel",
    "BackupAlert",
    "BackupArtifact",
    "BackupConfiguration",
    "BackupDestination",
    "BackupDestinationState",
    "BackupEvent",
    "BackupJob",
    "BackupJobState",
    "BackupManifest",
    "BackupMetrics",
    "BackupSchedule",
    "BackupSettings",
    "RestoreJob",
    "RestoreJobState",
    "RestoreResult",
    "RestoreResultBundle",
    "build_backup_id",
    "utc_now",
]
