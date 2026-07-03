import { describe, expect, it } from 'vitest';
import { AgentPriority, AgentStatus, TaskMode, createAgentContext, createAgentResult, createTask } from '@agents';

describe('agent core', () => {
  it('creates deterministic contexts, tasks, and results', () => {
    const context = createAgentContext({
      brainSessionId: 'brain-session-1',
      permissions: ['crm:prepare'],
      approvedDelegations: ['delegation-1']
    });

    const task = createTask({
      id: 'task-1',
      title: 'Prepare lead',
      description: 'Prepare a CRM lead package',
      agentId: 'agent-crm',
      intent: 'CreateLead',
      priority: AgentPriority.High,
      mode: TaskMode.Sequential
    });

    const result = createAgentResult({ summary: 'Lead package prepared' });

    expect(context.brainSessionId).toBe('brain-session-1');
    expect(task.priority).toBe(AgentPriority.High);
    expect(task.mode).toBe(TaskMode.Sequential);
    expect(result.status).toBe(AgentStatus.Succeeded);
    expect(result.summary).toContain('Lead package');
  });
});
