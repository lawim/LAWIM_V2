import { describe, expect, it } from 'vitest';
import { createDelegationRequest, DelegationManager, DelegationStatus } from '@agents';

describe('agent delegations', () => {
  it('tracks pending approvals and blocks critical delegations', () => {
    const manager = new DelegationManager();
    const reminder = manager.request(
      createDelegationRequest({
        id: 'delegation-reminder',
        action: {
          id: 'action-reminder',
          name: 'Send reminders',
          description: 'Prepare reminder messages for human approval',
          targetAgentId: 'agent-communication',
          intent: 'SendReminder',
          critical: false
        },
        requestedBy: 'lawim-brain'
      })
    );

    expect(reminder.status).toBe(DelegationStatus.Pending);
    expect(manager.pending()).toHaveLength(1);

    const approved = manager.approve(reminder.id, 'lawim-brain', 'Approved for mock coordination');
    expect(approved?.status).toBe(DelegationStatus.Approved);
    expect(manager.allows(reminder.id)).toBe(true);

    const critical = manager.request(
      createDelegationRequest({
        id: 'delegation-critical',
        action: {
          id: 'action-critical',
          name: 'Critical release',
          description: 'A critical operation that remains forbidden',
          targetAgentId: 'agent-deployment',
          intent: 'PrepareRelease',
          critical: true
        },
        requestedBy: 'lawim-brain'
      })
    );

    expect(critical.status).toBe(DelegationStatus.Rejected);
    expect(critical.reason).toMatch(/forbidden/i);
    expect(manager.summary().rejected).toBe(1);
  });
});
