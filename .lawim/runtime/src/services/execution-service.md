# Service: Execution Service

## Objective

Coordinate a single execution flow.

## Responsibilities

- Prepare execution context.
- Apply workflow and policy decisions.
- Emit traceable execution output.

## Inputs

- Ticket context.
- Workflow decision.
- Policy gate.
- Report sink.

## Outputs

- Execution trace.
- Status update input.

## Critical errors

- Missing assignment.
- Invalid execution state.
- Blocked gate.
- No report sink.

## Implementation status

SKELETON_CREATED

## TODO

- Connect to the future command dispatcher.
- Define the execution envelope for `run`.
