from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import time
from typing import Any
import uuid


@dataclass(frozen=True, slots=True)
class InternalResponse:
    content: str
    reasoning_path: str
    sources: tuple[str, ...] = ()
    confidence: float = 0.0
    latency_ms: int = 0
    requires_escalation: bool = False
    escalation_reason: str = ""
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "content": self.content,
            "reasoning_path": self.reasoning_path,
            "sources": list(self.sources),
            "confidence": self.confidence,
            "latency_ms": self.latency_ms,
            "requires_escalation": self.requires_escalation,
            "escalation_reason": self.escalation_reason,
            "metadata": self.metadata,
        }


@dataclass(frozen=True, slots=True)
class ReasoningContext:
    user_text: str
    user_id: int | None = None
    organization_id: int | None = None
    conversation_key: str = ""
    language: str = "fr"
    known_facts: tuple[str, ...] = ()
    known_intent: str = ""
    known_goal: str = ""
    agent_code: str = ""
    property_criteria: dict[str, Any] = field(default_factory=dict)
    qualification_data: dict[str, Any] = field(default_factory=dict)
    matching_results: list[dict[str, Any]] = field(default_factory=list)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class InternalReasoningEngine:
    def __init__(self, repository, config, knowledge_runtime=None, services=None):
        self.repository = repository
        self.config = config
        self.knowledge_runtime = knowledge_runtime
        self.services = services

    def reason(self, ctx: ReasoningContext) -> InternalResponse:
        started = time.perf_counter()
        intent = ctx.known_intent or self._detect_intent(ctx)
        handler = self._get_handler(intent)
        if handler:
            response = handler(ctx)
        else:
            response = self._default_response(ctx)
        elapsed = int((time.perf_counter() - started) * 1000)
        return InternalResponse(
            content=response.get("content", ""),
            reasoning_path=response.get("path", "internal_reasoning"),
            sources=tuple(response.get("sources", [])),
            confidence=float(response.get("confidence", 0.5)),
            latency_ms=elapsed,
            requires_escalation=bool(response.get("escalate", False)),
            escalation_reason=str(response.get("escalate_reason", "")),
            metadata={"intent": intent, "conversation_key": ctx.conversation_key},
        )

    def _get_handler(self, intent: str):
        handlers = {
            "property_search": self._handle_property_search,
            "qualification": self._handle_qualification,
            "matching": self._handle_matching,
            "financial": self._handle_financial,
            "support": self._handle_support,
            "scheduling": self._handle_scheduling,
            "greeting": self._handle_greeting,
            "farewell": self._handle_farewell,
            "general_inquiry": self._handle_general,
        }
        return handlers.get(intent)

    def _detect_intent(self, ctx: ReasoningContext) -> str:
        text = ctx.user_text.lower()
        if any(w in text for w in ["bonjour", "salut", "hello", "hi"]):
            return "greeting"
        if any(w in text for w in ["au revoir", "merci", "bye"]):
            return "farewell"
        if any(w in text for w in ["acheter", "louer", "recherche", "bien", "maison", "appartement"]):
            return "property_search"
        if any(w in text for w in ["qualification", "évaluation", "estimation", "critère", "besoin"]):
            return "qualification"
        if any(w in text for w in ["matching", "correspond", "similaire"]):
            return "matching"
        if any(w in text for w in ["prix", "coût", "payer", "campay", "facture", "budget"]):
            return "financial"
        if any(w in text for w in ["aide", "support", "problème", "erreur", "bug"]):
            return "support"
        if any(w in text for w in ["rendez-vous", "visite", "programmer", "rencontre"]):
            return "scheduling"
        return "general_inquiry"

    def _handle_property_search(self, ctx: ReasoningContext) -> dict[str, Any]:
        sources: list[str] = []
        response = ""
        criteria = ctx.property_criteria or {}
        if criteria:
            city = criteria.get("city", "")
            ptype = criteria.get("property_type", "")
            price_min = criteria.get("price_min", "")
            price_max = criteria.get("price_max", "")
            parts = ["recherche de biens"]
            if city:
                parts.append(f"à {city}")
            if ptype:
                parts.append(f"de type {ptype}")
            if price_min or price_max:
                parts.append(f"entre {price_min} et {price_max} XAF")
            response = f"Suite à votre {' '.join(parts)}, je vais consulter notre catalogue. "
            try:
                props = self.repository.search_properties(city=city, property_type=ptype)
                if props:
                    count = len(props)
                    titles = [p.get("title", f"Bien {p.get('id', '')}") for p in props[:3]]
                    response += (f"J'ai trouvé {count} bien{'s' if count > 1 else ''} "
                                 f"correspondant à vos critères. Parmi eux : {'; '.join(titles)}. "
                                 f"Souhaitez-vous plus de détails sur l'un d'eux ?")
                    sources.append("catalogue_immobilier")
                else:
                    response += ("Malheureusement, aucun bien ne correspond exactement à vos critères dans notre base actuelle. "
                                 "Je peux élargir la recherche ou vous proposer des biens similaires.")
            except Exception:
                response += ("Je n'ai pas pu interroger le catalogue pour le moment. "
                             "Veuillez réessayer dans quelques instants.")
        else:
            response = ("Je peux vous aider à trouver un bien immobilier. "
                        "Pourriez-vous me préciser : ville, type de bien et budget approximatif ?")
        path = "knowledge_runtime > property_catalog > search"
        return {"content": response, "path": path, "sources": sources, "confidence": 0.7}

    def _handle_qualification(self, ctx: ReasoningContext) -> dict[str, Any]:
        if self.knowledge_runtime:
            try:
                wizard = self.knowledge_runtime.wizard
                if wizard:
                    state = ctx.qualification_data or {}
                    result = wizard.process(state, ctx.user_text)
                    return {
                        "content": result.get("question", "Merci, pouvez-vous préciser ?"),
                        "path": "knowledge_runtime > qualification_wizard",
                        "sources": ["qualification_engine"],
                        "confidence": 0.8,
                    }
            except Exception:
                pass
        return {
            "content": ("Je vais vous poser quelques questions pour mieux comprendre votre projet immobilier. "
                        "Quel type de bien recherchez-vous ?"),
            "path": "internal_rules > qualification",
            "sources": ["qualification_rules"],
            "confidence": 0.6,
        }

    def _handle_matching(self, ctx: ReasoningContext) -> dict[str, Any]:
        if ctx.matching_results:
            matches = ctx.matching_results[:3]
            titles = [m.get("title", f"Bien {m.get('id', '')}") for m in matches]
            scores = [m.get("score", 0) for m in matches]
            details = [f"{t} (score: {s}%)" for t, s in zip(titles, scores)]
            return {
                "content": f"Voici les meilleures correspondances : {'; '.join(details)}. Souhaitez-vous plus d'informations ?",
                "path": "matching_engine > scoring",
                "sources": ["matching_engine", "property_catalog"],
                "confidence": 0.75,
            }
        return {
            "content": ("Pour établir des correspondances, j'ai besoin de connaître vos critères. "
                        "Quel type de bien recherchez-vous et dans quelle ville ?"),
            "path": "matching_engine > await_criteria",
            "sources": ["matching_rules"],
            "confidence": 0.5,
        }

    def _handle_financial(self, ctx: ReasoningContext) -> dict[str, Any]:
        return {
            "content": ("Pour toute question financière, je vous invite à contacter notre service client "
                        "qui pourra vous fournir des informations personnalisées. "
                        "Vous pouvez aussi consulter les prix indicatifs sur les fiches de nos biens."),
            "path": "internal_rules > financial_info",
            "sources": ["financial_policy"],
            "confidence": 0.5,
            "escalate": True,
            "escalate_reason": "financial_inquiry_needs_human",
        }

    def _handle_support(self, ctx: ReasoningContext) -> dict[str, Any]:
        return {
            "content": ("Je transmets votre demande à notre équipe support. "
                        "En attendant, puis-je vous aider avec autre chose ?"),
            "path": "internal_rules > support_escalation",
            "sources": ["support_policy"],
            "confidence": 0.4,
            "escalate": True,
            "escalate_reason": "support_request_escalated",
        }

    def _handle_scheduling(self, ctx: ReasoningContext) -> dict[str, Any]:
        return {
            "content": ("Je note votre demande de visite. Pour planifier, "
                        "pourriez-vous me préciser vos disponibilités (jour et créneau horaire) ?"),
            "path": "internal_rules > scheduling",
            "sources": ["scheduling_policy"],
            "confidence": 0.6,
        }

    def _handle_greeting(self, ctx: ReasoningContext) -> dict[str, Any]:
        lang = ctx.language or "fr"
        if lang == "fr":
            content = "Bonjour ! Je suis l'assistant LAWIM. Comment puis-je vous aider dans votre projet immobilier aujourd'hui ?"
        elif lang == "en":
            content = "Hello! I'm the LAWIM assistant. How can I help you with your real estate project today?"
        else:
            content = "Bonjour ! Je suis l'assistant LAWIM. Comment puis-je vous aider ?"
        return {
            "content": content,
            "path": "internal_rules > greeting",
            "sources": ["conversation_policy"],
            "confidence": 0.9,
        }

    def _handle_farewell(self, ctx: ReasoningContext) -> dict[str, Any]:
        return {
            "content": "Merci d'avoir utilisé LAWIM. N'hésitez pas à revenir pour toute question. Bonne journée !",
            "path": "internal_rules > farewell",
            "sources": ["conversation_policy"],
            "confidence": 0.9,
        }

    def _handle_general(self, ctx: ReasoningContext) -> dict[str, Any]:
        known = ctx.known_facts or []
        if known:
            facts = "\n".join(f"- {f}" for f in known[:5])
            return {
                "content": (f"Je dispose des informations suivantes vous concernant :\n{facts}\n\n"
                            "Sur quoi souhaitez-vous que je vous aide ?"),
                "path": "internal_rules > general_with_context",
                "sources": ["conversation_facts"],
                "confidence": 0.5,
            }
        return {
            "content": ("Je suis votre assistant LAWIM. Je peux vous aider à :\n"
                        "- Rechercher un bien immobilier\n"
                        "- Évaluer vos critères\n"
                        "- Trouver des correspondances\n"
                        "- Planifier des visites\n\n"
                        "Que souhaitez-vous faire ?"),
            "path": "internal_rules > general_capabilities",
            "sources": ["capability_catalog"],
            "confidence": 0.7,
        }

    def _default_response(self, ctx: ReasoningContext) -> dict[str, Any]:
        return {
            "content": ("Je n'ai pas pu traiter votre demande pour le moment. "
                        "Un membre de notre équipe va vous recontacter rapidement."),
            "path": "internal_rules > default_fallback",
            "sources": ["fallback_policy"],
            "confidence": 0.3,
            "escalate": True,
            "escalate_reason": "unhandled_request",
        }
