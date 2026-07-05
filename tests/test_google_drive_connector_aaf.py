from __future__ import annotations

import json
import unittest

from lawim_v2 import GoogleDriveConnector, GoogleDriveOAuthCredentials, StorageResourceRegistry, StorageSetupWizard


class GoogleDriveConnectorAAFTest(unittest.TestCase):
    def test_oauth_contract_and_required_folders(self) -> None:
        registry = StorageResourceRegistry.default()
        connector = registry.connector_for("drive-1")

        self.assertIsInstance(connector.oauth, GoogleDriveOAuthCredentials)
        self.assertEqual(connector.oauth.status, "placeholder-configured")
        self.assertEqual(len(connector.required_folders()), 10)
        self.assertIn("VIDEOS", connector.required_folders())

        connection = connector.connect()
        refresh = connector.refresh_access_token()

        self.assertTrue(connection["connected"])
        self.assertEqual(connection["oauth_status"], "placeholder-configured")
        self.assertEqual(connection["api_version"], "v3")
        self.assertEqual(refresh["token_refresh"], "automatic")
        self.assertEqual(refresh["expiry"], "never")
        self.assertNotIn("drive.google.com", json.dumps(connection))

    def test_read_write_delete_and_quota_tracking(self) -> None:
        registry = StorageResourceRegistry.default()
        connector = registry.connector_for("drive-1")

        created = connector.create_folder("videos")
        uploaded = connector.write(folder_name="VIDEOS", object_name="clip.mp4", size_bytes=50_000_000)
        downloaded = connector.read(folder_name="VIDEOS", object_name="clip.mp4")
        deleted = connector.delete(folder_name="VIDEOS", object_name="clip.mp4")
        quota = connector.quota_status()

        self.assertEqual(created["status"], "created")
        self.assertEqual(uploaded["status"], "ok")
        self.assertEqual(downloaded["status"], "ok")
        self.assertEqual(deleted["status"], "ok")
        self.assertGreaterEqual(quota["available_gb"], 0)
        self.assertGreaterEqual(len(connector.journal), 4)
        self.assertNotIn("drive.google.com", json.dumps(connector.activation_snapshot()))

    def test_health_and_monitoring_snapshot_include_alerts(self) -> None:
        registry = StorageResourceRegistry.default()
        connector = registry.connector_for("drive-8")

        health = connector.health_status()
        monitoring = connector.monitoring_snapshot()

        self.assertEqual(health["state"], "blocked")
        self.assertEqual(monitoring["quota_monitor"]["band"], "blocked")
        self.assertGreaterEqual(len(monitoring["alerts"]), 1)
        self.assertIn("rotation", monitoring)

    def test_dashboard_and_wizard_are_activation_ready(self) -> None:
        registry = StorageResourceRegistry.default()
        dashboard = registry.google_drive_admin_snapshot()
        wizard = StorageSetupWizard()
        plan = wizard.build_activation_plan(registry)

        self.assertEqual(len(dashboard["drives"]), 10)
        self.assertEqual(dashboard["blocked_drives"], ["drive-8"])
        self.assertIn("required_folders", dashboard)
        self.assertEqual(len(plan["steps"]), 11)
        self.assertEqual(plan["steps"][0]["step"], "Register the credential vault")
        self.assertTrue(plan["activation_ready"])
        self.assertEqual(plan["required_folders"], list(GoogleDriveConnector.required_folders()))
        self.assertEqual(dashboard["monitoring"]["apiMonitor"]["apiVersion"], "v3")
        self.assertNotIn("drive.google.com", json.dumps(dashboard))
        self.assertNotIn("drive.google.com", json.dumps(plan))


if __name__ == "__main__":
    unittest.main()
