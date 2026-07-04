from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from unittest import TestCase


def _load_smoke_module():
    script = Path(__file__).resolve().parent.parent / "scripts" / "smoke_runtime.py"
    spec = importlib.util.spec_from_file_location("smoke_runtime", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["smoke_runtime"] = module
    spec.loader.exec_module(module)
    return module


class RuntimeSmokeTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.smoke = _load_smoke_module()

    def test_runtime_smoke_passes(self) -> None:
        result = self.smoke.run_smoke()
        self.assertTrue(result.ok, msg=result.message)


class ConfigValidationTest(TestCase):
    def test_invalid_config_reports_readable_errors(self) -> None:
        from lawim_v2.config import AppConfig

        config = AppConfig.legacy_construct(
            host="127.0.0.1",
            port=0,
            db_path=Path("data/runtime/lawim.sqlite3"),
            db_driver="sqlite",
            database_url="postgresql://lawim:lawim@localhost:5432/lawim_v2",
            db_fallback=True,
            app_env="development",
            stack_profile="development",
            log_level="info",
            public_base_url="http://127.0.0.1:3000",
            secret_provider="external",
            seed_demo_data=True,
            session_ttl_seconds=3600,
            media_storage_path=Path("data/runtime/media"),
            max_upload_bytes=5 * 1024 * 1024,
            geocoding_provider="local",
            geocoding_base_url="https://example.test",
            geocoding_api_key=None,
            cdn_base_url=None,
            metrics_enabled=True,
            match_min_score=10.0,
            max_json_body_bytes=1_048_576,
            cors_allowed_origins=("http://127.0.0.1:3000",),
            auth_rate_limit_max=30,
            auth_rate_limit_window_seconds=300,
            public_media=True,
        )
        with self.assertRaises(ValueError) as ctx:
            config.validate()
        self.assertIn("LAWIM_PORT", str(ctx.exception))
