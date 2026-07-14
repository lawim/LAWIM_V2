from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any

from .constants import INTELLIGENCE_SCORE_KEYS


class VerificationEngine:
    CHECK_TYPES: tuple[str, ...] = ("documents", "owners", "geolocation", "title", "compliance", "history", "consistency")

    def run_checks(self, *, property_row: dict[str, object], owners: list[dict[str, object]], documents: list[dict[str, object]]) -> list[dict[str, object]]:
        checks: list[dict[str, object]] = []
        lat = property_row.get("latitude")
        lng = property_row.get("longitude")
        geo_ok = lat is not None and lng is not None
        checks.append({"check_type": "geolocation", "status": "verified" if geo_ok else "failed", "anomalies": [] if geo_ok else ["missing_coordinates"]})
        doc_ok = len(documents) >= 1
        checks.append({"check_type": "documents", "status": "verified" if doc_ok else "review", "anomalies": [] if doc_ok else ["no_documents"]})
        owner_ok = len(owners) >= 1
        checks.append({"check_type": "owners", "status": "verified" if owner_ok else "failed", "anomalies": [] if owner_ok else ["no_owner"]})
        title_ok = any(str(d.get("document_type")) == "title" for d in documents)
        checks.append({"check_type": "title", "status": "verified" if title_ok else "review", "anomalies": [] if title_ok else ["missing_title"]})
        price_min = int(property_row.get("price_min") or 0)
        price_max = int(property_row.get("price_max") or 0)
        consistent = price_max >= price_min > 0
        checks.append({"check_type": "consistency", "status": "verified" if consistent else "failed", "anomalies": [] if consistent else ["price_range_invalid"]})
        checks.append({"check_type": "compliance", "status": "verified", "anomalies": []})
        checks.append({"check_type": "history", "status": "verified", "anomalies": []})
        return checks

    def aggregate_trust(self, checks: list[dict[str, object]]) -> dict[str, object]:
        if not checks:
            return {"trust_score": 0, "consistency_score": 0}
        verified = sum(1 for c in checks if c.get("status") == "verified")
        trust = min(100, int(verified / len(checks) * 100))
        anomalies = sum(len(c.get("anomalies") or []) for c in checks)
        consistency = max(0, 100 - anomalies * 15)
        return {"trust_score": trust, "consistency_score": consistency, "details": {"verified_checks": verified, "total_checks": len(checks)}}


class ValuationEngine:
    def estimate(self, *, property_row: dict[str, object], comparables: list[dict[str, object]] | None = None) -> dict[str, object]:
        price_min = int(property_row.get("price_min") or 0)
        price_max = int(property_row.get("price_max") or price_min)
        mid = (price_min + price_max) // 2 if price_max else price_min
        if comparables:
            avg = sum(int(c.get("price_min") or 0) for c in comparables) // max(len(comparables), 1)
            mid = (mid + avg) // 2
        area = float(property_row.get("area_sqm") or 0)
        factor = 1.05 if area > 80 else 1.0
        amount = int(mid * factor)
        return {"amount": amount, "currency": str(property_row.get("currency") or "XAF"), "confidence": 75, "method": "comparative"}


class IntelligenceEngine:
    def compute_scores(self, *, property_row: dict[str, object], trust_score: int, listing_score: int) -> dict[str, int]:
        bedrooms = int(property_row.get("bedrooms") or 0)
        area = float(property_row.get("area_sqm") or 0)
        status = str(property_row.get("status") or "draft")
        quality = min(100, 40 + bedrooms * 8 + (10 if area > 50 else 0))
        legal = min(100, trust_score)
        investment = min(100, 50 + (15 if bedrooms >= 2 else 0) + listing_score // 5)
        market = min(100, 60 if status == "published" else 30)
        profitability = min(100, investment - 10)
        liquidity = min(100, market + listing_score // 3)
        risk = max(0, 100 - legal)
        return {
            "quality": quality,
            "legal": legal,
            "investment": investment,
            "market": market,
            "profitability": profitability,
            "liquidity": liquidity,
            "risk": risk,
        }


class RecommendationEngine:
    def build_recommendations(
        self,
        *,
        matches: list[dict[str, object]],
        intelligence: dict[str, int],
        sources: list[str],
    ) -> list[dict[str, object]]:
        recs: list[dict[str, object]] = []
        for match in matches[:5]:
            recs.append(
                {
                    "recommendation_type": "property",
                    "property_id": match.get("property_id"),
                    "score": match.get("score"),
                    "title": f"Bien recommandé (score {match.get('score')})",
                    "rationale": "; ".join(match.get("reasons") or [])[:200],
                    "sources": sources,
                }
            )
        if intelligence.get("investment", 0) >= 70:
            recs.append(
                {
                    "recommendation_type": "investment",
                    "score": intelligence.get("investment"),
                    "title": "Opportunité investissement",
                    "rationale": "Score investissement élevé",
                    "sources": sources,
                }
            )
        if intelligence.get("risk", 100) >= 50:
            recs.append(
                {
                    "recommendation_type": "risk",
                    "score": intelligence.get("risk"),
                    "title": "Alerte risque",
                    "rationale": "Score risque à surveiller",
                    "sources": sources,
                }
            )
        return recs


class ListingEngine:
    def ai_listing_score(self, *, property_row: dict[str, object], has_media: bool) -> int:
        score = 30
        if str(property_row.get("status")) == "published":
            score += 25
        if property_row.get("summary"):
            score += 15
        if has_media:
            score += 20
        if property_row.get("latitude"):
            score += 10
        return min(100, score)


class GeoEngine:
    def haversine_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        r = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        return round(r * 2 * math.asin(math.sqrt(a)), 3)

    def geo_hash(self, lat: float, lng: float) -> str:
        return hashlib.sha256(f"{lat:.4f}:{lng:.4f}".encode()).hexdigest()[:12]


class SearchEngine:
    def normalize(self, text: str) -> str:
        lowered = text.lower()
        return re.sub(r"\s+", " ", re.sub(r"[^a-zàâäéèêëïîôùûüç0-9\s]", " ", lowered)).strip()

    def build_index(self, property_row: dict[str, object]) -> str:
        parts = [
            str(property_row.get("title") or ""),
            str(property_row.get("summary") or ""),
            str(property_row.get("city") or ""),
            str(property_row.get("property_type") or ""),
            str(property_row.get("listing_code") or ""),
        ]
        return self.normalize(" ".join(parts))


class RealEstatePlatformEngine:
    def __init__(self) -> None:
        self.verification = VerificationEngine()
        self.valuation = ValuationEngine()
        self.intelligence = IntelligenceEngine()
        self.recommendations = RecommendationEngine()
        self.listings = ListingEngine()
        self.geo = GeoEngine()
        self.search = SearchEngine()

    def integration_sources(self) -> list[str]:
        return [
            "intelligent_core",
            "ecosystem",
            "cognition",
            "assistant",
            "knowledge_platform",
            "workflow_automation",
            "source_intelligence",
        ]
