from __future__ import annotations

import uuid
from typing import Any

from .agent_config import AgentConfig
from .agent_models import (
    AgentAction,
    AgentDelegation,
    AgentHandover,
    AgentInvocation,
    AgentResponse,
    AgentRuntimeContext,
    AgentToolInvocation,
    HandoverStatus,
    InvocationStatus,
    RiskCategory,
    SafetyDecision,
    ToolRiskLevel,
)
from .agent_registry import agent_registry
from .agent_runtime import AgentActionService, AgentAuditService, AgentInvocationService, AgentResponseBuilder
from .agent_specialized import (
    AdministrationAgent,
    CommercialAgent,
    ConversationAgent,
    DirectorAgent,
    DocumentAgent,
    FinancialAgent,
    LearningAgent,
    LegalAssistanceAgent,
    MatchingAgent,
    PaymentAgent,
    QualificationAgent,
    RealEstateAgent,
    RelationshipAgent,
    SearchAgent,
    SupportAgent,
)

_config = AgentConfig()


class AgentRouter:
    def __init__(self):
        self._agents = {
            "conversation": ConversationAgent(),
            "qualification": QualificationAgent(),
            "real_estate": RealEstateAgent(),
            "search": SearchAgent(),
            "matching": MatchingAgent(),
            "commercial": CommercialAgent(),
            "relationship": RelationshipAgent(),
            "document": DocumentAgent(),
            "legal": LegalAssistanceAgent(),
            "financial": FinancialAgent(),
            "payment": PaymentAgent(),
            "support": SupportAgent(),
            "admin": AdministrationAgent(),
            "director": DirectorAgent(),
            "learning": LearningAgent(),
        }

    def route(self, text: str) -> str:
        t = text.lower()
        if any(w in t for w in ("aide", "support", "problème", "erreur", "help")):
            return "support"
        if any(w in t for w in ("qualification", "question", "critère")):
            return "qualification"
        if any(w in t for w in ("acheter", "louer", "recherche", "bien", "propriété", "maison", "appartement")):
            return "real_estate"
        if any(w in t for w in ("matching", "correspondance", "compatibilité")):
            return "matching"
        if any(w in t for w in ("visite", "rendez-vous", "voir")):
            return "commercial"
        if any(w in t for w in ("document", "pièce", "fichier", "contrat")):
            return "document"
        if any(w in t for w in ("juridique", "notaire", "avocat", "loi", "droit", "clause")):
            return "legal"
        if any(w in t for w in ("paiement", "paié", "campay", "facture", "coût", "prix")):
            return "payment"
        if any(w in t for w in ("statistique", "kpi", "performance", "rapport", "chiffre")):
            return "director"
        if any(w in t for w in ("apprentissage", "dataset", "proposition", "amelioration")):
            return "learning"
        if any(w in t for w in ("admin", "configuration", "paramètre")):
            return "admin"
        return "conversation"

    def get_agent(self, code: str):
        return self._agents.get(code)

    def check_flag(self, code: str) -> bool:
        flag_map = {
            "conversation": _config.conversation_agent_enabled,
            "qualification": _config.qualification_agent_enabled,
            "real_estate": _config.real_estate_agent_enabled,
            "search": _config.search_agent_enabled,
            "matching": _config.matching_agent_enabled,
            "support": _config.support_agent_enabled,
            "document": _config.document_agent_enabled,
            "legal": _config.legal_assistance_agent_enabled,
            "financial": _config.financial_agent_enabled,
            "payment": _config.payment_agent_enabled,
            "commercial": _config.commercial_agent_enabled,
            "relationship": _config.relationship_agent_enabled,
            "director": _config.director_agent_enabled,
            "learning": _config.learning_agent_enabled,
            "admin": _config.administration_agent_enabled,
        }
        return flag_map.get(code, False)


class AgentSafetyService:
    def check(self, action: str, target: str,
               risk: RiskCategory = RiskCategory.READ_ONLY) -> SafetyDecision:
        if risk in (RiskCategory.IRREVERSIBLE,):
            return SafetyDecision.HANDOVER_REQUIRED
        if risk in (RiskCategory.FINANCIAL, RiskCategory.LEGAL):
            return SafetyDecision.ALLOW_WITH_CONFIRMATION
        if risk == RiskCategory.ADMINISTRATIVE:
            return SafetyDecision.ALLOW_WITH_MASKING
        return SafetyDecision.ALLOW


class MultiAgentOrchestrator:
    def __init__(self):
        self.router = AgentRouter()
        self.inv_svc = AgentInvocationService()
        self.safety = AgentSafetyService()
        self.audit = AgentAuditService()
        self._delegations: list[AgentDelegation] = []
        self._max_depth = 5

    def process(self, text: str, ctx: AgentRuntimeContext) -> dict[str, Any]:
        if not _config.multi_agent_orchestration_enabled:
            return {"status": "disabled", "message": "multi_agent_orchestration_enabled=false"}

        agent_code = self.router.route(text)

        if not self.router.check_flag(agent_code):
            agent_code = "conversation"

        agent_def = agent_registry.get(agent_code)
        if agent_def is None:
            return {"error": f"Unknown agent: {agent_code}"}

        inv = self.inv_svc.create(AgentInvocation(
            agent_id=agent_def.agent_id,
            agent_code=agent_code,
            conversation_id=ctx.conversation_id,
            actor_id=ctx.actor_id,
            input_text=text,
        ))

        agent = self.router.get_agent(agent_code)
        if agent is None:
            self.inv_svc.fail(inv.invocation_id, f"Agent {agent_code} not found")
            return {"error": "agent_not_found"}

        resp = agent.process(inv, ctx, text) if hasattr(agent, 'process') and 'text' in type(agent.process).__code__.co_varnames else agent.process(inv, ctx)

        self.inv_svc.complete(inv.invocation_id, resp.content)
        self.audit.record({
            "event": "agent_invocation",
            "agent_code": agent_code,
            "invocation_id": inv.invocation_id,
            "conversation_id": ctx.conversation_id,
            "status": "completed",
        })
        return {
            "agent": agent_code,
            "response": resp.to_dict(),
            "invocation": inv.to_dict(),
        }


class OrchestrationPlanner:
    def plan(self, steps: list[dict[str, Any]],
              ctx: AgentRuntimeContext) -> list[dict[str, Any]]:
        results = []
        for step in steps:
            orch = MultiAgentOrchestrator()
            result = orch.process(step.get("text", ""), ctx)
            results.append({
                "step": step.get("name", ""),
                "agent": step.get("agent", ""),
                "result": result,
            })
        return results
