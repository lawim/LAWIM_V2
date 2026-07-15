from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .r6_workflow import WorkflowType, WORKFLOW_STATE_MACHINES


GOLD_WORKFLOW_STATES: dict[str, list[str]] = {
    "matching": ["created", "scored", "proposed", "demandeur_consented",
                  "holder_consented", "relationship", "active", "expired",
                  "closed", "archived"],
    "contact": ["initiated", "demandeur_consented", "holder_consented",
                "active", "closed", "archived"],
    "visit": ["requested", "scheduled", "confirmed", "reminder",
              "in_progress", "completed", "cancelled", "no_show", "rescheduled"],
    "transaction": ["initiated", "offer", "negotiation", "accepted",
                    "docs", "signed", "payment", "completed", "cancelled", "disputed"],
    "service_payment": [f"s{i}" for i in range(18)],
    "incident": [f"i{i}" for i in range(8)],
    "mediation": [f"m{i}" for i in range(8)],
    "pipeline": ["lead_in", "qualification", "proposition", "negotiation",
                 "closing", "won", "lost", "recycled"],
    "publication": [f"p{i}" for i in range(11)],
    "redirection": [f"r{i}" for i in range(12)],
    "conversion": [f"c{i}" for i in range(12)],
    "agent_invitation": [f"a{i}" for i in range(7)],
    "identity_resolution": [f"id{i}" for i in range(5)],
    "orchestrator": [f"o{i}" for i in range(9)],
}


@dataclass
class WorkflowMigrationHelper:
    def gold_to_v2(self, gold_name: str) -> WorkflowType | None:
        mapping: dict[str, WorkflowType] = {
            "matching": WorkflowType.MATCHING,
            "contact": WorkflowType.CONTACT,
            "visit": WorkflowType.VISIT,
            "transaction": WorkflowType.TRANSACTION,
            "service_payment": WorkflowType.SERVICE_PAYMENT,
            "incident": WorkflowType.INCIDENT,
            "mediation": WorkflowType.MEDIATION,
            "pipeline": WorkflowType.PIPELINE,
            "publication": WorkflowType.PUBLICATION,
            "redirection": WorkflowType.REDIRECTION,
            "conversion": WorkflowType.CONVERSION,
            "agent_invitation": WorkflowType.AGENT_INVITATION,
            "identity_resolution": WorkflowType.IDENTITY_RESOLUTION,
            "orchestrator": WorkflowType.ORCHESTRATOR,
        }
        return mapping.get(gold_name.lower())

    def state_compatibility(self, gold_name: str, v2_states: list[str]) -> dict[str, Any]:
        gold_states = GOLD_WORKFLOW_STATES.get(gold_name.lower(), [])
        if not gold_states:
            return {"compatible": False, "reason": "Unknown Gold workflow"}
        v2_set = set(v2_states)
        gold_set = set(gold_states)
        missing_in_v2 = gold_set - v2_set
        extra_in_v2 = v2_set - gold_set
        return {
            "compatible": len(missing_in_v2) == 0,
            "gold_states": len(gold_states),
            "v2_states": len(v2_states),
            "missing_in_v2": sorted(missing_in_v2),
            "extra_in_v2": sorted(extra_in_v2),
            "coverage_pct": round(len(gold_set & v2_set) / max(len(gold_set), 1) * 100, 1),
        }


@dataclass
class CrosswalkEntry:
    gold_id: str = ""
    v2_component: str = ""
    status: str = "MIGRATED"
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"gold_id": self.gold_id, "v2_component": self.v2_component,
                "status": self.status}


CROSSWALK_ENTRIES: list[CrosswalkEntry] = [
    CrosswalkEntry("GOLD-WF-01", "r6_workflow.WorkflowInstance", "MIGRATED"),
    CrosswalkEntry("GOLD-WF-02", "r6_workflow.NBAEngine", "MIGRATED"),
    CrosswalkEntry("GOLD-WF-03", "r6_workflow.OrchestratorEngine", "MIGRATED"),
    CrosswalkEntry("GOLD-DM-014", "q5_matching.MatchingEngine", "MIGRATED"),
    CrosswalkEntry("GOLD-QUAL-001", "q2_qualification.PriorityEngine", "MIGRATED"),
    CrosswalkEntry("GOLD-CONSENT-001", "r5_relationship.Consent", "MIGRATED"),
    CrosswalkEntry("GOLD-DOS-001", "r4_project.Dossier", "MIGRATED"),
    CrosswalkEntry("GOLD-SERVICE-001", "r3_service.ServiceOrder", "MIGRATED"),
    CrosswalkEntry("GOLD-AGENCY-001", "r2_agency.Agency", "MIGRATED"),
    CrosswalkEntry("GOLD-CRM-001", "r1_crm.LeadScoringEngine", "MIGRATED"),
]
