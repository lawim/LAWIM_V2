from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from ..errors import NotFoundError
from ..repository_introspection import tables_present
from .constants import DEFAULT_SOURCE_TARGET, SOURCE_CHANNELS, SOURCE_IMPORT_STATUSES, SOURCE_STATUSES
from .dto import source_context_dto, source_dto, import_dto
from .engines import DashboardEngine, ReferenceCodeEngine, SourceAnalysisEngine, WhatsAppLinkEngine


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _parse_json(value: str | None, fallback: Any) -> Any:
    if value in (None, ""):
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def _slugify(text: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return normalized or f"source-{uuid.uuid4().hex[:8]}"


class SourceIntelligenceRepositoryMixin:
    def source_intelligence_tables_present(self) -> bool:
        return tables_present(self, ("source_intelligence_source_contexts", "source_intelligence_imports"))

    def _source_engine(self) -> SourceAnalysisEngine:
        return SourceAnalysisEngine()

    def _reference_code_engine(self) -> ReferenceCodeEngine:
        return ReferenceCodeEngine()

    def _whatsapp_engine(self) -> WhatsAppLinkEngine:
        return WhatsAppLinkEngine()

    def _dashboard_engine(self) -> DashboardEngine:
        return DashboardEngine()

    def seed_source_intelligence_catalog(self) -> dict[str, object]:
        now = _utcnow()
        source_owner = self.one("SELECT id FROM users ORDER BY id ASC LIMIT 1")
        created_by = int(source_owner["id"]) if source_owner else None
        seed_sources = (
            {
                "source_key": "source-web",
                "name": "Site web LAWIM",
                "channel": "web",
                "target": "organic",
                "publication_url": "https://lawim.cm",
                "publication_title": "LAWIM Website",
                "publication_author": "LAWIM",
                "campaign": "organic",
                "city": "Douala",
                "property_type": "apartment",
                "target_audience": "prospects",
                "format": "link",
                "language": "fr",
                "tags": ["lawim", "web"],
                "notes": "Seeded acquisition source for the public website.",
            },
            {
                "source_key": "source-whatsapp",
                "name": "WhatsApp entrant",
                "channel": "whatsapp",
                "target": "conversation",
                "publication_url": "",
                "publication_title": "WhatsApp",
                "publication_author": "LAWIM",
                "campaign": "messaging",
                "city": "",
                "property_type": "",
                "target_audience": "prospects",
                "format": "message",
                "language": "fr",
                "tags": ["lawim", "whatsapp"],
                "notes": "Seeded acquisition source for inbound WhatsApp requests.",
            },
            {
                "source_key": "source-referral",
                "name": "Recommandation",
                "channel": "referral",
                "target": "referral",
                "publication_url": "",
                "publication_title": "Referral",
                "publication_author": "Community",
                "campaign": "referral",
                "city": "",
                "property_type": "",
                "target_audience": "prospects",
                "format": "manual",
                "language": "fr",
                "tags": ["lawim", "referral"],
                "notes": "Seeded acquisition source for referrals.",
            },
            {
                "source_key": "source-rei",
                "name": "Real Estate Intelligence",
                "channel": "rei",
                "target": "pipeline",
                "publication_url": "",
                "publication_title": "REI",
                "publication_author": "LAWIM",
                "campaign": "rei",
                "city": "",
                "property_type": "apartment",
                "target_audience": "buyers",
                "format": "system",
                "language": "fr",
                "tags": ["lawim", "rei"],
                "notes": "Seeded internal acquisition source for REI workflows.",
            },
        )
        created = 0
        for seed in seed_sources:
            reference_code = self._reference_code_engine().generate(seed=seed["source_key"])
            metadata = {
                "seeded": True,
                "source_key": seed["source_key"],
                "channel": seed["channel"],
            }
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO crm_lead_sources (
                        source_key, reference_code, name, channel, status, target, created_by,
                        metadata_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', ?, ?, ?, ?, ?)
                    """,
                    (
                        seed["source_key"],
                        reference_code,
                        seed["name"],
                        seed["channel"],
                        seed["target"],
                        created_by,
                        _json(metadata),
                        now,
                        now,
                    ),
                )
                conn.execute(
                    """
                    UPDATE crm_lead_sources
                    SET reference_code = COALESCE(NULLIF(reference_code, ''), ?),
                        name = ?,
                        channel = ?,
                        status = COALESCE(NULLIF(status, ''), 'active'),
                        target = COALESCE(NULLIF(target, ''), ?),
                        created_by = COALESCE(created_by, ?),
                        updated_at = ?
                    WHERE source_key = ?
                    """,
                    (
                        reference_code,
                        seed["name"],
                        seed["channel"],
                        seed["target"],
                        created_by,
                        now,
                        seed["source_key"],
                    ),
                )
            source_row = self.one("SELECT * FROM crm_lead_sources WHERE source_key = ?", (seed["source_key"],))
            assert source_row is not None
            context_payload = self._source_engine().analyze(
                source_name=str(seed["name"]),
                source_key=str(seed["source_key"]),
                reference_code=str(source_row["reference_code"] or reference_code),
                url=str(seed.get("publication_url") or ""),
                title=str(seed.get("publication_title") or seed["name"]),
                text=str(seed.get("publication_text") or ""),
                author=str(seed.get("publication_author") or ""),
                campaign=str(seed.get("campaign") or ""),
                city=str(seed.get("city") or ""),
                district=str(seed.get("district") or ""),
                property_type=str(seed.get("property_type") or ""),
                target_audience=str(seed.get("target_audience") or DEFAULT_SOURCE_TARGET),
                format_name=str(seed.get("format") or ""),
                language=str(seed.get("language") or "fr"),
                tags=list(seed.get("tags") or []),
                notes=str(seed.get("notes") or ""),
                network=str(seed.get("channel") or "web"),
            )
            context_payload["whatsapp_link"] = self._whatsapp_engine().build_link(
                reference_code=str(source_row["reference_code"] or reference_code),
                source_name=str(source_row["name"]),
            )
            self.upsert_source_intelligence_context(
                int(source_row["id"]),
                network=str(context_payload["network"]),
                publication_url=str(context_payload["publication_url"]),
                publication_title=str(context_payload["publication_title"]),
                publication_text=str(context_payload["publication_text"]),
                publication_author=str(context_payload["publication_author"]),
                campaign=str(context_payload["campaign"]),
                city=str(context_payload["city"]),
                district=str(context_payload["district"]),
                property_type=str(context_payload["property_type"]),
                target_audience=str(context_payload["target_audience"]),
                format_name=str(context_payload["format"]),
                language=str(context_payload["language"]),
                tags=list(context_payload["tags_json"]),
                ai_classification=str(context_payload["ai_classification"]),
                ai_confidence=float(context_payload["ai_confidence"]),
                analysis=dict(context_payload["analysis_json"]),
                notes=str(context_payload["notes"]),
                whatsapp_link=str(context_payload["whatsapp_link"]),
            )
            created += 1
        self.record_event("source_intelligence_catalog_seeded", {"sources": created})
        return {"seeded": created, "sources": created}

    def _resolve_source_row(
        self,
        *,
        source_id: int | None = None,
        reference_code: str | None = None,
        source_key: str | None = None,
    ) -> dict[str, object] | None:
        if source_id is not None:
            row = self.one(
                """
                SELECT s.*, c.network, c.publication_url, c.publication_title, c.publication_text,
                       c.publication_author, c.campaign, c.city, c.district, c.property_type,
                       c.target_audience, c.format, c.language, c.tags_json, c.ai_classification,
                       c.ai_confidence, c.analysis_json, c.notes, c.whatsapp_link, c.created_at AS context_created_at,
                       c.updated_at AS context_updated_at,
                       COALESCE((SELECT COUNT(*) FROM crm_leads l WHERE l.source_id = s.id), 0) AS lead_count,
                       COALESCE((SELECT COUNT(*) FROM crm_leads l WHERE l.source_id = s.id AND l.converted_customer_id IS NOT NULL), 0) AS customer_count,
                       COALESCE((SELECT COUNT(*) FROM crm_communications comm JOIN crm_leads l ON l.contact_id = comm.contact_id WHERE l.source_id = s.id AND comm.channel = 'whatsapp'), 0) AS whatsapp_count,
                       COALESCE((SELECT COUNT(*) FROM source_intelligence_imports i WHERE i.source_id = s.id), 0) AS import_count,
                       (SELECT MAX(i.imported_at) FROM source_intelligence_imports i WHERE i.source_id = s.id) AS last_imported_at
                FROM crm_lead_sources s
                LEFT JOIN source_intelligence_source_contexts c ON c.source_id = s.id
                WHERE s.id = ?
                """,
                (source_id,),
            )
            return dict(row) if row else None
        if reference_code:
            row = self.one(
                """
                SELECT s.*, c.network, c.publication_url, c.publication_title, c.publication_text,
                       c.publication_author, c.campaign, c.city, c.district, c.property_type,
                       c.target_audience, c.format, c.language, c.tags_json, c.ai_classification,
                       c.ai_confidence, c.analysis_json, c.notes, c.whatsapp_link, c.created_at AS context_created_at,
                       c.updated_at AS context_updated_at,
                       COALESCE((SELECT COUNT(*) FROM crm_leads l WHERE l.source_id = s.id), 0) AS lead_count,
                       COALESCE((SELECT COUNT(*) FROM crm_leads l WHERE l.source_id = s.id AND l.converted_customer_id IS NOT NULL), 0) AS customer_count,
                       COALESCE((SELECT COUNT(*) FROM crm_communications comm JOIN crm_leads l ON l.contact_id = comm.contact_id WHERE l.source_id = s.id AND comm.channel = 'whatsapp'), 0) AS whatsapp_count,
                       COALESCE((SELECT COUNT(*) FROM source_intelligence_imports i WHERE i.source_id = s.id), 0) AS import_count,
                       (SELECT MAX(i.imported_at) FROM source_intelligence_imports i WHERE i.source_id = s.id) AS last_imported_at
                FROM crm_lead_sources s
                LEFT JOIN source_intelligence_source_contexts c ON c.source_id = s.id
                WHERE s.reference_code = ?
                """,
                (reference_code,),
            )
            return dict(row) if row else None
        if source_key:
            row = self.one(
                """
                SELECT s.*, c.network, c.publication_url, c.publication_title, c.publication_text,
                       c.publication_author, c.campaign, c.city, c.district, c.property_type,
                       c.target_audience, c.format, c.language, c.tags_json, c.ai_classification,
                       c.ai_confidence, c.analysis_json, c.notes, c.whatsapp_link, c.created_at AS context_created_at,
                       c.updated_at AS context_updated_at,
                       COALESCE((SELECT COUNT(*) FROM crm_leads l WHERE l.source_id = s.id), 0) AS lead_count,
                       COALESCE((SELECT COUNT(*) FROM crm_leads l WHERE l.source_id = s.id AND l.converted_customer_id IS NOT NULL), 0) AS customer_count,
                       COALESCE((SELECT COUNT(*) FROM crm_communications comm JOIN crm_leads l ON l.contact_id = comm.contact_id WHERE l.source_id = s.id AND comm.channel = 'whatsapp'), 0) AS whatsapp_count,
                       COALESCE((SELECT COUNT(*) FROM source_intelligence_imports i WHERE i.source_id = s.id), 0) AS import_count,
                       (SELECT MAX(i.imported_at) FROM source_intelligence_imports i WHERE i.source_id = s.id) AS last_imported_at
                FROM crm_lead_sources s
                LEFT JOIN source_intelligence_source_contexts c ON c.source_id = s.id
                WHERE s.source_key = ?
                """,
                (source_key,),
            )
            return dict(row) if row else None
        return None

    def resolve_source_intelligence_source(
        self,
        *,
        source_id: int | None = None,
        reference_code: str | None = None,
        source_key: str | None = None,
    ) -> dict[str, object]:
        row = self._resolve_source_row(
            source_id=source_id,
            reference_code=reference_code,
            source_key=source_key,
        )
        if row is None:
            raise NotFoundError("source not found")
        return row

    def list_source_intelligence_sources(
        self,
        *,
        status: str | None = None,
        query: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, object]]:
        clauses = []
        params: list[object] = []
        if status:
            clauses.append("s.status = ?")
            params.append(status)
        if query:
            clauses.append(
                "(LOWER(s.source_key) LIKE ? OR LOWER(s.reference_code) LIKE ? OR LOWER(s.name) LIKE ? OR LOWER(c.publication_url) LIKE ?)"
            )
            pattern = f"%{query.lower()}%"
            params.extend([pattern, pattern, pattern, pattern])
        where_clause = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        rows = self.all(
            f"""
            SELECT s.*, c.network, c.publication_url, c.publication_title, c.publication_text,
                   c.publication_author, c.campaign, c.city, c.district, c.property_type,
                   c.target_audience, c.format, c.language, c.tags_json, c.ai_classification,
                   c.ai_confidence, c.analysis_json, c.notes, c.whatsapp_link, c.created_at AS context_created_at,
                   c.updated_at AS context_updated_at,
                   COALESCE((SELECT COUNT(*) FROM crm_leads l WHERE l.source_id = s.id), 0) AS lead_count,
                   COALESCE((SELECT COUNT(*) FROM crm_leads l WHERE l.source_id = s.id AND l.converted_customer_id IS NOT NULL), 0) AS customer_count,
                   COALESCE((SELECT COUNT(*) FROM crm_communications comm JOIN crm_leads l ON l.contact_id = comm.contact_id WHERE l.source_id = s.id AND comm.channel = 'whatsapp'), 0) AS whatsapp_count,
                   COALESCE((SELECT COUNT(*) FROM source_intelligence_imports i WHERE i.source_id = s.id), 0) AS import_count,
                   (SELECT MAX(i.imported_at) FROM source_intelligence_imports i WHERE i.source_id = s.id) AS last_imported_at
            FROM crm_lead_sources s
            LEFT JOIN source_intelligence_source_contexts c ON c.source_id = s.id
            {where_clause}
            ORDER BY s.created_at DESC, s.id DESC
            LIMIT ?
            """,
            (*params, limit),
        )
        payload = [dict(row) for row in rows]
        for row in payload:
            context = source_context_dto(row)
            row.update(context)
            row["metadata"] = _parse_json(row.get("metadata_json"), {})
            row["reference_code"] = row.get("reference_code") or row.get("source_key")
            lead_count = int(row.get("lead_count") or 0)
            customer_count = int(row.get("customer_count") or 0)
            row["conversion_rate"] = round((customer_count / lead_count) * 100.0, 2) if lead_count else 0.0
            if not row.get("whatsapp_link") and row.get("reference_code"):
                row["whatsapp_link"] = self._whatsapp_engine().build_link(
                    reference_code=str(row["reference_code"]),
                    source_name=str(row.get("name") or ""),
                )
        return payload

    def create_source_intelligence_source(
        self,
        *,
        name: str,
        channel: str = "web",
        target: str = DEFAULT_SOURCE_TARGET,
        source_key: str | None = None,
        reference_code: str | None = None,
        status: str = "active",
        created_by: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        normalized_name = str(name).strip()
        normalized_channel = str(channel or "web").strip().lower()
        if normalized_channel not in SOURCE_CHANNELS:
            normalized_channel = "other"
        normalized_status = str(status or "active").strip().lower()
        if normalized_status not in SOURCE_STATUSES:
            normalized_status = "active"
        key = source_key or f"source-{_slugify(normalized_name)}"
        code = reference_code or self._reference_code_engine().generate(seed=f"{key}:{normalized_name}")
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO crm_lead_sources (
                    source_key, reference_code, name, channel, status, target, created_by,
                    metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    code,
                    normalized_name,
                    normalized_channel,
                    normalized_status,
                    target,
                    created_by,
                    _json(metadata or {}),
                    now,
                    now,
                ),
            )
            conn.execute(
                """
                UPDATE crm_lead_sources
                SET name = ?,
                    channel = ?,
                    status = ?,
                    reference_code = COALESCE(NULLIF(reference_code, ''), ?),
                    target = COALESCE(NULLIF(target, ''), ?),
                    created_by = COALESCE(created_by, ?),
                    metadata_json = COALESCE(NULLIF(metadata_json, ''), ?),
                    updated_at = ?
                WHERE source_key = ?
                """,
                (
                    normalized_name,
                    normalized_channel,
                    normalized_status,
                    code,
                    target,
                    created_by,
                    _json(metadata or {}),
                    now,
                    key,
                ),
            )
        return self.resolve_source_intelligence_source(source_key=key)

    def update_source_intelligence_source(self, source_id: int, **fields: object) -> dict[str, object]:
        current = self.resolve_source_intelligence_source(source_id=source_id)
        allowed = {"name", "channel", "status", "target", "metadata_json", "created_by"}
        updates: dict[str, object] = {}
        for key, value in fields.items():
            if key in allowed and value is not None:
                updates[key] = value
        if "metadata" in fields and fields["metadata"] is not None:
            updates["metadata_json"] = _json(fields["metadata"])
        if not updates:
            return current
        if "status" in updates and str(updates["status"]) not in SOURCE_STATUSES:
            updates["status"] = current["status"]
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{column} = ?" for column in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE crm_lead_sources SET {cols} WHERE id = ?", (*updates.values(), source_id))
        return self.resolve_source_intelligence_source(source_id=source_id)

    def upsert_source_intelligence_context(
        self,
        source_id: int,
        *,
        network: str = "",
        publication_url: str = "",
        publication_title: str = "",
        publication_text: str = "",
        publication_author: str = "",
        campaign: str = "",
        city: str = "",
        district: str = "",
        property_type: str = "",
        target_audience: str = "",
        format_name: str = "",
        language: str = "",
        tags: list[str] | None = None,
        ai_classification: str = "",
        ai_confidence: float = 0.0,
        analysis: dict[str, Any] | None = None,
        notes: str = "",
        whatsapp_link: str = "",
    ) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO source_intelligence_source_contexts (
                    source_id, network, publication_url, publication_title, publication_text,
                    publication_author, campaign, city, district, property_type,
                    target_audience, format, language, tags_json, ai_classification,
                    ai_confidence, analysis_json, notes, whatsapp_link, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source_id,
                    network,
                    publication_url,
                    publication_title,
                    publication_text,
                    publication_author,
                    campaign,
                    city,
                    district,
                    property_type,
                    target_audience,
                    format_name,
                    language,
                    _json(tags or []),
                    ai_classification,
                    ai_confidence,
                    _json(analysis or {}),
                    notes,
                    whatsapp_link,
                    now,
                    now,
                ),
            )
            conn.execute(
                """
                UPDATE source_intelligence_source_contexts
                SET network = ?,
                    publication_url = ?,
                    publication_title = ?,
                    publication_text = ?,
                    publication_author = ?,
                    campaign = ?,
                    city = ?,
                    district = ?,
                    property_type = ?,
                    target_audience = ?,
                    format = ?,
                    language = ?,
                    tags_json = ?,
                    ai_classification = ?,
                    ai_confidence = ?,
                    analysis_json = ?,
                    notes = ?,
                    whatsapp_link = ?,
                    updated_at = ?
                WHERE source_id = ?
                """,
                (
                    network,
                    publication_url,
                    publication_title,
                    publication_text,
                    publication_author,
                    campaign,
                    city,
                    district,
                    property_type,
                    target_audience,
                    format_name,
                    language,
                    _json(tags or []),
                    ai_classification,
                    ai_confidence,
                    _json(analysis or {}),
                    notes,
                    whatsapp_link,
                    now,
                    source_id,
                ),
            )
        row = self.one("SELECT * FROM source_intelligence_source_contexts WHERE source_id = ?", (source_id,))
        return dict(row) if row else {}

    def get_source_intelligence_context(self, source_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM source_intelligence_source_contexts WHERE source_id = ?", (source_id,))
        if row is None:
            raise NotFoundError("source context not found")
        return dict(row)

    def list_source_intelligence_contexts(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all(
            """
            SELECT * FROM source_intelligence_source_contexts
            ORDER BY updated_at DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in rows]

    def create_source_intelligence_import(
        self,
        *,
        source_id: int,
        source_url: str,
        source_channel: str = "",
        payload: dict[str, Any] | None = None,
        result: dict[str, Any] | None = None,
        import_status: str = "imported",
        analyzed_at: str | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        import_key = f"import-{uuid.uuid4().hex[:12]}"
        normalized_status = import_status if import_status in SOURCE_IMPORT_STATUSES else "imported"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO source_intelligence_imports (
                    import_key, source_id, source_url, import_status, source_channel,
                    imported_at, analyzed_at, payload_json, result_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    import_key,
                    source_id,
                    source_url,
                    normalized_status,
                    source_channel,
                    now,
                    analyzed_at,
                    _json(payload or {}),
                    _json(result or {}),
                    now,
                    now,
                ),
            )
        row = self.one("SELECT * FROM source_intelligence_imports WHERE import_key = ?", (import_key,))
        return dict(row) if row else {}

    def list_source_intelligence_imports(self, *, limit: int = 50, source_id: int | None = None) -> list[dict[str, object]]:
        query = "SELECT * FROM source_intelligence_imports WHERE 1=1"
        params: list[object] = []
        if source_id is not None:
            query += " AND source_id = ?"
            params.append(source_id)
        query += " ORDER BY imported_at DESC, id DESC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(query, tuple(params))]

    def analyze_source_intelligence(
        self,
        *,
        source_id: int,
        url: str | None = None,
        title: str | None = None,
        text: str | None = None,
        author: str | None = None,
        campaign: str | None = None,
        city: str | None = None,
        district: str | None = None,
        property_type: str | None = None,
        target_audience: str | None = None,
        format_name: str | None = None,
        language: str | None = None,
        tags: list[str] | None = None,
        notes: str | None = None,
        network: str | None = None,
    ) -> dict[str, object]:
        source = self.resolve_source_intelligence_source(source_id=source_id)
        analysis = self._source_engine().analyze(
            source_name=str(source.get("name") or ""),
            source_key=str(source.get("source_key") or ""),
            reference_code=str(source.get("reference_code") or source.get("source_key") or ""),
            url=url or str(source.get("publication_url") or ""),
            title=title or str(source.get("publication_title") or ""),
            text=text or str(source.get("publication_text") or ""),
            author=author or str(source.get("publication_author") or ""),
            campaign=campaign or str(source.get("campaign") or ""),
            city=city or str(source.get("city") or ""),
            district=district or str(source.get("district") or ""),
            property_type=property_type or str(source.get("property_type") or ""),
            target_audience=target_audience or str(source.get("target_audience") or DEFAULT_SOURCE_TARGET),
            format_name=format_name or str(source.get("format") or ""),
            language=language or str(source.get("language") or ""),
            tags=tags or list(_parse_json(source.get("tags_json"), [])),
            notes=notes or str(source.get("notes") or ""),
            network=network or str(source.get("network") or source.get("channel") or ""),
        )
        context = self.upsert_source_intelligence_context(
            source_id,
            network=str(analysis["network"]),
            publication_url=str(analysis["publication_url"]),
            publication_title=str(analysis["publication_title"]),
            publication_text=str(analysis["publication_text"]),
            publication_author=str(analysis["publication_author"]),
            campaign=str(analysis["campaign"]),
            city=str(analysis["city"]),
            district=str(analysis["district"]),
            property_type=str(analysis["property_type"]),
            target_audience=str(analysis["target_audience"]),
            format_name=str(analysis["format"]),
            language=str(analysis["language"]),
            tags=list(analysis["tags_json"]),
            ai_classification=str(analysis["ai_classification"]),
            ai_confidence=float(analysis["ai_confidence"]),
            analysis=dict(analysis["analysis_json"]),
            notes=str(analysis["notes"]),
            whatsapp_link=self._whatsapp_engine().build_link(
                reference_code=str(source.get("reference_code") or source.get("source_key") or ""),
                source_name=str(source.get("name") or ""),
            ),
        )
        import_row = self.create_source_intelligence_import(
            source_id=source_id,
            source_url=str(analysis["publication_url"]),
            source_channel=str(analysis["network"]),
            payload={"analysis": analysis},
            result=context,
            import_status="analyzed",
            analyzed_at=_utcnow(),
        )
        self.record_event("source_intelligence_analyzed", {"source_id": source_id})
        return {
            "source": source_dto(source),
            "context": source_context_dto(context),
            "import": import_dto(import_row),
        }

    def source_intelligence_stats(self) -> dict[str, object]:
        sources = self.list_source_intelligence_sources(limit=1000)
        dashboard = self._dashboard_engine().build_stats(sources)
        sources_with_context = self.scalar("SELECT COUNT(*) FROM source_intelligence_source_contexts")
        imports_total = self.scalar("SELECT COUNT(*) FROM source_intelligence_imports")
        imports_analyzed = self.scalar("SELECT COUNT(*) FROM source_intelligence_imports WHERE analyzed_at IS NOT NULL")
        active_sources = self.scalar("SELECT COUNT(*) FROM crm_lead_sources WHERE status = 'active'")
        source_leads = self.scalar("SELECT COUNT(*) FROM crm_leads WHERE source_id IS NOT NULL")
        source_customers = self.scalar("SELECT COUNT(*) FROM crm_leads WHERE source_id IS NOT NULL AND converted_customer_id IS NOT NULL")
        average_row = self.one("SELECT COALESCE(AVG(ai_confidence), 0) AS average_ai_confidence FROM source_intelligence_source_contexts")
        average_confidence = float(average_row["average_ai_confidence"]) if average_row else 0.0
        return {
            **dashboard,
            "sources_total": self.scalar("SELECT COUNT(*) FROM crm_lead_sources"),
            "active_sources": active_sources,
            "sources_with_context": sources_with_context,
            "imports_total": imports_total,
            "imports_analyzed": imports_analyzed,
            "lead_count": source_leads,
            "customer_count": source_customers,
            "average_ai_confidence": average_confidence,
        }

    def source_intelligence_dashboard(self, *, limit: int = 10) -> dict[str, object]:
        sources = self.list_source_intelligence_sources(limit=max(limit, 10))
        dashboard_engine = self._dashboard_engine()
        return {
            "stats": self.source_intelligence_stats(),
            "sources": sources,
            "imports": [dict(row) for row in self.list_source_intelligence_imports(limit=limit)],
            "top_sources": dashboard_engine.top_sources(sources, limit=limit),
        }

    def source_intelligence_whatsapp_link(self, source_id: int) -> dict[str, object]:
        source = self.resolve_source_intelligence_source(source_id=source_id)
        code = str(source.get("reference_code") or source.get("source_key") or "")
        link = self._whatsapp_engine().build_link(reference_code=code, source_name=str(source.get("name") or ""))
        self.upsert_source_intelligence_context(
            source_id,
            network=str(source.get("network") or source.get("channel") or ""),
            publication_url=str(source.get("publication_url") or ""),
            publication_title=str(source.get("publication_title") or ""),
            publication_text=str(source.get("publication_text") or ""),
            publication_author=str(source.get("publication_author") or ""),
            campaign=str(source.get("campaign") or ""),
            city=str(source.get("city") or ""),
            district=str(source.get("district") or ""),
            property_type=str(source.get("property_type") or ""),
            target_audience=str(source.get("target_audience") or DEFAULT_SOURCE_TARGET),
            format_name=str(source.get("format") or ""),
            language=str(source.get("language") or ""),
            tags=list(_parse_json(source.get("tags_json"), [])),
            ai_classification=str(source.get("ai_classification") or ""),
            ai_confidence=float(source.get("ai_confidence") or 0.0),
            analysis=dict(_parse_json(source.get("analysis_json"), {})),
            notes=str(source.get("notes") or ""),
            whatsapp_link=link,
        )
        self.record_event("source_intelligence_whatsapp_link_generated", {"source_id": source_id})
        return {"source": source_dto({**source, "whatsapp_link": link}), "whatsapp_link": link}
