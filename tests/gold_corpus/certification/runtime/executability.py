"""Executability checker for b4rc-reviewed specifications."""

import json
import os
from typing import Dict, Any, List

SPEC_ROOT = "tests/gold_corpus/specifications/b4rc-reviewed"
REQUIRED_EXPECTED_FILES = [
    "expected_state.json",
    "expected_business.json",
    "expected_language.json",
    "expected_runtime.json",
    "expected_questions.json",
    "expected_assertions.json",
]


def can_execute(conversation_id: str, spec_root: str = SPEC_ROOT) -> Dict[str, Any]:
    """Check if a b4rc-reviewed spec is executable by the runtime."""
    result = {
        "conversation_id": conversation_id,
        "executable": False,
        "reasons": [],
        "user_turns": 0,
        "system_events": 0,
        "expected_turns": 0,
        "runtime_requirements_met": False,
    }

    spec_dir = os.path.join(spec_root, conversation_id)

    # Check conversation.json exists
    conv_path = os.path.join(spec_dir, "conversation.json")
    if not os.path.exists(conv_path):
        result["reasons"].append(f"Missing conversation.json for {conversation_id}")
        return result

    with open(conv_path) as f:
        conv = json.load(f)

    # Check conversation has ID
    if "id" not in conv:
        result["reasons"].append("Missing 'id' field in conversation.json")
        return result

    # Check ID consistency
    if conv["id"] != conversation_id:
        result["reasons"].append(f"ID mismatch: expected {conversation_id}, got {conv['id']}")
        return result

    # Check messages exist
    if "messages" not in conv or not conv["messages"]:
        result["reasons"].append("No messages in conversation")
        return result

    # Check user messages exist
    user_msgs = [m for m in conv["messages"] if m["role"] == "user"]
    if not user_msgs:
        result["reasons"].append("No user messages found")
        return result

    # Check for placeholder patterns
    for msg in conv["messages"]:
        if msg["role"] == "user":
            text = msg.get("text", "")
            if "{{" in text or "[PLACEHOLDER]" in text:
                result["reasons"].append(f"Placeholder detected in message: {text[:50]}")
                return result

    # Check expected files exist
    for fname in REQUIRED_EXPECTED_FILES:
        fpath = os.path.join(spec_dir, fname)
        if not os.path.exists(fpath):
            result["reasons"].append(f"Missing expected file: {fname}")
            return result

    # Check valid role order
    roles = [m["role"] for m in conv["messages"] if m["role"] in ("user", "assistant", "system")]
    if not roles or roles[0] != "user":
        result["reasons"].append(f"First role is not user: {roles[0] if roles else 'empty'}")
        return result

    # All checks passed
    result["executable"] = True
    result["user_turns"] = len(user_msgs)
    result["system_events"] = len([m for m in conv["messages"] if m["role"] == "system"])
    result["expected_turns"] = len(conv["messages"])
    result["runtime_requirements_met"] = True
    result["reasons"] = ["All checks passed"]

    return result


def audit_all(spec_root: str = SPEC_ROOT) -> List[Dict[str, Any]]:
    """Audit all b4rc-reviewed specs for executability."""
    import os
    results = []
    for cid in sorted(os.listdir(spec_root)):
        result = can_execute(cid, spec_root)
        results.append(result)
    return results
