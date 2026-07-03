import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const securityAgentId = 'agent-security';

export function createSecurityAgent() {
  return createDomainAgent({
    id: securityAgentId,
    name: 'Security Agent',
    description: 'Coordinates policy review, risk triage, and access preparation under strict human control.',
    module: 'security',
    capabilities: ['risk-triage', 'policy-review', 'access-preparation'],
    permissions: ['security:review', 'security:prepare'],
    supportedIntents: ['ReviewAccess', 'InspectRisk', 'PrepareSecurityCheck'],
    dependencies: ['knowledge-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Restricted,
    summary: 'Security coordination staged with restricted availability.',
    recommendations: ['Escalate sensitive security actions to the approval queue immediately.'],
    nextSteps: ['Prepare the risk synopsis and await governance review.']
  });
}
