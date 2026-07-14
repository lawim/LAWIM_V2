from __future__ import annotations

import json
from typing import Any

from .constants import COMMISSION_TYPES, REPUTATION_SCORE_KEYS, SERVICE_CATEGORIES


class PartnerQualificationEngine:
    def evaluate(
        self,
        *,
        registration: dict[str, object],
        partner: dict[str, object] | None = None,
    ) -> dict[str, object]:
        status = str(registration.get("status") or "draft")
        score = 20
        if registration.get("applicant_email"):
            score += 10
        if registration.get("applicant_phone"):
            score += 10
        categories = registration.get("service_categories_json") or "[]"
        try:
            cats = json.loads(str(categories))
            score += min(20, len(cats) * 5)
        except json.JSONDecodeError:
            cats = []
        if partner:
            score += min(40, int(partner.get("trust_score") or 0) // 3)
        qualified = score >= 60 and status in {"submitted", "under_review", "approved"}
        return {
            "qualification_score": min(100, score),
            "qualified": qualified,
            "categories": cats,
            "recommended_status": "approved" if qualified else "under_review",
        }


class CatalogEngine:
    def normalize_category(self, category: str) -> str:
        return category if category in SERVICE_CATEGORIES else "other"

    def price_band(self, *, price_min: int | None, price_max: int | None) -> dict[str, object]:
        pmin = int(price_min or 0)
        pmax = int(price_max or pmin)
        mid = (pmin + pmax) // 2 if pmax else pmin
        return {"price_min": pmin, "price_max": pmax, "mid_price": mid}

    def enrich_item(
        self,
        *,
        item: dict[str, object],
        service_catalog: dict[str, object] | None = None,
    ) -> dict[str, object]:
        enriched = dict(item)
        if service_catalog:
            enriched["ecosystem_service"] = {
                "id": service_catalog.get("id"),
                "service_key": service_catalog.get("service_key"),
                "title": service_catalog.get("title"),
            }
        enriched["category"] = self.normalize_category(str(item.get("category") or "other"))
        return enriched


class QuoteEngine:
    def compute_total(self, lines: list[dict[str, object]]) -> int:
        return sum(int(line.get("amount") or 0) for line in lines)

    def build_line(self, *, description: str, quantity: int = 1, unit_price: int = 0) -> dict[str, object]:
        qty = max(1, quantity)
        price = max(0, unit_price)
        return {
            "description": description,
            "quantity": qty,
            "unit_price": price,
            "amount": qty * price,
        }

    def validate_quote(self, *, quote: dict[str, object], lines: list[dict[str, object]]) -> dict[str, object]:
        total = self.compute_total(lines)
        amount = int(quote.get("amount") or 0)
        return {"valid": total == amount, "computed_total": total, "quoted_amount": amount}


class ReputationEngine:
    def compute_scores(
        self,
        *,
        partner: dict[str, object],
        reviews: list[dict[str, object]],
        missions_completed: int = 0,
    ) -> dict[str, int]:
        avg_rating = 0.0
        if reviews:
            avg_rating = sum(int(r.get("rating") or 0) for r in reviews) / len(reviews)
        trust = int(partner.get("trust_score") or 0)
        quality = min(100, int(partner.get("quality_score") or 0))
        responsiveness = min(100, 50 + max(0, 24 - int(partner.get("response_time_hours") or 24)) * 2)
        reliability = min(100, int(float(partner.get("completion_rate") or 0) * 100))
        value = min(100, int(avg_rating * 10))
        communication = min(100, int(partner.get("satisfaction_score") or 0))
        completion = min(100, 40 + missions_completed * 10)
        satisfaction = min(100, int(avg_rating * 10) if reviews else int(partner.get("satisfaction_score") or 70))
        scores = {
            "quality": max(quality, trust // 2),
            "responsiveness": responsiveness,
            "reliability": reliability,
            "value": value,
            "communication": communication,
            "completion": completion,
            "satisfaction": satisfaction,
        }
        return {k: scores[k] for k in REPUTATION_SCORE_KEYS}


class CommissionEngine:
    def compute(
        self,
        *,
        contract_amount: int,
        rule: dict[str, object] | None = None,
    ) -> dict[str, object]:
        commission_type = str(rule.get("commission_type") if rule else "percentage")
        if commission_type not in COMMISSION_TYPES:
            commission_type = "percentage"
        if commission_type == "flat":
            amount = int(rule.get("flat_amount") if rule else 0)
        elif commission_type == "percentage":
            rate = float(rule.get("rate_percent") if rule and rule.get("rate_percent") is not None else 10.0)
            amount = int(contract_amount * rate / 100)
        else:
            amount = int(contract_amount * 0.1)
        return {
            "commission_type": commission_type,
            "amount": max(0, amount),
            "currency": str(rule.get("currency") if rule else "XAF"),
        }


class RecommendationEngine:
    def build_recommendations(
        self,
        *,
        matches: list[dict[str, object]],
        request: dict[str, object] | None = None,
        sources: list[str],
    ) -> list[dict[str, object]]:
        recs: list[dict[str, object]] = []
        for match in matches[:5]:
            provider_id = match.get("provider_profile_id")
            recs.append(
                {
                    "recommendation_type": "provider",
                    "provider_profile_id": provider_id,
                    "score": match.get("score"),
                    "title": f"Prestataire recommandé (score {match.get('score')})",
                    "rationale": "; ".join(match.get("reasons") or [])[:200],
                    "sources": sources,
                }
            )
        if request and request.get("property_id"):
            recs.append(
                {
                    "recommendation_type": "property_linked",
                    "score": 75,
                    "title": "Demande liée à un bien immobilier",
                    "rationale": "Coordonner avec Real Estate Intelligence",
                    "sources": sources,
                }
            )
        return recs


class AiIntegrationBridge:
    PROGRAM_SOURCES: tuple[str, ...] = (
        "intelligent_core",
        "ecosystem",
        "cognition",
        "assistant",
        "knowledge_platform",
        "workflow_automation",
        "real_estate_intelligence",
        "crm",
        "source_intelligence",
    )

    def sources(self) -> list[str]:
        return list(self.PROGRAM_SOURCES)

    def enrich_with_knowledge(self, repository: Any, query: str) -> dict[str, object] | None:
        if hasattr(repository, "expert_rag_query"):
            try:
                return repository.expert_rag_query(query)
            except Exception:
                return None
        return None

    def enrich_with_assistant(self, repository: Any, prompt: str) -> dict[str, object] | None:
        if hasattr(repository, "assistant_chat"):
            try:
                return repository.assistant_chat(prompt)
            except Exception:
                return None
        return None

    def trigger_workflow(self, repository: Any, *, workflow_key: str, context: dict[str, object]) -> dict[str, object] | None:
        if hasattr(repository, "start_automation_instance"):
            try:
                return repository.start_automation_instance(workflow_key=workflow_key, context=context)
            except Exception:
                return None
        return None

    def link_crm_contact(self, repository: Any, *, contact_id: int) -> dict[str, object] | None:
        if hasattr(repository, "get_crm_contact"):
            try:
                return repository.get_crm_contact(contact_id)
            except Exception:
                return None
        return None

    def link_property(self, repository: Any, *, property_id: int) -> dict[str, object] | None:
        if hasattr(repository, "get_rei_property_bundle"):
            try:
                return repository.get_rei_property_bundle(property_id)
            except Exception:
                return None
        return None


class MarketplacePlatformEngine:
    def __init__(self) -> None:
        self.partner_qualification = PartnerQualificationEngine()
        self.catalog = CatalogEngine()
        self.quotes = QuoteEngine()
        self.reputation = ReputationEngine()
        self.commission = CommissionEngine()
        self.recommendations = RecommendationEngine()
        self.ai = AiIntegrationBridge()

    def integration_sources(self) -> list[str]:
        return self.ai.sources()
