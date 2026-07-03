import { describe, expect, it } from 'vitest';
import { AgentHistory, AgentLogger, AgentMetrics, ExecutionStatus } from '@agents';

describe('agent metrics', () => {
  it('tracks success and failure rates', () => {
    const metrics = new AgentMetrics();
    metrics.recordExecution(ExecutionStatus.Completed, 120, 1);
    metrics.recordExecution(ExecutionStatus.Failed, 80, 0);

    const snapshot = metrics.snapshot();

    expect(snapshot.executions).toBe(2);
    expect(snapshot.successes).toBe(1);
    expect(snapshot.failures).toBe(1);
    expect(snapshot.successRate).toBeCloseTo(0.5);
    expect(snapshot.retries).toBe(1);
  });

  it('records history and logs for the runtime', () => {
    const history = new AgentHistory();
    const logger = new AgentLogger();

    history.record({
      id: 'execution-1',
      agentId: 'agent-crm',
      taskId: 'task-1',
      status: ExecutionStatus.Completed,
      summary: 'Completed',
      startedAt: '2026-07-03T09:00:00.000Z',
      endedAt: '2026-07-03T09:00:01.000Z',
      durationMs: 1000,
      retries: 0
    });
    logger.info('agent-crm', 'Completed task-1');

    expect(history.list()).toHaveLength(1);
    expect(history.successRate()).toBe(1);
    expect(logger.list()).toHaveLength(1);
  });
});
