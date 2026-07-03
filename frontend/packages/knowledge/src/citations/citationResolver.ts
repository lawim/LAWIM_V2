import type { KnowledgeCitation } from '../core/types';

export class CitationFormatter {
  format(citation: KnowledgeCitation): string {
    return `${citation.sourceId}: ${citation.excerpt}`;
  }
}

export class CitationResolver {
  resolve(citation: Omit<KnowledgeCitation, 'id'> & { id?: string }): KnowledgeCitation {
    return {
      id: citation.id ?? `citation-${citation.itemId}`,
      itemId: citation.itemId,
      sourceId: citation.sourceId,
      excerpt: citation.excerpt,
      score: citation.score ?? 0.8
    };
  }
}
