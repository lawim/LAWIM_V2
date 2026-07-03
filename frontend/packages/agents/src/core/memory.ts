export interface WorkingMemoryRecord {
  id: string;
  kind: 'note' | 'failure' | 'success' | 'recommendation';
  content: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface MemoryExecutionRecord {
  id: string;
  agentId: string;
  taskId: string;
  status: string;
  summary: string;
  timestamp: string;
}

export interface AgentMemoryStatistics {
  executions: number;
  failures: number;
  successes: number;
  recommendations: number;
}

export interface AgentMemorySnapshot {
  workingMemory: WorkingMemoryRecord[];
  executionHistory: MemoryExecutionRecord[];
  failures: string[];
  successes: string[];
  recommendations: string[];
  statistics: AgentMemoryStatistics;
}

export class AgentMemory {
  private readonly workingMemory: WorkingMemoryRecord[] = [];
  private readonly executionHistory: MemoryExecutionRecord[] = [];
  private readonly failures: string[] = [];
  private readonly successes: string[] = [];
  private readonly recommendations: string[] = [];
  private readonly statistics: AgentMemoryStatistics = {
    executions: 0,
    failures: 0,
    successes: 0,
    recommendations: 0
  };

  rememberWorking(record: WorkingMemoryRecord) {
    this.workingMemory.push(record);
  }

  rememberExecution(record: MemoryExecutionRecord) {
    this.executionHistory.push(record);
    this.statistics.executions += 1;
  }

  rememberFailure(message: string) {
    this.failures.push(message);
    this.statistics.failures += 1;
    this.rememberWorking({
      id: `failure-${this.failures.length}`,
      kind: 'failure',
      content: message,
      timestamp: new Date().toISOString()
    });
  }

  rememberSuccess(message: string) {
    this.successes.push(message);
    this.statistics.successes += 1;
    this.rememberWorking({
      id: `success-${this.successes.length}`,
      kind: 'success',
      content: message,
      timestamp: new Date().toISOString()
    });
  }

  rememberRecommendation(message: string) {
    this.recommendations.push(message);
    this.statistics.recommendations += 1;
    this.rememberWorking({
      id: `recommendation-${this.recommendations.length}`,
      kind: 'recommendation',
      content: message,
      timestamp: new Date().toISOString()
    });
  }

  snapshot(): AgentMemorySnapshot {
    return {
      workingMemory: [...this.workingMemory],
      executionHistory: [...this.executionHistory],
      failures: [...this.failures],
      successes: [...this.successes],
      recommendations: [...this.recommendations],
      statistics: { ...this.statistics }
    };
  }
}
