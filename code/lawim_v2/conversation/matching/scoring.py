from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .criteria import MatchDimension, MatchingCriteria
from .results import MatchExplanation


class DimensionScorer(ABC):
    dimension: MatchDimension

    @abstractmethod
    def score(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> MatchExplanation:
        ...


class LocationScorer(DimensionScorer):
    dimension = MatchDimension.LOCATION

    def score(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> MatchExplanation:
        requested_city = (request_criteria.get("city") or "").lower().strip()
        item_city = (item.get("city") or "").lower().strip()

        if not requested_city:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.5,
                weight=criteria.get_weight(self.dimension),
                details="No location preference specified",
                is_match=True,
            )

        if requested_city == item_city:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=1.0,
                weight=criteria.get_weight(self.dimension),
                details=f"Exact city match: {item_city}",
                is_match=True,
            )

        if item.get("district") and request_criteria.get("district"):
            if item["district"].lower().strip() == request_criteria["district"].lower().strip():
                return MatchExplanation(
                    dimension=self.dimension.value,
                    score=0.9,
                    weight=criteria.get_weight(self.dimension),
                    details=f"District match in {item_city}",
                    is_match=True,
                )

        return MatchExplanation(
            dimension=self.dimension.value,
            score=0.0,
            weight=criteria.get_weight(self.dimension),
            details=f"City mismatch: requested {requested_city}, got {item_city}",
            is_match=False,
        )


class BudgetScorer(DimensionScorer):
    dimension = MatchDimension.BUDGET

    def score(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> MatchExplanation:
        item_price = item.get("price")
        if item_price is None:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.0,
                weight=criteria.get_weight(self.dimension),
                details="No price information available",
                is_match=False,
            )

        budget_min = request_criteria.get("budget_min")
        budget_max = request_criteria.get("budget_max")

        if budget_min is None and budget_max is None:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.5,
                weight=criteria.get_weight(self.dimension),
                details=f"No budget constraints; item price is {item_price}",
                is_match=True,
            )

        if budget_min is not None and item_price < budget_min:
            ratio = item_price / budget_min if budget_min > 0 else 0
            return MatchExplanation(
                dimension=self.dimension.value,
                score=max(0, 1 - ratio),
                weight=criteria.get_weight(self.dimension),
                details=f"Below minimum budget: {item_price} < {budget_min}",
                is_match=False,
            )

        if budget_max is not None and item_price > budget_max:
            over_ratio = (item_price - budget_max) / budget_max if budget_max > 0 else 1
            return MatchExplanation(
                dimension=self.dimension.value,
                score=max(0, 1 - over_ratio),
                weight=criteria.get_weight(self.dimension),
                details=f"Exceeds maximum budget: {item_price} > {budget_max}",
                is_match=False,
            )

        if budget_min is not None and budget_max is not None:
            mid = (budget_min + budget_max) / 2
            range_size = budget_max - budget_min
            if range_size > 0:
                deviation = abs(item_price - mid) / range_size
                score = max(0, 1 - deviation)
            else:
                score = 1.0 if item_price == budget_min else 0.0
        else:
            score = 1.0

        return MatchExplanation(
            dimension=self.dimension.value,
            score=score,
            weight=criteria.get_weight(self.dimension),
            details=f"Price {item_price} within budget range [{budget_min}, {budget_max}]" if budget_min is not None and budget_max is not None else f"Price {item_price} meets budget criteria",
            is_match=score > 0,
        )


class PropertyTypeScorer(DimensionScorer):
    dimension = MatchDimension.PROPERTY_TYPE

    def score(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> MatchExplanation:
        requested_type = (request_criteria.get("property_type") or "").lower().strip()
        item_type = (item.get("property_type") or "").lower().strip()

        if not requested_type:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.5,
                weight=criteria.get_weight(self.dimension),
                details="No property type preference",
                is_match=True,
            )

        if requested_type == item_type:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=1.0,
                weight=criteria.get_weight(self.dimension),
                details=f"Property type matches: {item_type}",
                is_match=True,
            )

        return MatchExplanation(
            dimension=self.dimension.value,
            score=0.0,
            weight=criteria.get_weight(self.dimension),
            details=f"Type mismatch: requested {requested_type}, got {item_type}",
            is_match=False,
        )


class BedroomsScorer(DimensionScorer):
    dimension = MatchDimension.BEDROOMS

    def score(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> MatchExplanation:
        requested_bedrooms = request_criteria.get("bedrooms")
        item_bedrooms = item.get("bedrooms")

        if requested_bedrooms is None:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.5,
                weight=criteria.get_weight(self.dimension),
                details="No bedroom preference",
                is_match=True,
            )

        if item_bedrooms is None:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.0,
                weight=criteria.get_weight(self.dimension),
                details="No bedroom information available",
                is_match=False,
            )

        if item_bedrooms >= requested_bedrooms:
            ratio = requested_bedrooms / max(1, item_bedrooms)
            return MatchExplanation(
                dimension=self.dimension.value,
                score=ratio,
                weight=criteria.get_weight(self.dimension),
                details=f"{item_bedrooms} bedrooms (requested {requested_bedrooms})",
                is_match=True,
            )

        return MatchExplanation(
            dimension=self.dimension.value,
            score=0.0,
            weight=criteria.get_weight(self.dimension),
            details=f"Too few bedrooms: {item_bedrooms} < {requested_bedrooms}",
            is_match=False,
        )


