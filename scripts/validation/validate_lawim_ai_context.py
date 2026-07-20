#!/usr/bin/env python3
"""Validate the LAWIM V2 canonical AI context documents."""

import json
import os
import re
import sys

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))


def check_file(path: str) -> bool:
    full = os.path.join(REPO_ROOT, path)
    if not os.path.isfile(full):
        print(f"FAIL: {path} — missing")
        return False
    if os.path.getsize(full) == 0:
        print(f"FAIL: {path} — empty")
        return False
    return True


def check_content(path: str, pattern: str, name: str) -> bool:
    full = os.path.join(REPO_ROOT, path)
    if not os.path.isfile(full):
        return False
    with open(full, encoding="utf-8") as f:
        content = f.read()
    if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
        print(f"FAIL: {path} — missing '{name}'")
        return False
    return True


def check_no_content(path: str, pattern: str, name: str) -> bool:
    full = os.path.join(REPO_ROOT, path)
    if not os.path.isfile(full):
        return True
    with open(full, encoding="utf-8") as f:
        content = f.read()
    if re.search(pattern, content, re.IGNORECASE):
        print(f"FAIL: {path} — contains forbidden '{name}'")
        return False
    return True


def validate() -> int:
    errors = 0

    # 1. AGENTS.md present
    if not check_file("AGENTS.md"):
        errors += 1

    # 2. All canonical documents present
    docs = [
        "docs/ai-context/LAWIM_CANONICAL_SCOPE.md",
        "docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md",
        "docs/ai-context/LAWIM_ENGINEERING_RULES.md",
        "docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md",
        "docs/ai-context/LAWIM_SECRET_MANAGEMENT_POLICY.md",
        "docs/ai-context/LAWIM_CURRENT_STATE.md",
    ]
    for d in docs:
        if not check_file(d):
            errors += 1

    # 3. opencode.json valid and references exist
    opencode_path = os.path.join(REPO_ROOT, "opencode.json")
    if os.path.isfile(opencode_path):
        try:
            with open(opencode_path, encoding="utf-8") as f:
                cfg = json.load(f)
            for ref in cfg.get("instructions", []):
                if not check_file(ref):
                    errors += 1
        except (json.JSONDecodeError, Exception) as e:
            print(f"FAIL: opencode.json — invalid JSON: {e}")
            errors += 1
    else:
        print("FAIL: opencode.json — missing")
        errors += 1

    # 4. Anti-redirect rule present (in CANONICAL_SCOPE or CONVERSATION_CONTRACT)
    redirect_found = (
        check_content("docs/ai-context/LAWIM_CANONICAL_SCOPE.md", r"Jumia|SeLoger|Leboncoin|redirection", "anti-redirect")
        or check_content("docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md", r"redirection", "anti-redirect")
    )
    if not redirect_found:
        print("FAIL: anti-redirect rule missing from scope or contract")
        errors += 1

    # 5. Memory rule present (in CONVERSATION_CONTRACT or CURRENT_STATE)
    memory_found = check_content(
        "docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md",
        r"conserver.*(critères|mémoire|informations)",
        "memory rule",
    ) or check_content(
        "docs/ai-context/LAWIM_CURRENT_STATE.md",
        r"perte de contexte|mémoire",
        "memory rule",
    )
    if not memory_found:
        print("FAIL: no document contains a memory/storage rule")
        errors += 1

    # 6. Runtime evidence rule (in PRODUCTION_EVIDENCE_POLICY or ENGINEERING_RULES)
    evidence_found = check_content(
        "docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md",
        r"preuve.*runtime|preuve.*réelle|RUNTIME_VALIDATED",
        "runtime evidence",
    ) or check_content(
        "docs/ai-context/LAWIM_ENGINEERING_RULES.md",
        r"preuve runtime|tag.*Git",
        "runtime evidence",
    )
    if not evidence_found:
        print("FAIL: no document contains a runtime evidence rule")
        errors += 1

    # 7. Engine/LLM separation rule (in ENGINEERING_RULES or CONVERSATION_CONTRACT)
    sep_found = check_content(
        "docs/ai-context/LAWIM_ENGINEERING_RULES.md",
        r"moteur.*décide|code métier.*décide|LLM.*formule",
        "engine/LLM separation",
    ) or check_content(
        "docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md",
        r"LLM ne peut pas décider|LLM peut",
        "engine/LLM separation",
    )
    if not sep_found:
        print("FAIL: no document contains engine/LLM separation rule")
        errors += 1

    # 8. Secret management rule (in SECRET_MANAGEMENT_POLICY or ENGINEERING_RULES)
    secret_found = check_content(
        "docs/ai-context/LAWIM_SECRET_MANAGEMENT_POLICY.md",
        r"secret|Secret|jamais.*commettre",
        "secret management",
    ) or check_content(
        "docs/ai-context/LAWIM_ENGINEERING_RULES.md",
        r"secret|journalisée sans secret",
        "secret management",
    )
    if not secret_found:
        print("FAIL: no document contains secret management rules")
        errors += 1

    # 9. No Jumia House / SeLoger / Leboncoin as active recommendations
    lawim_docs = docs + ["AGENTS.md", "opencode.json"]
    for ld in lawim_docs:
        if not check_no_content(
            ld,
            r"(recommand.*|propos.*|utilis.*)(Jumia House|SeLoger|Leboncoin)",
            "external platform recommendation",
        ):
            errors += 1

    # 10. No obvious secrets in docs
    all_check_docs = docs + ["AGENTS.md", ".opencode/AGENTS.md", "opencode.json"]
    for d in all_check_docs:
        full = os.path.join(REPO_ROOT, d)
        if not os.path.isfile(full):
            continue
        with open(full, encoding="utf-8") as f:
            content = f.read()
        secret_patterns = [
            (r"sk-[A-Za-z0-9]{20,}", "OpenAI API key"),
            (r"ghp_[A-Za-z0-9]{36}", "GitHub token"),
            (r"AIza[A-Za-z0-9_-]{35}", "Google API key"),
        ]
        for pat, name in secret_patterns:
            if re.search(pat, content):
                print(f"FAIL: {d} — contains potential {name}")
                errors += 1

    if errors == 0:
        print("ALL CHECKS PASSED")
    return errors


if __name__ == "__main__":
    sys.exit(validate())
