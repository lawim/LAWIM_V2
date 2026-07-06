from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from ..repository_introspection import table_exists
from .constants import PROPERTY_TYPES
from .engines import RealEstatePlatformEngine


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _parse_json(value: str | None) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


class RealEstateIntelligenceRepositoryMixin:
    def rei_tables_present(self) -> bool:
        return table_exists(self, "rei_property_profiles")

    def seed_rei_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM rei_property_profiles") > 0:
            return
        engine = RealEstatePlatformEngine()
        now = _utcnow()
        properties = self.all("SELECT * FROM properties WHERE deleted_at IS NULL ORDER BY id ASC")
        for prop in properties:
            pid = int(prop["id"])
            ptype = str(prop.get("property_type") or "apartment")
            if ptype not in PROPERTY_TYPES:
                ptype = "apartment" if ptype == "apartment" else ("house" if "house" in ptype else "apartment")
            self.ensure_rei_property_profile(pid, property_type=ptype)
            media_count = self.scalar("SELECT COUNT(*) FROM media WHERE property_id = ? AND deleted_at IS NULL", (pid,))
            ai_score = engine.listings.ai_listing_score(property_row=dict(prop), has_media=media_count > 0)
            listing_key = f"listing-{prop.get('listing_code') or pid}"
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO rei_listings (
                        listing_key, property_id, title, status, visibility, ai_score, published_at, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'public', ?, ?, ?, ?)
                    """,
                    (
                        listing_key,
                        pid,
                        str(prop.get("title") or f"Listing {pid}"),
                        str(prop.get("status") or "draft"),
                        ai_score,
                        prop.get("published_at"),
                        now,
                        now,
                    ),
                )
                conn.execute(
                    """
                    INSERT OR IGNORE INTO rei_property_owners (property_id, owner_type, owner_name, owner_contact, verified, created_at)
                    VALUES (?, 'organization', 'LAWIM Demo Owner', 'owner@lawim.local', 1, ?)
                    """,
                    (pid, now),
                )
            self.run_rei_verification(pid)
            self.compute_rei_intelligence_scores(pid)
            self._index_rei_property(pid)
        self.record_event("rei_catalog_seeded", {"properties": len(properties)})

    def ensure_rei_property_profile(self, property_id: int, *, property_type: str = "apartment") -> dict[str, object]:
        row = self.one("SELECT * FROM rei_property_profiles WHERE property_id = ?", (property_id,))
        if row:
            return dict(row)
        now = _utcnow()
        prop = self.one("SELECT * FROM properties WHERE id = ?", (property_id,))
        if prop is None:
            from ..errors import NotFoundError
            raise NotFoundError("property not found")
        ptype = property_type if property_type in PROPERTY_TYPES else "apartment"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_property_profiles (
                    property_id, property_type, characteristics_json, provenance, availability_status, created_at, updated_at
                ) VALUES (?, ?, '{}', 'internal', ?, ?, ?)
                """,
                (property_id, ptype, str(prop.get("availability") or "available"), now, now),
            )
        return dict(self.one("SELECT * FROM rei_property_profiles WHERE property_id = ?", (property_id,)))

    def get_rei_property_bundle(self, property_id: int) -> dict[str, object]:
        prop = self.one("SELECT * FROM properties WHERE id = ? AND deleted_at IS NULL", (property_id,))
        if prop is None:
            from ..errors import NotFoundError
            raise NotFoundError("property not found")
        profile = self.one("SELECT * FROM rei_property_profiles WHERE property_id = ?", (property_id,))
        listing = self.one("SELECT * FROM rei_listings WHERE property_id = ? ORDER BY id DESC LIMIT 1", (property_id,))
        scores = self.all("SELECT * FROM rei_intelligence_scores WHERE property_id = ?", (property_id,))
        verification = self.one("SELECT * FROM rei_verification_scores WHERE property_id = ?", (property_id,))
        return {
            "property": dict(prop),
            "profile": dict(profile) if profile else None,
            "listing": dict(listing) if listing else None,
            "intelligence_scores": {str(s["score_key"]): s["score"] for s in scores},
            "verification": dict(verification) if verification else None,
        }

    def list_rei_enriched_properties(self, *, limit: int = 50, status: str | None = None) -> list[dict[str, object]]:
        query = "SELECT p.* FROM properties p WHERE p.deleted_at IS NULL"
        params: list[object] = []
        if status:
            query += " AND p.status = ?"
            params.append(status)
        query += " ORDER BY p.id DESC LIMIT ?"
        params.append(limit)
        rows = self.all(query, tuple(params))
        return [self.get_rei_property_bundle(int(r["id"])) for r in rows]

    def list_rei_listings(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all("SELECT * FROM rei_listings WHERE status = ? ORDER BY id DESC LIMIT ?", (status, limit))
        else:
            rows = self.all("SELECT * FROM rei_listings ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def create_rei_listing(self, *, property_id: int, title: str) -> dict[str, object]:
        self.ensure_rei_property_profile(property_id)
        now = _utcnow()
        listing_key = f"listing-{uuid.uuid4().hex[:10]}"
        prop = self.one("SELECT * FROM properties WHERE id = ?", (property_id,))
        engine = RealEstatePlatformEngine()
        media_count = self.scalar("SELECT COUNT(*) FROM media WHERE property_id = ?", (property_id,))
        ai_score = engine.listings.ai_listing_score(property_row=dict(prop), has_media=media_count > 0)
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_listings (listing_key, property_id, title, status, ai_score, created_at, updated_at)
                VALUES (?, ?, ?, 'draft', ?, ?, ?)
                """,
                (listing_key, property_id, title, ai_score, now, now),
            )
        self._record_rei_history(property_id, event_type="listing_created", summary=f"Listing {title} created")
        row = self.one("SELECT * FROM rei_listings WHERE listing_key = ?", (listing_key,))
        return dict(row)

    def publish_rei_listing(self, property_id: int) -> dict[str, object]:
        now = _utcnow()
        listing = self.one("SELECT * FROM rei_listings WHERE property_id = ? ORDER BY id DESC LIMIT 1", (property_id,))
        if listing is None:
            prop = self.one("SELECT title FROM properties WHERE id = ?", (property_id,))
            listing = self.create_rei_listing(property_id=property_id, title=str(prop["title"]))
        with self._transaction() as conn:
            conn.execute(
                "UPDATE rei_listings SET status = 'published', published_at = ?, updated_at = ? WHERE id = ?",
                (now, now, listing["id"]),
            )
            conn.execute(
                "UPDATE properties SET status = 'published', published_at = ? WHERE id = ?",
                (now, property_id),
            )
            conn.execute(
                """
                INSERT INTO rei_listing_publications (listing_id, channel, status, published_at, created_at)
                VALUES (?, 'lawim', 'published', ?, ?)
                """,
                (listing["id"], now, now),
            )
        self._record_rei_history(property_id, event_type="listing_published", summary="Listing published")
        return dict(self.one("SELECT * FROM rei_listings WHERE id = ?", (listing["id"],)))

    def archive_rei_listing(self, property_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE rei_listings SET status = 'archived', archived_at = ?, updated_at = ? WHERE property_id = ?",
                (now, now, property_id),
            )
            conn.execute("UPDATE properties SET status = 'archived' WHERE id = ?", (property_id,))
        self._record_rei_history(property_id, event_type="listing_archived", summary="Listing archived")
        listing = self.one("SELECT * FROM rei_listings WHERE property_id = ? ORDER BY id DESC LIMIT 1", (property_id,))
        return dict(listing) if listing else {}

    def duplicate_rei_listing(self, property_id: int) -> dict[str, object]:
        source = self.one("SELECT * FROM rei_listings WHERE property_id = ? ORDER BY id DESC LIMIT 1", (property_id,))
        title = f"{source['title']} (copie)" if source else f"Listing copy {property_id}"
        return self.create_rei_listing(property_id=property_id, title=title)

    def list_rei_owners(self, property_id: int) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM rei_property_owners WHERE property_id = ?", (property_id,))]

    def add_rei_owner(self, property_id: int, *, owner_name: str, owner_type: str = "individual") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_property_owners (property_id, owner_type, owner_name, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (property_id, owner_type, owner_name, now),
            )
        row = self.one("SELECT * FROM rei_property_owners WHERE property_id = ? ORDER BY id DESC LIMIT 1", (property_id,))
        return dict(row)

    def list_rei_documents(self, property_id: int) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM rei_property_documents WHERE property_id = ?", (property_id,))]

    def add_rei_document(self, property_id: int, *, title: str, document_type: str = "other") -> dict[str, object]:
        now = _utcnow()
        doc_key = f"doc-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_property_documents (property_id, document_key, document_type, title, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (property_id, doc_key, document_type, title, now),
            )
        return dict(self.one("SELECT * FROM rei_property_documents WHERE document_key = ?", (doc_key,)))

    def run_rei_verification(self, property_id: int) -> dict[str, object]:
        prop = self.one("SELECT * FROM properties WHERE id = ?", (property_id,))
        owners = self.list_rei_owners(property_id)
        documents = self.list_rei_documents(property_id)
        engine = RealEstatePlatformEngine()
        checks = engine.verification.run_checks(property_row=dict(prop), owners=owners, documents=documents)
        now = _utcnow()
        with self._transaction() as conn:
            for check in checks:
                check_key = f"chk-{check['check_type']}-{property_id}"
                conn.execute(
                    """
                    INSERT OR REPLACE INTO rei_verification_checks (
                        property_id, check_key, check_type, status, anomaly_flags_json, checked_at, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (property_id, check_key, check["check_type"], check["status"], _json(check.get("anomalies")), now, now),
                )
            agg = engine.verification.aggregate_trust(checks)
            conn.execute(
                """
                INSERT OR REPLACE INTO rei_verification_scores (property_id, trust_score, consistency_score, details_json, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (property_id, agg["trust_score"], agg["consistency_score"], _json(agg.get("details")), now),
            )
        return dict(self.one("SELECT * FROM rei_verification_scores WHERE property_id = ?", (property_id,)))

    def get_rei_valuation(self, property_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM rei_property_valuations WHERE property_id = ? ORDER BY id DESC LIMIT 1", (property_id,))
        if row:
            return dict(row)
        prop = self.one("SELECT * FROM properties WHERE id = ?", (property_id,))
        engine = RealEstatePlatformEngine()
        estimate = engine.valuation.estimate(property_row=dict(prop))
        now = _utcnow()
        vkey = f"val-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_property_valuations (
                    property_id, valuation_key, amount, currency, method, confidence, valued_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (property_id, vkey, estimate["amount"], estimate["currency"], estimate["method"], estimate["confidence"], now, now),
            )
        return dict(self.one("SELECT * FROM rei_property_valuations WHERE valuation_key = ?", (vkey,)))

    def run_rei_matching(self, *, user_id: int | None, project_id: int | None, criteria: dict[str, Any]) -> dict[str, object]:
        engine = RealEstatePlatformEngine()
        properties = [dict(r) for r in self.all("SELECT * FROM properties WHERE deleted_at IS NULL AND status = 'published'")]
        matches = engine.matching.match(properties=properties, criteria=criteria)
        now = _utcnow()
        session_key = f"match-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO rei_matching_sessions (session_key, user_id, project_id, criteria_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (session_key, user_id, project_id, _json(criteria), now),
            )
            session_id = int(cursor.lastrowid)
            for rank, match in enumerate(matches, start=1):
                conn.execute(
                    """
                    INSERT INTO rei_matching_results (session_id, property_id, score, reasons_json, rank_position, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (session_id, match["property_id"], match["score"], _json(match.get("reasons")), rank, now),
                )
        return {"session_key": session_key, "session_id": session_id, "results": matches}

    def schedule_rei_visit(self, *, property_id: int, user_id: int | None, scheduled_at: str) -> dict[str, object]:
        now = _utcnow()
        visit_key = f"visit-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_visits (visit_key, property_id, user_id, scheduled_at, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'scheduled', ?, ?)
                """,
                (visit_key, property_id, user_id, scheduled_at, now, now),
            )
        self._record_rei_history(property_id, event_type="visit_scheduled", summary=f"Visit scheduled {scheduled_at}")
        if hasattr(self, "start_automation_instance"):
            try:
                self.start_automation_instance(workflow_key="wf-immobilier-achat", project_id=None, context={"property_id": property_id, "visit": visit_key})
            except Exception:
                pass
        return dict(self.one("SELECT * FROM rei_visits WHERE visit_key = ?", (visit_key,)))

    def confirm_rei_visit(self, visit_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute("UPDATE rei_visits SET status = 'confirmed', confirmed_at = ?, updated_at = ? WHERE id = ?", (now, now, visit_id))
        return dict(self.one("SELECT * FROM rei_visits WHERE id = ?", (visit_id,)))

    def cancel_rei_visit(self, visit_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute("UPDATE rei_visits SET status = 'cancelled', cancelled_at = ?, updated_at = ? WHERE id = ?", (now, now, visit_id))
        return dict(self.one("SELECT * FROM rei_visits WHERE id = ?", (visit_id,)))

    def complete_rei_visit(self, visit_id: int, *, summary: str, rating: int = 3) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute("UPDATE rei_visits SET status = 'completed', updated_at = ? WHERE id = ?", (now, visit_id))
            conn.execute(
                """
                INSERT OR REPLACE INTO rei_visit_reports (visit_id, summary, rating, report_json, created_at)
                VALUES (?, ?, ?, '{}', ?)
                """,
                (visit_id, summary, rating, now),
            )
        visit = self.one("SELECT property_id FROM rei_visits WHERE id = ?", (visit_id,))
        if visit:
            self._record_rei_history(int(visit["property_id"]), event_type="visit_completed", summary=summary)
        return dict(self.one("SELECT * FROM rei_visit_reports WHERE visit_id = ?", (visit_id,)))

    def list_rei_visits(self, *, property_id: int | None = None) -> list[dict[str, object]]:
        if property_id is not None:
            rows = self.all("SELECT * FROM rei_visits WHERE property_id = ? ORDER BY scheduled_at DESC", (property_id,))
        else:
            rows = self.all("SELECT * FROM rei_visits ORDER BY id DESC LIMIT 100")
        return [dict(r) for r in rows]

    def open_rei_negotiation(self, *, property_id: int, buyer_id: int | None) -> dict[str, object]:
        now = _utcnow()
        neg_key = f"neg-{uuid.uuid4().hex[:8]}"
        wf_id = None
        if hasattr(self, "start_automation_instance"):
            try:
                inst = self.start_automation_instance(workflow_key="wf-immobilier-vente", context={"property_id": property_id})
                wf_id = inst.get("id")
            except Exception:
                wf_id = None
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_negotiations (negotiation_key, property_id, buyer_id, status, workflow_instance_id, created_at, updated_at)
                VALUES (?, ?, ?, 'open', ?, ?, ?)
                """,
                (neg_key, property_id, buyer_id, wf_id, now, now),
            )
        self._record_rei_history(property_id, event_type="negotiation_opened", summary="Negotiation opened")
        return dict(self.one("SELECT * FROM rei_negotiations WHERE negotiation_key = ?", (neg_key,)))

    def submit_rei_offer(self, *, negotiation_id: int, amount: int, currency: str = "XAF") -> dict[str, object]:
        now = _utcnow()
        offer_key = f"offer-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_offers (offer_key, negotiation_id, amount, currency, status, submitted_at, created_at)
                VALUES (?, ?, ?, ?, 'submitted', ?, ?)
                """,
                (offer_key, negotiation_id, amount, currency, now, now),
            )
            conn.execute("UPDATE rei_negotiations SET status = 'offer', updated_at = ? WHERE id = ?", (now, negotiation_id))
        return dict(self.one("SELECT * FROM rei_offers WHERE offer_key = ?", (offer_key,)))

    def list_rei_negotiations(self, property_id: int | None = None) -> list[dict[str, object]]:
        if property_id is not None:
            rows = self.all("SELECT * FROM rei_negotiations WHERE property_id = ?", (property_id,))
        else:
            rows = self.all("SELECT * FROM rei_negotiations ORDER BY id DESC LIMIT 100")
        return [dict(r) for r in rows]

    def list_rei_offers(self, negotiation_id: int) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM rei_offers WHERE negotiation_id = ? ORDER BY id ASC", (negotiation_id,))]

    def start_rei_transaction(self, *, property_id: int, transaction_type: str, buyer_id: int | None, amount: int | None) -> dict[str, object]:
        now = _utcnow()
        tx_key = f"tx-{uuid.uuid4().hex[:8]}"
        wf_id = None
        if hasattr(self, "start_automation_instance"):
            try:
                wf_key = "wf-juridique-contrats" if transaction_type == "sale" else "wf-immobilier-achat"
                inst = self.start_automation_instance(workflow_key=wf_key, context={"property_id": property_id, "transaction_type": transaction_type})
                wf_id = inst.get("id")
            except Exception:
                wf_id = None
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_transactions (
                    transaction_key, property_id, transaction_type, status, amount, buyer_id, workflow_instance_id, created_at, updated_at
                ) VALUES (?, ?, ?, 'pending', ?, ?, ?, ?, ?)
                """,
                (tx_key, property_id, transaction_type, amount, buyer_id, wf_id, now, now),
            )
        self._record_rei_history(property_id, event_type="transaction_started", summary=f"Transaction {transaction_type} started")
        return dict(self.one("SELECT * FROM rei_transactions WHERE transaction_key = ?", (tx_key,)))

    def close_rei_transaction(self, transaction_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute("UPDATE rei_transactions SET status = 'closed', closed_at = ?, updated_at = ? WHERE id = ?", (now, now, transaction_id))
        tx = self.one("SELECT property_id FROM rei_transactions WHERE id = ?", (transaction_id,))
        if tx:
            self._record_rei_history(int(tx["property_id"]), event_type="transaction_closed", summary="Transaction closed")
        return dict(self.one("SELECT * FROM rei_transactions WHERE id = ?", (transaction_id,)))

    def list_rei_transactions(self, *, property_id: int | None = None) -> list[dict[str, object]]:
        if property_id is not None:
            rows = self.all("SELECT * FROM rei_transactions WHERE property_id = ?", (property_id,))
        else:
            rows = self.all("SELECT * FROM rei_transactions ORDER BY id DESC LIMIT 100")
        return [dict(r) for r in rows]

    def create_rei_reservation(self, *, property_id: int, user_id: int | None, days: int = 7, amount: int | None = None) -> dict[str, object]:
        now = _utcnow()
        until = (datetime.now(timezone.utc) + timedelta(days=days)).replace(microsecond=0).isoformat()
        res_key = f"res-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_reservations (reservation_key, property_id, user_id, status, reserved_until, amount, created_at)
                VALUES (?, ?, ?, 'pending', ?, ?, ?)
                """,
                (res_key, property_id, user_id, until, amount, now),
            )
        return dict(self.one("SELECT * FROM rei_reservations WHERE reservation_key = ?", (res_key,)))

    def compute_rei_intelligence_scores(self, property_id: int) -> dict[str, int]:
        prop = self.one("SELECT * FROM properties WHERE id = ?", (property_id,))
        verification = self.one("SELECT trust_score FROM rei_verification_scores WHERE property_id = ?", (property_id,))
        listing = self.one("SELECT ai_score FROM rei_listings WHERE property_id = ? ORDER BY id DESC LIMIT 1", (property_id,))
        trust = int(verification["trust_score"]) if verification else 50
        listing_score = int(listing["ai_score"]) if listing else 0
        engine = RealEstatePlatformEngine()
        scores = engine.intelligence.compute_scores(property_row=dict(prop), trust_score=trust, listing_score=listing_score)
        now = _utcnow()
        with self._transaction() as conn:
            for key, value in scores.items():
                conn.execute(
                    """
                    INSERT OR REPLACE INTO rei_intelligence_scores (property_id, score_key, score, computed_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (property_id, key, value, now),
                )
        return scores

    def build_rei_recommendations(self, *, user_id: int | None, project_id: int | None, criteria: dict[str, Any]) -> list[dict[str, object]]:
        engine = RealEstatePlatformEngine()
        match_payload = self.run_rei_matching(user_id=user_id, project_id=project_id, criteria=criteria)
        intel: dict[str, int] = {}
        if match_payload.get("results"):
            pid = int(match_payload["results"][0]["property_id"])
            intel = self.compute_rei_intelligence_scores(pid)
        recs = engine.recommendations.build_recommendations(
            matches=match_payload.get("results") or [],
            intelligence=intel,
            sources=engine.integration_sources(),
        )
        now = _utcnow()
        stored: list[dict[str, object]] = []
        with self._transaction() as conn:
            for rec in recs:
                rkey = f"rec-{uuid.uuid4().hex[:8]}"
                conn.execute(
                    """
                    INSERT INTO rei_recommendations (
                        recommendation_key, user_id, project_id, property_id, recommendation_type, score, title, rationale, sources_json, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        rkey,
                        user_id,
                        project_id,
                        rec.get("property_id"),
                        rec.get("recommendation_type"),
                        rec.get("score"),
                        rec.get("title"),
                        rec.get("rationale"),
                        _json(rec.get("sources")),
                        now,
                    ),
                )
                stored.append(dict(self.one("SELECT * FROM rei_recommendations WHERE recommendation_key = ?", (rkey,))))
        if hasattr(self, "expert_rag_query") and criteria.get("query"):
            try:
                self.expert_rag_query(str(criteria["query"]))
            except Exception:
                pass
        return stored

    def list_rei_recommendations(self, *, user_id: int | None = None) -> list[dict[str, object]]:
        if user_id is not None:
            rows = self.all("SELECT * FROM rei_recommendations WHERE user_id = ? ORDER BY id DESC LIMIT 50", (user_id,))
        else:
            rows = self.all("SELECT * FROM rei_recommendations ORDER BY id DESC LIMIT 50")
        return [dict(r) for r in rows]

    def list_rei_history(self, property_id: int) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM rei_property_history WHERE property_id = ? ORDER BY created_at ASC", (property_id,))
        return [dict(r) for r in rows]

    def rei_search(self, *, query: str, limit: int = 20) -> list[dict[str, object]]:
        engine = RealEstatePlatformEngine()
        normalized = engine.search.normalize(query)
        if not normalized:
            return []
        pattern = f"%{normalized.split()[0]}%"
        rows = self.all(
            """
            SELECT p.* FROM rei_search_index si
            JOIN properties p ON p.id = si.property_id
            WHERE si.index_text LIKE ? AND p.deleted_at IS NULL
            LIMIT ?
            """,
            (pattern, limit),
        )
        return [dict(r) for r in rows]

    def rei_map_properties(self, *, city: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if city:
            rows = self.all(
                "SELECT id, title, latitude, longitude, city, status, price_min, price_max FROM properties WHERE deleted_at IS NULL AND LOWER(city) = LOWER(?) LIMIT ?",
                (city, limit),
            )
        else:
            rows = self.all(
                "SELECT id, title, latitude, longitude, city, status, price_min, price_max FROM properties WHERE deleted_at IS NULL AND latitude IS NOT NULL LIMIT ?",
                (limit,),
            )
        return [dict(r) for r in rows]

    def rei_nearby(self, property_id: int, *, limit: int = 10) -> list[dict[str, object]]:
        origin = self.one("SELECT latitude, longitude FROM properties WHERE id = ?", (property_id,))
        if not origin or origin.get("latitude") is None:
            return []
        engine = RealEstatePlatformEngine()
        lat1, lon1 = float(origin["latitude"]), float(origin["longitude"])
        candidates = self.all(
            "SELECT id, title, latitude, longitude, city FROM properties WHERE deleted_at IS NULL AND id != ? AND latitude IS NOT NULL",
            (property_id,),
        )
        ranked: list[tuple[float, dict[str, object]]] = []
        now = _utcnow()
        for cand in candidates:
            dist = engine.geo.haversine_km(lat1, lon1, float(cand["latitude"]), float(cand["longitude"]))
            if dist <= 25:
                ranked.append((dist, dict(cand)))
        ranked.sort(key=lambda item: item[0])
        results: list[dict[str, object]] = []
        with self._transaction() as conn:
            for dist, cand in ranked[:limit]:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO rei_nearby_properties (property_id, nearby_property_id, distance_km, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (property_id, cand["id"], dist, now),
                )
                cand["distance_km"] = dist
                results.append(cand)
        return results

    def rei_analytics(self) -> dict[str, object]:
        return {
            "properties": self.scalar("SELECT COUNT(*) FROM properties WHERE deleted_at IS NULL"),
            "published_listings": self.scalar("SELECT COUNT(*) FROM rei_listings WHERE status = 'published'"),
            "visits_scheduled": self.scalar("SELECT COUNT(*) FROM rei_visits WHERE status IN ('scheduled', 'confirmed')"),
            "transactions_open": self.scalar("SELECT COUNT(*) FROM rei_transactions WHERE status NOT IN ('closed', 'cancelled')"),
            "avg_trust_score": self.scalar("SELECT COALESCE(AVG(trust_score), 0) FROM rei_verification_scores"),
            "matching_sessions": self.scalar("SELECT COUNT(*) FROM rei_matching_sessions"),
        }

    def rei_stats(self) -> dict[str, object]:
        analytics = self.rei_analytics()
        return {**analytics, "recommendations": self.scalar("SELECT COUNT(*) FROM rei_recommendations")}

    def generate_rei_report(self, property_id: int, *, report_type: str = "summary") -> dict[str, object]:
        bundle = self.get_rei_property_bundle(property_id)
        now = _utcnow()
        report_key = f"report-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_property_reports (report_key, property_id, report_type, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (report_key, property_id, report_type, _json(bundle), now),
            )
        return {"report_key": report_key, "property_id": property_id, "report_type": report_type, "payload": bundle}

    def _index_rei_property(self, property_id: int) -> None:
        prop = self.one("SELECT * FROM properties WHERE id = ?", (property_id,))
        if prop is None:
            return
        engine = RealEstatePlatformEngine()
        index_text = engine.search.build_index(dict(prop))
        geo_hash = engine.geo.geo_hash(float(prop["latitude"]), float(prop["longitude"])) if prop.get("latitude") else None
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO rei_search_index (property_id, index_text, geo_hash, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (property_id, index_text, geo_hash, now),
            )

    def _record_rei_history(self, property_id: int, *, event_type: str, summary: str, actor_id: int | None = None) -> None:
        now = _utcnow()
        event_key = f"hist-{event_type}-{uuid.uuid4().hex[:6]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_property_history (property_id, event_type, event_key, summary, actor_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (property_id, event_type, event_key, summary, actor_id, now),
            )

    def snapshot_rei_analytics(self) -> dict[str, object]:
        stats = self.rei_analytics()
        now = _utcnow()
        key = f"snapshot-{now}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO rei_analytics_snapshots (snapshot_key, scope, metrics_json, created_at)
                VALUES (?, 'global', ?, ?)
                """,
                (key, _json(stats), now),
            )
        return {"snapshot_key": key, "metrics": stats}
