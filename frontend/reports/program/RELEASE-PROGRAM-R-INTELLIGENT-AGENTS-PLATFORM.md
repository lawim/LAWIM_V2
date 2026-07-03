# RELEASE PROGRAM R - INTELLIGENT AGENTS PLATFORM

## 1. Architecture of Agents

The LAWIM agent platform was added as a new frontend-only coordination layer under `frontend/packages/agents/`.
It provides a shared core for registry, execution, policies, delegations, approvals, observability, memory, and eventing.

## 2. Agent Registry

`AgentRegistry` is the discovery source for the Brain.
Each agent exposes id, name, description, version, capabilities, permissions, health, availability, supported intents, supported modules, and dependencies.

## 3. Agent Core

The core includes:

- `Agent`
- `AgentCapability`
- `AgentExecution`
- `AgentTask`
- `AgentContext`
- `AgentResult`
- `AgentStatus`
- `AgentHealth`
- `AgentPriority`
- `AgentPolicy`
- `AgentAuthorization`
- `AgentScheduler`
- `AgentQueue`
- `AgentMetrics`
- `AgentLogger`
- `AgentHistory`
- `AgentAudit`

## 4. Business Agents

The platform includes CRM, Marketplace, Documents, Communication, Analytics, Security, Operations, Deployment, Backup, Assistant, Knowledge, Workflow, and Map agents.
They coordinate only and never replace business ownership.

## 5. Delegations

Delegation management supports inactive, pending, approved, rejected, revoked, and expired states.
Critical delegations are rejected by policy.

## 6. Policies

Policy structures cover rules, constraints, permissions, rate limits, execution windows, and business restrictions.
Authorization remains deterministic and mock-friendly.

## 7. Human Approvals

Sensitive actions are routed through approval requests, queue, history, notifications, and dashboard views.

## 8. Multi-Agent Orchestration

The scheduler builds execution graphs and pipelines for parallel, sequential, and conditional tasks.
Retry and rollback metadata are preserved in execution records.

## 9. Observability

The platform records logs, metrics, history, and audit events.
The dashboard exposes execution timelines, success and failure rates, retries, and durations.

## 10. Dashboard

`AgentsConsolePage` is now available in the admin console.
It renders the official agent overview and the detailed `AgentDashboard` surface.

## 11. Tests

Coverage was added for:

- agent core
- registry
- delegations
- execution
- approvals
- policies
- dashboard
- metrics
- Brain to agent-registry integration

## 12. Documentation

Dedicated docs were added for:

- `AGENTS.md`
- `AGENT_REGISTRY.md`
- `AGENT_POLICIES.md`
- `AGENT_DELEGATIONS.md`
- `AGENT_EXECUTION.md`
- `AGENT_DASHBOARD.md`

## 13. Compatibility A to Q

The release is additive.
No backend code was changed.
No existing API or schema was modified.
No prior module was removed or rewritten.

## 14. Preparation for LAWIM 2.0

This release establishes the official coordination substrate for next-generation agent workflows, approval handling, and admin observability.
It gives LAWIM 2.0 a stable frontend foundation for agent orchestration.

## 15. Preparation for LAWIM 3.0

The current design keeps the platform open for future execution backends, richer policy engines, and deeper multi-agent pipelines.
LAWIM 3.0 can evolve from this registry-first, Brain-controlled foundation without breaking earlier releases.
