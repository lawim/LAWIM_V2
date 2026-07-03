export type KnowledgeStatus = 'draft' | 'review' | 'published' | 'archived';

export interface KnowledgeMetadata {
  sourceType?: string;
  owner?: string;
  language?: string;
  tags?: string[];
  lastIndexedAt?: string;
  [key: string]: unknown;
}

export interface KnowledgeItem {
  id: string;
  title: string;
  summary: string;
  content: string;
  tags?: string[];
  status?: KnowledgeStatus;
  category?: string;
  source?: string;
  metadata?: KnowledgeMetadata;
  createdAt?: string;
  updatedAt?: string;
}

export interface KnowledgeChunk {
  id: string;
  itemId: string;
  content: string;
  score?: number;
  metadata?: KnowledgeMetadata;
}

export interface KnowledgeSource {
  id: string;
  label: string;
  type: string;
  description?: string;
  url?: string;
}

export interface KnowledgeCategory {
  id: string;
  name: string;
  description?: string;
  parentId?: string;
}

export interface KnowledgeCitation {
  id: string;
  itemId: string;
  sourceId: string;
  excerpt: string;
  score?: number;
}

export interface KnowledgeSearchResult {
  item: KnowledgeItem;
  score: number;
  excerpt: string;
}

export interface KnowledgeSearchFilter {
  key: string;
  value: string;
}

export interface KnowledgeNode {
  id: string;
  label: string;
  type: string;
  properties?: Record<string, unknown>;
}

export interface KnowledgeEdge {
  id: string;
  from: string;
  to: string;
  type: string;
  strength?: number;
}

export interface KnowledgeGraph {
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
}

export interface AnswerContext {
  query: string;
  results: KnowledgeSearchResult[];
  citations: KnowledgeCitation[];
}
