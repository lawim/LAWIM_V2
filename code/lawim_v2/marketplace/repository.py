from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from ..repository_introspection import table_exists
from .constants import (
    PARTNER_REGISTRATION_STATUSES,
    PAYMENT_METHODS,
    PROVIDER_TYPES,
    REQUEST_STATUSES,
    SERVICE_CATEGORIES,
)
from .engines import MarketplacePlatformEngine


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


def _marketplace_provider_to_partner_type(provider_type: str) -> str:
    mapping = {
        "company": "property_manager",
        "individual": "artisan",
        "agency": "real_estate_agency",
        "freelancer": "artisan",
        "enterprise": "construction_company",
        "collective": "property_manager",
    }
    return mapping.get(provider_type, "property_manager")


class MarketplaceRepositoryMixin:
    def marketplace_tables_present(self) -> bool:
        return table_exists(self, "marketplace_provider_profiles")

    def seed_marketplace_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM marketplace_catalog_categories") > 0:
            return
        engine = MarketplacePlatformEngine()
        now = _utcnow()
        categories = [
            ("cat-legal", "Juridique & Notaire", "legal_notary", 0),
            ("cat-finance", "Financement", "financing", 1),
            ("cat-renovation", "Rénovation", "renovation", 2),
            ("cat-inspection", "Inspection", "inspection", 3),
            ("cat-moving", "Déménagement", "moving", 4),
        ]
        with self._transaction() as conn:
            for category_key, name, cat, position in categories:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO marketplace_catalog_categories (
                        category_key, name, description, position, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (category_key, name, f"Services {name}", position, now, now),
                )
            conn.execute(
                """
                INSERT OR IGNORE INTO marketplace_subscription_plans (
                    plan_key, name, description, price, currency, billing_period, features_json, status, created_at, updated_at
                ) VALUES ('plan-provider-basic', 'Prestataire Basic', 'Visibilité marketplace standard', 25000, 'XAF', 'monthly', '[]', 'active', ?, ?)
                """,
                (now, now),
            )
            conn.execute(
                """
                INSERT OR IGNORE INTO marketplace_commission_rules (
                    rule_key, name, commission_type, rate_percent, flat_amount, currency, status, created_at, updated_at
                ) VALUES ('rule-default', 'Commission LAWIM standard', 'percentage', 10.0, 0, 'XAF', 'active', ?, ?)
                """,
                (now, now),
            )
        self._seed_marketplace_demo_data(engine)
        self.record_event("marketplace_catalog_seeded", {"categories": len(categories)})

    def _seed_marketplace_demo_data(self, engine: MarketplacePlatformEngine) -> None:
        partners = self.all("SELECT * FROM partner_profiles WHERE status = 'active' ORDER BY id ASC")
        if not partners:
            return
        services = self.all("SELECT * FROM service_catalog WHERE status = 'active' ORDER BY id ASC")
        categories = self.all("SELECT * FROM marketplace_catalog_categories ORDER BY position ASC")
        category_by_key = {str(c["category_key"]): c for c in categories}
        now = _utcnow()
        for partner in partners:
            partner_id = int(partner["id"])
            existing = self.one(
                "SELECT id FROM marketplace_provider_profiles WHERE partner_profile_id = ?",
                (partner_id,),
            )
            if existing:
                continue
            provider = self.create_marketplace_provider(
                partner_profile_id=partner_id,
                provider_type="company" if str(partner.get("partner_type")) != "individual" else "individual",
                headline=str(partner.get("display_name") or "Prestataire LAWIM"),
                bio=str(partner.get("description") or ""),
            )
            provider_id = int(provider["id"])
            self.add_marketplace_provider_certification(
                provider_id,
                certification_key="cert-lawim-partner",
                title="Partenaire LAWIM vérifié",
                issuer="LAWIM",
            )
            for day in range(1, 6):
                self.set_marketplace_availability(provider_id, day_of_week=day, start_time="08:00", end_time="18:00")
            self.add_marketplace_portfolio_item(
                provider_id,
                title=f"Réalisations — {partner.get('display_name')}",
                category="consulting",
                description="Portfolio démo marketplace",
            )
            self.compute_marketplace_reputation(provider_id)
        providers = self.all("SELECT * FROM marketplace_provider_profiles ORDER BY id ASC")
        for service in services[:5]:
            cat_row = category_by_key.get("cat-legal") or (categories[0] if categories else None)
            if cat_row is None:
                continue
            marketplace_cat = engine.catalog.normalize_category(str(service.get("category") or "other"))
            if marketplace_cat not in SERVICE_CATEGORIES:
                marketplace_cat = "other"
            provider = providers[int(service["id"]) % len(providers)] if providers else None
            self.create_marketplace_catalog_item(
                category_id=int(cat_row["id"]),
                title=str(service.get("title") or "Service"),
                description=str(service.get("description") or ""),
                category=marketplace_cat,
                service_catalog_id=int(service["id"]),
                provider_profile_id=int(provider["id"]) if provider else None,
                price_min=int(service.get("indicative_price_min") or 0) or None,
                price_max=int(service.get("indicative_price_max") or 0) or None,
                status="active",
            )
        if providers:
            request = self.create_marketplace_request(
                title="Demande démo inspection bien",
                description="Inspection avant achat — marketplace demo",
                category="inspection",
                city="Douala",
                region="Littoral",
                budget_min=150000,
                budget_max=350000,
                status="submitted",
            )
            self.run_marketplace_matching(int(request["id"]))
        self.snapshot_marketplace_analytics()

    # --- Integration hooks ---

    def marketplace_integrations(self) -> dict[str, object]:
        engine = MarketplacePlatformEngine()
        payload: dict[str, object] = {"sources": engine.integration_sources()}
        if hasattr(self, "start_automation_instance"):
            try:
                payload["workflow_automation"] = True
            except Exception:
                payload["workflow_automation"] = False
        if hasattr(self, "get_crm_contact"):
            payload["crm"] = True
        if hasattr(self, "get_rei_property_bundle"):
            payload["real_estate_intelligence"] = True
        if hasattr(self, "expert_rag_query"):
            payload["knowledge_platform"] = True
        if hasattr(self, "assistant_chat"):
            payload["assistant"] = True
        return payload

    def marketplace_link_contact(self, contact_id: int) -> dict[str, object] | None:
        engine = MarketplacePlatformEngine()
        return engine.ai.link_crm_contact(self, contact_id=contact_id)

    def marketplace_link_property(self, property_id: int) -> dict[str, object] | None:
        engine = MarketplacePlatformEngine()
        return engine.ai.link_property(self, property_id=property_id)

    def marketplace_trigger_workflow(self, *, workflow_key: str, context: dict[str, object]) -> dict[str, object] | None:
        engine = MarketplacePlatformEngine()
        return engine.ai.trigger_workflow(self, workflow_key=workflow_key, context=context)

    # --- Partner registrations ---

    def create_marketplace_partner_registration(
        self,
        *,
        applicant_name: str,
        applicant_email: str = "",
        applicant_phone: str = "",
        provider_type: str = "company",
        organization_id: int | None = None,
        partner_profile_id: int | None = None,
        service_categories: list[str] | None = None,
        status: str = "draft",
    ) -> dict[str, object]:
        if provider_type not in PROVIDER_TYPES:
            provider_type = "company"
        if status not in PARTNER_REGISTRATION_STATUSES:
            status = "draft"
        now = _utcnow()
        key = f"reg-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_partner_registrations (
                    registration_key, partner_profile_id, organization_id, applicant_name,
                    applicant_email, applicant_phone, provider_type, status,
                    service_categories_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    partner_profile_id,
                    organization_id,
                    applicant_name,
                    applicant_email,
                    applicant_phone,
                    provider_type,
                    status,
                    _json(service_categories or []),
                    now,
                    now,
                ),
            )
        return dict(self.one("SELECT * FROM marketplace_partner_registrations WHERE registration_key = ?", (key,)))

    def get_marketplace_partner_registration(self, registration_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM marketplace_partner_registrations WHERE id = ?", (registration_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("registration not found")
        return dict(row)

    def list_marketplace_partner_registrations(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM marketplace_partner_registrations WHERE status = ? ORDER BY id DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT * FROM marketplace_partner_registrations ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def update_marketplace_partner_registration(self, registration_id: int, **fields: object) -> dict[str, object]:
        allowed = {"status", "notes", "partner_profile_id", "reviewed_by", "reviewed_at", "metadata_json"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if "metadata" in fields and fields["metadata"] is not None:
            updates["metadata_json"] = _json(fields["metadata"])
        if not updates:
            return self.get_marketplace_partner_registration(registration_id)
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(
                f"UPDATE marketplace_partner_registrations SET {cols} WHERE id = ?",
                (*updates.values(), registration_id),
            )
        return self.get_marketplace_partner_registration(registration_id)

    def approve_marketplace_partner_registration(self, registration_id: int, *, reviewer_id: int | None = None) -> dict[str, object]:
        reg = self.get_marketplace_partner_registration(registration_id)
        partner_id = reg.get("partner_profile_id")
        if partner_id is None:
            org_id = reg.get("organization_id")
            if org_id and hasattr(self, "create_partner_profile"):
                partner = self.create_partner_profile(
                    organization_id=int(org_id),
                    partner_type=_marketplace_provider_to_partner_type(str(reg.get("provider_type") or "company")),
                    display_name=str(reg.get("applicant_name") or "Partner"),
                    description=str(reg.get("notes") or ""),
                )
                partner_id = partner["id"]
        now = _utcnow()
        reg = self.update_marketplace_partner_registration(
            registration_id,
            status="approved",
            partner_profile_id=int(partner_id) if partner_id else None,
            reviewed_by=reviewer_id,
            reviewed_at=now,
        )
        if partner_id:
            existing = self.one(
                "SELECT id FROM marketplace_provider_profiles WHERE partner_profile_id = ?",
                (int(partner_id),),
            )
            if existing is None:
                self.create_marketplace_provider(
                    partner_profile_id=int(partner_id),
                    provider_type=str(reg.get("provider_type") or "company"),
                    headline=str(reg.get("applicant_name") or ""),
                )
        return reg

    # --- Providers ---

    def create_marketplace_provider(
        self,
        *,
        partner_profile_id: int,
        provider_type: str = "company",
        headline: str = "",
        bio: str = "",
        service_radius_km: int = 50,
        featured: bool = False,
    ) -> dict[str, object]:
        if provider_type not in PROVIDER_TYPES:
            provider_type = "company"
        now = _utcnow()
        key = f"provider-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_provider_profiles (
                    provider_key, partner_profile_id, provider_type, headline, bio,
                    service_radius_km, status, featured, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?, ?)
                """,
                (key, partner_profile_id, provider_type, headline, bio, service_radius_km, int(featured), now, now),
            )
        return dict(self.one("SELECT * FROM marketplace_provider_profiles WHERE provider_key = ?", (key,)))

    def get_marketplace_provider(self, provider_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM marketplace_provider_profiles WHERE id = ?", (provider_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("provider not found")
        return dict(row)

    def list_marketplace_providers(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM marketplace_provider_profiles WHERE status = ? ORDER BY featured DESC, id DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all(
                "SELECT * FROM marketplace_provider_profiles ORDER BY featured DESC, id DESC LIMIT ?",
                (limit,),
            )
        return [dict(r) for r in rows]

    def update_marketplace_provider(self, provider_id: int, **fields: object) -> dict[str, object]:
        allowed = {"headline", "bio", "service_radius_km", "status", "featured", "provider_type", "metadata_json"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if "metadata" in fields and fields["metadata"] is not None:
            updates["metadata_json"] = _json(fields["metadata"])
        if not updates:
            return self.get_marketplace_provider(provider_id)
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE marketplace_provider_profiles SET {cols} WHERE id = ?", (*updates.values(), provider_id))
        return self.get_marketplace_provider(provider_id)

    def get_marketplace_provider_bundle(self, provider_id: int) -> dict[str, object]:
        provider = self.get_marketplace_provider(provider_id)
        partner = self.one("SELECT * FROM partner_profiles WHERE id = ?", (int(provider["partner_profile_id"]),))
        certifications = self.all(
            "SELECT * FROM marketplace_provider_certifications WHERE provider_profile_id = ?",
            (provider_id,),
        )
        reputation = self.all(
            "SELECT score_key, score FROM marketplace_reputation_snapshots WHERE provider_profile_id = ?",
            (provider_id,),
        )
        portfolio = self.all(
            "SELECT * FROM marketplace_portfolio_items WHERE provider_profile_id = ? ORDER BY id DESC LIMIT 10",
            (provider_id,),
        )
        return {
            "provider": provider,
            "partner": dict(partner) if partner else None,
            "certifications": [dict(c) for c in certifications],
            "reputation": {str(r["score_key"]): r["score"] for r in reputation},
            "portfolio": [dict(p) for p in portfolio],
        }

    def add_marketplace_provider_certification(
        self,
        provider_id: int,
        *,
        certification_key: str,
        title: str,
        issuer: str = "",
    ) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO marketplace_provider_certifications (
                    provider_profile_id, certification_key, title, issuer, issued_at, status, created_at
                ) VALUES (?, ?, ?, ?, ?, 'active', ?)
                """,
                (provider_id, certification_key, title, issuer, now, now),
            )
        row = self.one(
            "SELECT * FROM marketplace_provider_certifications WHERE provider_profile_id = ? AND certification_key = ?",
            (provider_id, certification_key),
        )
        return dict(row)

    # --- Catalog ---

    def create_marketplace_catalog_category(self, *, name: str, category_key: str | None = None, description: str = "") -> dict[str, object]:
        now = _utcnow()
        key = category_key or f"cat-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_catalog_categories (category_key, name, description, status, created_at, updated_at)
                VALUES (?, ?, ?, 'active', ?, ?)
                """,
                (key, name, description, now, now),
            )
        return dict(self.one("SELECT * FROM marketplace_catalog_categories WHERE category_key = ?", (key,)))

    def list_marketplace_catalog_categories(self) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM marketplace_catalog_categories ORDER BY position ASC, id ASC")]

    def create_marketplace_catalog_item(
        self,
        *,
        category_id: int,
        title: str,
        description: str = "",
        category: str = "other",
        service_catalog_id: int | None = None,
        provider_profile_id: int | None = None,
        price_min: int | None = None,
        price_max: int | None = None,
        currency: str = "XAF",
        duration_days: int | None = None,
        status: str = "draft",
    ) -> dict[str, object]:
        engine = MarketplacePlatformEngine()
        category = engine.catalog.normalize_category(category)
        now = _utcnow()
        key = f"item-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_catalog_items (
                    item_key, category_id, service_catalog_id, provider_profile_id, title, description,
                    category, price_min, price_max, currency, duration_days, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    category_id,
                    service_catalog_id,
                    provider_profile_id,
                    title,
                    description,
                    category,
                    price_min,
                    price_max,
                    currency,
                    duration_days,
                    status,
                    now,
                    now,
                ),
            )
        return dict(self.one("SELECT * FROM marketplace_catalog_items WHERE item_key = ?", (key,)))

    def get_marketplace_catalog_item(self, item_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM marketplace_catalog_items WHERE id = ?", (item_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("catalog item not found")
        return dict(row)

    def list_marketplace_catalog_items(
        self,
        *,
        category: str | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, object]]:
        query = "SELECT * FROM marketplace_catalog_items WHERE 1=1"
        params: list[object] = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(r) for r in self.all(query, tuple(params))]

    def update_marketplace_catalog_item(self, item_id: int, **fields: object) -> dict[str, object]:
        allowed = {"title", "description", "category", "price_min", "price_max", "status", "duration_days", "metadata_json"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if not updates:
            return self.get_marketplace_catalog_item(item_id)
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE marketplace_catalog_items SET {cols} WHERE id = ?", (*updates.values(), item_id))
        return self.get_marketplace_catalog_item(item_id)

    # --- Service requests ---

    def create_marketplace_request(
        self,
        *,
        title: str,
        description: str = "",
        category: str = "other",
        city: str = "",
        region: str = "",
        country: str = "Cameroon",
        budget_min: int | None = None,
        budget_max: int | None = None,
        currency: str = "XAF",
        user_id: int | None = None,
        contact_id: int | None = None,
        project_id: int | None = None,
        property_id: int | None = None,
        catalog_item_id: int | None = None,
        status: str = "draft",
        criteria: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = MarketplacePlatformEngine()
        category = engine.catalog.normalize_category(category)
        if status not in REQUEST_STATUSES:
            status = "draft"
        if contact_id:
            self.marketplace_link_contact(int(contact_id))
        if property_id:
            self.marketplace_link_property(int(property_id))
        now = _utcnow()
        key = f"req-{uuid.uuid4().hex[:10]}"
        submitted_at = now if status != "draft" else None
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_service_requests (
                    request_key, user_id, contact_id, project_id, property_id, catalog_item_id,
                    title, description, category, city, region, country, budget_min, budget_max,
                    currency, status, criteria_json, submitted_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    user_id,
                    contact_id,
                    project_id,
                    property_id,
                    catalog_item_id,
                    title,
                    description,
                    category,
                    city,
                    region,
                    country,
                    budget_min,
                    budget_max,
                    currency,
                    status,
                    _json(criteria or {}),
                    submitted_at,
                    now,
                    now,
                ),
            )
        return dict(self.one("SELECT * FROM marketplace_service_requests WHERE request_key = ?", (key,)))

    def get_marketplace_request(self, request_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM marketplace_service_requests WHERE id = ?", (request_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("request not found")
        return dict(row)

    def list_marketplace_requests(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM marketplace_service_requests WHERE status = ? ORDER BY id DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT * FROM marketplace_service_requests ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def update_marketplace_request(self, request_id: int, **fields: object) -> dict[str, object]:
        allowed = {"title", "description", "status", "budget_min", "budget_max", "city", "region", "metadata_json"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if "criteria" in fields and fields["criteria"] is not None:
            updates["criteria_json"] = _json(fields["criteria"])
        if not updates:
            return self.get_marketplace_request(request_id)
        if updates.get("status") == "submitted":
            updates["submitted_at"] = _utcnow()
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE marketplace_service_requests SET {cols} WHERE id = ?", (*updates.values(), request_id))
        return self.get_marketplace_request(request_id)

    def add_marketplace_request_document(
        self,
        request_id: int,
        *,
        title: str,
        document_type: str = "other",
        storage_ref: str = "",
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"rdoc-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_request_documents (
                    request_id, document_key, title, document_type, storage_ref, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (request_id, key, title, document_type, storage_ref, now),
            )
        return dict(self.one("SELECT * FROM marketplace_request_documents WHERE document_key = ?", (key,)))

    # --- Quotes ---

    def create_marketplace_quote(
        self,
        *,
        request_id: int,
        provider_profile_id: int,
        lines: list[dict[str, object]] | None = None,
        notes: str = "",
        valid_days: int = 14,
    ) -> dict[str, object]:
        engine = MarketplacePlatformEngine()
        raw_lines = lines or [engine.quotes.build_line(description="Prestation standard", unit_price=100000)]
        built_lines: list[dict[str, object]] = []
        for line in raw_lines:
            if line.get("amount") is None:
                built_lines.append(
                    engine.quotes.build_line(
                        description=str(line.get("description") or "Line item"),
                        quantity=int(line.get("quantity") or 1),
                        unit_price=int(line.get("unit_price") or 0),
                    )
                )
            else:
                built_lines.append(line)
        total = engine.quotes.compute_total(built_lines)
        now = _utcnow()
        key = f"quote-{uuid.uuid4().hex[:10]}"
        valid_until = (datetime.now(timezone.utc) + timedelta(days=valid_days)).replace(microsecond=0).isoformat()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_quotes (
                    quote_key, request_id, provider_profile_id, status, amount, valid_until, notes, created_at, updated_at
                ) VALUES (?, ?, ?, 'draft', ?, ?, ?, ?, ?)
                """,
                (key, request_id, provider_profile_id, total, valid_until, notes, now, now),
            )
            quote = self.one("SELECT id FROM marketplace_quotes WHERE quote_key = ?", (key,))
            quote_id = int(quote["id"])
            for idx, line in enumerate(built_lines):
                conn.execute(
                    """
                    INSERT INTO marketplace_quote_lines (
                        quote_id, line_key, description, quantity, unit_price, amount, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quote_id,
                        f"line-{idx + 1}",
                        line["description"],
                        line["quantity"],
                        line["unit_price"],
                        line["amount"],
                        now,
                    ),
                )
        return self.get_marketplace_quote(quote_id)

    def get_marketplace_quote(self, quote_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM marketplace_quotes WHERE id = ?", (quote_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("quote not found")
        result = dict(row)
        result["lines"] = [
            dict(l)
            for l in self.all("SELECT * FROM marketplace_quote_lines WHERE quote_id = ? ORDER BY id ASC", (quote_id,))
        ]
        return result

    def list_marketplace_quotes(self, *, request_id: int | None = None, status: str | None = None) -> list[dict[str, object]]:
        query = "SELECT * FROM marketplace_quotes WHERE 1=1"
        params: list[object] = []
        if request_id is not None:
            query += " AND request_id = ?"
            params.append(request_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC"
        return [self.get_marketplace_quote(int(r["id"])) for r in self.all(query, tuple(params))]

    def send_marketplace_quote(self, quote_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE marketplace_quotes SET status = 'sent', sent_at = ?, updated_at = ? WHERE id = ?",
                (now, now, quote_id),
            )
        return self.get_marketplace_quote(quote_id)

    def accept_marketplace_quote(self, quote_id: int) -> dict[str, object]:
        quote = self.get_marketplace_quote(quote_id)
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE marketplace_quotes SET status = 'accepted', accepted_at = ?, updated_at = ? WHERE id = ?",
                (now, now, quote_id),
            )
        self.update_marketplace_request(int(quote["request_id"]), status="quoted")
        return self.get_marketplace_quote(quote_id)

    # --- Contracts ---

    def create_marketplace_contract(self, *, quote_id: int) -> dict[str, object]:
        quote = self.get_marketplace_quote(quote_id)
        if str(quote.get("status")) != "accepted":
            from ..errors import ValidationError
            raise ValidationError("quote must be accepted before contract")
        now = _utcnow()
        key = f"contract-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_contracts (
                    contract_key, request_id, quote_id, provider_profile_id, status,
                    amount, currency, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'draft', ?, ?, ?, ?)
                """,
                (
                    key,
                    quote["request_id"],
                    quote_id,
                    quote["provider_profile_id"],
                    quote["amount"],
                    quote.get("currency", "XAF"),
                    now,
                    now,
                ),
            )
        row = self.one("SELECT * FROM marketplace_contracts WHERE contract_key = ?", (key,))
        contract_id = int(row["id"])
        self.compute_marketplace_commission(contract_id)
        self.update_marketplace_request(int(quote["request_id"]), status="contracted")
        return dict(row)

    def get_marketplace_contract(self, contract_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM marketplace_contracts WHERE id = ?", (contract_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("contract not found")
        return dict(row)

    def list_marketplace_contracts(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM marketplace_contracts WHERE status = ? ORDER BY id DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT * FROM marketplace_contracts ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def activate_marketplace_contract(self, contract_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                UPDATE marketplace_contracts
                SET status = 'active', signed_at = ?, starts_at = ?, updated_at = ?
                WHERE id = ?
                """,
                (now, now, now, contract_id),
            )
        contract = self.get_marketplace_contract(contract_id)
        self.create_marketplace_mission(
            contract_id=contract_id,
            provider_profile_id=int(contract["provider_profile_id"]),
            title=f"Mission — {contract['contract_key']}",
        )
        self.marketplace_trigger_workflow(
            workflow_key="workflow-marketplace-contract",
            context={"contract_id": contract_id},
        )
        return contract

    # --- Missions ---

    def create_marketplace_mission(
        self,
        *,
        contract_id: int,
        provider_profile_id: int,
        title: str,
        scheduled_start: str | None = None,
        scheduled_end: str | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"mission-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_missions (
                    mission_key, contract_id, provider_profile_id, title, status,
                    scheduled_start, scheduled_end, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'planned', ?, ?, ?, ?)
                """,
                (key, contract_id, provider_profile_id, title, scheduled_start, scheduled_end, now, now),
            )
            mission = self.one("SELECT id FROM marketplace_missions WHERE mission_key = ?", (key,))
            mission_id = int(mission["id"])
            for idx, milestone_title in enumerate(("Kickoff", "Exécution", "Livraison"), start=1):
                conn.execute(
                    """
                    INSERT INTO marketplace_mission_milestones (
                        mission_id, milestone_key, title, position, status, created_at
                    ) VALUES (?, ?, ?, ?, 'pending', ?)
                    """,
                    (mission_id, f"ms-{idx}", milestone_title, idx, now),
                )
        return dict(self.one("SELECT * FROM marketplace_missions WHERE mission_key = ?", (key,)))

    def get_marketplace_mission(self, mission_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM marketplace_missions WHERE id = ?", (mission_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("mission not found")
        result = dict(row)
        result["milestones"] = [
            dict(m)
            for m in self.all(
                "SELECT * FROM marketplace_mission_milestones WHERE mission_id = ? ORDER BY position ASC",
                (mission_id,),
            )
        ]
        result["deliverables"] = [
            dict(d)
            for d in self.all("SELECT * FROM marketplace_mission_deliverables WHERE mission_id = ?", (mission_id,))
        ]
        return result

    def list_marketplace_missions(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT id FROM marketplace_missions WHERE status = ? ORDER BY id DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT id FROM marketplace_missions ORDER BY id DESC LIMIT ?", (limit,))
        return [self.get_marketplace_mission(int(r["id"])) for r in rows]

    def update_marketplace_mission(self, mission_id: int, **fields: object) -> dict[str, object]:
        allowed = {"status", "progress_percent", "scheduled_start", "scheduled_end", "actual_start", "actual_end"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if not updates:
            return self.get_marketplace_mission(mission_id)
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE marketplace_missions SET {cols} WHERE id = ?", (*updates.values(), mission_id))
        return self.get_marketplace_mission(mission_id)

    def add_marketplace_mission_deliverable(
        self,
        mission_id: int,
        *,
        title: str,
        description: str = "",
        storage_ref: str = "",
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"del-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_mission_deliverables (
                    mission_id, deliverable_key, title, description, storage_ref, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (mission_id, key, title, description, storage_ref, now),
            )
        return dict(self.one("SELECT * FROM marketplace_mission_deliverables WHERE deliverable_key = ?", (key,)))

    # --- Availability ---

    def set_marketplace_availability(
        self,
        provider_id: int,
        *,
        day_of_week: int,
        start_time: str = "08:00",
        end_time: str = "18:00",
        timezone: str = "Africa/Douala",
    ) -> dict[str, object]:
        now = _utcnow()
        existing = self.one(
            "SELECT id FROM marketplace_availability WHERE provider_profile_id = ? AND day_of_week = ?",
            (provider_id, day_of_week),
        )
        with self._transaction() as conn:
            if existing:
                conn.execute(
                    """
                    UPDATE marketplace_availability
                    SET start_time = ?, end_time = ?, timezone = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (start_time, end_time, timezone, now, int(existing["id"])),
                )
                row = self.one("SELECT * FROM marketplace_availability WHERE id = ?", (int(existing["id"]),))
            else:
                conn.execute(
                    """
                    INSERT INTO marketplace_availability (
                        provider_profile_id, day_of_week, start_time, end_time, timezone, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (provider_id, day_of_week, start_time, end_time, timezone, now, now),
                )
                row = self.one(
                    "SELECT * FROM marketplace_availability WHERE provider_profile_id = ? AND day_of_week = ?",
                    (provider_id, day_of_week),
                )
        return dict(row)

    def list_marketplace_availability(self, provider_id: int) -> list[dict[str, object]]:
        rows = self.all(
            "SELECT * FROM marketplace_availability WHERE provider_profile_id = ? ORDER BY day_of_week ASC",
            (provider_id,),
        )
        return [dict(r) for r in rows]

    # --- Reviews ---

    def create_marketplace_review(
        self,
        *,
        provider_profile_id: int,
        rating: int = 5,
        title: str = "",
        body: str = "",
        mission_id: int | None = None,
        user_id: int | None = None,
    ) -> dict[str, object]:
        rating = max(1, min(5, rating))
        now = _utcnow()
        key = f"review-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_reviews (
                    review_key, provider_profile_id, mission_id, user_id, rating, title, body, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)
                """,
                (key, provider_profile_id, mission_id, user_id, rating, title, body, now, now),
            )
            review = self.one("SELECT * FROM marketplace_reviews WHERE review_key = ?", (key,))
            conn.execute(
                """
                INSERT INTO marketplace_review_moderation (review_id, action, created_at)
                VALUES (?, 'pending', ?)
                """,
                (int(review["id"]), now),
            )
        self.compute_marketplace_reputation(provider_profile_id)
        return dict(review)

    def list_marketplace_reviews(self, *, provider_id: int | None = None, status: str | None = None) -> list[dict[str, object]]:
        query = "SELECT * FROM marketplace_reviews WHERE 1=1"
        params: list[object] = []
        if provider_id is not None:
            query += " AND provider_profile_id = ?"
            params.append(provider_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC"
        return [dict(r) for r in self.all(query, tuple(params))]

    def publish_marketplace_review(self, review_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE marketplace_reviews SET status = 'published', published_at = ?, updated_at = ? WHERE id = ?",
                (now, now, review_id),
            )
            conn.execute(
                "UPDATE marketplace_review_moderation SET action = 'approved' WHERE review_id = ?",
                (review_id,),
            )
        row = self.one("SELECT * FROM marketplace_reviews WHERE id = ?", (review_id,))
        return dict(row)

    # --- Reputation ---

    def compute_marketplace_reputation(self, provider_id: int) -> dict[str, int]:
        engine = MarketplacePlatformEngine()
        provider = self.get_marketplace_provider(provider_id)
        partner = self.one("SELECT * FROM partner_profiles WHERE id = ?", (int(provider["partner_profile_id"]),))
        reviews = self.list_marketplace_reviews(provider_id=provider_id, status="published")
        missions_done = self.scalar(
            "SELECT COUNT(*) FROM marketplace_missions WHERE provider_profile_id = ? AND status IN ('delivered', 'accepted', 'closed')",
            (provider_id,),
        )
        scores = engine.reputation.compute_scores(
            partner=dict(partner) if partner else {},
            reviews=reviews,
            missions_completed=int(missions_done or 0),
        )
        now = _utcnow()
        with self._transaction() as conn:
            for score_key, score in scores.items():
                conn.execute(
                    """
                    INSERT INTO marketplace_reputation_snapshots (provider_profile_id, score_key, score, computed_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(provider_profile_id, score_key) DO UPDATE SET score = excluded.score, computed_at = excluded.computed_at
                    """,
                    (provider_id, score_key, score, now),
                )
        return scores

    def get_marketplace_reputation(self, provider_id: int) -> dict[str, int]:
        rows = self.all(
            "SELECT score_key, score FROM marketplace_reputation_snapshots WHERE provider_profile_id = ?",
            (provider_id,),
        )
        if not rows:
            return self.compute_marketplace_reputation(provider_id)
        return {str(r["score_key"]): int(r["score"]) for r in rows}

    # --- Disputes ---

    def open_marketplace_dispute(
        self,
        *,
        contract_id: int,
        reason: str,
        mission_id: int | None = None,
        opened_by_user_id: int | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"dispute-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_disputes (
                    dispute_key, contract_id, mission_id, opened_by_user_id, status, reason, opened_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'open', ?, ?, ?, ?)
                """,
                (key, contract_id, mission_id, opened_by_user_id, reason, now, now, now),
            )
        return dict(self.one("SELECT * FROM marketplace_disputes WHERE dispute_key = ?", (key,)))

    def list_marketplace_disputes(self, *, status: str | None = None) -> list[dict[str, object]]:
        if status:
            rows = self.all("SELECT * FROM marketplace_disputes WHERE status = ? ORDER BY id DESC", (status,))
        else:
            rows = self.all("SELECT * FROM marketplace_disputes ORDER BY id DESC")
        return [dict(r) for r in rows]

    def add_marketplace_dispute_message(
        self,
        dispute_id: int,
        *,
        message: str,
        author_user_id: int | None = None,
        visibility: str = "parties",
    ) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_dispute_messages (dispute_id, author_user_id, message, visibility, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (dispute_id, author_user_id, message, visibility, now),
            )
        return dict(
            self.one(
                "SELECT * FROM marketplace_dispute_messages WHERE dispute_id = ? ORDER BY id DESC LIMIT 1",
                (dispute_id,),
            )
        )

    def resolve_marketplace_dispute(self, dispute_id: int, *, resolution: str) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                UPDATE marketplace_disputes SET status = 'resolved', resolution = ?, resolved_at = ?, updated_at = ?
                WHERE id = ?
                """,
                (resolution, now, now, dispute_id),
            )
        return dict(self.one("SELECT * FROM marketplace_disputes WHERE id = ?", (dispute_id,)))

    # --- Subscriptions ---

    def list_marketplace_subscription_plans(self) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM marketplace_subscription_plans WHERE status = 'active'")]

    def create_marketplace_subscription(
        self,
        *,
        plan_id: int,
        provider_profile_id: int | None = None,
        user_id: int | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"sub-{uuid.uuid4().hex[:10]}"
        plan = self.one("SELECT * FROM marketplace_subscription_plans WHERE id = ?", (plan_id,))
        ends_at = (datetime.now(timezone.utc) + timedelta(days=30)).replace(microsecond=0).isoformat()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_subscriptions (
                    subscription_key, plan_id, provider_profile_id, user_id, status, started_at, ends_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'active', ?, ?, ?, ?)
                """,
                (key, plan_id, provider_profile_id, user_id, now, ends_at, now, now),
            )
        sub = dict(self.one("SELECT * FROM marketplace_subscriptions WHERE subscription_key = ?", (key,)))
        if plan:
            self.prepare_marketplace_payment(
                amount=int(plan.get("price") or 0),
                subscription_id=int(sub["id"]),
                payment_method="mobile_money",
            )
        return sub

    def list_marketplace_subscriptions(self, *, provider_id: int | None = None) -> list[dict[str, object]]:
        if provider_id is not None:
            rows = self.all(
                "SELECT * FROM marketplace_subscriptions WHERE provider_profile_id = ? ORDER BY id DESC",
                (provider_id,),
            )
        else:
            rows = self.all("SELECT * FROM marketplace_subscriptions ORDER BY id DESC")
        return [dict(r) for r in rows]

    # --- Commissions ---

    def compute_marketplace_commission(self, contract_id: int) -> dict[str, object]:
        engine = MarketplacePlatformEngine()
        contract = self.get_marketplace_contract(contract_id)
        rule = self.one("SELECT * FROM marketplace_commission_rules WHERE status = 'active' ORDER BY id ASC LIMIT 1")
        computed = engine.commission.compute(contract_amount=int(contract.get("amount") or 0), rule=dict(rule) if rule else None)
        now = _utcnow()
        key = f"comm-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_commissions (
                    commission_key, contract_id, rule_id, commission_type, amount, currency, computed_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    contract_id,
                    rule["id"] if rule else None,
                    computed["commission_type"],
                    computed["amount"],
                    computed["currency"],
                    now,
                    now,
                ),
            )
        return dict(self.one("SELECT * FROM marketplace_commissions WHERE commission_key = ?", (key,)))

    def list_marketplace_commissions(self, *, contract_id: int | None = None) -> list[dict[str, object]]:
        if contract_id is not None:
            rows = self.all("SELECT * FROM marketplace_commissions WHERE contract_id = ?", (contract_id,))
        else:
            rows = self.all("SELECT * FROM marketplace_commissions ORDER BY id DESC")
        return [dict(r) for r in rows]

    # --- Payment preparations ---

    def prepare_marketplace_payment(
        self,
        *,
        amount: int,
        payment_method: str = "mobile_money",
        contract_id: int | None = None,
        subscription_id: int | None = None,
        payer_reference: str = "",
    ) -> dict[str, object]:
        if payment_method not in PAYMENT_METHODS:
            payment_method = "mobile_money"
        now = _utcnow()
        key = f"pay-{uuid.uuid4().hex[:10]}"
        expires_at = (datetime.now(timezone.utc) + timedelta(hours=24)).replace(microsecond=0).isoformat()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_payment_preparations (
                    preparation_key, contract_id, subscription_id, payment_method, amount, status,
                    payer_reference, prepared_at, expires_at, created_at
                ) VALUES (?, ?, ?, ?, ?, 'prepared', ?, ?, ?, ?)
                """,
                (key, contract_id, subscription_id, payment_method, amount, payer_reference, now, expires_at, now),
            )
        return dict(self.one("SELECT * FROM marketplace_payment_preparations WHERE preparation_key = ?", (key,)))

    def list_marketplace_payment_preparations(self, *, contract_id: int | None = None) -> list[dict[str, object]]:
        if contract_id is not None:
            rows = self.all("SELECT * FROM marketplace_payment_preparations WHERE contract_id = ?", (contract_id,))
        else:
            rows = self.all("SELECT * FROM marketplace_payment_preparations ORDER BY id DESC LIMIT 50")
        return [dict(r) for r in rows]

    # --- Matching ---

    def run_marketplace_matching(self, request_id: int, *, limit: int = 10) -> dict[str, object]:
        engine = MarketplacePlatformEngine()
        request = self.get_marketplace_request(request_id)
        providers = self.list_marketplace_providers(status="active", limit=100)
        partner_ids = [int(p["partner_profile_id"]) for p in providers]
        partners: list[dict[str, object]] = []
        if partner_ids:
            placeholders = ",".join("?" for _ in partner_ids)
            partners = [
                dict(r)
                for r in self.all(
                    f"SELECT * FROM partner_profiles WHERE id IN ({placeholders}) AND status = 'active'",
                    tuple(partner_ids),
                )
            ]
        matches = engine.matching.match_providers(request=request, providers=providers, partners=partners, limit=limit)
        now = _utcnow()
        key = f"match-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_matching_sessions (
                    session_key, request_id, status, criteria_json, result_count, started_at, completed_at, created_at
                ) VALUES (?, ?, 'completed', ?, ?, ?, ?, ?)
                """,
                (key, request_id, request.get("criteria_json") or "{}", len(matches), now, now, now),
            )
            session = self.one("SELECT id FROM marketplace_matching_sessions WHERE session_key = ?", (key,))
            session_id = int(session["id"])
            for match in matches:
                conn.execute(
                    """
                    INSERT INTO marketplace_matching_results (
                        session_id, provider_profile_id, partner_profile_id, score, rank,
                        reasons_json, breakdown_json, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        session_id,
                        match["provider_profile_id"],
                        match["partner_profile_id"],
                        match["score"],
                        match["rank"],
                        _json(match.get("reasons") or []),
                        _json(match.get("breakdown") or {}),
                        now,
                    ),
                )
        self.update_marketplace_request(request_id, status="matching")
        recs = engine.recommendations.build_recommendations(matches=matches, request=request, sources=engine.integration_sources())
        for rec in recs:
            self.store_marketplace_ai_recommendation(
                request_id=request_id,
                provider_profile_id=rec.get("provider_profile_id"),
                recommendation_type=str(rec.get("recommendation_type") or "provider"),
                title=str(rec.get("title") or ""),
                rationale=str(rec.get("rationale") or ""),
                score=float(rec.get("score") or 0),
                sources=list(rec.get("sources") or []),
            )
        return {
            "session": dict(self.one("SELECT * FROM marketplace_matching_sessions WHERE id = ?", (session_id,))),
            "results": matches,
        }

    def get_marketplace_matching_session(self, session_id: int) -> dict[str, object]:
        session = self.one("SELECT * FROM marketplace_matching_sessions WHERE id = ?", (session_id,))
        if session is None:
            from ..errors import NotFoundError
            raise NotFoundError("matching session not found")
        results = self.all(
            "SELECT * FROM marketplace_matching_results WHERE session_id = ? ORDER BY rank ASC",
            (session_id,),
        )
        return {"session": dict(session), "results": [dict(r) for r in results]}

    # --- Portfolio ---

    def add_marketplace_portfolio_item(
        self,
        provider_id: int,
        *,
        title: str,
        description: str = "",
        category: str = "other",
        media_ref: str = "",
    ) -> dict[str, object]:
        engine = MarketplacePlatformEngine()
        category = engine.catalog.normalize_category(category)
        now = _utcnow()
        key = f"port-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_portfolio_items (
                    portfolio_key, provider_profile_id, title, description, category, media_ref, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (key, provider_id, title, description, category, media_ref, now, now),
            )
        return dict(self.one("SELECT * FROM marketplace_portfolio_items WHERE portfolio_key = ?", (key,)))

    def list_marketplace_portfolio(self, provider_id: int) -> list[dict[str, object]]:
        rows = self.all(
            "SELECT * FROM marketplace_portfolio_items WHERE provider_profile_id = ? ORDER BY id DESC",
            (provider_id,),
        )
        return [dict(r) for r in rows]

    # --- AI recommendations ---

    def store_marketplace_ai_recommendation(
        self,
        *,
        title: str,
        rationale: str = "",
        recommendation_type: str = "provider",
        request_id: int | None = None,
        provider_profile_id: int | None = None,
        user_id: int | None = None,
        score: float = 0,
        sources: list[str] | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"rec-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_ai_recommendations (
                    recommendation_key, user_id, request_id, provider_profile_id, recommendation_type,
                    title, rationale, score, sources_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    user_id,
                    request_id,
                    provider_profile_id,
                    recommendation_type,
                    title,
                    rationale,
                    score,
                    _json(sources or []),
                    now,
                ),
            )
        return dict(self.one("SELECT * FROM marketplace_ai_recommendations WHERE recommendation_key = ?", (key,)))

    def list_marketplace_ai_recommendations(self, *, request_id: int | None = None, limit: int = 20) -> list[dict[str, object]]:
        if request_id is not None:
            rows = self.all(
                "SELECT * FROM marketplace_ai_recommendations WHERE request_id = ? ORDER BY score DESC LIMIT ?",
                (request_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM marketplace_ai_recommendations ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    # --- Analytics ---

    def snapshot_marketplace_analytics(self) -> dict[str, object]:
        metrics = {
            "providers": self.scalar("SELECT COUNT(*) FROM marketplace_provider_profiles"),
            "requests": self.scalar("SELECT COUNT(*) FROM marketplace_service_requests"),
            "quotes": self.scalar("SELECT COUNT(*) FROM marketplace_quotes"),
            "contracts": self.scalar("SELECT COUNT(*) FROM marketplace_contracts"),
            "missions": self.scalar("SELECT COUNT(*) FROM marketplace_missions"),
            "reviews": self.scalar("SELECT COUNT(*) FROM marketplace_reviews"),
            "disputes": self.scalar("SELECT COUNT(*) FROM marketplace_disputes WHERE status = 'open'"),
        }
        now = _utcnow()
        key = f"snap-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO marketplace_analytics_snapshots (snapshot_key, scope, metrics_json, created_at)
                VALUES (?, 'global', ?, ?)
                """,
                (key, _json(metrics), now),
            )
        return metrics

    def marketplace_analytics(self) -> dict[str, object]:
        latest = self.one("SELECT * FROM marketplace_analytics_snapshots ORDER BY id DESC LIMIT 1")
        if latest is None:
            metrics = self.snapshot_marketplace_analytics()
            return {"metrics": metrics, "snapshot": None}
        return {"metrics": _parse_json(str(latest.get("metrics_json"))) or {}, "snapshot": dict(latest)}

    def marketplace_dashboard(self) -> dict[str, object]:
        analytics = self.marketplace_analytics()
        recent_requests = self.list_marketplace_requests(limit=5)
        top_providers = self.list_marketplace_providers(status="active", limit=5)
        return {
            "summary": analytics.get("metrics") or {},
            "recent_requests": recent_requests,
            "top_providers": top_providers,
            "integrations": self.marketplace_integrations(),
        }

    def marketplace_stats(self) -> dict[str, object]:
        return {
            "active_providers": self.scalar("SELECT COUNT(*) FROM marketplace_provider_profiles WHERE status = 'active'"),
            "open_requests": self.scalar(
                "SELECT COUNT(*) FROM marketplace_service_requests WHERE status NOT IN ('completed', 'cancelled')"
            ),
            "active_contracts": self.scalar("SELECT COUNT(*) FROM marketplace_contracts WHERE status = 'active'"),
            "pending_reviews": self.scalar("SELECT COUNT(*) FROM marketplace_reviews WHERE status = 'pending'"),
        }
