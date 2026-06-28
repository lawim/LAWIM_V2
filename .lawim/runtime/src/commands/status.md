# Command: status

## Objective

Expose a read-only snapshot of runtime readiness and trace links.

## Inputs

- Runtime root.
- PCC summary.
- Latest report pointers.

## Outputs

- Readiness snapshot.
- Trace links to the active runtime docs.

## Critical errors

- Runtime root missing.
- Report trail unreadable.
- PCC reference missing.

## Implementation status

SKELETON_CREATED

## TODO

- Bind to the Report Service and PCC Service read models.
- Define the final output shape.
