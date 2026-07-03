#!/usr/bin/env python3
"""Reproducible API latency benchmark for critical LAWIM_V2 routes."""

from __future__ import annotations

import errno
import io
import json
import os
import socket
import statistics
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _ensure_import_path() -> None:
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

    def _handle_post(self) -> None:
        self._handler_cls._handle_post(self)

    def do_GET(self) -> None:
        self._handler_cls.do_GET(self)

    def do_POST(self) -> None:
        self._handler_cls.do_POST(self)

    def __getattr__(self, name: str):
        attr = getattr(self._handler_cls, name)
        if callable(attr):
            return attr.__get__(self, type(self))
        return attr


@dataclass(frozen=True, slots=True)
class ProbeResult:
    route: str
    samples_ms: tuple[float, ...]

    @property
    def p50(self) -> float:
        return statistics.median(self.samples_ms) if self.samples_ms else 0.0

    @property
    def p95(self) -> float:
        if not self.samples_ms:
            return 0.0
        ordered = sorted(self.samples_ms)
        index = min(len(ordered) - 1, int(round(0.95 * (len(ordered) - 1))))
        return ordered[index]


def _fetch(base: str, path: str, *, headers: dict[str, str] | None = None) -> tuple[int, bytes]:
    request = urllib.request.Request(f"{base}{path}", headers=headers or {})
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.status, response.read()


def _fetch_direct(repository, config, path: str, *, method: str = "GET", headers: dict[str, str] | None = None, body: dict[str, object] | None = None) -> tuple[int, dict[str, str], bytes]:
    request_headers: dict[str, str] = dict(headers or {})
    payload = b""
    if body is not None:
        payload = json.dumps(body).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
        request_headers.setdefault("Content-Length", str(len(payload)))
    handler = _DirectHandler(repository, config, path, method=method, headers=request_headers, body=payload)
    if method == "POST":
        handler.do_POST()
    elif method == "GET":
        handler.do_GET()
    else:  # pragma: no cover
        raise AssertionError(f"Unsupported method: {method}")
    status = int(handler.status or 0)
    headers_out = {key.lower(): value for key, value in handler.response_headers.items()}
    body_out = handler.wfile.getvalue()
    return status, headers_out, body_out


def _run_benchmark_http(*, iterations: int = 20) -> dict[str, object]:
    _ensure_import_path()
    from lawim_v2.config import AppConfig
    from lawim_v2.server import create_server

    port = _free_port()
    tempdir = tempfile.TemporaryDirectory()
    root = Path(tempdir.name)
    config = AppConfig.for_test(
        db_path=root / "lawim.sqlite3",
        media_storage_path=root / "media",
        host="127.0.0.1",
        port=port,
        log_level="warning",
        public_base_url=f"http://127.0.0.1:{port}",
    )
    config.validate()
    config.ensure_runtime_dir()
    server = create_server(config)
    thread = threading.Thread(target=server.serve_forever, name="lawim-benchmark", daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"

    probes = (
        "/healthz",
        "/readyz",
        "/api/health",
        "/api/properties?limit=10",
        "/api/bootstrap",
    )
    results: list[dict[str, object]] = []
    try:
        login_status, login_body = _post_json(
            base,
            "/api/auth/login",
            {"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        token = ""
        if login_status == 201:
            token = json.loads(login_body.decode("utf-8")).get("token", "")
        auth_headers = {"Authorization": f"Bearer {token}"} if token else {}

        for route in probes:
            samples: list[float] = []
            headers = auth_headers if route.startswith("/api/") and route != "/api/health" else None
            for _ in range(iterations):
                started = time.perf_counter()
                status, _ = _fetch(base, route, headers=headers)
                elapsed_ms = (time.perf_counter() - started) * 1000.0
                if status >= 400:
                    raise RuntimeError(f"{route} returned HTTP {status}")
                samples.append(elapsed_ms)
            probe = ProbeResult(route=route, samples_ms=tuple(samples))
            results.append(
                {
                    "route": route,
                    "iterations": iterations,
                    "p50_ms": round(probe.p50, 2),
                    "p95_ms": round(probe.p95, 2),
                    "max_ms": round(max(samples), 2),
                }
            )
        return {"base": base, "iterations": iterations, "routes": results}
    finally:
        server.shutdown()
        server.server_close()
        server.repository.close()  # type: ignore[attr-defined]
        thread.join(timeout=5)
        tempdir.cleanup()


def _run_benchmark_direct(*, iterations: int = 20) -> dict[str, object]:
    _ensure_import_path()
    from lawim_v2.config import AppConfig
    from lawim_v2.persistence_adapter import resolve_persistence_adapter

    tempdir = tempfile.TemporaryDirectory()
    root = Path(tempdir.name)
    config = AppConfig.for_test(
        db_path=root / "lawim.sqlite3",
        media_storage_path=root / "media",
        host="127.0.0.1",
        port=3000,
        log_level="warning",
        public_base_url="http://127.0.0.1:3000",
    )
    config.validate()
    config.ensure_runtime_dir()
    adapter = resolve_persistence_adapter(
        config.db_path,
        db_driver=config.db_driver,
        database_url=config.database_url,
        allow_sqlite_fallback=config.db_fallback,
    )
    repository = adapter.create_repository()
    repository.initialize(seed_demo_data=config.seed_demo_data)
    base = "direct://lawim-runtime"

    probes = (
        "/healthz",
        "/readyz",
        "/api/health",
        "/api/properties?limit=10",
        "/api/bootstrap",
    )
    results: list[dict[str, object]] = []
    try:
        status, login_headers, login_body = _fetch_direct(
            repository,
            config,
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        token = ""
        if status == 201:
            token = json.loads(login_body.decode("utf-8")).get("token", "")
        auth_headers = {"Authorization": f"Bearer {token}"} if token else {}

        for route in probes:
            samples: list[float] = []
            headers = auth_headers if route.startswith("/api/") and route != "/api/health" else None
            for _ in range(iterations):
                started = time.perf_counter()
                status, _, _ = _fetch_direct(repository, config, route, headers=headers)
                elapsed_ms = (time.perf_counter() - started) * 1000.0
                if status >= 400:
                    raise RuntimeError(f"{route} returned HTTP {status}")
                samples.append(elapsed_ms)
            probe = ProbeResult(route=route, samples_ms=tuple(samples))
            results.append(
                {
                    "route": route,
                    "iterations": iterations,
                    "p50_ms": round(probe.p50, 2),
                    "p95_ms": round(probe.p95, 2),
                    "max_ms": round(max(samples), 2),
                }
            )
        return {"base": base, "iterations": iterations, "routes": results}
    finally:
        repository.close()
        tempdir.cleanup()


def run_benchmark(*, iterations: int = 20) -> dict[str, object]:
    if _test_mode_enabled():
        return _run_benchmark_direct(iterations=iterations)
    try:
        return _run_benchmark_http(iterations=iterations)
    except PermissionError:
        return _run_benchmark_direct(iterations=iterations)
    except OSError as exc:
        if exc.errno in {errno.EPERM, errno.EACCES}:
            return _run_benchmark_direct(iterations=iterations)
        raise


def _post_json(base: str, path: str, payload: dict[str, object]) -> tuple[int, bytes]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{base}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def main() -> int:
    report = run_benchmark()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    slow = [row for row in report["routes"] if row["p95_ms"] > 250.0]  # type: ignore[index]
    if slow:
        print("WARN: routes above 250ms p95:", ", ".join(str(row["route"]) for row in slow))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
