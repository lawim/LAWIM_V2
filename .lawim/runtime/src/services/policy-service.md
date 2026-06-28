# Service: Policy Service

## Objective

Resolve and enforce imported policy sources.

## Responsibilities

- Read the policy registry.
- Gate command or service actions.
- Return explicit allow or deny decisions.

## Inputs

- Policy registry.
- Runtime context.
- Command intent.

## Outputs

- Policy decision.
- Gate reason.

## Critical errors

- Missing policy source.
- Unreadable policy file.
- Conflicting policy directives.

## Implementation status

SKELETON_CREATED

## TODO

- Read from `.lawim/architecture-backlog/policies/`.
- Add a minimal machine-readable policy map if required.
