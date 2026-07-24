from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any

_log = logging.getLogger("lawim_v2.conversation.marketplace_adapter")

try:
    from lawim_runtime.conversation.journey import BusinessActionResult, PropertySearchService
    HAS_PORT = True
except ImportError:
    HAS_PORT = False
    BusinessActionResult = None  # type: ignore[assignment]
    PropertySearchService = None  # type: ignore[assignment, misc]


class _PostgresMarketplaceRepository:
    def __init__(self, database_url: str) -> None:
        self._database_url = database_url
        self._conn = self._connect()

    def _connect(self):
        import psycopg2
        return psycopg2.connect(self._database_url)

    def create_marketplace_request(
        self, *, title, description, category, city, country,
        budget_min, budget_max, currency, criteria, status, user_id,
    ) -> dict[str, Any]:
        import uuid
        now = datetime.now(timezone.utc).isoformat()
        key = f"pf-req-{uuid.uuid4().hex[:10]}"
        criteria_json = criteria
        c = self._conn.cursor()
        c.execute(
            """INSERT INTO marketplace_service_requests
               (request_key, user_id, title, description, category, city, country,
                budget_min, budget_max, currency, status, criteria_json,
                submitted_at, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (key, user_id, title, description, category, city, country,
             budget_min, budget_max, currency, status,
             _json_dumps(criteria_json) if isinstance(criteria_json, dict) else criteria_json,
             now, now, now),
        )
        row = c.fetchone()
        self._conn.commit()
        return {"id": row[0], "request_key": key}

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass


def _json_dumps(obj: Any) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False, default=str)


class _SQLiteMarketplaceRepository:
    def __init__(self, repository: Any) -> None:
        self._repository = repository

    def create_marketplace_request(
        self, *, title, description, category, city, country,
        budget_min, budget_max, currency, criteria, status, user_id,
    ) -> dict[str, Any]:
        return dict(self._repository.create_marketplace_request(
            title=title, description=description, category=category,
            city=city, country=country, budget_min=budget_min,
            budget_max=budget_max, currency=currency, criteria=criteria,
            status=status, user_id=user_id,
        ))


class MarketplacePropertySearchAdapter:
    def __init__(
        self,
        repository: Any = None,
        database_url: str = "",
    ) -> None:
        if not HAS_PORT:
            raise ImportError("lawim_runtime BusinessActionResult required")

        if database_url:
            _log.info("Using PostgreSQL marketplace repository")
            self._delegate = _PostgresMarketplaceRepository(database_url)
        elif repository is not None:
            _log.warning("Using SQLite marketplace repository (no DATABASE_URL provided)")
            self._delegate = _SQLiteMarketplaceRepository(repository)
        else:
            raise ValueError("Either repository or database_url must be provided")

        self._repository = repository
        self._database_url = database_url

    def create_search_request(
        self,
        *,
        conversation_id: str,
        user_id: str | None = None,
        channel: str = "web",
        facts: dict[str, Any] | None = None,
        idempotency_key: str = "",
    ) -> BusinessActionResult:
        facts = facts or {}
        if not facts:
            return BusinessActionResult(
                success=False, action="create_property_search",
                error_code="no_facts",
            )

        try:
            cf = dict(facts)
            city = cf.get("city", "")
            budget_max = cf.get("budget_max")
            bedrooms = cf.get("bedrooms")
            preferred_areas = cf.get("preferred_areas", [])
            move_in_date = cf.get("move_in_date")
            proximity_ref = cf.get("proximity_reference")
            district = cf.get("district")
            property_type = cf.get("property_type", "")
            transaction_type = cf.get("transaction_type", "")

            title = f"Recherche {transaction_type} - {property_type} - {city}"
            description_parts = [f"Recherche d'un {property_type} à {transaction_type}"]
            if bedrooms:
                description_parts.append(f"{bedrooms} chambre(s)")
            if preferred_areas:
                description_parts.append(f"Secteur: {', '.join(preferred_areas)}")
            if district:
                description_parts.append(f"Quartier: {district}")
            if move_in_date:
                description_parts.append(f"Entrée: {move_in_date}")
            if proximity_ref:
                description_parts.append(f"Proximité: {proximity_ref}")
            description = ". ".join(description_parts)

            criteria = {
                "conversation_id": conversation_id,
                "channel": channel,
                "property_type": property_type,
                "transaction_type": transaction_type,
                "bedrooms": bedrooms,
                "preferred_areas": preferred_areas,
                "district": district,
                "move_in_date": move_in_date,
                "proximity_reference": proximity_ref,
                "source": "program_f_conversation_engine",
                "idempotency_key": idempotency_key,
            }

            result = self._delegate.create_marketplace_request(
                title=title,
                description=description,
                category="rental" if transaction_type == "rent" else "sale",
                city=city,
                country="Cameroon",
                budget_min=None,
                budget_max=budget_max,
                currency="XAF",
                criteria=criteria,
                status="new",
                user_id=int(user_id) if user_id is not None else None,
            )

            object_id = str(result.get("id", ""))
            if object_id:
                _log.info("Business object created id=%s type=marketplace_service_request repo=%s",
                          object_id, "postgresql" if self._database_url else "sqlite")
                return BusinessActionResult(
                    success=True,
                    action="create_property_search",
                    object_type="marketplace_service_request",
                    object_id=object_id,
                    message="Recherche créée",
                )
            else:
                return BusinessActionResult(
                    success=False, action="create_property_search",
                    error_code="no_object_id",
                )

        except Exception as exc:
            _log.exception("MarketplacePropertySearchAdapter.create_search_request failed")
            return BusinessActionResult(
                success=False, action="create_property_search",
                error_code=str(exc) if str(exc) else "exception",
            )
