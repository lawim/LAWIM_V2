from __future__ import annotations

from typing import Any

from lawim_runtime.domains.base.context import DomainRuntimeContext
from lawim_runtime.domains.base.errors import DomainValidationError
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.domains.base.runtime import DomainRuntime

from .models import MatchingRequestData, MatchingResultItem, MatchingStatus


class MatchingRuntime(DomainRuntime):
    runtime_name: str = "matching"
    supported_actions: list[str] = [
        "START_PRELIMINARY_MATCHING",
        "START_MATCHING",
        "REFINE_MATCHING",
        "PRESENT_MATCHES",
    ]

    def __init__(self) -> None:
        self._properties: list[dict[str, Any]] = []
        self._searches: dict[str, dict[str, Any]] = {}

    def load_properties(self, properties: list[dict[str, Any]]) -> None:
        self._properties = list(properties)

    def execute_op(self, request: DomainRuntimeRequest, context: DomainRuntimeContext) -> dict[str, Any]:
        action = request.action_code
        params = request.parameters

        if action == "START_PRELIMINARY_MATCHING":
            return self._execute_preliminary(params)
        elif action == "START_MATCHING":
            return self._execute_matching(params)
        elif action == "REFINE_MATCHING":
            return self._execute_refine(params)
        elif action == "PRESENT_MATCHES":
            return self._execute_present(params)
        else:
            raise DomainValidationError(f"unsupported action: {action}")

    def _execute_preliminary(self, params: dict[str, Any]) -> dict[str, Any]:
        property_type = params.get("property_type", "")
        city = params.get("city", "")
        district = params.get("district", "")
        preliminary_matches = [
            p for p in self._properties
            if (not property_type or p.get("property_type") == property_type)
            and (not city or p.get("city", "").lower() == city.lower())
            and (not district or p.get("district", "").lower() == district.lower())
        ]
        count = len(preliminary_matches)
        if pending := self._searches.setdefault("preliminary_latest", {}):
            pending.clear()
        self._searches["preliminary_latest"] = {
            "parameters": params,
            "property_ids": [p.get("property_id", "") for p in preliminary_matches],
            "count": count,
        }
        return {
            "status": MatchingStatus.MATCH_FOUND.value if count > 0 else MatchingStatus.NO_MATCH.value,
            "preliminary_count": count,
            "property_ids": [p.get("property_id", "") for p in preliminary_matches],
            "matches": preliminary_matches[:10],
        }

    def _execute_matching(self, params: dict[str, Any]) -> dict[str, Any]:
        property_type = params.get("property_type", "")
        bedrooms = params.get("bedrooms", 0)
        min_budget = params.get("min_budget", 0.0)
        max_budget = params.get("max_budget", 0.0)
        city = params.get("city", "")
        district = params.get("district", "")
        features = params.get("features", [])
        criteria = params.get("criteria", {})
        scored: list[tuple[float, dict[str, Any]]] = []
        for prop in self._properties:
            score = 0.0
            reasons: list[str] = []
            if property_type and prop.get("property_type") == property_type:
                score += 30.0
                reasons.append("property_type_match")
            if bedrooms and prop.get("bedrooms") == bedrooms:
                score += 20.0
                reasons.append("bedrooms_match")
            price = prop.get("price", 0.0)
            if max_budget > 0 and min_budget <= price <= max_budget:
                score += 25.0
                reasons.append("budget_match")
            elif max_budget > 0 and price <= max_budget:
                score += 10.0
                reasons.append("budget_partial_match")
            if city and prop.get("city", "").lower() == city.lower():
                score += 15.0
                reasons.append("city_match")
            if district and prop.get("district", "").lower() == district.lower():
                score += 10.0
                reasons.append("district_match")
            if features:
                prop_features = prop.get("features", [])
                feature_match = len(set(features) & set(prop_features))
                if feature_match > 0:
                    score += 5.0 * feature_match
                    reasons.append(f"feature_match_count_{feature_match}")
            if criteria:
                criteria_score = self._score_criteria(prop, criteria)
                score += criteria_score
                if criteria_score > 0:
                    reasons.append("criteria_match")
            if score > 0:
                scored.append((score, prop))
        scored.sort(key=lambda x: x[0], reverse=True)
        matches = [
            {
                "property_id": prop.get("property_id", ""),
                "score": round(s, 2),
                "match_reasons": [],
                "match_explanations": {},
                "property_snapshot": dict(prop),
            }
            for s, prop in scored
        ]
        self._searches["latest"] = {
            "parameters": params,
            "property_ids": [m["property_id"] for m in matches],
            "count": len(matches),
        }
        return {
            "status": MatchingStatus.MATCH_FOUND.value if matches else MatchingStatus.NO_MATCH.value,
            "total_count": len(matches),
            "matches": matches,
        }

    def _execute_refine(self, params: dict[str, Any]) -> dict[str, Any]:
        previous = self._searches.get("latest")
        if not previous:
            return {
                "status": MatchingStatus.NO_MATCH.value,
                "total_count": 0,
                "matches": [],
                "error": "no previous search to refine",
            }
        prior_ids = set(previous.get("property_ids", []))
        new_features = params.get("features", [])
        refined: list[dict[str, Any]] = []
        for prop in self._properties:
            pid = prop.get("property_id", "")
            if pid not in prior_ids:
                continue
            if new_features:
                prop_features = set(prop.get("features", []))
                if not set(new_features) & prop_features:
                    continue
            refined.append({
                "property_id": pid,
                "score": 0.0,
                "match_reasons": ["refined_match"],
                "match_explanations": {},
                "property_snapshot": dict(prop),
            })
        return {
            "status": MatchingStatus.MATCH_FOUND.value if refined else MatchingStatus.NO_MATCH.value,
            "total_count": len(refined),
            "matches": refined,
        }

    def _execute_present(self, params: dict[str, Any]) -> dict[str, Any]:
        previous = self._searches.get("latest") or self._searches.get("preliminary_latest")
        if not previous:
            return {
                "status": MatchingStatus.NO_MATCH.value,
                "total_count": 0,
                "matches": [],
                "error": "no matches available to present",
            }
        ids = previous.get("property_ids", [])
        present: list[dict[str, Any]] = []
        for prop in self._properties:
            if prop.get("property_id", "") in ids:
                present.append({
                    "property_id": prop.get("property_id", ""),
                    "score": 0.0,
                    "match_reasons": ["presented"],
                    "match_explanations": {},
                    "property_snapshot": dict(prop),
                })
        return {
            "status": MatchingStatus.MATCH_FOUND.value if present else MatchingStatus.NO_MATCH.value,
            "total_count": len(present),
            "matches": present,
        }

    def _score_criteria(self, prop: dict[str, Any], criteria: dict[str, Any]) -> float:
        total = 0.0
        for key, value in criteria.items():
            prop_value = prop.get(key)
            if isinstance(value, (int, float)) and isinstance(prop_value, (int, float)):
                if prop_value >= value:
                    total += 10.0
            elif prop_value == value:
                total += 10.0
        return total

    def validate(self, request: DomainRuntimeRequest) -> list[str]:
        errors = super().validate(request)
        params = request.parameters
        action = request.action_code
        if action in ("START_PRELIMINARY_MATCHING", "START_MATCHING"):
            if not params.get("property_type") and not params.get("city"):
                errors.append("property_type or city is required for matching")
        if "min_budget" in params and "max_budget" in params:
            min_b = params.get("min_budget", 0)
            max_b = params.get("max_budget", 0)
            if isinstance(min_b, (int, float)) and isinstance(max_b, (int, float)) and min_b > max_b:
                errors.append("min_budget cannot exceed max_budget")
        return errors

    def verify(self, request: DomainRuntimeRequest, output: dict[str, Any]) -> bool:
        if not isinstance(output, dict):
            return False
        if "status" not in output:
            return False
        if output.get("status") == MatchingStatus.MATCH_FOUND.value:
            matches = output.get("matches", [])
            if not isinstance(matches, list):
                return False
            for item in matches:
                if not isinstance(item, dict) or "property_id" not in item:
                    return False
        total_count = output.get("total_count", 0)
        matches = output.get("matches", [])
        if isinstance(total_count, int) and isinstance(matches, list):
            if total_count != len(matches):
                return False
        return True
