from __future__ import annotations

from .models import BackupArtifact
from .providers import LocalDiskProvider
from .service import BackupService


def test_backup_service_exposes_target_policy() -> None:
    service = BackupService()
    status = service.status()
    assert status["policy"]["google_drive"]["timezone"] == "Africa/Douala"
    assert status["policy"]["google_drive"]["time"] == ["02:00", "14:30"]


def test_backup_service_returns_canonical_destinations() -> None:
    service = BackupService()
    destinations = service.destinations()
    identifiers = {destination["identifier"] for destination in destinations}
    assert {"local", "google-drive", "external-disk"} <= identifiers


def test_backup_service_reports_configuration_paths() -> None:
    service = BackupService()
    configuration = service.configuration()
    assert configuration["backup_root"] == "/var/backups/lawim"
    assert configuration["state_root"] == "/var/lib/lawim-backup"
    assert configuration["logs_root"] == "/var/log/lawim-backup"
    assert configuration["temp_root"] == "/var/tmp/lawim-backup"


def test_backup_service_exposes_history_and_status() -> None:
    service = BackupService()
    assert len(service.list()) >= 1
    assert service.status()["global_status"] in {"WATCH", "UNKNOWN", "PROTECTED", "DEGRADED", "CRITICAL"}


def test_local_disk_provider_tracks_artifacts() -> None:
    provider = LocalDiskProvider(identifier="local", name="Local disk", kind="local_disk", available=True, free_space_bytes=1024)
    artifact = BackupArtifact(
        identifier="artifact-1",
        backup_id="LAWIM-20260711-020000",
        kind="postgresql",
        filename="LAWIM-20260711-020000.sql.gz.enc",
    )
    snapshot = provider.store(artifact)
    assert snapshot["provider"] == "local"
    assert provider.verify("artifact-1") is True
    assert provider.health()["artifact_count"] == 1
