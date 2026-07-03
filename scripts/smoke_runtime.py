#!/usr/bin/env python3
"""Runtime smoke test: start server, probe endpoints, shut down cleanly."""

from __future__ import annotations

import errno
import io
import json
import os
import socket
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _ensure_import_path() -> None:
    if os.environ.get("LAWIM_SMOKE_USE_SOURCE_PATH", "1").strip().lower() in {"0", "false", "no", "off"}:
        return
    code_dir = _repo_root() / "code"
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))


_TRUE_VALUES = {"1", "true", "yes", "on"}


def _test_mode_enabled() -> bool:
    if os.environ.get("LAWIM_TEST_MODE", "").strip().lower() in _TRUE_VALUES:
        return True
    if os.environ.get("APP_ENV", "").strip().lower() == "test":
        return True
    if "pytest" in sys.modules or "pytest.__main__" in sys.modules:
        return True
    if "unittest.__main__" in sys.modules:
        return True
    return False


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class _DirectHandler:
    def __init__(
        self,
        repository,
        config,
        path: str,
        *,
        method: str = "GET",
        headers: dict[str, str] | None = None,
        body: bytes = b"",
    ) -> None:
        from lawim_v2.rate_limit import AuthRateLimiter
        from lawim_v2.server import LawimRequestHandler
        from lawim_v2.services import LawimServices

        self.repository = repository
        self.config = config
        self.services = LawimServices(repository, config)
        self.path = path
        self.command = method
        self.headers = {str(key): str(value) for key, value in (headers or {}).items()}
        self.rfile = io.BytesIO(body)
        self.wfile = io.BytesIO()
        self.status: int | None = None
        self.response_headers: dict[str, str] = {}
        self.client_address = ("127.0.0.1", 0)
        self.request_version = "HTTP/1.1"
        self.server_version = LawimRequestHandler.server_version
        self.protocol_version = LawimRequestHandler.protocol_version
        self.auth_limiter = AuthRateLimiter(
            max_attempts=config.auth_rate_limit_max,
            window_seconds=config.auth_rate_limit_window_seconds,
        )
        self._handler_cls = LawimRequestHandler
        self.send_response = lambda status: setattr(self, "status", int(status))
        self.send_header = lambda key, value: self.response_headers.__setitem__(key, value)
        self.end_headers = lambda: None

    def _handle_request(self, handler) -> None:
        self._handler_cls._handle_request(self, handler)

    def _handle_get(self) -> None:
        self._handler_cls._handle_get(self)

    def do_GET(self) -> None:
        self._handler_cls.do_GET(self)

    def __getattr__(self, name: str):
        attr = getattr(self._handler_cls, name)
        if callable(attr):
            return attr.__get__(self, type(self))
        return attr


@dataclass(frozen=True, slots=True)
class SmokeResult:
    ok: bool
    message: str


def _run_smoke_http(*, host: str = "127.0.0.1", timeout: float = 5.0) -> SmokeResult:
    _ensure_import_path()

    from lawim_v2.config import AppConfig
    from lawim_v2.server import create_server

    port = _free_port()
    tempdir = tempfile.TemporaryDirectory()
    root = Path(tempdir.name)
    db_path = root / "lawim.sqlite3"
    media_path = root / "media"

    config = AppConfig.for_test(
        db_path=db_path,
        media_storage_path=media_path,
        host=host,
        port=port,
        log_level="warning",
        public_base_url=f"http://{host}:{port}",
    )
    config.validate()
    config.ensure_runtime_dir()

    server = create_server(config)
    thread = threading.Thread(target=server.serve_forever, name="lawim-smoke-server", daemon=True)
    thread.start()

    base = f"http://{host}:{port}"

    def fetch(path: str, *, expected_status: int | None = None) -> tuple[int, dict[str, str], bytes]:
        request = urllib.request.Request(f"{base}{path}", method="GET")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status = response.status
                headers = {key.lower(): value for key, value in response.headers.items()}
                body = response.read()
        except urllib.error.HTTPError as exc:
            status = exc.code
            headers = {key.lower(): value for key, value in exc.headers.items()}
            body = exc.read()
        if expected_status is not None and status != expected_status:
            raise RuntimeError(f"{path} returned HTTP {status}, expected {expected_status}")
        return status, headers, body

    try:
        status, headers, body = fetch("/healthz")
        if status != 200 or body.strip() != b"ok":
            return SmokeResult(False, f"/healthz returned unexpected response: {status!r} {body!r}")

        status, _, body = fetch("/readyz")
        if status != 200:
            return SmokeResult(False, f"/readyz returned HTTP {status}")
        readiness = json.loads(body.decode("utf-8"))
        if readiness.get("status") != "ready":
            return SmokeResult(False, f"/readyz payload invalid: {readiness!r}")

        status, headers, body = fetch("/api/health")
        if status != 200:
            return SmokeResult(False, f"/api/health returned HTTP {status}")
        health = json.loads(body.decode("utf-8"))
        if health.get("status") != "ok":
            return SmokeResult(False, f"/api/health payload invalid: {health!r}")

        for header in ("x-content-type-options", "x-frame-options"):
            if header not in headers:
                return SmokeResult(False, f"/api/health missing security header {header}")

        status, _, body = fetch("/")
        if status != 200 or (b"LAWIM" not in body and b"lawim" not in body.lower()):
            return SmokeResult(False, "Static UI root did not return expected content")

        status, _, body = fetch("/app.js")
        if status != 200 or b"function" not in body:
            return SmokeResult(False, "/app.js did not return JavaScript")

        status, _, body = fetch("/api/properties?limit=1")
        if status != 200:
            return SmokeResult(False, f"/api/properties returned HTTP {status}")
        properties_payload = json.loads(body.decode("utf-8"))
        if "properties" not in properties_payload:
            return SmokeResult(False, "/api/properties payload missing properties key")

        status, headers, _ = fetch("/api/me", expected_status=401)
        if "www-authenticate" not in headers:
            return SmokeResult(False, "/api/me did not require authentication")

        return SmokeResult(True, f"Smoke OK on {base}")
    except Exception as exc:  # pragma: no cover - surfaced to caller
        return SmokeResult(False, str(exc))
    finally:
        server.shutdown()
        server.server_close()
        server.repository.close()  # type: ignore[attr-defined]
        thread.join(timeout=timeout)
        tempdir.cleanup()


