# Service: Report Service

## Objective

Produce and archive runtime reports.

## Responsibilities

- Assemble report content.
- Store runtime reports in a stable location.
- Keep links to trace inputs.

## Inputs

- Execution trace.
- Review trace.
- Closure trace.
- Runtime context.

## Outputs

- Report file.
- Reference bundle.

## Critical errors

- Missing inputs.
- Unreadable trace.
- Archive path failure.

## Implementation status

SKELETON_CREATED

## TODO

- Write to `reports/runtime/` with stable naming.
- Add a report index for future queries.
