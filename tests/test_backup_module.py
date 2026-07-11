from __future__ import annotations

from lawim_v2.backup import BackupArtifact, BackupService, BackupSettings, LocalDiskProvider
from lawim_v2.backup.models import build_backup_id


def test_build_backup_id_uses_canonical_prefix_and_suffix() -> None:
    backup_id = build_backup_id(suffix="google-drive")
    assert backup_id.startswith("LAWIM-")
    assert backup_id.endswith("-google-drive")


def test_backup_settings_expose_canonical_schedule() -> None:
    settings = BackupSettings()
    schedules = settings.schedules()
    calendars = {schedule.calendar for schedule in schedules}
    assert "TZ=Africa/Douala *-*-* 02:00:00" in calendars
    assert "TZ=Africa/Douala *-*-* 14:30:00" in calendars


def test_backup_service_reports_canonical_policy_and_paths() -> None:
    service = BackupService()
    status = service.status()
    configuration = service.configuration()
    assert status["policy"]["google_drive"]["timezone"] == "Africa/Douala"
    assert status["policy"]["google_drive"]["time"] == ["02:00", "14:30"]
    assert configuration["backup_root"] == "/var/backups/lawim"
    assert configuration["state_root"] == "/var/lib/lawim-backup"
    assert configuration["logs_root"] == "/var/log/lawim-backup"
    assert configuration["temp_root"] == "/var/tmp/lawim-backup"


def test_backup_service_exposes_destinations_history_and_events() -> None:
    service = BackupService()
    job = service.record_job(kind="google-drive", state="COMPLETED", destination="google-drive", duration_seconds=12.5)
    restore = service.record_restore_job(kind="postgresql", state="COMPLETED")
    alert = service.record_alert(level="WARNING", title="Disk space low", message="Free space below threshold")
    event = service.record_event(backup_id=job.backup_id, kind="backup.completed", level="INFO", message="Completed")

    history = service.history()
    alerts = service.alerts()
    events = service.events()
    restores = service.restore_history()

    assert any(item["identifier"] == job.identifier for item in history)
    assert any(item["identifier"] == restore.identifier for item in restores)
    assert any(item["identifier"] == alert.identifier for item in alerts)
    assert any(item["identifier"] == event.identifier for item in events)
    assert service.status()["global_status"] in {"WATCH", "PROTECTED", "DEGRADED", "CRITICAL", "UNKNOWN"}


def test_local_disk_provider_tracks_artifacts_and_health() -> None:
    provider = LocalDiskProvider(identifier="local", name="Local disk", kind="local_disk", available=True, free_space_bytes=1024)
    artifact = BackupArtifact(
        identifier="artifact-1",
        backup_id="LAWIM-20260711-020000",
        kind="postgresql",
        filename="LAWIM-20260711-020000.sql.gz.enc",
    )
    snapshot = provider.store(artifact)
    assert snapshot["provider"] == "local"
    assert provider.is_available() is True
    assert provider.verify("artifact-1") is True
    assert provider.retrieve("artifact-1") is not None
    assert provider.list()[0]["identifier"] == "artifact-1"
    assert provider.delete("artifact-1") is True
    assert provider.health()["artifact_count"] == 0
