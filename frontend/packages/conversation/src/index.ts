export type ConversationMode = 'free' | 'guided' | 'business' | 'admin' | 'documentary';

export interface ConversationMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export interface ConversationSession {
  id: string;
  mode: ConversationMode;
  messages: ConversationMessage[];
  metadata?: Record<string, unknown>;
  createdAt: string;
}

export interface ConversationIntent {
  type: string;
  confidence: number;
  summary: string;
}

export interface ConversationContext {
  mode: ConversationMode;
  summary?: string;
}

export interface ConversationSummary {
  summary: string;
}

export interface ConversationAction {
  type: string;
  payload?: Record<string, unknown>;
}

export interface ConversationMetadata {
  source: string;
}

export interface Conversation {
  id: string;
  sessionId: string;
  mode: ConversationMode;
  messages: ConversationMessage[];
  metadata: ConversationMetadata;
  createdAt: string;
}

export class ConversationParser {
  parse(content: string): ConversationIntent {
    const lowered = content.toLowerCase();
    if (lowered.includes('estimate')) return { type: 'EstimateProperty', confidence: 0.86, summary: 'Estimate request detected' };
    if (lowered.includes('search')) return { type: 'SearchProperty', confidence: 0.84, summary: 'Search request detected' };
    if (lowered.includes('document')) return { type: 'GenerateDocument', confidence: 0.82, summary: 'Document request detected' };
    if (lowered.includes('workflow')) return { type: 'CreateWorkflow', confidence: 0.8, summary: 'Workflow request detected' };
    return { type: 'OpenConversation', confidence: 0.6, summary: 'General conversation' };
  }
}

export class ConversationRouter {
  route(intent: ConversationIntent, mode: ConversationMode) {
    return { route: intent.type, mode };
  }
}

export class ConversationHistory {
  constructor(private readonly messages: ConversationMessage[]) {}

  latest() {
    return this.messages[this.messages.length - 1];
  }
}

export class ConversationPipeline {
  constructor(private readonly history: ConversationHistory, private readonly parser: ConversationParser, private readonly router: ConversationRouter) {}

  run(mode: ConversationMode) {
    const latest = this.history.latest();
    const intent = this.parser.parse(latest?.content ?? '');
    const route = this.router.route(intent, mode);
    return { intent, route, summary: `${intent.summary} in ${mode} mode` };
  }
}

export class ConversationEngine {
  private readonly parser = new ConversationParser();
  private readonly router = new ConversationRouter();

  analyze(conversation: Conversation) {
    const pipeline = new ConversationPipeline(new ConversationHistory(conversation.messages), this.parser, this.router);
    const parsed = pipeline.run(conversation.mode);
    const messageContext = conversation.messages.map((message) => message.content).join(' ');
    return {
      intent: parsed.intent,
      summary: `${parsed.summary} • ${messageContext}`,
      actions: [{ type: 'route-to-brain', payload: { mode: conversation.mode } } as ConversationAction]
    };
  }
}

export function createConversationMessage(role: ConversationMessage['role'], content: string): ConversationMessage {
  return { id: `msg-${Math.random().toString(36).slice(2)}`, role, content, timestamp: new Date().toISOString() };
}
