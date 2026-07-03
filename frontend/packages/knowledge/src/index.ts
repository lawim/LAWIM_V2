export * from './core/types';
export * from './core/knowledgeService';
export * from './rag/ragEngine';
export * from './indexing/indexer';
export * from './search/hybridSearch';
export * from './sources/sourceRegistry';
export * from './embeddings/embeddingService';
export * from './ontology/taxonomy';
export * from './knowledge-graph/knowledgeGraph';
export * from './citations/citationResolver';

import { createKnowledgeItem } from './core/knowledgeService';
import { KnowledgeGraphExplorer } from './knowledge-graph/knowledgeGraph';
import type { KnowledgeGraph, KnowledgeSearchResult } from './core/types';

export interface KnowledgeHub {
  search(query: string): Promise<KnowledgeSearchResult[]>;
  graph(query: string): KnowledgeGraph;
}

export class KnowledgeSdk {
  constructor(private readonly hub: KnowledgeHub) {}

  async search(query: string) {
    return this.hub.search(query);
  }

  graph(query: string) {
    return this.hub.graph(query);
  }
}

export function createMockKnowledgeHub(): KnowledgeHub {
  return {
    async search(query: string) {
      return [
        {
          item: createKnowledgeItem({
            title: `Mock knowledge for ${query}`,
            summary: 'Mock summary',
            content: 'Mock knowledge content for the LAWIM platform.'
          }),
          score: 0.91,
          excerpt: 'Mock summary'
        }
      ];
    },
    graph(query: string) {
      return new KnowledgeGraphExplorer().build(query);
    }
  };
}

export class KnowledgeExplorer {
  overview() {
    return {
      dashboard: 'Knowledge Dashboard',
      graph: 'Knowledge Graph',
      explorer: 'Knowledge Explorer',
      searchConsole: 'Search Console'
    };
  }
}
