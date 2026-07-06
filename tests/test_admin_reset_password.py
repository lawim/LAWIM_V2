from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from lawim_v2.bootstrap import build_runtime
from lawim_v2.config import AppConfig
from lawim_v2.security import verify_password


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "admin_reset_password.py"


def _script_env(
    config: AppConfig,
    *,
    database_url: str | None = None,
    db_driver: str | None = None,
    db_fallback: bool | None = None,
) -> dict[str, str]:
    env = dict(os.environ)
    env.update(
        {
            "APP_ENV": config.app_env,
            "STACK_PROFILE": config.stack_profile,
            "LOG_LEVEL": config.log_level,
            "LAWIM_HOST": config.host,
            "LAWIM_PORT": str(config.port),
            "LAWIM_DB_DRIVER": db_driver or config.db_driver,
            "LAWIM_DB_PATH": str(config.db_path),
            "LAWIM_MEDIA_STORAGE_PATH": str(config.media_storage_path),
            "LAWIM_DATABASE_URL": database_url if database_url is not None else config.database_url,
            "LAWIM_DB_FALLBACK": "true" if (config.db_fallback if db_fallback is None else db_fallback) else "false",
            "PUBLIC_BASE_URL": config.public_base_url,
            "SECRET_PROVIDER": config.secret_provider,
            "LAWIM_SEED_DEMO_DATA": "true" if config.seed_demo_data else "false",
            "LAWIM_MEDIA_PROVIDER": config.media_provider,
            "LAWIM_MAX_UPLOAD_BYTES": str(config.max_upload_bytes),
            "LAWIM_GEOCODING_PROVIDER": config.geocoding_provider,
            "LAWIM_GEOCODING_BASE_URL": config.geocoding_base_url,
            "LAWIM_METRICS_ENABLED": "true" if config.metrics_enabled else "false",
            "LAWIM_MATCH_MIN_SCORE": str(config.match_min_score),
            "LAWIM_MAX_JSON_BODY_BYTES": str(config.max_json_body_bytes),
            "LAWIM_CORS_ORIGINS": ",".join(config.cors_allowed_origins),
            "LAWIM_AUTH_RATE_LIMIT_MAX": str(config.auth_rate_limit_max),
            "LAWIM_AUTH_RATE_LIMIT_WINDOW_SECONDS": str(config.auth_rate_limit_window_seconds),
            "LAWIM_PUBLIC_MEDIA": "true" if config.public_media else "false",
            "LAWIM_SESSION_TTL_SECONDS": str(config.session_ttl_seconds),
        }
    )
    if config.geocoding_api_key is not None:
        env["LAWIM_GEOCODING_API_KEY"] = config.geocoding_api_key
    if config.cdn_base_url is not None:
        env["LAWIM_CDN_BASE_URL"] = config.cdn_base_url
    return env


def _run_script(env: dict[str, str], *, email: str, password: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--email", email, "--password", password],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _verify_password_in_test_mode(password: str, salt: object, hashed: object) -> bool:
    saved_app_env = os.environ.get("APP_ENV")
    os.environ["APP_ENV"] = "test"
    try:
        return verify_password(password, str(salt), str(hashed))
    finally:
        if saved_app_env is None:
            os.environ.pop("APP_ENV", None)
        else:
            os.environ["APP_ENV"] = saved_app_env


class AdminResetPasswordTest(unittest.TestCase):
    def test_admin_reset_password_script_updates_user_password(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            db_path = root / "lawim.sqlite3"
            media_path = root / "media"
            config = AppConfig.for_test(db_path=db_path, media_storage_path=media_path)
            runtime = build_runtime(config)
            try:
                runtime.repository.create_user(
                    email="reset@example.com",
                    full_name="Reset User",
                    role="owner",
                    password="old-password",
                    organization_id=None,
                )

                result = _run_script(
                    _script_env(config),
                    email="reset@example.com",
                    password="new-password",
                )

                self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
                self.assertIn("Password reset successfully for user: reset@example.com", result.stdout.strip())

                updated = runtime.repository.get_user_by_email("reset@example.com")
                self.assertTrue(_verify_password_in_test_mode("new-password", updated["password_salt"], updated["password_hash"]))
            finally:
                runtime.close()

    def test_admin_reset_password_script_returns_error_for_unknown_user(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            db_path = root / "lawim.sqlite3"
            media_path = root / "media"
            config = AppConfig.for_test(db_path=db_path, media_storage_path=media_path)
            runtime = build_runtime(config)
            try:
                result = _run_script(
                    _script_env(config),
                    email="missing@example.com",
                    password="new-password",
                )

                self.assertEqual(result.returncode, 1)
                self.assertIn("User not found: missing@example.com", result.stdout.strip())
            finally:
                runtime.close()


class PostgreSQLAdminResetPasswordIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dsn = os.getenv("LAWIM_TEST_POSTGRES_URL", "").strip()
        if not cls.dsn:
            raise unittest.SkipTest("LAWIM_TEST_POSTGRES_URL not set — PostgreSQL admin reset skipped")
        try:
            import pg8000  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("pg8000 not installed — pip install -r requirements-postgresql.txt") from exc

    def test_admin_reset_password_script_updates_user_password(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            db_path = Path(tempdir) / "fallback.sqlite3"
            media_path = Path(tempdir) / "media"
            config = AppConfig.for_test(
                db_path=db_path,
                media_storage_path=media_path,
                db_driver="postgresql",
                database_url=self.dsn,
                db_fallback=False,
            )
            runtime = build_runtime(config)
            try:
                runtime.repository.create_user(
                    email="pg-reset@example.com",
                    full_name="Reset User",
                    role="owner",
                    password="old-password",
                    organization_id=None,
                )

                result = _run_script(
                    _script_env(
                        config,
                        database_url=self.dsn,
                        db_driver="postgresql",
                        db_fallback=False,
                    ),
                    email="pg-reset@example.com",
                    password="new-password",
                )

                assert result.returncode == 0, result.stderr or result.stdout
                assert "Password reset successfully for user: pg-reset@example.com" in result.stdout.strip()

                updated = runtime.repository.get_user_by_email("pg-reset@example.com")
                assert _verify_password_in_test_mode("new-password", updated["password_salt"], updated["password_hash"])
            finally:
                runtime.close()
