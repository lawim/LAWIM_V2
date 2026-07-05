from __future__ import annotations

import json
import unittest

from lawim_v2 import GoogleDriveConfigurationModel, StorageResourceRegistry, StorageSetupWizard


class StorageResourceRegistryAAFTest(unittest.TestCase):
    def test_registry_models_ten_drives_with_phase_one_fields(self) -> None:
        registry = StorageResourceRegistry.default()

        self.assertEqual(len(registry.resources), 10)
        self.assertEqual(registry.get("drive-1").role, "Videos A")
        self.assertEqual(registry.get("drive-3").role, "Photos + Audio")
        self.assertEqual(registry.get("drive-5").quota_gb, 13.0)
        self.assertEqual(registry.get("drive-8").threshold_band(), "blocked")
        self.assertEqual(registry.get("drive-1").resource_type, "google-drive-resource")
        self.assertEqual(registry.get("drive-1").api_version, "v3")
        self.assertEqual(registry.get("drive-1").routing_strategy, "official-priority-route")
        self.assertEqual(registry.get("drive-1").backup_policy, "backup-center-activation")
        self.assertEqual(registry.get("drive-1").restore_policy, "restore-center-activation")
        self.assertEqual(registry.get("drive-1").last_control, "2026-07-05T10:00:00Z")
        self.assertEqual(registry.get("drive-1").last_access, "2026-07-05T10:00:00Z")

    def test_google_drive_configuration_is_placeholder_safe(self) -> None:
        registry = StorageResourceRegistry.default()
        configurations = registry.google_drive_configurations()

        self.assertEqual(len(configurations), 10)
        for configuration in configurations:
            self.assertIsInstance(configuration, GoogleDriveConfigurationModel)
            self.assertTrue(configuration.email_placeholder.endswith(".invalid"))
            self.assertIn("placeholder", configuration.credential_status)
            self.assertIn(configuration.test_status, {"activation-passed", "activation-review"})
            self.assertNotIn("drive.google.com", json.dumps(configuration.as_dict()))

    def test_dashboard_monitoring_and_backup_snapshots_are_operational(self) -> None:
        registry = StorageResourceRegistry.default()
        snapshot = registry.dashboard_snapshot()
        admin_snapshot = registry.google_drive_admin_snapshot()
        monitoring_snapshot = registry.monitoring_snapshot()
        backup_snapshot = registry.backup_center_configuration()

        self.assertEqual(snapshot["summary"]["resource_count"], 10)
        self.assertEqual(snapshot["summary"]["blocked_count"], 1)
        self.assertEqual(snapshot["summary"]["available_count"], 9)
        self.assertIn("drive-8", snapshot["blocked_resources"])
        self.assertEqual(snapshot["summary"]["last_control"], "2026-07-05T10:00:00Z")
        self.assertEqual(snapshot["summary"]["last_access"], "2026-07-05T10:00:00Z")
        self.assertEqual(len(snapshot["routes"]), 10)
        self.assertEqual(admin_snapshot["blocked_drives"], ["drive-8"])
        self.assertEqual(admin_snapshot["available_drives"], [
            "drive-1",
            "drive-2",
            "drive-3",
            "drive-4",
            "drive-5",
            "drive-6",
            "drive-7",
            "drive-9",
            "drive-10",
        ])
        self.assertEqual(monitoring_snapshot["quota_monitor"]["band"], "normal")
        self.assertIn("latency_ms", monitoring_snapshot)
        self.assertEqual(backup_snapshot["backup_center"], "activation-ready")
        self.assertEqual(backup_snapshot["storage_resource_registry"], "connected")
        self.assertEqual(backup_snapshot["storage_orchestrator"], "connected")
        self.assertIn("monitoring", backup_snapshot)

    def test_setup_wizard_builds_activation_plan_and_returns_safe_routes(self) -> None:
        wizard = StorageSetupWizard()
        registry = StorageResourceRegistry.default()
        result = wizard.build_activation_plan(registry)

        self.assertEqual(len(result["steps"]), 11)
        self.assertEqual(result["steps"][0]["step"], "Register the credential vault")
        self.assertEqual(result["sample_routes"]["video"], ["drive-1", "drive-2", "drive-8"])
        self.assertEqual(result["sample_routes"]["conversation archive"], ["drive-5", "drive-8"])
        self.assertTrue(result["no_real_secrets"])
        self.assertTrue(result["activation_ready"])
        self.assertEqual(len(result["required_folders"]), 10)
        self.assertIn("credential_vault", result)


if __name__ == "__main__":
    unittest.main()
