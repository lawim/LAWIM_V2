from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ReconstructedContext:
    summary: str
    user_intent: str
    current_goal: str
    previous_decisions: tuple[str, ...] = ()
    known_constraints: tuple[str, ...] = ()
    relevant_facts: tuple[str, ...] = ()
    next_expected_action: str = ""
    agent_context: str = ""
    language: str = "fr"
    confidence_score: float = 0.0
    estimated_tokens: int = 0

    def to_prompt_block(self) -> str:
        parts: list[str] = []
        if self.summary:
            parts.append(f"--- Résumé conversationnel ---\n{self.summary}")
        if self.user_intent:
            parts.append(f"--- Intention utilisateur ---\n{self.user_intent}")
        if self.current_goal:
            parts.append(f"--- Objectif actuel ---\n{self.current_goal}")
        if self.previous_decisions:
            decisions = "\n".join(f"- {d}" for d in self.previous_decisions)
            parts.append(f"--- Décisions précédentes ---\n{decisions}")
        if self.known_constraints:
            constraints = "\n".join(f"- {c}" for c in self.known_constraints)
            parts.append(f"--- Contraintes connues ---\n{constraints}")
        if self.relevant_facts:
            facts = "\n".join(f"- {f}" for f in self.relevant_facts)
            parts.append(f"--- Faits pertinents ---\n{facts}")
        if self.next_expected_action:
            parts.append(f"--- Prochaine action attendue ---\n{self.next_expected_action}")
        if self.agent_context:
            parts.append(f"--- Contexte agent ---\n{self.agent_context}")
        return "\n\n".join(parts)


