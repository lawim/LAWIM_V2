#!/usr/bin/env python3
"""LAWIM Gold Corpus Validator.

Exit codes:
  0 = corpus Gold valide
  1 = erreurs de schema
  2 = placeholders detectes
  3 = doublons
  4 = conversations non executables
  5 = donnees sensibles
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent.parent / "blocks"
PLACEHOLDER_RE = re.compile(
    r"User turn \d+|Assistant turn \d+|user message \d+|"
    r"assistant reply \d+|Final confirmation|Business object created"
)
PHONE_RE = re.compile(r"[+]?237[6-9][0-9]{7}")
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def validate() -> int:
    errors: list[str] = []
    seen_ids: set[str] = set()
    has_placeholder = False
    has_personal_data = False
    total = 0
    executable = 0

    for block_dir in sorted(CORPUS_DIR.iterdir()):
        if not block_dir.is_dir() or not block_dir.name.startswith("block_"):
            continue
        for fpath in sorted(block_dir.iterdir()):
            if not fpath.name.endswith(".json") or "manifest" in fpath.name:
                continue
            try:
                data = json.loads(fpath.read_text())
            except json.JSONDecodeError as e:
                errors.append(f"{fpath}: invalid JSON ({e})")
                continue
            convs = data if isinstance(data, list) else [data]
            for conv in convs:
                total += 1
                cid = conv.get("id", "UNKNOWN")
                if cid in seen_ids:
                    errors.append(f"DUPLICATE ID: {cid}")
                seen_ids.add(cid)
                text = json.dumps(conv)
                if PLACEHOLDER_RE.search(text):
                    errors.append(f"PLACEHOLDER: {cid}")
                    has_placeholder = True
                if PHONE_RE.search(text):
                    errors.append(f"PHONE: {cid}")
                    has_personal_data = True
                if EMAIL_RE.search(text):
                    errors.append(f"EMAIL: {cid}")
                    has_personal_data = True
                turns = conv.get("turns", [])
                if not turns:
                    errors.append(f"NO_TURNS: {cid}")
                    continue
                if conv.get("assertions") and not PLACEHOLDER_RE.search(text):
                    executable += 1

    print(f"Total conversations: {total}")
    print(f"Executable (Gold):  {executable}")
    print(f"Errors:              {len(errors)}")
    for e in errors[:20]:
        print(f"  {e}")
    if len(errors) > 20:
        print(f"  ... and {len(errors)-20} more")

    if has_personal_data:
        return 5
    if has_placeholder and errors:
        return 2
    if any("DUPLICATE" in e for e in errors):
        return 3
    if errors:
        return 1
    if executable == 0:
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(validate())
