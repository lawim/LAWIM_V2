from __future__ import annotations

from typing import Any
from uuid import uuid4

from ..config import AppConfig
from .models import (
    AlertLevel,
    BackupAlert,
    BackupDestination,
    BackupEvent,
    BackupJob,
    BackupMetrics,
    BackupSchedule,
    BackupSettings,
    RestoreJob,
    build_backup_id,
    utc_now,
)
from .providers import ExternalDiskProvider, GoogleDriveProvider, LocalDiskProvider
from .repository import InMemoryBackupRepository


class BackupService:
    def __init__(
        self,
        repository: object | None = None,
        config: AppConfig | None = None,
        settings: BackupSettings | None = None,
    ) -> None:
        self.repository = repository
        self.config = config
        self.settings = settings or BackupSettings()
        self.store = InMemoryBackupRepository()
        self.providers = {
            "local": LocalDiskProvider(identifier="local", name="Local disk", kind="local_disk"),
            "google_drive": GoogleDriveProvider(identifier="google-drive", name="Google Drive", kind="google_drive"),
            "external_disk": ExternalDiskProvider(identifier="external-disk", name="External disk", kind="external_disk"),
        }
        self.store.destinations.extend(
            [
                BackupDestination(
                    identifier="local",
                    name="Local disk",
                    kind="local_disk",
                    path=str(self.settings.backup_root),
                    mount_point=str(self.settings.state_root),
                    state="UNKNOWN",
                ),
                BackupDestination(
                    identifier="google-drive",
                    name="Google Drive",
                    kind="google_drive",
                    state="CONFIGURED",
                ),
                BackupDestination(
                    identifier="external-disk",
                    name="External disk",
                    kind="external_disk",
                    state="UNKNOWN",
                ),
            ]
        )
        self.store.schedules.extend(self.settings.schedules())
        self._seed_schedule_jobs()

    def _seed_schedule_jobs(self) -> None:
        for schedule in self.store.schedules:
            backup_id = build_backup_id(suffix=schedule.identifier)
            self.store.add_job(
                BackupJob(
                    identifier=backup_id,
                    backup_id=backup_id,
                    kind=schedule.identifier,
                    state="PENDING",
                )
            )

    def list(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [job.as_dict() for job in self.store.list_jobs(limit=limit)]

    def history(self, *, limit: int = 50) -> list[dict[str, object]]:
        return self.list(limit=limit)

    def schedules(self) -> list[dict[str, object]]:
        return [schedule.as_dict() for schedule in self.store.list_schedules()]

    def destinations(self) -> list[dict[str, object]]:
        return [destination.as_dict() for destination in self.store.list_destinations()]

    def alerts(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [alert.as_dict() for alert in self.store.list_alerts(limit=limit)]

    def events(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [event.as_dict() for event in self.store.list_events(limit=limit)]

    def restore_history(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [job.as_dict() for job in self.store.list_restore_jobs(limit=limit)]

    def configuration(self) -> dict[str, object]:
        return self.settings.as_dict()

    def metrics(self) -> dict[str, object]:
        jobs = self.store.list_jobs()
        completed = [job for job in jobs if job.state == "COMPLETED"]
        failed = [job for job in jobs if job.state == "FAILED"]
        durations = [job.duration_seconds for job in jobs if job.duration_seconds is not None]
        metrics = BackupMetrics(
            total_jobs=len(jobs),
            successful_jobs=len(completed),
            failed_jobs=len(failed),
            mean_duration_seconds=(sum(durations) / len(durations)) if durations else 0.0,
            max_duration_seconds=max(durations) if durations else 0.0,
        )
        return metrics.as_dict()

    def last_backup(self) -> dict[str, object] | None:
        jobs = self.store.list_jobs()
        return jobs[-1].as_dict() if jobs else None

    def last_restore(self) -> dict[str, object] | None:
        jobs = self.store.list_restore_jobs()
        return jobs[-1].as_dict() if jobs else None

    def next_backup(self) -> dict[str, object] | None:
        schedules = self.store.list_schedules()
        return schedules[0].as_dict() if schedules else None

    def status(self) -> dict[str, object]:
        jobs = [job.as_dict() for job in self.store.list_jobs()]
        destinations = self.destinations()
        alerts = self.alerts(limit=10)
        last_success = next((job for job in reversed(jobs) if job["state"] == "COMPLETED"), None)
        last_failed = next((job for job in reversed(jobs) if job["state"] == "FAILED"), None)
        if not jobs:
            global_status = "UNKNOWN"
        elif all(job["state"] == "PENDING" for job in jobs):
            global_status = "WATCH"
        elif last_success is None:
            global_status = "CRITICAL"
        elif any(dest["state"] in {"UNAVAILABLE", "DEGRADED"} for dest in destinations):
            global_status = "DEGRADED"
        elif alerts:
            global_status = "WATCH"
        else:
            global_status = "PROTECTED"
        return {
            "global_status": global_status,
            "policy": {
                "google_drive": {"time": list(self.settings.google_drive_schedule), "timezone": self.settings.timezone},
                "local_replication_interval_minutes": self.settings.local_replication_interval_minutes,
                "external_backup_weekday": self.settings.external_backup_weekday,
            },
            "destinations": destinations,
            "alerts": alerts,
            "last_backup": last_success,
            "last_failed_backup": last_failed,
            "next_backup": self.next_backup(),
            "last_restore": self.last_restore(),
            "metrics": self.metrics(),
        }

    def record_job(
        self,
        *,
        kind: str,
        state: str = "PENDING",
        destination: str = "",
        size_bytes: int = 0,
        trigger: str = "scheduler",
        git_commit: str = "",
        version: str = "",
        duration_seconds: float | None = None,
    ) -> BackupJob:
        unique_suffix = uuid4().hex[:8]
        job = BackupJob(
            identifier=build_backup_id(suffix=f"job-{unique_suffix}"),
            backup_id=build_backup_id(suffix=f"backup-{unique_suffix}"),
            kind=kind,
            state=state,  # type: ignore[arg-type]
            destination=destination,
            size_bytes=size_bytes,
            trigger=trigger,
            git_commit=git_commit,
            version=version,
            duration_seconds=duration_seconds,
        )
        self.store.add_job(job)
        return job

    def record_restore_job(
        self,
        *,
        kind: str,
        state: str = "PENDING",
        target_environment: str = "isolated",
    ) -> RestoreJob:
        unique_suffix = uuid4().hex[:8]
        job = RestoreJob(
            identifier=build_backup_id(suffix=f"restore-{unique_suffix}"),
            backup_id=build_backup_id(suffix=f"restore-src-{unique_suffix}"),
            kind=kind,
            state=state,  # type: ignore[arg-type]
            target_environment=target_environment,
        )
        self.store.add_restore_job(job)
        return job

    def record_alert(self, *, level: AlertLevel, title: str, message: str, status: str = "NEW") -> BackupAlert:
        alert = BackupAlert(
            identifier=build_backup_id(suffix=f"alert-{uuid4().hex[:8]}"),
            level=level,
            title=title,
            message=message,
            status=status,
        )
        self.store.add_alert(alert)
        return alert

    def record_event(self, *, backup_id: str, kind: str, level: AlertLevel, message: str) -> BackupEvent:
        event = BackupEvent(
            identifier=build_backup_id(suffix=f"event-{uuid4().hex[:8]}"),
            backup_id=backup_id,
            kind=kind,
            level=level,
            message=message,
        )
        self.store.add_event(event)
        return event

    def get_destination(self, identifier: str) -> dict[str, object] | None:
        for destination in self.destinations():
            if destination["identifier"] == identifier:
                return destination
        return None

    def require_destination(self, identifier: str) -> dict[str, object]:
        destination = self.get_destination(identifier)
        if destination is None:
            raise KeyError(f"Unknown backup destination: {identifier}")
        return destination

    def touch(self) -> str:
        return utc_now()
