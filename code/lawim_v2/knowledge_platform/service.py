from __future__ import annotations

import time

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as kdto


class KnowledgePlatformService:
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

    def search(
        self,
        *,
        actor: dict[str, object],
        query: str,
        domain: str | None = None,
        category: str | None = None,
        tag: str | None = None,
        author: str | None = None,
        project_id: int | None = None,
        partner_id: int | None = None,
        service_id: int | None = None,
        limit: int = 20,
    ) -> dict[str, object]:
        self._require_auth(actor)
        if project_id is not None:
            self.projects._require_access(actor, project_id)
        started = time.perf_counter()
        results = self.repository.search_expert_knowledge(
            query=query,
            domain=domain,
            category=category,
            tag=tag,
            author=author,
            project_id=project_id,
            partner_id=partner_id,
            service_id=service_id,
            limit=limit,
        )
        latency_ms = (time.perf_counter() - started) * 1000
        METRICS.record_knowledge_search(latency_ms=latency_ms)
        return {"results": [kdto.search_result_dto(r) for r in results], "query": query}

    def list_articles(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"articles": [kdto.article_dto(r) for r in self.repository.list_expert_articles(status=status)]}

    def get_article(self, *, actor: dict[str, object], article_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"article": self.repository.get_expert_article(article_id)}

    def list_documents(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("knowledge_documents")
        return {"documents": [kdto.document_dto(r) for r in self.repository.list_expert_documents(status=status)]}

    def get_document(self, *, actor: dict[str, object], document_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"document": kdto.document_dto(self.repository.get_expert_document(document_id))}

    def import_document(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        doc = self.repository.import_expert_document(
            title=str(body["title"]),
            content=str(body["content"]),
            format_name=str(body.get("format") or "markdown"),
            domain=str(body["domain"]),
            category_key=str(body["category_key"]),
            tags=list(body.get("tags") or []),
            author=str(body.get("author") or str(actor.get("full_name") or "admin")),
            publish=bool(body.get("publish")),
        )
        METRICS.increment("knowledge_import")
        return {"document": kdto.document_dto(doc)}

    def bulk_import(self, *, actor: dict[str, object], records: list[dict[str, object]]) -> dict[str, object]:
        self._require_admin(actor)
        payload = self.repository.bulk_import_expert_documents(records)
        METRICS.increment("knowledge_import")
        return payload

    def export(self, *, actor: dict[str, object], format_name: str = "json") -> dict[str, object]:
        self._require_admin(actor)
        return self.repository.export_expert_knowledge(format_name)

    def list_categories(self, *, actor: dict[str, object], domain: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"categories": [kdto.category_dto(r) for r in self.repository.list_expert_categories(domain)]}

    def list_tags(self, *, actor: dict[str, object], domain: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"tags": [kdto.tag_dto(r) for r in self.repository.list_expert_tags(domain)]}

    def list_sources(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return {"sources": [kdto.source_dto(r) for r in self.repository.list_expert_sources()]}

    def reindex(self, *, actor: dict[str, object], document_id: int | None = None) -> dict[str, object]:
        self._require_admin(actor)
        payload = self.repository.reindex_expert_knowledge(document_id)
        METRICS.increment("knowledge_index")
        return payload

    def rag(self, *, actor: dict[str, object], query: str, **filters: object) -> dict[str, object]:
        self._require_auth(actor)
        payload = self.repository.expert_rag_query(query, **filters)
        METRICS.record_rag_request(context_size=int(payload.get("context", {}).get("context_size", 0)))
        return kdto.rag_dto(payload)

    def list_citations(self, *, actor: dict[str, object], document_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"citations": [kdto.citation_dto(r) for r in self.repository.list_expert_citations(document_id=document_id)]}

    def list_references(self, *, actor: dict[str, object], document_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"references": [kdto.reference_dto(r) for r in self.repository.list_expert_references(document_id)]}

    def stats(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return {"stats": self.repository.expert_knowledge_stats()}

    def publish(self, *, actor: dict[str, object], document_id: int) -> dict[str, object]:
        self._require_admin(actor)
        return {"document": kdto.document_dto(self.repository.publish_expert_document(document_id))}

    def unpublish(self, *, actor: dict[str, object], document_id: int) -> dict[str, object]:
        self._require_admin(actor)
        return {"document": kdto.document_dto(self.repository.unpublish_expert_document(document_id))}

    def approve(self, *, actor: dict[str, object], document_id: int) -> dict[str, object]:
        self._require_admin(actor)
        approver_id = int(actor["id"]) if actor.get("id") is not None else None
        return {"document": kdto.document_dto(self.repository.approve_expert_document(document_id, approver_id))}
