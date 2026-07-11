from __future__ import annotations

from importlib import import_module
from typing import Any

from .models import (
    AlertLevel,
    BackupAlert,
    BackupArtifact,
    BackupConfiguration,
    BackupDestination,
    BackupDestinationState,
    BackupEvent,
    BackupJob,
    BackupJobState,
    BackupManifest,
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
from .recovery import (
    DisasterRecoveryService,
    RecoveryBundleManifest,
    RecoveryBundleSummary,
    RecoveryReadinessScore,
    RecoveryValidationResult,
    build_recovery_bundle_id,
)

_ORCHESTRATOR_EXPORTS = {
    "BackupAlertService",
    "BackupEventBus",
    "BackupHealthService",
    "BackupJobRunner",
    "BackupMetricsService",
    "BackupOrchestrator",
    "BackupRestoreService",
    "BackupScheduler",
    "BackupService",
}


def __getattr__(name: str) -> Any:
    if name not in _ORCHESTRATOR_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(".orchestrator", __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | _ORCHESTRATOR_EXPORTS)

__all__ = [
    "AlertLevel",
    "BackupAlert",
    "BackupAlertService",
    "BackupArtifact",
    "BackupConfiguration",
    "BackupDestination",
    "BackupDestinationState",
    "BackupEvent",
    "BackupEventBus",
    "BackupHealthService",
    "BackupJob",
    "BackupJobRunner",
    "BackupJobState",
    "BackupManifest",
    "BackupMetrics",
    "BackupMetricsService",
    "BackupOrchestrator",
    "BackupRestoreService",
    "BackupSchedule",
    "BackupScheduler",
    "BackupService",
    "BackupSettings",
    "DisasterRecoveryService",
    "ExternalDiskProvider",
    "GoogleDriveProvider",
    "RestoreJob",
    "RestoreJobState",
    "RestoreResult",
    "RestoreResultBundle",
    "RecoveryBundleManifest",
    "RecoveryBundleSummary",
    "RecoveryReadinessScore",
    "RecoveryValidationResult",
    "LocalDiskProvider",
    "StorageProvider",
    "build_backup_id",
    "build_recovery_bundle_id",
    "utc_now",
]
