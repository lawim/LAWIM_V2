# Command: git-sync

## Objective

Prepare a controlled repository sync.

## Inputs

- Diff summary.
- Branch state.
- Commit message.
- Tag intent.
- Remote availability.
- Policy gates.

## Outputs

- Git status snapshot.
- Commit result.
- Tag result.
- Push result.
- Trace record.

## Critical errors

- Empty commit message.
- Clean tree for commit.
- Empty tag name.
- Existing tag.
- Remote absent when push is required.
- Forbidden policy transition.

## Implementation status

IMPLEMENTED

## TODO

- Keep the command aligned with the Git Service and Policy Service.
- Extend only if the Git governance contract changes.
