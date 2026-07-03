export interface MemoryRetentionPolicy {
  maxItems: number;
  retainRaw: boolean;
}

export interface MemoryConversation {
  id: string;
  sessionId: string;
  mode: 'free' | 'guided' | 'business' | 'admin' | 'documentary';
  messages: Array<{ id: string; role: 'user' | 'assistant' | 'system'; content: string; timestamp: string }>;
  metadata?: Record<string, unknown>;
  createdAt: string;
}

export interface StoredFact {
  id: string;
  text: string;
  source: string;
}

export interface MemorySummary {
  summary: string;
}

export class MemoryService {
  constructor(private readonly options: { retentionPolicy: MemoryRetentionPolicy }) {}

  private conversations: MemoryConversation[] = [];

  addConversation(conversation: MemoryConversation) {
    this.conversations = [conversation, ...this.conversations].slice(0, this.options.retentionPolicy.maxItems);
  }

  getConversationHistory() {
    return this.conversations;
  }
}

export class SummaryGenerator {
  generate(conversation: MemoryConversation): MemorySummary {
    const joined = conversation.messages.map((message) => message.content).join(' ');
    return { summary: `Summary of ${conversation.mode} conversation: ${joined}` };
  }
}

export class FactExtractor {
  extract(conversation: MemoryConversation): StoredFact[] {
    return conversation.messages
      .filter((message) => message.role === 'user')
      .map((message) => ({ id: message.id, text: message.content, source: conversation.sessionId }));
  }
}

export class DecisionExtractor {
  extract(conversation: MemoryConversation) {
    return conversation.messages.filter((message) => message.content.includes('prefer')).map((message) => ({ text: message.content, source: conversation.sessionId }));
  }
}

export class TaskExtractor {
  extract(conversation: MemoryConversation) {
    return conversation.messages.filter((message) => message.content.includes('need')).map((message) => ({ text: message.content, source: conversation.sessionId }));
  }
}

export class PreferenceExtractor {
  extract(conversation: MemoryConversation) {
    return conversation.messages.filter((message) => message.content.includes('prefer')).map((message) => ({ text: message.content, source: conversation.sessionId }));
  }
}

export class TimelineBuilder {
  build(conversation: MemoryConversation) {
    return conversation.messages.map((message) => ({ timestamp: message.timestamp, content: message.content }));
  }
}

export function createMemoryRetentionPolicy(overrides: Partial<MemoryRetentionPolicy> = {}): MemoryRetentionPolicy {
  return {
    maxItems: 20,
    retainRaw: false,
    ...overrides
  };
}
