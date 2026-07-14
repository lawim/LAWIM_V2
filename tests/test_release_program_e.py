from __future__ import annotations

import sqlite3
import tempfile
from http import HTTPStatus
from pathlib import Path

from lawim_v2.knowledge_platform.constants import (
    DOCUMENT_STATUSES,
    EXPORT_FORMATS,
    IMPORT_FORMATS,
    INDEX_TYPES,
    KNOWLEDGE_DOMAINS,
    RELATION_TYPES,
)
from lawim_v2.knowledge_platform.engines import (
    ChunkingEngine,
    CitationEngine,
    LexicalIndexEngine,
    RAGFoundationEngine,
    RankingEngine,
    SemanticIndexEngine,
)
from lawim_v2.knowledge_platform.parsers import parse_document, parse_html, parse_markdown, parse_txt
from lawim_v2.knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations, migration_strategy_profile

from tests.lawim_harness import LawimTestHarness


class ReleaseProgramEPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v11(self) -> None:
        self.assertEqual(self.repository.schema_version(), 19)
        self.assertEqual(APPLICATION_SCHEMA_VERSION, 19)

    def test_expert_knowledge_tables_present(self) -> None:
        self.assertTrue(self.repository.expert_knowledge_tables_present())

    def test_all_v11_tables_exist(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V11_TABLE_NAMES:
            self.assertIn(table, names)

    def test_assistant_v10_tables_are_decommissioned(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertNotIn("assistant_sessions", names)
        self.assertNotIn("assistant_agents", names)

    def test_expert_knowledge_catalog_seeded(self) -> None:
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM expert_knowledge_collections"), 5)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM expert_knowledge_documents"), 5)

    def test_v10_to_v11_legacy_migration(self) -> None:
        db_path = Path(tempfile.mkdtemp()) / "v10.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        from lawim_v2.knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES as V11

        for table in V11:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='10' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("expert_knowledge_documents", names)
        self.assertNotIn("assistant_sessions", names)


class ReleaseProgramEConstantsTests(LawimTestHarness):
    def test_knowledge_domains_immobilier(self) -> None:
        self.assertIn("achat", KNOWLEDGE_DOMAINS["immobilier"])

    def test_knowledge_domains_juridique(self) -> None:
        self.assertIn("compromis", KNOWLEDGE_DOMAINS["juridique"])

    def test_knowledge_domains_financement(self) -> None:
        self.assertIn("prets", KNOWLEDGE_DOMAINS["financement"])

    def test_knowledge_domains_technique(self) -> None:
        self.assertIn("diagnostics", KNOWLEDGE_DOMAINS["technique"])

    def test_knowledge_domains_administration(self) -> None:
        self.assertIn("permis", KNOWLEDGE_DOMAINS["administration"])

    def test_import_formats(self) -> None:
        self.assertIn("markdown", IMPORT_FORMATS)
        self.assertIn("pdf", IMPORT_FORMATS)
        self.assertIn("docx", IMPORT_FORMATS)

    def test_export_formats(self) -> None:
        self.assertIn("json", EXPORT_FORMATS)
        self.assertIn("markdown", EXPORT_FORMATS)

    def test_document_statuses(self) -> None:
        self.assertIn("published", DOCUMENT_STATUSES)

    def test_index_types(self) -> None:
        self.assertIn("hybrid", INDEX_TYPES)

    def test_relation_types(self) -> None:
        self.assertIn("references", RELATION_TYPES)


class ReleaseProgramEParserTests(LawimTestHarness):
    def test_parse_markdown_sections(self) -> None:
        plain, sections = parse_markdown("# Title\n\nBody paragraph.")
        self.assertIn("Title", plain)
        self.assertGreaterEqual(len(sections), 1)

    def test_parse_html_strips_tags(self) -> None:
        plain, sections = parse_html("<p>Hello <b>world</b></p>")
        self.assertIn("Hello world", plain)

    def test_parse_txt_paragraphs(self) -> None:
        plain, sections = parse_txt("First.\n\nSecond.")
        self.assertEqual(len(sections), 2)

    def test_parse_document_markdown(self) -> None:
        plain, sections = parse_document("markdown", "# Guide\n\nContent.")
        self.assertIn("Guide", plain)

    def test_parse_document_html(self) -> None:
        plain, _ = parse_document("html", "<h1>Doc</h1>")
        self.assertIn("Doc", plain)

    def test_parse_document_txt(self) -> None:
        plain, _ = parse_document("txt", "Simple text.")
        self.assertEqual(plain, "Simple text.")

    def test_parse_document_pdf(self) -> None:
        plain, _ = parse_document("pdf", "PDF extracted content")
        self.assertIn("PDF", plain)

    def test_parse_document_docx(self) -> None:
        plain, _ = parse_document("docx", "<w:t>Word content</w:t>")
        self.assertIn("Word", plain)


