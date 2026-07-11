from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from lawim_v2.services import LawimServices

from .lawim_harness import LawimTestHarness


class MonthlyRecoveryTestTests(LawimTestHarness):
    def setUp(self) -> None:
        super().setUp()
        self.script = Path(__file__).resolve().parents[1] / "deployment" / "recovery" / "monthly-recovery-test.sh"

    def _run_script(self, *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        merged_env = os.environ.copy()
        merged_env.update(env)
        return subprocess.run(
            ["bash", str(self.script)],
            check=False,
            capture_output=True,
            text=True,
            env=merged_env,
        )

    def _prepare_bundle(self, bundle_id: str = "LAWIM-DRF-MONTHLY-TEST") -> tuple[str, Path]:
        services = LawimServices(self.repository, self.config)
        bundle = services.disaster_recovery.generate_bundle(bundle_id=bundle_id)
        return bundle_id, Path(str(bundle["bundle_path"])).parent

    def test_monthly_recovery_test_script_is_executable_and_syntax_valid(self) -> None:
        self.assertTrue(self.script.is_file())
        self.assertTrue(os.access(self.script, os.X_OK))

        syntax = subprocess.run(
            ["bash", "-n", str(self.script)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(syntax.returncode, 0, msg=f"stdout:\n{syntax.stdout}\nstderr:\n{syntax.stderr}")

    def test_monthly_recovery_test_creates_report_in_isolated_workspace(self) -> None:
        bundle_id, bundle_root = self._prepare_bundle()
        test_root = Path(self.tempdir.name) / "recovery-test"

        run = self._run_script(
            env={
                "LAWIM_RECOVERY_TEST_ROOT": str(test_root),
                "LAWIM_RECOVERY_BUNDLE_ROOT": str(bundle_root),
                "LAWIM_RECOVERY_BUNDLE": "",
            }
        )

        self.assertEqual(run.returncode, 0, msg=f"stdout:\n{run.stdout}\nstderr:\n{run.stderr}")
        report_json = test_root / "reports" / "latest-report.json"
        report_md = test_root / "reports" / "latest-report.md"
        payload = json.loads(report_json.read_text(encoding="utf-8"))

        self.assertEqual(payload["bundle_id"], bundle_id)
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["exit_code"], 0)
        self.assertGreater(payload["duration_seconds"], 0)
        self.assertTrue(any("selected recovery bundle" in line for line in payload["stdout"]))
        self.assertTrue(any("dry-run: stack launch prepared" in line for line in payload["stdout"]))
        self.assertTrue(report_md.is_file())
        self.assertIn("Monthly Recovery Test", report_md.read_text(encoding="utf-8"))
        self.assertIn(bundle_id, run.stdout)
        self.assertIn("isolated recovery report written", run.stdout)

    def test_monthly_recovery_test_is_idempotent_in_an_isolated_workspace(self) -> None:
        bundle_id, bundle_root = self._prepare_bundle("LAWIM-DRF-MONTHLY-IDEMPOTENT")
        test_root = Path(self.tempdir.name) / "recovery-test"

        first = self._run_script(
            env={
                "LAWIM_RECOVERY_TEST_ROOT": str(test_root),
                "LAWIM_RECOVERY_BUNDLE_ROOT": str(bundle_root),
                "LAWIM_RECOVERY_BUNDLE": "",
            }
        )
        second = self._run_script(
            env={
                "LAWIM_RECOVERY_TEST_ROOT": str(test_root),
                "LAWIM_RECOVERY_BUNDLE_ROOT": str(bundle_root),
                "LAWIM_RECOVERY_BUNDLE": "",
            }
        )

        self.assertEqual(first.returncode, 0, msg=f"stdout:\n{first.stdout}\nstderr:\n{first.stderr}")
        self.assertEqual(second.returncode, 0, msg=f"stdout:\n{second.stdout}\nstderr:\n{second.stderr}")

        report_json = test_root / "reports" / "latest-report.json"
        payload = json.loads(report_json.read_text(encoding="utf-8"))
        self.assertEqual(payload["bundle_id"], bundle_id)
        self.assertEqual(payload["status"], "PASS")
        self.assertGreater(payload["duration_seconds"], 0)
        self.assertEqual(payload["run_id"].startswith("LAWIM-DRF-TEST-"), True)
