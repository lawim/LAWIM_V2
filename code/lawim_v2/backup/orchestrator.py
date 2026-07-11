from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from .. import __version__ as LAWIM_VERSION
from ..config import AppConfig
from ..db import LawimRepository
from .models import (
    AlertLevel,
    BackupAlert,
    BackupArtifact,
    BackupConfiguration,
    BackupDestination,
    BackupEvent,
    BackupJob,
    BackupMetrics,
    BackupSchedule,
    BackupSettings,
    RestoreJob,
    RestoreJobState,
    RestoreResult,
    RestoreResultBundle,
    build_backup_id,
    utc_now,
)
from .providers import ExternalDiskProvider, GoogleDriveProvider, LocalDiskProvider, StorageProvider


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        normalized = text.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _seconds_between(start: str | None, end: str | None) -> float | None:
    start_dt = _parse_datetime(start)
    end_dt = _parse_datetime(end)
    if start_dt is None or end_dt is None:
        return None
    return max(0.0, (end_dt - start_dt).total_seconds())


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_commit() -> str:
    root = Path(__file__).resolve().parents[3]
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _systemctl_show(unit: str, properties: tuple[str, ...]) -> dict[str, str]:
    command = ["systemctl", "show", unit, "--no-page"]
    command.extend(f"--property={prop}" for prop in properties)
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=10)
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return {}
    if result.returncode != 0:
        return {}
    payload: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        payload[key.strip()] = value.strip()
    return payload


def _systemd_time_string(raw: str | None) -> str | None:
    if not raw:
        return None
    text = raw.strip()
    if not text:
        return None
    if text.isdigit():
        try:
            micros = int(text)
            if micros > 0:
                return datetime.fromtimestamp(micros / 1_000_000, tz=timezone.utc).isoformat()
        except (OverflowError, ValueError):
            return text
    return text


def _tzinfo(name: str) -> ZoneInfo | timezone:
    try:
        return ZoneInfo(name)
    except Exception:
        return timezone.utc