class ReleaseProgramEEngineTests(LawimTestHarness):
    def test_chunking_engine(self) -> None:
        chunks = ChunkingEngine().chunk("word " * 200)
        self.assertGreater(len(chunks), 1)

    def test_lexical_normalize(self) -> None:
        normalized = LexicalIndexEngine().normalize("  Achats   Immobilier!  ")
        self.assertIn("achats", normalized)

    def test_lexical_tokenize(self) -> None:
        tokens = LexicalIndexEngine().tokenize("achat immobilier Douala")
        self.assertIn("achat", tokens)

    def test_semantic_embed_dimensions(self) -> None:
        vector = SemanticIndexEngine().embed("prêt immobilier")
        self.assertEqual(len(vector), 16)

    def test_ranking_lexical_score(self) -> None:
        score = RankingEngine().score_lexical("achat Douala", "guide achat immobilier Douala")
        self.assertGreater(score, 0)

    def test_ranking_rerank(self) -> None:
        rows = RankingEngine().rerank([{"score": 10, "freshness_score": 80, "confidence_score": 70}], query="x")
        self.assertGreater(rows[0]["score"], 10)

    def test_citation_engine(self) -> None:
        cites = CitationEngine().build_citations("Excerpt content for citation.", source_label="Guide")
        self.assertEqual(cites[0]["label"], "Guide")

    def test_rag_retrieve(self) -> None:
        engine = RAGFoundationEngine()
        chunks = [{"content": "compromis vente immobilier", "title": "Compromis", "domain": "juridique"}]
        results = engine.retrieve(query="compromis", chunks=chunks)
        self.assertGreaterEqual(len(results), 1)

    def test_rag_build_context(self) -> None:
        ctx = RAGFoundationEngine().build_context([{"content": "budget achat", "title": "Budget"}])
        self.assertGreater(ctx["context_size"], 0)
        self.assertIn("citations", ctx)

    def test_rag_empty_query(self) -> None:
        self.assertEqual(RAGFoundationEngine().ranking.score_lexical("", "text"), 0)

    def test_deterministic_embedding(self) -> None:
        record = RAGFoundationEngine().deterministic_embedding_record(1, "test content")
        self.assertEqual(record["dimensions"], 16)


