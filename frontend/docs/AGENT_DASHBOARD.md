# Agent Dashboard

The administration dashboard surfaces the agent platform state.

## Sections

- Agent Registry
- Agent Health
- Running Tasks
- Execution Graph
- Delegations
- Policies
- Approvals
- Agent History
- Agent Metrics
- Agent Logs

## Implementation

- `AgentsConsolePage` renders the official admin entry point.
- `AgentDashboard` renders the detailed operational view.
- `ApprovalDashboard` renders approval queue state and notifications.

## Mock Runtime

- The dashboard works without backend connectivity.
- Demo data is seeded from `createMockAgentPlatform()`.
