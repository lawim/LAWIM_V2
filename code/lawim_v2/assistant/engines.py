from __future__ import annotations

import re
from typing import Any

class ProjectContextEngine:
    def build(
        self,
        *,
        project: dict[str, object],
        goals: list[dict[str, object]],
        journey_state: dict[str, object] | None,
        intelligence: dict[str, object] | None,
        next_action: dict[str, object] | None,
        partner_matches: list[dict[str, object]],
        service_matches: list[dict[str, object]],
        decisions: list[dict[str, object]],
        risks: list[dict[str, object]],
    ) -> dict[str, object]:
        return {
            "project": {
                "id": project.get("id"),
                "title": project.get("title"),
                "project_type": project.get("project_type"),
                "status": project.get("status"),
                "location_city": project.get("location_city"),
                "budget_min": project.get("budget_min"),
                "budget_max": project.get("budget_max"),
            },
            "goals": [{"goal_key": g.get("goal_key"), "title": g.get("title"), "status": g.get("status")} for g in goals[:5]],
            "journey": journey_state or {},
            "intelligence_summary": intelligence or {},
            "next_best_action": next_action,
            "partner_matches": partner_matches[:3],
            "service_matches": service_matches[:3],
            "decisions": [
                {"title": d.get("title"), "confidence": d.get("confidence"), "reason": d.get("reason")}
                for d in decisions[:3]
            ],
            "risks": [{"risk_key": r.get("risk_key"), "score": r.get("score")} for r in risks[:5]],
        }


class RAGFoundationEngine:
    def chunk_text(self, text: str, *, chunk_size: int = 240) -> list[str]:
        words = text.split()
        if not words:
            return []
        chunks: list[str] = []
        current: list[str] = []
        length = 0
        for word in words:
            if length + len(word) + 1 > chunk_size and current:
                chunks.append(" ".join(current))
                current = [word]
                length = len(word)
            else:
                current.append(word)
                length += len(word) + 1
        if current:
            chunks.append(" ".join(current))
        return chunks

    def score_query(self, query: str, chunk: str) -> int:
        tokens = {t for t in re.findall(r"[a-zàâäéèêëïîôùûüç0-9]+", query.lower()) if len(t) > 2}
        if not tokens:
            return 0
        haystack = chunk.lower()
        hits = sum(1 for token in tokens if token in haystack)
        return min(100, hits * 20)

    def retrieve(self, *, query: str, chunks: list[dict[str, object]], limit: int = 5) -> list[dict[str, object]]:
        scored = [
            {**chunk, "score": self.score_query(query, str(chunk.get("content", "")))}
            for chunk in chunks
        ]
        scored.sort(key=lambda row: int(row.get("score", 0)), reverse=True)
        return [row for row in scored if int(row.get("score", 0)) > 0][:limit]


class ConversationMemoryEngine:
    def summarize(self, messages: list[dict[str, object]], *, max_messages: int = 12) -> str:
        recent = messages[-max_messages:]
        parts = [f"{m.get('role', 'user')}: {str(m.get('content', ''))[:80]}" for m in recent]
        return " | ".join(parts) if parts else "Aucun historique."
