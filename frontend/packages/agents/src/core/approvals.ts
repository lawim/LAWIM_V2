export enum ApprovalStatus {
  Inactive = 'inactive',
  Pending = 'pending',
  Approved = 'approved',
  Rejected = 'rejected',
  Revoked = 'revoked',
  Expired = 'expired'
}

export interface ApprovalRequest {
  id: string;
  referenceId: string;
  title: string;
  description: string;
  requestedBy: string;
  targetAgentId?: string;
  sensitive: boolean;
  status: ApprovalStatus;
  createdAt: string;
  updatedAt: string;
  reviewedBy?: string;
  reviewedAt?: string;
  reason?: string;
  metadata?: Record<string, unknown>;
}

export interface ApprovalNotification {
  id: string;
  requestId: string;
  message: string;
  channel: 'dashboard' | 'in-app' | 'email';
  createdAt: string;
  readAt?: string;
}

export interface ApprovalEvent {
  id: string;
  requestId: string;
  status: ApprovalStatus;
  actor: string;
  timestamp: string;
  note?: string;
}

export function createApprovalRequest(
  overrides: Omit<Partial<ApprovalRequest>, 'id' | 'referenceId'> & { id: string; referenceId: string; title: string; description: string; requestedBy: string }
): ApprovalRequest {
  const now = overrides.createdAt ?? new Date().toISOString();
  return {
    id: overrides.id,
    referenceId: overrides.referenceId,
    title: overrides.title,
    description: overrides.description,
    requestedBy: overrides.requestedBy,
    targetAgentId: overrides.targetAgentId,
    sensitive: overrides.sensitive ?? false,
    status: overrides.status ?? ApprovalStatus.Pending,
    createdAt: now,
    updatedAt: overrides.updatedAt ?? now,
    reviewedBy: overrides.reviewedBy,
    reviewedAt: overrides.reviewedAt,
    reason: overrides.reason,
    metadata: overrides.metadata
  };
}

export class ApprovalHistory {
  private readonly entries: ApprovalEvent[] = [];

  record(event: ApprovalEvent) {
    this.entries.push(event);
  }

  list() {
    return [...this.entries];
  }

  byRequest(requestId: string) {
    return this.entries.filter((event) => event.requestId === requestId);
  }
}

export class ApprovalQueue {
  private readonly requests = new Map<string, ApprovalRequest>();
  private readonly notificationLog: ApprovalNotification[] = [];

  constructor(private readonly historyStore = new ApprovalHistory()) {}

  request(request: ApprovalRequest) {
    const current = {
      ...request,
      status: request.status ?? ApprovalStatus.Pending,
      updatedAt: request.updatedAt ?? request.createdAt
    };
    this.requests.set(current.id, current);
    this.historyStore.record({
      id: `approval-event-${current.id}-pending`,
      requestId: current.id,
      status: current.status,
      actor: current.requestedBy,
      timestamp: current.updatedAt,
      note: 'Approval request created'
    });
    this.notificationLog.push({
      id: `approval-notification-${current.id}`,
      requestId: current.id,
      message: `${current.title} is awaiting human approval.`,
      channel: 'dashboard',
      createdAt: current.updatedAt
    });
    return current;
  }

  approve(requestId: string, reviewedBy: string, note?: string) {
    return this.transition(requestId, ApprovalStatus.Approved, reviewedBy, note);
  }

  reject(requestId: string, reviewedBy: string, note?: string) {
    return this.transition(requestId, ApprovalStatus.Rejected, reviewedBy, note);
  }

  revoke(requestId: string, reviewedBy: string, note?: string) {
    return this.transition(requestId, ApprovalStatus.Revoked, reviewedBy, note);
  }

  expire(requestId: string, reviewedBy: string, note?: string) {
    return this.transition(requestId, ApprovalStatus.Expired, reviewedBy, note);
  }

  list(status?: ApprovalStatus) {
    const items = [...this.requests.values()];
    return status ? items.filter((request) => request.status === status) : items;
  }

  pending() {
    return this.list(ApprovalStatus.Pending);
  }

  approved() {
    return this.list(ApprovalStatus.Approved);
  }

  history() {
    return this.historyStore.list();
  }

  notifications() {
    return [...this.notificationLog];
  }

  markRead(notificationId: string) {
    const notification = this.notificationLog.find((entry) => entry.id === notificationId);
    if (notification) {
      notification.readAt = new Date().toISOString();
    }
    return notification;
  }

  findByReference(referenceId: string) {
    return this.list().find((request) => request.referenceId === referenceId);
  }

  hasApproved(referenceId: string) {
    return this.list().some((request) => request.referenceId === referenceId && request.status === ApprovalStatus.Approved);
  }

  summary() {
    const requests = this.list();
    return {
      total: requests.length,
      pending: requests.filter((request) => request.status === ApprovalStatus.Pending).length,
      approved: requests.filter((request) => request.status === ApprovalStatus.Approved).length,
      rejected: requests.filter((request) => request.status === ApprovalStatus.Rejected).length,
      revoked: requests.filter((request) => request.status === ApprovalStatus.Revoked).length,
      expired: requests.filter((request) => request.status === ApprovalStatus.Expired).length
    };
  }

  private transition(requestId: string, status: ApprovalStatus, reviewedBy: string, note?: string) {
    const current = this.requests.get(requestId);
    if (!current) {
      return undefined;
    }

    const updated: ApprovalRequest = {
      ...current,
      status,
      reviewedBy,
      reviewedAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      reason: note ?? current.reason
    };

    this.requests.set(requestId, updated);
    this.historyStore.record({
      id: `approval-event-${requestId}-${status}`,
      requestId,
      status,
      actor: reviewedBy,
      timestamp: updated.updatedAt,
      note
    });
    this.notificationLog.push({
      id: `approval-notification-${requestId}-${status}`,
      requestId,
      message: `${updated.title} was marked ${status}.`,
      channel: 'dashboard',
      createdAt: updated.updatedAt
    });
    return updated;
  }
}
