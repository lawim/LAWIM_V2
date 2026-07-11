from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .models import BackupAlert, BackupArtifact, BackupDestination, BackupEvent, BackupJob, BackupSchedule, RestoreJob


class BackupRepository(Protocol):
    def add_job(self, job: BackupJob) -> BackupJob: ...
    def add_restore_job(self, job: RestoreJob) -> RestoreJob: ...
    def add_event(self, event: BackupEvent) -> BackupEvent: ...
    def add_alert(self, alert: BackupAlert) -> BackupAlert: ...
    def list_jobs(self, *, limit: int = 50) -> list[BackupJob]: ...
    def list_restore_jobs(self, *, limit: int = 50) -> list[RestoreJob]: ...
    def list_events(self, *, limit: int = 50) -> list[BackupEvent]: ...
    def list_alerts(self, *, limit: int = 50) -> list[BackupAlert]: ...
    def list_artifacts(self, *, limit: int = 50) -> list[BackupArtifact]: ...
    def list_destinations(self) -> list[BackupDestination]: ...
    def list_schedules(self) -> list[BackupSchedule]: ...


@dataclass(slots=True)
class InMemoryBackupRepository:
    jobs: list[BackupJob] = field(default_factory=list)
    restore_jobs: list[RestoreJob] = field(default_factory=list)
    events: list[BackupEvent] = field(default_factory=list)
    alerts: list[BackupAlert] = field(default_factory=list)
    artifacts: list[BackupArtifact] = field(default_factory=list)
    destinations: list[BackupDestination] = field(default_factory=list)
    schedules: list[BackupSchedule] = field(default_factory=list)

    def add_job(self, job: BackupJob) -> BackupJob:
        self.jobs.append(job)
        return job

    def add_restore_job(self, job: RestoreJob) -> RestoreJob:
        self.restore_jobs.append(job)
        return job

    def add_event(self, event: BackupEvent) -> BackupEvent:
        self.events.append(event)
        return event

    def add_alert(self, alert: BackupAlert) -> BackupAlert:
        self.alerts.append(alert)
        return alert

    def list_jobs(self, *, limit: int = 50) -> list[BackupJob]:
        return self.jobs[-limit:]

    def list_restore_jobs(self, *, limit: int = 50) -> list[RestoreJob]:
        return self.restore_jobs[-limit:]

    def list_events(self, *, limit: int = 50) -> list[BackupEvent]:
        return self.events[-limit:]

    def list_alerts(self, *, limit: int = 50) -> list[BackupAlert]:
        return self.alerts[-limit:]

    def list_artifacts(self, *, limit: int = 50) -> list[BackupArtifact]:
        return self.artifacts[-limit:]

    def list_destinations(self) -> list[BackupDestination]:
        return list(self.destinations)

    def list_schedules(self) -> list[BackupSchedule]:
        return list(self.schedules)
