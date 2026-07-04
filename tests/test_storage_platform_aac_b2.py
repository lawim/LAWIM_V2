from __future__ import annotations

import unittest

from lawim_v2.storage_platform import (
    BackupCenter,
    BackupJob,
    BackupManager,
    CompressionPolicy,
    DeduplicationPolicy,
    DriveBalancingRule,
    DriveQuotaManager,
    ExternalDiskProvider,
    GoogleDriveProvider,
    LifecycleStateMachine,
    ProviderHealth,
    RestoreJob,
    RestorationEngine,
    SetupWizardConfiguration,
    StorageOptimizer,
    StorageOrchestrator,
    StorageOrchestratorPolicy,
    SyncJob,
)


class StoragePlatformAACB2Test(unittest.TestCase):
    def test_storage_orchestrator_uses_default_provider_and_temporary_access(self) -> None:
        orchestrator = StorageOrchestrator(
            providers=[GoogleDriveProvider("drive-1", quota_gb=100)],
            policy=StorageOrchestratorPolicy(default_provider="local"),
        )
        resolved = orchestrator.resolve_media_access(media_id=42, kind="video")

        self.assertEqual(resolved["provider"], "local")
        self.assertTrue(resolved["temporary_access_url"].startswith("https://"))
        self.assertEqual(resolved["lifecycle_state"], "hot")

    def test_drive_quota_and_balancing_rule_can_assign_drive(self) -> None:
        manager = DriveQuotaManager()
        rule = DriveBalancingRule(name="video-a", target_kind="video", provider_name="drive-1")
        assignment = manager.assign_drive(kind="video", size_bytes=4_000_000, rule=rule)

        self.assertEqual(assignment.provider_name, "drive-1")
        self.assertEqual(assignment.kind, "video")
        self.assertGreaterEqual(assignment.size_bytes, 0)

    def test_lifecycle_state_machine_supports_transition_and_backup_state(self) -> None:
        lifecycle = LifecycleStateMachine()
        self.assertEqual(lifecycle.transition("hot", "warm"), "warm")
        self.assertEqual(lifecycle.transition("warm", "cold"), "cold")
        self.assertEqual(lifecycle.backup_state_for("cold"), "queued")

    def test_backup_manager_creates_backup_and_restore_jobs(self) -> None:
        backup_center = BackupCenter()
        manager = BackupManager(backup_center=backup_center)
        backup_job = manager.create_backup_job(media_id=17, kind="image")
        restore_job = manager.create_restore_job(media_id=17, reason="recovery")

        self.assertIsInstance(backup_job, BackupJob)
        self.assertIsInstance(restore_job, RestoreJob)
        self.assertEqual(backup_job.media_id, 17)
        self.assertEqual(restore_job.reason, "recovery")

    def test_optimizer_and_restoration_engine_emit_expected_policy(self) -> None:
        optimizer = StorageOptimizer(
            compression=CompressionPolicy(level="balanced"),
            deduplication=DeduplicationPolicy(enabled=True),
        )
        restoration = RestorationEngine()
        plan = optimizer.plan(media_id=7, kind="document")
        restore = restoration.build_restore_plan(media_id=7, reason="quota")

        self.assertEqual(plan["compression"], "balanced")
        self.assertTrue(plan["deduplication_enabled"])
        self.assertEqual(restore["reason"], "quota")

    def test_setup_wizard_configuration_and_provider_health_are_mock_ready(self) -> None:
        wizard = SetupWizardConfiguration(
            architecture="OVH VPS + Backup Center + 10 Google Drive + external disk",
            backup_center_enabled=True,
            external_disk_enabled=True,
        )
        provider_health = ProviderHealth(name="drive-1", status="mock-ready")
        self.assertTrue(wizard.backup_center_enabled)
        self.assertEqual(provider_health.status, "mock-ready")

    def test_external_disk_provider_and_sync_job_are_supported(self) -> None:
        provider = ExternalDiskProvider(name="external-disk", capacity_gb=200)
        sync_job = SyncJob(media_id=99, provider_name=provider.name, direction="outbound")
        self.assertEqual(provider.name, "external-disk")
        self.assertEqual(sync_job.direction, "outbound")


if __name__ == "__main__":
    unittest.main()
