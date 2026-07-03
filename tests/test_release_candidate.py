from __future__ import annotations

from http import HTTPStatus

from lawim_harness import LawimTestHarness


class ReleaseCandidateSecurityTest(LawimTestHarness):
    PRIVATE_GET_ROUTES = (
        "/api/me",
        "/api/notifications",
        "/api/conversations",
        "/api/events",
    )

    def test_private_endpoints_require_authentication(self) -> None:
        for path in self.PRIVATE_GET_ROUTES:
            response = self.invoke(path)
            self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED, msg=path)
            error = self.assert_error_shape(response)
            self.assertIn(error["code"], {"unauthorized", "missing_token"})
            self.assertIn("WWW-Authenticate", response.response_headers)

    def test_security_headers_on_api_static_and_media(self) -> None:
        health = self.invoke("/api/health")
        for header in ("X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy"):
            self.assertIn(header, health.response_headers)

        static = self.invoke("/")
        self.assertIn("Content-Security-Policy", static.response_headers)
        self.assertIn("X-Frame-Options", static.response_headers)

        token = self.login(email="admin@lawim.local")
        media_list = self.invoke("/api/media?limit=1", token=token)
        self.assertEqual(media_list.status, HTTPStatus.OK)
        items = media_list.body_json().get("media") or []
        if items:
            media_url = items[0].get("url")
            if isinstance(media_url, str) and media_url.startswith("/media/"):
                media = self.invoke(media_url)
                self.assertEqual(media.status, HTTPStatus.OK)
                self.assertIn("X-Content-Type-Options", media.response_headers)
                self.assertIn("X-Frame-Options", media.response_headers)

    def test_oversized_json_payload_is_rejected(self) -> None:
        token = self.login(email="admin@lawim.local")
        oversized = b'{"title":"' + b"x" * self.max_json_body_bytes + b'"}'
        response = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            raw_body=oversized,
            headers={"Content-Type": "application/json", "Content-Length": str(len(oversized))},
        )
        self.assertEqual(response.status, HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
        self.assertEqual(self.assert_error_shape(response)["code"], "payload_too_large")

    def test_compose_configs_are_valid(self) -> None:
        import subprocess
        from pathlib import Path

        root = Path(__file__).resolve().parent.parent
        compose = root / "platform" / "compose.sh"
        pairs = (
            ("compose/docker-compose.base.yml", "compose/docker-compose.dev.yml"),
            ("compose/docker-compose.base.yml", "compose/docker-compose.postgres.yml"),
            ("docker/compose/docker-compose.base.yml", "docker/compose/docker-compose.development.yml"),
            ("docker/compose/docker-compose.base.yml", "docker/compose/docker-compose.postgres.yml"),
        )
        for base, overlay in pairs:
            result = subprocess.run(
                [str(compose), "-f", str(root / base), "-f", str(root / overlay), "config"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, msg=f"{base} + {overlay}: {result.stderr}")
