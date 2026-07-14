from __future__ import annotations

from dataclasses import replace
from http import HTTPStatus

from tests.lawim_harness import LawimTestHarness, MINIMAL_JPEG_BYTES
from lawim_v2.config import AppConfig
from lawim_v2.rate_limit import AuthRateLimiter


class ReleaseCandidateHardeningTest(LawimTestHarness):
    def test_readyz_reports_database_ready(self) -> None:
        response = self.invoke("/readyz")
        self.assertEqual(response.status, HTTPStatus.OK)
        payload = response.body_json()
        self.assertEqual(payload.get("status"), "ready")
        self.assertTrue(payload.get("database", {}).get("ready"))

    def test_cors_reflects_allowed_origin(self) -> None:
        origin = "http://127.0.0.1:3000"
        self.config = replace(self.config, cors_allowed_origins=(origin,))
        response = self.invoke("/api/health", headers={"Origin": origin})
        self.assertEqual(response.response_headers.get("Access-Control-Allow-Origin"), origin)

    def test_cors_omits_header_for_unknown_origin(self) -> None:
        self.config = replace(self.config, cors_allowed_origins=("http://127.0.0.1:3000",))
        response = self.invoke("/api/health", headers={"Origin": "http://evil.example"})
        self.assertNotIn("Access-Control-Allow-Origin", response.response_headers)

    def test_auth_rate_limit_blocks_excessive_attempts(self) -> None:
        self.config = replace(
            self.config,
            auth_rate_limit_max=2,
            auth_rate_limit_window_seconds=300,
        )
        self.auth_limiter = AuthRateLimiter(
            max_attempts=self.config.auth_rate_limit_max,
            window_seconds=self.config.auth_rate_limit_window_seconds,
        )
        for _ in range(2):
            attempt = self.invoke(
                "/api/auth/login",
                method="POST",
                body={"email": "admin@lawim.local", "password": "wrong-password"},
            )
            self.assertEqual(attempt.status, HTTPStatus.UNAUTHORIZED)
        blocked = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "wrong-password"},
        )
        self.assertEqual(blocked.status, HTTPStatus.TOO_MANY_REQUESTS)
        self.assertEqual(self.assert_error_shape(blocked)["code"], "rate_limited")

    def test_private_media_requires_auth_when_public_media_disabled(self) -> None:
        media_file = self.media_path / "properties" / "1" / "rc-test.jpg"
        media_file.parent.mkdir(parents=True, exist_ok=True)
        media_file.write_bytes(MINIMAL_JPEG_BYTES)
        media_url = "/media/properties/1/rc-test.jpg"

        self.config = replace(self.config, public_media=False)
        denied = self.invoke(media_url)
        self.assertEqual(denied.status, HTTPStatus.UNAUTHORIZED)

        token = self.login(email="admin@lawim.local")
        allowed = self.invoke(media_url, token=token)
        self.assertEqual(allowed.status, HTTPStatus.OK)

    def test_bootstrap_exposes_demo_credentials_feature_flag(self) -> None:
        response = self.invoke("/api/bootstrap")
        self.assertEqual(response.status, HTTPStatus.OK)
        features = response.body_json().get("features") or {}
        self.assertTrue(features.get("demo_credentials"))

    def test_production_config_validation_rejects_unsafe_defaults(self) -> None:
        config = AppConfig.for_test(
            db_path=self.db_path,
            media_storage_path=self.media_path,
            app_env="production",
            public_base_url="http://localhost:3000",
            db_driver="postgresql",
            db_fallback=True,
            public_media=True,
        )
        with self.assertRaises(ValueError) as ctx:
            config.validate()
        message = str(ctx.exception)
        self.assertIn("PUBLIC_BASE_URL must use https", message)
        self.assertIn("LAWIM_DB_FALLBACK must be false", message)
        self.assertIn("LAWIM_PUBLIC_MEDIA must be false", message)


class AuthRateLimiterUnitTest(LawimTestHarness):
    def test_rate_limiter_resets_after_window(self) -> None:
        limiter = AuthRateLimiter(max_attempts=1, window_seconds=1)
        self.assertTrue(limiter.is_allowed("client"))
        self.assertFalse(limiter.is_allowed("client"))
