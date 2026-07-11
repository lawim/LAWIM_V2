from __future__ import annotations

import json
from pathlib import Path

from lawim_v2 import __version__ as LAWIM_VERSION
from lawim_v2.backup import build_recovery_bundle_id
from lawim_v2.services import LawimServices

from .lawim_harness import LawimTestHarness


class DisasterRecoveryBundleTests(LawimTestHarness):
    def test_recovery_bundle_id_uses_lawim_prefix(self) -> None:
        bundle_id = build_recovery_bundle_id()
        self.assertTrue(bundle_id.startswith("LAWIM-DRF-"))

    def test_bundle_generation_creates_manifest_database_and_checklist(self) -> None:
        services = LawimServices(self.repository, self.config)
        result = services.disaster_recovery.generate_bundle(bundle_id="LAWIM-DRF-TEST")

        bundle_path = Path(str(result["bundle_path"]))
        manifest_path = Path(str(result["manifest_path"]))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(manifest["bundle_id"], "LAWIM-DRF-TEST")
        self.assertEqual(manifest["lawim_version"], LAWIM_VERSION)
        self.assertIn("checksum", manifest)
        self.assertEqual(manifest["encryption_method"], "none")
        self.assertGreater(len(manifest["files"]), 0)

        file_paths = {str(item["relative_path"]) for item in manifest["files"]}
        self.assertIn("database/postgresql.dump.sql", file_paths)
        self.assertIn("documents/RECOVERY_CHECKLIST.md", file_paths)
        self.assertIn("documents/BACKUP_STATUS.json", file_paths)
        self.assertIn("inventories/software-inventory.json", file_paths)
        self.assertIn("inventories/hardware-inventory.json", file_paths)
        self.assertIn("inventories/docker-inventory.json", file_paths)
        self.assertIn("inventories/git-state.json", file_paths)
        self.assertIn("inventories/secret-inventory.json", file_paths)
        self.assertIn("inventories/backup-config.json", file_paths)
        self.assertIn("config/Dockerfile", file_paths)
        self.assertTrue((bundle_path / "database" / "postgresql.dump.sql").is_file())
        self.assertTrue((bundle_path / "documents" / "RECOVERY_CHECKLIST.md").is_file())
        self.assertTrue((bundle_path / "documents" / "BACKUP_STATUS.json").is_file())
        self.assertTrue((bundle_path / "inventories" / "software-inventory.json").is_file())
        self.assertTrue((bundle_path / "inventories" / "hardware-inventory.json").is_file())
        self.assertTrue((bundle_path / "inventories" / "docker-inventory.json").is_file())
        self.assertTrue((bundle_path / "inventories" / "git-state.json").is_file())
        self.assertTrue((bundle_path / "inventories" / "secret-inventory.json").is_file())
        self.assertTrue((bundle_path / "inventories" / "backup-config.json").is_file())

    def test_bundle_status_and_validation_expose_latest_bundle(self) -> None:
        services = LawimServices(self.repository, self.config)
        result = services.disaster_recovery.generate_bundle(bundle_id="LAWIM-DRF-VALIDATION")

        status = services.disaster_recovery.status()
        validation = services.disaster_recovery.validate_bundle("LAWIM-DRF-VALIDATION")

        self.assertEqual(status["latest_bundle"]["bundle_id"], "LAWIM-DRF-VALIDATION")
        self.assertIn("readiness", status)
        self.assertGreaterEqual(int(status["readiness"]["score"]), 0)
        self.assertLessEqual(int(status["readiness"]["score"]), 100)
        self.assertIn(status["readiness"]["state"], {"READY", "WATCH", "DEGRADED", "BLOCKED"})
        self.assertEqual(validation["bundle_id"], "LAWIM-DRF-VALIDATION")
        self.assertTrue(validation["manifest_present"])
        self.assertTrue(validation["checksum_valid"])
        self.assertTrue(validation["compatible"])
        self.assertTrue(validation["restore_ready"])
        self.assertEqual(Path(str(result["bundle_path"])).name, "LAWIM-DRF-VALIDATION")

        secret_inventory = json.loads(
            (Path(str(result["bundle_path"])) / "inventories" / "secret-inventory.json").read_text(encoding="utf-8")
        )
        self.assertGreater(len(secret_inventory), 0)
        for entry in secret_inventory:
            self.assertSetEqual(set(entry.keys()), {"name", "type", "location", "required", "present"})
