import { describe, expect, it } from 'vitest';
import { BrainOrchestrator, BrainRegistry, createDemoBrainContext, createDemoIntent } from '../packages/brain/src';

describe('Brain foundation', () => {
  it('builds an execution plan from a user intent', async () => {
    const registry = new BrainRegistry();
    registry.register({
      name: 'search',
      description: 'Property search',
      capabilities: ['search'],
      supportedIntents: ['SearchProperty'],
      priority: 1,
      health: 'healthy',
      availability: 'available',
      async execute() {
        return { outcome: 'search-complete', summary: 'Found matching properties' };
      }
    });

    const orchestrator = new BrainOrchestrator(registry);
    const result = await orchestrator.orchestrate(createDemoIntent('SearchProperty', 'Find a townhouse in Paris'), createDemoBrainContext());

    expect(result.plan.steps.length).toBeGreaterThan(0);
    expect(result.finalMessage).toContain('Paris');
  });
});
