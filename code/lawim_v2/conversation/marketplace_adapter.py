from __future__ import annotations

import logging
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


class MarketplacePropertySearchAdapter:
    def __init__(self, repository: Any) -> None:
        if not HAS_PORT:
            raise ImportError("lawim_runtime BusinessActionResult required")
        self._repository = repository

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

            result = self._repository.create_marketplace_request(
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
