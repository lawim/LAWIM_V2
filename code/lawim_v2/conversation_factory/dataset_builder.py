from __future__ import annotations
import json, hashlib, uuid
from datetime import datetime, timezone
from typing import Any


class DatasetBuilder:
    def build(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        dataset = []
        for r in results:
            entry = {
                "id": f"SYNTH-{uuid.uuid4().hex[:12]}",
                "source": "conversation_factory",
                "language": "fr",
                "intent": "synthetic",
                "difficulty": "medium",
                "channel": "web",
                "user_role": "prospect",
                "handover_required": False,
                "expected_agent": "CONVERSATION",
                "synthetic": True,
                "generator": "multi_agent_v1",
                "scenario_id": r.get("scenario_id", ""),
                "turn_count": r.get("turn_count", 0),
                "score": r.get("score", 0.0),
                "messages": [
                    {"role": t["role"], "content": t["content"]}
                    for t in r.get("turns", [])
                ],
            }
            raw = json.dumps(entry, sort_keys=True, ensure_ascii=False)
            entry["checksum"] = hashlib.sha256(raw.encode()).hexdigest()[:16]
            dataset.append(entry)
        return dataset
