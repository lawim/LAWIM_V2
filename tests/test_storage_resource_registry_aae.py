from __future__ import annotations

import json
import unittest

from lawim_v2.storage_platform import LocalStorageProvider, StorageOrchestrator, StorageOrchestratorPolicy
from lawim_v2.storage_registry import (
    GoogleDriveConfigurationModel,
    StorageResourceRegistry,
    StorageRoutingPolicy,
    StorageSetupWizard,
    StorageUsageThresholds,
)


class StorageResourceRegistryAAETest(unittest.TestCase):
    def test_registry_models_ten_drives_with_quota_and_thresholds(self) -> None:
        registry = StorageResourceRegistry.default()

        self.assertEqual(len(registry.resources), 10)
        self.assertEqual(registry.get("drive-1").role, "Videos A")
        self.assertEqual(registry.get("drive-3").role, "Photos + Audio")
        self.assertEqual(registry.get("drive-5").quota_gb, 13.0)
        self.assertEqual(registry.get("drive-8").threshold_band(), "blocked")
        self.assertEqual(registry.thresholds.as_dict()["normal_max_percent"], 70)

    def test_google_drive_configuration_is_placeholder_safe(self) -> None:
        registry = StorageResourceRegistry.default()
        configurations = registry.google_drive_configurations()

        self.assertEqual(len(configurations), 10)
        for configuration in configurations:
            self.assertIsInstance(configuration, GoogleDriveConfigurationModel)
            self.assertTrue(configuration.email_placeholder.endswith(".invalid"))
            self.assertIn("placeholder", configuration.credential_status)
            self.assertNotIn("drive.google.com", json.dumps(configuration.as_dict()))

    def test_routing_policy_matches_official_routes(self) -> None:
        policy = StorageRoutingPolicy()

        self.assertEqual(policy.route_for("video"), ("drive-1", "drive-2", "drive-8"))
        self.assertEqual(policy.route_for("photo"), ("drive-3", "drive-8"))
        self.assertEqual(policy.route_for("audio"), ("drive-3", "drive-8"))
        self.assertEqual(policy.route_for("conversation archive"), ("drive-5", "drive-8"))
        self.assertEqual(policy.route_for("export/rapport"), ("drive-6", "drive-8"))
        self.assertEqual(policy.route_for("backup applicatif"), ("drive-7", "drive-10"))
        self.assertEqual(policy.route_for("réplication critique"), ("drive-8", "drive-10"))
        self.assertEqual(policy.route_for("reserve"), ("drive-9",))
        self.assertEqual(policy.route_for("maintenance/migration"), ("drive-10",))

    def test_registry_dashboard_reports_available_and_blocked_resources(self) -> None:
        registry = StorageResourceRegistry.default()
        snapshot = registry.dashboard_snapshot()

        self.assertEqual(snapshot["summary"]["resource_count"], 10)
        self.assertEqual(snapshot["summary"]["blocked_count"], 1)
        self.assertEqual(snapshot["summary"]["available_count"], 9)
        self.assertIn("drive-8", snapshot["blocked_resources"])
        self.assertGreaterEqual(snapshot["summary"]["alert_count"], 3)
        self.assertEqual(snapshot["thresholds"]["slowdown_max_percent"], 92)

    def test_setup_wizard_runs_mock_steps_and_returns_safe_routes(self) -> None:
        wizard = StorageSetupWizard()
        registry = StorageResourceRegistry.default()
        result = wizard.run_mock(registry)

        self.assertEqual(len(result["steps"]), 8)
        self.assertEqual(result["steps"][0]["step"], "Declaration of the 10 drives")
        self.assertEqual(result["sample_routes"]["video"], ["drive-1", "drive-2", "drive-8"])
        self.assertEqual(result["sample_routes"]["conversation archive"], ["drive-5", "drive-8"])
        self.assertTrue(result["no_real_secrets"])

    def test_orchestrator_uses_registry_and_keeps_google_urls_out_of_business_data(self) -> None:
        orchestrator = StorageOrchestrator(
            providers=[LocalStorageProvider()],
            policy=StorageOrchestratorPolicy(default_provider="local"),
            resource_registry=StorageResourceRegistry.default(),
        )

        media_access = orchestrator.resolve_media_access(media_id=42, kind="video")
        conversation_access = orchestrator.resolve_conversation_archive_access(conversation_id=7)
        snapshot = orchestrator.resource_snapshot()

        self.assertEqual(media_access["routing"]["route"], ["drive-1", "drive-2", "drive-8"])
        self.assertEqual(media_access["storage_resource"]["drive_id"], "drive-1")
        self.assertEqual(conversation_access["provider"], "drive-5")
        self.assertEqual(conversation_access["routing"]["route"], ["drive-5", "drive-8"])
        self.assertNotIn("drive.google.com", json.dumps(media_access))
        self.assertNotIn("drive.google.com", json.dumps(conversation_access))
        self.assertNotIn("drive.google.com", json.dumps(snapshot))


if __name__ == "__main__":
    unittest.main()
