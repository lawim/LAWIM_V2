import { describe, expect, it } from 'vitest';
import { MemoryService, SummaryGenerator, FactExtractor, createMemoryRetentionPolicy } from '../packages/memory/src';

describe('Conversation memory', () => {
  it('extracts facts and generates a summary', () => {
    const memory = new MemoryService({ retentionPolicy: createMemoryRetentionPolicy({ maxItems: 3, retainRaw: false }) });
    memory.addConversation({
      id: 'c-1',
      sessionId: 's-1',
      mode: 'business',
      messages: [{ id: 'm-1', role: 'user', content: 'I prefer villas with sea views', timestamp: new Date().toISOString() }],
      metadata: { source: 'web' },
      createdAt: new Date().toISOString()
    });

    const summary = new SummaryGenerator().generate(memory.getConversationHistory()[0]);
    const facts = new FactExtractor().extract(memory.getConversationHistory()[0]);

    expect(summary.summary).toContain('villas');
    expect(facts.length).toBeGreaterThan(0);
  });
});
