import { AgentAvailability, AgentHealth, createDomainAgent } from '../core';

export const documentsAgentId = 'agent-documents';

export function createDocumentsAgent() {
  return createDomainAgent({
    id: documentsAgentId,
    name: 'Documents Agent',
    description: 'Classifies and prepares documents while preserving human control over sensitive processing.',
    module: 'documents',
    capabilities: ['document-classification', 'template-preparation', 'metadata-extraction'],
    permissions: ['documents:classify', 'documents:prepare'],
    supportedIntents: ['ClassifyDocument', 'GenerateDocument', 'ExtractMetadata'],
    dependencies: ['knowledge-agent'],
    health: AgentHealth.Healthy,
    availability: AgentAvailability.Available,
    summary: 'Document coordination prepared for approval.',
    recommendations: ['Use the Brain to confirm whether a document requires review before release.'],
    nextSteps: ['Assemble the document classification proposal and route approval.']
  });
}
