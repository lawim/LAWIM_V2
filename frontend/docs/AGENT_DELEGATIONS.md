# Agent Delegations

Delegations define what an agent is allowed to prepare or execute.

## Statuses

- `inactive`
- `pending`
- `approved`
- `rejected`
- `revoked`
- `expired`

## Lifecycle

- `request()` submits a delegation.
- `approve()` authorizes it.
- `reject()` blocks it.
- `revoke()` removes an approval.
- `expire()` closes the delegation.

## Rules

- Critical delegations are rejected immediately.
- Noncritical delegations can remain pending for human review.
- Approval history is recorded for auditability.
