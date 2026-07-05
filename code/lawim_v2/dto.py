from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .conversation_domain import allowed_stage_transitions
from .media_domain import THUMBNAIL_CONTRACT, metadata_dict as media_metadata_dict
from .property_domain import metadata_dict as property_metadata_dict
from .project_domain import metadata_dict as project_metadata_dict


@dataclass(frozen=True, slots=True)
class PaginationMeta:
    page: int
    limit: int
    total: int
    pages: int
    sort: str
    order: str

    def to_dict(self) -> dict[str, int | str]:
        return {
            "page": self.page,
            "limit": self.limit,
            "total": self.total,
            "pages": self.pages,
            "sort": self.sort,
            "order": self.order,
        }


def paginated_payload(items: list[dict[str, object]], *, key: str, pagination: PaginationMeta) -> dict[str, object]:
    return {
        key: items,
        "pagination": pagination.to_dict(),
    }


def user_dto(user: dict[str, object] | None) -> dict[str, object] | None:
    if user is None:
        return None
    return {
        "id": user["id"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "organization_id": user["organization_id"],
        "organization_name": user.get("organization_name"),
        "organization_slug": user.get("organization_slug"),
    }


def organization_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "name": row["name"],
        "slug": row["slug"],
        "kind": row["kind"],
        "city": row.get("city"),
        "created_at": row.get("created_at"),
        "user_count": row.get("user_count", 0),
    }


def property_dto(property_row: dict[str, object]) -> dict[str, object]:
    latitude = property_row.get("latitude")
    longitude = property_row.get("longitude")
    return {
        "id": property_row["id"],
        "listing_code": property_row.get("listing_code"),
        "title": property_row["title"],
        "summary": property_row["summary"],
        "status": property_row["status"],
        "availability": property_row.get("availability", "available"),
        "property_type": property_row["property_type"],
        "price": {
            "min": property_row.get("price_min"),
            "max": property_row.get("price_max"),
            "currency": property_row.get("currency"),
        },
        "ownership": {
            "organization_id": property_row.get("owner_organization_id"),
            "organization_name": property_row.get("owner_organization_name"),
            "organization_slug": property_row.get("owner_organization_slug"),
        },
        "geo": {
            "address_line": property_row.get("address_line"),
            "city": property_row.get("city"),
            "region": property_row.get("region"),
            "postal_code": property_row.get("postal_code"),
            "country": property_row.get("country"),
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude,
            },
            "search_key": property_row.get("search_key"),
        },
        "metrics": {
            "bedrooms": property_row.get("bedrooms"),
            "bathrooms": property_row.get("bathrooms"),
            "area_sqm": property_row.get("area_sqm"),
        },
        "metadata": property_metadata_dict(str(property_row.get("metadata_json") or "{}")),
        "lifecycle": {
            "created_at": property_row.get("created_at"),
            "published_at": property_row.get("published_at"),
            "deleted_at": property_row.get("deleted_at"),
        },
        "version": property_row.get("version", 1),
        "media_count": property_row.get("media_count", 0),
        "conversation_count": property_row.get("conversation_count", 0),
    }


def media_dto(media_row: dict[str, object]) -> dict[str, object]:
    return {
        "id": media_row["id"],
        "property_id": media_row["property_id"],
        "property_title": media_row.get("property_title"),
        "kind": media_row["kind"],
        "url": media_row["url"],
        "caption": media_row["caption"],
        "storage_path": media_row.get("storage_path"),
        "provider": {
            "name": media_row.get("provider_name") or "local",
            "object_id": media_row.get("provider_object_id"),
        },
        "mime_type": media_row.get("mime_type"),
        "size_bytes": media_row.get("size_bytes"),
        "thumbnail": {
            "url": media_row.get("thumbnail_url"),
            "contract": THUMBNAIL_CONTRACT,
        },
        "metadata": media_metadata_dict(str(media_row.get("metadata_json") or "{}")),
        "position": media_row.get("position", 0),
        "lifecycle": {
            "created_at": media_row.get("created_at"),
            "deleted_at": media_row.get("deleted_at"),
        },
        "lifecycle_state": media_row.get("lifecycle_state") or "active",
        "backup_state": media_row.get("backup_state") or "available",
        "version": media_row.get("version", 1),
    }


def geo_location_dto(location: dict[str, object]) -> dict[str, object]:
    payload: dict[str, object] = {
        "kind": location.get("kind") or "city",
        "name": location.get("name") or location.get("display_name") or location.get("city"),
        "city": location.get("city"),
        "region": location.get("region"),
        "department": location.get("department"),
        "country": location.get("country"),
        "property_count": location.get("property_count", 0),
        "search_key": location.get("search_key"),
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
        "confidence": location.get("confidence"),
        "match_score": location.get("match_score"),
    }
    for key in (
        "aliases",
        "typos",
        "landmarks",
        "informal_references",
        "related_zones",
        "target",
        "common_property_types",
        "sources",
        "market_segment",
        "source",
    ):
        value = location.get(key)
        if value is not None:
            payload[key] = value
    return payload


def error_dto(code: str, message: str) -> dict[str, object]:
    return {"error": {"code": code, "message": message}}


