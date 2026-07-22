# ADR-009: Domain Runtime Boundaries

**Status:** Accepted
**Date:** 2026-07-22

## Context

Domain logic is spread across handlers, channel adapters, and inline callbacks. Business rules for matching, visits, CRM, notifications, documents, verification, transactions, and payments interleave with channel-specific code and LLM calls. This makes domain logic untestable without spinning up the full stack and impossible to migrate independently.

## Decision

Each business domain (matching, visit, CRM, notification, document, verification, transaction, payment) has a dedicated DomainRuntime. A DomainRuntime has NO LLM calls, NO channel dependencies, and NO decision authority. It executes the work, verifies the outcome, and produces events. Decision authority remains in ProjectBrain; DomainRuntimes receive DecisionResults and execute them.

## Justification

Separation of concerns makes domain logic independently testable. Channel independence means a domain runtime can be used from WhatsApp, Telegram, or API without modification. Migration readiness follows from domain isolation — each domain can be migrated from V2 to V3 independently. Removing LLM calls from domain logic ensures deterministic execution.

## Positive Consequences

- Each domain is independently testable without LLM or channel dependencies
- Domain runtimes are portable across channels
- Per-domain migration from V2 to V3 is feasible
- Domain logic is deterministic: same input, same output
- New domains follow a clear structural pattern

## Negative Consequences

- More files and boilerplate per domain
- Coordination between domains requires events (not direct calls)
- Domain boundaries must be designed upfront to avoid cross-domain leaks
- Shared domain concepts (e.g., property, user) require shared models

## Rejected Alternatives

- **Monolithic service containing all domain logic**: Untestable, no migration path
- **Domain logic in channel adapters**: Current state; tightly coupled to channels
- **Domain logic in LLM prompts**: Non-deterministic, unauditable

## Affected Components

- DomainRuntimes (matching, visit, CRM, notification, document, verification, transaction, payment)
- ProjectBrain (produces DecisionResults for domain runtimes)
- LROS kernel (event bus between domain runtimes)
- Channel adapters (call domain runtimes via LROS)

## Compliance Criteria

- No DomainRuntime contains an LLM call
- No DomainRuntime imports a channel adapter
- No DomainRuntime sets business state directly (receives DecisionResults)
- Each DomainRuntime has a unit test suite with no LLM or channel mocks
- DomainRuntimes communicate only via LROS events
- A new channel can use all existing domain runtimes without modification

## References

- ADR-002: LROS Runtime Kernel
- ADR-004: LLM Is Not the Business Decision Maker
- ADR-005: Decision-Execution Separation
- ADR-006: Event-Driven Runtime
