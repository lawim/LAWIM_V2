import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const crmAgentId = 'agent-crm';

export function createCrmAgent() {
  return createDomainAgent({
    id: crmAgentId,
    name: 'CRM Agent',
    description: 'Coordinates lead preparation, follow-up packaging, and contact enrichment for the Brain.',
    module: 'crm',
    capabilities: ['lead-preparation', 'follow-up-coordination', 'contact-enrichment'],
    permissions: ['crm:prepare', 'crm:follow-up'],
    supportedIntents: ['CreateLead', 'PrepareFollowUp', 'EnrichContact'],
    dependencies: ['assistant-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'CRM coordination prepared without making a business decision.',
    recommendations: ['Route lead creation to human approval before persistence.'],
    nextSteps: ['Assemble the proposed lead payload and wait for Brain validation.']
  });
}