class ReleaseProgramERepositoryTests(LawimTestHarness):
    def test_import_expert_document(self) -> None:
        doc = self.repository.import_expert_document(
            title="Test import",
            content="# Test\n\nContenu expert.",
            format_name="markdown",
            domain="immobilier",
            category_key="immobilier-achat",
            tags=["tag-immobilier-achat"],
            publish=True,
        )
        self.assertEqual(doc["status"], "published")

    def test_bulk_import_expert_documents(self) -> None:
        payload = self.repository.bulk_import_expert_documents(
            [
                {
                    "title": "Bulk A",
                    "content": "Content A",
                    "domain": "juridique",
                    "category_key": "juridique-contrats",
                },
                {
                    "title": "Bulk B",
                    "content": "Content B",
                    "domain": "financement",
                    "category_key": "financement-prets",
                },
            ]
        )
        self.assertEqual(payload["imported"], 2)

    def test_search_expert_knowledge(self) -> None:
        results = self.repository.search_expert_knowledge(query="compromis vente")
        self.assertGreaterEqual(len(results), 1)

    def test_search_by_domain(self) -> None:
        results = self.repository.search_expert_knowledge(query="prêt", domain="financement")
        for row in results:
            self.assertEqual(row.get("domain"), "financement")

    def test_search_by_category(self) -> None:
        results = self.repository.search_expert_knowledge(query="diagnostic", category="technique-diagnostics")
        self.assertIsInstance(results, list)

    def test_expert_rag_query(self) -> None:
        payload = self.repository.expert_rag_query("permis construire", domain="administration")
        self.assertIn("context", payload)
        self.assertIn("chunks", payload)

    def test_list_expert_articles(self) -> None:
        articles = self.repository.list_expert_articles()
        self.assertGreaterEqual(len(articles), 5)

    def test_get_expert_article(self) -> None:
        article_id = int(self.repository.one("SELECT id FROM expert_knowledge_articles LIMIT 1")["id"])
        article = self.repository.get_expert_article(article_id)
        self.assertIn("sections", article)

    def test_list_expert_documents(self) -> None:
        docs = self.repository.list_expert_documents()
        self.assertGreaterEqual(len(docs), 5)

    def test_get_expert_document(self) -> None:
        doc_id = int(self.repository.one("SELECT id FROM expert_knowledge_documents LIMIT 1")["id"])
        doc = self.repository.get_expert_document(doc_id)
        self.assertIn("document_key", doc)

    def test_list_expert_categories(self) -> None:
        cats = self.repository.list_expert_categories(domain="immobilier")
        self.assertGreaterEqual(len(cats), 5)

    def test_list_expert_tags(self) -> None:
        tags = self.repository.list_expert_tags(domain="juridique")
        self.assertGreaterEqual(len(tags), 5)

    def test_list_expert_sources(self) -> None:
        sources = self.repository.list_expert_sources()
        self.assertGreaterEqual(len(sources), 1)

    def test_list_expert_citations(self) -> None:
        cites = self.repository.list_expert_citations()
        self.assertGreaterEqual(len(cites), 1)

    def test_reindex_expert_knowledge(self) -> None:
        doc_id = int(self.repository.one("SELECT id FROM expert_knowledge_documents LIMIT 1")["id"])
        payload = self.repository.reindex_expert_knowledge(doc_id)
        self.assertEqual(payload["reindexed_documents"], 1)

    def test_reindex_all_expert_knowledge(self) -> None:
        payload = self.repository.reindex_expert_knowledge()
        self.assertGreaterEqual(payload["reindexed_documents"], 1)

    def test_publish_expert_document(self) -> None:
        doc = self.repository.import_expert_document(
            title="Draft doc",
            content="Draft content",
            format_name="txt",
            domain="technique",
            category_key="technique-normes",
        )
        published = self.repository.publish_expert_document(int(doc["id"]))
        self.assertEqual(published["status"], "published")

    def test_unpublish_expert_document(self) -> None:
        doc_id = int(self.repository.one("SELECT id FROM expert_knowledge_documents WHERE status='published' LIMIT 1")["id"])
        unpublished = self.repository.unpublish_expert_document(doc_id)
        self.assertEqual(unpublished["status"], "draft")

    def test_approve_expert_document(self) -> None:
        doc = self.repository.import_expert_document(
            title="Review doc",
            content="Review content",
            format_name="txt",
            domain="administration",
            category_key="administration-cadastre",
        )
        approved = self.repository.approve_expert_document(int(doc["id"]), approver_id=1)
        self.assertEqual(approved["status"], "approved")

    def test_export_expert_knowledge_json(self) -> None:
        payload = self.repository.export_expert_knowledge("json")
        self.assertEqual(payload["format"], "json")
        self.assertGreater(payload["records"], 0)

    def test_export_expert_knowledge_markdown(self) -> None:
        payload = self.repository.export_expert_knowledge("markdown")
        self.assertEqual(payload["format"], "markdown")

    def test_expert_knowledge_stats(self) -> None:
        stats = self.repository.expert_knowledge_stats()
        self.assertGreaterEqual(stats["documents"], 5)
        self.assertGreaterEqual(stats["chunks"], 5)

    def test_snapshot_expert_knowledge(self) -> None:
        snap = self.repository.snapshot_expert_knowledge()
        self.assertIn("snapshot_key", snap)


