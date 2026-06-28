# Policies

This runtime reuses the official policy backlog instead of creating new policy text.

| Runtime concern | Imported policy source | Runtime binding |
| --- | --- | --- |
| Workflow governance | `.lawim/architecture-backlog/policies/workflow-policy.md` | Workflow Service, Planning Service, Execution Service |
| Review governance | `.lawim/architecture-backlog/policies/review-policy.md` | Review Service, Policy Service |
| Git governance | `.lawim/architecture-backlog/policies/git-policy.md` | Git Service, Policy Service |
| Release governance | `.lawim/architecture-backlog/policies/release-policy.md` | Planning Service, Report Service |
| Security governance | `.lawim/architecture-backlog/policies/security-policy.md` | Policy Service, Review Service |

## Source of truth

- `.lawim/architecture-backlog/policies/`
- `.lawim/runtime/src/policies/policy-registry.md`

## Notes

- The runtime only references these policies.
- No policy text is duplicated here.

## Status

FOUNDATION_CREATED
