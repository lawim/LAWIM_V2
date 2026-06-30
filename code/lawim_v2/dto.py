from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .geo_domain import build_geo_dto
from .media_domain import THUMBNAIL_CONTRACT, metadata_dict as media_metadata_dict
from .property_domain import metadata_dict as property_metadata_dict


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


def property_dto(property_row: dict[str, object]) -> dict[str, object]:
    geo = build_geo_dto(
        city=str(property_row.get("city") or ""),
        country=str(property_row.get("country") or ""),
        latitude=property_row.get("latitude"),  # type: ignore[arg-type]
        longitude=property_row.get("longitude"),  # type: ignore[arg-type]
        region=property_row.get("region"),  # type: ignore[arg-type]
        address_line=property_row.get("address_line"),  # type: ignore[arg-type]
        postal_code=property_row.get("postal_code"),  # type: ignore[arg-type]
    )
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
        "geo": geo,
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
        "version": media_row.get("version", 1),
    }


def geo_location_dto(location: dict[str, object]) -> dict[str, object]:
    return {
        "city": location.get("city"),
        "region": location.get("region"),
        "country": location.get("country"),
        "property_count": location.get("property_count", 0),
        "search_key": location.get("search_key"),
    }


def error_dto(code: str, message: str) -> dict[str, object]:
    return {"error": {"code": code, "message": message}}


def match_dto(match_row: dict[str, object]) -> dict[str, object]:
    property_row = match_row.get("property")
    if isinstance(property_row, dict):
        property_payload = property_dto(property_row)
    else:
        property_payload = property_row
    return {
        "score": match_row.get("score", 0),
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
    payload: dict[str, object] = {
        "id": conversation_row["id"],
        "subject": conversation_row["subject"],
        "status": conversation_row["status"],
        "negotiation_stage": conversation_row.get("negotiation_stage", "inquiry"),
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
