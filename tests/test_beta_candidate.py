from __future__ import annotations

from http import HTTPStatus
from importlib import resources

from tests.lawim_harness import LawimTestHarness, MINIMAL_JPEG_BYTES


class BetaSecurityTest(LawimTestHarness):
    def test_public_users_list_is_forbidden(self) -> None:
        response = self.invoke("/api/users")
        self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED)

    def test_admin_users_list_redacts_password_fields(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/users?limit=10", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        for user in response.body_json()["users"]:
            self.assertIn("email", user)
            self.assertNotIn("password_hash", user)
            self.assertNotIn("password_salt", user)

    def test_public_health_is_minimal_admin_health_is_detailed(self) -> None:
        public = self.invoke("/api/health")
        self.assertEqual(public.status, HTTPStatus.OK)
        public_payload = public.body_json()
        self.assertEqual(public_payload["status"], "ok")
        self.assertNotIn("audit", public_payload)
        self.assertNotIn("metrics", public_payload)
        self.assertIn("schema_version", public_payload["database"])

        admin_token = self.login(email="admin@lawim.local")
        detailed = self.invoke("/api/health", token=admin_token)
        self.assertEqual(detailed.status, HTTPStatus.OK)
        detailed_payload = detailed.body_json()
        self.assertIn("audit", detailed_payload)
        self.assertIn("metrics", detailed_payload)

    def test_metrics_requires_admin(self) -> None:
        guest = self.invoke("/api/metrics")
        self.assertEqual(guest.status, HTTPStatus.UNAUTHORIZED)
        owner = self.invoke("/api/metrics", token=self.login(email="owner@lawim.local"))
        self.assertEqual(owner.status, HTTPStatus.FORBIDDEN)
        admin = self.invoke("/api/metrics", token=self.login(email="admin@lawim.local"))
        self.assertEqual(admin.status, HTTPStatus.OK)

    def test_include_deleted_requires_admin(self) -> None:
        owner_token = self.login(email="owner@lawim.local")
        denied = self.invoke("/api/properties?include_deleted=true", token=owner_token)
        self.assertEqual(denied.status, HTTPStatus.FORBIDDEN)
        admin_token = self.login(email="admin@lawim.local")
        allowed = self.invoke("/api/properties?include_deleted=true", token=admin_token)
        self.assertEqual(allowed.status, HTTPStatus.OK)


class BetaValidationTest(LawimTestHarness):
    def test_register_rejects_invalid_email_and_short_password(self) -> None:
        bad_email = self.invoke(
            "/api/auth/register",
            method="POST",
            body={"email": "not-an-email", "password": "lawim-demo", "full_name": "Bad", "role": "owner"},
        )
        self.assertEqual(bad_email.status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(self.assert_error_shape(bad_email)["code"], "invalid_payload")

        short_password = self.invoke(
            "/api/auth/register",
            method="POST",
            body={"email": "valid.user@lawim.local", "password": "short", "full_name": "Bad", "role": "owner"},
        )
        self.assertEqual(short_password.status, HTTPStatus.BAD_REQUEST)

    def test_media_upload_rejects_unrecognized_content(self) -> None:
        token = self.login(email="admin@lawim.local")
        created = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            body={"title": "Media reject test", "city": "Douala", "country": "Cameroon", "status": "draft"},
        )
        property_id = int(created.body_json()["property"]["id"])
        boundary = "----BetaMedia"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="property_id"\r\n\r\n'
            f"{property_id}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="bad.bin"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode("utf-8") + b"not-a-real-image" + f"\r\n--{boundary}--\r\n".encode("utf-8")
        response = self.invoke(
            "/api/media/upload",
            method="POST",
            token=token,
            raw_body=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)


class BetaGuestJourneyTest(LawimTestHarness):
    def test_guest_bootstrap_and_public_search(self) -> None:
        bootstrap = self.invoke("/api/bootstrap")
        self.assertEqual(bootstrap.status, HTTPStatus.OK)
        payload = bootstrap.body_json()
        self.assertIsNone(payload["current_user"])
        self.assertEqual(payload["conversations"], [])
        self.assertEqual(payload["notifications"], [])
        self.assertEqual(payload["users"], [])

        search = self.invoke("/api/properties?status=published&limit=5")
        self.assertEqual(search.status, HTTPStatus.OK)
        self.assertIn("properties", search.body_json())

        static = self.invoke("/")
        self.assertEqual(static.status, HTTPStatus.OK)
        self.assertIn("Content-Security-Policy", static.response_headers)


class BetaUiRegressionTest(LawimTestHarness):
    def test_static_ui_beta_markers(self) -> None:
        app_js = resources.files("lawim_v2.static").joinpath("app.js").read_text(encoding="utf-8")
        for marker in (
            "escapeHtml",
            "setLoading",
            "media-preview",
            "formatApiError",
            "notification-unread-count",
            "function journeyForRole",
            "applyJourney(journeyForRole(payload.user.role));",
            'applyJourney(journeyForRole(form.get("role")));',
        ):
            self.assertIn(marker, app_js)

        styles = resources.files("lawim_v2.static").joinpath("styles.css").read_text(encoding="utf-8")
        self.assertIn("media-preview", styles)
        self.assertIn('data-loading="true"', styles)
