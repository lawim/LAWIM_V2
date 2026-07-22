# Program D -- Domain Runtime Engines

## Purpose

Implement domain-specific execution engines that sit between the
ActionExecutionEngine (Program C.5) and external systems. These engines
translate generic action execution into domain-specific business logic.

## Design Constraints

- No LLM dependency
- No channel awareness
- No decision authority
- Shadow mode enabled by default (no external effects)

## Domain Engines

| Engine | Responsibility |
|--------|---------------|
| Matching | Property-to-requirement matching logic |
| Visit | Visit planning, scheduling, lifecycle |
| CRM | Contact management, lead tracking |
| Notification | Outbound messaging orchestration |
| Document | Document generation and management |
| Verification | Identity and document verification |
| Transaction | Transaction management and lifecycle |
| Payment | Payment processing and reconciliation |

## Per-Engine Structure

Each engine implements the following modules:

| Module | Purpose |
|--------|---------|
| `runtime.py` | Execution lifecycle, shadow mode hooks |
| `models.py` | Domain data models and value objects |
| `policy.py` | Business rules and constraints |
| `repository.py` | Persistence layer |
| `events.py` | Domain events |
| `metrics.py` | Observability metrics |
| `handlers.py` | Action handler registration |

## Contracts

- Base contracts are defined in `lawim_runtime/domains/base/`
- Handlers register in ActionHandlerRegistry for their action codes
- Default feature flags: all disabled
