import { describe, expect, it } from 'vitest';
import { PolicyEngine, createDefaultPolicies } from '@agents';

describe('agent policies', () => {
  it('blocks critical delegations and flags sensitive actions for approval', () => {
    const engine = new PolicyEngine(createDefaultPolicies());

    const blocked = engine.evaluate('critical-delegation', {
      permissions: [],
      metadata: { brainControlled: true },
      mode: 'business',
      now: '2026-07-03T09:00:00.000Z'
    });

    const sensitive = engine.evaluate('SendReminder', {
      permissions: [],
      metadata: { brainControlled: true, sensitive: true },
      mode: 'business',
      now: '2026-07-03T09:00:00.000Z'
    });

    expect(blocked.allowed).toBe(false);
    expect(blocked.reason).toMatch(/critical/i);
    expect(sensitive.allowed).toBe(true);
    expect(sensitive.requiresApproval).toBe(true);
  });
});