class ReleaseProgramEApiTests(LawimTestHarness):
    def test_knowledge_stats_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/stats", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("stats", response.body_json())

    def test_knowledge_documents_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/documents", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["documents"]), 5)

    def test_knowledge_document_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        doc_id = int(self.invoke("/api/v2/knowledge/documents", token=token).body_json()["documents"][0]["id"])
        response = self.invoke(f"/api/v2/knowledge/documents/{doc_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_articles_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/articles", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_article_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        article_id = int(self.invoke("/api/v2/knowledge/articles", token=token).body_json()["articles"][0]["id"])
        response = self.invoke(f"/api/v2/knowledge/articles/{article_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_categories_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/categories?domain=immobilier", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_tags_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/tags", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_sources_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/sources", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_search_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/search?q=compromis", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("results", response.body_json())

    def test_knowledge_rag_get_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/rag?q=achat+immobilier", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_rag_post_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/knowledge/rag",
            method="POST",
            token=token,
            body={"query": "diagnostics obligatoires"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_knowledge_citations_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/citations", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_references_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/references", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_import_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/knowledge/import",
            method="POST",
            token=token,
            body={
                "title": "API Import",
                "content": "# API\n\nImported via API.",
                "format": "markdown",
                "domain": "immobilier",
                "category_key": "immobilier-vente",
                "publish": True,
            },
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_knowledge_bulk_import_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/knowledge/import",
            method="POST",
            token=token,
            body={
                "records": [
                    {
                        "title": "Bulk API 1",
                        "content": "Content 1",
                        "domain": "juridique",
                        "category_key": "juridique-baux",
                    }
                ]
            },
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_knowledge_export_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/knowledge/export", method="POST", token=token, body={"format": "json"})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_reindex_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/knowledge/reindex", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_publish_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        doc_id = int(self.invoke("/api/v2/knowledge/documents", token=token).body_json()["documents"][0]["id"])
        response = self.invoke(f"/api/v2/knowledge/documents/{doc_id}/publish", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_approve_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        created = self.invoke(
            "/api/v2/knowledge/import",
            method="POST",
            token=token,
            body={
                "title": "Approve me",
                "content": "Content",
                "format": "txt",
                "domain": "financement",
                "category_key": "financement-taux",
            },
        )
        doc_id = int(created.body_json()["document"]["id"])
        response = self.invoke(f"/api/v2/knowledge/documents/{doc_id}/approve", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_knowledge_root_global_search_still_works(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/knowledge?q=budget", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_cognition_graph_route_preserved(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])
        response = self.invoke(f"/api/v2/knowledge/graph?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)


class ReleaseProgramEUiTests(LawimTestHarness):
    def test_index_has_expert_knowledge_section(self) -> None:
        html = self.invoke("/")
        self.assertIn("Expert knowledge", html.body_text())

    def test_app_js_references_knowledge_api(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/knowledge/search", js.body_text())
        self.assertIn("refreshKnowledgeAdmin", js.body_text())


class ReleaseProgramEHealthTests(LawimTestHarness):
    def test_health_schema_v11(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 19)

    def test_migration_strategy_v11(self) -> None:
        self.assertEqual(migration_strategy_profile()["schema_version"], 19)

    def test_metrics_include_knowledge_counters(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/knowledge/search?q=achat", token=token)
        admin = self.login(email="admin@lawim.local")
        metrics = self.invoke("/api/metrics", token=admin)
        snapshot = metrics.body_json()["metrics"]
        self.assertGreaterEqual(snapshot.get("knowledge_queries_total", 0), 1)


class ReleaseProgramEV11TableTests(LawimTestHarness):
    def _table_names(self) -> set[str]:
        return {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}

    def test_v11_table_collections(self) -> None:
        self.assertIn("expert_knowledge_collections", self._table_names())

    def test_v11_table_documents(self) -> None:
        self.assertIn("expert_knowledge_documents", self._table_names())

    def test_v11_table_chunks(self) -> None:
        self.assertIn("expert_knowledge_chunks", self._table_names())

    def test_v11_table_embeddings(self) -> None:
        self.assertIn("expert_knowledge_embeddings", self._table_names())

    def test_v11_table_indexes(self) -> None:
        self.assertIn("expert_knowledge_indexes", self._table_names())

    def test_v11_table_citations(self) -> None:
        self.assertIn("expert_knowledge_citations", self._table_names())

    def test_v11_table_publications(self) -> None:
        self.assertIn("expert_knowledge_publications", self._table_names())

    def test_v11_table_imports(self) -> None:
        self.assertIn("expert_knowledge_imports", self._table_names())

    def test_v11_table_exports(self) -> None:
        self.assertIn("expert_knowledge_exports", self._table_names())

    def test_v11_table_snapshots(self) -> None:
        self.assertIn("expert_knowledge_snapshots", self._table_names())


class ReleaseProgramEDomainCoverageTests(LawimTestHarness):
    def test_all_domains_have_categories(self) -> None:
        for domain in KNOWLEDGE_DOMAINS:
            count = self.repository.scalar(
                "SELECT COUNT(*) FROM expert_knowledge_categories WHERE domain = ?",
                (domain,),
            )
            self.assertGreaterEqual(count, len(KNOWLEDGE_DOMAINS[domain]))

    def test_seeded_sample_covers_domains(self) -> None:
        domains = {
            row["domain"]
            for row in self.repository.all(
                """
                SELECT col.domain FROM expert_knowledge_documents d
                JOIN expert_knowledge_collections col ON col.id = d.collection_id
                """
            )
        }
        for expected in ("immobilier", "juridique", "financement", "technique", "administration"):
            self.assertIn(expected, domains)
