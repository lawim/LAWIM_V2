from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from ..repository_introspection import table_exists
from .constants import EXPORT_FORMATS, IMPORT_FORMATS, KNOWLEDGE_DOMAINS
from .engines import RAGFoundationEngine
from .parsers import parse_document


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


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "article"


class KnowledgePlatformRepositoryMixin:
    def expert_knowledge_tables_present(self) -> bool:
        return table_exists(self, "expert_knowledge_collections")

    def seed_expert_knowledge_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM expert_knowledge_collections") > 0:
            return
        now = _utcnow()
        rag = RAGFoundationEngine()
        with self._transaction() as conn:
            for domain, topics in KNOWLEDGE_DOMAINS.items():
                conn.execute(
                    """
                    INSERT INTO expert_knowledge_collections (
                        collection_key, title, domain, description, status, metadata_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', '{}', ?, ?)
                    """,
                    (f"collection-{domain}", f"Collection {domain.title()}", domain, f"Base expert knowledge {domain}", now, now),
                )
                for topic in topics:
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO expert_knowledge_categories (
                            category_key, domain, title, description, created_at
                        ) VALUES (?, ?, ?, ?, ?)
                        """,
                        (f"{domain}-{topic}", domain, topic.replace("_", " ").title(), f"Catégorie {topic}", now),
                    )
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO expert_knowledge_tags (tag_key, label, domain, created_at)
                        VALUES (?, ?, ?, ?)
                        """,
                        (f"tag-{domain}-{topic}", topic.replace("_", " "), domain, now),
                    )
            conn.execute(
                """
                INSERT INTO expert_knowledge_sources (
                    source_key, title, source_type, publisher, trust_score, metadata_json, created_at
                ) VALUES ('lawim-expert-base', 'LAWIM Expert Knowledge Base', 'internal', 'LAWIM', 90, '{}', ?)
                """,
                (now,),
            )
        samples = (
            ("immobilier", "achat", "Guide d'achat immobilier", "Étapes clés : budget, recherche, visite, offre, compromis, acte authentique."),
            ("juridique", "compromis", "Compromis de vente", "Le compromis engage vendeur et acquéreur sous conditions suspensives."),
            ("financement", "prets", "Prêt immobilier", "Capacité d'emprunt, apport, taux, assurance emprunteur et garanties bancaires."),
            ("technique", "diagnostics", "Diagnostics obligatoires", "DPE, amiante, plomb, électricité, gaz, termites selon bien et date."),
            ("administration", "permis", "Permis de construire", "Dépôt en mairie, délais d'instruction, affichage et recours des tiers."),
        )
        source_id = int(self.one("SELECT id FROM expert_knowledge_sources WHERE source_key='lawim-expert-base'")["id"])
        for domain, topic, title, body in samples:
            self.import_expert_document(
                title=title,
                content=f"# {title}\n\n{body}",
                format_name="markdown",
                domain=domain,
                category_key=f"{domain}-{topic}",
                tags=[f"tag-{domain}-{topic}"],
                author="LAWIM Expert",
                source_id=source_id,
                publish=True,
            )
        self.record_event("expert_knowledge_seeded", {"collections": len(KNOWLEDGE_DOMAINS)})

    def import_expert_document(
        self,
        *,
        title: str,
        content: str,
        format_name: str,
        domain: str,
        category_key: str,
        tags: list[str] | None = None,
        author: str | None = None,
        source_id: int | None = None,
        publish: bool = False,
    ) -> dict[str, object]:
        if format_name not in IMPORT_FORMATS:
            raise ValueError(f"unsupported format: {format_name}")
        now = _utcnow()
        plain, sections = parse_document(format_name, content)
        collection = self.one("SELECT id FROM expert_knowledge_collections WHERE domain = ? LIMIT 1", (domain,))
        if collection is None:
            raise ValueError(f"unknown domain: {domain}")
        document_key = f"doc-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO expert_knowledge_documents (
                    collection_id, source_id, document_key, title, format, status, author,
                    category_key, tags_json, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 'draft', ?, ?, ?, '{}', ?, ?)
                """,
                (collection["id"], source_id, document_key, title, format_name, author, category_key, _json(tags or []), now, now),
            )
            document_id = int(cursor.lastrowid)
            version_key = f"v1-{document_key}"
            content_hash = hashlib.sha256(plain.encode("utf-8")).hexdigest()
            vcur = conn.execute(
                """
                INSERT INTO expert_knowledge_versions (
                    document_id, version_key, version_number, content_hash, status, change_note, content_text, created_at
                ) VALUES (?, ?, 1, ?, 'draft', 'initial import', ?, ?)
                """,
                (document_id, version_key, content_hash, plain, now),
            )
            version_id = int(vcur.lastrowid)
            conn.execute("UPDATE expert_knowledge_documents SET current_version_id = ? WHERE id = ?", (version_id, document_id))
            article_key = f"article-{document_key}"
            slug = _slugify(title)
            acur = conn.execute(
                """
                INSERT INTO expert_knowledge_articles (
                    document_id, article_key, title, slug, status, summary, body_format, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'draft', ?, ?, ?, ?)
                """,
                (document_id, article_key, title, slug, plain[:240], format_name, now, now),
            )
            article_id = int(acur.lastrowid)
            for position, section in enumerate(sections):
                scur = conn.execute(
                    """
                    INSERT INTO expert_knowledge_sections (article_id, section_key, title, position, content, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (article_id, f"sec-{position}", str(section["title"]), position, str(section["content"]), now),
                )
                section_id = int(scur.lastrowid)
                for pidx, paragraph in enumerate(str(section["content"]).split("\n\n")):
                    if paragraph.strip():
                        conn.execute(
                            """
                            INSERT INTO expert_knowledge_paragraphs (section_id, paragraph_key, position, content, created_at)
                            VALUES (?, ?, ?, ?, ?)
                            """,
                            (section_id, f"p-{pidx}", pidx, paragraph.strip(), now),
                        )
        self._index_expert_document(document_id, article_id, plain, domain=domain, category_key=category_key, tags=tags or [], title=title)
        if publish:
            self.publish_expert_document(document_id)
        return self.get_expert_document(document_id)

    def bulk_import_expert_documents(self, records: list[dict[str, object]]) -> dict[str, object]:
        imported: list[dict[str, object]] = []
        errors: list[dict[str, object]] = []
        for record in records:
            try:
                imported.append(
                    self.import_expert_document(
                        title=str(record["title"]),
                        content=str(record["content"]),
                        format_name=str(record.get("format") or "markdown"),
                        domain=str(record["domain"]),
                        category_key=str(record["category_key"]),
                        tags=list(record.get("tags") or []),
                        author=str(record.get("author") or "import"),
                        publish=bool(record.get("publish")),
                    )
                )
            except (ValueError, KeyError, TypeError) as exc:
                errors.append({"title": record.get("title"), "error": str(exc)})
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO expert_knowledge_imports (import_key, format, status, source_filename, records_count, error_json, created_at)
                VALUES (?, 'bulk', ?, 'bulk.json', ?, ?, ?)
                """,
                (f"import-{now}", "completed" if not errors else "partial", len(imported), _json(errors), now),
            )
        return {"imported": len(imported), "errors": errors, "documents": imported}

    def _index_expert_document(
        self,
        document_id: int,
        article_id: int,
        plain: str,
        *,
        domain: str,
        category_key: str,
        tags: list[str],
        title: str,
    ) -> None:
        rag = RAGFoundationEngine()
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute("DELETE FROM expert_knowledge_chunks WHERE document_id = ?", (document_id,))
            conn.execute("DELETE FROM expert_knowledge_embeddings WHERE chunk_id IN (SELECT id FROM expert_knowledge_chunks WHERE document_id = ?)", (document_id,))
        for idx, chunk in enumerate(rag.chunker.chunk(plain)):
            chunk_key = f"chunk-{document_id}-{idx}"
            lexical = rag.lexical.build_lexical_index(chunk)
            with self._transaction() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO expert_knowledge_chunks (
                        document_id, article_id, chunk_key, content, token_estimate, index_lexical,
                        metadata_json, freshness_score, confidence_score, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 85, 80, ?)
                    """,
                    (document_id, article_id, chunk_key, chunk, len(chunk.split()), lexical, _json({"domain": domain, "tags": tags}), now),
                )
                chunk_id = int(cursor.lastrowid)
                emb = rag.deterministic_embedding_record(chunk_id, chunk)
                conn.execute(
                    """
                    INSERT INTO expert_knowledge_embeddings (chunk_id, model_key, vector_json, dimensions, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (chunk_id, emb["model_key"], _json(emb["vector_json"]), emb["dimensions"], now),
                )
                for cite in rag.citations.build_citations(chunk, source_label=title):
                    conn.execute(
                        """
                        INSERT INTO expert_knowledge_citations (chunk_id, citation_key, label, source_ref, quote, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (chunk_id, f"cite-{chunk_id}", cite["label"], cite["source_ref"], cite["quote"], now),
                    )
        token_count = len(rag.lexical.tokenize(plain))
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO expert_knowledge_indexes (
                    document_id, index_key, index_type, status, token_count, metadata_json, created_at, updated_at
                ) VALUES (?, ?, 'hybrid', 'active', ?, ?, ?, ?)
                """,
                (document_id, f"idx-{document_id}", token_count, _json({"domain": domain, "category_key": category_key}), now, now),
            )

    def reindex_expert_knowledge(self, document_id: int | None = None) -> dict[str, object]:
        if document_id is not None:
            doc = self.get_expert_document(document_id)
            version = self.one("SELECT content_text FROM expert_knowledge_versions WHERE document_id = ? ORDER BY version_number DESC LIMIT 1", (document_id,))
            article = self.one("SELECT id FROM expert_knowledge_articles WHERE document_id = ? LIMIT 1", (document_id,))
            self._index_expert_document(
                document_id,
                int(article["id"]),
                str(version["content_text"]),
                domain=str(self.one("SELECT domain FROM expert_knowledge_collections WHERE id = ?", (doc["collection_id"],))["domain"]),
                category_key=str(doc.get("category_key") or ""),
                tags=_parse_json(str(doc.get("tags_json"))) or [],
                title=str(doc["title"]),
            )
            count = 1
        else:
            count = 0
            for row in self.all("SELECT id FROM expert_knowledge_documents"):
                self.reindex_expert_knowledge(int(row["id"]))
                count += 1
        return {"reindexed_documents": count}

    def search_expert_knowledge(
        self,
        *,
        query: str,
        domain: str | None = None,
        category: str | None = None,
        tag: str | None = None,
        author: str | None = None,
        project_id: int | None = None,
        partner_id: int | None = None,
        service_id: int | None = None,
        limit: int = 20,
    ) -> list[dict[str, object]]:
        rag = RAGFoundationEngine()
        rows = self.all(
            """
            SELECT c.id, c.content, c.chunk_key, c.freshness_score, c.confidence_score, c.metadata_json,
                   d.document_key, d.title, d.author, d.category_key, col.domain
            FROM expert_knowledge_chunks c
            JOIN expert_knowledge_documents d ON d.id = c.document_id
            JOIN expert_knowledge_collections col ON col.id = d.collection_id
            WHERE d.status IN ('published', 'approved', 'draft')
            """
        )
        chunks = []
        for row in rows:
            meta = _parse_json(str(row.get("metadata_json"))) or {}
            if domain and row.get("domain") != domain:
                continue
            if category and row.get("category_key") != category:
                continue
            if tag and tag not in (meta.get("tags") or []):
                continue
            if author and str(row.get("author") or "").lower() != author.lower():
                continue
            chunks.append(
                {
                    "id": row["id"],
                    "content": row["content"],
                    "document_key": row["document_key"],
                    "title": row["title"],
                    "domain": row["domain"],
                    "category_key": row.get("category_key"),
                    "tags": meta.get("tags") or [],
                    "freshness_score": row.get("freshness_score"),
                    "confidence_score": row.get("confidence_score"),
                }
            )
        if project_id and hasattr(self, "get_project"):
            project = self.get_project(project_id)
            query = f"{query} {project.get('location_city', '')} {project.get('project_type', '')}".strip()
        if partner_id:
            query = f"{query} partner {partner_id}"
        if service_id:
            query = f"{query} service {service_id}"
        retrieved = rag.retrieve(query=query, chunks=chunks, limit=limit, domain=domain, category=category, tag=tag)
        results: list[dict[str, object]] = []
        for item in retrieved:
            results.append(
                {
                    "result_type": "chunk",
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "score": item.get("score"),
                    "snippet": str(item.get("content", ""))[:200],
                    "domain": item.get("domain"),
                    "category_key": item.get("category_key"),
                }
            )
        return results

    def expert_rag_query(
        self,
        query: str,
        *,
        domain: str | None = None,
        category: str | None = None,
        tag: str | None = None,
        limit: int = 8,
        project_id: int | None = None,
    ) -> dict[str, object]:
        rag_engine = RAGFoundationEngine()
        chunks = self.search_expert_knowledge(
            query=query,
            domain=domain,
            category=category,
            tag=tag,
            project_id=project_id,
            limit=limit,
        )
        chunk_rows = [{"content": c.get("snippet"), "title": c.get("title"), "score": c.get("score")} for c in chunks]
        context = rag_engine.build_context(chunk_rows)
        return {"query": query, "chunks": chunks, "context": context, "citations": context.get("citations", [])}

    def list_expert_articles(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all("SELECT * FROM expert_knowledge_articles WHERE status = ? ORDER BY id DESC LIMIT ?", (status, limit))
        else:
            rows = self.all("SELECT * FROM expert_knowledge_articles ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def get_expert_article(self, article_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM expert_knowledge_articles WHERE id = ?", (article_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("article not found")
        sections = self.all("SELECT * FROM expert_knowledge_sections WHERE article_id = ? ORDER BY position ASC", (article_id,))
        payload = dict(row)
        payload["sections"] = [dict(s) for s in sections]
        return payload

    def list_expert_documents(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM expert_knowledge_documents WHERE status = ? ORDER BY id DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT * FROM expert_knowledge_documents ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def get_expert_document(self, document_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM expert_knowledge_documents WHERE id = ?", (document_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("document not found")
        return dict(row)

    def list_expert_categories(self, domain: str | None = None) -> list[dict[str, object]]:
        if domain:
            rows = self.all("SELECT * FROM expert_knowledge_categories WHERE domain = ? ORDER BY title ASC", (domain,))
        else:
            rows = self.all("SELECT * FROM expert_knowledge_categories ORDER BY domain, title ASC")
        return [dict(row) for row in rows]

    def list_expert_tags(self, domain: str | None = None) -> list[dict[str, object]]:
        if domain:
            rows = self.all("SELECT * FROM expert_knowledge_tags WHERE domain = ? ORDER BY label ASC", (domain,))
        else:
            rows = self.all("SELECT * FROM expert_knowledge_tags ORDER BY domain, label ASC")
        return [dict(row) for row in rows]

    def list_expert_sources(self) -> list[dict[str, object]]:
        return [dict(row) for row in self.all("SELECT * FROM expert_knowledge_sources ORDER BY id ASC")]

    def list_expert_citations(self, *, document_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if document_id is not None:
            rows = self.all(
                """
                SELECT cit.* FROM expert_knowledge_citations cit
                JOIN expert_knowledge_chunks c ON c.id = cit.chunk_id
                WHERE c.document_id = ? ORDER BY cit.id DESC LIMIT ?
                """,
                (document_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM expert_knowledge_citations ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def list_expert_references(self, document_id: int | None = None) -> list[dict[str, object]]:
        if document_id is not None:
            rows = self.all(
                "SELECT * FROM expert_knowledge_references WHERE from_document_id = ? OR to_document_id = ?",
                (document_id, document_id),
            )
        else:
            rows = self.all("SELECT * FROM expert_knowledge_references ORDER BY id DESC LIMIT 100")
        return [dict(row) for row in rows]

    def publish_expert_document(self, document_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute("UPDATE expert_knowledge_documents SET status = 'published', updated_at = ? WHERE id = ?", (now, document_id))
            conn.execute("UPDATE expert_knowledge_articles SET status = 'published', published_at = ?, updated_at = ? WHERE document_id = ?", (now, now, document_id))
            conn.execute(
                """
                INSERT OR REPLACE INTO expert_knowledge_publications (document_id, publication_key, status, published_at, created_at)
                VALUES (?, ?, 'published', ?, ?)
                """,
                (document_id, f"pub-{document_id}", now, now),
            )
        return self.get_expert_document(document_id)

    def unpublish_expert_document(self, document_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute("UPDATE expert_knowledge_documents SET status = 'draft', updated_at = ? WHERE id = ?", (now, document_id))
            conn.execute("UPDATE expert_knowledge_articles SET status = 'draft', updated_at = ? WHERE document_id = ?", (now, document_id))
            conn.execute(
                "UPDATE expert_knowledge_publications SET status = 'unpublished', unpublished_at = ? WHERE document_id = ?",
                (now, document_id),
            )
        return self.get_expert_document(document_id)

    def approve_expert_document(self, document_id: int, approver_id: int | None = None) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute("UPDATE expert_knowledge_documents SET status = 'approved', updated_at = ? WHERE id = ?", (now, document_id))
            conn.execute(
                "INSERT INTO expert_knowledge_approvals (document_id, approver_id, status, note, created_at) VALUES (?, ?, 'approved', 'approved', ?)",
                (document_id, approver_id, now),
            )
        return self.get_expert_document(document_id)

    def review_expert_document(self, document_id: int, reviewer_id: int | None, note: str = "") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "INSERT INTO expert_knowledge_reviews (document_id, reviewer_id, status, note, created_at) VALUES (?, ?, 'reviewed', ?, ?)",
                (document_id, reviewer_id, note, now),
            )
        return self.get_expert_document(document_id)

    def export_expert_knowledge(self, format_name: str = "json") -> dict[str, object]:
        if format_name not in EXPORT_FORMATS:
            raise ValueError(f"unsupported export format: {format_name}")
        docs = self.list_expert_documents(limit=500)
        articles = self.list_expert_articles(limit=500)
        payload = {"documents": docs, "articles": articles}
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO expert_knowledge_exports (export_key, format, status, destination, records_count, created_at)
                VALUES (?, ?, 'completed', 'api', ?, ?)
                """,
                (f"export-{now}", format_name, len(docs) + len(articles), now),
            )
        if format_name == "json":
            export_body: str | dict[str, object] = payload
        elif format_name == "markdown":
            export_body = "\n\n".join(f"# {a['title']}\n{a.get('summary', '')}" for a in articles)
        else:
            export_body = str(payload)
        return {"format": format_name, "records": len(docs) + len(articles), "payload": export_body}

    def expert_knowledge_stats(self) -> dict[str, object]:
        return {
            "documents": self.scalar("SELECT COUNT(*) FROM expert_knowledge_documents"),
            "chunks": self.scalar("SELECT COUNT(*) FROM expert_knowledge_chunks"),
            "articles": self.scalar("SELECT COUNT(*) FROM expert_knowledge_articles"),
            "index_size": self.scalar("SELECT COALESCE(SUM(token_count), 0) FROM expert_knowledge_indexes"),
            "categories": self.scalar("SELECT COUNT(*) FROM expert_knowledge_categories"),
            "tags": self.scalar("SELECT COUNT(*) FROM expert_knowledge_tags"),
        }

    def snapshot_expert_knowledge(self) -> dict[str, object]:
        stats = self.expert_knowledge_stats()
        now = _utcnow()
        key = f"snapshot-{now}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO expert_knowledge_snapshots (snapshot_key, scope, payload_json, record_count, created_at)
                VALUES (?, 'global', ?, ?, ?)
                """,
                (key, _json(stats), int(stats["documents"]), now),
            )
        return {"snapshot_key": key, "stats": stats}
