from __future__ import annotations

from ..contact import to_public_dict
from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as cdto


class CrmService:
    def __init__(self, repository, project_service: ProjectService, policy) -> None:
        self.repository = repository
        self.projects = project_service
        self.policy = policy

    def _require_auth(self, actor: dict[str, object] | None) -> None:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")

    def _require_admin(self, actor: dict[str, object]) -> None:
        if not self.policy.is_admin(actor):
            raise ProjectPermissionDenied("Admin required")

    # --- Contacts ---

    def list_contacts(self, *, actor: dict[str, object], contact_type: str | None = None, limit: int = 50) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("crm_contact_list")
        METRICS.increment("contact_list")
        return {"contacts": [cdto.contact_dto(r) for r in self.repository.list_crm_contacts(contact_type=contact_type, limit=limit)]}

    def get_contact(self, *, actor: dict[str, object], contact_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("contact_detail")
        return {"contact": cdto.contact_dto(self.repository.get_crm_contact(contact_id))}

    def create_contact(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        contact = self.repository.create_crm_contact(
            full_name=str(body["full_name"]),
            contact_type=str(body.get("contact_type") or "individual"),
            email=str(body.get("email") or ""),
            phone=str(body.get("phone") or ""),
            whatsapp=str(body.get("whatsapp") or ""),
            telegram=str(body.get("telegram") or ""),
            company=str(body.get("company") or ""),
            country=str(body.get("country") or "Cameroon"),
        )
        METRICS.increment("crm_contact_created")
        METRICS.increment("contact_created")
        return {"contact": cdto.contact_dto(contact)}

    def update_contact(self, *, actor: dict[str, object], contact_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        contact = self.repository.update_crm_contact(contact_id, **body)
        METRICS.increment("contact_updated")
        return {"contact": cdto.contact_dto(contact)}

    def delete_contact(self, *, actor: dict[str, object], contact_id: int) -> dict[str, object]:
        self._require_admin(actor)
        self.repository.delete_crm_contact(contact_id)
        METRICS.increment("contact_deleted")
        return {"deleted": True, "contact_id": contact_id}

    def add_contact_tag(self, *, actor: dict[str, object], contact_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        tag = self.repository.add_crm_contact_tag(contact_id, str(body["tag"]))
        return {"tag": tag}

    def grant_consent(self, *, actor: dict[str, object], contact_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        consent = self.repository.grant_crm_consent(contact_id, consent_type=str(body.get("consent_type") or "marketing"))
        return {"consent": consent}

    # --- Leads ---

    def list_leads(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("crm_lead_list")
        METRICS.increment("lead_list")
        return {"leads": [cdto.lead_dto(r) for r in self.repository.list_crm_leads(status=status)]}

    def get_lead(self, *, actor: dict[str, object], lead_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("lead_detail")
        return {"lead": cdto.lead_dto(self.repository.get_crm_lead(lead_id))}

    def create_lead(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        lead = self.repository.create_crm_lead(
            contact_id=int(body["contact_id"]),
            title=str(body.get("title") or ""),
            status=str(body.get("status") or "new"),
            source_id=int(body["source_id"]) if body.get("source_id") is not None else None,
            notes=str(body.get("notes") or ""),
        )
        METRICS.increment("crm_lead_created")
        METRICS.increment("lead_created")
        return {"lead": cdto.lead_dto(lead)}

    def update_lead(self, *, actor: dict[str, object], lead_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        lead = self.repository.update_crm_lead(lead_id, **body)
        METRICS.increment("lead_updated")
        return {"lead": cdto.lead_dto(lead)}

    def convert_lead(self, *, actor: dict[str, object], lead_id: int, body: dict[str, object] | None = None) -> dict[str, object]:
        self._require_auth(actor)
        roles = list(body.get("roles") or ["buyer"]) if body else ["buyer"]
        customer = self.repository.convert_crm_lead_to_customer(lead_id, roles=roles)
        METRICS.increment("lead_converted")
        METRICS.increment("customer_created")
        return {"customer": cdto.customer_dto(customer)}

    def list_lead_sources(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return {"sources": self.repository.list_crm_lead_sources()}

    # --- Customers ---

    def list_customers(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("crm_customer_list")
        METRICS.increment("customer_list")
        return {"customers": [cdto.customer_dto(r) for r in self.repository.list_crm_customers(status=status)]}

    def get_customer(self, *, actor: dict[str, object], customer_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("customer_detail")
        return {"customer": cdto.customer_dto(self.repository.get_crm_customer(customer_id))}

    def create_customer(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        roles = list(body.get("roles") or ["buyer"])
        customer = self.repository.create_crm_customer(contact_id=int(body["contact_id"]), roles=roles)
        METRICS.increment("crm_customer_created")
        METRICS.increment("customer_created")
        return {"customer": cdto.customer_dto(customer)}

    def update_customer(self, *, actor: dict[str, object], customer_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        customer = self.repository.update_crm_customer(customer_id, **body)
        METRICS.increment("customer_updated")
        return {"customer": cdto.customer_dto(customer)}

    def customer_360(self, *, actor: dict[str, object], contact_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("customer_360")
        return cdto.customer_360_dto(self.repository.customer_360(contact_id))

    # --- Opportunities ---

    def list_opportunities(self, *, actor: dict[str, object], contact_id: int | None = None, status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"opportunities": [cdto.opportunity_dto(r) for r in self.repository.list_crm_opportunities(contact_id=contact_id, status=status)]}

    def create_opportunity(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        opp = self.repository.create_crm_opportunity(
            contact_id=int(body["contact_id"]),
            title=str(body["title"]),
            customer_id=int(body["customer_id"]) if body.get("customer_id") is not None else None,
            amount=int(body["amount"]) if body.get("amount") is not None else None,
            currency=str(body.get("currency") or "XAF"),
            status=str(body.get("status") or "open"),
            probability=int(body.get("probability") or 50),
        )
        return {"opportunity": cdto.opportunity_dto(opp)}

    def update_opportunity(self, *, actor: dict[str, object], opportunity_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        opp = self.repository.update_crm_opportunity(opportunity_id, **body)
        return {"opportunity": cdto.opportunity_dto(opp)}

    # --- Pipelines ---

    def list_pipelines(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("pipeline_list")
        return {"pipelines": [cdto.pipeline_dto(r) for r in self.repository.list_crm_pipelines()]}

    def create_pipeline(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        pipeline = self.repository.create_crm_pipeline(name=str(body["name"]), is_default=bool(body.get("is_default")))
        METRICS.increment("pipeline_created")
        return {"pipeline": cdto.pipeline_dto(pipeline)}

    def pipeline_board(self, *, actor: dict[str, object], pipeline_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("pipeline_board")
        return {"board": self.repository.get_crm_pipeline_board(pipeline_id)}

    def move_pipeline_item(self, *, actor: dict[str, object], item_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        item = self.repository.move_crm_pipeline_item(item_id, stage_id=int(body["stage_id"]), position=int(body.get("position") or 0))
        METRICS.increment("pipeline_item_moved")
        return {"item": cdto.pipeline_item_dto(item)}

    def advance_pipeline_item(self, *, actor: dict[str, object], item_id: int) -> dict[str, object]:
        self._require_auth(actor)
        item = self.repository.advance_crm_pipeline_item(item_id)
        METRICS.increment("pipeline_item_advanced")
        return {"item": cdto.pipeline_item_dto(item)}

    # --- Communications ---

    def list_communications(self, *, actor: dict[str, object], contact_id: int | None = None, channel: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_list")
        return {"communications": [cdto.communication_dto(r) for r in self.repository.list_crm_communications(contact_id=contact_id, channel=channel)]}

    def send_whatsapp(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        msg = self.repository.send_crm_whatsapp(
            contact_id=int(body["contact_id"]),
            body=str(body["body"]),
            to_number=str(body["to_number"]) if body.get("to_number") else None,
        )
        METRICS.increment("crm_whatsapp_sent")
        METRICS.increment("whatsapp_sent")
        METRICS.increment("communication_sent")
        return {"message": cdto.whatsapp_dto(msg)}

    def send_telegram(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        msg = self.repository.send_crm_telegram(
            contact_id=int(body["contact_id"]),
            body=str(body["body"]),
            to_handle=str(body["to_handle"]) if body.get("to_handle") else None,
        )
        METRICS.increment("crm_telegram_sent")
        METRICS.increment("telegram_sent")
        METRICS.increment("communication_sent")
        return {"message": cdto.telegram_dto(msg)}

    def send_email(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        msg = self.repository.send_crm_email(
            contact_id=int(body["contact_id"]),
            subject=str(body.get("subject") or "LAWIM"),
            body=str(body["body"]),
            to_email=str(body["to_email"]) if body.get("to_email") else None,
        )
        METRICS.increment("crm_email_sent")
        METRICS.increment("email_sent")
        METRICS.increment("communication_sent")
        return {"message": cdto.email_dto(msg)}

    def send_sms(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        msg = self.repository.send_crm_sms(
            contact_id=int(body["contact_id"]),
            body=str(body["body"]),
            to_number=str(body["to_number"]) if body.get("to_number") else None,
        )
        METRICS.increment("crm_sms_sent")
        METRICS.increment("sms_sent")
        METRICS.increment("communication_sent")
        return {"message": cdto.sms_dto(msg)}

    def official_contact(self, *, actor: dict[str, object] | None = None) -> dict[str, object]:
        if actor is not None:
            self._require_auth(actor)
        return {"contact": to_public_dict()}

    # --- Reminders & Followups ---

    def list_reminders(self, *, actor: dict[str, object], contact_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"reminders": [cdto.reminder_dto(r) for r in self.repository.list_crm_reminders(contact_id=contact_id)]}

    def create_reminder(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        reminder = self.repository.create_crm_reminder(
            contact_id=int(body["contact_id"]),
            title=str(body["title"]),
            due_at=str(body["due_at"]),
            assigned_user_id=user_id,
        )
        return {"reminder": cdto.reminder_dto(reminder)}

    def list_followups(self, *, actor: dict[str, object], contact_id: int | None = None, status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("followup_list")
        return {"followups": [cdto.followup_dto(r) for r in self.repository.list_crm_followups(contact_id=contact_id, status=status)]}

    def schedule_followup(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        followup = self.repository.schedule_crm_followup(
            contact_id=int(body["contact_id"]),
            scheduled_at=str(body["scheduled_at"]),
            channel=str(body.get("channel") or "whatsapp"),
            lead_id=int(body["lead_id"]) if body.get("lead_id") is not None else None,
            opportunity_id=int(body["opportunity_id"]) if body.get("opportunity_id") is not None else None,
            notes=str(body.get("notes") or ""),
        )
        METRICS.increment("followup_scheduled")
        METRICS.increment("crm_followup_scheduled")
        return {"followup": cdto.followup_dto(followup)}

    def complete_followup(self, *, actor: dict[str, object], followup_id: int) -> dict[str, object]:
        self._require_auth(actor)
        followup = self.repository.complete_crm_followup(followup_id)
        METRICS.increment("followup_completed")
        return {"followup": cdto.followup_dto(followup)}

    # --- Campaigns & Segments ---

    def list_campaigns(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("campaign_list")
        return {"campaigns": [cdto.campaign_dto(r) for r in self.repository.list_crm_campaigns(status=status)]}

    def create_campaign(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        campaign = self.repository.create_crm_campaign(
            name=str(body["name"]),
            channel=str(body.get("channel") or "email"),
            audience=dict(body.get("audience") or {}),
            content=dict(body.get("content") or {}),
        )
        METRICS.increment("campaign_created")
        METRICS.increment("crm_campaign_created")
        return {"campaign": cdto.campaign_dto(campaign)}

    def launch_campaign(self, *, actor: dict[str, object], campaign_id: int) -> dict[str, object]:
        self._require_admin(actor)
        result = self.repository.launch_crm_campaign(campaign_id)
        METRICS.increment("campaign_launched")
        METRICS.increment("crm_campaign_launched")
        return result

    def list_segments(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return {"segments": [cdto.segment_dto(r) for r in self.repository.list_crm_segments()]}

    def create_segment(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        segment = self.repository.create_crm_segment(name=str(body["name"]), criteria=dict(body.get("criteria") or {}))
        return {"segment": cdto.segment_dto(segment)}

    # --- Scoring & Satisfaction ---

    def scores(self, *, actor: dict[str, object], contact_id: int) -> dict[str, object]:
        self._require_auth(actor)
        scores = self.repository.get_crm_customer_scores(contact_id)
        METRICS.increment("crm_score_computed")
        return cdto.score_dto(scores)

    def compute_scores(self, *, actor: dict[str, object], contact_id: int) -> dict[str, object]:
        self._require_auth(actor)
        scores = self.repository.compute_crm_customer_scores(contact_id)
        METRICS.increment("crm_score_computed")
        return cdto.score_dto(scores)

    def satisfaction_surveys(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return {"surveys": self.repository.list_crm_satisfaction_surveys()}

    def submit_satisfaction(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        response = self.repository.submit_crm_satisfaction_response(
            survey_id=int(body["survey_id"]),
            contact_id=int(body["contact_id"]),
            rating=int(body.get("rating") or 3),
            answers=dict(body.get("answers") or {}),
        )
        return {"response": response}

    def satisfaction_summary(self, *, actor: dict[str, object], survey_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return cdto.satisfaction_dto(self.repository.crm_satisfaction_summary(survey_id))

    # --- Journey / Timeline / Notes ---

    def timeline(self, *, actor: dict[str, object], contact_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("journey_timeline")
        return {"timeline": [cdto.timeline_dto(r) for r in self.repository.list_crm_timeline(contact_id)]}

    def journey(self, *, actor: dict[str, object], contact_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("journey_events")
        return {"journey": [cdto.journey_dto(r) for r in self.repository.list_crm_journey(contact_id)]}

    def add_note(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        author_id = int(actor["id"]) if actor.get("id") is not None else None
        note = self.repository.add_crm_note(
            contact_id=int(body["contact_id"]),
            content=str(body["content"]),
            author_id=author_id,
            visibility=str(body.get("visibility") or "internal"),
        )
        return {"note": cdto.note_dto(note)}

    def list_notes(self, *, actor: dict[str, object], contact_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"notes": [cdto.note_dto(r) for r in self.repository.list_crm_notes(contact_id)]}

    # --- AI Suggestions ---

    def ai_suggestions(self, *, actor: dict[str, object], contact_id: int) -> dict[str, object]:
        self._require_auth(actor)
        suggestions = self.repository.generate_crm_ai_suggestions(contact_id)
        METRICS.increment("crm_ai_suggestion")
        return {"suggestions": [cdto.ai_suggestion_dto(r) for r in suggestions]}

    def list_ai_suggestions(self, *, actor: dict[str, object], contact_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"suggestions": [cdto.ai_suggestion_dto(r) for r in self.repository.list_crm_ai_suggestions(contact_id=contact_id)]}

    # --- Search / Analytics / Dashboard ---

    def search(self, *, actor: dict[str, object], query: str, limit: int = 20) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("crm_search")
        return {"results": [cdto.contact_dto(r) for r in self.repository.crm_search(query=query, limit=limit)]}

    def analytics(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("crm_analytics")
        METRICS.increment("analytics_view")
        return cdto.analytics_dto(self.repository.crm_analytics())

    def stats(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("crm_stats")
        return {"stats": self.repository.crm_stats()}

    def dashboard(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("crm_dashboard")
        return cdto.dashboard_dto(self.repository.crm_dashboard())

    def seed_catalog(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        self.repository.seed_crm_catalog()
        METRICS.increment("crm_catalog_seeded")
        return {"seeded": True}
