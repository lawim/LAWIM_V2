from __future__ import annotations

import io
import json
import tempfile
from http import HTTPStatus
from pathlib import Path
from unittest import TestCase

from lawim_v2.config import AppConfig
from lawim_v2.db import LawimRepository
from lawim_v2.server import LawimRequestHandler, MAX_JSON_BODY_BYTES
from lawim_v2.services import LawimServices


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
        self.services = LawimServices(repository, config)
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


class LawimTestHarness(TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tempdir.name) / "lawim.sqlite3"
        self.media_path = Path(self.tempdir.name) / "media"
        self.repository = LawimRepository(self.db_path)
        self.repository.initialize(seed_demo_data=True)
        self.config = AppConfig(
            host="127.0.0.1",
            port=3000,
            db_path=self.db_path,
            db_driver="sqlite",
            database_url="postgresql://lawim:lawim@localhost:5432/lawim_v2",
            db_fallback=True,
            app_env="test",
            stack_profile="test",
            log_level="debug",
            public_base_url="http://127.0.0.1:3000",
            secret_provider="external",
            seed_demo_data=True,
            session_ttl_seconds=3600,
            media_storage_path=self.media_path,
            max_upload_bytes=5 * 1024 * 1024,
            geocoding_provider="local",
            geocoding_base_url="https://nominatim.openstreetmap.org/search",
            geocoding_api_key=None,
            cdn_base_url=None,
            metrics_enabled=True,
        )

    def tearDown(self) -> None:
        self.repository.close()
        self.tempdir.cleanup()

    def invoke(
        self,
        path: str,
        *,
        method: str = "GET",
        body: dict[str, object] | None = None,
        raw_body: bytes | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
    ) -> DummyHandler:
        request_headers: dict[str, str] = dict(headers or {})
        payload = b""
        if raw_body is not None:
            payload = raw_body
            request_headers.setdefault("Content-Length", str(len(payload)))
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            request_headers.setdefault("Content-Length", str(len(payload)))
            request_headers.setdefault("Content-Type", "application/json")
        if token:
            request_headers["Authorization"] = f"Bearer {token}"

        handler = DummyHandler(self.repository, self.config, path, method=method, headers=request_headers, body=payload)
        if method == "GET":
            handler.do_GET()
        elif method == "POST":
            handler.do_POST()
        elif method == "PUT":
            handler.do_PUT()
        elif method == "PATCH":
            handler.do_PATCH()
        elif method == "DELETE":
            handler.do_DELETE()
        else:  # pragma: no cover
            raise AssertionError(f"Unsupported method: {method}")
        return handler

    def login(self, *, email: str, password: str = "lawim-demo") -> str:
        response = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": email, "password": password},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED, msg=response.body_text())
        return str(response.body_json()["token"])

    def register(
        self,
        *,
        email: str,
        full_name: str,
        role: str = "owner",
        password: str = "lawim-demo",
        organization_id: int | None = None,
        token: str | None = None,
    ) -> str:
        body: dict[str, object] = {
            "email": email,
            "full_name": full_name,
            "role": role,
            "password": password,
        }
        if organization_id is not None:
            body["organization_id"] = organization_id
        response = self.invoke("/api/auth/register", method="POST", body=body, token=token)
        self.assertEqual(response.status, HTTPStatus.CREATED, msg=response.body_text())
        return str(response.body_json()["token"])

    def assert_error_shape(self, response: DummyHandler) -> dict[str, object]:
        payload = response.body_json()
        self.assertIn("error", payload)
        error = payload["error"]
        self.assertIsInstance(error, dict)
        self.assertIn("code", error)
        self.assertIn("message", error)
        return error  # type: ignore[return-value]

    @property
    def max_json_body_bytes(self) -> int:
        return MAX_JSON_BODY_BYTES
