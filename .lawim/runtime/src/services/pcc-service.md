# Service: PCC Service

## Objective

Maintain the program control center view.

## Responsibilities

- Hold coordination state.
- Record decisions, risks, dependencies, and validations.
- Keep the trace append-only.

## Inputs

- Status updates.
- Decisions.
- Risks.
- Dependencies.
- Validations.

## Outputs

- PCC snapshot.
- Update trace.

## Critical errors

- Missing coordination data.
- Stale state.
- Conflicting decision.

## Implementation status

SKELETON_CREATED

## TODO

- Bind to the PCC contract.
- Define a canonical update envelope.