class PromptReconstructionEngine:
    MAX_SUMMARY_TOKENS = 512
    MAX_FACTS = 20
    MAX_DECISIONS = 10

    def __init__(self, repository, config):
        self.repository = repository
        self.config = config

    def reconstruct(
        self,
        *,
        conversation_key: str,
        user_id: int | None = None,
        organization_id: int | None = None,
        agent_code: str | None = None,
        language: str = "fr",
        current_text: str = "",
    ) -> ReconstructedContext:
        summary = self._build_summary(conversation_key)
        user_intent = self._detect_intent(conversation_key, current_text)
        current_goal = self._identify_goal(conversation_key, user_intent)
        decisions = self._collect_decisions(conversation_key)
        constraints = self._collect_constraints(conversation_key, organization_id)
        facts = self._collect_facts(conversation_key, user_id)
        next_action = self._predict_next_action(conversation_key, agent_code)
        agent_ctx = self._get_agent_context(agent_code, conversation_key)
        return ReconstructedContext(
            summary=summary,
            user_intent=user_intent,
            current_goal=current_goal,
            previous_decisions=decisions,
            known_constraints=constraints,
            relevant_facts=facts,
            next_expected_action=next_action,
            agent_context=agent_ctx,
            language=language,
        )

    def _build_summary(self, conversation_key: str) -> str:
        try:
            decisions = self.repository.list_conversation_decisions(
                conversation_key=conversation_key, limit=20
            )
            if not decisions:
                return ""
            lines: list[str] = []
            for d in decisions[-10:]:
                payload = d.get("payload") or d.get("decision") or {}
                if isinstance(payload, str):
                    payload = {"raw": payload[:200]}
                action = payload.get("action") or payload.get("type") or "message"
                result = payload.get("result") or payload.get("status") or "processed"
                lines.append(f"{action}: {result}")
            return "; ".join(lines[-8:]) if lines else ""
        except Exception:
            return ""

    def _detect_intent(self, conversation_key: str, current_text: str) -> str:
        from .complexity import classify_text
        report = classify_text(current_text)
        signals = report.signals
        if any(s in current_text.lower() for s in ["acheter", "louer", "recherche", "bien"]):
            return "property_search"
        if any(s in current_text.lower() for s in ["prix", "coût", "payer", "campay"]):
            return "financial"
        if any(s in current_text.lower() for s in ["aide", "support", "problème", "erreur"]):
            return "support"
        if any(s in current_text.lower() for s in ["qualification", "évaluation", "estimation"]):
            return "qualification"
        if any(s in current_text.lower() for s in ["rendez-vous", "visite", "programmer"]):
            return "scheduling"
        return "general_inquiry"

    def _identify_goal(self, conversation_key: str, intent: str) -> str:
        goal_map: dict[str, str] = {
            "property_search": "Trouver un bien immobilier correspondant aux critères",
            "financial": "Obtenir des informations financières ou effectuer un paiement",
            "support": "Résoudre un problème ou obtenir de l'aide",
            "qualification": "Compléter le processus de qualification",
            "scheduling": "Planifier une visite ou un rendez-vous",
            "general_inquiry": "Répondre à une question générale",
        }
        return goal_map.get(intent, "Poursuivre la conversation en cours")

    def _collect_decisions(self, conversation_key: str) -> tuple[str, ...]:
        try:
            decisions = self.repository.list_conversation_decisions(
                conversation_key=conversation_key, limit=self.MAX_DECISIONS
            )
            return tuple(
                str(d.get("action") or d.get("type") or "decision")
                for d in decisions[-self.MAX_DECISIONS:]
            )
        except Exception:
            return ()

    def _collect_constraints(
        self, conversation_key: str, organization_id: int | None
    ) -> tuple[str, ...]:
        constraints: list[str] = []
        try:
            facts = self.repository.list_conversation_facts(
                conversation_key=conversation_key
            )
            known = set()
            for fact in facts:
                key = fact.get("fact_key") or fact.get("key") or ""
                value = fact.get("value") or fact.get("fact_value") or ""
                status = fact.get("status") or "confirmed"
                serialized = f"{key}={value} ({status})"
                if serialized not in known:
                    known.add(serialized)
                    constraints.append(serialized)
        except Exception:
            pass
        return tuple(constraints[: self.MAX_FACTS])

    def _collect_facts(
        self, conversation_key: str, user_id: int | None
    ) -> tuple[str, ...]:
        facts: list[str] = []
        try:
            conv_facts = self.repository.list_conversation_facts(
                conversation_key=conversation_key
            )
            for fact in conv_facts[: self.MAX_FACTS]:
                key = fact.get("fact_key") or fact.get("key") or ""
                value = fact.get("value") or fact.get("fact_value") or ""
                facts.append(f"{key}: {value}")
        except Exception:
            pass
        return tuple(facts)

    def _predict_next_action(self, conversation_key: str, agent_code: str | None) -> str:
        if agent_code == "qualification":
            return "Continuer la qualification avec les informations disponibles"
        if agent_code == "matching":
            return "Proposer des biens correspondant aux critères identifiés"
        if agent_code == "search":
            return "Effectuer une recherche selon les paramètres actuels"
        if agent_code == "payment":
            return "Finaliser le processus de paiement"
        return "Attendre la prochaine instruction utilisateur"

    def _get_agent_context(self, agent_code: str | None, conversation_key: str) -> str:
        if not agent_code:
            return ""
        descriptions = {
            "conversation": "Agent conversationnel général — gère les échanges standards",
            "qualification": "Agent de qualification — collecte les critères et préférences",
            "real_estate": "Agent immobilier — conseille sur les biens et le marché",
            "search": "Agent de recherche — exécute les recherches dans le catalogue",
            "matching": "Agent de matching — calcule les correspondances biens/profils",
            "commercial": "Agent commercial — gère les actions commerciales",
            "financial": "Agent financier — traite les questions de coûts et budgets",
            "payment": "Agent de paiement — gère les transactions Campay",
            "support": "Agent support — résout les problèmes utilisateur",
            "legal": "Agent juridique — fournit des informations légales générales",
            "document": "Agent documentaire — gère les documents et pièces jointes",
            "relationship": "Agent relationnel — gère les relations utilisateur",
            "admin": "Agent administrateur — configuration système",
            "director": "Agent directeur — indicateurs et vision stratégique",
            "learning": "Agent d'apprentissage — propose des améliorations",
            "orchestrator": "Agent orchestrateur — coordonne les autres agents",
        }
        return descriptions.get(agent_code, f"Agent {agent_code}")
