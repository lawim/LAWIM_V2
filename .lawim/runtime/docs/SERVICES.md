# Services

This document summarizes the runtime services that will eventually back the commands.
The per-service skeletons live in `.lawim/runtime/src/services/`.

| Service | Role | Inputs | Outputs | Critical errors | Status | TODO |
| --- | --- | --- | --- | --- | --- | --- |
| Workflow Service | Own workflow state and allowed transitions. | Ticket state, workflow contract, transition context. | Transition decision and normalized workflow summary. | Unknown state, invalid transition, contract drift. | SKELETON_CREATED | Bind imported workflow contract and policy. |
| Policy Service | Resolve and enforce imported policy sources. | Policy registry, runtime context, command intent. | Policy decision and gate result. | Missing policy, unreadable policy source, conflicting policy. | SKELETON_CREATED | Read from `.lawim/architecture-backlog/policies/`. |
| Execution Service | Coordinate a single execution flow. | Ticket input, workflow decision, policy gate, runtime context. | Execution trace and report seed. | Missing assignment, invalid execution state, blocked gate. | SKELETON_CREATED | Connect to future command dispatcher. |
| Review Service | Manage review checks and findings. | Deliverable, checklist, evidence, reviewer context. | Review outcome, findings, and trace. | Missing evidence, incomplete review, policy violation. | SKELETON_CREATED | Bind review contract and review policy. |
| Git Service | Control repository operations and traceability. | Diff summary, branch state, target action, policy gate. | Git action plan and repository trace. | Dirty tree, remote mismatch, forbidden mutation. | SKELETON_CREATED | Bind git contract and git policy. |
| PCC Service | Maintain the program control center view. | Status updates, decisions, risks, dependencies, validations. | PCC snapshot and traceable updates. | Missing coordination data, stale state, conflicting decisions. | SKELETON_CREATED | Bind to the PCC contract and reporting path. |
| Planning Service | Prepare sequencing, sprint scope, and dependencies. | Ticket pool, sprint context, ordering rules, constraints. | Plan, schedule, or closure input bundle. | Missing dependency data, invalid ordering, unsatisfied gate. | SKELETON_CREATED | Add sprint and batch planning helpers. |
| Report Service | Produce and archive runtime reports. | Execution trace, review trace, closure trace, runtime context. | Report file and reference bundle. | Missing inputs, unreadable trace, archive path failure. | SKELETON_CREATED | Write to `reports/runtime/` with stable naming. |

## Notes

- The services are contracts, not implementations.
- The runtime uses them as separable boundaries to avoid mixing orchestration with governance.
