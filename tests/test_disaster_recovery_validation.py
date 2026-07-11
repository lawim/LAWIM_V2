from __future__ import annotations

from http import HTTPStatus
from pathlib import Path

from lawim_v2.services import LawimServices

from .lawim_harness import LawimTestHarness


class DisasterRecoveryValidationTests(LawimTestHarness):
    def test_recovery_validation_routes_require_admin_authentication(self) -> None:
        response = self.invoke("/api/v2/backup/recovery")
        self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED)

    def test_recovery_status_and_validation_are_exposed(self) -> None:
        token = self.login(email="admin@lawim.local")
        services = LawimServices(self.repository, self.config)
        bundle_id = "LAWIM-DRF-API-VALIDATION"
        bundle = services.disaster_recovery.generate_bundle(bundle_id=bundle_id)

        status = self.invoke("/api/v2/backup/recovery", token=token)
        bundles = self.invoke("/api/v2/backup/recovery/bundles", token=token)
        latest = self.invoke("/api/v2/backup/recovery/latest", token=token)
        validation = self.invoke(
            "/api/v2/backup/recovery/validate",
            method="POST",
            token=token,
            body={"bundle_id": bundle_id},
        )

        self.assertEqual(status.status, HTTPStatus.OK)
        self.assertEqual(bundles.status, HTTPStatus.OK)
        self.assertEqual(latest.status, HTTPStatus.OK)
        self.assertEqual(validation.status, HTTPStatus.OK)

        status_payload = status.body_json()["data"]
        validation_payload = validation.body_json()["data"]
        self.assertEqual(status_payload["latest_bundle"]["bundle_id"], bundle_id)
        self.assertEqual(latest.body_json()["data"]["bundle_id"], bundle_id)
        self.assertTrue(validation_payload["restore_ready"])
        self.assertTrue(validation_payload["manifest_present"])
        self.assertTrue(validation_payload["checksum_valid"])
        self.assertGreater(len(validation_payload["checks"]), 0)
        self.assertTrue(any(check["name"] == "restore-ready" and check["passed"] for check in validation_payload["checks"]))
        self.assertTrue(any(check["name"] == "git-synced" and check["passed"] for check in validation_payload["checks"]))
        self.assertEqual(Path(str(bundle["bundle_path"])).name, bundle_id)
        self.assertGreaterEqual(len(bundles.body_json()["data"]), 1)

    def test_recovery_validation_detects_checksum_drift(self) -> None:
        services = LawimServices(self.repository, self.config)
        bundle_id = "LAWIM-DRF-CHECKSUM-DRIFT"
        bundle = services.disaster_recovery.generate_bundle(bundle_id=bundle_id)
        bundle_path = Path(str(bundle["bundle_path"]))
        checklist = bundle_path / "documents" / "RECOVERY_CHECKLIST.md"
        checklist.write_text(checklist.read_text(encoding="utf-8") + "\ncorrupted\n", encoding="utf-8")

        validation = services.disaster_recovery.validate_bundle(bundle_id)

        self.assertFalse(validation["checksum_valid"])
        self.assertFalse(validation["restore_ready"])
        self.assertTrue(any(check["name"] == "checksum-valid" and not check["passed"] for check in validation["checks"]))

    def test_recovery_validation_detects_missing_files(self) -> None:
        services = LawimServices(self.repository, self.config)
        bundle_id = "LAWIM-DRF-MISSING-FILE"
        bundle = services.disaster_recovery.generate_bundle(bundle_id=bundle_id)
        bundle_path = Path(str(bundle["bundle_path"]))
        missing_file = bundle_path / "inventories" / "secret-inventory.json"
        missing_file.unlink()

        validation = services.disaster_recovery.validate_bundle(bundle_id)

        self.assertIn("inventories/secret-inventory.json", validation["missing_files"])
        self.assertFalse(validation["checksum_valid"])
        self.assertFalse(validation["restore_ready"])
        self.assertTrue(any(check["name"] == "bundle-integrity" and not check["passed"] for check in validation["checks"]))
