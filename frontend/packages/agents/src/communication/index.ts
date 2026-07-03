import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const communicationAgentId = 'agent-communication';

export function createCommunicationAgent() {
  return createDomainAgent({
    id: communicationAgentId,
    name: 'Communication Agent',
    description: 'Prepares reminders, messages, and notification routing without deciding business content.',
    module: 'communication',
    capabilities: ['message-preparation', 'reminder-coordination', 'notification-routing'],
    permissions: ['communication:prepare', 'communication:send'],
    supportedIntents: ['SendReminder', 'PrepareMessage', 'RouteNotification'],
    dependencies: ['assistant-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Communication coordination prepared for the Brain.',
    recommendations: ['Keep reminder content under human approval for sensitive workflows.'],
    nextSteps: ['Queue reminder delivery and wait for explicit authorization.']
  });
}
