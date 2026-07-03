export interface AgentEvent {
  id: string;
  type: string;
  source: string;
  timestamp: string;
  correlationId?: string;
  severity?: 'info' | 'warning' | 'error';
  payload?: Record<string, unknown>;
}

export interface AgentMessage {
  id: string;
  channel: 'agent' | 'brain' | 'conversation' | 'learning' | 'task';
  sender: string;
  recipient?: string;
  message: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface TaskEvent extends AgentEvent {
  taskId: string;
}

export interface ExecutionEvent extends AgentEvent {
  executionId: string;
}

export interface BrainEvent extends AgentEvent {
  sessionId: string;
}

export interface ConversationEvent extends AgentEvent {
  conversationId: string;
}

export interface LearningEvent extends AgentEvent {
  learningId: string;
}

type EventListener = (event: AgentEvent) => void;

export class AgentEventBus {
  private readonly listeners = new Map<string, Set<EventListener>>();
  private readonly history: AgentEvent[] = [];

  subscribe(type: string, listener: EventListener) {
    const listeners = this.listeners.get(type) ?? new Set<EventListener>();
    listeners.add(listener);
    this.listeners.set(type, listeners);

    return () => {
      const current = this.listeners.get(type);
      current?.delete(listener);
      if (current && current.size === 0) {
        this.listeners.delete(type);
      }
    };
  }

  emit(event: AgentEvent) {
    this.history.push(event);
    this.listeners.get(event.type)?.forEach((listener) => listener(event));
    this.listeners.get('*')?.forEach((listener) => listener(event));
  }

  emitMessage(message: AgentMessage) {
    this.emit({
      id: message.id,
      type: `${message.channel}.message`,
      source: message.sender,
      timestamp: message.timestamp,
      payload: { ...message } as Record<string, unknown>
    });
  }

  list() {
    return [...this.history];
  }

  clear() {
    this.history.length = 0;
  }
}
