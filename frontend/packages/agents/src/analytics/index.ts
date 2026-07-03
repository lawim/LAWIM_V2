import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const analyticsAgentId = 'agent-analytics';

export function createAnalyticsAgent() {
  return createDomainAgent({
    id: analyticsAgentId,
    name: 'Analytics Agent',
    description: 'Synthesizes metrics, trends, and operational summaries for review by the Brain.',
    module: 'analytics',
    capabilities: ['trend-synthesis', 'report-preparation', 'metric-monitoring'],
    permissions: ['analytics:read', 'analytics:prepare'],
    supportedIntents: ['AnalyzeMetrics', 'GenerateReport', 'MonitorTrend'],
    dependencies: ['knowledge-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Analytics context prepared for human review.',
    recommendations: ['Use the synthesized metrics as a proposal layer only.'],
    nextSteps: ['Prepare a report draft and await the Brain decision.']
  });
}
