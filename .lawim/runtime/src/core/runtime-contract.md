# Runtime Contract

## Objective

Define the internal execution boundary for the LAWIM runtime.

## Boundaries

- Accept a command name and a runtime context.
- Resolve the command against the skeleton registry.
- Delegate orchestration to services.
- Emit a traceable runtime result.

## Inputs

- CLI command name.
- Runtime root.
- Imported contracts and policies.
- Execution context prepared by the caller.

## Outputs

- Normalized runtime decision.
- Traceable report seed.
- Exit status.

## Critical errors

- Unknown command.
- Missing contract binding.
- Missing policy binding.
- Unreadable runtime root.

## Implementation status

SKELETON_CREATED

## TODO

- Define the parser and dispatcher.
- Bind command resolution to real service adapters.
- Add error normalization.
