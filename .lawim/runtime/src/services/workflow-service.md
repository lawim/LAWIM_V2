# Service: Workflow Service

## Objective

Manage runtime workflow state and allowed transitions.

## Responsibilities

- Read the imported workflow contract.
- Validate transitions.
- Reject illegal status jumps.

## Inputs

- Ticket state.
- Workflow contract.
- Policy context.

## Outputs

- Normalized transition decision.
- Allowed next-state list.

## Critical errors

- Unknown state.
- Contract mismatch.
- Transition not allowed.

## Implementation status

SKELETON_CREATED

## TODO

- Bind to `.lawim/architecture-backlog/contracts/workflow-contract.md`.
- Bind to `.lawim/architecture-backlog/policies/workflow-policy.md`.
