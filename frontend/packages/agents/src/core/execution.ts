import { AgentPriority, type Agent, type AgentContext, type AgentResult } from './agent';
import { AgentHistory, AgentLogger, AgentMetrics, type AgentHistoryEntry } from './observability';
import { AgentAuthorization, type AuthorizationDecision } from './authorization';
import { ApprovalQueue } from './approvals';
import type { AgentTask, ExecutionPlan, TaskMode } from './tasks';
import type { AgentEventBus } from './events';

export enum ExecutionStatus {
  Idle = 'idle',
  Queued = 'queued',
  Running = 'running',
  WaitingApproval = 'waiting-approval',
  Completed = 'completed',
  Failed = 'failed',
  RolledBack = 'rolled-back',
  Cancelled = 'cancelled'
}

export interface ExecutionGraphNode {
  id: string;
  taskId: string;
  agentId: string;
  mode: TaskMode;
  priority: AgentPriority;
  dependencies: string[];
}

export interface ExecutionGraphEdge {
  from: string;
  to: string;
  reason: string;
}

export interface ExecutionGraph {
  id: string;
  name: string;
  nodes: ExecutionGraphNode[];
  edges: ExecutionGraphEdge[];
}

export interface ExecutionPipelineStage {
  id: string;
  name: string;
  taskIds: string[];
  mode: TaskMode;
  parallel: boolean;
}

export interface ExecutionPipeline {
  id: string;
  name: string;
  stages: ExecutionPipelineStage[];
}

export interface AgentExecution {
  id: string;
  agentId: string;
  taskId: string;
  status: ExecutionStatus;
  startedAt: string;
  endedAt?: string;
  attempts: number;
  timeline: Array<{ at: string; event: string; detail?: string }>;
  result?: AgentResult;
  error?: string;
}

export class AgentQueue<T extends AgentTask = AgentTask> {
  private readonly tasks: T[] = [];

  enqueue(task: T) {
    this.tasks.push(task);
    this.tasks.sort((left, right) => right.priority - left.priority || left.title.localeCompare(right.title));
    return task;
  }

  enqueueMany(tasks: T[]) {
    tasks.forEach((task) => this.enqueue(task));
    return this.list();
  }

  dequeue() {
    return this.tasks.shift();
  }

  peek() {
    return this.tasks[0];
  }

  list() {
    return [...this.tasks];
  }

  size() {
    return this.tasks.length;
  }

  clear() {
    this.tasks.length = 0;
  }
}

export class AgentScheduler {
  buildExecutionGraph(tasks: AgentTask[], name = 'execution-graph'): ExecutionGraph {
    const nodes = tasks.map((task) => ({
      id: `node-${task.id}`,
      taskId: task.id,
      agentId: task.agentId,
      mode: task.mode,
      priority: task.priority,
      dependencies: [...task.dependencies]
    }));

    const edges: ExecutionGraphEdge[] = [];
    for (const task of tasks) {
      for (const dependency of task.dependencies) {
        edges.push({
          from: `node-${dependency}`,
          to: `node-${task.id}`,
          reason: `${task.id} depends on ${dependency}`
        });
      }
    }

    return {
      id: `graph-${name}`,
      name,
      nodes,
      edges
    };
  }

  buildExecutionPipeline(tasks: AgentTask[], name = 'execution-pipeline'): ExecutionPipeline {
    const depthCache = new Map<string, number>();
    const taskMap = new Map(tasks.map((task) => [task.id, task]));

    const depthFor = (taskId: string): number => {
      if (depthCache.has(taskId)) {
        return depthCache.get(taskId) ?? 0;
      }

      const task = taskMap.get(taskId);
      if (!task || task.dependencies.length === 0) {
        depthCache.set(taskId, 0);
        return 0;
      }

      const depth = 1 + Math.max(...task.dependencies.map((dependency) => depthFor(dependency)));
      depthCache.set(taskId, depth);
      return depth;
    };

    const grouped = new Map<number, AgentTask[]>();
    for (const task of tasks) {
      const depth = depthFor(task.id);
      const current = grouped.get(depth) ?? [];
      current.push(task);
      grouped.set(depth, current);
    }

    const stages = [...grouped.entries()]
      .sort(([leftDepth], [rightDepth]) => leftDepth - rightDepth)
      .map(([depth, stageTasks]) => ({
        id: `stage-${depth}`,
        name: `Stage ${depth + 1}`,
        taskIds: stageTasks
          .sort((left, right) => right.priority - left.priority || left.title.localeCompare(right.title))
          .map((task) => task.id),
        mode: stageTasks[0]?.mode ?? 'sequential',
        parallel: stageTasks.length > 1
      }));

    return {
      id: `pipeline-${name}`,
      name,
      stages
    };
  }

  buildPlan(tasks: AgentTask[], name = 'agent-plan'): ExecutionPlan & { graph: ExecutionGraph; pipeline: ExecutionPipeline } {
    return {
      ...this.buildExecutionPlan(tasks, name),
      graph: this.buildExecutionGraph(tasks, `${name}-graph`),
      pipeline: this.buildExecutionPipeline(tasks, `${name}-pipeline`)
    };
  }

  private buildExecutionPlan(tasks: AgentTask[], name: string): ExecutionPlan {
    return {
      id: `plan-${name}`,
      name,
      tasks,
      parallelTasks: tasks.filter((task) => task.mode === 'parallel'),
      sequentialTasks: tasks.filter((task) => task.mode === 'sequential'),
      conditionalTasks: tasks.filter((task) => task.mode === 'conditional'),
      dependencies: Object.fromEntries(tasks.map((task) => [task.id, task.dependencies]))
    };
  }
}