class SurfaceScorer(DimensionScorer):
    dimension = MatchDimension.SURFACE

    def score(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> MatchExplanation:
        item_surface = item.get("surface")
        surface_min = request_criteria.get("surface_min")
        surface_max = request_criteria.get("surface_max")

        if surface_min is None and surface_max is None:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.5,
                weight=criteria.get_weight(self.dimension),
                details="No surface preference",
                is_match=True,
            )

        if item_surface is None:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.0,
                weight=criteria.get_weight(self.dimension),
                details="No surface information available",
                is_match=False,
            )

        if surface_min is not None and item_surface < surface_min:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.0,
                weight=criteria.get_weight(self.dimension),
                details=f"Surface too small: {item_surface}m² < {surface_min}m²",
                is_match=False,
            )

        if surface_max is not None and item_surface > surface_max:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.0,
                weight=criteria.get_weight(self.dimension),
                details=f"Surface too large: {item_surface}m² > {surface_max}m²",
                is_match=False,
            )

        return MatchExplanation(
            dimension=self.dimension.value,
            score=1.0,
            weight=criteria.get_weight(self.dimension),
            details=f"Surface {item_surface}m² meets criteria",
            is_match=True,
        )


class TransactionTypeScorer(DimensionScorer):
    dimension = MatchDimension.TRANSACTION_TYPE

    def score(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> MatchExplanation:
        requested_tx = (request_criteria.get("transaction_type") or "").lower().strip()
        item_tx = (item.get("transaction_type") or "").lower().strip()

        if not requested_tx:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.5,
                weight=criteria.get_weight(self.dimension),
                details="No transaction type preference",
                is_match=True,
            )

        if requested_tx == item_tx:
            return MatchExplanation(
                dimension=self.dimension.value,
                score=1.0,
                weight=criteria.get_weight(self.dimension),
                details=f"Transaction type matches: {item_tx}",
                is_match=True,
            )

        return MatchExplanation(
            dimension=self.dimension.value,
            score=0.0,
            weight=criteria.get_weight(self.dimension),
            details=f"Transaction type mismatch: requested {requested_tx}, got {item_tx}",
            is_match=False,
        )


class AvailabilityScorer(DimensionScorer):
    dimension = MatchDimension.AVAILABILITY

    def score(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> MatchExplanation:
        status = (item.get("status") or "").lower().strip()
        if status == "available":
            return MatchExplanation(
                dimension=self.dimension.value,
                score=1.0,
                weight=criteria.get_weight(self.dimension),
                details="Item is available",
                is_match=True,
            )
        if status == "pending":
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.3,
                weight=criteria.get_weight(self.dimension),
                details="Item is pending",
                is_match=True,
            )
        if status in ("sold", "rented", "unavailable"):
            return MatchExplanation(
                dimension=self.dimension.value,
                score=0.0,
                weight=criteria.get_weight(self.dimension),
                details=f"Item is {status}",
                is_match=False,
            )
        return MatchExplanation(
            dimension=self.dimension.value,
            score=0.5,
            weight=criteria.get_weight(self.dimension),
            details="Availability status unknown",
            is_match=True,
        )


class PartnerReputationScorer(DimensionScorer):
    dimension = MatchDimension.PARTNER_REPUTATION

    def score(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> MatchExplanation:
        rating = item.get("partner_rating") or item.get("rating")
        if rating is not None:
            normalized = min(1.0, max(0.0, float(rating) / 5.0))
            return MatchExplanation(
                dimension=self.dimension.value,
                score=normalized,
                weight=criteria.get_weight(self.dimension),
                details=f"Partner rating: {rating}/5",
                is_match=True,
            )
        return MatchExplanation(
            dimension=self.dimension.value,
            score=0.5,
            weight=criteria.get_weight(self.dimension),
            details="No partner rating available",
            is_match=True,
        )


DEFAULT_SCORERS: list[DimensionScorer] = [
    LocationScorer(),
    BudgetScorer(),
    PropertyTypeScorer(),
    BedroomsScorer(),
    SurfaceScorer(),
    TransactionTypeScorer(),
    AvailabilityScorer(),
    PartnerReputationScorer(),
]


class ScoringEngine:
    def __init__(self, scorers: list[DimensionScorer] | None = None):
        self.scorers = scorers or list(DEFAULT_SCORERS)

    def evaluate(
        self,
        item: dict[str, Any],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
    ) -> list[MatchExplanation]:
        explanations: list[MatchExplanation] = []
        for scorer in self.scorers:
            explanation = scorer.score(item, criteria, request_criteria)
            explanations.append(explanation)
        return explanations
