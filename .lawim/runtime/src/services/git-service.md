# Service: Git Service

## Objective

Control repository actions and traceability.

## Responsibilities

- Report Git status safely.
- Gate commit, tag, and push operations.
- Enforce repository policy gates.
- Keep action traces readable.

## Inputs

- Diff summary.
- Branch state.
- Commit message.
- Tag intent.
- Remote availability.

## Outputs

- Git status snapshot.
- Commit result.
- Tag result.
- Push result.
- Repository trace.

## Critical errors

- Empty commit message.
- Clean tree.
- Empty tag name.
- Existing tag.
- Missing remote.
- Forbidden mutation.

## Implementation status

IMPLEMENTED

## TODO

- Keep the command aligned with the Git contract and Git policy.
- Extend only when upstream governance changes.