export interface ExecutorEnvironment {
  eventBus?: AgentEventBus;
  logger?: AgentLogger;
  metrics?: AgentMetrics;
  history?: AgentHistory;
  approvals?: ApprovalQueue;
  authorization?: AgentAuthorization;
  audit?: { record: (entry: { id: string; actor: string; action: string; target: string; outcome: string; timestamp: string; metadata?: Record<string, unknown> }) => void };
}

export class AgentExecutor {
  constructor(private readonly environment: ExecutorEnvironment = {}) {}

  async execute(agent: Agent, task: AgentTask, context: AgentContext): Promise<AgentExecution> {
    const startedAt = context.now ?? new Date().toISOString();
    const execution: AgentExecution = {
      id: `execution-${task.id}`,
      agentId: agent.id,
      taskId: task.id,
      status: ExecutionStatus.Running,
      startedAt,
      attempts: 0,
      timeline: [{ at: startedAt, event: 'execution-started', detail: task.intent }]
    };

    this.environment.eventBus?.emit({
      id: `event-${execution.id}-started`,
      type: 'execution.started',
      source: agent.id,
      timestamp: startedAt,
      payload: { taskId: task.id, intent: task.intent }
    });

    const authorization: AuthorizationDecision | undefined = this.environment.authorization?.authorize(agent, task, context);
    if (authorization && !authorization.allowed) {
      execution.status = authorization.requiresApproval ? ExecutionStatus.WaitingApproval : ExecutionStatus.Failed;
      execution.error = authorization.reason;
      execution.timeline.push({
        at: new Date().toISOString(),
        event: authorization.requiresApproval ? 'waiting-approval' : 'authorization-denied',
        detail: authorization.reason
      });
      this.recordExecution(agent, task, execution);
      return execution;
    }

    const maxAttempts = task.retryPolicy.maxAttempts ?? 1;
    let lastError: string | undefined;
    const approvalRequired = this.environment.approvals
      ? Boolean(task.metadata?.requiresApproval || task.metadata?.sensitive) &&
        !this.environment.approvals.hasApproved(String(task.metadata?.approvalReferenceId ?? task.id))
      : false;
    if (approvalRequired) {
      execution.status = ExecutionStatus.WaitingApproval;
      execution.error = 'Awaiting human approval';
      execution.timeline.push({
        at: new Date().toISOString(),
        event: 'waiting-approval',
        detail: 'Human approval required'
      });
      this.recordExecution(agent, task, execution);
      return execution;
    }

    for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
      execution.attempts = attempt;
      execution.timeline.push({
        at: new Date().toISOString(),
        event: 'attempt-started',
        detail: `Attempt ${attempt}`
      });

      try {
        const result = await Promise.resolve(agent.execute(task, context));
        execution.result = result;
        if (result.success) {
          execution.status = ExecutionStatus.Completed;
          execution.timeline.push({
            at: new Date().toISOString(),
            event: 'attempt-succeeded',
            detail: result.summary
          });
          lastError = undefined;
          break;
        }

        lastError = result.summary;
        execution.timeline.push({
          at: new Date().toISOString(),
          event: 'attempt-failed',
          detail: result.summary
        });
      } catch (error) {
        lastError = error instanceof Error ? error.message : String(error);
        execution.timeline.push({
          at: new Date().toISOString(),
          event: 'attempt-threw',
          detail: lastError
        });
      }

      if (attempt < maxAttempts) {
        execution.timeline.push({
          at: new Date().toISOString(),
          event: 'retry-scheduled',
          detail: `Retry ${attempt + 1}`
        });
      }
    }

    if (execution.status !== ExecutionStatus.Completed) {
      execution.status = task.rollback.supported ? ExecutionStatus.RolledBack : ExecutionStatus.Failed;
      execution.error = lastError ?? 'Execution failed';
      if (task.rollback.supported) {
        execution.timeline.push({
          at: new Date().toISOString(),
          event: 'rollback-triggered',
          detail: task.rollback.reason ?? 'Rollback policy enabled'
        });
      }
    }

    execution.endedAt = new Date().toISOString();
    this.recordExecution(agent, task, execution);
    return execution;
  }

  private recordExecution(agent: Agent, task: AgentTask, execution: AgentExecution) {
    const endedAt = execution.endedAt ?? new Date().toISOString();
    const durationMs = Math.max(0, Date.parse(endedAt) - Date.parse(execution.startedAt));
    const historyEntry: AgentHistoryEntry = {
      id: execution.id,
      agentId: agent.id,
      taskId: task.id,
      status: execution.status,
      summary: execution.result?.summary ?? execution.error ?? `${task.title} finished with ${execution.status}`,
      startedAt: execution.startedAt,
      endedAt,
      durationMs,
      retries: Math.max(0, execution.attempts - 1),
      metadata: {
        intent: task.intent,
        result: execution.result?.metadata ?? {},
        timeline: execution.timeline
      }
    };

    this.environment.metrics?.recordExecution(execution.status, durationMs, Math.max(0, execution.attempts - 1));
    this.environment.history?.record(historyEntry);
    this.environment.logger?.info(agent.id, `Task ${task.id} finished with ${execution.status}`, {
      taskId: task.id,
      status: execution.status,
      retries: execution.attempts - 1
    });
    this.environment.audit?.record({
      id: `audit-${execution.id}`,
      actor: agent.id,
      action: 'execute-task',
      target: task.id,
      outcome: execution.status,
      timestamp: endedAt,
      metadata: {
        taskIntent: task.intent
      }
    });
    this.environment.eventBus?.emit({
      id: `event-${execution.id}-${execution.status}`,
      type: 'execution.completed',
      source: agent.id,
      timestamp: endedAt,
      payload: {
        taskId: task.id,
        status: execution.status,
        result: execution.result?.summary
      }
    });
  }
}
