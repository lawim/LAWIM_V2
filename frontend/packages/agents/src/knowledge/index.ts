import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const knowledgeAgentId = 'agent-knowledge';

export function createKnowledgeAgent() {
  return createDomainAgent({
    id: knowledgeAgentId,
    name: 'Knowledge Agent',
    description: 'Aggregates context, retrieves references, and prepares evidence for review.',
    module: 'knowledge',
    capabilities: ['knowledge-retrieval', 'context-assembly', 'evidence-preparation'],
    permissions: ['knowledge:read', 'knowledge:prepare'],
    supportedIntents: ['RetrieveKnowledge', 'BuildContext', 'PrepareEvidence'],
    dependencies: [],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Knowledge context staged for higher-level orchestration.',
    recommendations: ['Keep evidence summaries short and reviewable by the Brain.'],
    nextSteps: ['Provide the knowledge packet to dependent agents.']
  });
}
