from __future__ import annotations


def message_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "message_key": row.get("message_key"),
        "thread_id": row.get("thread_id"),
        "channel_type": row.get("channel_type"),
        "direction": row.get("direction"),
        "priority": row.get("priority"),
        "status": row.get("status"),
        "subject": row.get("subject"),
        "body": row.get("body"),
        "sender_user_id": row.get("sender_user_id"),
        "recipient_user_id": row.get("recipient_user_id"),
        "contact_id": row.get("contact_id"),
        "organization_id": row.get("organization_id"),
        "scheduled_at": row.get("scheduled_at"),
        "sent_at": row.get("sent_at"),
        "created_at": row.get("created_at"),
    }


def thread_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "thread_key": row.get("thread_key"),
        "channel_id": row.get("channel_id"),
        "subject": row.get("subject"),
        "status": row.get("status"),
        "organization_id": row.get("organization_id"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def channel_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "channel_key": row.get("channel_key"),
        "channel_type": row.get("channel_type"),
        "name": row.get("name"),
        "provider": row.get("provider"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def notification_event_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "event_key": row.get("event_key"),
        "notification_type": row.get("notification_type"),
        "user_id": row.get("user_id"),
        "contact_id": row.get("contact_id"),
        "title": row.get("title"),
        "body": row.get("body"),
        "priority": row.get("priority"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def notification_rule_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "rule_key": row.get("rule_key"),
        "name": row.get("name"),
        "event_kind": row.get("event_kind"),
        "channel_type": row.get("channel_type"),
        "status": row.get("status"),
    }


def template_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "template_key": row.get("template_key"),
        "name": row.get("name"),
        "channel_type": row.get("channel_type"),
        "subject": row.get("subject"),
        "body": row.get("body"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def campaign_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "campaign_key": row.get("campaign_key"),
        "name": row.get("name"),
        "campaign_type": row.get("campaign_type"),
        "campaign_status": row.get("campaign_status"),
        "organization_id": row.get("organization_id"),
        "scheduled_at": row.get("scheduled_at"),
        "started_at": row.get("started_at"),
        "completed_at": row.get("completed_at"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def queue_job_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "job_key": row.get("job_key"),
        "job_type": row.get("job_type"),
        "channel_type": row.get("channel_type"),
        "priority": row.get("priority"),
        "job_status": row.get("job_status"),
        "attempt_count": row.get("attempt_count"),
        "max_attempts": row.get("max_attempts"),
        "scheduled_at": row.get("scheduled_at"),
        "created_at": row.get("created_at"),
    }


def preference_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "preference_key": row.get("preference_key"),
        "user_id": row.get("user_id"),
        "contact_id": row.get("contact_id"),
        "channel_type": row.get("channel_type"),
        "enabled": row.get("enabled"),
        "status": row.get("status"),
        "updated_at": row.get("updated_at"),
    }


def email_message_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "message_key": row.get("message_key"),
        "to_email": row.get("to_email"),
        "from_email": row.get("from_email"),
        "subject": row.get("subject"),
        "email_status": row.get("email_status"),
        "sent_at": row.get("sent_at"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def sms_message_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "message_key": row.get("message_key"),
        "to_number": row.get("to_number"),
        "from_number": row.get("from_number"),
        "body": row.get("body"),
        "sms_status": row.get("sms_status"),
        "sent_at": row.get("sent_at"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def whatsapp_message_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "message_key": row.get("message_key"),
        "to_number": row.get("to_number"),
        "body": row.get("body"),
        "whatsapp_status": row.get("whatsapp_status"),
        "sent_at": row.get("sent_at"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def telegram_message_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "message_key": row.get("message_key"),
        "chat_id": row.get("chat_id"),
        "body": row.get("body"),
        "telegram_status": row.get("telegram_status"),
        "sent_at": row.get("sent_at"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def push_notification_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "notification_key": row.get("notification_key"),
        "title": row.get("title"),
        "body": row.get("body"),
        "push_status": row.get("push_status"),
        "sent_at": row.get("sent_at"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def event_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "event_key": row.get("event_key"),
        "event_kind": row.get("event_kind"),
        "source_program": row.get("source_program"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def history_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "history_key": row.get("history_key"),
        "message_id": row.get("message_id"),
        "action": row.get("action"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def group_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "group_key": row.get("group_key"),
        "name": row.get("name"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def inapp_notification_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "notification_key": row.get("notification_key"),
        "user_id": row.get("user_id"),
        "title": row.get("title"),
        "body": row.get("body"),
        "read_at": row.get("read_at"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def delivery_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "delivery_key": row.get("delivery_key"),
        "channel_type": row.get("channel_type"),
        "delivery_status": row.get("delivery_status"),
        "delivered_at": row.get("delivered_at"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def ai_recommendation_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "recommendation_key": row.get("recommendation_key"),
        "user_id": row.get("user_id"),
        "contact_id": row.get("contact_id"),
        "recommendation_type": row.get("recommendation_type"),
        "score": row.get("score"),
        "generated_at": row.get("generated_at"),
        "status": row.get("status"),
    }


def dashboard_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"dashboard": payload}


def analytics_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"analytics": payload}


def stats_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"stats": payload}
