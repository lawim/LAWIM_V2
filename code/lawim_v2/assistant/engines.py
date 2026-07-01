from __future__ import annotations

import re
from typing import Any

from .constants import AGENT_KEYS, INTENT_KEYWORDS
from .prompts import get_system_prompt


class AgentRouterEngine:
    def route(self, *, message: str, project: dict[str, object], default_agent: str = "project_advisor") -> dict[str, object]:
        text = message.lower()
        scores: dict[str, int] = {key: 0 for key in AGENT_KEYS}
        for agent_key, keywords in INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    scores[agent_key] += 1
        best = max(scores.items(), key=lambda item: item[1])
        agent_key = best[0] if best[1] > 0 else default_agent
        if agent_key not in AGENT_KEYS:
            agent_key = "project_advisor"
        return {"agent_key": agent_key, "scores": scores, "confidence": min(95, 40 + best[1] * 15)}


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


class DeterministicAssistantEngine:
    def compose(
        self,
        *,
        agent_key: str,
        user_message: str,
        context: dict[str, object],
        rag_chunks: list[dict[str, object]],
        routing: dict[str, object],
    ) -> dict[str, object]:
        project = context.get("project") or {}
        title = str(project.get("title") or "votre projet")
        nba = context.get("next_best_action") or {}
        next_title = str(nba.get("title") or "consolider le contexte projet")
        rag_hint = ""
        if rag_chunks:
            rag_hint = f" Référence : {rag_chunks[0].get('content', '')[:120]}…"
        templates = {
            "project_advisor": (
                f"Pour {title}, je recommande de prioriser : {next_title}. "
                f"Votre question « {user_message[:80]} » concerne le pilotage global du projet.{rag_hint}"
            ),
            "decision_coach": (
                f"Analyse décisionnelle pour {title} : consultez les décisions cognition récentes "
                f"et leur niveau de confiance avant d'agir.{rag_hint}"
            ),
            "ecosystem_navigator": (
                f"Écosystème : mobilisez les partenaires et services matchés pour {title}. "
                f"Vérifiez le matching et l'orchestration.{rag_hint}"
            ),
            "risk_analyst": (
                f"Risques : traitez d'abord les scores élevés identifiés par l'intelligence risques "
                f"sur {title}.{rag_hint}"
            ),
            "journey_guide": (
                f"Parcours : avancez l'étape courante et débloquez les milestones en attente "
                f"pour {title}.{rag_hint}"
            ),
            "simulation_planner": (
                f"Simulation : lancez un scénario (budget, prêt, relocation) pour évaluer "
                f"l'impact sur {title}.{rag_hint}"
            ),
        }
        content = templates.get(agent_key, templates["project_advisor"])
        return {
            "content": content,
            "agent_key": agent_key,
            "mode": "deterministic",
            "provider": "deterministic",
            "fallback_used": True,
            "routing": routing,
            "rag_chunks_used": len(rag_chunks),
        }

    def maybe_llm_enhance(
        self,
        *,
        provider,
        system_prompt: str,
        user_message: str,
        context: dict[str, object],
        deterministic: dict[str, object],
    ) -> dict[str, object]:
        if provider.is_available():
            llm_text = provider.complete(system_prompt=system_prompt, user_message=user_message, context=context)
            if llm_text:
                return {
                    **deterministic,
                    "content": llm_text,
                    "mode": "llm",
                    "provider": getattr(provider, "name", "llm"),
                    "fallback_used": False,
                }
        return deterministic


class ConversationMemoryEngine:
    def summarize(self, messages: list[dict[str, object]], *, max_messages: int = 12) -> str:
        recent = messages[-max_messages:]
        parts = [f"{m.get('role', 'user')}: {str(m.get('content', ''))[:80]}" for m in recent]
        return " | ".join(parts) if parts else "Aucun historique."
