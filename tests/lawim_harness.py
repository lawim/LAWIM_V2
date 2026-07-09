from __future__ import annotations

import atexit
import base64
import io
import json
import os
import sqlite3
import tempfile
import threading
from dataclasses import dataclass
from http import HTTPStatus
from pathlib import Path
from unittest import TestCase

from lawim_v2.config import AppConfig
from lawim_v2.db import LawimRepository
from lawim_v2.rate_limit import AuthRateLimiter
from lawim_v2.server import LawimRequestHandler
from lawim_v2.services import LawimServices


MINIMAL_JPEG_BYTES = (
    b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01"
    b"\x00\x00\xff\xd9"
)


def minimal_jpeg_base64() -> str:
    return base64.b64encode(MINIMAL_JPEG_BYTES).decode("ascii")


_TRUE_VALUES = {"1", "true", "yes", "on"}
_TEST_TEMPLATE_LOCK = threading.Lock()
_TEST_TEMPLATE_REPOSITORY: LawimRepository | None = None
_TEST_TEMPLATE_TEMPDIR: tempfile.TemporaryDirectory[str] | None = None


def _test_mode_enabled() -> bool:
    return os.getenv("LAWIM_TEST_MODE", "").strip().lower() in _TRUE_VALUES


def _cleanup_test_template() -> None:
    global _TEST_TEMPLATE_REPOSITORY, _TEST_TEMPLATE_TEMPDIR
    if _TEST_TEMPLATE_REPOSITORY is not None:
        _TEST_TEMPLATE_REPOSITORY.close()
        _TEST_TEMPLATE_REPOSITORY = None
    if _TEST_TEMPLATE_TEMPDIR is not None:
        _TEST_TEMPLATE_TEMPDIR.cleanup()
        _TEST_TEMPLATE_TEMPDIR = None


atexit.register(_cleanup_test_template)


def _test_template_repository() -> LawimRepository:
    global _TEST_TEMPLATE_REPOSITORY, _TEST_TEMPLATE_TEMPDIR
    if _TEST_TEMPLATE_REPOSITORY is not None:
        return _TEST_TEMPLATE_REPOSITORY

    with _TEST_TEMPLATE_LOCK:
        if _TEST_TEMPLATE_REPOSITORY is None:
            template_tempdir = tempfile.TemporaryDirectory(prefix="lawim-test-template-")
            template_db_path = Path(template_tempdir.name) / "lawim.sqlite3"
            repository = LawimRepository(template_db_path)
            repository.initialize(seed_demo_data=True)
            _TEST_TEMPLATE_TEMPDIR = template_tempdir
            _TEST_TEMPLATE_REPOSITORY = repository
    return _TEST_TEMPLATE_REPOSITORY


def _clone_test_template(db_path: Path) -> None:
    template_repository = _test_template_repository()
    with sqlite3.connect(db_path) as clone_connection:
        template_repository.connection.backup(clone_connection)


@dataclass(slots=True)
class TestFixture:
    tempdir: tempfile.TemporaryDirectory[str]
    db_path: Path
    media_path: Path
    repository: LawimRepository
    config: AppConfig
    auth_limiter: AuthRateLimiter


def build_test_fixture() -> TestFixture:
    tempdir = tempfile.TemporaryDirectory()
    db_path = Path(tempdir.name) / "lawim.sqlite3"
    media_path = Path(tempdir.name) / "media"

    test_mode = _test_mode_enabled()
    if test_mode:
        _clone_test_template(db_path)

    repository = LawimRepository(db_path)
    if not test_mode:
        repository.initialize(seed_demo_data=True)

    config = AppConfig.for_test(db_path=db_path, media_storage_path=media_path)
    auth_limiter = AuthRateLimiter(
        max_attempts=config.auth_rate_limit_max,
        window_seconds=config.auth_rate_limit_window_seconds,
    )
    return TestFixture(
        tempdir=tempdir,
        db_path=db_path,
        media_path=media_path,
        repository=repository,
        config=config,
        auth_limiter=auth_limiter,
    )


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
        fixture = build_test_fixture()
        self.tempdir = fixture.tempdir
        self.db_path = fixture.db_path
        self.media_path = fixture.media_path
        self.repository = fixture.repository
        self.config = fixture.config
        self.auth_limiter = fixture.auth_limiter

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
        handler.client_address = ("127.0.0.1", 0)
        handler.auth_limiter = self.auth_limiter
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

    def login(self, *, email: str | None = None, identifier: str | None = None, password: str = "lawim-demo") -> str:
        lookup = identifier or email
        if not lookup:
            raise AssertionError("identifier or email is required")
        response = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"identifier": lookup, "password": password},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED, msg=response.body_text())
        return str(response.body_json()["token"])

    def register(
        self,
        *,
        email: str,
        full_name: str,
        role: str | None = None,
        username: str | None = None,
        phone_e164: str | None = None,
        password: str = "lawim-demo",
        password_confirmation: str | None = None,
        preferred_language: str = "fr",
        accept_terms: bool = True,
        organization_id: int | None = None,
        token: str | None = None,
    ) -> str:
        derived_username = username or email.split("@", 1)[0].replace(".", "_")
        derived_phone = phone_e164 or f"+23769{sum(ord(char) for char in email) % 10_000_000:07d}"
        body: dict[str, object] = {
            "email": email,
            "full_name": full_name,
            "username": derived_username,
            "phone_e164": derived_phone,
            "password": password,
            "password_confirmation": password_confirmation or password,
            "preferred_language": preferred_language,
            "accept_terms": accept_terms,
        }
        if role is not None:
            body["role"] = role
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
        return self.config.max_json_body_bytes
