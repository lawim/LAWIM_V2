export class EmbeddingService {
  async embed(text: string): Promise<number[]> {
    const normalized = text.toLowerCase();
    return Array.from(normalized).map((char) => char.charCodeAt(0) % 7);
  }
}
