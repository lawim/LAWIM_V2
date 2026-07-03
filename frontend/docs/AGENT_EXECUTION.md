# Agent Execution

Execution is mock-backed and Brain-controlled.

## Core Objects

- `AgentTask`
- `SubTask`
- `ExecutionPlan`
- `ExecutionGraph`
- `ExecutionPipeline`
- `RetryPolicy`
- `TimeoutPolicy`
- `RollbackInformation`

## Runtime Flow

1. The Brain resolves the intent against the agent registry.
2. The scheduler builds the graph and pipeline.
3. The authorization layer checks policy, delegation, and approvals.
4. The executor runs the agent proposal.
5. History, metrics, logs, and audit entries are recorded.

## Safeguards

- Approval-gated tasks pause instead of executing.
- Retry is supported for transient failures.
- Rollback metadata is preserved for failed executions.
