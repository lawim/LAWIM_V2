import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const assistantAgentId = 'agent-assistant';

export function createAssistantAgent() {
  return createDomainAgent({
    id: assistantAgentId,
    name: 'Assistant Agent',
    description: 'Provides intake, guidance, and orchestration suggestions without making decisions.',
    module: 'assistant',
    capabilities: ['intake-routing', 'summarization', 'proposal-writing'],
    permissions: ['assistant:read', 'assistant:prepare'],
    supportedIntents: ['AssistUser', 'SummarizeContext', 'PrepareProposal'],
    dependencies: ['knowledge-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Assistant coordination ready for the Brain.',
    recommendations: ['Always keep the Brain in control of the final output.'],
    nextSteps: ['Prepare the proposal draft for the appropriate domain agent.']
  });
}
