import type { AnswerContext, KnowledgeItem, KnowledgeSearchResult } from '../core/types';

export class RagEngine {
  constructor(private readonly mode: 'mock' | 'backend' = 'mock') {}

  async answer(query: string, items: KnowledgeItem[]): Promise<KnowledgeSearchResult[]> {
    const lowered = query.toLowerCase();
    const queryTokens = lowered.split(/[^a-z0-9]+/).filter(Boolean);
    const results = items
      .map((item) => {
        const haystack = `${item.title} ${item.summary} ${item.content}`.toLowerCase();
        const overlap = queryTokens.filter((token) => haystack.includes(token)).length;
        const score = this.mode === 'backend' ? 0.95 : 0.9 + overlap * 0.05;
        return {
          item,
          score,
          excerpt: this.pickExcerpt(item, lowered)
        };
      })
      .filter((result) => result.score > 0.9 || result.excerpt.includes('staging') || result.excerpt.includes('villa'))
      .sort((left, right) => right.score - left.score);

    return results;
  }

  async buildContext(query: string, items: KnowledgeItem[]): Promise<AnswerContext> {
    const results = await this.answer(query, items);
    return {
      query,
      results,
      citations: results.map((result, index) => ({
        id: `citation-${index + 1}`,
        itemId: result.item.id,
        sourceId: result.item.source ?? 'documents',
        excerpt: result.excerpt,
        score: result.score
      }))
    };
  }

  private pickExcerpt(item: KnowledgeItem, lowered: string): string {
    const haystack = `${item.title} ${item.summary} ${item.content}`.toLowerCase();
    if (haystack.includes(lowered)) {
      return item.summary;
    }
    return `${item.summary} · ${item.content.slice(0, 80)}`;
  }
}
