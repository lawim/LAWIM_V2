from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_SECTIONS = ["users", "professional_profiles", "organizations", "properties", "services", "scenarios", "negative_cases"]
OPTIONAL_SECTIONS = ["property_media", "documents", "appointments", "visits", "search_profiles", "matches", "connections", "conversations", "messages", "consents", "notifications"]
REFERENCE_ONLY_SECTIONS = ["scenarios", "negative_cases"]  # validated but not persisted


def _find_db() -> str:
    paths = [
        os.getenv("LAWIM_DB_PATH", ""),
        "data/runtime/lawim.sqlite3",
        "/app/data/runtime/lawim.sqlite3",
        "/app/data/runtime/conversation/state.sqlite3",
    ]
    for p in paths:
        if p and Path(p).exists():
            return p
    return paths[1] if paths else "data/runtime/lawim.sqlite3"


def _get_conn(db_path: str | None = None):
    path = db_path or _find_db()
    os.makedirs(Path(path).parent, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS demo_registry (
            demo_reference_id TEXT PRIMARY KEY,
            demo_dataset_id TEXT NOT NULL,
            demo_section TEXT NOT NULL,
            object_type TEXT NOT NULL,
            object_id TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(demo_dataset_id, demo_section, demo_reference_id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS demo_properties (
            reference_id TEXT PRIMARY KEY,
            dataset_id TEXT NOT NULL,
            property_id TEXT NOT NULL,
            title TEXT,
            city TEXT,
            district TEXT,
            price REAL,
            property_type TEXT,
            status TEXT,
            owner_id TEXT,
            available INTEGER DEFAULT 1
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS demo_users (
            reference_id TEXT PRIMARY KEY,
            dataset_id TEXT NOT NULL,
            full_name TEXT,
            role TEXT,
            city TEXT,
            profile_status TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS demo_organizations (
            reference_id TEXT PRIMARY KEY,
            dataset_id TEXT NOT NULL,
            name TEXT,
            category TEXT,
            city TEXT
        )
    """)
    return conn


class DemoWorldEngine:
    def __init__(self, db_path: str | None = None):
        self._db_path = db_path
        self._data: dict[str, Any] = {}
        self._dataset_id = "LAWIM_DEMO_WORLD_V1"

    def load_yaml(self, path: str = "demo/reference/LAWIM-DEMO-WORLD-REFERENCE.yaml") -> dict[str, Any]:
        with open(path) as f:
            self._data = yaml.safe_load(f)
        self._dataset_id = self._data.get("dataset", {}).get("id", "LAWIM_DEMO_WORLD_V1")
        return self._data

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self._data:
            errors.append("No data loaded. Call load_yaml() first.")
            return errors
        ds = self._data.get("dataset", {})
        if ds.get("id") != "LAWIM_DEMO_WORLD_V1":
            errors.append(f"Unknown dataset: {ds.get('id')}")
        for sec in REQUIRED_SECTIONS:
            if sec not in self._data:
                errors.append(f"Missing required section: {sec}")
        ids: dict[str, set[str]] = {}
        for sec in REQUIRED_SECTIONS + OPTIONAL_SECTIONS:
            items = self._data.get(sec, [])
            if not isinstance(items, list):
                continue
            for item in items:
                rid = item.get("id") or item.get("reference_id") or item.get("property_id") or ""
                if not rid:
                    continue
                ids.setdefault(sec, set()).add(rid)
        # Verify references
        refs: dict[str, dict[str, Any]] = {}
        for sec in REQUIRED_SECTIONS + OPTIONAL_SECTIONS:
            for item in self._data.get(sec, []):
                rid = item.get("id") or item.get("reference_id") or ""
                if rid:
                    refs[rid] = item
        # Check property owner references
        for p in self._data.get("properties", []):
            oid = p.get("owner_id", "")
            if oid and oid not in refs:
                errors.append(f"Property {p.get('id')} references unknown owner: {oid}")
        # Check professional org references
        for pp in self._data.get("professional_profiles", []):
            oid = pp.get("organization_id", "")
            if oid and oid not in refs:
                errors.append(f"Professional {pp.get('id')} references unknown org: {oid}")
        return errors

    def seed(self, dry_run: bool = False) -> dict[str, int]:
        conn = _get_conn(self._db_path)
        counts: dict[str, int] = {}
        dataset_id = self._dataset_id
        now = datetime.now(timezone.utc).isoformat()

        sections_order = [
            ("cities", "cities"),
            ("users", "demo_users"),
            ("organizations", "demo_organizations"),
            ("professional_profiles", "demo_professionals"),
            ("services", "demo_services"),
            ("properties", "demo_properties"),
            ("property_media", "demo_media"),
            ("documents", "demo_documents"),
            ("appointments", "demo_appointments"),
        ]

        if dry_run:
            for sec_name, _ in sections_order:
                items = self._data.get(sec_name, [])
                counts[sec_name] = len(items) if isinstance(items, list) else 0
            return counts

        for sec_name, table_name in sections_order:
            if sec_name in REFERENCE_ONLY_SECTIONS:
                continue
            items = self._data.get(sec_name, [])
            if not isinstance(items, list):
                continue
            created = 0
            for item in items:
                ref_id = item.get("id") or item.get("reference_id") or ""
                if not ref_id:
                    continue
                existing = conn.execute(
                    "SELECT 1 FROM demo_registry WHERE demo_reference_id=? AND demo_dataset_id=?",
                    (ref_id, dataset_id),
                ).fetchone()
                if existing:
                    continue
                conn.execute(
                    "INSERT OR IGNORE INTO demo_registry (demo_reference_id, demo_dataset_id, demo_section, object_type, object_id, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (ref_id, dataset_id, sec_name, sec_name, ref_id, now),
                )
                created += 1
            counts[sec_name] = created

        conn.commit()
        conn.close()
        return counts

    def verify(self) -> dict[str, Any]:
        conn = _get_conn(self._db_path)
        dataset_id = self._dataset_id
        yaml_counts: dict[str, int] = {}
        db_counts: dict[str, int] = {}
        errors: list[str] = []

        for sec in REQUIRED_SECTIONS + OPTIONAL_SECTIONS:
            yaml_items = self._data.get(sec, [])
            if isinstance(yaml_items, list):
                yaml_counts[sec] = len(yaml_items)

        rows = conn.execute(
            "SELECT demo_section, COUNT(*) as cnt FROM demo_registry WHERE demo_dataset_id=? GROUP BY demo_section",
            (dataset_id,),
        ).fetchall()
        for r in rows:
            db_counts[r["demo_section"]] = r["cnt"]

        for sec in yaml_counts:
            if sec in REFERENCE_ONLY_SECTIONS:
                continue
            yc = yaml_counts[sec]
            dc = db_counts.get(sec, 0)
            if yc != dc:
                errors.append(f"Section {sec}: YAML has {yc}, DB has {dc}")

        conn.close()
        return {
            "dataset_id": dataset_id,
            "yaml_counts": yaml_counts,
            "db_counts": db_counts,
            "errors": errors,
            "valid": len(errors) == 0,
        }

    def reset(self, dry_run: bool = False) -> dict[str, int]:
        conn = _get_conn(self._db_path)
        dataset_id = self._dataset_id
        if dry_run:
            counts = conn.execute(
                "SELECT demo_section, COUNT(*) as cnt FROM demo_registry WHERE demo_dataset_id=? GROUP BY demo_section",
                (dataset_id,),
            ).fetchall()
            conn.close()
            return {r["demo_section"]: r["cnt"] for r in counts}

        deleted = conn.execute(
            "DELETE FROM demo_registry WHERE demo_dataset_id=?", (dataset_id,)
        ).rowcount
        conn.commit()
        conn.close()
        return {"deleted_total": deleted}

    def report(self) -> dict[str, Any]:
        data = self._data
        props = data.get("properties", [])
        cities: dict[str, int] = {}
        types: dict[str, int] = {}
        for p in props:
            cities[p.get("city", "?")] = cities.get(p.get("city", "?"), 0) + 1
            types[p.get("property_type", "?")] = types.get(p.get("property_type", "?"), 0) + 1

        return {
            "dataset": data.get("dataset", {}),
            "counts": {k: len(v) for k, v in data.items() if isinstance(v, list)},
            "cities": cities,
            "property_types": types,
            "scenarios_ready": sum(1 for s in data.get("scenarios", []) if s.get("status") == "READY"),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="LAWIM Demo World Management")
    parser.add_argument("command", choices=["validate", "seed", "verify", "reset", "reseed", "report"])
    parser.add_argument("--dataset", default="LAWIM_DEMO_WORLD_V1")
    parser.add_argument("--db", default=None)
    parser.add_argument("--yaml", default="demo/reference/LAWIM-DEMO-WORLD-REFERENCE.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    engine = DemoWorldEngine(db_path=args.db)
    engine.load_yaml(args.yaml)

    if args.command == "validate":
        errors = engine.validate()
        if errors:
            for e in errors:
                print(f"ERROR: {e}")
            sys.exit(1)
        print("VALIDATION PASSED")
        sys.exit(0)

    elif args.command == "seed":
        counts = engine.seed(dry_run=args.dry_run)
        total = sum(counts.values())
        if args.dry_run:
            print(f"DRY RUN: would create {total} objects")
        else:
            print(f"SEEDED: {total} objects created")
        for sec, cnt in sorted(counts.items()):
            if cnt > 0:
                print(f"  {sec}: {cnt}")
        sys.exit(0)

    elif args.command == "verify":
        result = engine.verify()
        print(f"Dataset: {result['dataset_id']}")
        print(f"YAML:  {json.dumps(result['yaml_counts'], indent=2)}")
        print(f"DB:    {json.dumps(result['db_counts'], indent=2)}")
        if result["errors"]:
            for e in result["errors"]:
                print(f"DIVERGENCE: {e}")
            sys.exit(1)
        print("VERIFY PASSED — YAML and DB match")
        sys.exit(0)

    elif args.command == "reset":
        if not args.dry_run and input("Confirm reset of LAWIM_DEMO_WORLD_V1? (y/N): ").lower() != "y":
            print("Reset cancelled.")
            sys.exit(0)
        result = engine.reset(dry_run=args.dry_run)
        if args.dry_run:
            print(f"DRY RUN: would delete {sum(result.values())} objects")
            for sec, cnt in result.items():
                print(f"  {sec}: {cnt}")
        else:
            print(f"RESET: {result['deleted_total']} objects deleted")
        sys.exit(0)

    elif args.command == "reseed":
        engine.reset(dry_run=False)
        counts = engine.seed(dry_run=False)
        result = engine.verify()
        if result["errors"]:
            for e in result["errors"]:
                print(f"RESEED ERROR: {e}")
            sys.exit(1)
        print(f"RESEED COMPLETE: {sum(counts.values())} objects, verify PASSED")
        sys.exit(0)

    elif args.command == "report":
        r = engine.report()
        total_yaml = sum(r['counts'].values())
        persistable = sum(v for k, v in r['counts'].items() if k not in REFERENCE_ONLY_SECTIONS)
        ref_only = sum(v for k, v in r['counts'].items() if k in REFERENCE_ONLY_SECTIONS)
        print(f"LAWIM Demo World Report")
        print(f"  Dataset: {r['dataset'].get('id')} v{r['dataset'].get('version')}")
        print(f"  Status: {r['dataset'].get('status')}")
        print(f"  YAML entities: {total_yaml}")
        print(f"  Persistable entities: {persistable}")
        print(f"  Reference-only entities: {ref_only} ({', '.join(k for k in r['counts'] if k in REFERENCE_ONLY_SECTIONS)})")
        for sec, cnt in sorted(r['counts'].items()):
            tag = " [REFERENCE_ONLY]" if sec in REFERENCE_ONLY_SECTIONS else ""
            print(f"  {sec}: {cnt}{tag}")
        print(f"  Cities: {json.dumps(r['cities'])}")
        print(f"  Property types: {json.dumps(r['property_types'])}")
        print(f"  Scenarios READY: {r['scenarios_ready']}{' [REFERENCE_ONLY]' if 'scenarios' in REFERENCE_ONLY_SECTIONS else ''}")
        sys.exit(0)


if __name__ == "__main__":
    main()
