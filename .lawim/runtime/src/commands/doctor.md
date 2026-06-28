# Command: doctor

## Objective

Check runtime health, contract coverage, and policy availability.

## Inputs

- Filesystem state.
- Imported contracts.
- Imported policies.
- Git metadata.

## Outputs

- Diagnostic result with PASS, WARN, or FAIL.
- Structural findings.

## Critical errors

- Contract drift.
- Unreadable policy source.
- Broken path layout.
- Missing executable entrypoint.

## Implementation status

SKELETON_CREATED

## TODO

- Add structural and policy validators.
- Define a stable diagnostic format.
