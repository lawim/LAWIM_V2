import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const mapAgentId = 'agent-map';

export function createMapAgent() {
  return createDomainAgent({
    id: mapAgentId,
    name: 'Map Agent',
    description: 'Prepares spatial context, routing cues, and geographic summaries for the Brain.',
    module: 'maps',
    capabilities: ['location-context', 'spatial-routing', 'geo-summary'],
    permissions: ['maps:read', 'maps:prepare'],
    supportedIntents: ['AnalyzeLocation', 'PlanRoute', 'AssessCoverage'],
    dependencies: ['knowledge-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Spatial context prepared without selecting a final route.',
    recommendations: ['Let human review confirm the final location decision.'],
    nextSteps: ['Prepare the map proposal and await authorization.']
  });
}
