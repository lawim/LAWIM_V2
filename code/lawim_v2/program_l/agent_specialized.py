from __future__ import annotations

from typing import Any

from .agent_models import AgentResponse, AgentRuntimeContext
from .agent_runtime import AgentInvocationService, AgentResponseBuilder


class ConversationAgent:
    def __init__(self):
        self._responses = AgentResponseBuilder()

    def process(self, inv, ctx: AgentRuntimeContext, text: str) -> AgentResponse:
        return self._responses.build(inv, f"Conversation agent received: {text[:50]}...")


class QualificationAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="q1", invocation_id=inv.invocation_id,
                              agent_code="qualification",
                              content="Qualification session would be managed via ProgressiveWizard.")


class RealEstateAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="re1", invocation_id=inv.invocation_id,
                              agent_code="real_estate",
                              content="Real estate request understood. Coordinating search and matching.")


class SearchAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="s1", invocation_id=inv.invocation_id,
                              agent_code="search",
                              content="Search would use existing search engine.")


class MatchingAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="m1", invocation_id=inv.invocation_id,
                              agent_code="matching",
                              content="Matching would use existing matching engine.")


class CommercialAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="c1", invocation_id=inv.invocation_id,
                              agent_code="commercial",
                              content="Next commercial action identified.")


class RelationshipAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="r1", invocation_id=inv.invocation_id,
                              agent_code="relationship",
                              content="Relationship status assessed.")


class DocumentAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="d1", invocation_id=inv.invocation_id,
                              agent_code="document",
                              content="Document identified. Would use existing document services.")


class LegalAssistanceAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        resp = AgentResponse(response_id="l1", invocation_id=inv.invocation_id,
                              agent_code="legal",
                              content="Legal information provided. This is not a professional legal decision.")
        resp.limitations = ["This is informational assistance only",
                            "Consult a qualified notary or lawyer for binding advice"]
        return resp


class FinancialAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="f1", invocation_id=inv.invocation_id,
                              agent_code="financial",
                              content="Financial summary prepared from available data.")


class PaymentAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        resp = AgentResponse(response_id="p1", invocation_id=inv.invocation_id,
                              agent_code="payment",
                              content="Payment status checked. Would use Campay services.")
        resp.limitations = ["Cannot simulate confirmed payments",
                            "Cannot modify payment status directly"]
        return resp


class SupportAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="sp1", invocation_id=inv.invocation_id,
                              agent_code="support",
                              content="Support request received. Common issues can be resolved here.")


class AdministrationAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="a1", invocation_id=inv.invocation_id,
                              agent_code="admin",
                              content="System status summary would be provided.")


class DirectorAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        return AgentResponse(response_id="dr1", invocation_id=inv.invocation_id,
                              agent_code="director",
                              content="KPI summary would be generated from J analytics.")


class LearningAgent:
    def process(self, inv, ctx: AgentRuntimeContext) -> AgentResponse:
        resp = AgentResponse(response_id="lrn1", invocation_id=inv.invocation_id,
                              agent_code="learning",
                              content="Learning insights and proposals are available for review.")
        resp.limitations = ["Cannot approve proposals alone",
                            "Cannot publish packages without human validation"]
        return resp
