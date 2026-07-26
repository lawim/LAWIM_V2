#!/usr/bin/env python3
"""Validate assertions against actual conversation output."""

import json
import os
import re
import sys


def evaluate_assertion(assertion: dict, actual: dict) -> dict:
    op = assertion.get("operator", "eq")
    expected = assertion["expected"]
    path = assertion.get("path", "")

    actual_value = actual
    if path:
        parts = path.split(".")
        for part in parts:
            if isinstance(actual_value, dict):
                actual_value = actual_value.get(part)
            elif isinstance(actual_value, list) and part.isdigit():
                actual_value = actual_value[int(part)]
            else:
                actual_value = None
                break

    result = {"id": assertion["id"], "pass": False, "expected": expected, "actual": actual_value}

    if op == "eq":
        result["pass"] = actual_value == expected
    elif op == "neq":
        result["pass"] = actual_value != expected
    elif op == "contains":
        result["pass"] = expected in str(actual_value) if actual_value is not None else False
    elif op == "not_contains":
        result["pass"] = expected not in str(actual_value) if actual_value is not None else True
    elif op == "exists":
        result["pass"] = actual_value is not None
    elif op == "not_exists":
        result["pass"] = actual_value is None
    elif op == "gt":
        result["pass"] = (actual_value or 0) > expected
    elif op == "lt":
        result["pass"] = (actual_value or 0) < expected
    elif op == "regex":
        result["pass"] = bool(re.search(str(expected), str(actual_value or "")))
    else:
        result["pass"] = False
        result["error"] = f"Unknown operator: {op}"

    return result


def validate_assertions_file(assertions_path: str, actual: dict) -> dict:
    if not os.path.isfile(assertions_path):
        return {"pass": True, "results": [], "note": "No assertions file"}

    with open(assertions_path) as f:
        data = json.load(f)

    results = []
    for assertion in data.get("assertions", []):
        r = evaluate_assertion(assertion, actual)
        results.append(r)

    passed = sum(1 for r in results if r["pass"])
    failed = sum(1 for r in results if not r["pass"])

    return {"pass": failed == 0, "results": results, "passed": passed, "failed": failed}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate assertions against actual output")
    parser.add_argument("assertions_file", help="Path to expected_assertions.json")
    parser.add_argument("actual_file", nargs="?", default=None,
                        help="Path to actual output JSON (optional for dry-run)")
    args = parser.parse_args()

    if args.actual_file:
        with open(args.actual_file) as f:
            actual = json.load(f)
    else:
        actual = {}

    result = validate_assertions_file(args.assertions_file, actual)

    if result.get("note"):
        print(f"NOTE: {result['note']}")
        return 0

    print(f"Assertions: {result.get('passed', 0)} PASS, {result.get('failed', 0)} FAIL")
    for r in result.get("results", []):
        status = "PASS" if r["pass"] else "FAIL"
        print(f"  {status}: {r['id']} (expected={r['expected']}, actual={r['actual']})")

    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
