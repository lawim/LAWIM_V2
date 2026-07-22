from __future__ import annotations
from typing import Any


class V2ReadinessEvaluatorAdapter:
    def evaluate(self, known_slots: dict[str, Any]) -> dict[str, Any]:
        required = {"city", "property_type", "transaction_type"}
        present = set(known_slots.keys())
        missing = required - present
        return {"ready": len(missing) == 0, "missing": list(missing)}
