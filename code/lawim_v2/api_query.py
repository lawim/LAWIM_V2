from __future__ import annotations

from dataclasses import dataclass

from .errors import ValidationError
from .dto import PaginationMeta, coerce_sort_field, coerce_sort_order
from .geo_domain import normalize_city, normalize_country, normalize_region
from .property_domain import normalize_availability, normalize_property_type


def _coerce_sort_field(field: str | None, allowed: set[str], default: str) -> str:
    try:
        return coerce_sort_field(field, allowed, default)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc


def _coerce_sort_order(order: str | None) -> str:
    try:
        return coerce_sort_order(order)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc


DEFAULT_LIMIT = 10
MAX_LIMIT = 100


@dataclass(frozen=True, slots=True)
class ListQuery:
    page: int = 1
    limit: int = DEFAULT_LIMIT
    sort: str = "created_at"
    order: str = "desc"
    city: str | None = None
    country: str | None = None
    region: str | None = None
    status: str | None = None
    availability: str | None = None
    property_type: str | None = None
    owner_organization_id: int | None = None
    include_deleted: bool = False
    property_id: int | None = None
    kind: str | None = None
    search: str | None = None
    price_min: int | None = None
    price_max: int | None = None
    unread_only: bool = False

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


def parse_page(value: int | None) -> int:
    if value is None:
        return 1
    if value < 1:
        raise ValidationError("page must be positive")
    return value


def parse_price(value: int | None, *, field: str) -> int | None:
    if value is None:
        return None
    if value < 0:
        raise ValidationError(f"{field} must be non-negative")
    return value


def parse_limit(value: int | None, *, default: int = DEFAULT_LIMIT) -> int:
    if value is None:
        return default
    if value < 1:
        raise ValidationError("limit must be positive")
    if value > MAX_LIMIT:
        raise ValidationError(f"limit must not exceed {MAX_LIMIT}")
    return value


def build_property_query(
    *,
    page: int | None = None,
    limit: int | None = None,
    sort: str | None = None,
    order: str | None = None,
    city: str | None = None,
    country: str | None = None,
    region: str | None = None,
    status: str | None = None,
    availability: str | None = None,
    property_type: str | None = None,
    owner_organization_id: int | None = None,
    include_deleted: bool = False,
    search: str | None = None,
    price_min: int | None = None,
    price_max: int | None = None,
) -> ListQuery:
    parsed_price_min = parse_price(price_min, field="price_min")
    parsed_price_max = parse_price(price_max, field="price_max")
    if parsed_price_min is not None and parsed_price_max is not None and parsed_price_min > parsed_price_max:
        raise ValidationError("price_min cannot exceed price_max")
    normalized_city = _optional_city(city)
    normalized_country = _optional_country(country)
    normalized_region = _optional_region(region, city=normalized_city)
    return ListQuery(
        page=parse_page(page),
        limit=parse_limit(limit),
        sort=_coerce_sort_field(sort, {"created_at", "title", "price_min", "city", "status"}, "created_at"),
        order=_coerce_sort_order(order),
        city=normalized_city,
        country=normalized_country,
        region=normalized_region,
        status=_optional_lower(status),
        availability=_optional_availability(availability),
        property_type=_optional_property_type(property_type),
        owner_organization_id=owner_organization_id,
        include_deleted=include_deleted,
        search=_optional_lower(search),
        price_min=parsed_price_min,
        price_max=parsed_price_max,
    )


def build_notification_query(
    *,
    page: int | None = None,
    limit: int | None = None,
    kind: str | None = None,
    unread_only: bool = False,
) -> ListQuery:
    return ListQuery(
        page=parse_page(page),
        limit=parse_limit(limit),
        kind=_optional_lower(kind),
        unread_only=unread_only,
    )


def build_media_query(
    *,
    page: int | None = None,
    limit: int | None = None,
    sort: str | None = None,
    order: str | None = None,
    property_id: int | None = None,
    kind: str | None = None,
    include_deleted: bool = False,
) -> ListQuery:
    return ListQuery(
        page=parse_page(page),
        limit=parse_limit(limit),
        sort=_coerce_sort_field(sort, {"created_at", "position", "kind"}, "created_at"),
        order=_coerce_sort_order(order),
        property_id=property_id,
        kind=_optional_lower(kind),
        include_deleted=include_deleted,
    )


def pagination_meta(*, page: int, limit: int, total: int, sort: str, order: str) -> PaginationMeta:
    pages = max(1, (total + limit - 1) // limit) if total else 1
    return PaginationMeta(page=page, limit=limit, total=total, pages=pages, sort=sort, order=order)


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _optional_lower(value: str | None) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    return text.lower()


def _optional_city(value: str | None) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    return normalize_city(text)


def _optional_country(value: str | None) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    return normalize_country(text)


def _optional_region(value: str | None, *, city: str | None = None) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    return normalize_region(text, city=city)


def _optional_availability(value: str | None) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    return normalize_availability(text)


def _optional_property_type(value: str | None) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    return normalize_property_type(text)
