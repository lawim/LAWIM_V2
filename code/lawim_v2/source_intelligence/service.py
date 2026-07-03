from __future__ import annotations

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as sdto
from .engines import ReferenceCodeEngine


class ReferenceCodeService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = ReferenceCodeEngine()

    def generate(self, *, seed: str | None = None) -> dict[str, object]:
        code = self.engine.generate(seed=seed)
        return {"reference_code": code}


class SourceService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.references = ReferenceCodeService(repository)

    def list(self, *, status: str | None = None, query: str | None = None, limit: int = 50) -> dict[str, object]:
        METRICS.increment("source_intelligence_sources_total")
        rows = self.repository.list_source_intelligence_sources(status=status, query=query, limit=limit)
        return {"sources": [sdto.source_dto(row) for row in rows]}

    def get(self, *, source_id: int) -> dict[str, object]:
        METRICS.increment("source_intelligence_sources_total")
        return {"source": sdto.source_dto(self.repository.resolve_source_intelligence_source(source_id=source_id))}

    def create(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        source = self.repository.create_source_intelligence_source(
            name=str(body["name"]),
            channel=str(body.get("channel") or "web"),
            target=str(body.get("target") or "acquisition"),
            source_key=str(body.get("source_key")) if body.get("source_key") else None,
            reference_code=str(body.get("reference_code")) if body.get("reference_code") else None,
            status=str(body.get("status") or "active"),
            created_by=int(actor["id"]) if actor.get("id") is not None else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        METRICS.increment("source_intelligence_sources_total")
        return {"source": sdto.source_dto(source)}

    def update(self, *, source_id: int, body: dict[str, object]) -> dict[str, object]:
        source = self.repository.update_source_intelligence_source(source_id, **body)
        METRICS.increment("source_intelligence_sources_total")
        return {"source": sdto.source_dto(source)}

    def archive(self, *, source_id: int) -> dict[str, object]:
        source = self.repository.update_source_intelligence_source(source_id, status="archived")
        METRICS.increment("source_intelligence_sources_total")
        return {"source": sdto.source_dto(source)}


class SourceContextService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def get(self, *, source_id: int) -> dict[str, object]:
        METRICS.increment("source_intelligence_contexts_total")
        return {"context": sdto.source_context_dto(self.repository.get_source_intelligence_context(source_id))}

    def update(self, *, source_id: int, body: dict[str, object]) -> dict[str, object]:
        context = self.repository.upsert_source_intelligence_context(
            source_id,
            network=str(body.get("network") or ""),
            publication_url=str(body.get("publication_url") or ""),
            publication_title=str(body.get("publication_title") or ""),
            publication_text=str(body.get("publication_text") or ""),
            publication_author=str(body.get("publication_author") or ""),
            campaign=str(body.get("campaign") or ""),
            city=str(body.get("city") or ""),
            district=str(body.get("district") or ""),
            property_type=str(body.get("property_type") or ""),
            target_audience=str(body.get("target_audience") or ""),
            format_name=str(body.get("format") or body.get("format_name") or ""),
            language=str(body.get("language") or ""),
            tags=list(body.get("tags") or []),
            ai_classification=str(body.get("ai_classification") or ""),
            ai_confidence=float(body.get("ai_confidence") or 0.0),
            analysis=dict(body.get("analysis") or {}) if isinstance(body.get("analysis"), dict) else {},
            notes=str(body.get("notes") or ""),
            whatsapp_link=str(body.get("whatsapp_link") or ""),
        )
        METRICS.increment("source_intelligence_contexts_total")
        return {"context": sdto.source_context_dto(context)}


class ImportSourceService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def import_url(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        url = str(body.get("url") or body.get("publication_url") or "").strip()
        if not url:
            raise ValueError("url is required")
        name = str(body.get("name") or body.get("source_name") or body.get("title") or url).strip()
        channel = str(body.get("channel") or "").strip().lower() or self.repository._source_engine().infer_network(url, fallback="web")
        source = self.repository.create_source_intelligence_source(
            name=name,
            channel=channel,
            target=str(body.get("target") or "acquisition"),
            source_key=str(body.get("source_key")) if body.get("source_key") else None,
            reference_code=str(body.get("reference_code")) if body.get("reference_code") else None,
            status=str(body.get("status") or "active"),
            created_by=int(actor["id"]) if actor.get("id") is not None else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        analysis_payload = self.repository._source_engine().analyze(
            source_name=name,
            source_key=str(source.get("source_key") or ""),
            reference_code=str(source.get("reference_code") or source.get("source_key") or ""),
            url=url,
            title=str(body.get("title") or body.get("publication_title") or name),
            text=str(body.get("text") or body.get("publication_text") or ""),
            author=str(body.get("author") or body.get("publication_author") or ""),
            campaign=str(body.get("campaign") or ""),
            city=str(body.get("city") or ""),
            district=str(body.get("district") or ""),
            property_type=str(body.get("property_type") or ""),
            target_audience=str(body.get("target_audience") or body.get("target") or "acquisition"),
            format_name=str(body.get("format") or ""),
            language=str(body.get("language") or ""),
            tags=list(body.get("tags") or []),
            notes=str(body.get("notes") or ""),
            network=channel,
        )
        context = self.repository.upsert_source_intelligence_context(
            int(source["id"]),
            network=str(analysis_payload["network"]),
            publication_url=str(analysis_payload["publication_url"]),
            publication_title=str(analysis_payload["publication_title"]),
            publication_text=str(analysis_payload["publication_text"]),
            publication_author=str(analysis_payload["publication_author"]),
            campaign=str(analysis_payload["campaign"]),
            city=str(analysis_payload["city"]),
            district=str(analysis_payload["district"]),
            property_type=str(analysis_payload["property_type"]),
            target_audience=str(analysis_payload["target_audience"]),
            format_name=str(analysis_payload["format"]),
            language=str(analysis_payload["language"]),
            tags=list(analysis_payload["tags_json"]),
            ai_classification=str(analysis_payload["ai_classification"]),
            ai_confidence=float(analysis_payload["ai_confidence"]),
            analysis=dict(analysis_payload["analysis_json"]),
            notes=str(analysis_payload["notes"]),
            whatsapp_link=self.repository._whatsapp_engine().build_link(
                reference_code=str(source.get("reference_code") or source.get("source_key") or ""),
                source_name=str(source.get("name") or ""),
            ),
        )
        import_row = self.repository.create_source_intelligence_import(
            source_id=int(source["id"]),
            source_url=url,
            source_channel=channel,
            payload=body,
            result=context,
            import_status="imported",
        )
        METRICS.increment("source_intelligence_imports_total")
        return {
            "source": sdto.source_dto(source),
            "context": sdto.source_context_dto(context),
            "import": sdto.import_dto(import_row),
            "whatsapp_link": context.get("whatsapp_link"),
        }


class AIAnalysisService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def analyze(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        source_id = body.get("source_id")
        if source_id is None and body.get("reference_code"):
            source = self.repository.resolve_source_intelligence_source(reference_code=str(body["reference_code"]))
            source_id = int(source["id"])
        elif source_id is None and body.get("source_key"):
            source = self.repository.resolve_source_intelligence_source(source_key=str(body["source_key"]))
            source_id = int(source["id"])
        elif source_id is None and body.get("url"):
            imported = ImportSourceService(self.repository).import_url(actor=actor, body=body)
            return {"analysis": imported}
        if source_id is None:
            raise ValueError("source_id or reference_code is required")
        METRICS.increment("source_intelligence_analysis_total")
        return {
            "analysis": self.repository.analyze_source_intelligence(
                source_id=int(source_id),
                url=str(body.get("url") or body.get("publication_url") or ""),
                title=str(body.get("title") or body.get("publication_title") or ""),
                text=str(body.get("text") or body.get("publication_text") or ""),
                author=str(body.get("author") or body.get("publication_author") or ""),
                campaign=str(body.get("campaign") or ""),
                city=str(body.get("city") or ""),
                district=str(body.get("district") or ""),
                property_type=str(body.get("property_type") or ""),
                target_audience=str(body.get("target_audience") or ""),
                format_name=str(body.get("format") or ""),
                language=str(body.get("language") or ""),
                tags=list(body.get("tags") or []),
                notes=str(body.get("notes") or ""),
                network=str(body.get("network") or ""),
            )
        }


class WhatsAppLinkService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def build(self, *, source_id: int) -> dict[str, object]:
        METRICS.increment("source_intelligence_whatsapp_links_total")
        return self.repository.source_intelligence_whatsapp_link(source_id)


class DashboardService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def get(self) -> dict[str, object]:
        METRICS.increment("source_intelligence_dashboard_total")
        return {"dashboard": sdto.dashboard_dto(self.repository.source_intelligence_dashboard())}

    def stats(self) -> dict[str, object]:
        METRICS.increment("source_intelligence_dashboard_total")
        return sdto.stats_dto(self.repository.source_intelligence_stats())


class SourceIntelligenceService:
    def __init__(self, repository, project_service: ProjectService | None = None, policy=None) -> None:
        self.repository = repository
        self.projects = project_service
        self.policy = policy
        self.references = ReferenceCodeService(repository)
        self.sources = SourceService(repository)
        self.contexts = SourceContextService(repository)
        self.imports = ImportSourceService(repository)
        self.analysis = AIAnalysisService(repository)
        self.whatsapp = WhatsAppLinkService(repository)
        self.dashboard = DashboardService(repository)

    def _require_auth(self, actor: dict[str, object] | None) -> None:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")

    def _require_admin(self, actor: dict[str, object]) -> None:
        if self.policy is not None and not self.policy.is_admin(actor):
            raise ProjectPermissionDenied("Admin required")

    def list_sources(self, *, actor: dict[str, object], status: str | None = None, query: str | None = None, limit: int = 50) -> dict[str, object]:
        self._require_auth(actor)
        return self.sources.list(status=status, query=query, limit=limit)

    def get_source(self, *, actor: dict[str, object], source_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return self.sources.get(source_id=source_id)

    def create_source(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return self.sources.create(actor=actor, body=body)

    def update_source(self, *, actor: dict[str, object], source_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return self.sources.update(source_id=source_id, body=body)

    def archive_source(self, *, actor: dict[str, object], source_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return self.sources.archive(source_id=source_id)

    def get_context(self, *, actor: dict[str, object], source_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return self.contexts.get(source_id=source_id)

    def update_context(self, *, actor: dict[str, object], source_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return self.contexts.update(source_id=source_id, body=body)

    def import_source(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return self.imports.import_url(actor=actor, body=body)

    def analyze_source(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return self.analysis.analyze(actor=actor, body=body)

    def build_whatsapp_link(self, *, actor: dict[str, object], source_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return self.whatsapp.build(source_id=source_id)

    def stats(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return self.dashboard.stats()

    def dashboard_view(self, *, actor: dict[str, object], limit: int = 10) -> dict[str, object]:
        self._require_auth(actor)
        payload = self.repository.source_intelligence_dashboard(limit=limit)
        return {"dashboard": sdto.dashboard_dto(payload)}

