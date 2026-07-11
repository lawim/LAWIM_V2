from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from lawim_v2.services import LawimServices

from .lawim_harness import LawimTestHarness


class DisasterRecoveryReadinessTests(LawimTestHarness):
    def test_readiness_score_is_exposed_with_signals(self) -> None:
        services = LawimServices(self.repository, self.config)
        services.disaster_recovery.generate_bundle(bundle_id="LAWIM-DRF-READINESS")

        readiness = services.disaster_recovery.readiness_score()

        self.assertGreaterEqual(int(readiness["score"]), 0)
        self.assertLessEqual(int(readiness["score"]), 100)
        self.assertIn(readiness["state"], {"READY", "WATCH", "DEGRADED", "BLOCKED"})
        self.assertGreater(len(readiness["signals"]), 0)
        self.assertIn("bundle_id", readiness)

    def test_readiness_score_drops_when_secret_inventory_is_missing(self) -> None:
        services = LawimServices(self.repository, self.config)
        bundle = services.disaster_recovery.generate_bundle(bundle_id="LAWIM-DRF-READINESS-SECRET")
        bundle_path = Path(str(bundle["bundle_path"]))

        baseline = services.disaster_recovery.readiness_score()
        (bundle_path / "inventories" / "secret-inventory.json").unlink()
        degraded = services.disaster_recovery.readiness_score()

        self.assertGreater(baseline["score"], degraded["score"])
        self.assertTrue(
            any(signal["name"] in {"secret-inventory", "secret-coverage"} and not signal["passed"] for signal in degraded["signals"])
        )

    def test_readiness_score_drops_when_recovery_test_report_is_removed(self) -> None:
        services = LawimServices(self.repository, self.config)
        services.disaster_recovery.generate_bundle(bundle_id="LAWIM-DRF-READINESS-REPORT")

        state_root = Path(str(services.backup.configuration()["state_root"]))
        report_dir = state_root / "recovery-tests" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "latest-report.json"
        report_path.write_text(
            json.dumps(
                {
                    "bundle_id": "LAWIM-DRF-READINESS-REPORT",
                    "bundle_path": str(state_root / "recovery-bundles" / "LAWIM-DRF-READINESS-REPORT"),
                    "completed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                    "duration_seconds": 12.5,
                    "exit_code": 0,
                    "run_id": "LAWIM-DRF-TEST-READINESS",
                    "started_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                    "status": "PASS",
                    "stdout": ["dry-run: stack launch prepared"],
                },
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        baseline = services.disaster_recovery.readiness_score()
        report_path.unlink()
        degraded = services.disaster_recovery.readiness_score()

        self.assertGreater(baseline["score"], degraded["score"])
        self.assertTrue(any(signal["name"] == "isolated-recovery-test" and not signal["passed"] for signal in degraded["signals"]))
