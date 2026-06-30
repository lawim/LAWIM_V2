#!/usr/bin/env python3
"""Optional PostgreSQL smoke: initialize repository and run SELECT 1."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def main() -> int:
    dsn = os.getenv("LAWIM_TEST_POSTGRES_URL", "").strip()
    if not dsn:
        print("SKIP: LAWIM_TEST_POSTGRES_URL not set")
        return 0

    code_dir = _repo_root() / "code"
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))

    try:
        import pg8000  # noqa: F401
    except ImportError:
        print("SKIP: pg8000 not installed")
        return 0

    from lawim_v2.persistence_adapter import resolve_persistence_adapter

    tempdir = tempfile.TemporaryDirectory()
    fallback = Path(tempdir.name) / "fallback.sqlite3"
    adapter = resolve_persistence_adapter(
        fallback,
        db_driver="postgresql",
        database_url=dsn,
        allow_sqlite_fallback=False,
    )
    repository = adapter.create_repository()
    try:
        repository.initialize(seed_demo_data=True)
        repository.scalar("SELECT 1")
        summary = repository.summary()
        print(f"PostgreSQL smoke OK — organizations={summary['organizations']}")
        return 0
    finally:
        repository.close()
        tempdir.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
