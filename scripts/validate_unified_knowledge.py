#!/usr/bin/env python3
"""Validate the unified knowledge repository in LAWIM_V2/knowledge_unified/."""

import json
import os
import sys
from pathlib import Path

BASE = Path("/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/knowledge_unified")
REQUIRED_DIRS = ["sources", "geography", "qualification", "real_estate", "language",
                 "matching", "commercial", "professionals", "legal_and_documents",
                 "validation", "schemas"]

REQUIRED_FILES = {
    "sources": ["SOURCE_INVENTORY.md"],
    "geography": ["cities.json", "neighborhoods.json", "aliases.json",
                  "proximity_rules.json", "geographic_scoring.md"],
    "matching": ["matching_dimensions.json", "scoring_rules.json",
                 "exclusion_rules.json", "ranking_rules.json",
                 "geographic_weights.json", "matching_explanations.md"],
    "qualification": ["user_typologies.json", "intentions.json",
                      "property_search_matrices.json", "professional_search_matrices.json",
                      "seller_matrices.json", "owner_matrices.json",
                      "investor_matrices.json", "qualification_rules.md"],
    "language": ["common_expressions.json", "cameroon_expressions.json",
                 "spelling_variants.json", "abbreviations.json",
                 "amount_expressions.json", "intent_phrases.json"],
    "commercial": ["negotiation_techniques.md", "objection_handling.md",
                   "follow_up_strategies.md", "closing_techniques.md",
                   "conversation_tone.md"],
}

SENSITIVE_KEYWORDS = [
    "password", "secret", "api_key", "api_key", "token", "jwt",
    "private_key", "-----BEGIN", "DATABASE_URL", "JWT_SECRET",
    "process.env", "process.env", ".env",
]

FORBIDDEN_CODE_PATTERNS = [
    "import ", "module.exports", "export default", "function ",
    "class ", "interface ", "type ", "require(", "prisma.",
    "prisma.", "schema.prisma",
]


def check_dirs():
    missing_dirs = []
    for d in REQUIRED_DIRS:
        if not (BASE / d).is_dir():
            missing_dirs.append(d)
    return missing_dirs


def check_required_files():
    missing = []
    present = []
    for subdir, files in REQUIRED_FILES.items():
        for f in files:
            path = BASE / subdir / f
            if path.exists():
                present.append(str(path.relative_to(BASE)))
            else:
                missing.append(str(path.relative_to(BASE)))
    return present, missing


def validate_json(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return True, data, None
    except json.JSONDecodeError as e:
        return False, None, str(e)
    except Exception as e:
        return False, None, str(e)


def check_no_duplicate_ids(data, path_label):
    """Check for duplicate IDs in JSON objects that have 'id' or 'intent_id' fields."""
    ids = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for key in ("id", "intent_id"):
                    if key in item:
                        ids.append(item[key])
    elif isinstance(data, dict):
        for key in ("intent_id",):
            if key in data and isinstance(data[key], str):
                ids.append(data[key])
        for k, v in data.items():
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        for idkey in ("id", "intent_id"):
                            if idkey in item:
                                ids.append(item[idkey])
    dupes = [x for x in ids if ids.count(x) > 1]
    return list(set(dupes))


def check_sensitive_content(content, path_label):
    issues = []
    for keyword in SENSITIVE_KEYWORDS:
        if keyword.lower() in content.lower():
            issues.append(f"Sensitive keyword '{keyword}' found in {path_label}")
    for pattern in FORBIDDEN_CODE_PATTERNS:
        if pattern in content:
            issues.append(f"Code pattern '{pattern}' found in {path_label}")
    return issues


def check_string_refs(data, known_keys, path=""):
    issues = []
    if isinstance(data, dict):
        for k, v in data.items():
            subpath = f"{path}.{k}" if path else k
            if k.endswith("_id") or k.endswith("reference") or k == "source":
                if isinstance(v, str) and v and not v.startswith("LAWIM") and not v.startswith("CM-"):
                    if v not in known_keys and not any(kn in v for kn in ["LAWIM", "KNOWLEDGE", "Module"]):
                        pass
            issues.extend(check_string_refs(v, known_keys, subpath))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            issues.extend(check_string_refs(item, known_keys, f"{path}[{i}]"))
    return issues


def main():
    print("=" * 60)
    print("LAWIM V2 Unified Knowledge Repository - Validation")
    print("=" * 60)

    errors = []
    warnings = []
    total_file_count = 0

    # Check directories
    missing_dirs = check_dirs()
    if missing_dirs:
        errors.append(f"Missing required directories: {missing_dirs}")
    else:
        print(f"[OK] All {len(REQUIRED_DIRS)} required directories exist")

    # Check required files
    present_files, missing_files = check_required_files()
    if missing_files:
        errors.append(f"Missing required files: {missing_files}")
    else:
        print(f"[OK] All {len(REQUIRED_FILES)} required file sets present")

    # Walk all JSON files and validate
    json_files = list(BASE.rglob("*.json"))
    md_files = list(BASE.rglob("*.md"))

    print(f"\nFound {len(json_files)} JSON files, {len(md_files)} MD files to validate")

    for jf in json_files:
        total_file_count += 1
        rel = jf.relative_to(BASE)
        is_valid, data, err = validate_json(jf)
        if not is_valid:
            errors.append(f"Invalid JSON: {rel} - {err}")
        else:
            dupes = check_no_duplicate_ids(data, str(rel))
            if dupes:
                warnings.append(f"Duplicate IDs in {rel}: {dupes}")

        with open(jf, "r", encoding="utf-8") as fh:
            content = fh.read()
        sensitive_issues = check_sensitive_content(content, str(rel))
        warnings.extend(sensitive_issues)

    # Check markdown files for sensitive content
    for mf in md_files:
        total_file_count += 1
        rel = mf.relative_to(BASE)
        with open(mf, "r", encoding="utf-8") as fh:
            content = fh.read()
        sensitive_issues = check_sensitive_content(content, str(rel))
        warnings.extend(sensitive_issues)

    # Check for any non-MD/non-JSON files that shouldn't be there
    all_files = list(BASE.rglob("*"))
    unexpected = []
    for f in all_files:
        if f.is_file() and f.suffix not in (".json", ".md", ""):
            unexpected.append(f.relative_to(BASE))
    if unexpected:
        warnings.append(f"Unexpected file types found: {unexpected}")

    print(f"\nTotal files checked: {total_file_count}")

    print("\n" + "=" * 60)
    if errors:
        print(f"FAILED: {len(errors)} error(s) found:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("OK: No errors found")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("\nNo warnings")

    print("=" * 60)

    result = {
        "status": "FAILED" if errors else "PASSED",
        "total_files": total_file_count,
        "errors": errors,
        "warnings": warnings,
        "present_files": present_files,
        "missing_files": missing_files,
    }

    report_path = BASE / "validation" / "validation_report.json"
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)
    print(f"\nValidation report written to {report_path}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
