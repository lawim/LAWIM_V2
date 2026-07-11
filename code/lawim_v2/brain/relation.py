from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from ..matching import MatchCriteria, MatchWeights, rank_properties, rank_partners


class RelationType(str, Enum):
    PERSON_TO_PROPERTY = "person_to_property"
    PERSON_TO_PERSON = "person_to_person"
    PERSON_TO_PARTNER = "person_to_partner"
    PROJECT_TO_PROJECT = "project_to_project"
    PROPERTY_TO_PARTNER = "property_to_partner"
    PARTNER_TO_PARTNER = "partner_to_partner"


class ProposalStatus(str, Enum):
    DETECTED = "detected"
    PROPOSED = "proposed"
    CONSULTED = "consulted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    CONSENT_PENDING = "consent_pending"
    RELATION_ESTABLISHED = "relation_established"
    CONTACT_MADE = "contact_made"
    APPOINTMENT_SCHEDULED = "appointment_scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NO_FOLLOW_UP = "no_follow_up"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


PARTNER_INTENT_MAP: dict[str, list[str]] = {
    "notaire": ("find_partner", "buy", "sell"),
    "architecte": ("build", "find_land"),
    "géomètre": ("find_land", "buy"),
    "banque": ("find_funding", "invest", "buy", "build"),
    "agent immobilier": ("find_partner", "buy", "sell", "rent"),
    "avocat": ("find_partner", "buy", "sell"),
    "photographe": ("sell", "rent"),
    "entreprise de construction": ("build",),
}

PROPERTY_TYPE_BY_INTENT: dict[str, list[str]] = {
    "buy": ("maison", "villa", "appartement", "terrain", "immeuble"),
    "rent": ("appartement", "maison", "studio", "bureau"),
    "invest": ("immeuble", "terrain", "commerce", "bureau"),
    "build": ("terrain",),
}

MATCHABLE_PROJECT_STATUSES: frozenset[str] = frozenset({"active", "in_progress"})


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _build_match_context(project: dict[str, Any] | None, analysis: dict[str, Any] | None) -> dict[str, Any]:
    ctx: dict[str, Any] = {}
    if project:
        ctx["project_id"] = project.get("id")
        ctx["intent"] = project.get("project_type", "other")
        ctx["city"] = project.get("location_city")
        ctx["budget_min"] = project.get("budget_min")
        ctx["budget_max"] = project.get("budget_max")
    if analysis:
        ctx["primary_intent"] = analysis.get("primary_intent", ctx.get("intent", "other"))
        ctx["entities"] = analysis.get("entities", {})
        ctx["language"] = analysis.get("language", "fr")
        if not ctx.get("city") and analysis.get("entities", {}).get("cities"):
            ctx["city"] = analysis["entities"]["cities"][0]["city"]
        if not ctx.get("budget_max") and analysis.get("entities", {}).get("budgets"):
            ctx["budget_max"] = analysis["entities"]["budgets"][0]["value"]
    return ctx


