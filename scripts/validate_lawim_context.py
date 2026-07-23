#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=str, default=None, help="Project root directory")
args = parser.parse_args()

ROOT = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]

REQUIRED_FILES: list[str] = [
    "LAWIM_CONTEXT.md",
    "AGENTS.md",
    "lawim_program_status.yaml",
    "reports/programs/PROGRAM-A-SUMMARY.md",
    "reports/programs/PROGRAM-B-SUMMARY.md",
    "reports/programs/PROGRAM-C-SUMMARY.md",
    "reports/programs/PROGRAM-C5-STATUS.md",
    "reports/programs/PROGRAM-D-SPECIFICATION.md",
    "reports/programs/PROGRAM-D-REPORT.md",
    "reports/programs/PROGRAM-D5-REPORT.md",
    "reports/programs/ROADMAP-V3.md",
    "reports/programs/OPENCODE-SESSION-BOOTSTRAP.md",
    "reports/programs/AGENT-REVIEW-CHECKLIST.md",
    "reports/architecture/LAWIM-GLOSSARY.md",
    "reports/architecture/LAWIM-ARCHITECTURE-MAP.md",
    "reports/architecture/LAWIM-VALIDATION-LEVELS.md",
    "reports/architecture/LAWIM-CONTEXT-AUDIT.md",
    "reports/architecture/LAWIM-PROGRAM-D5-INITIAL-AUDIT.md",
    "reports/architecture/LAWIM-PROGRAM-D-FILE-JUSTIFICATION.md",
    "reports/architecture/LAWIM-PROGRAM-D-DEPENDENCY-MAP.md",
    "reports/architecture/LAWIM-PROGRAM-D-TEST-QUALITY.md",
    "reports/architecture/LAWIM-PROGRAM-D-SIMPLIFICATION-REPORT.md",
]

VALID_STATUSES = frozenset({
    "not_started", "planned", "in_progress", "blocked",
    "complete", "complete_with_baseline_verification_pending",
    "pending_certification_review", "certified_with_reservations",
})

REQUIRED_PROGRAMS = frozenset({"A", "B", "C", "C5", "D"})

EXPECTED_COMMITS = {
    "A": "cf633f5f",
    "B": "46fbbc49",
    "C": "86b449b9",
    "C5": "18de07d2",
    "D": "d8c379c3",
}

AGENTS_REQUIRED_SECTIONS = {
    "pre-modification reading": r"## 2\. Verification pre-modification",
    "no external redirection": r"## 3\. Perimetre LAWIM",
    "LLM role": r"## 4\. Separation metier / LLM",
}

CANONICAL_STATEMENTS = [
    "LAWIM n'est pas un chatbot. LAWIM est une plateforme immobiliere intelligente et operationnelle.",
    "Une conversation ne constitue pas un projet. Un projet est une entite metier persistante.",
    "Un message ne constitue pas une decision. La decision est prise par le moteur metier.",
    "Une decision ne constitue pas une execution. L'execution est realisee par ActionExecutionEngine.",
    "Une execution automatisee ne constitue pas necessairement une preuve reelle. La preuve reelle necessite un test de bout en bout sur canal reel.",
    "Un test unitaire ne prouve pas une integration reelle. L'integration reelle necessite des tests cross-composant et cross-canal.",
    "Un commit ne prouve pas un deploiement. Le deploiement necessite un environnement cible operationnel.",
    "Un service sain ne prouve pas le fonctionnement du parcours metier. Le parcours metier necessite une validation de bout en bout.",
]

all_pass = True


def fail(msg: str) -> None:
    global all_pass
    all_pass = False
    print(f"[FAIL] {msg}")


def pass_(msg: str) -> None:
    print(f"[PASS] {msg}")


def check_file_exists(path: Path, label: str) -> None:
    if path.exists():
        pass_(f"{label} exists")
    else:
        fail(f"{label} — file not found: {path}")


