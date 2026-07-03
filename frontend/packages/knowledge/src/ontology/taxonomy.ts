export class Taxonomy {
  private readonly categories = new Map<string, string[]>([
    ['documents', ['guides', 'procedures', 'reports']],
    ['crm', ['clients', 'projects']],
    ['marketplace', ['providers', 'offers']]
  ]);

  getTopics(category: string): string[] {
    return this.categories.get(category) ?? [];
  }
}
