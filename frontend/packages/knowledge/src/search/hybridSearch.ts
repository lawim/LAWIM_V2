import { KnowledgeService, createKnowledgeItem } from '../core/knowledgeService';
import type { KnowledgeSearchFilter, KnowledgeSearchResult } from '../core/types';

export class HybridSearch {
  constructor(private readonly service = new KnowledgeService()) {}

  async search(query: string, filters: KnowledgeSearchFilter[] = []): Promise<KnowledgeSearchResult[]> {
    const seeded = [
      createKnowledgeItem({
        id: 'villa-doc',
        title: 'Luxury villa compliance',
        summary: 'Villa compliance and staging guidance',
        content: 'Luxury villas require compliance checks, premium staging, and documented procedures.',
        tags: ['villa', 'compliance'],
        source: 'documents',
        category: 'knowledge'
      })
    ];

    seeded.forEach((item) => this.service.addDocument(item));
    return this.service.search(query, filters);
  }
}
