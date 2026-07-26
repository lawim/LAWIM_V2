#!/usr/bin/env python3
"""Check that a mission report complies with LAWIM_REPORTING_POLICY.md."""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone


REQUIRED_DETAILS = [
    "git-details.md",
    "tests-details.md",
    "corpus-details.md",
    "runtime-details.md",
    "web-details.md",
    "telegram-details.md",
    "whatsapp-details.md",
    "sqlite-details.md",
    "postgresql-details.md",
    "ovh-details.md",
    "logs-details.md",
]

REQUIRED_EVIDENCE_SUBDIRS = ["raw", "normalized"]


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_mission(mission_dir: str) -> int:
    errors = []
    report_dir = os.path.abspath(mission_dir)
    mission_name = os.path.basename(report_dir)

    # REPORT.md
    report_path = os.path.join(report_dir, "REPORT.md")
    report_ok = os.path.isfile(report_path)
    if not report_ok:
        errors.append(f"MISSING REPORT.md in {report_dir}")

    # TRACEABILITY.md
    trace_path = os.path.join(report_dir, "TRACEABILITY.md")
    trace_ok = os.path.isfile(trace_path)
    if not trace_ok:
        errors.append(f"MISSING TRACEABILITY.md in {report_dir}")

    # details/
    details_dir = os.path.join(report_dir, "details")
    details_ok = os.path.isdir(details_dir)
    if not details_ok:
        errors.append(f"MISSING details/ directory in {report_dir}")
    else:
        for detail_file in REQUIRED_DETAILS:
            dp = os.path.join(details_dir, detail_file)
            if not os.path.isfile(dp):
                errors.append(f"MISSING details/{detail_file}")

    # evidence/
    evidence_dir = os.path.join(report_dir, "evidence")
    evidence_ok = os.path.isdir(evidence_dir)
    if not evidence_ok:
        errors.append(f"MISSING evidence/ directory in {report_dir}")
    else:
        manifest_path = os.path.join(evidence_dir, "manifest.json")
        if not os.path.isfile(manifest_path):
            errors.append("MISSING evidence/manifest.json")
        else:
            try:
                with open(manifest_path) as f:
                    manifest = json.load(f)
                if not isinstance(manifest, list):
                    errors.append("evidence/manifest.json is not a list")
                else:
                    for i, entry in enumerate(manifest):
                        for key in ("control_id", "category", "path", "sha256", "created_at", "generated_by"):
                            if key not in entry:
                                errors.append(f"evidence/manifest.json[{i}] missing key '{key}'")
            except (json.JSONDecodeError, IOError) as e:
                errors.append(f"evidence/manifest.json read error: {e}")

        sha256_path = os.path.join(evidence_dir, "SHA256SUMS")
        if not os.path.isfile(sha256_path):
            errors.append("MISSING evidence/SHA256SUMS")

        for subdir in REQUIRED_EVIDENCE_SUBDIRS:
            sd = os.path.join(evidence_dir, subdir)
            if not os.path.isdir(sd):
                errors.append(f"MISSING evidence/{subdir}/ directory")

    # REPORT_INDEX.md
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(report_dir)))
    index_path = os.path.join(repo_root, "docs", "reviews", "REPORT_INDEX.md")
    index_ok = os.path.isfile(index_path)
    if not index_ok:
        errors.append("MISSING docs/reviews/REPORT_INDEX.md at repo root")
    else:
        with open(index_path) as f:
            content = f.read()
        if mission_name not in content:
            errors.append(f"Mission '{mission_name}' not found in REPORT_INDEX.md")

    # report
    if errors:
        print("REPORTING_POLICY_FAIL")
        for err in errors:
            print(f"  FAIL: {err}")
        return 1
    else:
        print("REPORTING_POLICY_PASS")
        print(f"  Mission: {mission_name}")
        print(f"  REPORT.md: {'PRESENT' if report_ok else 'MISSING'}")
        print(f"  TRACEABILITY.md: {'PRESENT' if trace_ok else 'MISSING'}")
        print(f"  details/: {'PRESENT' if details_ok else 'MISSING'}")
        print(f"  evidence/: {'PRESENT' if evidence_ok else 'MISSING'}")
        print(f"  REPORT_INDEX.md: {'PRESENT' if index_ok else 'MISSING'}")
        print(f"  Mission in index: YES")
        return 0


def check_index_only(repo_root: str) -> int:
    index_path = os.path.join(repo_root, "docs", "reviews", "REPORT_INDEX.md")
    if not os.path.isfile(index_path):
        print("MISSING docs/reviews/REPORT_INDEX.md at repo root")
        return 1
    print(f"REPORT_INDEX.md: PRESENT at {index_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check LAWIM report compliance with reporting policy."
    )
    parser.add_argument(
        "mission_dir",
        nargs="?",
        default=None,
        help="Path to the mission report directory (e.g. docs/reviews/my-mission/)",
    )
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Only check that REPORT_INDEX.md exists at the repo root",
    )
    args = parser.parse_args()

    if args.index_only:
        repo_root = os.getcwd()
        return check_index_only(repo_root)

    if args.mission_dir is None:
        parser.print_help()
        return 1

    return check_mission(args.mission_dir)


if __name__ == "__main__":
    sys.exit(main())
