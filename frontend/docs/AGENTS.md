# LAWIM Agents

This document describes the official intelligent agent layer for LAWIM V2.

## Principles

- Agents are coordination layers only.
- The LAWIM Brain keeps all business authority.
- Sensitive actions must go through approval and delegation controls.
- The frontend mock runtime must remain functional without backend access.

## Package Layout

- `frontend/packages/agents/src/core/`: shared types, registry, execution, policies, approvals, delegations, observability, and memory.
- `frontend/packages/agents/src/crm/`: CRM coordination agent.
- `frontend/packages/agents/src/marketplace/`: marketplace coordination agent.
- `frontend/packages/agents/src/documents/`: document coordination agent.
- `frontend/packages/agents/src/communication/`: communication coordination agent.
- `frontend/packages/agents/src/analytics/`: analytics coordination agent.
- `frontend/packages/agents/src/security/`: security coordination agent.
- `frontend/packages/agents/src/operations/`: operations, deployment, and backup coordination agents.
- `frontend/packages/agents/src/workflow/`: workflow coordination agent.
- `frontend/packages/agents/src/knowledge/`: knowledge coordination agent.
- `frontend/packages/agents/src/map/`: map and spatial coordination agent.

## Runtime

- Use `createMockAgentPlatform()` to seed a complete local runtime.
- Use `AgentRegistry` to inspect available agents and Brain routing candidates.
- Use `AgentDashboard` to visualize registry, health, approvals, delegations, metrics, logs, and execution history.

## Compatibility

- The assistant coordination agent was removed during Mission 2 decommissioning.
- No backend contract, schema, or frozen release behavior is changed.
- Existing A to Q modules remain intact.
