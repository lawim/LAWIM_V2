#!/usr/bin/env python3
"""Mission 3B.1 — Assertion Audit Script

Analyzes the strength of assertions in:
  - corpus.py        (expected dict in each message)
  - test_behavioral.py (unit-test assertions)
  - harness.py       (harness check methods)
"""

from __future__ import annotations

import ast
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def classify_assertion_strength(
    method_name: str,
    assert_call: str,
    args: list[str],
) -> tuple[str, str]:
    """Return (STRONG|MEDIUM|WEAK, reason)."""
    call = assert_call.strip()

    # --- STRONG: specific business behavior ---
    strong_patterns = [
        # Equality checks with specific values (business rules)
        (r"assertEqual\(.*,\s*['\"](?!$)['\"]", "string equality"),  # will refine
    ]

    # Check for specific assertEqual with business values
    if call.startswith("assertEqual"):
        arg_str = call[len("assertEqual"):].strip().lstrip("(").rstrip(")")
        parts = split_args(arg_str)
        if len(parts) >= 2:
            val = parts[1].strip()
            # Specific business values
            if val in ("'BUY'", "'RENT'", "'SELL'", "'VILLA'", "'HOUSE'", "'APARTMENT'",
                        "'STUDIO'", "'LAND'", "'BUILDING'", '"BUY"', '"RENT"', '"SELL"',
                        '"VILLA"', '"HOUSE"', '"APARTMENT"', '"STUDIO"', '"LAND"', '"BUILDING"',
                        "'city'", "'budget_max'", "'property_type'", "'transaction_type'",
                        '"city"', '"budget_max"', '"property_type"', '"transaction_type"',
                        "'QUALIFYING'", "'READY_FOR_SEARCH'", "'AWAITING_INTENT'",
                        "'HUMAN_HANDOVER'", "'CLOSED'", "'NEW'", "'AWAITING_CLARIFICATION'",
                        "'RESULTS_AVAILABLE'", "'AWAITING_RELATIONSHIP_CONSENT'",
                        "'RELATIONSHIP_PROPOSED'",
                        '"QUALIFYING"', '"READY_FOR_SEARCH"', '"AWAITING_INTENT"',
                        '"HUMAN_HANDOVER"', '"CLOSED"', '"NEW"', '"AWAITING_CLARIFICATION"',
                        "'handover'", "'ambiguous'", "'select_existing'", "'GREETING'",
                        "'UPDATE_FACT'", "'REQUEST_CLARIFICATION'", "'PROVIDE_INFORMATION'",
                        '"handover"', '"ambiguous"', '"select_existing"',
                        '"GREETING"', '"UPDATE_FACT"', '"REQUEST_CLARIFICATION"', '"PROVIDE_INFORMATION"',
                        "None", "True", "False",
                        # Numeric values specific to business
                        "50000", "200000", "0.0", "1.0", "0.9",
            ):
                return ("STRONG", f"assertEqual with specific business value {val}")
            if val.startswith("ConversationState.") or val.startswith("FactStatus."):
                return ("STRONG", f"assertEqual with enum {val}")

    if call.startswith("assertTrue") or call.startswith("assertFalse"):
        arg_str = call[len("assertTrue" if call.startswith("assertTrue") else "assertFalse"):]
        arg_str = arg_str.strip().lstrip("(").rstrip(")")
        part = split_args(arg_str)[0] if split_args(arg_str) else ""
        # Check for business predicates
        business_predicates = [
            "loop_detected", "requires_clarification", "human_handover_requested",
            "is_duplicate", "can_transition", "has_field", "ambiguity",
            "ok", ".passed", "wasSuccessful",
        ]
        for bp in business_predicates:
            if bp in part:
                return ("STRONG", f"assertTrue/False on business predicate '{bp}'")

    if call.startswith("assertIn") or call.startswith("assertNotIn"):
        arg_str = call[len("assertIn" if call.startswith("assertIn") else "assertNotIn"):]
        arg_str = arg_str.strip().lstrip("(").rstrip(")")
        parts = split_args(arg_str)
        if parts:
            val = parts[0].strip()
            # Business-specific field checks
            if val in ("'city'", "'budget_max'", "'property_type'", "'transaction_type'",
                        '"city"', '"budget_max"', '"property_type"', '"transaction_type"',
                        "'neighborhood'", "'bedroom_count'", "'bathroom_count'",
                        "'surface_sqm'", "'deadline'", "'coordinates'", "'latitude'", "'longitude'",
                        '"neighborhood"', '"bedroom_count"', '"bathroom_count"',
                        '"surface_sqm"', '"deadline"',
            ):
                return ("STRONG", f"assertIn/NotIn with specific business field {val}")

    if call.startswith("assertIsNotNone"):
        return ("MEDIUM", "assertIsNotNone - structural existence check")

    if call.startswith("assertIsNone"):
        return ("STRONG", "assertIsNone - specific null check")

    if call.startswith("assertGreater"):
        arg_str = call[len("assertGreater"):].strip().lstrip("(").rstrip(")")
        parts = split_args(arg_str)
        if parts:
            val = parts[1].strip() if len(parts) > 1 else ""
            if val in ("0.5", "0.0", "40", "0"):
                return ("STRONG", f"assertGreater with business threshold {val}")
            return ("MEDIUM", f"assertGreater with threshold {val}")

    if call.startswith("assertLess"):
        return ("STRONG", "assertLess with specific comparison")

    if call.startswith("assertNotEqual"):
        return ("STRONG", "assertNotEqual - specific inequality")

    # --- WEAK: general existence/shape checks ---
    if call.startswith("assertIn") or call.startswith("assertNotIn"):
        return ("WEAK", "assertIn/NotIn - existence check in collection")

    if call.startswith("assertIsNotNone"):
        return ("MEDIUM", "assertIsNotNone - existence check")

    # Generic fallback
    return ("MEDIUM", f"uncategorized: {call[:60]}")


