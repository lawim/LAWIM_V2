from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

from lawim_v2.db import LawimRepository
from lawim_v2.security import verify_password


def test_admin_reset_password_script_updates_user_password(tmp_path: Path) -> None:
    db_path = tmp_path / "lawim.sqlite3"
    repository = LawimRepository(db_path)
    repository.initialize(seed_demo_data=False)
    user = repository.create_user(
        email="reset@example.com",
        full_name="Reset User",
        role="owner",
        password="old-password",
        organization_id=None,
    )

    env = {
        **dict(os.environ),
        "LAWIM_DB_DRIVER": "sqlite",
        "LAWIM_DB_PATH": str(db_path),
        "APP_ENV": "test",
        "LAWIM_DATABASE_URL": "",
    }

    script = Path(__file__).resolve().parent.parent / "scripts" / "admin_reset_password.py"
    result = subprocess.run(
        [sys.executable, str(script), "--email", "reset@example.com", "--password", "new-password"],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    output = result.stdout.strip()
    assert "Password reset successfully for user: reset@example.com" in output

    saved_app_env = os.environ.get("APP_ENV")
    os.environ["APP_ENV"] = "test"
    try:
        fresh_repository = LawimRepository(db_path)
        updated = fresh_repository.get_user_by_email("reset@example.com")
        assert verify_password("new-password", str(updated["password_salt"]), str(updated["password_hash"]))
    finally:
        if saved_app_env is None:
            del os.environ["APP_ENV"]
        else:
            os.environ["APP_ENV"] = saved_app_env


def test_admin_reset_password_script_returns_error_for_unknown_user(tmp_path: Path) -> None:
    db_path = tmp_path / "lawim.sqlite3"
    repository = LawimRepository(db_path)
    repository.initialize(seed_demo_data=False)

    env = {
        **dict(os.environ),
        "LAWIM_DB_DRIVER": "sqlite",
        "LAWIM_DB_PATH": str(db_path),
        "APP_ENV": "test",
        "LAWIM_DATABASE_URL": "",
    }

    script = Path(__file__).resolve().parent.parent / "scripts" / "admin_reset_password.py"
    result = subprocess.run(
        [sys.executable, str(script), "--email", "missing@example.com", "--password", "new-password"],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "User not found: missing@example.com" in result.stdout.strip()
