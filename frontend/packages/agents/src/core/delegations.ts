export enum DelegationStatus {
  Inactive = 'inactive',
  Pending = 'pending',
  Approved = 'approved',
  Rejected = 'rejected',
  Revoked = 'revoked',
  Expired = 'expired'
}

export interface DelegationAction {
  id: string;
  name: string;
  description: string;
  targetAgentId: string;
  intent: string;
  critical: boolean;
  metadata?: Record<string, unknown>;
}

export interface AgentDelegation {
  id: string;
  action: DelegationAction;
  requestedBy: string;
  requestedAt: string;
  status: DelegationStatus;
  approvedBy?: string;
  reviewedAt?: string;
  reason?: string;
  expiresAt?: string;
  metadata?: Record<string, unknown>;
}

export interface DelegationRequest extends Omit<AgentDelegation, 'status'> {
  status?: DelegationStatus;
}

export function createDelegationRequest(
  overrides: Omit<Partial<DelegationRequest>, 'id' | 'action' | 'requestedBy' | 'requestedAt'> & {
    id: string;
    action: DelegationAction;
    requestedBy: string;
    requestedAt?: string;
  }
): AgentDelegation {
  return {
    id: overrides.id,
    action: overrides.action,
    requestedBy: overrides.requestedBy,
    requestedAt: overrides.requestedAt ?? new Date().toISOString(),
    status: overrides.status ?? DelegationStatus.Inactive,
    approvedBy: overrides.approvedBy,
    reviewedAt: overrides.reviewedAt,
    reason: overrides.reason,
    expiresAt: overrides.expiresAt,
    metadata: overrides.metadata
  };
}

export class DelegationManager {
  private readonly delegations = new Map<string, AgentDelegation>();

  request(request: DelegationRequest) {
    const current = createDelegationRequest({
      ...request,
      requestedAt: request.requestedAt ?? new Date().toISOString(),
      status: request.action.critical
        ? DelegationStatus.Rejected
        : request.status === DelegationStatus.Inactive
          ? DelegationStatus.Pending
          : request.status ?? DelegationStatus.Pending
    });

    if (request.action.critical) {
      current.reason = 'Critical delegations are forbidden';
    }

    this.delegations.set(current.id, current);
    return current;
  }

  approve(delegationId: string, approvedBy: string, reason?: string) {
    return this.transition(delegationId, DelegationStatus.Approved, approvedBy, reason);
  }

  reject(delegationId: string, reviewedBy: string, reason?: string) {
    return this.transition(delegationId, DelegationStatus.Rejected, reviewedBy, reason);
  }

  revoke(delegationId: string, reviewedBy: string, reason?: string) {
    return this.transition(delegationId, DelegationStatus.Revoked, reviewedBy, reason);
  }

  expire(delegationId: string, reviewedBy: string, reason?: string) {
    return this.transition(delegationId, DelegationStatus.Expired, reviewedBy, reason);
  }

  list(status?: DelegationStatus) {
    const items = [...this.delegations.values()];
    return status ? items.filter((delegation) => delegation.status === status) : items;
  }

  pending() {
    return this.list(DelegationStatus.Pending);
  }

  approved() {
    return this.list(DelegationStatus.Approved);
  }

  inactive() {
    return this.list(DelegationStatus.Inactive);
  }

  history() {
    return this.list();
  }

  get(delegationId: string) {
    return this.delegations.get(delegationId);
  }

  allows(delegationId: string) {
    return this.get(delegationId)?.status === DelegationStatus.Approved;
  }

  summary() {
    const requests = this.list();
    return {
      total: requests.length,
      inactive: requests.filter((request) => request.status === DelegationStatus.Inactive).length,
      pending: requests.filter((request) => request.status === DelegationStatus.Pending).length,
      approved: requests.filter((request) => request.status === DelegationStatus.Approved).length,
      rejected: requests.filter((request) => request.status === DelegationStatus.Rejected).length,
      revoked: requests.filter((request) => request.status === DelegationStatus.Revoked).length,
      expired: requests.filter((request) => request.status === DelegationStatus.Expired).length
    };
  }

  private transition(delegationId: string, status: DelegationStatus, reviewedBy: string, reason?: string) {
    const current = this.delegations.get(delegationId);
    if (!current) {
      return undefined;
    }

    const updated: AgentDelegation = {
      ...current,
      status,
      approvedBy: status === DelegationStatus.Approved ? reviewedBy : current.approvedBy,
      reviewedAt: new Date().toISOString(),
      reason: reason ?? current.reason
    };

    this.delegations.set(delegationId, updated);
    return updated;
  }
}