def split_args(arg_str: str) -> list[str]:
    """Naively split comma-separated args respecting parentheses."""
    parts = []
    depth = 0
    current = []
    for ch in arg_str:
        if ch in "({[":
            depth += 1
            current.append(ch)
        elif ch in ")}]":
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current).strip())
    return parts


def find_assertions_in_file(filepath: str) -> list[dict[str, Any]]:
    """Find unit-test style assertions in a Python file."""
    assertions = []
    with open(filepath) as f:
        content = f.read()

    # Find all assert* calls
    # Pattern: self.assertXxx(...) or just assertXxx(...)
    pattern = re.compile(
        r'(?:self\.)?(assert(?:Equal|True|False|In|NotIn|IsNotNone|IsNone|Greater|Less|GreaterEqual|LessEqual|Raises|AlmostEqual|NotEqual|MultiLineEqual|Regex|NotRegex))\s*\(',
        re.DOTALL,
    )

    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Skip comments
        if stripped.startswith("#"):
            continue

        # Find assert calls on this line
        for m in re.finditer(
            r'(?:self\.)?(assert\w+)\s*\(', stripped
        ):
            call_name = m.group(1)
            # Try to extract args
            start = m.start()
            # Find matching paren
            depth = 0
            j = m.end() - 1  # position at '('
            args_start = j + 1
            while j < len(stripped):
                if stripped[j] == "(":
                    depth += 1
                elif stripped[j] == ")":
                    depth -= 1
                    if depth == 0:
                        args_str = stripped[args_start:j]
                        args = split_args(args_str)
                        assertions.append({
                            "line": i,
                            "assert_call": f"{call_name}",
                            "args": args,
                            "full_text": stripped.strip(),
                        })
                        break
                j += 1

    # Also check multi-line assert patterns
    # Look for assert methods spanning multiple lines
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if re.search(r'(?:self\.)?(assert\w+)\s*\(', stripped) and not stripped.rstrip().endswith(")"):
            # Multi-line
            call_match = re.search(r'(?:self\.)?(assert\w+)\s*\(', stripped)
            if call_match:
                call_name = call_match.group(1)
                full_call = [stripped]
                j = i + 1
                while j < len(lines):
                    full_call.append(lines[j].strip())
                    if ")" in lines[j]:
                        break
                    j += 1
                full_text = " ".join(full_call)
                assertions.append({
                    "line": i + 1,
                    "assert_call": f"{call_name}",
                    "args": [],
                    "full_text": full_text[:120],
                })
        i += 1

    return assertions


