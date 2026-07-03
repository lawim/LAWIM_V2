import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const marketplaceAgentId = 'agent-marketplace';

export function createMarketplaceAgent() {
  return createDomainAgent({
    id: marketplaceAgentId,
    name: 'Marketplace Agent',
    description: 'Prepares marketplace coordination for offers, listings, and publication workflows.',
    module: 'marketplace',
    capabilities: ['offer-coordination', 'listing-preparation', 'publication-routing'],
    permissions: ['marketplace:prepare'],
    supportedIntents: ['PrepareListing', 'ReviewOffer', 'PublishOffer'],
    dependencies: ['workflow-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Marketplace coordination staged for review.',
    recommendations: ['Let the Brain confirm listing visibility and publication scope.'],
    nextSteps: ['Prepare the offer package and queue the publishing delegation.']
  });
}
