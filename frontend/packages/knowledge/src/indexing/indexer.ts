import type { KnowledgeChunk, KnowledgeItem } from '../core/types';

export class Indexer {
  private readonly chunks: KnowledgeChunk[] = [];
  private documents = 0;

  async index(items: KnowledgeItem[]): Promise<KnowledgeChunk[]> {
    this.documents = items.length;
    const chunked = items.flatMap((item) => this.chunkItem(item));
    this.chunks.push(...chunked);
    return chunked;
  }

  async reindex(items: KnowledgeItem[]): Promise<KnowledgeChunk[]> {
    this.chunks.length = 0;
    return this.index(items);
  }

  getStatistics() {
    return {
      documents: this.documents,
      chunks: this.chunks.length,
      status: 'ready'
    };
  }

  private chunkItem(item: KnowledgeItem): KnowledgeChunk[] {
    const segments = item.content.split(/(?<=[.!?])\s+/).filter(Boolean);
    return segments.map((segment, index) => ({
      id: `${item.id}-chunk-${index + 1}`,
      itemId: item.id,
      content: segment,
      score: 1 - index * 0.05,
      metadata: {
        source: item.source,
        category: item.category,
        tags: item.tags
      }
    }));
  }
}
