export interface PolicyRule {
  id: string;
  description: string;
  effect: 'allow' | 'deny' | 'review';
  when: string;
}

export interface PolicyConstraint {
  id: string;
  description: string;
  field: string;
  operator: 'eq' | 'neq' | 'gte' | 'lte' | 'includes';
  value: string | number | boolean;
}

export interface PolicyPermission {
  scope: string;
  action: string;
  requiresApproval?: boolean;
}

export interface RateLimitPolicy {
  id: string;
  scope: string;
  max: number;
  perMinutes: number;
}

export interface ExecutionWindow {
  id: string;
  label: string;
  timezone: string;
  startHour: number;
  endHour: number;
  daysOfWeek?: number[];
}

export interface BusinessRestriction {
  id: string;
  description: string;
  blockedActions: string[];
  critical: boolean;
}

export interface AgentPolicy {
  id: string;
  name: string;
  description: string;
  rules: PolicyRule[];
  constraints: PolicyConstraint[];
  permissions: PolicyPermission[];
  rateLimits: RateLimitPolicy[];
  executionWindows: ExecutionWindow[];
  businessRestrictions: BusinessRestriction[];
}

export interface PolicyEvaluation {
  allowed: boolean;
  requiresApproval: boolean;
  reason: string;
  matchedRules: string[];
}

export function createDefaultPolicies(): AgentPolicy[] {
  return [
    {
      id: 'policy-safety-default',
      name: 'Safety Default',
      description: 'Default coordination policy for the agent platform.',
      rules: [
        { id: 'rule-review-sensitive', description: 'Sensitive actions require review', effect: 'review', when: 'sensitive === true' },
        { id: 'rule-allow-standard', description: 'Standard actions may proceed', effect: 'allow', when: 'sensitive === false' }
      ],
      constraints: [
        { id: 'constraint-brain-control', description: 'Brain must authorize execution', field: 'brainControlled', operator: 'eq', value: true }
      ],
      permissions: [
        { scope: 'delegation', action: 'request', requiresApproval: true },
        { scope: 'execution', action: 'prepare', requiresApproval: false }
      ],
      rateLimits: [{ id: 'limit-default', scope: 'coordinator', max: 100, perMinutes: 60 }],
      executionWindows: [{ id: 'window-global', label: '24/7 coordination', timezone: 'UTC', startHour: 0, endHour: 23 }],
      businessRestrictions: [
        {
          id: 'restriction-critical',
          description: 'Critical delegations remain forbidden',
          blockedActions: ['critical-delegation'],
          critical: true
        }
      ]
    }
  ];
}

export class PolicyEngine {
  constructor(private readonly policies: AgentPolicy[] = createDefaultPolicies()) {}

  evaluate(action: string, context: { metadata?: Record<string, unknown>; permissions: string[]; now?: string; mode: string }): PolicyEvaluation {
    const matchedRules: string[] = [];
    const sensitive = Boolean(context.metadata?.sensitive);
    const brainControlled = context.metadata?.brainControlled !== false;

    for (const policy of this.policies) {
      for (const rule of policy.rules) {
        if (rule.effect === 'review' && sensitive) {
          matchedRules.push(rule.id);
        }
        if (rule.effect === 'deny' && String(context.metadata?.[rule.when]) === 'true') {
          return {
            allowed: false,
            requiresApproval: false,
            reason: `Denied by ${rule.id}`,
            matchedRules
          };
        }
      }

      for (const restriction of policy.businessRestrictions) {
        if (restriction.blockedActions.includes(action)) {
          return {
            allowed: false,
            requiresApproval: false,
            reason: restriction.critical ? `Critical restriction: ${restriction.description}` : restriction.description,
            matchedRules
          };
        }
      }

      for (const permission of policy.permissions) {
        if (permission.action === action && permission.requiresApproval) {
          return {
            allowed: true,
            requiresApproval: true,
            reason: `Approval required by policy ${policy.id}`,
            matchedRules: [...matchedRules, policy.id]
          };
        }
      }

      if (!brainControlled) {
        return {
          allowed: false,
          requiresApproval: false,
          reason: 'Execution is not brain controlled',
          matchedRules
        };
      }
    }

    return {
      allowed: true,
      requiresApproval: sensitive,
      reason: sensitive ? 'Sensitive action routed to approval' : 'Allowed by policy',
      matchedRules
    };
  }

  describe() {
    return this.policies.map((policy) => ({
      id: policy.id,
      name: policy.name,
      rules: policy.rules.length,
      constraints: policy.constraints.length,
      permissions: policy.permissions.length,
      rateLimits: policy.rateLimits.length,
      executionWindows: policy.executionWindows.length,
      businessRestrictions: policy.businessRestrictions.length
    }));
  }
}
