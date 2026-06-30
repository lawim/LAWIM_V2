#!/usr/bin/env python3
"""Reproducible hot-path benchmark for LAWIM_V2."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import tempfile
import time
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _ensure_import_path() -> None:
    code_dir = _repo_root() / "code"
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))


def _bench(label: str, iterations: int, fn) -> dict[str, object]:
    timings: list[float] = []
    fn()
    for _ in range(iterations):
        started = time.perf_counter()
        fn()
        timings.append(time.perf_counter() - started)
    return {
        "label": label,
        "iterations": iterations,
        "mean_ms": round(statistics.fmean(timings) * 1000.0, 3),
        "median_ms": round(statistics.median(timings) * 1000.0, 3),
        "p95_ms": round(statistics.quantiles(timings, n=20)[18] * 1000.0, 3) if len(timings) >= 20 else round(max(timings) * 1000.0, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=50, help="Iterations per hot path")
    args = parser.parse_args(argv)

    _ensure_import_path()

    from lawim_v2.config import AppConfig
    from lawim_v2.db import LawimRepository
    from lawim_v2.services import LawimServices

    with tempfile.TemporaryDirectory() as tempdir:
        root = Path(tempdir)
        db_path = root / "lawim.sqlite3"
        media_path = root / "media"
        repository = LawimRepository(db_path)
        try:
            repository.initialize(seed_demo_data=True)
            config = AppConfig.for_test(db_path=db_path, media_storage_path=media_path)
            services = LawimServices(repository, config)
            admin = repository.get_user_by_email("admin@lawim.local")
            token = repository.create_session(user_id=int(admin["id"]), ttl_seconds=config.session_ttl_seconds)["token"]

            payload = {
                "summary": _bench("repository.summary", args.iterations, repository.summary),
                "properties": _bench("repository.list_properties", args.iterations, lambda: repository.list_properties(limit=10)),
                "conversations": _bench(
                    "services.list_conversations",
                    args.iterations,
                    lambda: services.list_conversations(actor=admin, limit=10),
                ),
                "bootstrap": _bench(
                    "services.bootstrap",
                    args.iterations,
                    lambda: services.bootstrap(token=token),
                ),
                "locations": _bench(
                    "repository.search_locations",
                    args.iterations,
                    lambda: repository.search_locations(query="Douala", limit=10),
                ),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        finally:
            repository.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