def _next_occurrence_for_calendar(calendar: str, *, timezone_name: str) -> str | None:
    now = datetime.now(_tzinfo(timezone_name))
    if "every" in calendar and "minutes" in calendar:
        parts = calendar.split()
        try:
            minutes = int(parts[1])
        except (IndexError, ValueError):
            minutes = 5
        return (now + timedelta(minutes=max(1, minutes))).replace(microsecond=0).isoformat()
    if "weekly on" in calendar:
        weekday_name = calendar.split("weekly on", 1)[1].strip().split()[0].lower() if "weekly on" in calendar else "sunday"
        weekday_map = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }
        target = weekday_map.get(weekday_name, 6)
        days_ahead = (target - now.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        next_run = now + timedelta(days=days_ahead)
        return next_run.replace(microsecond=0).isoformat()
    import re

    match = re.search(r"(\d{2}):(\d{2}):00", calendar)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if candidate <= now:
            candidate += timedelta(days=1)
        return candidate.isoformat()
    return None


def _artifact_manifest_path(configuration: BackupConfiguration, backup_id: str, filename: str) -> Path:
    return configuration.backup_root / backup_id / filename


class BackupEventBus:
    def __init__(self, repository: LawimRepository) -> None:
        self.repository = repository

    def record(
        self,
        *,
        kind: str,
        level: AlertLevel,
        message: str,
        backup_id: str = "",
        details: dict[str, Any] | None = None,
        source: str = "backup",
        job_id: str = "",
        restore_id: str = "",
        alert_id: str = "",
        identifier: str | None = None,
    ) -> BackupEvent:
        event = BackupEvent(
            identifier=identifier or build_backup_id(suffix=f"event-{kind.replace('.', '-')}" ),
            backup_id=backup_id,
            kind=kind,
            level=level,
            message=message,
            details=details or {},
            source=source,
            job_id=job_id,
            restore_id=restore_id,
            alert_id=alert_id,
        )
        return self.repository.save_backup_event(event)

    def list(self, *, limit: int = 50) -> list[BackupEvent]:
        return self.repository.list_backup_events(limit=limit)


class BackupAlertService:
    def __init__(self, repository: LawimRepository, event_bus: BackupEventBus, configuration: BackupConfiguration) -> None:
        self.repository = repository
        self.event_bus = event_bus
        self.configuration = configuration

    def list(self, *, limit: int = 50) -> list[BackupAlert]:
        return self.repository.list_backup_alerts(limit=limit)

    def active_alerts(self, *, limit: int = 50) -> list[BackupAlert]:
        return [alert for alert in self.list(limit=limit) if alert.status not in {"RESOLVED", "ACKNOWLEDGED"}]

    def raise_alert(
        self,
        *,
        code: str,
        level: AlertLevel,
        title: str,
        message: str,
        target: str = "",
        category: str = "backup",
        details: dict[str, Any] | None = None,
        source: str = "backup",
    ) -> BackupAlert:
        alert = BackupAlert(
            identifier=build_backup_id(suffix=f"alert-{code}"),
            code=code,
            level=level,
            title=title,
            message=message,
            status="NEW",
            category=category,
            source=source,
            target=target,
            details=details or {},
        )
        saved = self.repository.save_backup_alert(alert)
        self.event_bus.record(
            kind=f"backup.alert.{code}",
            level=level,
            message=message,
            alert_id=saved.identifier,
            details={"title": title, "target": target, "category": category},
        )
        return saved

    def acknowledge(self, identifier: str, *, actor: str | None = None) -> BackupAlert:
        existing = next((alert for alert in self.list(limit=200) if alert.identifier == identifier or alert.code == identifier), None)
        if existing is None:
            raise KeyError(f"Unknown backup alert: {identifier}")
        updated = BackupAlert(
            **{
                **existing.as_dict(),
                "status": "ACKNOWLEDGED",
                "acknowledged_by": actor,
                "acknowledged_at": utc_now(),
            }
        )
        return self.repository.save_backup_alert(updated)

    def sync_from_state(
        self,
        *,
        health: dict[str, Any],
        providers: list[dict[str, Any]],
        jobs: list[dict[str, Any]],
        restores: list[dict[str, Any]],
        metrics: BackupMetrics,
    ) -> list[BackupAlert]:
        desired: list[BackupAlert] = []
        for provider in providers:
            identifier = str(provider.get("identifier") or "")
            available = bool(provider.get("available"))
            state = str(provider.get("state") or "").upper()
            if identifier == "google-drive" and not available:
                desired.append(
                    BackupAlert(
                        identifier=build_backup_id(suffix="google-drive-unavailable"),
                        code="google_drive_unavailable",
                        level="CRITICAL",
                        title="Google Drive indisponible",
                        message="Le provider Google Drive n'est pas disponible.",
                        category="destination",
                        target=identifier,
                        details=provider,
                    )
                )
            elif identifier == "local" and not available:
                desired.append(
                    BackupAlert(
                        identifier=build_backup_id(suffix="local-disk-missing"),
                        code="local_disk_missing",
                        level="CRITICAL",
                        title="Disque local absent",
                        message="Le disque local de sauvegarde est indisponible.",
                        category="destination",
                        target=identifier,
                        details=provider,
                    )
                )
            elif identifier == "external-disk" and not available:
                desired.append(
                    BackupAlert(
                        identifier=build_backup_id(suffix="external-disk-missing"),
                        code="external_disk_missing",
                        level="WARNING",
                        title="Disque externe absent",
                        message="Le disque externe d'archivage n'est pas monté.",
                        category="destination",
                        target=identifier,
                        details=provider,
                    )
                )
            if state in {"DEGRADED", "UNAVAILABLE"} and identifier:
                desired.append(
                    BackupAlert(
                        identifier=build_backup_id(suffix=f"{identifier}-degraded"),
                        code=f"{identifier.replace('-', '_')}_degraded",
                        level="WARNING" if state == "DEGRADED" else "CRITICAL",
                        title=f"Destination {identifier} dégradée",
                        message=f"La destination {identifier} signale un état {state.lower()}.",
                        category="destination",
                        target=identifier,
                        details=provider,
                    )
                )

        failed_jobs = [job for job in jobs if str(job.get("state")) == "FAILED"]
        if failed_jobs:
            latest_failed = failed_jobs[0]
            desired.append(
                BackupAlert(
                    identifier=build_backup_id(suffix="backup-failed"),
                    code="backup_failed",
                    level="CRITICAL",
                    title="Sauvegarde échouée",
                    message=f"La dernière sauvegarde échouée est {latest_failed.get('backup_id')}.",
                    category="job",
                    target=str(latest_failed.get("kind") or ""),
                    details=latest_failed,
                )
            )

        running_jobs = [job for job in jobs if str(job.get("state")) == "RUNNING"]
        if len(running_jobs) > 1:
            desired.append(
                BackupAlert(
                    identifier=build_backup_id(suffix="concurrency-detected"),
                    code="concurrency_detected",
                    level="WARNING",
                    title="Concurrence détectée",
                    message="Plusieurs sauvegardes sont en cours simultanément.",
                    category="job",
                    details={"running_jobs": running_jobs},
                )
            )

        if any(not bool(artifact.checksum_valid) for artifact in self.repository.list_backup_artifacts(limit=200)):
            desired.append(
                BackupAlert(
                    identifier=build_backup_id(suffix="checksum-invalid"),
                    code="checksum_invalid",
                    level="CRITICAL",
                    title="Checksum invalide",
                    message="Un artefact de sauvegarde a échoué à la vérification d'intégrité.",
                    category="artifact",
                )
            )

        if restores and any(str(item.get("state")) == "FAILED" for item in restores):
            desired.append(
                BackupAlert(
                    identifier=build_backup_id(suffix="restore-test-failed"),
                    code="restore_test_failed",
                    level="CRITICAL",
                    title="Test de restauration échoué",
                    message="Une restauration récente a échoué.",
                    category="restore",
                )
            )

        if metrics.last_backup_age_seconds > 0 and metrics.last_backup_age_seconds > self.configuration.retention_google_drive_days * 24 * 3600:
            desired.append(
                BackupAlert(
                    identifier=build_backup_id(suffix="backup-too-old"),
                    code="backup_too_old",
                    level="WARNING",
                    title="Sauvegarde trop ancienne",
                    message="La dernière sauvegarde validée dépasse la fenêtre de rétention.",
                    category="policy",
                    details={"last_backup_age_seconds": metrics.last_backup_age_seconds},
                )
            )

        quota_breaches = [
            provider
            for provider in providers
            if int(provider.get("quota_bytes") or 0) > 0
            and int(provider.get("used_bytes") or 0) >= int(provider.get("quota_bytes") or 0)
        ]
        if quota_breaches:
            desired.append(
                BackupAlert(
                    identifier=build_backup_id(suffix="quota-drive-reached"),
                    code="quota_drive_reached",
                    level="CRITICAL",
                    title="Quota Drive atteint",
                    message="Une destination de sauvegarde a atteint sa limite de quota.",
                    category="destination",
                    details={"destinations": quota_breaches},
                )
            )

        postgres_failures = [
            job
            for job in jobs
            if str(job.get("state")) == "FAILED" and "postgres" in str(job.get("kind") or "").lower()
        ]
        if postgres_failures:
            desired.append(
                BackupAlert(
                    identifier=build_backup_id(suffix="postgres-error"),
                    code="postgres_error",
                    level="CRITICAL",
                    title="Erreur PostgreSQL",
                    message="Une erreur PostgreSQL a été observée durant la chaîne de sauvegarde.",
                    category="database",
                    details=postgres_failures[0],
                )
            )

        persisted: list[BackupAlert] = []
        for alert in desired:
            persisted.append(self.repository.save_backup_alert(alert))
        return persisted or self.active_alerts(limit=50)


class BackupMetricsService:
    def __init__(self, repository: LawimRepository, configuration: BackupConfiguration) -> None:
        self.repository = repository
        self.configuration = configuration

    def snapshot(
        self,
        *,
        providers: list[dict[str, Any]] | None = None,
        alerts: list[BackupAlert] | None = None,
    ) -> BackupMetrics:
        jobs = self.repository.list_backup_jobs(limit=500)
        restores = self.repository.list_restore_jobs(limit=500)
        artifacts = self.repository.list_backup_artifacts(limit=500)
        alerts_rows = alerts or self.repository.list_backup_alerts(limit=500)

        completed = [job for job in jobs if job.state == "COMPLETED"]
        failed = [job for job in jobs if job.state == "FAILED"]
        durations = [job.duration_seconds for job in jobs if job.duration_seconds is not None]
        restore_durations = [job.duration_seconds for job in restores if job.duration_seconds is not None]
        artifact_sizes = [artifact.size_bytes for artifact in artifacts if artifact.size_bytes > 0]
        bytes_stored = sum(artifact_sizes)
        successful_jobs = len(completed)
        total_jobs = len(jobs)
        checksum_validations = sum(1 for artifact in artifacts if artifact.checksum_valid)
        checksum_failures = sum(1 for artifact in artifacts if not artifact.checksum_valid)
        last_success = next((job for job in jobs if job.state == "COMPLETED" and job.finished_at), None)
        last_failed = next((job for job in jobs if job.state == "FAILED" and job.finished_at), None)
        now = datetime.now(timezone.utc)
        last_backup_age_seconds = 0.0
        if last_success and last_success.finished_at:
            parsed = _parse_datetime(last_success.finished_at)
            if parsed is not None:
                last_backup_age_seconds = max(0.0, (now - parsed.astimezone(timezone.utc)).total_seconds())
        provider_free = 0
        provider_used = 0
        if providers:
            for provider in providers:
                if bool(provider.get("available", True)):
                    provider_free += int(provider.get("free_space_bytes") or 0)
                    provider_used += int(provider.get("used_bytes") or 0)
        storage_usage_percent = 0.0
        if provider_free + provider_used > 0:
            storage_usage_percent = round((provider_used / (provider_free + provider_used)) * 100.0, 2)
        average_size_bytes = (bytes_stored / len(artifact_sizes)) if artifact_sizes else 0.0
        average_duration = (sum(duration for duration in durations if duration is not None) / len(durations)) if durations else 0.0
        max_duration = max((duration for duration in durations if duration is not None), default=0.0)
        upload_time_seconds = average_duration if completed else 0.0
        restore_time_seconds = (sum(duration for duration in restore_durations if duration is not None) / len(restore_durations)) if restore_durations else 0.0
        availability_percent = round((successful_jobs / total_jobs) * 100.0, 2) if total_jobs else 100.0
        rpo_seconds = last_backup_age_seconds
        rto_seconds = restore_time_seconds
        metrics = BackupMetrics(
            total_jobs=total_jobs,
            successful_jobs=successful_jobs,
            failed_jobs=len(failed),
            mean_duration_seconds=round(average_duration, 3),
            max_duration_seconds=round(max_duration, 3),
            bytes_stored=bytes_stored,
            storage_usage_percent=round(storage_usage_percent, 2),
            last_success_at=last_success.finished_at if last_success else None,
            last_failed_at=last_failed.finished_at if last_failed else None,
            average_size_bytes=round(average_size_bytes, 2),
            total_size_bytes=bytes_stored,
            transferred_bytes=bytes_stored,
            upload_time_seconds=round(upload_time_seconds, 3),
            restore_time_seconds=round(restore_time_seconds, 3),
            alert_count=len([alert for alert in alerts_rows if getattr(alert, "status", "NEW") not in {"RESOLVED", "ACKNOWLEDGED"}]),
            checksum_validations=checksum_validations,
            checksum_failures=checksum_failures,
            availability_percent=availability_percent,
            rpo_seconds=round(rpo_seconds, 3),
            rto_seconds=round(rto_seconds, 3),
            last_backup_age_seconds=round(last_backup_age_seconds, 3),
        )
        return self.repository.upsert_backup_metrics(metrics)


class BackupHealthService:
    def __init__(self, repository: LawimRepository, configuration: BackupConfiguration, providers: dict[str, StorageProvider]) -> None:
        self.repository = repository
        self.configuration = configuration
        self.providers = providers

    def systemd_snapshot(self) -> dict[str, Any]:
        service_fields = _systemctl_show(
            self.configuration.systemd_service,
            (
                "ActiveState",
                "SubState",
                "Result",
                "ExecMainStatus",
                "ExecMainCode",
                "ExecMainStartTimestamp",
                "ExecMainExitTimestamp",
                "ExecMainPID",
                "ActiveEnterTimestamp",
                "InactiveExitTimestamp",
            ),
        )
        timer_fields = _systemctl_show(
            self.configuration.systemd_timer,
            (
                "ActiveState",
                "SubState",
                "Result",
                "NextElapseUSecRealtime",
                "LastTriggerUSecRealtime",
                "Unit",
            ),
        )
        last_launch_at = _systemd_time_string(service_fields.get("ExecMainStartTimestamp") or service_fields.get("ActiveEnterTimestamp"))
        next_execution_at = _systemd_time_string(timer_fields.get("NextElapseUSecRealtime"))
        last_return = service_fields.get("ExecMainStatus") or service_fields.get("Result") or "unknown"
        state = service_fields.get("ActiveState") or "unknown"
        timer_state = timer_fields.get("ActiveState") or "unknown"
        duration_seconds: float | None = None
        job = next((item for item in self.repository.list_backup_jobs(limit=50) if item.state == "COMPLETED" and item.duration_seconds is not None), None)
        if job and job.duration_seconds is not None:
            duration_seconds = float(job.duration_seconds)
        else:
            start = _systemd_time_string(service_fields.get("ExecMainStartTimestamp"))
            end = _systemd_time_string(service_fields.get("ExecMainExitTimestamp"))
            if start and end:
                duration_seconds = _seconds_between(start, end)
        if duration_seconds is None:
            duration_seconds = 0.0
        if not next_execution_at:
            next_schedule = self._fallback_next_schedule()
            next_execution_at = next_schedule.next_run_at if next_schedule else None
        if not last_launch_at:
            last_launch_at = next((item.started_at for item in self.repository.list_backup_jobs(limit=50) if item.started_at), None)
        if not last_return:
            last_return = "unknown"
        return {
            "service": {
                "unit": self.configuration.systemd_service,
                "active_state": state,
                "sub_state": service_fields.get("SubState") or "unknown",
                "result": service_fields.get("Result") or "unknown",
                "exec_main_status": service_fields.get("ExecMainStatus") or "",
                "exec_main_code": service_fields.get("ExecMainCode") or "",
                "exec_main_pid": service_fields.get("ExecMainPID") or "",
                "last_launch_at": last_launch_at,
                "last_exit_at": _systemd_time_string(service_fields.get("ExecMainExitTimestamp")),
            },
            "timer": {
                "unit": self.configuration.systemd_timer,
                "active_state": timer_state,
                "sub_state": timer_fields.get("SubState") or "unknown",
                "result": timer_fields.get("Result") or "unknown",
                "next_execution_at": next_execution_at,
                "last_trigger_at": _systemd_time_string(timer_fields.get("LastTriggerUSecRealtime")),
            },
            "last_launch_at": last_launch_at,
            "next_execution_at": next_execution_at,
            "last_return": last_return,
            "duration_seconds": round(float(duration_seconds), 3),
            "state": state,
            "timer_state": timer_state,
        }

    def _fallback_next_schedule(self) -> BackupSchedule | None:
        schedules = BackupScheduler(self.repository, self.configuration).schedules()
        return next((schedule for schedule in schedules if schedule.enabled), None)

    def snapshot(self) -> dict[str, Any]:
        systemd = self.systemd_snapshot()
        providers = self.providers
        provider_health = [provider.health() for provider in providers.values()]
        unavailable = [item for item in provider_health if not item.get("available")]
        degraded = [item for item in provider_health if str(item.get("state")).upper() in {"DEGRADED", "UNAVAILABLE"}]
        last_success = next((job for job in self.repository.list_backup_jobs(limit=50) if job.state == "COMPLETED"), None)
        last_failed = next((job for job in self.repository.list_backup_jobs(limit=50) if job.state == "FAILED"), None)
        if not last_success and self.repository.list_backup_jobs(limit=1):
            global_status = "WATCH"
        elif unavailable:
            global_status = "CRITICAL" if any(item.get("identifier") == "local" for item in unavailable) else "DEGRADED"
        elif degraded:
            global_status = "DEGRADED"
        elif last_failed:
            global_status = "WATCH"
        elif systemd["state"] in {"failed", "inactive"} and not last_success:
            global_status = "CRITICAL"
        else:
            global_status = "PROTECTED"
        return {
            "systemd": systemd,
            "providers": provider_health,
            "global_status": global_status,
            "last_success_at": last_success.finished_at if last_success else None,
            "last_failed_at": last_failed.finished_at if last_failed else None,
            "next_execution_at": systemd["next_execution_at"],
            "last_launch_at": systemd["last_launch_at"],
            "duration_seconds": systemd["duration_seconds"],
            "last_return": systemd["last_return"],
            "service_state": systemd["state"],
            "timer_state": systemd["timer_state"],
        }


class BackupScheduler:
    def __init__(self, repository: LawimRepository, configuration: BackupConfiguration) -> None:
        self.repository = repository
        self.configuration = configuration

    def _last_run_for_source(self, source: str) -> str | None:
        jobs = self.repository.list_backup_jobs(limit=200)
        for job in jobs:
            if job.destination == source or job.provider == source or job.kind == source:
                return job.finished_at or job.started_at or job.created_at
        return None

    def schedules(self) -> list[BackupSchedule]:
        items: list[BackupSchedule] = []
        for schedule in self.configuration.schedules():
            next_run = _next_occurrence_for_calendar(schedule.calendar, timezone_name=schedule.timezone)
            items.append(
                BackupSchedule(
                    **{
                        **schedule.as_dict(),
                        "next_run_at": next_run,
                        "last_run_at": self._last_run_for_source(schedule.source),
                    }
                )
            )
        return items

    def next_backup(self) -> BackupSchedule | None:
        schedules = [schedule for schedule in self.schedules() if schedule.enabled]
        if not schedules:
            return None
        def _sort_key(item: BackupSchedule) -> tuple[int, str]:
            return (0 if item.next_run_at else 1, item.next_run_at or "9999-12-31T23:59:59+00:00")
        return sorted(schedules, key=_sort_key)[0]

    def snapshot(self, *, health: dict[str, Any] | None = None) -> dict[str, Any]:
        latest = self.next_backup()
        return {
            "schedules": [schedule.as_dict() for schedule in self.schedules()],
            "next_backup": latest.as_dict() if latest else None,
            "health_hint": health or {},
        }


class BackupJobRunner:
    def __init__(
        self,
        repository: LawimRepository,
        configuration: BackupConfiguration,
        providers: dict[str, StorageProvider],
        event_bus: BackupEventBus,
        alert_service: BackupAlertService,
        metrics_service: BackupMetricsService,
        health_service: BackupHealthService,
    ) -> None:
        self.repository = repository
        self.configuration = configuration
        self.providers = providers
        self.event_bus = event_bus
        self.alert_service = alert_service
        self.metrics_service = metrics_service
        self.health_service = health_service

    def provider_statuses(self) -> list[dict[str, Any]]:
        destinations = {item.identifier: item for item in self.repository.list_backup_destinations(limit=50)}
        payload: list[dict[str, Any]] = []
        for provider in self.providers.values():
            destination = destinations.get(provider.identifier)
            if destination is None:
                payload.append(provider.health())
                continue
            merged = destination.as_dict()
            merged.update(provider.health())
            payload.append(merged)
        return payload

    def _provider_for(self, provider_name: str | None, destination: str | None = None) -> StorageProvider | None:
        names = [name for name in (provider_name, destination) if name]
        for name in names:
            normalized = name.replace("-", "_")
            if normalized in self.providers:
                return self.providers[normalized]
            if name in self.providers:
                return self.providers[name]
        return self.providers.get("local")

    def _write_manifest(self, *, backup_id: str, kind: str, destination: str, trigger: str, metadata: dict[str, Any] | None = None) -> tuple[Path, dict[str, Any]]:
        root = self.configuration.backup_root / backup_id
        root.mkdir(parents=True, exist_ok=True)
        manifest_path = root / "manifest.json"
        payload = {
            "backup_id": backup_id,
            "kind": kind,
            "destination": destination,
            "trigger": trigger,
            "created_at": utc_now(),
            "lawim_version": self.configuration.lawim_version or LAWIM_VERSION,
            "git_commit": self.configuration.git_commit,
            "configuration": self.configuration.policy(),
            "metadata": metadata or {},
            "systemd": self.health_service.systemd_snapshot(),
        }
        manifest_path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
        return manifest_path, payload

    def run(
        self,
        *,
        kind: str,
        destination: str = "local",
        provider_name: str | None = None,
        trigger: str = "manual",
        metadata: dict[str, Any] | None = None,
        backup_id: str | None = None,
        attempt: int = 1,
    ) -> BackupJob:
        provider = self._provider_for(provider_name, destination)
        job = BackupJob(
            identifier=build_backup_id(suffix=f"job-{kind}-{trigger}"),
            backup_id=backup_id or build_backup_id(suffix=f"{kind}-{destination}"),
            kind=kind,
            state="RUNNING",
            destination=destination,
            provider=provider.identifier if provider else destination,
            trigger=trigger,
            git_commit=self.configuration.git_commit,
            version=self.configuration.lawim_version or LAWIM_VERSION,
            started_at=utc_now(),
            attempt=max(1, attempt),
            source="backup",
        )
        self.repository.save_backup_job(job)
        self.event_bus.record(kind="backup.started", level="INFO", message=f"Backup {job.backup_id} started", backup_id=job.backup_id, job_id=job.identifier)
        if provider is None or not provider.is_available():
            finished = replace(
                job,
                state="FAILED",
                finished_at=utc_now(),
                duration_seconds=_seconds_between(job.started_at, utc_now()) or 0.0,
                validation_result="provider_unavailable",
                notes="Provider unavailable",
            )
            saved = self.repository.save_backup_job(finished)
            self.alert_service.raise_alert(
                code=f"{(provider.identifier if provider else destination).replace('-', '_')}_unavailable",
                level="CRITICAL",
                title="Backup destination unavailable",
                message=f"Provider {provider.identifier if provider else destination} is unavailable.",
                target=provider.identifier if provider else destination,
                category="destination",
            )
            self.event_bus.record(kind="backup.failed", level="CRITICAL", message=f"Backup {job.backup_id} failed", backup_id=job.backup_id, job_id=saved.identifier)
            self.metrics_service.snapshot(providers=self.provider_statuses())
            return saved
        manifest_path, manifest_payload = self._write_manifest(
            backup_id=job.backup_id,
            kind=kind,
            destination=destination,
            trigger=trigger,
            metadata=metadata,
        )
        sha256 = _sha256(manifest_path)
        artifact = BackupArtifact(
            identifier=build_backup_id(suffix=f"artifact-{kind}-{destination}"),
            backup_id=job.backup_id,
            kind=kind,
            filename=manifest_path.name,
            path=str(manifest_path),
            size_bytes=manifest_path.stat().st_size,
            sha256=sha256,
            encrypted=False,
            checksum_algorithm="sha256",
            verified_at=utc_now(),
            version=self.configuration.lawim_version or LAWIM_VERSION,
            git_commit=self.configuration.git_commit,
            job_id=job.identifier,
            destination_id=destination,
            provider=provider.identifier,
            storage_uri=str(manifest_path),
            checksum_valid=True,
            uploaded_at=utc_now(),
            metadata=manifest_payload,
        )
        saved_artifact = self.repository.save_backup_artifact(artifact)
        provider.store(saved_artifact)
        provider.available = True
        provider.state = "AVAILABLE"
        finished = replace(
            job,
            state="COMPLETED",
            finished_at=utc_now(),
            duration_seconds=_seconds_between(job.started_at, utc_now()) or 0.0,
            checksum=sha256,
            validation_result="verified" if provider.verify(saved_artifact.identifier) else "checksum_invalid",
            artifact_count=1,
        )
        saved = self.repository.save_backup_job(finished)
        self.event_bus.record(kind="backup.completed", level="INFO", message=f"Backup {job.backup_id} completed", backup_id=job.backup_id, job_id=saved.identifier)
        self.metrics_service.snapshot(providers=self.provider_statuses())
        return saved

    def test(self, *, kind: str = "full", destination: str = "local", metadata: dict[str, Any] | None = None) -> BackupJob:
        return self.run(kind=f"test-{kind}", destination=destination, provider_name=destination, trigger="test", metadata=metadata)

    def retry(self, *, identifier: str | None = None) -> BackupJob:
        source_job = None
        if identifier:
            source_job = self.repository.get_backup_job(identifier)
        if source_job is None:
            source_job = next((job for job in self.repository.list_backup_jobs(limit=200) if job.state == "FAILED"), None)
        if source_job is None:
            raise KeyError("No failed backup job available for retry")
        return self.run(
            kind=source_job.kind,
            destination=source_job.destination or "local",
            provider_name=source_job.provider or source_job.destination or "local",
            trigger="retry",
            metadata={"retry_of": source_job.identifier},
            backup_id=build_backup_id(suffix=f"retry-{source_job.backup_id}"),
            attempt=source_job.attempt + 1,
        )

    def provider_test(self, provider_identifier: str) -> dict[str, Any]:
        provider = self._provider_for(provider_identifier, provider_identifier)
        if provider is None:
            raise KeyError(f"Unknown provider: {provider_identifier}")
        health = provider.health()
        if not provider.is_available():
            self.alert_service.raise_alert(
                code=f"{provider.identifier.replace('-', '_')}_unavailable",
                level="CRITICAL",
                title=f"{provider.name} unavailable",
                message=f"Provider {provider.name} is unavailable.",
                target=provider.identifier,
                category="destination",
            )
        self.event_bus.record(
            kind="backup.provider.test",
            level="INFO",
            message=f"Provider test for {provider.identifier}",
            details=health,
        )
        self.metrics_service.snapshot(providers=self.provider_statuses())
        return health


class BackupRestoreService:
    def __init__(
        self,
        repository: LawimRepository,
        configuration: BackupConfiguration,
        event_bus: BackupEventBus,
        alert_service: BackupAlertService,
        metrics_service: BackupMetricsService,
    ) -> None:
        self.repository = repository
        self.configuration = configuration
        self.event_bus = event_bus
        self.alert_service = alert_service
        self.metrics_service = metrics_service

    def restore(
        self,
        *,
        backup_id: str,
        kind: str,
        target_environment: str = "isolated",
        database_restored: bool = False,
        media_restored: bool = False,
        notes: str = "",
        checksum_verified: bool = True,
        decrypted: bool = True,
        report: dict[str, Any] | None = None,
        success: bool = True,
    ) -> RestoreResultBundle:
        restore_job = RestoreJob(
            identifier=build_backup_id(suffix=f"restore-{kind}-{target_environment}"),
            backup_id=backup_id,
            kind=kind,
            state="RUNNING",
            target_environment=target_environment,
            started_at=utc_now(),
            checksum_verified=checksum_verified,
            decrypted=decrypted,
            validation_result="running",
            report=report or {},
        )
        self.repository.save_restore_job(restore_job)
        completed_at = utc_now()
        result = RestoreResult(
            identifier=build_backup_id(suffix=f"restore-result-{kind}-{target_environment}"),
            restore_job_id=restore_job.identifier,
            backup_id=backup_id,
            kind=kind,
            state="COMPLETED" if success else "FAILED",
            success=success,
            created_at=restore_job.created_at,
            completed_at=completed_at,
            duration_seconds=_seconds_between(restore_job.started_at, completed_at) or 0.0,
            checksum_verified=checksum_verified,
            media_restored=media_restored,
            database_restored=database_restored,
            report=report or {},
            notes=notes,
        )
        restore_job = replace(
            restore_job,
            state="COMPLETED" if success else "FAILED",
            finished_at=completed_at,
            duration_seconds=result.duration_seconds,
            validation_result="verified" if success else "failed",
            report=report or {},
        )
        saved_job = self.repository.save_restore_job(restore_job)
        saved_result = self.repository.save_restore_result(result)
        if success:
            self.event_bus.record(kind="backup.restore.completed", level="INFO", message=f"Restore {backup_id} completed", backup_id=backup_id, restore_id=saved_job.identifier)
        else:
            self.event_bus.record(kind="backup.restore.failed", level="CRITICAL", message=f"Restore {backup_id} failed", backup_id=backup_id, restore_id=saved_job.identifier)
            self.alert_service.raise_alert(
                code="restore_test_failed",
                level="CRITICAL",
                title="Restore failed",
                message=f"Restore {backup_id} failed.",
                target=kind,
                category="restore",
                details=result.as_dict(),
            )
        self.metrics_service.snapshot(providers=[])
        return RestoreResultBundle(restore_job=saved_job, restore_result=saved_result)

    def test_postgresql(self, *, backup_id: str) -> RestoreResultBundle:
        return self.restore(
            backup_id=backup_id,
            kind="postgresql",
            target_environment="isolated",
            database_restored=True,
            media_restored=False,
            notes="PostgreSQL test restore",
        )

    def test_media(self, *, backup_id: str) -> RestoreResultBundle:
        return self.restore(
            backup_id=backup_id,
            kind="media",
            target_environment="isolated",
            database_restored=False,
            media_restored=True,
            notes="Media test restore",
        )

    def test_complete(self, *, backup_id: str) -> RestoreResultBundle:
        return self.restore(
            backup_id=backup_id,
            kind="full",
            target_environment="isolated",
            database_restored=True,
            media_restored=True,
            notes="Full test restore",
        )


class BackupOrchestrator:
    def __init__(
        self,
        repository: LawimRepository | None = None,
        config: AppConfig | None = None,
        settings: BackupConfiguration | None = None,
    ) -> None:
        self._tempdir: tempfile.TemporaryDirectory[str] | None = None
        if repository is None:
            self._tempdir = tempfile.TemporaryDirectory(prefix="lawim-backup-db-")
            temp_db = Path(self._tempdir.name) / "backup.sqlite3"
            repository = LawimRepository(temp_db)
            repository.initialize(seed_demo_data=False)
        self.repository = repository
        self.config = config
        self._configuration = settings or BackupConfiguration.from_env(
            workspace_root=config.db_path.parent if config is not None else None,
            app_env=config.app_env if config is not None else None,
        )
        self.git_commit = _git_commit()
        self.lawim_version = LAWIM_VERSION
        self._configuration = replace(
            self._configuration,
            lawim_version=self.lawim_version,
            git_commit=self.git_commit,
            last_checked_at=utc_now(),
        )
        self.settings = self._configuration
        self.providers: dict[str, StorageProvider] = self._build_providers()
        self.event_bus = BackupEventBus(self.repository)
        self.alert_service = BackupAlertService(self.repository, self.event_bus, self._configuration)
        self.metrics_service = BackupMetricsService(self.repository, self._configuration)
        self.health_service = BackupHealthService(self.repository, self._configuration, self.providers)
        self.scheduler = BackupScheduler(self.repository, self._configuration)
        self.job_runner = BackupJobRunner(
            self.repository,
            self._configuration,
            self.providers,
            self.event_bus,
            self.alert_service,
            self.metrics_service,
            self.health_service,
        )
        self.restore_service = BackupRestoreService(
            self.repository,
            self._configuration,
            self.event_bus,
            self.alert_service,
            self.metrics_service,
        )
        self.bootstrap()

    def _build_providers(self) -> dict[str, StorageProvider]:
        backup_root = self._configuration.backup_root
        state_root = self._configuration.state_root
        providers: dict[str, StorageProvider] = {
            "local": LocalDiskProvider(
                identifier="local",
                name="Local disk",
                kind="local_disk",
                path=backup_root / "local",
                mount_point=str(backup_root),
                state="AVAILABLE",
                available=True,
            ),
            "google_drive": GoogleDriveProvider(
                identifier="google-drive",
                name="Google Drive",
                kind="google_drive",
                path=state_root / "google-drive",
                mount_point=str(state_root),
                state="AVAILABLE",
                available=True,
            ),
            "external_disk": ExternalDiskProvider(
                identifier="external-disk",
                name="External disk",
                kind="external_disk",
                path=state_root / "external-disk",
                mount_point=str(state_root),
                state="UNKNOWN",
                available=False,
            ),
        }
        for provider in providers.values():
            provider.initialize()
        return providers

    def bootstrap(self) -> None:
        self.repository.seed_backup_catalog(self._configuration)
        self.refresh_state()

    def refresh_state(self) -> None:
        providers = self.provider_statuses()
        jobs = self.list(limit=200)
        restores = self.restore_history(limit=200)
        health = self.health_service.snapshot()
        alerts = self.alert_service.sync_from_state(
            health=health,
            providers=providers,
            jobs=jobs,
            restores=restores,
            metrics=self.metrics_service.snapshot(providers=providers),
        )
        self.metrics_service.snapshot(providers=providers, alerts=alerts)

    def _merge_destination(self, destination: BackupDestination, provider: StorageProvider | None) -> dict[str, Any]:
        payload = destination.as_dict()
        if provider is not None:
            payload.update(provider.health())
        payload["provider"] = provider.health() if provider is not None else None
        return payload

    def provider_statuses(self) -> list[dict[str, Any]]:
        destinations = {destination.identifier: destination for destination in self.repository.list_backup_destinations(limit=50)}
        payload: list[dict[str, Any]] = []
        for key in ("local", "google_drive", "external_disk"):
            provider = self.providers.get(key)
            destination = destinations.get(provider.identifier if provider else key.replace("_", "-"))
            if destination is None and provider is not None:
                destination = BackupDestination(
                    identifier=provider.identifier,
                    name=provider.name,
                    kind=provider.kind,
                    path=str(provider.path),
                    mount_point=provider.mount_point,
                    state="UNKNOWN",
                    available_bytes=provider.get_free_space(),
                )
            if destination is not None:
                payload.append(self._merge_destination(destination, provider))
            elif provider is not None:
                payload.append(provider.health())
        return payload

    def list(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [job.as_dict() for job in self.repository.list_backup_jobs(limit=limit)]

    def jobs(self, *, limit: int = 50) -> list[dict[str, object]]:
        return self.list(limit=limit)

    def history(self, *, limit: int = 50) -> list[dict[str, object]]:
        return self.list(limit=limit)

    def schedules(self) -> list[dict[str, object]]:
        return [schedule.as_dict() for schedule in self.scheduler.schedules()]

    def destinations(self, *, limit: int = 50) -> list[dict[str, object]]:
        destinations = self.repository.list_backup_destinations(limit=limit)
        provider_status = {provider["identifier"]: provider for provider in self.provider_statuses()}
        payload: list[dict[str, object]] = []
        for destination in destinations:
            item = destination.as_dict()
            provider = provider_status.get(destination.identifier)
            if provider:
                item.update(provider)
            payload.append(item)
        return payload

    def alerts(self, *, limit: int = 50) -> list[dict[str, object]]:
        self.refresh_state()
        return [alert.as_dict() for alert in self.alert_service.active_alerts(limit=limit)]

    def events(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [event.as_dict() for event in self.event_bus.list(limit=limit)]

    def restore_history(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [job.as_dict() for job in self.repository.list_restore_jobs(limit=limit)]

    def restore_results(self, *, limit: int = 50) -> list[dict[str, object]]:
        return [result.as_dict() for result in self.repository.list_restore_results(limit=limit)]

    def configuration(self) -> dict[str, object]:
        payload = self._configuration.as_dict()
        payload["policy"] = self._configuration.policy()
        payload["schedules"] = [schedule.as_dict() for schedule in self.scheduler.schedules()]
        payload["systemd"] = {
            "service": self._configuration.systemd_service,
            "timer": self._configuration.systemd_timer,
        }
        payload["version"] = {"lawim": self.lawim_version, "git_commit": self.git_commit}
        return payload

    def metrics(self) -> dict[str, object]:
        return self.metrics_service.snapshot(providers=self.provider_statuses()).as_dict()

    def last_backup(self) -> dict[str, object] | None:
        for job in self.repository.list_backup_jobs(limit=100):
            if job.state == "COMPLETED":
                return job.as_dict()
        jobs = self.repository.list_backup_jobs(limit=1)
        return jobs[0].as_dict() if jobs else None

    def last_restore(self) -> dict[str, object] | None:
        restores = self.repository.list_restore_jobs(limit=1)
        return restores[0].as_dict() if restores else None

    def next_backup(self) -> dict[str, object] | None:
        schedule = self.scheduler.next_backup()
        return schedule.as_dict() if schedule else None

    def status(self) -> dict[str, object]:
        health = self.health_service.snapshot()
        providers = self.provider_statuses()
        jobs = self.list(limit=200)
        restores = self.restore_history(limit=200)
        alerts = self.alert_service.sync_from_state(
            health=health,
            providers=providers,
            jobs=jobs,
            restores=restores,
            metrics=self.metrics_service.snapshot(providers=providers),
        )
        metrics = self.metrics_service.snapshot(providers=providers, alerts=alerts).as_dict()
        last_success = next((job for job in jobs if job.get("state") == "COMPLETED"), None)
        last_failed = next((job for job in jobs if job.get("state") == "FAILED"), None)
        if any(alert.level == "CRITICAL" for alert in alerts):
            global_status = "CRITICAL"
        elif any(not provider.get("available", True) for provider in providers):
            global_status = "DEGRADED"
        elif health["service_state"] in {"failed", "inactive"} and last_success is None:
            global_status = "CRITICAL"
        elif last_success is None:
            global_status = "WATCH"
        elif any(job.get("state") == "FAILED" for job in jobs):
            global_status = "WATCH"
        else:
            global_status = "PROTECTED"
        return {
            "global_status": global_status,
            "policy": self._configuration.policy(),
            "configuration": self.configuration(),
            "destinations": self.destinations(),
            "providers": providers,
            "alerts": [alert.as_dict() for alert in alerts],
            "events": self.events(limit=20),
            "history": jobs,
            "jobs": jobs,
            "restores": restores,
            "last_backup": last_success,
            "last_failed_backup": last_failed,
            "next_backup": self.next_backup(),
            "last_restore": self.last_restore(),
            "metrics": metrics,
            "systemd": health["systemd"],
            "version": {"lawim": self.lawim_version, "git_commit": self.git_commit},
            "counts": {
                "jobs": len(jobs),
                "alerts": len(alerts),
                "restores": len(restores),
                "providers": len(providers),
                "destinations": len(self.destinations()),
            },
        }

    def run(
        self,
        *,
        kind: str,
        destination: str = "local",
        provider_name: str | None = None,
        trigger: str = "manual",
        metadata: dict[str, Any] | None = None,
        backup_id: str | None = None,
        attempt: int = 1,
    ) -> dict[str, object]:
        job = self.job_runner.run(
            kind=kind,
            destination=destination,
            provider_name=provider_name,
            trigger=trigger,
            metadata=metadata,
            backup_id=backup_id,
            attempt=attempt,
        )
        self.refresh_state()
        return job.as_dict()

    def test(self, *, kind: str = "full", destination: str = "local", metadata: dict[str, Any] | None = None) -> dict[str, object]:
        return self.run(kind=f"test-{kind}", destination=destination, provider_name=destination, trigger="test", metadata=metadata)

    def retry(self, *, identifier: str | None = None) -> dict[str, object]:
        job = self.job_runner.retry(identifier=identifier)
        self.refresh_state()
        return job.as_dict()

    def restore(
        self,
        *,
        backup_id: str,
        kind: str,
        target_environment: str = "isolated",
        database_restored: bool = False,
        media_restored: bool = False,
        notes: str = "",
        success: bool = True,
    ) -> dict[str, object]:
        bundle = self.restore_service.restore(
            backup_id=backup_id,
            kind=kind,
            target_environment=target_environment,
            database_restored=database_restored,
            media_restored=media_restored,
            notes=notes,
            success=success,
        )
        self.refresh_state()
        return {
            "restore_job": bundle.restore_job.as_dict(),
            "restore_result": bundle.restore_result.as_dict(),
        }

    def provider_test(self, provider_identifier: str) -> dict[str, Any]:
        result = self.job_runner.provider_test(provider_identifier)
        self.refresh_state()
        return result

    def patch_configuration(self, **changes: object) -> dict[str, object]:
        current = self._configuration.as_dict()
        current.update(changes)
        updated = BackupConfiguration.from_dict(current)
        self._configuration = replace(
            updated,
            lawim_version=self.lawim_version,
            git_commit=self.git_commit,
            last_checked_at=utc_now(),
        )
        self.settings = self._configuration
        self.repository.upsert_backup_configuration(self._configuration)
        self.providers = self._build_providers()
        self.health_service.providers = self.providers
        self.health_service.configuration = self._configuration
        self.scheduler = BackupScheduler(self.repository, self._configuration)
        self.job_runner.providers = self.providers
        self.job_runner.configuration = self._configuration
        self.job_runner.health_service = self.health_service
        self.alert_service.configuration = self._configuration
        self.alert_service.event_bus = self.event_bus
        self.metrics_service.configuration = self._configuration
        self.restore_service.configuration = self._configuration
        self.restore_service.event_bus = self.event_bus
        self.restore_service.alert_service = self.alert_service
        self.restore_service.metrics_service = self.metrics_service
        self.refresh_state()
        return self.configuration()

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
        job = BackupJob(
            identifier=build_backup_id(suffix=f"job-{kind}"),
            backup_id=build_backup_id(suffix=f"backup-{kind}"),
            kind=kind,
            state=state,  # type: ignore[arg-type]
            destination=destination,
            size_bytes=size_bytes,
            trigger=trigger,
            git_commit=git_commit or self.git_commit,
            version=version or self.lawim_version,
            duration_seconds=duration_seconds,
        )
        saved = self.repository.save_backup_job(job)
        self.metrics_service.snapshot(providers=self.provider_statuses())
        return saved

    def record_restore_job(
        self,
        *,
        kind: str,
        state: str = "PENDING",
        target_environment: str = "isolated",
    ) -> RestoreJob:
        job = RestoreJob(
            identifier=build_backup_id(suffix=f"restore-{kind}"),
            backup_id=build_backup_id(suffix=f"restore-src-{kind}"),
            kind=kind,
            state=state,  # type: ignore[arg-type]
            target_environment=target_environment,
        )
        saved = self.repository.save_restore_job(job)
        self.metrics_service.snapshot(providers=self.provider_statuses())
        return saved

    def record_alert(
        self,
        *,
        level: AlertLevel,
        title: str,
        message: str,
        status: str = "NEW",
        code: str = "",
        category: str = "backup",
        target: str = "",
        details: dict[str, Any] | None = None,
    ) -> BackupAlert:
        alert = BackupAlert(
            identifier=build_backup_id(suffix=f"alert-{title}"),
            level=level,
            title=title,
            message=message,
            status=status,
            code=code,
            category=category,
            target=target,
            details=details or {},
        )
        saved = self.repository.save_backup_alert(alert)
        self.metrics_service.snapshot(providers=self.provider_statuses())
        return saved

    def record_event(self, *, backup_id: str, kind: str, level: AlertLevel, message: str) -> BackupEvent:
        event = self.event_bus.record(kind=kind, level=level, message=message, backup_id=backup_id)
        return event

    def get_destination(self, identifier: str) -> dict[str, object] | None:
        destination = self.repository.get_backup_destination(identifier)
        if destination is None:
            return None
        provider = self.providers.get(identifier.replace("-", "_")) or self.providers.get(identifier)
        payload = destination.as_dict()
        if provider is not None:
            payload.update(provider.health())
        return payload

    def require_destination(self, identifier: str) -> dict[str, object]:
        destination = self.get_destination(identifier)
        if destination is None:
            raise KeyError(f"Unknown backup destination: {identifier}")
        return destination

    def touch(self) -> str:
        return utc_now()


class BackupService(BackupOrchestrator):
    pass


__all__ = [
    "BackupAlertService",
    "BackupEventBus",
    "BackupHealthService",
    "BackupJobRunner",
    "BackupMetricsService",
    "BackupOrchestrator",
    "BackupRestoreService",
    "BackupScheduler",
    "BackupService",
]
