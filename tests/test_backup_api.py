from __future__ import annotations

from http import HTTPStatus

from .lawim_harness import LawimTestHarness


class BackupApiTests(LawimTestHarness):
    def test_backup_routes_require_authentication(self) -> None:
        response = self.invoke("/api/v2/backup/status")
        self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED)

    def test_backup_status_history_metrics_and_providers_are_exposed(self) -> None:
        token = self.login(email="admin@lawim.local")

        status = self.invoke("/api/v2/backup/status", token=token)
        history = self.invoke("/api/v2/backup/history", token=token)
        jobs = self.invoke("/api/v2/backup/jobs", token=token)
        providers = self.invoke("/api/v2/backup/providers", token=token)
        alerts = self.invoke("/api/v2/backup/alerts", token=token)
        metrics = self.invoke("/api/v2/backup/metrics", token=token)

        self.assertEqual(status.status, HTTPStatus.OK)
        self.assertEqual(history.status, HTTPStatus.OK)
        self.assertEqual(jobs.status, HTTPStatus.OK)
        self.assertEqual(providers.status, HTTPStatus.OK)
        self.assertEqual(alerts.status, HTTPStatus.OK)
        self.assertEqual(metrics.status, HTTPStatus.OK)

        status_payload = status.body_json()["data"]
        self.assertIn(status_payload["global_status"], {"WATCH", "PROTECTED", "DEGRADED", "CRITICAL"})
        self.assertIn("metrics", status_payload)
        self.assertGreaterEqual(len(history.body_json()["data"]), 1)
        self.assertGreaterEqual(len(jobs.body_json()["data"]), 1)
        self.assertGreaterEqual(len(providers.body_json()["data"]), 1)
        self.assertIn("total_jobs", metrics.body_json()["data"])

    def test_backup_actions_work_end_to_end(self) -> None:
        token = self.login(email="admin@lawim.local")

        run_response = self.invoke(
            "/api/v2/backup/run",
            method="POST",
            token=token,
            body={
                "kind": "postgresql",
                "destination": "local",
                "provider_name": "google-drive",
                "trigger": "cockpit"
            },
        )
        provider_response = self.invoke(
            "/api/v2/backup/provider/test",
            method="POST",
            token=token,
            body={"provider_identifier": "google-drive"},
        )
        restore_response = self.invoke(
            "/api/v2/backup/restore",
            method="POST",
            token=token,
            body={
                "backup_id": "LAWIM-20260711-020000",
                "kind": "postgresql",
                "target_environment": "isolated",
                "database_restored": True,
                "media_restored": False,
                "notes": "API test",
                "success": True,
            },
        )
        config_response = self.invoke(
            "/api/v2/backup/config",
            method="PATCH",
            token=token,
            body={
                "timezone": "Africa/Douala",
                "backup_root": str(self.tempdir.name + "/custom-backups"),
                "google_drive_schedule": ["01:00", "13:00"],
                "alerts_enabled": True,
            },
        )

        self.assertEqual(run_response.status, HTTPStatus.CREATED)
        self.assertEqual(provider_response.status, HTTPStatus.OK)
        self.assertEqual(restore_response.status, HTTPStatus.CREATED)
        self.assertEqual(config_response.status, HTTPStatus.OK)

        self.assertEqual(run_response.body_json()["data"]["kind"], "postgresql")
        self.assertEqual(provider_response.body_json()["data"]["identifier"], "google-drive")
        self.assertTrue(restore_response.body_json()["data"]["restore_result"]["success"])
        self.assertEqual(config_response.body_json()["data"]["timezone"], "Africa/Douala")
