import { describe, expect, it } from 'vitest';
import { ConversationEngine, createConversationMessage } from '../packages/conversation/src';

describe('Conversation engine', () => {
  it('parses a business conversation into an intent', () => {
    const engine = new ConversationEngine();
    const conversation = {
      id: 'conv-1',
      sessionId: 'session-1',
      mode: 'business' as const,
      messages: [createConversationMessage('user', 'I need to estimate a villa near Marseille')],
      metadata: { source: 'web' },
      createdAt: new Date().toISOString()
    };

    const result = engine.analyze(conversation);

    expect(result.intent.type).toBe('EstimateProperty');
    expect(result.summary).toContain('villa');
  });
});