def _run_smoke_direct(*, host: str = "127.0.0.1") -> SmokeResult:
    _ensure_import_path()

    from lawim_v2.config import AppConfig
    from lawim_v2.db import LawimRepository
    from lawim_v2.persistence_adapter import resolve_persistence_adapter

    tempdir = tempfile.TemporaryDirectory()
    root = Path(tempdir.name)
    db_path = root / "lawim.sqlite3"
    media_path = root / "media"
    config = AppConfig.for_test(
        db_path=db_path,
        media_storage_path=media_path,
        host=host,
        port=3000,
        log_level="warning",
        public_base_url=f"http://{host}:3000",
    )
    config.validate()
    config.ensure_runtime_dir()

    adapter = resolve_persistence_adapter(
        config.db_path,
        db_driver=config.db_driver,
        database_url=config.database_url,
        allow_sqlite_fallback=config.db_fallback,
    )
    repository: LawimRepository = adapter.create_repository()
    repository.initialize(seed_demo_data=config.seed_demo_data)

    def fetch(path: str, *, expected_status: int | None = None) -> tuple[int, dict[str, str], bytes]:
        handler = _DirectHandler(repository, config, path)
        handler.do_GET()
        status = int(handler.status or 0)
        headers = {key.lower(): value for key, value in handler.response_headers.items()}
        body = handler.wfile.getvalue()
        if expected_status is not None and status != expected_status:
            raise RuntimeError(f"{path} returned HTTP {status}, expected {expected_status}")
        return status, headers, body

    try:
        status, headers, body = fetch("/healthz")
        if status != 200 or body.strip() != b"ok":
            return SmokeResult(False, f"/healthz returned unexpected response: {status!r} {body!r}")

        status, _, body = fetch("/readyz")
        if status != 200:
            return SmokeResult(False, f"/readyz returned HTTP {status}")
        readiness = json.loads(body.decode("utf-8"))
        if readiness.get("status") != "ready":
            return SmokeResult(False, f"/readyz payload invalid: {readiness!r}")

        status, headers, body = fetch("/api/health")
        if status != 200:
            return SmokeResult(False, f"/api/health returned HTTP {status}")
        health = json.loads(body.decode("utf-8"))
        if health.get("status") != "ok":
            return SmokeResult(False, f"/api/health payload invalid: {health!r}")

        for header in ("x-content-type-options", "x-frame-options"):
            if header not in headers:
                return SmokeResult(False, f"/api/health missing security header {header}")

        status, _, body = fetch("/")
        if status != 200 or (b"LAWIM" not in body and b"lawim" not in body.lower()):
            return SmokeResult(False, "Static UI root did not return expected content")

        status, _, body = fetch("/app.js")
        if status != 200 or b"function" not in body:
            return SmokeResult(False, "/app.js did not return JavaScript")

        status, _, body = fetch("/api/properties?limit=1")
        if status != 200:
            return SmokeResult(False, f"/api/properties returned HTTP {status}")
        properties_payload = json.loads(body.decode("utf-8"))
        if "properties" not in properties_payload:
            return SmokeResult(False, "/api/properties payload missing properties key")

        status, headers, _ = fetch("/api/me", expected_status=401)
        if "www-authenticate" not in headers:
            return SmokeResult(False, "/api/me did not require authentication")

        return SmokeResult(True, "Smoke OK in direct test mode")
    except Exception as exc:  # pragma: no cover - surfaced to caller
        return SmokeResult(False, str(exc))
    finally:
        repository.close()
        tempdir.cleanup()


def run_smoke(*, host: str = "127.0.0.1", timeout: float = 5.0) -> SmokeResult:
    if _test_mode_enabled():
        return _run_smoke_direct(host=host)
    try:
        return _run_smoke_http(host=host, timeout=timeout)
    except PermissionError:
        return _run_smoke_direct(host=host)
    except OSError as exc:
        if exc.errno in {errno.EPERM, errno.EACCES}:
            return _run_smoke_direct(host=host)
        raise


def main() -> int:
    result = run_smoke()
    print(result.message)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
