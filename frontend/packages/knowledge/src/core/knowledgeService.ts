import type { KnowledgeCategory, KnowledgeItem, KnowledgeSearchFilter, KnowledgeSearchResult } from './types';

export class KnowledgeService {
  private readonly items: KnowledgeItem[] = [];
  private readonly categories: KnowledgeCategory[] = [];

  addDocument(item: KnowledgeItem) {
    this.items.push(item);
  }

  addCategory(category: KnowledgeCategory) {
    this.categories.push(category);
  }

  getAllDocuments(): KnowledgeItem[] {
    return [...this.items];
  }

  getDocumentById(id: string): KnowledgeItem | undefined {
    return this.items.find((item) => item.id === id);
  }

  async search(query: string, filters: KnowledgeSearchFilter[] = []): Promise<KnowledgeSearchResult[]> {
    const lowered = query.trim().toLowerCase();
    const tokens = lowered.split(/\s+/).filter(Boolean);

    return this.items
      .filter((item) => this.matchesFilters(item, filters))
      .map((item) => {
        const haystack = `${item.title} ${item.summary} ${item.content} ${item.tags?.join(' ') ?? ''}`.toLowerCase();
        const score = tokens.reduce((value, token) => {
          return value + (haystack.includes(token) ? 1 : 0);
        }, 0);

        return {
          item,
          score: score + (item.tags?.length ? 0.2 : 0),
          excerpt: item.summary
        };
      })
      .filter((result) => result.score > 0 || lowered.length === 0)
      .sort((left, right) => right.score - left.score);
  }

  private matchesFilters(item: KnowledgeItem, filters: KnowledgeSearchFilter[]): boolean {
    return filters.every((filter) => {
      const value = item[filter.key as keyof KnowledgeItem];
      if (typeof value === 'string') {
        return value.toLowerCase() === filter.value.toLowerCase();
      }
      if (Array.isArray(value)) {
        return value.some((entry) => String(entry).toLowerCase() === filter.value.toLowerCase());
      }
      return true;
    });
  }
}

export function createKnowledgeItem(overrides: Partial<KnowledgeItem> = {}): KnowledgeItem {
  return {
    id: overrides.id ?? `knowledge-${Math.random().toString(36).slice(2)}`,
    title: overrides.title ?? 'Untitled knowledge item',
    summary: overrides.summary ?? 'Knowledge summary',
    content: overrides.content ?? 'Knowledge content',
    tags: overrides.tags ?? [],
    category: overrides.category ?? 'knowledge',
    source: overrides.source ?? 'documents',
    metadata: overrides.metadata ?? {},
    status: overrides.status ?? 'draft',
    createdAt: overrides.createdAt ?? new Date().toISOString(),
    updatedAt: overrides.updatedAt ?? new Date().toISOString()
  };
}
