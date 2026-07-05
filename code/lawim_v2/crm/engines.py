from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from ..contact import COMPANY_NAME, official_signature_block, to_public_dict
from .constants import LEAD_SCORING_SIGNAL_BONUSES, PIPELINE_STAGES, SCORE_KEYS


class LeadScoringEngine:
    def _lead_context_text(self, lead: dict[str, object]) -> str:
        parts = (
            lead.get("title"),
            lead.get("notes"),
            lead.get("metadata"),
        )
        return self._normalize(" ".join(str(part) for part in parts if part is not None))

    def _signal_bonus(self, lead_text: str) -> int:
        bonus = 0
        for pattern, value in LEAD_SCORING_SIGNAL_BONUSES:
            if re.search(pattern, lead_text):
                bonus += value
        return bonus

    def _normalize(self, text: str | None) -> str:
        return re.sub(r"\s+", " ", str(text or "").strip().lower())

    def compute(self, *, lead: dict[str, object], contact: dict[str, object], communications: int = 0) -> dict[str, int]:
        score = 10
        status = str(lead.get("status") or "new")
        if status in {"qualified", "proposal", "negotiation"}:
            score += 25
        elif status == "contacted":
            score += 15
        if contact.get("email"):
            score += 10
        if contact.get("phone") or contact.get("whatsapp"):
            score += 10
        if contact.get("company"):
            score += 5
        score += min(20, communications * 4)
        score += self._signal_bonus(self._lead_context_text(lead))
        return {"lead_score": min(100, score)}


class PipelineEngine:
    def default_stages(self) -> list[dict[str, object]]:
        return [{"stage_key": key, "label": key.replace("_", " ").title(), "position": idx} for idx, key in enumerate(PIPELINE_STAGES)]

    def stage_index(self, stage_key: str) -> int:
        try:
            return PIPELINE_STAGES.index(stage_key)
        except ValueError:
            return 0

    def advance_stage(self, current_stage: str) -> str | None:
        idx = self.stage_index(current_stage)
        if idx + 1 < len(PIPELINE_STAGES):
            return PIPELINE_STAGES[idx + 1]
        return None

    def kanban_payload(self, *, stages: list[dict[str, object]], items: list[dict[str, object]]) -> list[dict[str, object]]:
        by_stage: dict[int, list[dict[str, object]]] = {}
        for item in items:
            sid = int(item.get("stage_id") or 0)
            by_stage.setdefault(sid, []).append(item)
        board: list[dict[str, object]] = []
        for stage in sorted(stages, key=lambda s: int(s.get("position") or 0)):
            sid = int(stage["id"])
            board.append({"stage": stage, "items": by_stage.get(sid, [])})
        return board


class CommunicationEngine:
    def lawim_sender(self) -> dict[str, str]:
        return to_public_dict()

    def format_outbound_body(self, body: str, *, include_signature: bool = True) -> str:
        text = body.strip()
        if include_signature:
            text = f"{text}\n\n{official_signature_block()}"
        return text

    def whatsapp_payload(self, *, to_number: str, body: str) -> dict[str, object]:
        sender = self.lawim_sender()
        return {
            "from_number": sender["phone_e164"],
            "to_number": to_number,
            "body": self.format_outbound_body(body),
            "lawim_sender_json": sender,
            "channel": "whatsapp",
        }

    def telegram_payload(self, *, to_handle: str, body: str) -> dict[str, object]:
        sender = self.lawim_sender()
        return {
            "from_handle": sender["telegram_bot"],
            "to_handle": to_handle,
            "body": self.format_outbound_body(body),
            "lawim_sender_json": sender,
            "channel": "telegram",
        }

    def email_payload(self, *, to_email: str, subject: str, body: str) -> dict[str, object]:
        sender = self.lawim_sender()
        return {
            "from_email": sender["support_email"],
            "to_email": to_email,
            "subject": subject,
            "body": self.format_outbound_body(body),
            "lawim_sender_json": sender,
            "channel": "email",
        }

    def sms_payload(self, *, to_number: str, body: str) -> dict[str, object]:
        sender = self.lawim_sender()
        short_body = body[:140]
        return {
            "from_number": sender["phone_e164"],
            "to_number": to_number,
            "body": short_body,
            "lawim_sender_json": sender,
            "channel": "sms",
        }


class Customer360Engine:
    def assemble(
        self,
        *,
        contact: dict[str, object],
        leads: list[dict[str, object]],
        customer: dict[str, object] | None,
        opportunities: list[dict[str, object]],
        communications: list[dict[str, object]],
        scores: dict[str, int],
        timeline: list[dict[str, object]],
        journey: list[dict[str, object]],
    ) -> dict[str, object]:
        return {
            "contact": contact,
            "leads": leads,
            "customer": customer,
            "opportunities": opportunities,
            "communications_count": len(communications),
            "recent_communications": communications[:5],
            "scores": scores,
            "timeline": timeline[:20],
            "journey": journey[:20],
            "summary": {
                "full_name": contact.get("full_name"),
                "contact_type": contact.get("contact_type"),
                "is_customer": customer is not None,
                "open_opportunities": sum(1 for o in opportunities if str(o.get("status")) not in {"won", "lost", "closed"}),
                "lead_count": len(leads),
            },
        }