def check_commit_format(commit: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{7,40}", commit))


# ---------------------------------------------------------------------------
# 1. File existence
# ---------------------------------------------------------------------------
print("=== File existence checks ===")
for rel in REQUIRED_FILES:
    check_file_exists(ROOT / rel, rel)

# ADR files
print("--- ADR files ---")
for i in range(1, 10):
    pattern = f"ADR-{i:03d}-*.md"
    adr_dir = ROOT / "reports" / "architecture" / "adr"
    matches = list(adr_dir.glob(pattern))
    if matches:
        pass_(f"ADR-{i:03d} found: {matches[0].name}")
    else:
        fail(f"ADR-{i:03d} — no file matching {pattern} in {adr_dir}")

# Self check
check_file_exists(ROOT / "scripts" / "validate_lawim_context.py", "scripts/validate_lawim_context.py (self)")

# ---------------------------------------------------------------------------
# 2. YAML validation
# ---------------------------------------------------------------------------
print("\n=== lawim_program_status.yaml validation ===")
yaml_path = ROOT / "lawim_program_status.yaml"

if not yaml_path.exists():
    fail("lawim_program_status.yaml not found")
else:
    if yaml is None:
        print("[WARN] PyYAML not available — skipping YAML parsing checks")
    else:
        try:
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            pass_("YAML is valid")

            for key in ("project", "architecture", "programs"):
                if key in data:
                    pass_(f"top-level key '{key}' present")
                else:
                    fail(f"top-level key '{key}' missing")

            programs = data.get("programs", {})
            for prog in REQUIRED_PROGRAMS:
                if prog in programs:
                    pass_(f"program '{prog}' exists")
                else:
                    fail(f"program '{prog}' missing")
                    continue
                status = programs[prog].get("status", "")
                if status in VALID_STATUSES:
                    pass_(f"  {prog} status '{status}' valid")
                else:
                    fail(f"  {prog} status '{status}' invalid (valid: {sorted(VALID_STATUSES)})")

            for prog_key, expected_commit in EXPECTED_COMMITS.items():
                prog = programs.get(prog_key, {})
                commit = prog.get("commit", "")
                if not commit:
                    fail(f"  {prog_key} has no commit field")
                elif not check_commit_format(commit):
                    fail(f"  {prog_key} commit '{commit}' is not valid hex format")
                else:
                    pass_(f"  {prog_key} commit '{commit}' is valid hex")

        except yaml.YAMLError as e:
            fail(f"YAML parse error: {e}")
        except Exception as e:
            fail(f"Unexpected error reading YAML: {e}")

# ---------------------------------------------------------------------------
# 3. Commit matching (YAML commits vs expected)
# ---------------------------------------------------------------------------
print("\n=== Commit matching ===")
if yaml is not None and yaml_path.exists():
    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        programs = data.get("programs", {})
        for prog_key, expected in EXPECTED_COMMITS.items():
            actual = programs.get(prog_key, {}).get("commit", "")
            if actual == expected:
                pass_(f"Program {prog_key} commit matches expected: {expected}")
            else:
                fail(f"Program {prog_key} commit mismatch: got '{actual}', expected '{expected}'")
    except Exception as e:
        fail(f"Cannot verify commits: {e}")
else:
    fail("Cannot verify commits — YAML unavailable or file missing")

# ---------------------------------------------------------------------------
# 4. Domain Runtime file existence
# ---------------------------------------------------------------------------
print("\n=== Domain runtime files ===")
DOMAIN_RUNTIME_DIRS = [
    "lawim_runtime/domains/base",
    "lawim_runtime/domains/matching",
    "lawim_runtime/domains/visit",
    "lawim_runtime/domains/crm",
    "lawim_runtime/domains/notification",
    "lawim_runtime/domains/document",
    "lawim_runtime/domains/verification",
    "lawim_runtime/domains/transaction",
    "lawim_runtime/domains/payment",
    "lawim_runtime/domains/adapters",
]
for d in DOMAIN_RUNTIME_DIRS:
    p = ROOT / d
    if p.is_dir():
        pass_(f"{d}/ exists")
    else:
        fail(f"{d}/ missing")

DOMAIN_RUNTIME_FILES = [
    "lawim_runtime/domains/config.py",
    "lawim_runtime/domains/registration.py",
]
for f in DOMAIN_RUNTIME_FILES:
    p = ROOT / f
    if p.exists():
        pass_(f"{f} exists")
    else:
        fail(f"{f} missing")

# ---------------------------------------------------------------------------
# 5. AGENTS.md required sections
# ---------------------------------------------------------------------------
print("\n=== AGENTS.md sections ===")
agents_path = ROOT / "AGENTS.md"
if agents_path.exists():
    content = agents_path.read_text(encoding="utf-8")
    for label, pattern in AGENTS_REQUIRED_SECTIONS.items():
        if re.search(pattern, content):
            pass_(f"Section matching '{pattern}' found in AGENTS.md ({label})")
        else:
            fail(f"Section matching '{pattern}' not found in AGENTS.md ({label})")
    # Also check for LLM specific phrases within section 4
    if "Le LLM peut" in content:
        pass_("AGENTS.md contains 'Le LLM peut' (LLM role)")
    else:
        fail("AGENTS.md missing 'Le LLM peut' phrase")
    if "Le LLM ne peut pas" in content:
        pass_("AGENTS.md contains 'Le LLM ne peut pas' (LLM role)")
    else:
        fail("AGENTS.md missing 'Le LLM ne peut pas' phrase")
else:
    fail("AGENTS.md not found")

# ---------------------------------------------------------------------------
# 6. LAWIM_CONTEXT.md 8 canonical statements
# ---------------------------------------------------------------------------
print("\n=== LAWIM_CONTEXT.md canonical statements ===")
context_path = ROOT / "LAWIM_CONTEXT.md"
if context_path.exists():
    content = context_path.read_text(encoding="utf-8")
    for stmt in CANONICAL_STATEMENTS:
        if stmt in content:
            pass_(f"Canonical statement present: {stmt[:60]}...")
        else:
            fail(f"Canonical statement missing: {stmt[:60]}...")
else:
    fail("LAWIM_CONTEXT.md not found")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
if all_pass:
    print("All validations PASSED.")
    sys.exit(0)
else:
    print("Some validations FAILED.")
    sys.exit(1)