def match_dto(match_row: dict[str, object]) -> dict[str, object]:
    property_row = match_row.get("property")
    if isinstance(property_row, dict):
        property_payload = property_dto(property_row)
    else:
        property_payload = property_row
    score = match_row.get("score", 0)
    return {
        "score": score,
        "score_percent": match_row.get("score_percent", score),
        "grade": match_row.get("grade", "weak"),
        "summary": match_row.get("summary", ""),
        "eligible": match_row.get("eligible", True),
        "breakdown": match_row.get("breakdown", {}),
        "reasons": match_row.get("reasons", []),
        "distance_km": match_row.get("distance_km"),
        "weights": match_row.get("weights", {}),
        "property": property_payload,
    }


def message_dto(message_row: dict[str, object]) -> dict[str, object]:
    return {
        "id": message_row["id"],
        "conversation_id": message_row["conversation_id"],
        "body": message_row["body"],
        "sender": {
            "user_id": message_row["sender_user_id"],
            "full_name": message_row.get("sender_name"),
            "email": message_row.get("sender_email"),
        },
        "created_at": message_row.get("created_at"),
    }


def conversation_dto(conversation_row: dict[str, object], *, messages: list[dict[str, object]] | None = None) -> dict[str, object]:
    stage = str(conversation_row.get("negotiation_stage", "inquiry"))
    allowed_stages = allowed_stage_transitions(stage)
    payload: dict[str, object] = {
        "id": conversation_row["id"],
        "subject": conversation_row["subject"],
        "status": conversation_row["status"],
        "negotiation_stage": stage,
        "negotiation": {
            "stage": stage,
            "allowed_stages": allowed_stages,
            "history": [],
        },
        "property": {
            "id": conversation_row.get("property_id"),
            "title": conversation_row.get("property_title"),
        },
        "requester": {
            "user_id": conversation_row["user_id"],
            "full_name": conversation_row.get("requester_name"),
            "email": conversation_row.get("requester_email"),
        },
        "organization": {
            "id": conversation_row.get("organization_id"),
            "name": conversation_row.get("organization_name"),
            "slug": conversation_row.get("organization_slug"),
        },
        "message_count": conversation_row.get("message_count", 0),
        "last_message": conversation_row.get("last_message"),
        "lifecycle": {
            "created_at": conversation_row.get("created_at"),
            "updated_at": conversation_row.get("updated_at"),
        },
    }
    if messages is not None:
        payload["messages"] = [message_dto(item) for item in messages]
        payload["negotiation"] = {
            "stage": stage,
            "allowed_stages": allowed_stages,
            "history": [
                {
                    "type": "message",
                    "id": item["id"],
                    "body": item["body"],
                    "sender_user_id": item["sender_user_id"],
                    "created_at": item.get("created_at"),
                }
                for item in messages
            ],
        }
    return payload


def notification_dto(notification_row: dict[str, object]) -> dict[str, object]:
    from .notification_domain import payload_dict

    return {
        "id": notification_row["id"],
        "kind": notification_row["kind"],
        "title": notification_row["title"],
        "body": notification_row["body"],
        "payload": payload_dict(str(notification_row.get("payload_json") or "{}")),
        "read": notification_row.get("read_at") is not None,
        "read_at": notification_row.get("read_at"),
        "created_at": notification_row.get("created_at"),
    }


def project_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "organization_id": row.get("organization_id"),
        "title": row["title"],
        "project_type": row["project_type"],
        "objective": row["objective"],
        "budget": {
            "min": row.get("budget_min"),
            "max": row.get("budget_max"),
            "currency": row.get("currency", "XAF"),
        },
        "location": {
            "city": row.get("location_city"),
            "region": row.get("location_region"),
            "country": row.get("location_country"),
            "coordinates": {
                "latitude": row.get("location_latitude"),
                "longitude": row.get("location_longitude"),
            },
        },
        "timeline_horizon": row.get("timeline_horizon"),
        "status": row["status"],
        "priority": row.get("priority", "normal"),
        "progress_percent": row.get("progress_percent", 0),
        "metadata": project_metadata_dict(str(row.get("metadata_json") or "{}")),
        "archived_at": row.get("archived_at"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def project_step_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["id"],
        "project_id": row["project_id"],
        "step_key": row["step_key"],
        "title": row["title"],
        "description": row.get("description"),
        "position": row.get("position", 0),
        "status": row["status"],
        "milestone": row.get("milestone"),
        "next_action": row.get("next_action"),
        "completed_at": row.get("completed_at"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def project_progress_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "project_id": row["project_id"],
        "progress_percent": row.get("progress_percent", 0),
        "steps_total": row.get("steps_total", 0),
        "steps_completed": row.get("steps_completed", 0),
        "checklist_total": row.get("checklist_total", 0),
        "checklist_checked": row.get("checklist_checked", 0),
        "status": row.get("status"),
    }


def coerce_sort_field(field: str | None, allowed: set[str], default: str) -> str:
    if not field:
        return default
    normalized = field.strip().lower()
    if normalized not in allowed:
        raise ValueError(f"unsupported sort field: {normalized}")
    return normalized


def coerce_sort_order(order: str | None) -> str:
    if not order:
        return "desc"
    normalized = order.strip().lower()
    if normalized not in {"asc", "desc"}:
        raise ValueError("sort order must be asc or desc")
    return normalized
