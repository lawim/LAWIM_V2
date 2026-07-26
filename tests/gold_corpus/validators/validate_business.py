#!/usr/bin/env python3
"""Validate expected business behaviour against actual business output."""

import json
import os
import sys


def validate_business_file(expected_path: str, actual: dict = None) -> dict:
    if not os.path.isfile(expected_path):
        return {"pass": True, "note": "No expected_business.json file"}

    with open(expected_path) as f:
        expected = json.load(f)

    errors = []

    required = ["business_action", "target_service"]
    for field in required:
        if field not in expected:
            errors.append(f"Missing required field: {field}")

    if actual:
        if expected.get("business_action") and actual.get("business_action"):
            if expected["business_action"] != actual["business_action"]:
                errors.append(
                    f"business_action mismatch: expected={expected['business_action']}, "
                    f"actual={actual['business_action']}"
                )
        if expected.get("target_service") and actual.get("target_service"):
            if expected["target_service"] != actual["target_service"]:
                errors.append(
                    f"target_service mismatch: expected={expected['target_service']}, "
                    f"actual={actual['target_service']}"
                )
        if "handover_required" in expected and "handover_required" in actual:
            if expected["handover_required"] != actual["handover_required"]:
                errors.append(
                    f"handover_required mismatch: expected={expected['handover_required']}, "
                    f"actual={actual['handover_required']}"
                )

    return {"pass": len(errors) == 0, "errors": errors, "expected": expected}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate expected business behaviour")
    parser.add_argument("expected_path", help="Path to expected_business.json")
    parser.add_argument("actual_path", nargs="?", default=None,
                        help="Path to actual business output JSON (optional)")
    args = parser.parse_args()

    actual = None
    if args.actual_path:
        with open(args.actual_path) as f:
            actual = json.load(f)

    result = validate_business_file(args.expected_path, actual)

    if result.get("note"):
        print(f"NOTE: {result['note']}")
        return 0

    if result["pass"]:
        print("PASS: Business expectations valid")
    else:
        print("FAIL: Business expectations invalid")
        for e in result.get("errors", []):
            print(f"  ERROR: {e}")

    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
