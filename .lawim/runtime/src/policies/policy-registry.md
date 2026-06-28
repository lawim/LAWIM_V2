# Policy Registry

## Objective

Record the official policy bindings used by the runtime without duplicating policy text.

## Imported sources

| Policy | Source |
| --- | --- |
| Workflow policy | `.lawim/architecture-backlog/policies/workflow-policy.md` |
| Review policy | `.lawim/architecture-backlog/policies/review-policy.md` |
| Security policy | `.lawim/architecture-backlog/policies/security-policy.md` |
| Release policy | `.lawim/architecture-backlog/policies/release-policy.md` |
| Git policy | `.lawim/architecture-backlog/policies/git-policy.md` |

## Runtime use

- The Policy Service consults this registry.
- Command and service docs refer back to the imported sources.
- Any future extension must reuse the backlog file before creating a new policy artifact.

## Implementation status

SKELETON_CREATED

## TODO

- Add a machine-readable mapping if the runtime implementation needs it.
- Keep this registry aligned with the official backlog policies.
