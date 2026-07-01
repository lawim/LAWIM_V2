from __future__ import annotations


def partner_registration_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "registration_key": row.get("registration_key"),
        "partner_profile_id": row.get("partner_profile_id"),
        "organization_id": row.get("organization_id"),
        "applicant_name": row.get("applicant_name"),
        "applicant_email": row.get("applicant_email"),
        "applicant_phone": row.get("applicant_phone"),
        "provider_type": row.get("provider_type"),
        "status": row.get("status"),
    }


def provider_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "provider_key": row.get("provider_key"),
        "partner_profile_id": row.get("partner_profile_id"),
        "provider_type": row.get("provider_type"),
        "headline": row.get("headline"),
        "bio": row.get("bio"),
        "service_radius_km": row.get("service_radius_km"),
        "status": row.get("status"),
        "featured": row.get("featured"),
    }


def provider_certification_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "provider_profile_id": row.get("provider_profile_id"),
        "certification_key": row.get("certification_key"),
        "title": row.get("title"),
        "issuer": row.get("issuer"),
        "status": row.get("status"),
    }


def catalog_category_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "category_key": row.get("category_key"),
        "name": row.get("name"),
        "description": row.get("description"),
        "parent_id": row.get("parent_id"),
        "position": row.get("position"),
        "status": row.get("status"),
    }


def catalog_item_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "item_key": row.get("item_key"),
        "category_id": row.get("category_id"),
        "service_catalog_id": row.get("service_catalog_id"),
        "provider_profile_id": row.get("provider_profile_id"),
        "title": row.get("title"),
        "description": row.get("description"),
        "category": row.get("category"),
        "price_min": row.get("price_min"),
        "price_max": row.get("price_max"),
        "currency": row.get("currency"),
        "status": row.get("status"),
    }


def service_request_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "request_key": row.get("request_key"),
        "user_id": row.get("user_id"),
        "contact_id": row.get("contact_id"),
        "project_id": row.get("project_id"),
        "property_id": row.get("property_id"),
        "catalog_item_id": row.get("catalog_item_id"),
        "title": row.get("title"),
        "description": row.get("description"),
        "category": row.get("category"),
        "city": row.get("city"),
        "region": row.get("region"),
        "status": row.get("status"),
        "budget_min": row.get("budget_min"),
        "budget_max": row.get("budget_max"),
        "currency": row.get("currency"),
    }


def request_document_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "request_id": row.get("request_id"),
        "document_key": row.get("document_key"),
        "title": row.get("title"),
        "document_type": row.get("document_type"),
        "status": row.get("status"),
    }


def quote_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "quote_key": row.get("quote_key"),
        "request_id": row.get("request_id"),
        "provider_profile_id": row.get("provider_profile_id"),
        "status": row.get("status"),
        "amount": row.get("amount"),
        "currency": row.get("currency"),
        "valid_until": row.get("valid_until"),
    }


def quote_line_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "quote_id": row.get("quote_id"),
        "line_key": row.get("line_key"),
        "description": row.get("description"),
        "quantity": row.get("quantity"),
        "unit_price": row.get("unit_price"),
        "amount": row.get("amount"),
    }


def contract_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "contract_key": row.get("contract_key"),
        "request_id": row.get("request_id"),
        "quote_id": row.get("quote_id"),
        "provider_profile_id": row.get("provider_profile_id"),
        "status": row.get("status"),
        "amount": row.get("amount"),
        "currency": row.get("currency"),
        "signed_at": row.get("signed_at"),
    }


def contract_document_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "contract_id": row.get("contract_id"),
        "document_key": row.get("document_key"),
        "title": row.get("title"),
        "document_type": row.get("document_type"),
        "status": row.get("status"),
    }


def mission_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "mission_key": row.get("mission_key"),
        "contract_id": row.get("contract_id"),
        "provider_profile_id": row.get("provider_profile_id"),
        "title": row.get("title"),
        "status": row.get("status"),
        "progress_percent": row.get("progress_percent"),
        "scheduled_start": row.get("scheduled_start"),
        "scheduled_end": row.get("scheduled_end"),
    }


