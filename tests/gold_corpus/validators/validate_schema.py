#!/usr/bin/env python3
"""Validate that a conversation JSON conforms to its schema."""

import json
import os
import sys

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("FAIL: jsonschema library is required. Install with: pip install jsonschema")
    sys.exit(1)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(BASE_DIR, "schema")


def load_schema(schema_name: str) -> dict:
    path = os.path.join(SCHEMA_DIR, schema_name)
    if not os.path.isfile(path):
        print(f"FAIL: Schema file not found: {path}")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def validate_file(filepath: str, schema: dict, label: str) -> bool:
    if not os.path.isfile(filepath):
        print(f"  WARNING: {label} file not found: {filepath}")
        return True  # optional files are not failures
    try:
        with open(filepath) as f:
            data = json.load(f)
        validate(instance=data, schema=schema)
        print(f"  PASS: {label} ({filepath})")
        return True
    except ValidationError as e:
        print(f"  FAIL: {label} ({filepath})")
        print(f"    Reason: {e.message}")
        print(f"    Path: {' -> '.join(str(p) for p in e.absolute_path)}")
        return False
    except json.JSONDecodeError as e:
        print(f"  FAIL: {label} ({filepath}) — Invalid JSON: {e}")
        return False


def validate_conversation_dir(conv_dir: str) -> dict:
    results = {"pass": 0, "fail": 0, "warnings": 0}
    mappings = [
        ("conversation.json", "conversation.schema.json", "conversation"),
        ("expected_state.json", "expected_state.schema.json", "expected_state"),
        ("expected_business.json", "expected_business.schema.json", "expected_business"),
        ("expected_questions.json", "expected_questions.schema.json", "expected_questions"),
        ("expected_language.json", "expected_language.schema.json", "expected_language"),
        ("expected_runtime.json", "expected_runtime.schema.json", "expected_runtime"),
        ("expected_assertions.json", "assertions.schema.json", "expected_assertions"),
    ]

    for data_file, schema_file, label in mappings:
        data_path = os.path.join(conv_dir, data_file)
        schema = load_schema(schema_file)
        success = validate_file(data_path, schema, label)
        if success:
            results["pass"] += 1
        else:
            results["fail"] += 1

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate conversation JSON files against schemas")
    parser.add_argument("path", nargs="?", default=None,
                        help="Path to a conversation directory or a single JSON file")
    args = parser.parse_args()

    if args.path:
        path = args.path
        if os.path.isdir(path):
            results = validate_conversation_dir(path)
        elif os.path.isfile(path):
            results = {"pass": 0, "fail": 0, "warnings": 0}
            basename = os.path.basename(path)
            for data_file, schema_file, label in [
                ("conversation.json", "conversation.schema.json", "conversation"),
                ("expected_state.json", "expected_state.schema.json", "expected_state"),
                ("expected_business.json", "expected_business.schema.json", "expected_business"),
                ("expected_questions.json", "expected_questions.schema.json", "expected_questions"),
                ("expected_language.json", "expected_language.schema.json", "expected_language"),
                ("expected_runtime.json", "expected_runtime.schema.json", "expected_runtime"),
                ("expected_assertions.json", "assertions.schema.json", "expected_assertions"),
            ]:
                if basename == data_file or basename == schema_file:
                    data_path = path if basename == data_file else os.path.join(os.path.dirname(path), data_file)
                    schema = load_schema(schema_file)
                    success = validate_file(data_path if basename == data_file else path, schema, label)
                    if success:
                        results["pass"] += 1
                    else:
                        results["fail"] += 1
                    break
        else:
            print(f"FAIL: Path not found: {path}")
            return 1
    else:
        conversations_dir = os.path.join(BASE_DIR, "conversations")
        if not os.path.isdir(conversations_dir):
            print("WARNING: No conversations directory found")
            return 0
        results = {"pass": 0, "fail": 0, "warnings": 0}
        for entry in sorted(os.listdir(conversations_dir)):
            conv_dir = os.path.join(conversations_dir, entry)
            if os.path.isdir(conv_dir):
                print(f"\nValidating: {entry}")
                r = validate_conversation_dir(conv_dir)
                for k in results:
                    results[k] += r[k]

    print(f"\nTotal: {results['pass']} PASS, {results['fail']} FAIL, {results['warnings']} WARNING")
    if results["fail"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