def analyze_corpus_assertions(corpus_path: str) -> dict[str, Any]:
    """Analyze expected dict assertions in corpus.py."""
    with open(corpus_path) as f:
        content = f.read()

    # We can't easily import, but we can parse the CONVERSATIONS list manually
    # Try to find the CONVERSATIONS assignment
    tree = ast.parse(content)
    conv_nodes = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "CONVERSATIONS":
                    conv_nodes = node.value
                    break

    if conv_nodes is None or not isinstance(conv_nodes, ast.List):
        # Fallback: regex-based parsing
        return {"error": "Could not parse CONVERSATIONS list"}

    total_msgs = 0
    state_assertions = 0
    action_assertions = 0
    fact_checks = 0
    behavioral_checks = 0
    all_checks = []
    missing_expected = 0
    msg_state_action_both = 0
    msg_state_only = 0
    msg_action_only = 0

    for conv_el in conv_nodes.elts:
        if not isinstance(conv_el, ast.Dict):
            continue
        messages = None
        for kv in zip(conv_el.keys, conv_el.values):
            if isinstance(kv[0], ast.Constant) and kv[0].value == "messages":
                messages = kv[1]
                break
        if not isinstance(messages, ast.List):
            continue

        for msg_el in messages.elts:
            if not isinstance(msg_el, ast.Dict):
                continue
            total_msgs += 1
            expected = None
            for kv in zip(msg_el.keys, msg_el.values):
                if isinstance(kv[0], ast.Constant) and kv[0].value == "expected":
                    expected = kv[1]
                    break

            if expected is None or not isinstance(expected, ast.Dict):
                missing_expected += 1
                continue

            has_state = False
            has_action = False
            for ek in expected.keys:
                if isinstance(ek, ast.Constant):
                    if ek.value == "state_after":
                        has_state = True
                    elif ek.value == "action":
                        has_action = True

            if has_state:
                state_assertions += 1
            if has_action:
                action_assertions += 1
            if has_state and has_action:
                msg_state_action_both += 1
            elif has_state:
                msg_state_only += 1
            elif has_action:
                msg_action_only += 1

            # Check for checks list
            checks = None
            for kv in zip(expected.keys, expected.values):
                if isinstance(kv[0], ast.Constant) and kv[0].value == "checks":
                    checks = kv[1]
                    break
            if isinstance(checks, ast.List):
                for check_el in checks.elts:
                    if isinstance(check_el, ast.Tuple) or isinstance(check_el, ast.List):
                        check_elts = check_el.elts
                        if check_elts and isinstance(check_elts[0], ast.Constant):
                            check_name = check_elts[0].value
                            if check_name in ("no_loop", "not_ask_city", "no_external_recommendation"):
                                behavioral_checks += 1
                                all_checks.append(("BEHAVIORAL", check_name))
                            else:
                                fact_checks += 1
                                all_checks.append(("FACT", check_name))

    return {
        "total_messages_in_corpus": total_msgs,
        "messages_with_state_assertion": state_assertions,
        "messages_with_action_assertion": action_assertions,
        "messages_with_both_state_and_action": msg_state_action_both,
        "messages_with_state_only": msg_state_only,
        "messages_with_action_only": msg_action_only,
        "missing_expected_dict": missing_expected,
        "fact_checks_count": fact_checks,
        "behavioral_checks_count": behavioral_checks,
        "total_checks": fact_checks + behavioral_checks,
    }


