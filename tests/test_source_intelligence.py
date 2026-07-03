from __future__ import annotations

from http import HTTPStatus

from lawim_harness import LawimTestHarness


class SourceIntelligenceEngineTest(LawimTestHarness):
    def setUp(self) -> None:
        super().setUp()
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        self.assertEqual(login.status, HTTPStatus.CREATED, msg=login.body_text())
        self.admin_token = str(login.body_json()["token"])

    def test_dashboard_exposes_seeded_sources(self) -> None:
        response = self.invoke("/api/v2/source-intelligence/dashboard?limit=5", token=self.admin_token)
        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        payload = response.body_json()
        dashboard = payload["dashboard"]
        self.assertIn("stats", dashboard)
        self.assertGreaterEqual(len(dashboard["sources"]), 1)
        first_source = dashboard["sources"][0]
        self.assertIn("reference_code", first_source)
        self.assertIn("source_key", first_source)

    def test_reference_code_generation_is_deterministic_format(self) -> None:
        response = self.invoke(
            "/api/v2/source-intelligence/reference-code",
            method="POST",
            token=self.admin_token,
            body={"seed": "sie:test"},
        )
        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        code = str(response.body_json()["reference_code"])
        self.assertTrue(code.startswith("#"))
        self.assertEqual(len(code), 7)

    def test_import_creates_source_context_and_whatsapp_link(self) -> None:
        response = self.invoke(
            "/api/v2/source-intelligence/imports",
            method="POST",
            token=self.admin_token,
            body={
                "url": "https://example.cm/douala-apartment",
                "name": "Example Publication",
                "channel": "web",
                "title": "Douala apartment listing",
                "text": "Appartement à Douala #lawim",
                "city": "Douala",
                "property_type": "apartment",
                "notes": "Import from SIE test",
            },
        )
        self.assertEqual(response.status, HTTPStatus.CREATED, msg=response.body_text())
        payload = response.body_json()
        self.assertIn("source", payload)
        self.assertIn("context", payload)
        self.assertIn("import", payload)
        self.assertTrue(str(payload.get("whatsapp_link", "")).startswith("https://wa.me/"))
        source_id = int(payload["source"]["id"])

        context = self.invoke(
            f"/api/v2/source-intelligence/sources/{source_id}/context",
            token=self.admin_token,
        )
        self.assertEqual(context.status, HTTPStatus.OK, msg=context.body_text())
        self.assertEqual(context.body_json()["context"]["city"], "Douala")
