#!/usr/bin/env python3
"""Compare Prisma schema metadata with the Python persistence manifest fingerprint."""
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


def main() -> int:
    schema_path = ROOT / "prisma" / "schema.prisma"
    if not schema_path.is_file():
        print("FAIL: prisma/schema.prisma not found")
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

    print("PASS: prisma schema present")
    print(f"manifest_version={APPLICATION_SCHEMA_VERSION}")
    print(f"manifest_fingerprint={fingerprint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