def analyze_test_assertions(test_path: str) -> dict[str, Any]:
    """Analyze unit-test assertions in test_behavioral.py."""
    with open(test_path) as f:
        content = f.read()

    # Extract class and method names
    tree = ast.parse(content)
    class_methods = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(item.name)
            class_methods[node.name] = methods

    assertions_raw = find_assertions_in_file(test_path)

    classified = []
    for a in assertions_raw:
        method_name = _find_enclosing_method(content, a["line"])
        strength, reason = classify_assertion_strength(
            method_name, a["assert_call"], a["args"]
        )
        classified.append({
            "line": a["line"],
            "method": method_name,
            "assert_call": a["assert_call"],
            "args": a["args"],
            "strength": strength,
            "reason": reason,
            "full_text": a["full_text"],
        })

    counter = Counter(c["strength"] for c in classified)
    weak_examples = [c for c in classified if c["strength"] == "WEAK"]

    return {
        "total_assertions_found": len(classified),
        "strength_counts": dict(counter),
        "classes_found": class_methods,
        "weak_assertions": weak_examples[:20],
        "all_assertions": classified,
    }


def _find_enclosing_method(content: str, line_num: int) -> str:
    lines = content.split("\n")
    method_name = "<module-level>"
    for i in range(line_num - 2, -1, -1):
        m = re.match(r'\s+def\s+(test_\w+)\s*\(', lines[i])
        if m:
            method_name = m.group(1)
            break
    return method_name


