import { describe, expect, it } from 'vitest';
import {
  CitationResolver,
  createKnowledgeItem,
  createMockKnowledgeHub,
  HybridSearch,
  Indexer,
  KnowledgeService,
  RagEngine,
  KnowledgeSdk
} from '@knowledge';

describe('KnowledgeService', () => {
  it('indexes and retrieves knowledge relevant to a query', async () => {
    const service = new KnowledgeService();
    const document = createKnowledgeItem({
      id: 'doc-1',
      title: 'Luxury villa policy',
      summary: 'Guidelines for luxury villa listings',
      content: 'Luxury villas require premium staging, local market context, and a meticulous compliance checklist.'
    });

    service.addDocument(document);
    const results = await service.search('luxury villa staging');

    expect(results.length).toBeGreaterThan(0);
    expect(results[0].item.title).toBe('Luxury villa policy');
  });
});

describe('RAG and search', () => {
  it('answers questions with ranked evidence', async () => {
    const engine = new RagEngine('mock');
    const results = await engine.answer('How should we stage luxury villas?', [createKnowledgeItem({
      title: 'Luxury villa policy',
      summary: 'Guidelines for premium villa staging',
      content: 'Luxury villas require premium staging, local market context, and compliance checks.'
    })]);

    expect(results[0].score).toBeGreaterThan(0);
    expect(results[0].excerpt).toContain('staging');
  });

  it('supports hybrid retrieval with filters', async () => {
    const search = new HybridSearch();
    const results = await search.search('villa compliance', [{ key: 'source', value: 'documents' }]);

    expect(results.length).toBeGreaterThan(0);
    expect(results[0].item.title).toContain('villa');
  });
});

describe('Indexing and citations', () => {
  it('chunks and indexes content for incremental updates', async () => {
    const indexer = new Indexer();
    const chunks = await indexer.index([createKnowledgeItem({
      title: 'Quarterly market review',
      summary: 'Markets and compliance updates',
      content: 'Quarterly review covers market momentum, compliance reviews, and client outreach.'
    })]);

    expect(chunks.length).toBeGreaterThan(0);
    expect(indexer.getStatistics().documents).toBe(1);
  });

  it('resolves citations for answer context', () => {
    const resolver = new CitationResolver();
    const citation = resolver.resolve({
      itemId: 'doc-1',
      sourceId: 'docs',
      excerpt: 'Premium staging guidance.'
    });

    expect(citation.excerpt).toContain('Premium');
  });
});

describe('Knowledge hub and SDK', () => {
  it('exposes a mock knowledge hub and sdk helpers', async () => {
    const hub = createMockKnowledgeHub();
    const sdk = new KnowledgeSdk(hub);

    const searchResults = await sdk.search('luxury villa');
    const graph = sdk.graph('luxury');

    expect(searchResults.length).toBeGreaterThan(0);
    expect(graph.nodes.length).toBeGreaterThan(0);
  });
});
