import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const operationsAgentId = 'agent-operations';
export const deploymentAgentId = 'agent-deployment';
export const backupAgentId = 'agent-backup';

export function createOperationsAgent() {
  return createDomainAgent({
    id: operationsAgentId,
    name: 'Operations Agent',
    description: 'Coordinates operational queues, incidents, and execution proposals for the Brain.',
    module: 'operations',
    capabilities: ['queue-coordination', 'incident-triage', 'resource-observation'],
    permissions: ['operations:coordinate', 'operations:prepare'],
    supportedIntents: ['CoordinateOperations', 'TrackIncident', 'ReviewQueue'],
    dependencies: ['workflow-agent', 'knowledge-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Operations coordination prepared for human control.',
    recommendations: ['Keep incident triage in proposal mode only.'],
    nextSteps: ['Route the incident summary to the Brain review queue.']
  });
}

export function createDeploymentAgent() {
  return createDomainAgent({
    id: deploymentAgentId,
    name: 'Deployment Agent',
    description: 'Prepares release checklists and rollout coordination while the Brain retains the decision.',
    module: 'deployment',
    capabilities: ['release-coordination', 'rollout-checklist', 'environment-readiness'],
    permissions: ['deployment:prepare'],
    supportedIntents: ['PrepareRelease', 'AssessRollout', 'ReviewDeployment'],
    dependencies: ['operations-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Deployment rollout plan prepared for approval.',
    recommendations: ['Use the Brain to approve each rollout gate.'],
    nextSteps: ['Generate the release proposal and wait for the human decision.']
  });
}

export function createBackupAgent() {
  return createDomainAgent({
    id: backupAgentId,
    name: 'Backup Agent',
    description: 'Prepares backup coordination and restore readiness without initiating irreversible actions.',
    module: 'backup',
    capabilities: ['backup-preparation', 'restore-readiness', 'retention-review'],
    permissions: ['backup:prepare'],
    supportedIntents: ['CreateBackup', 'ReviewRestore', 'InspectRetention'],
    dependencies: ['operations-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Backup coordination prepared and waiting on authorization.',
    recommendations: ['Create backup proposals only after explicit approval.'],
    nextSteps: ['Queue the backup request and ask the Brain for authorization.']
  });
}
