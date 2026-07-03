import { describe, expect, it } from 'vitest';
import { createAgentRegistry, createMockAgentPlatform } from '@agents';

describe('agent registry', () => {
  it('registers the full agent set and resolves intents', () => {
    const platform = createMockAgentPlatform();

    expect(platform.registry.list()).toHaveLength(13);
    expect(platform.registry.healthy()).toHaveLength(13);

    const leadCandidates = platform.registry.resolveIntent('CreateLead');
    expect(leadCandidates[0]?.name).toBe('CRM Agent');
    expect(platform.registry.createRoutingPlan('SendReminder')[0]?.agentName).toBe('Communication Agent');
    expect(platform.registry.snapshot().agents.some((agent) => agent.id === 'agent-map')).toBe(true);
  });

  it('supports dynamic registration and removal', () => {
    const platform = createMockAgentPlatform();
    const registry = createAgentRegistry();
    const crmAgent = platform.registry.get('agent-crm');

    expect(crmAgent).toBeDefined();

    if (crmAgent) {
      registry.register(crmAgent);
      expect(registry.list()).toHaveLength(1);
      expect(registry.unregister(crmAgent.id)?.id).toBe(crmAgent.id);
    }

    expect(registry.list()).toHaveLength(0);
  });
});
