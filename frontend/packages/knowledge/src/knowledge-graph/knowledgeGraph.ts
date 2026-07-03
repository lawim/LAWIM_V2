import type { KnowledgeGraph, KnowledgeNode } from '../core/types';

export class KnowledgeGraphExplorer {
  build(query: string): KnowledgeGraph {
    const nodes: KnowledgeNode[] = [
      { id: 'knowledge', label: 'Knowledge Hub', type: 'hub' },
      { id: 'query', label: query, type: 'topic' }
    ];

    return {
      nodes,
      edges: [{ id: 'edge-1', from: 'knowledge', to: 'query', type: 'related', strength: 1 }]
    };
  }
}
