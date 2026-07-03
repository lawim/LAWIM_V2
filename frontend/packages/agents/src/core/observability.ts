import type { ExecutionStatus } from './execution';

export interface AgentLogEntry {
  id: string;
  level: 'debug' | 'info' | 'warn' | 'error';
  source: string;
  message: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface AgentHistoryEntry {
  id: string;
  agentId: string;
  taskId: string;
  status: ExecutionStatus | string;
  summary: string;
  startedAt: string;
  endedAt: string;
  durationMs: number;
  retries: number;
  metadata?: Record<string, unknown>;
}

export interface AgentAuditEntry {
  id: string;
  actor: string;
  action: string;
  target: string;
  outcome: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface AgentMetricSnapshot {
  executions: number;
  successes: number;
  failures: number;
  retries: number;
  averageDurationMs: number;
  successRate: number;
  failureRate: number;
}

export function createLogEntry(
  overrides: Omit<Partial<AgentLogEntry>, 'id' | 'level' | 'source' | 'message' | 'timestamp'> & {
    id: string;
    level: AgentLogEntry['level'];
    source: string;
    message: string;
    timestamp?: string;
  }
): AgentLogEntry {
  return {
    id: overrides.id,
    level: overrides.level,
    source: overrides.source,
    message: overrides.message,
    timestamp: overrides.timestamp ?? new Date().toISOString(),
    metadata: overrides.metadata
  };
}

export class AgentLogger {
  private readonly entries: AgentLogEntry[] = [];

  log(entry: AgentLogEntry) {
    this.entries.push(entry);
  }

  debug(source: string, message: string, metadata?: Record<string, unknown>) {
    this.log(createLogEntry({ id: `log-${this.entries.length + 1}`, level: 'debug', source, message, metadata }));
  }

  info(source: string, message: string, metadata?: Record<string, unknown>) {
    this.log(createLogEntry({ id: `log-${this.entries.length + 1}`, level: 'info', source, message, metadata }));
  }

  warn(source: string, message: string, metadata?: Record<string, unknown>) {
    this.log(createLogEntry({ id: `log-${this.entries.length + 1}`, level: 'warn', source, message, metadata }));
  }

  error(source: string, message: string, metadata?: Record<string, unknown>) {
    this.log(createLogEntry({ id: `log-${this.entries.length + 1}`, level: 'error', source, message, metadata }));
  }

  list() {
    return [...this.entries];
  }

  latest() {
    return this.entries[this.entries.length - 1];
  }

  clear() {
    this.entries.length = 0;
  }
}

export class AgentHistory {
  private readonly entries: AgentHistoryEntry[] = [];

  record(entry: AgentHistoryEntry) {
    this.entries.push(entry);
  }

  list() {
    return [...this.entries];
  }

  byAgent(agentId: string) {
    return this.entries.filter((entry) => entry.agentId === agentId);
  }

  byTask(taskId: string) {
    return this.entries.filter((entry) => entry.taskId === taskId);
  }

  successRate() {
    const total = this.entries.length;
    if (total === 0) {
      return 0;
    }
    const successes = this.entries.filter((entry) => isSuccessStatus(entry.status)).length;
    return successes / total;
  }

  failureRate() {
    const total = this.entries.length;
    if (total === 0) {
      return 0;
    }
    const failures = this.entries.filter((entry) => isFailureStatus(entry.status)).length;
    return failures / total;
  }

  averageDurationMs() {
    if (this.entries.length === 0) {
      return 0;
    }
    return this.entries.reduce((sum, entry) => sum + entry.durationMs, 0) / this.entries.length;
  }
}

export class AgentAudit {
  private readonly entries: AgentAuditEntry[] = [];

  record(entry: AgentAuditEntry) {
    this.entries.push(entry);
  }

  list() {
    return [...this.entries];
  }
}

export class AgentMetrics {
  private executions = 0;
  private successes = 0;
  private failures = 0;
  private retries = 0;
  private durationTotal = 0;

  recordExecution(status: string, durationMs: number, retryCount = 0) {
    this.executions += 1;
    this.retries += retryCount;
    this.durationTotal += durationMs;

    if (isSuccessStatus(status)) {
      this.successes += 1;
    } else if (isFailureStatus(status)) {
      this.failures += 1;
    }
  }

  snapshot(): AgentMetricSnapshot {
    const averageDurationMs = this.executions === 0 ? 0 : this.durationTotal / this.executions;
    const successRate = this.executions === 0 ? 0 : this.successes / this.executions;
    const failureRate = this.executions === 0 ? 0 : this.failures / this.executions;

    return {
      executions: this.executions,
      successes: this.successes,
      failures: this.failures,
      retries: this.retries,
      averageDurationMs,
      successRate,
      failureRate
    };
  }
}

export function createExecutionTimeline(history: AgentHistoryEntry[]) {
  return history.map((entry) => ({
    id: entry.id,
    label: `${entry.agentId} • ${entry.status}`,
    timestamp: entry.endedAt,
    detail: entry.summary
  }));
}

function isSuccessStatus(status: string) {
  return status === 'succeeded' || status === 'completed' || status === 'approved';
}

function isFailureStatus(status: string) {
  return status === 'failed' || status === 'rejected' || status === 'revoked' || status === 'expired';
}
