# Agent Policies

Policies constrain the agent platform.

## Elements

- Rules
- Constraints
- Permissions
- Rate limits
- Execution windows
- Business restrictions

## Behavior

- Sensitive actions are flagged for human review.
- Critical delegations remain forbidden.
- The Brain must remain in control of execution.
- Policy evaluation is deterministic and mock friendly.

## Authorization

- `AgentAuthorization` combines policy checks with approval and delegation checks.
- If a task is not authorized, the executor returns a waiting or failed state instead of proceeding.