def analyze_harness_assertions(harness_path: str) -> dict[str, Any]:
    """Analyze check methods in harness.py for assertion strength."""
    with open(harness_path) as f:
        content = f.read()

    # Look for the check methods and their assertions
    assertions_raw = find_assertions_in_file(harness_path)

    classified = []
    for a in assertions_raw:
        method_name = _find_enclosing_method(content, a["line"])
        strength, reason = classify_assertion_strength(
            method_name, a["assert_call"], a["args"]
        )
        classified.append({
            "line": a["line"],
            "method": method_name,
            "assert_call": a["assert_call"],
            "args": a["args"],
            "strength": strength,
            "reason": reason,
            "full_text": a["full_text"],
        })

    counter = Counter(c["strength"] for c in classified)
    weak_examples = [c for c in classified if c["strength"] == "WEAK"]

    # Also analyze the check logic in _run_step_check
    # Find the method and classify the checks it performs
    tree = ast.parse(content)
    check_methods_found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and (
            "check" in node.name.lower() or "assert" in node.name.lower()
            or "run" in node.name.lower()
        ):
            check_methods_found.append(node.name)

    return {
        "total_assertions_in_harness": len(classified),
        "strength_counts": dict(counter),
        "check_methods_found": check_methods_found,
        "weak_assertions": weak_examples[:20],
        "all_assertions": classified,
    }


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    corpus_path = os.path.join(base_dir, "tests", "mission_3b", "corpus.py")
    test_path = os.path.join(base_dir, "tests", "conversation_v2", "test_behavioral.py")
    harness_path = os.path.join(base_dir, "tests", "mission_3b", "harness.py")
    reports_dir = os.path.join(base_dir, "reports", "qa", "mission_3b")
    os.makedirs(reports_dir, exist_ok=True)

    # --- Corpus assertions ---
    print("=" * 70)
    print("  ANALYZING: corpus.py (expected dict assertions)")
    print("=" * 70)
    corpus_report = analyze_corpus_assertions(corpus_path)
    _print_corpus_report(corpus_report)

    # --- Test assertions ---
    print("\n" + "=" * 70)
    print("  ANALYZING: test_behavioral.py (unit-test assertions)")
    print("=" * 70)
    test_report = analyze_test_assertions(test_path)
    _print_test_report(test_report)

    # --- Harness assertions ---
    print("\n" + "=" * 70)
    print("  ANALYZING: harness.py (check methods)")
    print("=" * 70)
    harness_report = analyze_harness_assertions(harness_path)
    _print_harness_report(harness_report)

    # --- Combined summary ---
    combined = {
        "corpus": corpus_report,
        "test_behavioral": test_report,
        "harness": harness_report,
        "summary": {
            "total_assertions": (
                (test_report.get("total_assertions_found", 0) if isinstance(test_report, dict) else 0)
                + (harness_report.get("total_assertions_in_harness", 0) if isinstance(harness_report, dict) else 0)
            ),
            "corpus_messages_with_assertions": corpus_report.get("messages_with_state_assertion", 0),
        },
    }

    # Print summary
    print("\n" + "=" * 70)
    print("  ASSERTION AUDIT SUMMARY")
    print("=" * 70)
    
    if isinstance(test_report, dict):
        tc = test_report.get("strength_counts", {})
        print(f"\n  test_behavioral.py:")
        print(f"    Total: {test_report.get('total_assertions_found', 0)}")
        print(f"    STRONG: {tc.get('STRONG', 0)}, MEDIUM: {tc.get('MEDIUM', 0)}, WEAK: {tc.get('WEAK', 0)}")
        if test_report.get("weak_assertions"):
            print(f"\n  WEAK ASSERTIONS IN test_behavioral.py:")
            for wa in test_report["weak_assertions"][:10]:
                print(f"    Line {wa['line']} ({wa['method']}): {wa['full_text'][:80]}")

    if isinstance(harness_report, dict):
        hc = harness_report.get("strength_counts", {})
        print(f"\n  harness.py:")
        print(f"    Total: {harness_report.get('total_assertions_in_harness', 0)}")
        print(f"    STRONG: {hc.get('STRONG', 0)}, MEDIUM: {hc.get('MEDIUM', 0)}, WEAK: {hc.get('WEAK', 0)}")
        if harness_report.get("weak_assertions"):
            print(f"\n  WEAK ASSERTIONS IN harness.py:")
            for wa in harness_report["weak_assertions"][:10]:
                print(f"    Line {wa['line']} ({wa['method']}): {wa['full_text'][:80]}")

    # Save JSON
    out_path = "/tmp/mission-3b1-assertion-audit.json"
    with open(out_path, "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"\nJSON report saved to {out_path}")

    # Save report to reports directory too
    report_path = os.path.join(reports_dir, "assertion-audit.json")
    with open(report_path, "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Report also saved to {report_path}")


def _print_corpus_report(report: dict):
    if "error" in report:
        print(f"  ERROR: {report['error']}")
        return
    print(f"  Messages in corpus: {report['total_messages_in_corpus']}")
    print(f"  Messages with state_after: {report['messages_with_state_assertion']}")
    print(f"  Messages with action: {report['messages_with_action_assertion']}")
    print(f"  Both state+action: {report['messages_with_both_state_and_action']}")
    print(f"  State only: {report['messages_with_state_only']}")
    print(f"  Action only: {report['messages_with_action_only']}")
    print(f"  Missing expected dict: {report['missing_expected_dict']}")
    print(f"  Fact checks: {report['fact_checks_count']}")
    print(f"  Behavioral checks: {report['behavioral_checks_count']}")
    print(f"  Total checks: {report['total_checks']}")

    if report["total_messages_in_corpus"] > 0:
        pct = report["messages_with_both_state_and_action"] / report["total_messages_in_corpus"] * 100
        print(f"  Coverage: {pct:.1f}% messages have both state+action assertions")


def _print_test_report(report: dict):
    if "error" in report:
        print(f"  ERROR: {report['error']}")
        return
    print(f"  Total assert calls found: {report.get('total_assertions_found', 0)}")
    print(f"  Strength breakdown: {report.get('strength_counts', {})}")
    print(f"  Classes: {list(report.get('classes_found', {}).keys())}")

    weak = report.get("weak_assertions", [])
    if weak:
        print(f"\n  Weak assertions ({len(weak)} total, showing first 10):")
        for wa in weak[:10]:
            print(f"    Line {wa['line']} [{wa['method']}] {wa['full_text'][:90]}")


def _print_harness_report(report: dict):
    if "error" in report:
        print(f"  ERROR: {report['error']}")
        return
    print(f"  Total assert calls found: {report.get('total_assertions_in_harness', 0)}")
    print(f"  Strength breakdown: {report.get('strength_counts', {})}")
    print(f"  Check methods: {report.get('check_methods_found', [])}")


if __name__ == "__main__":
    main()
