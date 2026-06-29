from __future__ import annotations

import io
import json
import tempfile
from http import HTTPStatus
from pathlib import Path
from unittest import TestCase

from lawim_v2.config import AppConfig
from lawim_v2.db import LawimRepository
from lawim_v2.server import LawimRequestHandler


class DummyHandler(LawimRequestHandler):
    def __init__(
        self,
        repository: LawimRepository,
        config: AppConfig,
        path: str,
        *,
        method: str = "GET",
        headers: dict[str, str] | None = None,
        body: bytes = b"",
    ) -> None:
        self.repository = repository
        self.config = config
        self.path = path
        self.command = method
        self.headers = headers or {}
        self.rfile = io.BytesIO(body)
        self.wfile = io.BytesIO()
        self.status: int | None = None
        self.response_headers: dict[str, str] = {}
        self.send_response = lambda status: setattr(self, "status", int(status))
        self.send_header = lambda key, value: self.response_headers.__setitem__(key, value)
        self.end_headers = lambda: None

    def body_text(self) -> str:
        return self.wfile.getvalue().decode("utf-8")

    def body_json(self) -> dict[str, object]:
        return json.loads(self.body_text())


class LawimV2ExecutableBaselineTest(TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tempdir.name) / "lawim.sqlite3"
        self.repository = LawimRepository(self.db_path)
        self.repository.initialize(seed_demo_data=True)
        self.config = AppConfig(
            host="127.0.0.1",
            port=3000,
            db_path=self.db_path,
            app_env="test",
            stack_profile="test",
            log_level="debug",
            public_base_url="http://127.0.0.1:3000",
            secret_provider="external",
            seed_demo_data=True,
            session_ttl_seconds=3600,
        )

    def tearDown(self) -> None:
        self.repository.close()
        self.tempdir.cleanup()

    def invoke(self, path: str, *, method: str = "GET", body: dict[str, object] | None = None, token: str | None = None) -> DummyHandler:
        headers: dict[str, str] = {}
        payload = b""
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            headers["Content-Length"] = str(len(payload))
            headers["Content-Type"] = "application/json"
        if token:
            headers["Authorization"] = f"Bearer {token}"

        handler = DummyHandler(self.repository, self.config, path, method=method, headers=headers, body=payload)
        if method == "GET":
            handler.do_GET()
        elif method == "POST":
            handler.do_POST()
        else:  # pragma: no cover - helper is only used for GET/POST
            raise AssertionError(f"Unsupported method: {method}")
        return handler

    def test_health_bootstrap_and_static_assets_are_exposed(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.status, HTTPStatus.OK)
        health_payload = health.body_json()
        self.assertEqual(health_payload["status"], "ok")
        self.assertEqual(health_payload["summary"]["organizations"], 3)
        self.assertEqual(health_payload["summary"]["users"], 3)

        bootstrap = self.invoke("/api/bootstrap")
        self.assertEqual(bootstrap.status, HTTPStatus.OK)
        bootstrap_payload = bootstrap.body_json()
        self.assertEqual(bootstrap_payload["summary"]["published_properties"], 3)
        self.assertEqual(len(bootstrap_payload["properties"]), 3)

        html = self.invoke("/")
        self.assertEqual(html.status, HTTPStatus.OK)
        self.assertIn("LAWIM_V2 Executable Baseline", html.body_text())

        js = self.invoke("/app.js")
        self.assertEqual(js.status, HTTPStatus.OK)
        self.assertIn("renderBootstrap", js.body_text())

    def test_authentication_and_matching_flow_work_end_to_end(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        self.assertEqual(login.status, HTTPStatus.CREATED)
        login_payload = login.body_json()
        token = str(login_payload["token"])

        me = self.invoke("/api/me", token=token)
        self.assertEqual(me.status, HTTPStatus.OK)
        me_payload = me.body_json()
        self.assertEqual(me_payload["user"]["email"], "admin@lawim.local")

        matches = self.invoke("/api/matches?city=Douala&budget_max=320000&limit=1", token=token)
        self.assertEqual(matches.status, HTTPStatus.OK)
        matches_payload = matches.body_json()
        self.assertEqual(len(matches_payload["matches"]), 1)
        self.assertEqual(matches_payload["matches"][0]["property"]["title"], "Bonanjo City Loft")

    def test_authenticated_writes_persist(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        self.assertEqual(login.status, HTTPStatus.CREATED)
        token = str(login.body_json()["token"])

        created = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            body={
                "title": "Akwa Night Tower",
                "summary": "Prime city-center residence.",
                "city": "Douala",
                "country": "Cameroon",
                "price_min": 260000,
                "price_max": 340000,
                "property_type": "apartment",
            },
        )
        self.assertEqual(created.status, HTTPStatus.CREATED)
        property_id = created.body_json()["property"]["id"]

        property_detail = self.invoke(f"/api/properties/{property_id}", token=token)
        self.assertEqual(property_detail.status, HTTPStatus.OK)
        self.assertEqual(property_detail.body_json()["property"]["title"], "Akwa Night Tower")

        conversation = self.invoke(
            "/api/conversations",
            method="POST",
            token=token,
            body={
                "property_id": property_id,
                "subject": "Visit request",
                "initial_message": "I want a visit on Saturday morning.",
            },
        )
        self.assertEqual(conversation.status, HTTPStatus.CREATED)
        conversation_payload = conversation.body_json()["conversation"]
        self.assertEqual(conversation_payload["message_count"], 1)

        conversation_id = conversation_payload["id"]
        messages = self.invoke(f"/api/conversations/{conversation_id}/messages", token=token)
        self.assertEqual(messages.status, HTTPStatus.OK)
        self.assertEqual(len(messages.body_json()["messages"]), 1)