def mission_milestone_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "mission_id": row.get("mission_id"),
        "milestone_key": row.get("milestone_key"),
        "title": row.get("title"),
        "status": row.get("status"),
        "due_at": row.get("due_at"),
        "position": row.get("position"),
    }


def mission_deliverable_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "mission_id": row.get("mission_id"),
        "deliverable_key": row.get("deliverable_key"),
        "title": row.get("title"),
        "status": row.get("status"),
    }


def availability_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "provider_profile_id": row.get("provider_profile_id"),
        "day_of_week": row.get("day_of_week"),
        "start_time": row.get("start_time"),
        "end_time": row.get("end_time"),
        "timezone": row.get("timezone"),
        "status": row.get("status"),
    }


def review_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "review_key": row.get("review_key"),
        "provider_profile_id": row.get("provider_profile_id"),
        "mission_id": row.get("mission_id"),
        "rating": row.get("rating"),
        "title": row.get("title"),
        "body": row.get("body"),
        "status": row.get("status"),
    }


def review_moderation_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "review_id": row.get("review_id"),
        "action": row.get("action"),
        "reason": row.get("reason"),
    }


def reputation_dto(scores: dict[str, int]) -> dict[str, object]:
    return {"scores": scores}


def dispute_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "dispute_key": row.get("dispute_key"),
        "contract_id": row.get("contract_id"),
        "mission_id": row.get("mission_id"),
        "status": row.get("status"),
        "reason": row.get("reason"),
        "resolution": row.get("resolution"),
    }


def dispute_message_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "dispute_id": row.get("dispute_id"),
        "message": row.get("message"),
        "visibility": row.get("visibility"),
        "created_at": row.get("created_at"),
    }


def subscription_plan_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "plan_key": row.get("plan_key"),
        "name": row.get("name"),
        "price": row.get("price"),
        "currency": row.get("currency"),
        "billing_period": row.get("billing_period"),
        "status": row.get("status"),
    }


def subscription_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "subscription_key": row.get("subscription_key"),
        "plan_id": row.get("plan_id"),
        "provider_profile_id": row.get("provider_profile_id"),
        "user_id": row.get("user_id"),
        "status": row.get("status"),
        "started_at": row.get("started_at"),
        "ends_at": row.get("ends_at"),
    }


def commission_rule_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "rule_key": row.get("rule_key"),
        "name": row.get("name"),
        "commission_type": row.get("commission_type"),
        "rate_percent": row.get("rate_percent"),
        "flat_amount": row.get("flat_amount"),
        "status": row.get("status"),
    }


def commission_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "commission_key": row.get("commission_key"),
        "contract_id": row.get("contract_id"),
        "commission_type": row.get("commission_type"),
        "amount": row.get("amount"),
        "currency": row.get("currency"),
        "status": row.get("status"),
    }


def payment_preparation_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "preparation_key": row.get("preparation_key"),
        "contract_id": row.get("contract_id"),
        "subscription_id": row.get("subscription_id"),
        "payment_method": row.get("payment_method"),
        "amount": row.get("amount"),
        "currency": row.get("currency"),
        "status": row.get("status"),
    }


def matching_session_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "session_key": row.get("session_key"),
        "request_id": row.get("request_id"),
        "status": row.get("status"),
        "result_count": row.get("result_count"),
        "started_at": row.get("started_at"),
        "completed_at": row.get("completed_at"),
    }


def matching_result_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "session_id": row.get("session_id"),
        "provider_profile_id": row.get("provider_profile_id"),
        "partner_profile_id": row.get("partner_profile_id"),
        "score": row.get("score"),
        "rank": row.get("rank"),
    }


def portfolio_item_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "portfolio_key": row.get("portfolio_key"),
        "provider_profile_id": row.get("provider_profile_id"),
        "title": row.get("title"),
        "category": row.get("category"),
        "status": row.get("status"),
    }


def ai_recommendation_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "recommendation_key": row.get("recommendation_key"),
        "recommendation_type": row.get("recommendation_type"),
        "provider_profile_id": row.get("provider_profile_id"),
        "title": row.get("title"),
        "rationale": row.get("rationale"),
        "score": row.get("score"),
        "status": row.get("status"),
    }


def dashboard_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"dashboard": payload}


def analytics_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"analytics": payload}


def provider_bundle_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"provider": payload}
