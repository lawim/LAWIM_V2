#!/usr/bin/env python3
"""Compare Prisma schema and migration SQL with the Python persistence manifest."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from lawim_v2.persistence import (  # noqa: E402
    APPLICATION_SCHEMA_VERSION,
    build_application_schema_manifest,
    build_schema_fingerprint,
)
from lawim_v2.schema_ddl import (  # noqa: E402
    extract_sql_statements,
    normalize_sql_statement,
    normalized_ddl_fingerprint,
    POSTGRESQL_INIT_STATEMENTS,
)


def main() -> int:
    schema_path = ROOT / "prisma" / "schema.prisma"
    migration_path = ROOT / "prisma" / "migrations" / "20260629120000_init" / "migration.sql"
    if not schema_path.is_file():
        print("FAIL: prisma/schema.prisma not found")
        return 1
    if not migration_path.is_file():
        print("FAIL: prisma migration SQL not found")
        return 1

    manifest = build_application_schema_manifest()
    fingerprint = build_schema_fingerprint(manifest)
    text = schema_path.read_text(encoding="utf-8")

    checks = [
        ("organizations", "model Organization"),
        ("properties", "model Property"),
        ("media", "model Media"),
        ("notifications", "model Notification"),
        ("schema_meta", "model SchemaMeta"),
    ]
    for table, marker in checks:
        if marker not in text:
            print(f"FAIL: missing Prisma model marker for {table}")
            return 1

    version_match = re.search(r"runtime schema v(\d+)", text)
    if version_match and int(version_match.group(1)) != APPLICATION_SCHEMA_VERSION:
        print("FAIL: Prisma header version mismatch")
        return 1

    migration_text = migration_path.read_text(encoding="utf-8")
    migration_statements = extract_sql_statements(migration_text)
    runtime_statements = tuple(normalize_sql_statement(stmt) for stmt in POSTGRESQL_INIT_STATEMENTS)
    migration_normalized = tuple(normalize_sql_statement(stmt) for stmt in migration_statements)
    if migration_normalized != runtime_statements:
        print("FAIL: Prisma migration SQL drift from schema_ddl.POSTGRESQL_INIT_STATEMENTS")
        for index, (expected, actual) in enumerate(zip(runtime_statements, migration_normalized, strict=False)):
            if expected != actual:
                print(f"  first mismatch at statement {index + 1}")
                print(f"  expected: {expected[:120]}...")
                print(f"  actual:   {actual[:120]}...")
                break
        if len(migration_normalized) != len(runtime_statements):
            print(f"  statement count expected={len(runtime_statements)} actual={len(migration_normalized)}")
        return 1

    ddl_fingerprint = normalized_ddl_fingerprint()
    print("PASS: prisma schema present")
    print("PASS: prisma migration SQL aligned with runtime PostgreSQL DDL")
    print(f"manifest_version={APPLICATION_SCHEMA_VERSION}")
    print(f"manifest_fingerprint={fingerprint}")
    print(f"postgresql_ddl_fingerprint={ddl_fingerprint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
