# Service: Git Service

## Objective

Control repository actions and traceability.

## Responsibilities

- Build a controlled git action plan.
- Enforce repository policy gates.
- Keep action traces readable.

## Inputs

- Diff summary.
- Branch state.
- Tag intent.
- Remote availability.

## Outputs

- Git action plan.
- Repository trace.

## Critical errors

- Dirty tree.
- Remote mismatch.
- Forbidden mutation.

## Implementation status

SKELETON_CREATED

## TODO

- Bind git contract and git policy.
- Define local-only vs remote-aware sync behavior.
