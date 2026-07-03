import { describe, expect, it } from 'vitest';
import {
  AgentAuthorization,
  AgentAvailability,
  AgentHealth,
  AgentPriority,
  AgentStatus,
  ApprovalQueue,
  AgentExecutor,
  AgentHistory,
  AgentLogger,
  AgentMetrics,
  AgentScheduler,
  ApprovalStatus,
  createAgentContext,
  createAgentDefinition,
  createAgentResult,
  createApprovalRequest,
  createDefaultPolicies,
  createExecutionHistory,
  createRetryPolicy,
  createTask,
  ExecutionStatus,
  TaskMode,
  TaskStatus,
  PolicyEngine
} from '@agents';

describe('agent execution', () => {
  it('builds an execution graph and retries transient failures', async () => {
    const scheduler = new AgentScheduler();
    const tasks = [
      createTask({
        id: 'task-a',
        title: 'Prepare A',
        description: 'First step',
        agentId: 'agent-crm',
        intent: 'CreateLead',
        priority: AgentPriority.High,
        mode: TaskMode.Sequential
      }),
      createTask({
        id: 'task-b',
        title: 'Prepare B',
        description: 'Second step',
        agentId: 'agent-documents',
        intent: 'ClassifyDocument',
        priority: AgentPriority.Normal,
        mode: TaskMode.Parallel,
        dependencies: ['task-a']
      })
    ];

    const graph = scheduler.buildExecutionGraph(tasks);
    const pipeline = scheduler.buildExecutionPipeline(tasks);

    expect(graph.edges).toHaveLength(1);
    expect(pipeline.stages[0]?.taskIds).toContain('task-a');

    let attempts = 0;
    const agent = createAgentDefinition({
      id: 'agent-crm',
      name: 'CRM Test Agent',
      description: 'Test agent',
      capabilities: [],
      health: AgentHealth.Healthy,
      availability: AgentAvailability.Available,
      permissions: [],
      supportedIntents: ['CreateLead'],
      supportedModules: ['crm'],
      execute() {
        attempts += 1;
        if (attempts === 1) {
          return createAgentResult({
            success: false,
            status: AgentStatus.Failed,
            summary: 'Transient issue',
            recommendations: [],
            nextSteps: [],
            artifacts: [],
            metadata: {}
          });
        }

        return createAgentResult({
          summary: 'Execution complete',
          recommendations: [],
          nextSteps: [],
          artifacts: [],
          metadata: {}
        });
      }
    });

    const executor = new AgentExecutor({
      history: new AgentHistory(),
      logger: new AgentLogger(),
      metrics: new AgentMetrics()
    });
    const execution = await executor.execute(agent, createTask({
      id: 'task-retry',
      title: 'Retryable task',
      description: 'Retries once before success',
      agentId: 'agent-crm',
      intent: 'CreateLead',
      priority: AgentPriority.High,
      mode: TaskMode.Sequential,
      retryPolicy: createRetryPolicy({ maxAttempts: 2 }),
      history: createExecutionHistory({ attempts: [{ attempt: 1, status: TaskStatus.Failed, startedAt: '2026-07-03T09:00:00.000Z' }], lastUpdatedAt: '2026-07-03T09:00:00.000Z' })
    }), createAgentContext({ brainSessionId: 'brain-1', permissions: [], approvedDelegations: [] }));

    expect(execution.status).toBe(ExecutionStatus.Completed);
    expect(execution.attempts).toBe(2);
  });

  it('waits for approval on sensitive tasks', async () => {
    const approvals = new ApprovalQueue();
    const authorization = new AgentAuthorization({ policyEngine: new PolicyEngine(createDefaultPolicies()), approvals });
    const agent = createAgentDefinition({
      id: 'agent-documents',
      name: 'Documents Test Agent',
      description: 'Test agent',
      capabilities: [],
      health: AgentHealth.Healthy,
      availability: AgentAvailability.Available,
      permissions: ['documents:classify'],
      supportedIntents: ['ClassifyDocument'],
      supportedModules: ['documents']
    });
    const executor = new AgentExecutor({
      approvals,
      authorization
    });
    const task = createTask({
      id: 'task-sensitive',
      title: 'Sensitive classification',
      description: 'Requires approval',
      agentId: 'agent-documents',
      intent: 'ClassifyDocument',
      priority: AgentPriority.Normal,
      mode: TaskMode.Sequential,
      metadata: { sensitive: true, approvalReferenceId: 'approval-sensitive' }
    });

    const execution = await executor.execute(agent, task, createAgentContext({
      brainSessionId: 'brain-2',
      permissions: ['documents:classify'],
      approvedDelegations: [],
      metadata: { brainControlled: true }
    }));

    expect(execution.status).toBe(ExecutionStatus.WaitingApproval);
    expect(execution.error).toMatch(/approval/i);

    const approval = approvals.request(createApprovalRequest({
      id: 'approval-sensitive',
      referenceId: 'approval-sensitive',
      title: 'Approve sensitive classification',
      description: 'Approve the documents task',
      requestedBy: 'lawim-brain',
      targetAgentId: 'agent-documents',
      sensitive: true
    }));
    approvals.approve(approval.id, 'lawim-brain');
    expect(approvals.hasApproved('approval-sensitive')).toBe(true);
    expect(approvals.list(ApprovalStatus.Approved)).toHaveLength(1);
  });
});
