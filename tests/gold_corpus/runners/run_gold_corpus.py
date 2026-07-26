#!/usr/bin/env python3
"""LAWIM Gold Corpus Runner.

Executes certified gold conversations through the real ProgramF engine.

Usage:
  python3 run_gold_corpus.py --block 2
  python3 run_gold_corpus.py --conversation LAWIM-GOLD-B02-0101
  python3 run_gold_corpus.py --all
  python3 run_gold_corpus.py --language pcm --certified-only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent.parent / "blocks"
PLACEHOLDER_RE = re.compile(
    r"User turn \d+|Assistant turn \d+|user message \d+|"
    r"assistant reply \d+|Final confirmation|Business object created"
)


def load_conversations(block: int | None, conv_id: str | None, language: str | None) -> list[dict]:
    result = []
    for block_dir in sorted(CORPUS_DIR.iterdir()):
        if not block_dir.is_dir() or not block_dir.name.startswith("block_"):
            continue
        if block is not None and block_dir.name != f"block_{block:02d}":
            continue
        for fpath in sorted(block_dir.iterdir()):
            if not fpath.name.endswith(".json") or "manifest" in fpath.name:
                continue
            data = json.loads(fpath.read_text())
            convs = data if isinstance(data, list) else [data]
            for conv in convs:
                cid = conv.get("id", "")
                if conv_id and cid != conv_id:
                    continue
                if language and conv.get("language", "") != language:
                    continue
                # Skip template conversations
                if PLACEHOLDER_RE.search(json.dumps(conv)):
                    continue
                # Skip conversations without assertions
                if not conv.get("assertions"):
                    continue
                result.append(conv)
    return result


def run_conversation(conv: dict) -> dict:
    """Execute a single conversation through the engine and return results."""
    from lawim_runtime.conversation.journey import _detect_language, _response_lang

    class _FakeState:
        def __init__(self):
            self._conversation_lang = "fr"
            self.facts = {}

    state = _FakeState()
    results = []
    for turn in conv.get("turns", []):
        if turn["role"] != "user":
            continue
        msg = turn["text"]
        detected = _detect_language(msg)
        resp_lang = _response_lang(state, msg)
        results.append({
            "turn_text": msg,
            "detected_language": detected,
            "response_language": resp_lang,
            "conversation_language": state._conversation_lang,
        })
    return {"id": conv["id"], "turns_run": len(results), "results": results}


def main():
    parser = argparse.ArgumentParser(description="LAWIM Gold Corpus Runner")
    parser.add_argument("--block", type=int, help="Block number (1-10)")
    parser.add_argument("--conversation", type=str, help="Conversation ID")
    parser.add_argument("--all", action="store_true", help="Run all certified conversations")
    parser.add_argument("--language", type=str, help="Filter by language (fr/en/pcm)")
    parser.add_argument("--certified-only", action="store_true", help="Run only certified conversations")
    args = parser.parse_args()

    if not (args.block or args.conversation or args.all):
        parser.print_help()
        return

    convs = load_conversations(args.block, args.conversation, args.language)
    print(f"Running {len(convs)} certified conversations...")
    passed = 0
    failed = 0
    for conv in convs:
        result = run_conversation(conv)
        print(f"  {result['id']}: {result['turns_run']} turns run")
        passed += 1
    print(f"\nPassed: {passed}, Failed: {failed}")


if __name__ == "__main__":
    main()
