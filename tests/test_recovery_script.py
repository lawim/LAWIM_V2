from __future__ import annotations

import os
import subprocess
from pathlib import Path

from lawim_v2.services import LawimServices

from .lawim_harness import LawimTestHarness


class RecoveryScriptTests(LawimTestHarness):
    def setUp(self) -> None:
        super().setUp()
        self.script = Path(__file__).resolve().parents[1] / "deployment" / "recovery" / "rebuild-lawim.sh"

    def _run_script(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        merged_env = os.environ.copy()
        merged_env.update(env or {})
        return subprocess.run(
            ["bash", str(self.script), *args],
            check=False,
            capture_output=True,
            text=True,
            env=merged_env,
        )

    def test_rebuild_script_is_executable_and_has_valid_shell_syntax(self) -> None:
        self.assertTrue(self.script.is_file())
        self.assertTrue(os.access(self.script, os.X_OK))

        syntax = subprocess.run(
            ["bash", "-n", str(self.script)],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(syntax.returncode, 0, msg=f"stdout:\n{syntax.stdout}\nstderr:\n{syntax.stderr}")

    def test_rebuild_script_accepts_explicit_bundle_in_dry_run(self) -> None:
        services = LawimServices(self.repository, self.config)
        bundle_result = services.disaster_recovery.generate_bundle(bundle_id="LAWIM-DRF-REBUILD-EXPLICIT")
        bundle_path = str(Path(str(bundle_result["bundle_path"])))

        run = self._run_script(
            "--bundle",
            bundle_path,
            "--dry-run",
            env={
                "LAWIM_ROOT": str(Path(self.tempdir.name) / "current"),
                "LAWIM_RELEASES_ROOT": str(Path(self.tempdir.name) / "releases"),
                "LAWIM_MEDIA_STORAGE_PATH": str(Path(self.tempdir.name) / "media"),
                "LAWIM_RECOVERY_BUNDLE": "",
                "LAWIM_RECOVERY_BUNDLE_ROOT": "",
                "LAWIM_GIT_REMOTE": "",
                "LAWIM_DATABASE_URL": "",
                "DATABASE_URL": "",
            },
        )

        self.assertEqual(run.returncode, 0, msg=f"stdout:\n{run.stdout}\nstderr:\n{run.stderr}")
        self.assertIn("selected recovery bundle:", run.stdout)
        self.assertIn(bundle_path, run.stdout)
        self.assertIn("dry-run: repository restore prepared", run.stdout)
        self.assertIn("dry-run: stack launch prepared", run.stdout)

    def test_rebuild_script_discovers_latest_bundle_from_root(self) -> None:
        services = LawimServices(self.repository, self.config)
        first = services.disaster_recovery.generate_bundle(bundle_id="LAWIM-DRF-20260711-010000")
        second = services.disaster_recovery.generate_bundle(bundle_id="LAWIM-DRF-20260711-020000")
        bundle_root = Path(str(first["bundle_path"])).parent

        run = self._run_script(
            "--dry-run",
            env={
                "LAWIM_ROOT": str(Path(self.tempdir.name) / "current"),
                "LAWIM_RELEASES_ROOT": str(Path(self.tempdir.name) / "releases"),
                "LAWIM_MEDIA_STORAGE_PATH": str(Path(self.tempdir.name) / "media"),
                "LAWIM_RECOVERY_BUNDLE": "",
                "LAWIM_RECOVERY_BUNDLE_ROOT": str(bundle_root),
                "LAWIM_GIT_REMOTE": "",
                "LAWIM_DATABASE_URL": "",
                "DATABASE_URL": "",
            },
        )

        self.assertEqual(run.returncode, 0, msg=f"stdout:\n{run.stdout}\nstderr:\n{run.stderr}")
        self.assertIn("LAWIM-DRF-20260711-020000", run.stdout)
        self.assertNotIn("LAWIM-DRF-20260711-010000", run.stdout)
        self.assertIn(str(Path(str(second["bundle_path"]))), run.stdout)
