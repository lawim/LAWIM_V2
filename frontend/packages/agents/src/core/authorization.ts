import type { Agent } from './agent';
import type { AgentTask } from './tasks';
import type { ApprovalQueue } from './approvals';
import type { DelegationManager } from './delegations';
import { PolicyEngine, type PolicyEvaluation } from './policies';

export interface AuthorizationDecision {
  allowed: boolean;
  requiresApproval: boolean;
  reason: string;
  policy: PolicyEvaluation;
  missingPermissions: string[];
  approvalReferenceId?: string;
}

export interface AuthorizationEnvironment {
  policyEngine?: PolicyEngine;
  approvals?: ApprovalQueue;
  delegations?: DelegationManager;
}

export class AgentAuthorization {
  constructor(private readonly environment: AuthorizationEnvironment = {}) {}

  authorize(agent: Agent, task: AgentTask, context: { permissions: string[]; metadata?: Record<string, unknown>; approvedDelegations: string[]; mode: string; now?: string }): AuthorizationDecision {
    const policyEngine = this.environment.policyEngine ?? new PolicyEngine();
    const policy = policyEngine.evaluate(task.intent, context);
    const missingPermissions = agent.permissions.filter((permission) => !context.permissions.includes(permission));
    const sensitive = Boolean(task.metadata?.sensitive) || agent.capabilities.some((capability) => capability.requiresApproval) || policy.requiresApproval;
    const approvalReferenceId = String(task.metadata?.approvalReferenceId ?? task.id);

    if (missingPermissions.length > 0) {
      return {
        allowed: false,
        requiresApproval: false,
        reason: `Missing permissions: ${missingPermissions.join(', ')}`,
        policy,
        missingPermissions,
        approvalReferenceId
      };
    }

    if (!policy.allowed) {
      return {
        allowed: false,
        requiresApproval: policy.requiresApproval,
        reason: policy.reason,
        policy,
        missingPermissions,
        approvalReferenceId
      };
    }

    const approvalQueue = this.environment.approvals;
    const delegationManager = this.environment.delegations;
    const approvedByDelegation = task.approvedDelegations.some((delegationId) => delegationManager?.allows(delegationId) ?? false);
    const approvedByQueue = approvalQueue?.hasApproved(approvalReferenceId) ?? false;
    const contextApproved = context.approvedDelegations.includes(approvalReferenceId);

    if (sensitive && !(approvedByDelegation || approvedByQueue || contextApproved)) {
      return {
        allowed: false,
        requiresApproval: true,
        reason: 'Sensitive action awaits human approval',
        policy,
        missingPermissions,
        approvalReferenceId
      };
    }

    return {
      allowed: true,
      requiresApproval: false,
      reason: approvedByDelegation || approvedByQueue || contextApproved ? 'Approved delegation available' : 'Allowed by policy',
      policy,
      missingPermissions,
      approvalReferenceId
    };
  }
}
