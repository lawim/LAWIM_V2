from __future__ import annotations

from typing import Any, Protocol

from ..program_m_support import count_rows, create_record, get_row_by_key, json_loads, list_rows, tables_present, update_record, utcnow
from .models import (
    BackupAlert,
    BackupArtifact,
    BackupConfiguration,
    BackupDestination,
    BackupEvent,
    BackupJob,
    BackupMetrics,
    BackupSchedule,
    RestoreJob,
    RestoreResult,
    build_backup_id,
)
from .schema_v19_ddl import BACKUP_TABLE_NAMES


class BackupRepository(Protocol):
    def scalar(self, sql: str, params: tuple[object, ...] = ()) -> object | None: ...
    def one(self, sql: str, params: tuple[object, ...] = ()) -> dict[str, object] | None: ...
    def all(self, sql: str, params: tuple[object, ...] = ()) -> list[dict[str, object]]: ...
    def _transaction(self): ...


def _payload(row: dict[str, object] | None) -> dict[str, object]:
    if not row:
        return {}
    data = json_loads(str(row.get("payload_json") or "{}"), {})
    return dict(data) if isinstance(data, dict) else {}


class BackupRepositoryMixin:
    def backup_tables_present(self) -> bool:
        return tables_present(self, BACKUP_TABLE_NAMES)

    def _record_key(self, prefix: str, identifier: str) -> str:
        return f"backup:{prefix}:{identifier}"

    def _upsert_payload_record(
        self,
        table: str,
        *,
        record_key: str,
        name: str,
        kind: str,
        scope: str = "",
        status: str = "active",
        parent_id: int | None = None,
        reference_id: int | None = None,
        secondary_id: int | None = None,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        existing = get_row_by_key(self, table, record_key=record_key)
        if existing is not None:
            row = update_record(
                self,
                table,
                int(existing["id"]),
                record_key=record_key,
                name=name,
                kind=kind,
                scope=scope,
                status=status,
                parent_id=parent_id,
                reference_id=reference_id,
                secondary_id=secondary_id,
                payload=payload or {},
            )
            return row
        return create_record(
            self,
            table,
            record_key=record_key,
            name=name,
            kind=kind,
            scope=scope,
            status=status,
            parent_id=parent_id,
            reference_id=reference_id,
            secondary_id=secondary_id,
            payload=payload or {},
        )

    def seed_backup_catalog(self, configuration: BackupConfiguration | None = None) -> None:
        configuration = configuration or BackupConfiguration()
        self.upsert_backup_configuration(configuration)
        for destination in configuration.destinations():
            self.upsert_backup_destination(destination)
        if count_rows(self, "backup_jobs") == 0:
            for schedule in configuration.schedules():
                job = BackupJob(
                    identifier=build_backup_id(suffix=schedule.identifier),
                    backup_id=build_backup_id(suffix=f"{schedule.identifier}-seed"),
                    kind=schedule.source,
                    state="PENDING",
                    destination=schedule.source,
                    provider=schedule.source,
                    trigger="scheduler",
                    version=configuration.lawim_version,
                    git_commit=configuration.git_commit,
                    validation_result="seeded",
                    source="seed",
                )
                self.save_backup_job(job)
        self.upsert_backup_metrics(BackupMetrics(calculated_at=utcnow()))

    def upsert_backup_configuration(self, configuration: BackupConfiguration) -> BackupConfiguration:
        row = self._upsert_payload_record(
            "backup_configurations",
            record_key=self._record_key("configuration", configuration.identifier),
            name="Backup configuration",
            kind="configuration",
            scope=configuration.timezone,
            status="active" if configuration.enabled else "disabled",
            payload=configuration.as_dict(),
        )
        return BackupConfiguration.from_dict(_payload(row))

    def get_backup_configuration(self, identifier: str = "current") -> BackupConfiguration:
        row = get_row_by_key(self, "backup_configurations", record_key=self._record_key("configuration", identifier))
        if row is None:
            return BackupConfiguration(identifier=identifier)
        return BackupConfiguration.from_dict(_payload(row))

    def list_backup_configurations(self, *, limit: int = 50) -> list[BackupConfiguration]:
        return [BackupConfiguration.from_dict(_payload(row)) for row in list_rows(self, "backup_configurations", limit=limit, order_by="id DESC")]

    def upsert_backup_destination(self, destination: BackupDestination) -> BackupDestination:
        row = self._upsert_payload_record(
            "backup_destinations",
            record_key=self._record_key("destination", destination.identifier),
            name=destination.name,
            kind=destination.kind,
            scope=destination.path or destination.mount_point,
            status=destination.state,
            payload=destination.as_dict(),
        )
        return BackupDestination.from_dict(_payload(row))

    def get_backup_destination(self, identifier: str) -> BackupDestination | None:
        row = get_row_by_key(self, "backup_destinations", record_key=self._record_key("destination", identifier))
        if row is None:
            return None
        return BackupDestination.from_dict(_payload(row))

    def list_backup_destinations(self, *, limit: int = 50) -> list[BackupDestination]:
        rows = list_rows(self, "backup_destinations", limit=limit, order_by="id ASC")
        return [BackupDestination.from_dict(_payload(row)) for row in rows]

    def save_backup_job(self, job: BackupJob) -> BackupJob:
        row = self._upsert_payload_record(
            "backup_jobs",
            record_key=self._record_key("job", job.identifier),
            name=job.backup_id,
            kind=job.kind,
            scope=job.destination or job.provider,
            status=job.state,
            payload=job.as_dict(),
        )
        return BackupJob.from_dict(_payload(row))

    def get_backup_job(self, identifier: str) -> BackupJob | None:
        row = get_row_by_key(self, "backup_jobs", record_key=self._record_key("job", identifier))
        if row is None:
            return None
        return BackupJob.from_dict(_payload(row))

    def list_backup_jobs(self, *, limit: int = 50) -> list[BackupJob]:
        rows = list_rows(self, "backup_jobs", limit=limit, order_by="id DESC")
        return [BackupJob.from_dict(_payload(row)) for row in rows]

    def save_backup_artifact(self, artifact: BackupArtifact) -> BackupArtifact:
        row = self._upsert_payload_record(
            "backup_artifacts",
            record_key=self._record_key("artifact", artifact.identifier),
            name=artifact.filename,
            kind=artifact.kind,
            scope=artifact.provider or artifact.destination_id,
            status="verified" if artifact.checksum_valid else "invalid",
            payload=artifact.as_dict(),
        )
        return BackupArtifact.from_dict(_payload(row))

    def list_backup_artifacts(self, *, limit: int = 50) -> list[BackupArtifact]:
        rows = list_rows(self, "backup_artifacts", limit=limit, order_by="id DESC")
        return [BackupArtifact.from_dict(_payload(row)) for row in rows]

    def save_backup_event(self, event: BackupEvent) -> BackupEvent:
        row = self._upsert_payload_record(
            "backup_events",
            record_key=self._record_key("event", event.identifier),
            name=event.kind,
            kind=event.kind,
            scope=event.source,
            status=event.level.lower(),
            payload=event.as_dict(),
        )
        return BackupEvent.from_dict(_payload(row))

    def list_backup_events(self, *, limit: int = 50) -> list[BackupEvent]:
        rows = list_rows(self, "backup_events", limit=limit, order_by="id DESC")
        return [BackupEvent.from_dict(_payload(row)) for row in rows]

    def save_backup_alert(self, alert: BackupAlert) -> BackupAlert:
        key = alert.code or alert.identifier
        row = self._upsert_payload_record(
            "backup_alerts",
            record_key=self._record_key("alert", key),
            name=alert.title,
            kind=alert.level,
            scope=alert.category,
            status=alert.status,
            payload=alert.as_dict(),
        )
        return BackupAlert.from_dict(_payload(row))

    def list_backup_alerts(self, *, limit: int = 50) -> list[BackupAlert]:
        rows = list_rows(self, "backup_alerts", limit=limit, order_by="id DESC")
        return [BackupAlert.from_dict(_payload(row)) for row in rows]

    def save_restore_job(self, job: RestoreJob) -> RestoreJob:
        row = self._upsert_payload_record(
            "restore_jobs",
            record_key=self._record_key("restore", job.identifier),
            name=job.backup_id,
            kind=job.kind,
            scope=job.target_environment,
            status=job.state,
            payload=job.as_dict(),
        )
        return RestoreJob.from_dict(_payload(row))

    def list_restore_jobs(self, *, limit: int = 50) -> list[RestoreJob]:
        rows = list_rows(self, "restore_jobs", limit=limit, order_by="id DESC")
        return [RestoreJob.from_dict(_payload(row)) for row in rows]

    def save_restore_result(self, result: RestoreResult) -> RestoreResult:
        row = self._upsert_payload_record(
            "restore_results",
            record_key=self._record_key("restore-result", result.identifier),
            name=result.backup_id,
            kind=result.kind,
            scope=result.state,
            status="success" if result.success else "failed",
            payload=result.as_dict(),
        )
        return RestoreResult.from_dict(_payload(row))

    def list_restore_results(self, *, limit: int = 50) -> list[RestoreResult]:
        rows = list_rows(self, "restore_results", limit=limit, order_by="id DESC")
        return [RestoreResult.from_dict(_payload(row)) for row in rows]

    def upsert_backup_metrics(self, metrics: BackupMetrics) -> BackupMetrics:
        row = self._upsert_payload_record(
            "backup_metrics",
            record_key=self._record_key("metrics", "current"),
            name="Backup metrics",
            kind="snapshot",
            scope="global",
            status="current",
            payload=metrics.as_dict(),
        )
        return BackupMetrics.from_dict(_payload(row))

    def get_backup_metrics(self) -> BackupMetrics:
        row = get_row_by_key(self, "backup_metrics", record_key=self._record_key("metrics", "current"))
        if row is None:
            return BackupMetrics()
        return BackupMetrics.from_dict(_payload(row))

    def list_backup_metrics(self, *, limit: int = 10) -> list[BackupMetrics]:
        rows = list_rows(self, "backup_metrics", limit=limit, order_by="id DESC")
        return [BackupMetrics.from_dict(_payload(row)) for row in rows]

