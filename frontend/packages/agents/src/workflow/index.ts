import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const workflowAgentId = 'agent-workflow';

export function createWorkflowAgent() {
  return createDomainAgent({
    id: workflowAgentId,
    name: 'Workflow Agent',
    description: 'Builds coordination graphs, dependencies, and execution proposals for the Brain.',
    module: 'workflow',
    capabilities: ['task-orchestration', 'dependency-mapping', 'automation-design'],
    permissions: ['workflow:prepare'],
    supportedIntents: ['BuildWorkflow', 'OrchestrateTasks', 'DesignAutomation'],
    dependencies: ['assistant-agent', 'knowledge-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Workflow graph prepared without changing the underlying business rules.',
    recommendations: ['Use the Brain to approve each proposed automation step.'],
    nextSteps: ['Draft the execution graph and await delegation review.']
  });
}