class CampaignEngine:
    def build_audience_filter(self, criteria: dict[str, Any]) -> dict[str, object]:
        return {
            "tags": criteria.get("tags") or [],
            "contact_type": criteria.get("contact_type"),
            "min_score": criteria.get("min_score"),
            "segment_key": criteria.get("segment_key"),
        }

    def personalize_content(self, *, template: str, contact: dict[str, object]) -> str:
        name = str(contact.get("full_name") or "Client")
        return template.replace("{{name}}", name).replace("{{company}}", str(contact.get("company") or COMPANY_NAME))


class SatisfactionEngine:
    def nps_category(self, rating: int) -> str:
        if rating >= 9:
            return "promoter"
        if rating >= 7:
            return "passive"
        return "detractor"

    def csat_score(self, ratings: list[int]) -> float:
        if not ratings:
            return 0.0
        return round(sum(ratings) / len(ratings), 2)

    def survey_summary(self, *, survey_type: str, responses: list[dict[str, object]]) -> dict[str, object]:
        ratings = [int(r.get("rating") or 0) for r in responses]
        summary: dict[str, object] = {"survey_type": survey_type, "response_count": len(responses), "average_rating": self.csat_score(ratings)}
        if survey_type == "nps" and ratings:
            promoters = sum(1 for r in ratings if r >= 9)
            detractors = sum(1 for r in ratings if r <= 6)
            summary["nps"] = round((promoters - detractors) / len(ratings) * 100, 1)
        return summary


class AiIntegrationBridge:
    PROGRAM_SOURCES: tuple[str, ...] = (
        "intelligent_core",
        "ecosystem",
        "cognition",
        "assistant",
        "knowledge_platform",
        "workflow_automation",
        "real_estate_intelligence",
        "source_intelligence",
    )

    def sources(self) -> list[str]:
        return list(self.PROGRAM_SOURCES)

    def suggest_followup(self, *, contact: dict[str, object], last_communication: dict[str, object] | None) -> dict[str, object]:
        channel = str(last_communication.get("channel") if last_communication else "whatsapp")
        return {
            "suggestion_type": "followup",
            "title": f"Relance {channel} recommandée",
            "rationale": f"Contact {contact.get('full_name')} — relance via {channel}",
            "payload": {"channel": channel, "priority": "medium"},
            "sources": self.sources(),
        }

    def suggest_next_action(self, *, lead: dict[str, object]) -> dict[str, object]:
        status = str(lead.get("status") or "new")
        action = "qualify" if status == "new" else "send_proposal" if status == "qualified" else "schedule_call"
        return {
            "suggestion_type": "next_action",
            "title": f"Action suggérée: {action}",
            "rationale": f"Lead en statut {status}",
            "payload": {"action": action},
            "sources": self.sources(),
        }

    def enrich_with_knowledge(self, repository: Any, query: str) -> dict[str, object] | None:
        if hasattr(repository, "expert_rag_query"):
            try:
                return repository.expert_rag_query(query)
            except Exception:
                return None
        return None

    def enrich_with_assistant(self, repository: Any, prompt: str) -> dict[str, object] | None:
        if hasattr(repository, "assistant_chat"):
            try:
                return repository.assistant_chat(prompt)
            except Exception:
                return None
        return None

    def trigger_workflow(self, repository: Any, *, workflow_key: str, context: dict[str, object]) -> dict[str, object] | None:
        if hasattr(repository, "start_automation_instance"):
            try:
                return repository.start_automation_instance(workflow_key=workflow_key, context=context)
            except Exception:
                return None
        return None


class CrmSearchEngine:
    def normalize(self, text: str) -> str:
        lowered = text.lower()
        return re.sub(r"\s+", " ", re.sub(r"[^a-zàâäéèêëïîôùûüç0-9\s@.+]", " ", lowered)).strip()


class CrmAnalyticsEngine:
    def compute_scores(self, *, contact: dict[str, object], communications: int, opportunities: int, days_since_contact: int) -> dict[str, int]:
        engagement = min(100, 20 + communications * 8)
        intent = min(100, 15 + opportunities * 20)
        fit = min(100, 30 + (10 if contact.get("email") else 0) + (10 if contact.get("phone") else 0))
        recency = max(0, 100 - days_since_contact * 3)
        value = min(100, int(contact.get("lifetime_value") or 0) // 10000)
        loyalty = min(100, engagement // 2 + fit // 2)
        risk = max(0, 100 - recency)
        scores = {
            "engagement": engagement,
            "intent": intent,
            "fit": fit,
            "recency": recency,
            "value": value,
            "loyalty": loyalty,
            "risk": risk,
        }
        return {k: scores[k] for k in SCORE_KEYS}


class CrmPlatformEngine:
    def __init__(self) -> None:
        self.lead_scoring = LeadScoringEngine()
        self.pipeline = PipelineEngine()
        self.communication = CommunicationEngine()
        self.customer_360 = Customer360Engine()
        self.campaign = CampaignEngine()
        self.satisfaction = SatisfactionEngine()
        self.ai = AiIntegrationBridge()
        self.search = CrmSearchEngine()
        self.analytics = CrmAnalyticsEngine()

    def integration_sources(self) -> list[str]:
        return self.ai.sources()

    def days_since(self, iso_timestamp: str | None) -> int:
        if not iso_timestamp:
            return 999
        try:
            dt = datetime.fromisoformat(str(iso_timestamp).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            delta = datetime.now(timezone.utc) - dt
            return max(0, delta.days)
        except ValueError:
            return 999
