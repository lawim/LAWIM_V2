#!/usr/bin/env python3
"""Validate the structural integrity of a conversation."""

import json
import os
import sys


def validate_conversation_file(path: str) -> dict:
    errors = []
    warnings = []

    if not os.path.isfile(path):
        return {"pass": False, "errors": [f"File not found: {path}"]}

    try:
        with open(path) as f:
            conv = json.load(f)
    except json.JSONDecodeError as e:
        return {"pass": False, "errors": [f"Invalid JSON: {e}"]}

    if not isinstance(conv, dict):
        return {"pass": False, "errors": ["Root element is not an object"]}

    if "id" not in conv:
        errors.append("Missing 'id' field")
    else:
        import re
        if not re.match(r"^[A-Z]\d{6}$", str(conv["id"])):
            errors.append(f"Invalid id format: {conv['id']} (expected A######)")

    if "messages" not in conv:
        errors.append("Missing 'messages' field")
    elif not isinstance(conv["messages"], list) or len(conv["messages"]) == 0:
        errors.append("'messages' must be a non-empty array")
    else:
        for i, msg in enumerate(conv["messages"]):
            if not isinstance(msg, dict):
                errors.append(f"messages[{i}] is not an object")
                continue
            if "role" not in msg:
                errors.append(f"messages[{i}] missing 'role'")
            elif msg["role"] not in ("user", "assistant"):
                errors.append(f"messages[{i}] invalid role: {msg['role']}")
            if "text" not in msg:
                errors.append(f"messages[{i}] missing 'text'")
            elif not isinstance(msg["text"], str) or len(msg["text"]) == 0:
                errors.append(f"messages[{i}] 'text' must be non-empty string")

        roles = [m.get("role") for m in conv["messages"] if isinstance(m, dict)]
        if roles and roles[0] != "user":
            warnings.append("First message should be from 'user'")

        last_role = None
        for i, role in enumerate(roles):
            if role == last_role:
                warnings.append(f"messages[{i}] consecutive same role ({role})")
            last_role = role

    if "category" not in conv:
        errors.append("Missing 'category' field")

    if "level" not in conv:
        warnings.append("Missing 'level' field (recommended)")

    if "description" not in conv:
        warnings.append("Missing 'description' field (recommended)")

    return {"pass": len(errors) == 0, "errors": errors, "warnings": warnings}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate conversation structural integrity")
    parser.add_argument("path", nargs="?", default=None,
                        help="Path to conversation.json or conversation directory")
    args = parser.parse_args()

    if args.path:
        path = args.path
        if os.path.isdir(path):
            conv_file = os.path.join(path, "conversation.json")
        else:
            conv_file = path
        result = validate_conversation_file(conv_file)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        convs_dir = os.path.join(base_dir, "conversations")
        if not os.path.isdir(convs_dir):
            print("WARNING: No conversations directory found")
            return 0
        overall = {"pass": 0, "fail": 0, "errors": [], "warnings": []}
        for entry in sorted(os.listdir(convs_dir)):
            conv_dir = os.path.join(convs_dir, entry)
            if os.path.isdir(conv_dir):
                conv_file = os.path.join(conv_dir, "conversation.json")
                r = validate_conversation_file(conv_file)
                if r["pass"]:
                    overall["pass"] += 1
                    print(f"  PASS: {entry}")
                else:
                    overall["fail"] += 1
                    print(f"  FAIL: {entry}")
                for e in r.get("errors", []):
                    overall["errors"].append(f"{entry}: {e}")
                for w in r.get("warnings", []):
                    overall["warnings"].append(f"{entry}: {w}")
        print(f"\nTotal: {overall['pass']} PASS, {overall['fail']} FAIL")
        for e in overall["errors"]:
            print(f"  ERROR: {e}")
        for w in overall["warnings"]:
            print(f"  WARNING: {w}")
        return 1 if overall["fail"] > 0 else 0

    if result["pass"]:
        print("PASS")
    else:
        print("FAIL")
    for e in result.get("errors", []):
        print(f"  ERROR: {e}")
    for w in result.get("warnings", []):
        print(f"  WARNING: {w}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
