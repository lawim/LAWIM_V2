from __future__ import annotations

import json
from typing import Any

GENERATION_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["content", "language", "dialogue_act", "question_count"],
    "properties": {
        "content": {"type": "string", "minLength": 1},
        "language": {"type": "string", "enum": ["fr", "en", "pcm"]},
        "dialogue_act": {
            "type": "string",
            "enum": [
                "WELCOME",
                "ACKNOWLEDGE",
                "ACKNOWLEDGE_AND_ASK",
                "CONFIRM_CORRECTION_AND_ASK",
                "CLARIFY_CURRENT_SLOT",
                "REPHRASE_LAST_QUESTION",
                "SUMMARIZE_AND_CONFIRM",
                "SEARCH_READY",
                "PUBLICATION_READY",
                "VISIT_READY",
                "TRANSACTION_READY",
                "HANDOVER",
                "CONTROLLED_ERROR",
            ],
        },
        "question_count": {"type": "integer", "minimum": 0, "maximum": 1},
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
    },
    "additionalProperties": False,
}


def _validate_type(value: Any, expected: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []
    json_type = expected.get("type", "")
    if json_type == "string":
        if not isinstance(value, str):
            errors.append(f"{path}: expected string, got {type(value).__name__}")
        elif "minLength" in expected and len(value) < expected["minLength"]:
            errors.append(f"{path}: length {len(value)} < minLength {expected['minLength']}")
        elif "enum" in expected and value not in expected["enum"]:
            errors.append(f"{path}: '{value}' not in {expected['enum']}")
    elif json_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{path}: expected integer, got {type(value).__name__}")
        else:
            if "minimum" in expected and value < expected["minimum"]:
                errors.append(f"{path}: {value} < minimum {expected['minimum']}")
            if "maximum" in expected and value > expected["maximum"]:
                errors.append(f"{path}: {value} > maximum {expected['maximum']}")
    elif json_type == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"{path}: expected number, got {type(value).__name__}")
        else:
            if "minimum" in expected and value < expected["minimum"]:
                errors.append(f"{path}: {value} < minimum {expected['minimum']}")
            if "maximum" in expected and value > expected["maximum"]:
                errors.append(f"{path}: {value} > maximum {expected['maximum']}")
    return errors


def validate_response_json(json_str: str) -> tuple[bool, str, dict | None]:
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as exc:
        return False, f"Invalid JSON: {exc}", None

    if not isinstance(parsed, dict):
        return False, "Root value must be a JSON object", None

    errors: list[str] = []

    for required_key in GENERATION_RESPONSE_SCHEMA.get("required", []):
        if required_key not in parsed:
            errors.append(f"Missing required key: '{required_key}'")

    props = GENERATION_RESPONSE_SCHEMA.get("properties", {})
    for key, value in parsed.items():
        if key not in props:
            if GENERATION_RESPONSE_SCHEMA.get("additionalProperties", True) is False:
                errors.append(f"Unexpected key: '{key}'")
            continue
        schema_prop = props[key]
        errors.extend(_validate_type(value, schema_prop, f"$.{key}"))

    if errors:
        return False, "; ".join(errors), parsed

    return True, "", parsed
