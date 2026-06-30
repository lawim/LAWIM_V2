#!/usr/bin/env python3
"""Reproducible API latency benchmark for critical LAWIM_V2 routes."""

from __future__ import annotations

import json
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


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


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


def run_benchmark(*, iterations: int = 20) -> dict[str, object]:
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
