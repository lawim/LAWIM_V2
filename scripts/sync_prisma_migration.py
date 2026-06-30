#!/usr/bin/env python3
"""Regenerate Prisma migration SQL from schema_ddl (source of truth)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from lawim_v2.schema_ddl import migration_header, postgresql_migration_sql  # noqa: E402

MIGRATION_PATH = ROOT / "prisma" / "migrations" / "20260629120000_init" / "migration.sql"


def main() -> int:
    MIGRATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    MIGRATION_PATH.write_text(postgresql_migration_sql(header=migration_header()), encoding="utf-8")
    print(f"Wrote {MIGRATION_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
