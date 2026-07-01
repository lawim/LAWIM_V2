# RELEASE PROGRAM E — Knowledge Platform • RAG • Expert Knowledge Foundation

**Programme :** RELEASE PROGRAM E  
**Date :** 2026-07-01  
**Branche :** `develop/2.0-intelligent-platform`  
**Tag :** `release-program-e`  
**Schema :** v11  
**Prérequis :** Programs A, B, C, D

---

## 1. Résumé exécutif

RELEASE PROGRAM E transforme LAWIM en **plateforme de connaissances expertes** : domaines immobilier/juridique/financement/technique/administration, gestion documentaire, indexation hybride, fondation RAG et API complète — **sans dépendance LLM obligatoire**.

**476+ tests** passent (objectif 450+).

---

## 2. Architecture

Package : `code/lawim_v2/knowledge_platform/`

```
Expert Knowledge Domains (5 × 40 catégories)
├── Document Management (import MD/HTML/PDF/DOCX/TXT, bulk, versioning)
├── Parsing & Chunking (deterministic)
├── Lexical + Semantic pseudo-embeddings
├── Hybrid Index (expert_knowledge_indexes)
├── RAG Foundation (retrieval, ranking, reranking, citations, context)
├── Workflow (review, approval, publication, archive)
└── Knowledge API (/api/v2/knowledge/*)
```

Préfixe tables : `expert_knowledge_*` (évite collision avec cognition `knowledge_*`).

Intégration : `LawimRepository(KnowledgePlatformRepositoryMixin, AssistantRepositoryMixin, …)`.

---

## 3. Schema v11

23 tables (`schema_v11_ddl.py`) :

- `expert_knowledge_collections`, `expert_knowledge_sources`, `expert_knowledge_categories`, `expert_knowledge_tags`
- `expert_knowledge_documents`, `expert_knowledge_versions`, `expert_knowledge_articles`
- `expert_knowledge_sections`, `expert_knowledge_paragraphs`, `expert_knowledge_chunks`
- `expert_knowledge_citations`, `expert_knowledge_attachments`, `expert_knowledge_references`
- `expert_knowledge_embeddings`, `expert_knowledge_indexes`, `expert_knowledge_relationships`
- `expert_knowledge_feedback`, `expert_knowledge_reviews`, `expert_knowledge_approvals`
- `expert_knowledge_publications`, `expert_knowledge_imports`, `expert_knowledge_exports`
- `expert_knowledge_snapshots`

Compatibilité v10 (assistant) et v9 (cognition) préservée.

---

## 4. Domaines de connaissances

| Domaine | Thématiques |
|---------|-------------|
| Immobilier | achat, vente, location, gestion locative, copropriété, investissement, promotion, construction, rénovation, urbanisme |
| Juridique | contrats, compromis, actes, obligations, responsabilités, procédures, fiscalité, successions, donations, baux |
| Financement | prêts, banques, apport, taux, assurance, garanties, simulations, capacité d'emprunt |
| Technique | construction, matériaux, diagnostics, énergie, maintenance, sécurité, normes |
| Administration | permis, cadastre, impôts, formalités, procédures administratives |

---

## 5. API v2 knowledge (platform)

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/v2/knowledge` | GET | Recherche globale Program A (inchangé) |
| `/api/v2/knowledge/search` | GET | Recherche hybride expert |
| `/api/v2/knowledge/articles` | GET | Liste articles |
| `/api/v2/knowledge/articles/{id}` | GET | Détail article |
| `/api/v2/knowledge/documents` | GET | Liste documents |
| `/api/v2/knowledge/documents/{id}` | GET | Détail document |
| `/api/v2/knowledge/import` | POST | Import unitaire ou massif |
| `/api/v2/knowledge/export` | POST | Export JSON/Markdown |
| `/api/v2/knowledge/categories` | GET | Catégories par domaine |
| `/api/v2/knowledge/tags` | GET | Tags |
| `/api/v2/knowledge/sources` | GET | Sources |
| `/api/v2/knowledge/reindex` | POST | Réindexation |
| `/api/v2/knowledge/rag` | GET/POST | RAG foundation |
| `/api/v2/knowledge/citations` | GET | Citations |
| `/api/v2/knowledge/references` | GET | Références croisées |
| `/api/v2/knowledge/stats` | GET | Statistiques |
| `/api/v2/knowledge/documents/{id}/publish` | POST | Publication |
| `/api/v2/knowledge/documents/{id}/approve` | POST | Validation |

Routes cognition préservées : `/api/v2/knowledge/graph`, `/context`, POST `/refresh`.

---

## 6. Admin UI

Panel **Expert knowledge** dans `static/index.html` / `static/app.js` :

- Statistiques documents/chunks/catégories
- Liste documents récents
- Moteur de recherche expert
- Intégration journey admin/project

---

## 7. Observabilité

Métriques ajoutées :

- `knowledge_documents_total`, `knowledge_chunks_total`, `knowledge_queries_total`
- `knowledge_import_total`, `knowledge_index_total`
- `knowledge_search_latency_ms` (p50/p95)
- `rag_requests_total`, `rag_context_size_total`

---

## 8. Validations

```bash
./scripts/validate-install.sh
./scripts/validate-packaging.sh
./scripts/run-tests.sh
python3 scripts/validate_prisma_manifest.py
python3 scripts/smoke_runtime.py
./platform/validate-platform.sh
./platform/run-postgres-tests.sh
git diff --check
```

---

## 9. Compatibilité

- Programs A–D : intact (schema v7–v10 tables, APIs assistant/cognition/ecosystem)
- Routing knowledge : cognition vs platform via dispatcher unifié
- PostgreSQL + Prisma : migration SQL synchronisée (manifest v11)
