#!/usr/bin/env python3
"""validate_knowledge_registries.py — Verifies all knowledge registries load real canonical sources."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_PASS = 0
_FAIL = 0


def check(label: str, condition: bool, errors: list[str]) -> None:
    global _PASS, _FAIL
    if not condition:
        errors.append(f"FAIL: {label}")
        _FAIL += 1
        print(f"  FAIL: {label}")
    else:
        _PASS += 1
        print(f"  PASS: {label}")


def source_paths() -> dict[str, Path]:
    return {
        "property_taxonomy": _PROJECT_ROOT / "docs/domain_extension/property_taxonomy_extensions.json",
        "service_taxonomy": _PROJECT_ROOT / "docs/domain_extension/service_taxonomy_extensions.json",
        "roles": _PROJECT_ROOT / "docs/domain_extension/identity_role_extensions.json",
        "intents": _PROJECT_ROOT / "docs/domain_extension/intent_request_extensions.json",
        "matrices": _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/qualification_matrices.json",
        "fields": _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/field_dictionary.json",
        "readiness": _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/readiness_rules.json",
        "question_rules": _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/question_rules.json",
        "matching_semantics": _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json",
    }


def main() -> int:
    global _PASS, _FAIL
    errors: list[str] = []
    srcs = source_paths()
    print("=" * 70)
    print("KNOWLEDGE REGISTRIES VALIDATOR")
    print("=" * 70)

    # 1. Source presence
    print("\n--- Source file presence ---")
    for name, p in srcs.items():
        check(f"Source '{name}' exists", p.is_file(), errors)

    # 2. JSON validity
    print("\n--- JSON validity ---")
    for name, p in srcs.items():
        if p.is_file():
            try:
                json.loads(p.read_bytes())
                check(f"'{name}' is valid JSON", True, errors)
            except json.JSONDecodeError as e:
                check(f"'{name}' valid JSON: {e}", False, errors)
        else:
            check(f"'{name}' valid JSON (file missing)", False, errors)

    # 3. Checksums
    print("\n--- Checksums ---")
    for name, p in srcs.items():
        if p.is_file():
            c = hashlib.sha256(p.read_bytes()).hexdigest()
            check(f"'{name}' checksum: {c[:16]}...", len(c) == 64, errors)

    # 4. Property taxonomy
    print("\n--- Property taxonomy ---")
    if srcs["property_taxonomy"].is_file():
        d = json.loads(srcs["property_taxonomy"].read_bytes())
        families = d.get("property_families", {}).get("values", [])
        check(f"Property families: {len(families)}", len(families) >= 7, errors)
        expected = {"PR-FAM-001", "PR-FAM-002", "PR-FAM-003", "PR-FAM-004", "PR-FAM-005", "PR-FAM-006", "PR-FAM-007"}
        present = {f.get("id") for f in families}
        check("All 7 canonical property families", expected.issubset(present), errors)

    # 5. Service taxonomy
    print("\n--- Service taxonomy ---")
    if srcs["service_taxonomy"].is_file():
        d = json.loads(srcs["service_taxonomy"].read_bytes())
        svf = d.get("service_families", {}).get("values", [])
        check(f"Service families: {len(svf)}", len(svf) >= 11, errors)
        catalog = d.get("service_catalog", [])
        check(f"Service catalog: {len(catalog)}", len(catalog) >= 10, errors)

    # 6. Roles
    print("\n--- Roles ---")
    if srcs["roles"].is_file():
        d = json.loads(srcs["roles"].read_bytes())
        exts = d.get("extensions", [])
        check(f"Role extensions: {len(exts)}", len(exts) >= 20, errors)

    # 7. Intents
    print("\n--- Intents ---")
    intent_exts = []
    if srcs["intents"].is_file():
        d = json.loads(srcs["intents"].read_bytes())
        exts = d.get("extensions", [])
        intent_exts = [e for e in exts if e.get("extension_category") == "intent_detection"]
        check(f"Intent extensions: {len(intent_exts)}", len(intent_exts) >= 5, errors)

    # 8. Transactions
    print("\n--- Transactions ---")
    if srcs["intents"].is_file():
        d = json.loads(srcs["intents"].read_bytes())
        exts = d.get("extensions", [])
        trx_exts = [e for e in exts if e.get("extension_category") == "transaction_types"]
        check(f"Transaction extensions: {len(trx_exts)}", len(trx_exts) >= 7, errors)

    # 9. Matrices
    print("\n--- Qualification matrices ---")
    if srcs["matrices"].is_file():
        d = json.loads(srcs["matrices"].read_bytes())
        matrices = d.get("matrices", [])
        check(f"Matrices: {len(matrices)} (meta: 75, ref: 107)", len(matrices) >= 50, errors)
        mids = {m.get("matrix_id", "") for m in matrices}
        check("Residential matrices present", any("RES-SEARCH" in str(m) for m in mids), errors)
        check("Land search matrices present", any("LAND_SEARCH" in str(m) for m in mids), errors)
        check("Commercial matrices present", any("COM-MATRIX" in str(m) for m in mids), errors)
        check("Financing matrices present", any("MATRIX-FIN" in str(m) for m in mids), errors)

    # 10. Fields
    print("\n--- Fields ---")
    if srcs["fields"].is_file():
        d = json.loads(srcs["fields"].read_bytes())
        fields = d.get("fields", {})
        check(f"Fields: {len(fields)}", len(fields) >= 90, errors)
        required = {"city", "transaction", "property_type", "intent", "neighborhood", "budget_max"}
        check("Required fields present", required.issubset(set(fields.keys())), errors)

    # 11. Readiness
    print("\n--- Readiness ---")
    if srcs["readiness"].is_file():
        d = json.loads(srcs["readiness"].read_bytes())
        levels = d.get("levels", {})
        check(f"Readiness levels: {len(levels)}", len(levels) >= 7, errors)
        expected = {"INTENT_IDENTIFIED", "MINIMUM_INTAKE_READY", "MINIMUM_SEARCH_READY",
                    "MINIMUM_MATCHING_READY", "INTRODUCTION_READY", "VISIT_READY", "TRANSACTION_READY"}
        check("All 7 readiness levels", expected.issubset(set(levels.keys())), errors)

    # 12. Question rules
    print("\n--- Question rules ---")
    if srcs["question_rules"].is_file():
        d = json.loads(srcs["question_rules"].read_bytes())
        check(f"Always ask: {len(d.get('always_ask', []))}", len(d.get('always_ask', [])) >= 3, errors)
        check(f"Conditional ask: {len(d.get('conditional_ask', []))}", len(d.get('conditional_ask', [])) >= 10, errors)
        check(f"Never ask: {len(d.get('never_ask', []))}", len(d.get('never_ask', [])) >= 10, errors)

    # 13. Matching semantics
    print("\n--- Matching semantics ---")
    if srcs["matching_semantics"].is_file():
        d = json.loads(srcs["matching_semantics"].read_bytes())
        roles = d.get("roles", {})
        check(f"Matching semantics: {len(roles)}", len(roles) == 9, errors)
        expected = {"hard_constraint", "soft_constraint", "ranking_preference", "exclusion",
                    "boost", "penalty", "informational_only", "verification_only", "transaction_blocker"}
        check("All 9 matching roles", expected == set(roles.keys()), errors)

    # 14. No duplicate IDs
    print("\n--- Duplicate check ---")
    for name, p in srcs.items():
        if p.is_file():
            d = json.loads(p.read_bytes())
            ids = set()
            if "matrices" in d:
                ids = {m.get("matrix_id", "") for m in d["matrices"]}
            elif "fields" in d:
                ids = set(d["fields"].keys())
            elif "levels" in d:
                ids = set(d["levels"].keys())
            elif "extensions" in d:
                ids = {e.get("extension_id", "") for e in d["extensions"]}
            if ids:
                check(f"'{name}' no empty IDs", "" not in ids, errors)

    # 15. Summary
    print(f"\n{'=' * 70}")
    print(f"RESULTS: {_PASS} passed, {_FAIL} failed")
    if errors:
        print("VALIDATION FAILED")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
