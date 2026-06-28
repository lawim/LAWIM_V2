# Command: run

## Objective

Execute one prepared work item through the runtime.

## Inputs

- Ticket context.
- Planning data.
- Workflow gate.
- Policy gate.
- Execution context.

## Outputs

- Execution trace.
- Report seed.
- Status update input for PCC.

## Critical errors

- Missing ticket.
- Invalid state.
- Unresolved dependency.
- Policy violation.

## Implementation status

SKELETON_CREATED

## TODO

- Bind to the Execution Service.
- Define the single-ticket execution envelope.
