import { AgentPriority } from './agent';

export enum TaskStatus {
  Draft = 'draft',
  Queued = 'queued',
  Running = 'running',
  WaitingApproval = 'waiting-approval',
  Succeeded = 'succeeded',
  Failed = 'failed',
  RolledBack = 'rolled-back',
  Cancelled = 'cancelled'
}

export enum TaskMode {
  Parallel = 'parallel',
  Sequential = 'sequential',
  Conditional = 'conditional'
}

export interface RetryPolicy {
  maxAttempts: number;
  delayMs: number;
  backoffFactor: number;
  retryableErrors: string[];
}

export interface TimeoutPolicy {
  timeoutMs: number;
  graceMs: number;
}

export interface RollbackInformation {
  supported: boolean;
  steps: string[];
  reason?: string;
}

export interface ExecutionAttempt {
  attempt: number;
  status: TaskStatus;
  startedAt: string;
  endedAt?: string;
  error?: string;
  notes?: string;
}

export interface ExecutionHistory {
  attempts: ExecutionAttempt[];
  lastUpdatedAt: string;
}

export interface SubTask {
  id: string;
  title: string;
  description: string;
  agentId: string;
  intent: string;
  status: TaskStatus;
  priority: AgentPriority;
  dependencies: string[];
  condition?: string;
  metadata?: Record<string, unknown>;
}

export interface AgentTask {
  id: string;
  title: string;
  description: string;
  agentId: string;
  intent: string;
  status: TaskStatus;
  priority: AgentPriority;
  mode: TaskMode;
  dependencies: string[];
  subtasks: SubTask[];
  retryPolicy: RetryPolicy;
  timeoutPolicy: TimeoutPolicy;
  rollback: RollbackInformation;
  history: ExecutionHistory;
  approvedDelegations: string[];
  metadata?: Record<string, unknown>;
}

export interface ExecutionPlan {
  id: string;
  name: string;
  tasks: AgentTask[];
  parallelTasks: AgentTask[];
  sequentialTasks: AgentTask[];
  conditionalTasks: AgentTask[];
  dependencies: Record<string, string[]>;
}

export { AgentPriority as Priority };

export function createRetryPolicy(overrides: Partial<RetryPolicy> = {}): RetryPolicy {
  return {
    maxAttempts: overrides.maxAttempts ?? 2,
    delayMs: overrides.delayMs ?? 0,
    backoffFactor: overrides.backoffFactor ?? 1,
    retryableErrors: overrides.retryableErrors ?? ['transient', 'temporary']
  };
}

export function createTimeoutPolicy(overrides: Partial<TimeoutPolicy> = {}): TimeoutPolicy {
  return {
    timeoutMs: overrides.timeoutMs ?? 15_000,
    graceMs: overrides.graceMs ?? 1_000
  };
}

export function createRollbackInformation(overrides: Partial<RollbackInformation> = {}): RollbackInformation {
  return {
    supported: overrides.supported ?? false,
    steps: overrides.steps ?? [],
    reason: overrides.reason
  };
}

export function createExecutionHistory(overrides: Partial<ExecutionHistory> = {}): ExecutionHistory {
  return {
    attempts: overrides.attempts ?? [],
    lastUpdatedAt: overrides.lastUpdatedAt ?? new Date().toISOString()
  };
}

export function createSubTask(overrides: Omit<Partial<SubTask>, 'id'> & { id: string; title: string; description: string; agentId: string; intent: string }): SubTask {
  return {
    id: overrides.id,
    title: overrides.title,
    description: overrides.description,
    agentId: overrides.agentId,
    intent: overrides.intent,
    status: overrides.status ?? TaskStatus.Draft,
    priority: overrides.priority ?? AgentPriority.Normal,
    dependencies: overrides.dependencies ?? [],
    condition: overrides.condition,
    metadata: overrides.metadata
  };
}

export function createTask(overrides: Omit<Partial<AgentTask>, 'id'> & { id: string; title: string; description: string; agentId: string; intent: string }): AgentTask {
  return {
    id: overrides.id,
    title: overrides.title,
    description: overrides.description,
    agentId: overrides.agentId,
    intent: overrides.intent,
    status: overrides.status ?? TaskStatus.Queued,
    priority: overrides.priority ?? AgentPriority.Normal,
    mode: overrides.mode ?? TaskMode.Sequential,
    dependencies: overrides.dependencies ?? [],
    subtasks: overrides.subtasks ?? [],
    retryPolicy: overrides.retryPolicy ?? createRetryPolicy(),
    timeoutPolicy: overrides.timeoutPolicy ?? createTimeoutPolicy(),
    rollback: overrides.rollback ?? createRollbackInformation(),
    history: overrides.history ?? createExecutionHistory(),
    approvedDelegations: overrides.approvedDelegations ?? [],
    metadata: overrides.metadata
  };
}

export function createExecutionPlan(overrides: {
  id: string;
  name: string;
  tasks: AgentTask[];
}): ExecutionPlan {
  return {
    id: overrides.id,
    name: overrides.name,
    tasks: overrides.tasks,
    parallelTasks: overrides.tasks.filter((task) => task.mode === TaskMode.Parallel),
    sequentialTasks: overrides.tasks.filter((task) => task.mode === TaskMode.Sequential),
    conditionalTasks: overrides.tasks.filter((task) => task.mode === TaskMode.Conditional),
    dependencies: Object.fromEntries(overrides.tasks.map((task) => [task.id, task.dependencies]))
  };
}
