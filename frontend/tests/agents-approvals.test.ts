import { describe, expect, it } from 'vitest';
import { ApprovalQueue, ApprovalStatus, createApprovalRequest } from '@agents';

describe('agent approvals', () => {
  it('tracks request history, notifications, and approval status', () => {
    const queue = new ApprovalQueue();
    const request = queue.request(
      createApprovalRequest({
        id: 'approval-1',
        referenceId: 'approval-1',
        title: 'Approve lead preparation',
        description: 'Allow the CRM agent to prepare a lead proposal.',
        requestedBy: 'lawim-brain',
        targetAgentId: 'agent-crm',
        sensitive: true
      })
    );

    expect(request.status).toBe(ApprovalStatus.Pending);
    expect(queue.pending()).toHaveLength(1);
    expect(queue.notifications()).toHaveLength(1);

    const approved = queue.approve(request.id, 'lawim-brain', 'Approved for demo runtime');
    expect(approved?.status).toBe(ApprovalStatus.Approved);
    expect(queue.hasApproved('approval-1')).toBe(true);
    expect(queue.history()).toHaveLength(2);
    expect(queue.summary().approved).toBe(1);
  });
});
