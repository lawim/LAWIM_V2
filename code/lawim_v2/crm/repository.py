from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from ..contact import TELEGRAM_BOT, to_public_dict
from .constants import CONSENT_TYPES, CONTACT_TYPES, CUSTOMER_ROLES, LEAD_STATUSES
from .engines import CrmPlatformEngine


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


class CrmRepositoryMixin:
    def crm_tables_present(self) -> bool:
        row = self.one("SELECT name FROM sqlite_master WHERE type='table' AND name='crm_contact_profiles'")
        return row is not None

    def seed_crm_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM crm_contact_profiles") > 0:
            if hasattr(self, "seed_source_intelligence_catalog"):
                self.seed_source_intelligence_catalog()
            return
        now = _utcnow()
        engine = CrmPlatformEngine()
        if hasattr(self, "seed_source_intelligence_catalog"):
            self.seed_source_intelligence_catalog()
        with self._transaction() as conn:
            pipeline_key = "pipeline-default"
            conn.execute(
                """
                INSERT OR IGNORE INTO crm_pipelines (pipeline_key, name, is_default, created_at, updated_at)
                VALUES (?, 'Pipeline commercial LAWIM', 1, ?, ?)
                """,
                (pipeline_key, now, now),
            )
            pipeline = self.one("SELECT id FROM crm_pipelines WHERE pipeline_key = ?", (pipeline_key,))
            pipeline_id = int(pipeline["id"]) if pipeline else 1
            for stage in engine.pipeline.default_stages():
                conn.execute(
                    """
                    INSERT OR IGNORE INTO crm_pipeline_stages (pipeline_id, stage_key, label, position, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (pipeline_id, stage["stage_key"], stage["label"], stage["position"], now),
                )
            conn.execute(
                """
                INSERT OR IGNORE INTO crm_satisfaction_surveys (
                    survey_key, title, survey_type, questions_json, status, created_at, updated_at
                ) VALUES ('survey-csat-default', 'Satisfaction post-contact LAWIM', 'csat', '[]', 'active', ?, ?)
                """,
                (now, now),
            )
        self._seed_crm_demo_data()
        self.record_event("crm_catalog_seeded", {"pipeline_key": "pipeline-default"})

    def _seed_crm_demo_data(self) -> None:
        now = _utcnow()
        engine = CrmPlatformEngine()
        sender = to_public_dict()
        demo_contacts = [
            {
                "contact_key": "contact-demo-buyer",
                "full_name": "Marie Nguema",
                "email": "marie.nguema@example.cm",
                "phone": "+237 677 000 111",
                "whatsapp": "+237677000111",
                "contact_type": "prospect",
                "company": "",
            },
            {
                "contact_key": "contact-demo-investor",
                "full_name": "Jean-Paul Mbarga",
                "email": "jp.mbarga@invest.cm",
                "phone": "+237 699 000 222",
                "whatsapp": "+237699000222",
                "contact_type": "lead",
                "company": "Mbarga Invest",
            },
            {
                "contact_key": "contact-demo-tenant",
                "full_name": "Sophie Ekani",
                "email": "sophie.ekani@example.cm",
                "phone": "+237 655 000 333",
                "telegram": "@sophie_ekani",
                "contact_type": "customer",
                "company": "",
            },
        ]
        source_id = None
        if hasattr(self, "resolve_source_intelligence_source"):
            try:
                source = self.resolve_source_intelligence_source(source_key="source-web")
                source_id = int(source["id"])
            except Exception:
                source_id = None
        if source_id is None:
            source = self.one("SELECT id FROM crm_lead_sources WHERE source_key = 'source-web'")
            source_id = int(source["id"]) if source else None
        pipeline = self.one("SELECT id FROM crm_pipelines WHERE is_default = 1 ORDER BY id ASC LIMIT 1")
        pipeline_id = int(pipeline["id"]) if pipeline else 1
        first_stage = self.one(
            "SELECT id FROM crm_pipeline_stages WHERE pipeline_id = ? ORDER BY position ASC LIMIT 1",
            (pipeline_id,),
        )
        stage_id = int(first_stage["id"]) if first_stage else 1
        for demo in demo_contacts:
            contact = self.create_crm_contact(
                full_name=demo["full_name"],
                contact_type=demo["contact_type"],
                email=demo.get("email", ""),
                phone=demo.get("phone", ""),
                whatsapp=demo.get("whatsapp", ""),
                telegram=demo.get("telegram", ""),
                company=demo.get("company", ""),
                contact_key=demo["contact_key"],
            )
            contact_id = int(contact["id"])
            for consent_type in ("marketing", "whatsapp", "email"):
                self.grant_crm_consent(contact_id, consent_type=consent_type)
            lead = self.create_crm_lead(
                contact_id=contact_id,
                title=f"Intérêt immobilier — {demo['full_name']}",
                source_id=source_id,
                status="new" if demo["contact_type"] != "customer" else "qualified",
            )
            lead_id = int(lead["id"])
            self.add_crm_pipeline_item(
                pipeline_id=pipeline_id,
                stage_id=stage_id,
                entity_type="lead",
                entity_id=lead_id,
            )
            if demo["contact_type"] == "customer":
                self.convert_crm_lead_to_customer(lead_id, roles=["tenant"])
            wa_payload = engine.communication.whatsapp_payload(
                to_number=demo.get("whatsapp") or demo.get("phone", ""),
                body="Bonjour, merci pour votre intérêt pour LAWIM. Un conseiller vous contactera sous peu.",
            )
            self.send_crm_whatsapp(contact_id=contact_id, body=wa_payload["body"], to_number=str(wa_payload["to_number"]))
            if demo.get("email"):
                email_payload = engine.communication.email_payload(
                    to_email=demo["email"],
                    subject="Bienvenue chez LAWIM",
                    body="Merci de nous avoir contactés via notre plateforme immobilière.",
                )
                self.send_crm_email(
                    contact_id=contact_id,
                    to_email=str(email_payload["to_email"]),
                    subject=str(email_payload["subject"]),
                    body=str(email_payload["body"]),
                )
        self.snapshot_crm_analytics()

    # --- Contacts ---

    def create_crm_contact(
        self,
        *,
        full_name: str,
        contact_type: str = "individual",
        email: str = "",
        phone: str = "",
        whatsapp: str = "",
        telegram: str = "",
        company: str = "",
        country: str = "Cameroon",
        user_id: int | None = None,
        contact_key: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        if contact_type not in CONTACT_TYPES:
            contact_type = "individual"
        now = _utcnow()
        key = contact_key or f"contact-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_contact_profiles (
                    contact_key, contact_type, full_name, email, phone, whatsapp, telegram,
                    company, country, user_id, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    contact_type,
                    full_name,
                    email,
                    phone,
                    whatsapp,
                    telegram,
                    company,
                    country,
                    user_id,
                    _json(metadata or {}),
                    now,
                    now,
                ),
            )
        row = dict(self.one("SELECT * FROM crm_contact_profiles WHERE contact_key = ?", (key,)))
        self._record_crm_journey(int(row["id"]), event_type="contact_created", summary=f"Contact {full_name} créé")
        self._append_crm_timeline(int(row["id"]), entry_type="contact", summary=f"Contact créé: {full_name}", reference_type="contact", reference_id=int(row["id"]))
        return row

    def get_crm_contact(self, contact_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM crm_contact_profiles WHERE id = ?", (contact_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("contact not found")
        return dict(row)

    def list_crm_contacts(self, *, contact_type: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if contact_type:
            rows = self.all(
                "SELECT * FROM crm_contact_profiles WHERE contact_type = ? ORDER BY id DESC LIMIT ?",
                (contact_type, limit),
            )
        else:
            rows = self.all("SELECT * FROM crm_contact_profiles ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def update_crm_contact(self, contact_id: int, **fields: object) -> dict[str, object]:
        allowed = {"full_name", "email", "phone", "whatsapp", "telegram", "company", "country", "contact_type", "metadata_json"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if "metadata" in fields and fields["metadata"] is not None:
            updates["metadata_json"] = _json(fields["metadata"])
        if not updates:
            return self.get_crm_contact(contact_id)
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE crm_contact_profiles SET {cols} WHERE id = ?", (*updates.values(), contact_id))
        return self.get_crm_contact(contact_id)

    def delete_crm_contact(self, contact_id: int) -> None:
        with self._transaction() as conn:
            conn.execute("DELETE FROM crm_contact_profiles WHERE id = ?", (contact_id,))

    def add_crm_contact_tag(self, contact_id: int, tag: str) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO crm_contact_tags (contact_id, tag, created_at) VALUES (?, ?, ?)",
                (contact_id, tag, now),
            )
        row = self.one("SELECT * FROM crm_contact_tags WHERE contact_id = ? AND tag = ?", (contact_id, tag))
        return dict(row) if row else {}

    def list_crm_contact_tags(self, contact_id: int) -> list[str]:
        rows = self.all("SELECT tag FROM crm_contact_tags WHERE contact_id = ?", (contact_id,))
        return [str(r["tag"]) for r in rows]

    def grant_crm_consent(self, contact_id: int, *, consent_type: str = "marketing") -> dict[str, object]:
        if consent_type not in CONSENT_TYPES:
            consent_type = "marketing"
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO crm_contact_consents (contact_id, consent_type, granted, granted_at, created_at)
                VALUES (?, ?, 1, ?, ?)
                """,
                (contact_id, consent_type, now, now),
            )
        row = self.one("SELECT * FROM crm_contact_consents WHERE contact_id = ? AND consent_type = ?", (contact_id, consent_type))
        return dict(row) if row else {}

    def revoke_crm_consent(self, contact_id: int, *, consent_type: str) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                UPDATE crm_contact_consents SET granted = 0, revoked_at = ? WHERE contact_id = ? AND consent_type = ?
                """,
                (now, contact_id, consent_type),
            )
        row = self.one("SELECT * FROM crm_contact_consents WHERE contact_id = ? AND consent_type = ?", (contact_id, consent_type))
        return dict(row) if row else {}

    # --- Leads ---

    def create_crm_lead(
        self,
        *,
        contact_id: int,
        title: str = "",
        status: str = "new",
        source_id: int | None = None,
        assigned_user_id: int | None = None,
        notes: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        if status not in LEAD_STATUSES:
            status = "new"
        contact = self.get_crm_contact(contact_id)
        now = _utcnow()
        lead_key = f"lead-{uuid.uuid4().hex[:10]}"
        comm_count = self.scalar("SELECT COUNT(*) FROM crm_communications WHERE contact_id = ?", (contact_id,))
        engine = CrmPlatformEngine()
        scoring = engine.lead_scoring.compute(lead={"status": status}, contact=contact, communications=comm_count)
        score = scoring["lead_score"]
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_leads (
                    lead_key, contact_id, source_id, status, score, title, notes,
                    assigned_user_id, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (lead_key, contact_id, source_id, status, score, title, notes, assigned_user_id, _json(metadata or {}), now, now),
            )
        row = dict(
            self.one(
                """
                SELECT l.*, s.source_key AS source_key, s.reference_code AS source_reference_code,
                       s.name AS source_name, s.channel AS source_channel, s.target AS source_target,
                       s.status AS source_status
                FROM crm_leads l
                LEFT JOIN crm_lead_sources s ON s.id = l.source_id
                WHERE l.lead_key = ?
                """,
                (lead_key,),
            )
        )
        self._record_crm_journey(contact_id, event_type="lead_created", summary=f"Lead créé: {title or lead_key}")
        self._append_crm_timeline(contact_id, entry_type="lead", summary=f"Nouveau lead: {title}", reference_type="lead", reference_id=int(row["id"]))
        if hasattr(self, "start_automation_instance"):
            try:
                self.start_automation_instance(workflow_key="wf-crm-lead", context={"lead_id": int(row["id"]), "contact_id": contact_id})
            except Exception:
                pass
        return row

    def get_crm_lead(self, lead_id: int) -> dict[str, object]:
        row = self.one(
            """
            SELECT l.*, s.source_key AS source_key, s.reference_code AS source_reference_code,
                   s.name AS source_name, s.channel AS source_channel, s.target AS source_target,
                   s.status AS source_status
            FROM crm_leads l
            LEFT JOIN crm_lead_sources s ON s.id = l.source_id
            WHERE l.id = ?
            """,
            (lead_id,),
        )
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("lead not found")
        return dict(row)

    def list_crm_leads(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                """
                SELECT l.*, s.source_key AS source_key, s.reference_code AS source_reference_code,
                       s.name AS source_name, s.channel AS source_channel, s.target AS source_target,
                       s.status AS source_status
                FROM crm_leads l
                LEFT JOIN crm_lead_sources s ON s.id = l.source_id
                WHERE l.status = ?
                ORDER BY l.score DESC, l.id DESC
                LIMIT ?
                """,
                (status, limit),
            )
        else:
            rows = self.all(
                """
                SELECT l.*, s.source_key AS source_key, s.reference_code AS source_reference_code,
                       s.name AS source_name, s.channel AS source_channel, s.target AS source_target,
                       s.status AS source_status
                FROM crm_leads l
                LEFT JOIN crm_lead_sources s ON s.id = l.source_id
                ORDER BY l.id DESC
                LIMIT ?
                """,
                (limit,),
            )
        return [dict(r) for r in rows]

    def update_crm_lead(self, lead_id: int, **fields: object) -> dict[str, object]:
        lead = self.get_crm_lead(lead_id)
        allowed = {"status", "title", "notes", "assigned_user_id", "source_id", "score"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if "metadata" in fields and fields["metadata"] is not None:
            updates["metadata_json"] = _json(fields["metadata"])
        if not updates:
            return lead
        updates["updated_at"] = _utcnow()
        if "status" in updates and updates["status"] not in LEAD_STATUSES:
            updates["status"] = lead["status"]
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE crm_leads SET {cols} WHERE id = ?", (*updates.values(), lead_id))
        updated = self.get_crm_lead(lead_id)
        contact_id = int(updated["contact_id"])
        if "status" in updates:
            self._record_crm_journey(contact_id, event_type="lead_status_changed", summary=f"Lead → {updates['status']}")
        return updated

    def delete_crm_lead(self, lead_id: int) -> None:
        with self._transaction() as conn:
            conn.execute("DELETE FROM crm_leads WHERE id = ?", (lead_id,))

    def convert_crm_lead_to_customer(self, lead_id: int, *, roles: list[str] | None = None) -> dict[str, object]:
        lead = self.get_crm_lead(lead_id)
        contact_id = int(lead["contact_id"])
        existing = self.one("SELECT * FROM crm_customers WHERE contact_id = ?", (contact_id,))
        if existing:
            customer = dict(existing)
        else:
            now = _utcnow()
            customer_key = f"customer-{uuid.uuid4().hex[:10]}"
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO crm_customers (customer_key, contact_id, status, created_at, updated_at)
                    VALUES (?, ?, 'active', ?, ?)
                    """,
                    (customer_key, contact_id, now, now),
                )
            customer = dict(self.one("SELECT * FROM crm_customers WHERE customer_key = ?", (customer_key,)))
        customer_id = int(customer["id"])
        for role in roles or ["buyer"]:
            if role in CUSTOMER_ROLES:
                self.add_crm_customer_role(customer_id, role=role)
        self.update_crm_contact(contact_id, contact_type="customer")
        self.update_crm_lead(lead_id, status="won")
        with self._transaction() as conn:
            conn.execute("UPDATE crm_leads SET converted_customer_id = ? WHERE id = ?", (customer_id, lead_id))
        self._record_crm_journey(contact_id, event_type="lead_converted", summary="Lead converti en client")
        return customer

    def list_crm_lead_sources(self) -> list[dict[str, object]]:
        if hasattr(self, "list_source_intelligence_sources"):
            return self.list_source_intelligence_sources(limit=1000)
        return [dict(r) for r in self.all("SELECT * FROM crm_lead_sources ORDER BY id ASC")]

    # --- Customers ---

    def create_crm_customer(self, *, contact_id: int, roles: list[str] | None = None) -> dict[str, object]:
        existing = self.one("SELECT * FROM crm_customers WHERE contact_id = ?", (contact_id,))
        if existing:
            return dict(existing)
        now = _utcnow()
        customer_key = f"customer-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_customers (customer_key, contact_id, status, created_at, updated_at)
                VALUES (?, ?, 'active', ?, ?)
                """,
                (customer_key, contact_id, now, now),
            )
        customer = dict(self.one("SELECT * FROM crm_customers WHERE customer_key = ?", (customer_key,)))
        for role in roles or ["buyer"]:
            if role in CUSTOMER_ROLES:
                self.add_crm_customer_role(int(customer["id"]), role=role)
        self.update_crm_contact(contact_id, contact_type="customer")
        return customer

    def get_crm_customer(self, customer_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM crm_customers WHERE id = ?", (customer_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("customer not found")
        return dict(row)

    def list_crm_customers(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all("SELECT * FROM crm_customers WHERE status = ? ORDER BY id DESC LIMIT ?", (status, limit))
        else:
            rows = self.all("SELECT * FROM crm_customers ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def update_crm_customer(self, customer_id: int, **fields: object) -> dict[str, object]:
        allowed = {"status", "lifetime_value"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if "metadata" in fields and fields["metadata"] is not None:
            updates["metadata_json"] = _json(fields["metadata"])
        if not updates:
            return self.get_crm_customer(customer_id)
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE crm_customers SET {cols} WHERE id = ?", (*updates.values(), customer_id))
        return self.get_crm_customer(customer_id)

    def add_crm_customer_role(self, customer_id: int, *, role: str = "buyer") -> dict[str, object]:
        if role not in CUSTOMER_ROLES:
            role = "buyer"
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO crm_customer_roles (customer_id, role, assigned_at, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (customer_id, role, now, now),
            )
        row = self.one("SELECT * FROM crm_customer_roles WHERE customer_id = ? AND role = ?", (customer_id, role))
        return dict(row) if row else {}

    def list_crm_customer_roles(self, customer_id: int) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM crm_customer_roles WHERE customer_id = ?", (customer_id,))]

    # --- Opportunities ---

    def create_crm_opportunity(
        self,
        *,
        contact_id: int,
        title: str,
        customer_id: int | None = None,
        amount: int | None = None,
        currency: str = "XAF",
        status: str = "open",
        probability: int = 50,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        opportunity_key = f"opp-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_opportunities (
                    opportunity_key, customer_id, contact_id, title, status, amount, currency,
                    probability, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (opportunity_key, customer_id, contact_id, title, status, amount, currency, probability, _json(metadata or {}), now, now),
            )
        row = dict(self.one("SELECT * FROM crm_opportunities WHERE opportunity_key = ?", (opportunity_key,)))
        self._record_crm_journey(contact_id, event_type="opportunity_created", summary=f"Opportunité: {title}")
        self._append_crm_timeline(contact_id, entry_type="opportunity", summary=title, reference_type="opportunity", reference_id=int(row["id"]))
        return row

    def get_crm_opportunity(self, opportunity_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM crm_opportunities WHERE id = ?", (opportunity_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("opportunity not found")
        return dict(row)

    def list_crm_opportunities(self, *, contact_id: int | None = None, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        query = "SELECT * FROM crm_opportunities WHERE 1=1"
        params: list[object] = []
        if contact_id is not None:
            query += " AND contact_id = ?"
            params.append(contact_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(r) for r in self.all(query, tuple(params))]

    def update_crm_opportunity(self, opportunity_id: int, **fields: object) -> dict[str, object]:
        allowed = {"title", "status", "amount", "currency", "probability", "customer_id", "pipeline_item_id"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if "metadata" in fields and fields["metadata"] is not None:
            updates["metadata_json"] = _json(fields["metadata"])
        if not updates:
            return self.get_crm_opportunity(opportunity_id)
        updates["updated_at"] = _utcnow()
        if updates.get("status") in {"won", "lost", "closed"}:
            updates["closed_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE crm_opportunities SET {cols} WHERE id = ?", (*updates.values(), opportunity_id))
        return self.get_crm_opportunity(opportunity_id)

    def delete_crm_opportunity(self, opportunity_id: int) -> None:
        with self._transaction() as conn:
            conn.execute("DELETE FROM crm_opportunities WHERE id = ?", (opportunity_id,))

    # --- Pipelines ---

    def create_crm_pipeline(self, *, name: str, is_default: bool = False) -> dict[str, object]:
        now = _utcnow()
        pipeline_key = f"pipeline-{uuid.uuid4().hex[:8]}"
        engine = CrmPlatformEngine()
        with self._transaction() as conn:
            if is_default:
                conn.execute("UPDATE crm_pipelines SET is_default = 0")
            conn.execute(
                """
                INSERT INTO crm_pipelines (pipeline_key, name, is_default, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (pipeline_key, name, 1 if is_default else 0, now, now),
            )
            pipeline = self.one("SELECT id FROM crm_pipelines WHERE pipeline_key = ?", (pipeline_key,))
            pipeline_id = int(pipeline["id"])
            for stage in engine.pipeline.default_stages():
                conn.execute(
                    """
                    INSERT INTO crm_pipeline_stages (pipeline_id, stage_key, label, position, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (pipeline_id, stage["stage_key"], stage["label"], stage["position"], now),
                )
        return dict(self.one("SELECT * FROM crm_pipelines WHERE pipeline_key = ?", (pipeline_key,)))

    def get_crm_pipeline(self, pipeline_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM crm_pipelines WHERE id = ?", (pipeline_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("pipeline not found")
        return dict(row)

    def list_crm_pipelines(self) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM crm_pipelines ORDER BY is_default DESC, id ASC")]

    def list_crm_pipeline_stages(self, pipeline_id: int) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM crm_pipeline_stages WHERE pipeline_id = ? ORDER BY position ASC", (pipeline_id,))
        return [dict(r) for r in rows]

    def add_crm_pipeline_item(
        self,
        *,
        pipeline_id: int,
        stage_id: int,
        entity_type: str = "lead",
        entity_id: int,
        position: int = 0,
    ) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_pipeline_items (
                    pipeline_id, stage_id, entity_type, entity_id, position, entered_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (pipeline_id, stage_id, entity_type, entity_id, position, now, now, now),
            )
        row = dict(
            self.one(
                "SELECT * FROM crm_pipeline_items WHERE pipeline_id = ? AND entity_type = ? AND entity_id = ? ORDER BY id DESC LIMIT 1",
                (pipeline_id, entity_type, entity_id),
            )
        )
        return row

    def move_crm_pipeline_item(self, item_id: int, *, stage_id: int, position: int = 0) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                UPDATE crm_pipeline_items SET stage_id = ?, position = ?, entered_at = ?, updated_at = ?
                WHERE id = ?
                """,
                (stage_id, position, now, now, item_id),
            )
        return dict(self.one("SELECT * FROM crm_pipeline_items WHERE id = ?", (item_id,)))

    def get_crm_pipeline_board(self, pipeline_id: int) -> list[dict[str, object]]:
        engine = CrmPlatformEngine()
        stages = self.list_crm_pipeline_stages(pipeline_id)
        items = [dict(r) for r in self.all("SELECT * FROM crm_pipeline_items WHERE pipeline_id = ? ORDER BY position ASC", (pipeline_id,))]
        return engine.pipeline.kanban_payload(stages=stages, items=items)

    def advance_crm_pipeline_item(self, item_id: int) -> dict[str, object]:
        item = dict(self.one("SELECT * FROM crm_pipeline_items WHERE id = ?", (item_id,)))
        if not item:
            from ..errors import NotFoundError
            raise NotFoundError("pipeline item not found")
        stage = dict(self.one("SELECT * FROM crm_pipeline_stages WHERE id = ?", (item["stage_id"],)))
        engine = CrmPlatformEngine()
        next_key = engine.pipeline.advance_stage(str(stage["stage_key"]))
        if not next_key:
            return item
        next_stage = self.one(
            "SELECT id FROM crm_pipeline_stages WHERE pipeline_id = ? AND stage_key = ?",
            (item["pipeline_id"], next_key),
        )
        if next_stage is None:
            return item
        return self.move_crm_pipeline_item(item_id, stage_id=int(next_stage["id"]))

    # --- Communications ---

    def _create_crm_communication(
        self,
        *,
        contact_id: int,
        channel: str,
        body: str,
        subject: str = "",
        direction: str = "outbound",
        sender_json: dict[str, object] | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        comm_key = f"comm-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_communications (
                    communication_key, contact_id, channel, direction, status, subject, body,
                    sender_json, sent_at, created_at
                ) VALUES (?, ?, ?, ?, 'sent', ?, ?, ?, ?, ?)
                """,
                (comm_key, contact_id, channel, direction, subject, body, _json(sender_json or to_public_dict()), now, now),
            )
        comm = dict(self.one("SELECT * FROM crm_communications WHERE communication_key = ?", (comm_key,)))
        self._append_crm_timeline(
            contact_id,
            entry_type="communication",
            summary=f"{channel}: {subject or body[:60]}",
            reference_type="communication",
            reference_id=int(comm["id"]),
        )
        return comm

    def send_crm_whatsapp(self, *, contact_id: int, body: str, to_number: str | None = None) -> dict[str, object]:
        contact = self.get_crm_contact(contact_id)
        engine = CrmPlatformEngine()
        payload = engine.communication.whatsapp_payload(
            to_number=to_number or str(contact.get("whatsapp") or contact.get("phone") or ""),
            body=body,
        )
        comm = self._create_crm_communication(
            contact_id=contact_id,
            channel="whatsapp",
            body=str(payload["body"]),
            sender_json=dict(payload["lawim_sender_json"]),
        )
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_whatsapp_messages (
                    communication_id, contact_id, from_number, to_number, body, status,
                    lawim_sender_json, sent_at, created_at
                ) VALUES (?, ?, ?, ?, ?, 'sent', ?, ?, ?)
                """,
                (
                    comm["id"],
                    contact_id,
                    payload["from_number"],
                    payload["to_number"],
                    payload["body"],
                    _json(payload["lawim_sender_json"]),
                    now,
                    now,
                ),
            )
        row = dict(self.one("SELECT * FROM crm_whatsapp_messages WHERE communication_id = ?", (comm["id"],)))
        self._record_crm_journey(contact_id, event_type="whatsapp_sent", summary="Message WhatsApp envoyé")
        return row

    def send_crm_telegram(self, *, contact_id: int, body: str, to_handle: str | None = None) -> dict[str, object]:
        contact = self.get_crm_contact(contact_id)
        engine = CrmPlatformEngine()
        payload = engine.communication.telegram_payload(
            to_handle=to_handle or str(contact.get("telegram") or TELEGRAM_BOT),
            body=body,
        )
        comm = self._create_crm_communication(
            contact_id=contact_id,
            channel="telegram",
            body=str(payload["body"]),
            sender_json=dict(payload["lawim_sender_json"]),
        )
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_telegram_messages (
                    communication_id, contact_id, from_handle, to_handle, body, status,
                    lawim_sender_json, sent_at, created_at
                ) VALUES (?, ?, ?, ?, ?, 'sent', ?, ?, ?)
                """,
                (
                    comm["id"],
                    contact_id,
                    payload["from_handle"],
                    payload["to_handle"],
                    payload["body"],
                    _json(payload["lawim_sender_json"]),
                    now,
                    now,
                ),
            )
        row = dict(self.one("SELECT * FROM crm_telegram_messages WHERE communication_id = ?", (comm["id"],)))
        self._record_crm_journey(contact_id, event_type="telegram_sent", summary="Message Telegram envoyé")
        return row

    def send_crm_email(self, *, contact_id: int, subject: str, body: str, to_email: str | None = None) -> dict[str, object]:
        contact = self.get_crm_contact(contact_id)
        engine = CrmPlatformEngine()
        payload = engine.communication.email_payload(
            to_email=to_email or str(contact.get("email") or ""),
            subject=subject,
            body=body,
        )
        comm = self._create_crm_communication(
            contact_id=contact_id,
            channel="email",
            body=str(payload["body"]),
            subject=subject,
            sender_json=dict(payload["lawim_sender_json"]),
        )
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_email_messages (
                    communication_id, contact_id, from_email, to_email, subject, body, status,
                    lawim_sender_json, sent_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'sent', ?, ?, ?)
                """,
                (
                    comm["id"],
                    contact_id,
                    payload["from_email"],
                    payload["to_email"],
                    payload["subject"],
                    payload["body"],
                    _json(payload["lawim_sender_json"]),
                    now,
                    now,
                ),
            )
        row = dict(self.one("SELECT * FROM crm_email_messages WHERE communication_id = ?", (comm["id"],)))
        self._record_crm_journey(contact_id, event_type="email_sent", summary=f"Email: {subject}")
        return row

    def send_crm_sms(self, *, contact_id: int, body: str, to_number: str | None = None) -> dict[str, object]:
        contact = self.get_crm_contact(contact_id)
        engine = CrmPlatformEngine()
        payload = engine.communication.sms_payload(
            to_number=to_number or str(contact.get("phone") or ""),
            body=body,
        )
        comm = self._create_crm_communication(
            contact_id=contact_id,
            channel="sms",
            body=str(payload["body"]),
            sender_json=dict(payload["lawim_sender_json"]),
        )
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_sms_messages (
                    communication_id, contact_id, from_number, to_number, body, status,
                    lawim_sender_json, sent_at, created_at
                ) VALUES (?, ?, ?, ?, ?, 'sent', ?, ?, ?)
                """,
                (
                    comm["id"],
                    contact_id,
                    payload["from_number"],
                    payload["to_number"],
                    payload["body"],
                    _json(payload["lawim_sender_json"]),
                    now,
                    now,
                ),
            )
        row = dict(self.one("SELECT * FROM crm_sms_messages WHERE communication_id = ?", (comm["id"],)))
        self._record_crm_journey(contact_id, event_type="sms_sent", summary="SMS envoyé")
        return row

    def list_crm_communications(self, *, contact_id: int | None = None, channel: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        query = "SELECT * FROM crm_communications WHERE 1=1"
        params: list[object] = []
        if contact_id is not None:
            query += " AND contact_id = ?"
            params.append(contact_id)
        if channel:
            query += " AND channel = ?"
            params.append(channel)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(r) for r in self.all(query, tuple(params))]

    # --- Reminders & Followups ---

    def create_crm_reminder(
        self,
        *,
        contact_id: int,
        title: str,
        due_at: str,
        assigned_user_id: int | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        reminder_key = f"reminder-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_reminders (reminder_key, contact_id, assigned_user_id, title, due_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (reminder_key, contact_id, assigned_user_id, title, due_at, now),
            )
        return dict(self.one("SELECT * FROM crm_reminders WHERE reminder_key = ?", (reminder_key,)))

    def complete_crm_reminder(self, reminder_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE crm_reminders SET status = 'completed', completed_at = ? WHERE id = ?",
                (now, reminder_id),
            )
        return dict(self.one("SELECT * FROM crm_reminders WHERE id = ?", (reminder_id,)))

    def list_crm_reminders(self, *, contact_id: int | None = None, status: str = "pending") -> list[dict[str, object]]:
        if contact_id is not None:
            rows = self.all(
                "SELECT * FROM crm_reminders WHERE contact_id = ? AND status = ? ORDER BY due_at ASC",
                (contact_id, status),
            )
        else:
            rows = self.all("SELECT * FROM crm_reminders WHERE status = ? ORDER BY due_at ASC LIMIT 100", (status,))
        return [dict(r) for r in rows]

    def schedule_crm_followup(
        self,
        *,
        contact_id: int,
        scheduled_at: str,
        channel: str = "whatsapp",
        lead_id: int | None = None,
        opportunity_id: int | None = None,
        notes: str = "",
    ) -> dict[str, object]:
        now = _utcnow()
        followup_key = f"followup-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_followups (
                    followup_key, contact_id, lead_id, opportunity_id, channel, scheduled_at, notes, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (followup_key, contact_id, lead_id, opportunity_id, channel, scheduled_at, notes, now),
            )
        row = dict(self.one("SELECT * FROM crm_followups WHERE followup_key = ?", (followup_key,)))
        if hasattr(self, "start_automation_instance"):
            try:
                self.start_automation_instance(
                    workflow_key="wf-crm-followup",
                    context={"followup_id": int(row["id"]), "contact_id": contact_id, "channel": channel},
                )
            except Exception:
                pass
        return row

    def complete_crm_followup(self, followup_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE crm_followups SET status = 'completed', completed_at = ? WHERE id = ?",
                (now, followup_id),
            )
        return dict(self.one("SELECT * FROM crm_followups WHERE id = ?", (followup_id,)))

    def list_crm_followups(self, *, contact_id: int | None = None, status: str | None = None) -> list[dict[str, object]]:
        query = "SELECT * FROM crm_followups WHERE 1=1"
        params: list[object] = []
        if contact_id is not None:
            query += " AND contact_id = ?"
            params.append(contact_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY scheduled_at ASC LIMIT 100"
        return [dict(r) for r in self.all(query, tuple(params))]

    # --- Campaigns & Segments ---

    def create_crm_campaign(
        self,
        *,
        name: str,
        channel: str = "email",
        audience: dict[str, Any] | None = None,
        content: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        campaign_key = f"campaign-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_campaigns (campaign_key, name, channel, audience_json, content_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (campaign_key, name, channel, _json(audience or {}), _json(content or {}), now, now),
            )
        return dict(self.one("SELECT * FROM crm_campaigns WHERE campaign_key = ?", (campaign_key,)))

    def launch_crm_campaign(self, campaign_id: int) -> dict[str, object]:
        campaign = dict(self.one("SELECT * FROM crm_campaigns WHERE id = ?", (campaign_id,)))
        if not campaign:
            from ..errors import NotFoundError
            raise NotFoundError("campaign not found")
        engine = CrmPlatformEngine()
        audience = _parse_json(str(campaign.get("audience_json"))) or {}
        content = _parse_json(str(campaign.get("content_json"))) or {}
        contacts = self._resolve_crm_campaign_audience(audience)
        now = _utcnow()
        template = str(content.get("body") or "Bonjour {{name}}, découvrez LAWIM.")
        sent = 0
        with self._transaction() as conn:
            conn.execute(
                "UPDATE crm_campaigns SET status = 'running', started_at = ?, updated_at = ? WHERE id = ?",
                (now, now, campaign_id),
            )
            for contact in contacts:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO crm_campaign_targets (campaign_id, contact_id, status, created_at)
                    VALUES (?, ?, 'pending', ?)
                    """,
                    (campaign_id, contact["id"], now),
                )
                personalized = engine.campaign.personalize_content(template=template, contact=contact)
                channel = str(campaign.get("channel") or "email")
                if channel == "whatsapp" and (contact.get("whatsapp") or contact.get("phone")):
                    self.send_crm_whatsapp(contact_id=int(contact["id"]), body=personalized)
                elif channel == "email" and contact.get("email"):
                    self.send_crm_email(contact_id=int(contact["id"]), subject=str(content.get("subject") or campaign["name"]), body=personalized)
                elif channel == "telegram":
                    self.send_crm_telegram(contact_id=int(contact["id"]), body=personalized)
                elif channel == "sms":
                    self.send_crm_sms(contact_id=int(contact["id"]), body=personalized)
                conn.execute(
                    """
                    UPDATE crm_campaign_targets SET status = 'sent', sent_at = ? WHERE campaign_id = ? AND contact_id = ?
                    """,
                    (now, campaign_id, contact["id"]),
                )
                sent += 1
            conn.execute(
                "UPDATE crm_campaigns SET status = 'completed', completed_at = ?, updated_at = ? WHERE id = ?",
                (now, now, campaign_id),
            )
        return {"campaign_id": campaign_id, "targets_sent": sent}

    def _resolve_crm_campaign_audience(self, audience: dict[str, Any]) -> list[dict[str, object]]:
        segment_key = audience.get("segment_key")
        if segment_key:
            segment = self.one("SELECT id FROM crm_segments WHERE segment_key = ?", (segment_key,))
            if segment:
                rows = self.all(
                    """
                    SELECT c.* FROM crm_segment_members sm
                    JOIN crm_contact_profiles c ON c.id = sm.contact_id
                    WHERE sm.segment_id = ?
                    """,
                    (segment["id"],),
                )
                return [dict(r) for r in rows]
        contact_type = audience.get("contact_type")
        if contact_type:
            return self.list_crm_contacts(contact_type=str(contact_type), limit=200)
        return self.list_crm_contacts(limit=50)

    def list_crm_campaigns(self, *, status: str | None = None) -> list[dict[str, object]]:
        if status:
            rows = self.all("SELECT * FROM crm_campaigns WHERE status = ? ORDER BY id DESC", (status,))
        else:
            rows = self.all("SELECT * FROM crm_campaigns ORDER BY id DESC LIMIT 100")
        return [dict(r) for r in rows]

    def create_crm_segment(self, *, name: str, criteria: dict[str, Any] | None = None) -> dict[str, object]:
        now = _utcnow()
        segment_key = f"segment-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_segments (segment_key, name, criteria_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (segment_key, name, _json(criteria or {}), now, now),
            )
        return dict(self.one("SELECT * FROM crm_segments WHERE segment_key = ?", (segment_key,)))

    def add_crm_segment_member(self, segment_id: int, contact_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO crm_segment_members (segment_id, contact_id, added_at)
                VALUES (?, ?, ?)
                """,
                (segment_id, contact_id, now),
            )
        row = self.one("SELECT * FROM crm_segment_members WHERE segment_id = ? AND contact_id = ?", (segment_id, contact_id))
        return dict(row) if row else {}

    def list_crm_segments(self) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM crm_segments ORDER BY id DESC")]

    # --- Scoring ---

    def compute_crm_customer_scores(self, contact_id: int) -> dict[str, int]:
        contact = self.get_crm_contact(contact_id)
        customer = self.one("SELECT * FROM crm_customers WHERE contact_id = ?", (contact_id,))
        if customer:
            contact = {**contact, "lifetime_value": customer.get("lifetime_value")}
        comm_count = self.scalar("SELECT COUNT(*) FROM crm_communications WHERE contact_id = ?", (contact_id,))
        opp_count = self.scalar("SELECT COUNT(*) FROM crm_opportunities WHERE contact_id = ?", (contact_id,))
        last_comm = self.one(
            "SELECT sent_at, created_at FROM crm_communications WHERE contact_id = ? ORDER BY id DESC LIMIT 1",
            (contact_id,),
        )
        last_ts = str(last_comm.get("sent_at") or last_comm.get("created_at")) if last_comm else None
        engine = CrmPlatformEngine()
        days_since = engine.days_since(last_ts)
        scores = engine.analytics.compute_scores(
            contact=contact,
            communications=comm_count,
            opportunities=opp_count,
            days_since_contact=days_since,
        )
        now = _utcnow()
        with self._transaction() as conn:
            for key, value in scores.items():
                conn.execute(
                    """
                    INSERT OR REPLACE INTO crm_customer_scores (contact_id, score_key, score, computed_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (contact_id, key, value, now),
                )
        return scores

    def get_crm_customer_scores(self, contact_id: int) -> dict[str, int]:
        rows = self.all("SELECT score_key, score FROM crm_customer_scores WHERE contact_id = ?", (contact_id,))
        if not rows:
            return self.compute_crm_customer_scores(contact_id)
        return {str(r["score_key"]): int(r["score"]) for r in rows}

    # --- Satisfaction ---

    def submit_crm_satisfaction_response(
        self,
        *,
        survey_id: int,
        contact_id: int,
        rating: int,
        answers: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_satisfaction_responses (survey_id, contact_id, rating, answers_json, submitted_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (survey_id, contact_id, rating, _json(answers or {}), now, now),
            )
        self._record_crm_journey(contact_id, event_type="satisfaction_submitted", summary=f"Enquête satisfaction: {rating}/10")
        row = dict(
            self.one(
                "SELECT * FROM crm_satisfaction_responses WHERE survey_id = ? AND contact_id = ? ORDER BY id DESC LIMIT 1",
                (survey_id, contact_id),
            )
        )
        return row

    def list_crm_satisfaction_surveys(self) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM crm_satisfaction_surveys ORDER BY id DESC")]

    def crm_satisfaction_summary(self, survey_id: int) -> dict[str, object]:
        survey = self.one("SELECT * FROM crm_satisfaction_surveys WHERE id = ?", (survey_id,))
        if survey is None:
            from ..errors import NotFoundError
            raise NotFoundError("survey not found")
        responses = [dict(r) for r in self.all("SELECT * FROM crm_satisfaction_responses WHERE survey_id = ?", (survey_id,))]
        engine = CrmPlatformEngine()
        return engine.satisfaction.survey_summary(survey_type=str(survey["survey_type"]), responses=responses)

    # --- Notes & Documents ---

    def add_crm_note(self, *, contact_id: int, content: str, author_id: int | None = None, visibility: str = "internal") -> dict[str, object]:
        now = _utcnow()
        note_key = f"note-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_notes (note_key, contact_id, author_id, content, visibility, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (note_key, contact_id, author_id, content, visibility, now, now),
            )
        return dict(self.one("SELECT * FROM crm_notes WHERE note_key = ?", (note_key,)))

    def list_crm_notes(self, contact_id: int) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM crm_notes WHERE contact_id = ? ORDER BY id DESC", (contact_id,))]

    def add_crm_document(self, *, contact_id: int, title: str, document_type: str = "other") -> dict[str, object]:
        now = _utcnow()
        document_key = f"doc-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_documents (document_key, contact_id, title, document_type, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (document_key, contact_id, title, document_type, now),
            )
        return dict(self.one("SELECT * FROM crm_documents WHERE document_key = ?", (document_key,)))

    def list_crm_documents(self, contact_id: int) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM crm_documents WHERE contact_id = ?", (contact_id,))]

    # --- AI Suggestions ---

    def generate_crm_ai_suggestions(self, contact_id: int) -> list[dict[str, object]]:
        contact = self.get_crm_contact(contact_id)
        communications = self.list_crm_communications(contact_id=contact_id, limit=1)
        last_comm = communications[0] if communications else None
        leads = self.list_crm_leads(limit=1000)
        contact_leads = [l for l in leads if int(l["contact_id"]) == contact_id]
        engine = CrmPlatformEngine()
        suggestions: list[dict[str, object]] = []
        suggestions.append(engine.ai.suggest_followup(contact=contact, last_communication=last_comm))
        if contact_leads:
            suggestions.append(engine.ai.suggest_next_action(lead=contact_leads[0]))
        knowledge = engine.ai.enrich_with_knowledge(self, f"CRM followup for {contact.get('full_name')}")
        if knowledge:
            suggestions.append(
                {
                    "suggestion_type": "knowledge",
                    "title": "Contexte knowledge disponible",
                    "rationale": "RAG knowledge platform",
                    "payload": {"knowledge": True},
                    "sources": engine.integration_sources(),
                }
            )
        now = _utcnow()
        stored: list[dict[str, object]] = []
        with self._transaction() as conn:
            for suggestion in suggestions:
                skey = f"suggest-{uuid.uuid4().hex[:8]}"
                conn.execute(
                    """
                    INSERT INTO crm_ai_suggestions (
                        suggestion_key, contact_id, suggestion_type, title, rationale, payload_json, sources_json, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        skey,
                        contact_id,
                        suggestion.get("suggestion_type"),
                        suggestion.get("title"),
                        suggestion.get("rationale"),
                        _json(suggestion.get("payload") or {}),
                        _json(suggestion.get("sources") or engine.integration_sources()),
                        now,
                    ),
                )
                stored.append(dict(self.one("SELECT * FROM crm_ai_suggestions WHERE suggestion_key = ?", (skey,))))
        return stored

    def list_crm_ai_suggestions(self, *, contact_id: int | None = None) -> list[dict[str, object]]:
        if contact_id is not None:
            rows = self.all("SELECT * FROM crm_ai_suggestions WHERE contact_id = ? ORDER BY id DESC LIMIT 50", (contact_id,))
        else:
            rows = self.all("SELECT * FROM crm_ai_suggestions ORDER BY id DESC LIMIT 50")
        return [dict(r) for r in rows]

    # --- Customer 360 / Journey / Timeline ---

    def customer_360(self, contact_id: int) -> dict[str, object]:
        contact = self.get_crm_contact(contact_id)
        leads = [l for l in self.list_crm_leads(limit=500) if int(l["contact_id"]) == contact_id]
        customer_row = self.one("SELECT * FROM crm_customers WHERE contact_id = ?", (contact_id,))
        customer = dict(customer_row) if customer_row else None
        opportunities = self.list_crm_opportunities(contact_id=contact_id)
        communications = self.list_crm_communications(contact_id=contact_id, limit=20)
        scores = self.get_crm_customer_scores(contact_id)
        timeline = self.list_crm_timeline(contact_id)
        journey = self.list_crm_journey(contact_id)
        engine = CrmPlatformEngine()
        return engine.customer_360.assemble(
            contact=contact,
            leads=leads,
            customer=customer,
            opportunities=opportunities,
            communications=communications,
            scores=scores,
            timeline=timeline,
            journey=journey,
        )

    def list_crm_timeline(self, contact_id: int) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM crm_timeline_entries WHERE contact_id = ? ORDER BY created_at DESC LIMIT 50", (contact_id,))
        return [dict(r) for r in rows]

    def list_crm_journey(self, contact_id: int) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM crm_journey_events WHERE contact_id = ? ORDER BY created_at DESC LIMIT 50", (contact_id,))
        return [dict(r) for r in rows]

    # --- Search & Analytics ---

    def crm_search(self, *, query: str, limit: int = 20) -> list[dict[str, object]]:
        engine = CrmPlatformEngine()
        normalized = engine.search.normalize(query)
        if not normalized:
            return []
        pattern = f"%{normalized.split()[0]}%"
        rows = self.all(
            """
            SELECT * FROM crm_contact_profiles
            WHERE LOWER(full_name) LIKE ? OR LOWER(email) LIKE ? OR LOWER(phone) LIKE ? OR LOWER(company) LIKE ?
            ORDER BY id DESC LIMIT ?
            """,
            (pattern, pattern, pattern, pattern, limit),
        )
        return [dict(r) for r in rows]

    def crm_analytics(self) -> dict[str, object]:
        return {
            "contacts": self.scalar("SELECT COUNT(*) FROM crm_contact_profiles"),
            "leads": self.scalar("SELECT COUNT(*) FROM crm_leads"),
            "leads_new": self.scalar("SELECT COUNT(*) FROM crm_leads WHERE status = 'new'"),
            "customers": self.scalar("SELECT COUNT(*) FROM crm_customers"),
            "opportunities_open": self.scalar("SELECT COUNT(*) FROM crm_opportunities WHERE status NOT IN ('won', 'lost', 'closed')"),
            "communications": self.scalar("SELECT COUNT(*) FROM crm_communications"),
            "whatsapp_messages": self.scalar("SELECT COUNT(*) FROM crm_whatsapp_messages"),
            "telegram_messages": self.scalar("SELECT COUNT(*) FROM crm_telegram_messages"),
            "email_messages": self.scalar("SELECT COUNT(*) FROM crm_email_messages"),
            "sms_messages": self.scalar("SELECT COUNT(*) FROM crm_sms_messages"),
            "campaigns": self.scalar("SELECT COUNT(*) FROM crm_campaigns"),
            "followups_pending": self.scalar("SELECT COUNT(*) FROM crm_followups WHERE status = 'scheduled'"),
            "pipeline_items": self.scalar("SELECT COUNT(*) FROM crm_pipeline_items"),
            "avg_lead_score": self.scalar("SELECT COALESCE(AVG(score), 0) FROM crm_leads"),
            "sources": self.scalar("SELECT COUNT(*) FROM crm_lead_sources"),
            "sources_with_context": self.scalar("SELECT COUNT(*) FROM source_intelligence_source_contexts"),
            "source_imports": self.scalar("SELECT COUNT(*) FROM source_intelligence_imports"),
            "official_sender": to_public_dict(),
        }

    def crm_stats(self) -> dict[str, object]:
        analytics = self.crm_analytics()
        return {
            **analytics,
            "segments": self.scalar("SELECT COUNT(*) FROM crm_segments"),
            "satisfaction_responses": self.scalar("SELECT COUNT(*) FROM crm_satisfaction_responses"),
            "ai_suggestions": self.scalar("SELECT COUNT(*) FROM crm_ai_suggestions"),
        }

    def crm_dashboard(self) -> dict[str, object]:
        analytics = self.crm_analytics()
        recent_leads = self.list_crm_leads(limit=5)
        pending_followups = self.list_crm_followups(status="scheduled")[:5]
        default_pipeline = self.one("SELECT id FROM crm_pipelines WHERE is_default = 1 ORDER BY id ASC LIMIT 1")
        board = self.get_crm_pipeline_board(int(default_pipeline["id"])) if default_pipeline else []
        return {
            "analytics": analytics,
            "recent_leads": recent_leads,
            "pending_followups": pending_followups,
            "pipeline_board": board,
            "lawim_contact": to_public_dict(),
        }

    def snapshot_crm_analytics(self) -> dict[str, object]:
        stats = self.crm_analytics()
        now = _utcnow()
        key = f"snapshot-{uuid.uuid4().hex[:10]}-{now}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_analytics_snapshots (snapshot_key, scope, metrics_json, created_at)
                VALUES (?, 'global', ?, ?)
                """,
                (key, _json(stats), now),
            )
        return {"snapshot_key": key, "metrics": stats}

    def _record_crm_journey(self, contact_id: int, *, event_type: str, summary: str, actor_id: int | None = None) -> None:
        now = _utcnow()
        event_key = f"journey-{event_type}-{uuid.uuid4().hex[:6]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_journey_events (contact_id, event_type, event_key, summary, actor_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (contact_id, event_type, event_key, summary, actor_id, now),
            )

    def _append_crm_timeline(
        self,
        contact_id: int,
        *,
        entry_type: str,
        summary: str,
        reference_type: str | None = None,
        reference_id: int | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO crm_timeline_entries (
                    contact_id, entry_type, summary, reference_type, reference_id, payload_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (contact_id, entry_type, summary, reference_type, reference_id, _json(payload or {}), now),
            )
