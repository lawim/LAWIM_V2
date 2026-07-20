#!/usr/bin/env python3
"""Validate the LAWIM VS Code canonical context foundation."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "AGENTS.md",
    "docs/ai-context/LAWIM_CANONICAL_SCOPE.md",
    "docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md",
    "docs/ai-context/LAWIM_ENGINEERING_RULES.md",
    "docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md",
    "docs/ai-context/LAWIM_SECRET_MANAGEMENT_POLICY.md",
    "docs/ai-context/LAWIM_CURRENT_STATE.md",
    ".github/copilot-instructions.md",
    ".github/instructions/lawim-conversation.instructions.md",
    ".github/instructions/lawim-testing-evidence.instructions.md",
    ".github/prompts/lawim-preflight.prompt.md",
]

INSTRUCTION_FILES = [
    ".github/instructions/lawim-conversation.instructions.md",
    ".github/instructions/lawim-testing-evidence.instructions.md",
]

TEXT_FILES_TO_SCAN = REQUIRED_FILES + [
    "reports/governance/LAWIM-VSCODE-INSTRUCTION-AUDIT.md",
]

SECRET_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI API key"),
    (re.compile(r"ghp_[A-Za-z0-9]{36}"), "GitHub token"),
    (re.compile(r"AIza[A-Za-z0-9_-]{35}"), "Google API key"),
    (re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"), "private key"),
]

REQUIRED_SIGNALS = [
    (
        "règle anti-redirection",
        [".github/copilot-instructions.md", "docs/ai-context/LAWIM_CANONICAL_SCOPE.md"],
        r"Jumia|Lamudi|SeLoger|Facebook|redirection externe|plateforme concurrente",
    ),
    (
        "règle moteur métier / LLM",
        [".github/copilot-instructions.md", "docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md"],
        r"moteur métier.*LLM|LLM.*formule|LLM ne peut pas décider",
    ),
    (
        "ProgressiveWizard",
        [".github/copilot-instructions.md", ".github/instructions/lawim-conversation.instructions.md"],
        r"ProgressiveWizard",
    ),
    (
        "continuité linguistique",
        [".github/copilot-instructions.md", ".github/instructions/lawim-conversation.instructions.md"],
        r"langue active|changement de langue|continuer en français",
    ),
    (
        "preuve USER_ACCEPTED",
        [".github/instructions/lawim-testing-evidence.instructions.md", "docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md"],
        r"USER_ACCEPTED",
    ),
    (
        "footer canonique",
        [".github/copilot-instructions.md", ".github/prompts/lawim-preflight.prompt.md"],
        r"ℹ️ Réponse assistée par LAWIM AI",
    ),
]


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def fail(message: str) -> bool:
    print(f"FAIL: {message}")
    return False


def check_required_files() -> list[bool]:
    results = []
    for relative_path in REQUIRED_FILES:
        path = REPO_ROOT / relative_path
        if not path.is_file():
            results.append(fail(f"{relative_path} — missing"))
            continue
        if path.stat().st_size == 0:
            results.append(fail(f"{relative_path} — empty"))
            continue
        results.append(True)
    return results


def check_frontmatter() -> list[bool]:
    results = []
    for relative_path in INSTRUCTION_FILES:
        content = read_text(relative_path)
        match = re.match(r'^---\napplyTo: "([^"]+)"\n---\n', content)
        if not match:
            results.append(fail(f"{relative_path} — invalid frontmatter"))
            continue
        apply_to = match.group(1)
        if not apply_to.strip() or "\n" in apply_to:
            results.append(fail(f"{relative_path} — invalid applyTo value"))
            continue
        results.append(True)
    return results


def check_no_manifest_secrets() -> list[bool]:
    results = []
    for relative_path in TEXT_FILES_TO_SCAN:
        path = REPO_ROOT / relative_path
        if not path.is_file():
            continue
        content = read_text(relative_path)
        for pattern, name in SECRET_PATTERNS:
            if pattern.search(content):
                results.append(fail(f"{relative_path} — contains potential {name}"))
        results.append(True)
    return results


def check_required_signals() -> list[bool]:
    results = []
    for label, files, pattern in REQUIRED_SIGNALS:
        combined = "\n".join(read_text(path) for path in files if (REPO_ROOT / path).is_file())
        if not re.search(pattern, combined, re.IGNORECASE | re.DOTALL):
            results.append(fail(f"missing {label}"))
            continue
        results.append(True)
    return results


def main() -> int:
    checks = []
    checks.extend(check_required_files())
    checks.extend(check_frontmatter())
    checks.extend(check_no_manifest_secrets())
    checks.extend(check_required_signals())

    if all(checks):
        print("ALL VS CODE LAWIM CONTEXT CHECKS PASSED")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
