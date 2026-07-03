import type { KnowledgeSource } from '../core/types';

export class SourceRegistry {
  private readonly sources: KnowledgeSource[] = [
    { id: 'docs', label: 'Documents LAWIM', type: 'documents' },
    { id: 'crm', label: 'CRM', type: 'crm' },
    { id: 'marketplace', label: 'Marketplace', type: 'marketplace' },
    { id: 'contracts', label: 'Contracts', type: 'contracts' },
    { id: 'faq', label: 'FAQ', type: 'faq' }
  ];

  getAll(): KnowledgeSource[] {
    return [...this.sources];
  }
}