class RelationEngine:
    def __init__(self, repository) -> None:
        self.repository = repository

    def find_properties(
        self,
        *,
        project: dict[str, Any] | None = None,
        analysis: dict[str, Any] | None = None,
        limit: int = 10,
        min_score: float = 10.0,
    ) -> list[dict[str, Any]]:
        ctx = _build_match_context(project, analysis)
        intent = ctx.get("primary_intent") or ctx.get("intent", "other")
        if intent in ("find_land", "find_property"):
            intent = "buy"

        criteria = MatchCriteria(
            target_type="property",
            city=ctx.get("city"),
            country="Cameroon",
            budget_min=ctx.get("budget_min"),
            budget_max=ctx.get("budget_max"),
            property_type=None,
            status="published",
            limit=limit,
            min_score=min_score,
            weights=MatchWeights().normalized(),
        )
        all_properties = self.repository.list_properties_for_matching()
        if not all_properties:
            return []
        from dataclasses import replace
        criteria = replace(criteria, limit=limit)
        return rank_properties(all_properties, criteria)

    def find_partners(
        self,
        *,
        partner_type: str | None = None,
        project: dict[str, Any] | None = None,
        analysis: dict[str, Any] | None = None,
        limit: int = 10,
        min_score: float = 10.0,
    ) -> list[dict[str, Any]]:
        ctx = _build_match_context(project, analysis)
        intent = ctx.get("primary_intent") or ctx.get("intent", "other")
        partner_types = [partner_type] if partner_type else PARTNER_INTENT_MAP.get(intent, [])
        if not partner_types:
            partner_types = list(PARTNER_INTENT_MAP.keys())[:3]

        criteria = MatchCriteria(
            target_type="partner",
            city=ctx.get("city"),
            country="Cameroon",
            partner_type=partner_types[0] if partner_types else None,
            need=intent,
            status="active",
            limit=limit,
            min_score=min_score,
            weights=MatchWeights().normalized(),
        )
        all_partners = self.repository.list_partners_for_matching()
        if not all_partners:
            return []
        from dataclasses import replace
        criteria = replace(criteria, limit=limit)
        return rank_partners(all_partners, criteria)

    def propose(
        self,
        *,
        project_id: int,
        relation_type: str,
        target_type: str,
        target_id: int,
        score: int,
        justification: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return dict(self.repository.create_relation_proposal(
            project_id=project_id,
            relation_type=relation_type,
            target_type=target_type,
            target_id=target_id,
            score=score,
            justification=justification,
            metadata_json=metadata or {},
            status=ProposalStatus.DETECTED.value,
        ))

    def accept_proposal(self, proposal_id: int) -> dict[str, Any] | None:
        return self.repository.update_relation_proposal_status(
            proposal_id, ProposalStatus.ACCEPTED.value
        )

    def reject_proposal(self, proposal_id: int) -> dict[str, Any] | None:
        return self.repository.update_relation_proposal_status(
            proposal_id, ProposalStatus.REJECTED.value
        )

    def request_consent(
        self,
        proposal_id: int,
    ) -> dict[str, Any] | None:
        return self.repository.update_relation_proposal_status(
            proposal_id, ProposalStatus.CONSENT_PENDING.value
        )

    def grant_consent(self, proposal_id: int) -> dict[str, Any] | None:
        updated = self.repository.update_relation_proposal_status(
            proposal_id, ProposalStatus.RELATION_ESTABLISHED.value
        )
        if updated:
            self.repository.create_relation(
                project_id=int(updated["project_id"]),
                relation_type=str(updated["relation_type"]),
                source_type="proposal",
                source_id=proposal_id,
                target_type=str(updated["target_type"]),
                target_id=int(updated["target_id"]),
                status=ProposalStatus.RELATION_ESTABLISHED.value,
            )
        return updated

    def list_proposals(
        self,
        project_id: int,
        *,
        status: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        return self.repository.list_relation_proposals(
            project_id, status=status, limit=limit
        )

    def get_active_proposals(self, project_id: int) -> list[dict[str, Any]]:
        return self.list_proposals(project_id, status="proposed")

    def run_full_match(
        self,
        *,
        project_id: int,
        project: dict[str, Any] | None = None,
        analysis: dict[str, Any] | None = None,
        language: str = "fr",
    ) -> dict[str, Any]:
        properties = self.find_properties(project=project, analysis=analysis, limit=5)
        partners = self.find_partners(project=project, analysis=analysis, limit=5)
        proposals: list[dict[str, Any]] = []

        for match in properties:
            prop = match.get("property", {})
            if isinstance(prop, dict) and prop.get("id"):
                pid = int(str(prop["id"]))
                proposals.append(self.propose(
                    project_id=project_id,
                    relation_type=RelationType.PERSON_TO_PROPERTY.value,
                    target_type="property",
                    target_id=pid,
                    score=int(match.get("score", 50)),
                    justification=match.get("summary", "Correspondance trouvée"),
                    metadata={"match_data": match},
                ))

        for match in partners:
            partner = match.get("partner", {})
            if isinstance(partner, dict) and partner.get("id"):
                pid = int(str(partner["id"]))
                proposals.append(self.propose(
                    project_id=project_id,
                    relation_type=RelationType.PERSON_TO_PARTNER.value,
                    target_type="partner",
                    target_id=pid,
                    score=int(match.get("score", 50)),
                    justification=match.get("summary", "Professionnel correspondant"),
                    metadata={"match_data": match},
                ))

        return {
            "proposals_count": len(proposals),
            "properties_found": len(properties),
            "partners_found": len(partners),
            "proposals": proposals,
        }
