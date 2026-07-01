from __future__ import annotations


def contact_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "contact_key": row.get("contact_key"),
        "contact_type": row.get("contact_type"),
        "full_name": row.get("full_name"),
        "email": row.get("email"),
        "phone": row.get("phone"),
        "whatsapp": row.get("whatsapp"),
        "telegram": row.get("telegram"),
        "company": row.get("company"),
        "country": row.get("country"),
    }


def lead_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "lead_key": row.get("lead_key"),
        "contact_id": row.get("contact_id"),
        "status": row.get("status"),
        "score": row.get("score"),
        "title": row.get("title"),
        "source_id": row.get("source_id"),
        "assigned_user_id": row.get("assigned_user_id"),
    }


def customer_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "customer_key": row.get("customer_key"),
        "contact_id": row.get("contact_id"),
        "status": row.get("status"),
        "lifetime_value": row.get("lifetime_value"),
    }


def opportunity_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "opportunity_key": row.get("opportunity_key"),
        "contact_id": row.get("contact_id"),
        "customer_id": row.get("customer_id"),
        "title": row.get("title"),
        "status": row.get("status"),
        "amount": row.get("amount"),
        "currency": row.get("currency"),
        "probability": row.get("probability"),
    }


def pipeline_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "pipeline_key": row.get("pipeline_key"),
        "name": row.get("name"),
        "is_default": row.get("is_default"),
    }


def pipeline_stage_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "pipeline_id": row.get("pipeline_id"),
        "stage_key": row.get("stage_key"),
        "label": row.get("label"),
        "position": row.get("position"),
    }


def pipeline_item_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "pipeline_id": row.get("pipeline_id"),
        "stage_id": row.get("stage_id"),
        "entity_type": row.get("entity_type"),
        "entity_id": row.get("entity_id"),
        "position": row.get("position"),
    }


def communication_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "communication_key": row.get("communication_key"),
        "contact_id": row.get("contact_id"),
        "channel": row.get("channel"),
        "direction": row.get("direction"),
        "status": row.get("status"),
        "subject": row.get("subject"),
        "sent_at": row.get("sent_at"),
    }


def whatsapp_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "communication_id": row.get("communication_id"),
        "contact_id": row.get("contact_id"),
        "from_number": row.get("from_number"),
        "to_number": row.get("to_number"),
        "body": row.get("body"),
        "status": row.get("status"),
    }


def telegram_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "communication_id": row.get("communication_id"),
        "contact_id": row.get("contact_id"),
        "from_handle": row.get("from_handle"),
        "to_handle": row.get("to_handle"),
        "body": row.get("body"),
        "status": row.get("status"),
    }


def email_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "communication_id": row.get("communication_id"),
        "contact_id": row.get("contact_id"),
        "from_email": row.get("from_email"),
        "to_email": row.get("to_email"),
        "subject": row.get("subject"),
        "status": row.get("status"),
    }


def sms_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "communication_id": row.get("communication_id"),
        "contact_id": row.get("contact_id"),
        "from_number": row.get("from_number"),
        "to_number": row.get("to_number"),
        "body": row.get("body"),
        "status": row.get("status"),
    }


def campaign_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "campaign_key": row.get("campaign_key"),
        "name": row.get("name"),
        "channel": row.get("channel"),
        "status": row.get("status"),
        "scheduled_at": row.get("scheduled_at"),
    }


def segment_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "segment_key": row.get("segment_key"),
        "name": row.get("name"),
    }


def score_dto(scores: dict[str, int]) -> dict[str, object]:
    return {"scores": scores}


def satisfaction_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"satisfaction": payload}


def reminder_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "reminder_key": row.get("reminder_key"),
        "contact_id": row.get("contact_id"),
        "title": row.get("title"),
        "due_at": row.get("due_at"),
        "status": row.get("status"),
    }


def followup_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "followup_key": row.get("followup_key"),
        "contact_id": row.get("contact_id"),
        "channel": row.get("channel"),
        "scheduled_at": row.get("scheduled_at"),
        "status": row.get("status"),
    }


def timeline_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "entry_type": row.get("entry_type"),
        "summary": row.get("summary"),
        "reference_type": row.get("reference_type"),
        "reference_id": row.get("reference_id"),
        "created_at": row.get("created_at"),
    }


def journey_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "event_type": row.get("event_type"),
        "summary": row.get("summary"),
        "created_at": row.get("created_at"),
    }


def note_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "note_key": row.get("note_key"),
        "contact_id": row.get("contact_id"),
        "content": row.get("content"),
        "visibility": row.get("visibility"),
    }


def customer_360_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"customer_360": payload}


def dashboard_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"dashboard": payload}


def analytics_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"analytics": payload}


def ai_suggestion_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "suggestion_key": row.get("suggestion_key"),
        "suggestion_type": row.get("suggestion_type"),
        "title": row.get("title"),
        "rationale": row.get("rationale"),
        "status": row.get("status"),
    }
