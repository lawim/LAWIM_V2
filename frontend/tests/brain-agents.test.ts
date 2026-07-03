import { describe, expect, it } from 'vitest';
import { BrainOrchestrator, BrainRegistry, createDemoBrainContext, createDemoIntent } from '../packages/brain/src';
import { createMockAgentPlatform } from '@agents';

describe('brain to agent registry integration', () => {
  it('includes agent candidates from the official registry', async () => {
    const brainRegistry = new BrainRegistry();
    brainRegistry.register({
      name: 'search',
      description: 'Search module',
      capabilities: ['search'],
      supportedIntents: ['CreateLead'],
      priority: 1,
      health: 'healthy',
      availability: 'available',
      async execute() {
        return { outcome: 'ready' };
      }
    });

    const agentPlatform = createMockAgentPlatform();
    const orchestrator = new BrainOrchestrator(brainRegistry, agentPlatform.registry);
    const result = await orchestrator.orchestrate(createDemoIntent('CreateLead', 'Prepare a lead proposal'), createDemoBrainContext());

    expect(result.plan.agentCandidates?.[0]?.agentName).toBe('CRM Agent');
    expect(result.plan.agentCandidates?.[0]?.intent).toBe('CreateLead');
  });
});
