from __future__ import annotations


def property_profile_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "property_id": row.get("property_id"),
        "property_type": row.get("property_type"),
        "availability_status": row.get("availability_status"),
        "provenance": row.get("provenance"),
    }


def listing_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "listing_key": row.get("listing_key"),
        "property_id": row.get("property_id"),
        "title": row.get("title"),
        "status": row.get("status"),
        "visibility": row.get("visibility"),
        "ai_score": row.get("ai_score"),
        "published_at": row.get("published_at"),
    }


def owner_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row.get("id"), "property_id": row.get("property_id"), "owner_name": row.get("owner_name"), "verified": row.get("verified")}


def document_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row.get("id"), "property_id": row.get("property_id"), "document_type": row.get("document_type"), "title": row.get("title"), "status": row.get("status")}


def valuation_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row.get("id"), "property_id": row.get("property_id"), "amount": row.get("amount"), "currency": row.get("currency"), "confidence": row.get("confidence")}


def verification_dto(row: dict[str, object]) -> dict[str, object]:
    return {"property_id": row.get("property_id"), "trust_score": row.get("trust_score"), "consistency_score": row.get("consistency_score")}


def visit_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row.get("id"), "visit_key": row.get("visit_key"), "property_id": row.get("property_id"), "scheduled_at": row.get("scheduled_at"), "status": row.get("status")}


def negotiation_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row.get("id"), "negotiation_key": row.get("negotiation_key"), "property_id": row.get("property_id"), "status": row.get("status")}


def offer_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row.get("id"), "offer_key": row.get("offer_key"), "amount": row.get("amount"), "status": row.get("status")}


def transaction_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row.get("id"), "transaction_key": row.get("transaction_key"), "property_id": row.get("property_id"), "transaction_type": row.get("transaction_type"), "status": row.get("status")}


def recommendation_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row.get("id"), "recommendation_type": row.get("recommendation_type"), "property_id": row.get("property_id"), "score": row.get("score"), "title": row.get("title")}


def intelligence_dto(scores: dict[str, object]) -> dict[str, object]:
    return {"scores": scores}


def history_dto(row: dict[str, object]) -> dict[str, object]:
    return {"id": row.get("id"), "event_type": row.get("event_type"), "summary": row.get("summary"), "created_at": row.get("created_at")}


def analytics_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"analytics": payload}
