from __future__ import annotations

import time

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as rdto


class RealEstateIntelligenceService:
    def __init__(self, repository, project_service: ProjectService, policy) -> None:
        self.repository = repository
        self.projects = project_service
        self.policy = policy

    def _require_auth(self, actor: dict[str, object] | None) -> None:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")

    def _require_admin(self, actor: dict[str, object]) -> None:
        if not self.policy.is_admin(actor):
            raise ProjectPermissionDenied("Admin required")

    def list_properties(self, *, actor: dict[str, object], status: str | None = None, limit: int = 50) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("property_list")
        return {"properties": self.repository.list_rei_enriched_properties(status=status, limit=limit)}

    def get_property(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("property_detail")
        return self.repository.get_rei_property_bundle(property_id)

    def list_listings(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("listing_list")
        return {"listings": [rdto.listing_dto(r) for r in self.repository.list_rei_listings(status=status)]}

    def create_listing(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        listing = self.repository.create_rei_listing(property_id=int(body["property_id"]), title=str(body["title"]))
        METRICS.increment("listing_created")
        return {"listing": rdto.listing_dto(listing)}

    def publish(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_admin(actor)
        listing = self.repository.publish_rei_listing(property_id)
        METRICS.increment("listing_published")
        return {"listing": rdto.listing_dto(listing)}

    def archive(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_admin(actor)
        listing = self.repository.archive_rei_listing(property_id)
        METRICS.increment("listing_archived")
        return {"listing": rdto.listing_dto(listing)}

    def duplicate_listing(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_admin(actor)
        return {"listing": rdto.listing_dto(self.repository.duplicate_rei_listing(property_id))}

    def owners(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"owners": [rdto.owner_dto(r) for r in self.repository.list_rei_owners(property_id)]}

    def add_owner(self, *, actor: dict[str, object], property_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        owner = self.repository.add_rei_owner(property_id, owner_name=str(body["owner_name"]), owner_type=str(body.get("owner_type") or "individual"))
        return {"owner": rdto.owner_dto(owner)}

    def documents(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"documents": [rdto.document_dto(r) for r in self.repository.list_rei_documents(property_id)]}

    def add_document(self, *, actor: dict[str, object], property_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        doc = self.repository.add_rei_document(property_id, title=str(body["title"]), document_type=str(body.get("document_type") or "other"))
        return {"document": rdto.document_dto(doc)}

    def verification(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        started = time.perf_counter()
        score = self.repository.run_rei_verification(property_id)
        METRICS.record_verification(latency_ms=(time.perf_counter() - started) * 1000)
        METRICS.increment("verification_run")
        return {"verification": rdto.verification_dto(score)}

    def get_verification(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        row = self.repository.one("SELECT * FROM rei_verification_scores WHERE property_id = ?", (property_id,))
        if row is None:
            row = self.repository.run_rei_verification(property_id)
        return {"verification": rdto.verification_dto(dict(row))}

    def valuation(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        val = self.repository.get_rei_valuation(property_id)
        METRICS.increment("valuation_computed")
        return {"valuation": rdto.valuation_dto(val)}

    def matching(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        project_id = int(body["project_id"]) if body.get("project_id") is not None else None
        if project_id is not None:
            self.projects._require_access(actor, project_id)
        payload = self.repository.run_rei_matching(user_id=user_id, project_id=project_id, criteria=dict(body.get("criteria") or body))
        METRICS.increment("matching_run")
        METRICS.record_matching(score=len(payload.get("results") or []))
        return payload

    def recommendations(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        project_id = int(body["project_id"]) if body.get("project_id") is not None else None
        if project_id is not None:
            self.projects._require_access(actor, project_id)
        recs = self.repository.build_rei_recommendations(user_id=user_id, project_id=project_id, criteria=dict(body.get("criteria") or body))
        METRICS.increment("recommendation_generated")
        return {"recommendations": [rdto.recommendation_dto(r) for r in recs]}

    def list_recommendations(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        return {"recommendations": [rdto.recommendation_dto(r) for r in self.repository.list_rei_recommendations(user_id=user_id)]}

    def visits(self, *, actor: dict[str, object], property_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("visit_list")
        return {"visits": [rdto.visit_dto(r) for r in self.repository.list_rei_visits(property_id=property_id)]}

    def schedule_visit(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        visit = self.repository.schedule_rei_visit(
            property_id=int(body["property_id"]),
            user_id=user_id,
            scheduled_at=str(body["scheduled_at"]),
        )
        METRICS.increment("visit_scheduled")
        return {"visit": rdto.visit_dto(visit)}

    def confirm_visit(self, *, actor: dict[str, object], visit_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"visit": rdto.visit_dto(self.repository.confirm_rei_visit(visit_id))}

    def cancel_visit(self, *, actor: dict[str, object], visit_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"visit": rdto.visit_dto(self.repository.cancel_rei_visit(visit_id))}

    def complete_visit(self, *, actor: dict[str, object], visit_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        report = self.repository.complete_rei_visit(visit_id, summary=str(body.get("summary") or ""), rating=int(body.get("rating") or 3))
        METRICS.increment("visit_completed")
        return {"report": report}

    def negotiations(self, *, actor: dict[str, object], property_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"negotiations": [rdto.negotiation_dto(r) for r in self.repository.list_rei_negotiations(property_id)]}

    def open_negotiation(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        buyer_id = int(actor["id"]) if actor.get("id") is not None else None
        neg = self.repository.open_rei_negotiation(property_id=int(body["property_id"]), buyer_id=buyer_id)
        return {"negotiation": rdto.negotiation_dto(neg)}

    def submit_offer(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        offer = self.repository.submit_rei_offer(negotiation_id=int(body["negotiation_id"]), amount=int(body["amount"]), currency=str(body.get("currency") or "XAF"))
        return {"offer": rdto.offer_dto(offer)}

    def offers(self, *, actor: dict[str, object], negotiation_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"offers": [rdto.offer_dto(r) for r in self.repository.list_rei_offers(negotiation_id)]}

    def transactions(self, *, actor: dict[str, object], property_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("transaction_list")
        return {"transactions": [rdto.transaction_dto(r) for r in self.repository.list_rei_transactions(property_id=property_id)]}

    def start_transaction(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        buyer_id = int(actor["id"]) if actor.get("id") is not None else None
        tx = self.repository.start_rei_transaction(
            property_id=int(body["property_id"]),
            transaction_type=str(body.get("transaction_type") or "sale"),
            buyer_id=buyer_id,
            amount=int(body["amount"]) if body.get("amount") is not None else None,
        )
        METRICS.increment("transaction_started")
        return {"transaction": rdto.transaction_dto(tx)}

    def close_transaction(self, *, actor: dict[str, object], transaction_id: int) -> dict[str, object]:
        self._require_admin(actor)
        tx = self.repository.close_rei_transaction(transaction_id)
        METRICS.increment("transaction_closed")
        return {"transaction": rdto.transaction_dto(tx)}

    def reserve(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        res = self.repository.create_rei_reservation(
            property_id=int(body["property_id"]),
            user_id=user_id,
            days=int(body.get("days") or 7),
            amount=int(body["amount"]) if body.get("amount") is not None else None,
        )
        return {"reservation": res}

    def history(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"history": [rdto.history_dto(r) for r in self.repository.list_rei_history(property_id)]}

    def intelligence(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        scores = self.repository.compute_rei_intelligence_scores(property_id)
        METRICS.increment("intelligence_computed")
        return rdto.intelligence_dto(scores)

    def scores(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        return self.intelligence(actor=actor, property_id=property_id)

    def analytics(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return rdto.analytics_dto(self.repository.rei_analytics())

    def stats(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return {"stats": self.repository.rei_stats()}

    def report(self, *, actor: dict[str, object], property_id: int, report_type: str = "summary") -> dict[str, object]:
        self._require_auth(actor)
        return self.repository.generate_rei_report(property_id, report_type=report_type)

    def search(self, *, actor: dict[str, object], query: str, limit: int = 20) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("property_search")
        return {"results": self.repository.rei_search(query=query, limit=limit)}

    def map_view(self, *, actor: dict[str, object], city: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"properties": self.repository.rei_map_properties(city=city)}

    def nearby(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"nearby": self.repository.rei_nearby(property_id)}

    def media(self, *, actor: dict[str, object], property_id: int) -> dict[str, object]:
        self._require_auth(actor)
        rows = self.repository.all("SELECT * FROM media WHERE property_id = ? AND deleted_at IS NULL ORDER BY position ASC", (property_id,))
        return {"media": [dict(r) for r in rows]}
