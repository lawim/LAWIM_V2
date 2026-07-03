# Release Program S - Knowledge Platform

## 1. Architecture
- Frontend-only knowledge platform packaged under frontend/packages/knowledge.
- Mock-first RAG and search engine to preserve compatibility with frozen backend releases.

## 2. Knowledge Hub
- Knowledge items, categories, sources, metadata, and explorer entry points are available.

## 3. RAG
- RagEngine supports mock and backend modes and returns ranked results with answer context.

## 4. Search
- Hybrid search exposes keyword, filter, and ranking behavior for the knowledge hub.

## 5. Indexation
- Indexer supports indexing, reindexing, and statistics reporting.

## 6. Knowledge Graph
- KnowledgeGraphExplorer builds a lightweight graph representation for topics.

## 7. Taxonomie
- Taxonomy exposes topic groups for documents, CRM, and marketplace sources.

## 8. Citations
- CitationResolver and CitationFormatter provide answer evidence.

## 9. Administration
- KnowledgeExplorer exposes a simple admin-style overview.

## 10. Tests
- Vitest covers knowledge retrieval, RAG, indexing, citations, graph, and SDK behavior.

## 11. Documentation
- Documentation is available under docs/ for platform, RAG, graph, search, citations, and indexing.

## 12. Compatibilité A→R
- The frozen backend and release train remain untouched.

## 13. Préparation LAWIM 2.0
- The platform establishes the knowledge foundation for LAWIM 2.0.

## 14. Préparation LAWIM 3.0
- The SDK and explorer entry points prepare future enterprise knowledge experiences.
