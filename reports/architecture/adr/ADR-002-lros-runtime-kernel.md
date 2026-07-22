# ADR-002: LROS Runtime Kernel

**Status:** Accepted
**Date:** 2026-07-22

## Context

No central orchestrator exists in the current architecture. Components import each other directly, creating tight coupling. Testing requires instantiating the full dependency graph. Swapping implementations (e.g., switching AI providers or channel backends) requires code changes across multiple files.

## Decision

LROS (LAWIM Runtime Operating System) is a lightweight orchestration kernel. All components communicate through LROS contracts (interfaces, events, and service registrations). No component imports another component directly.

## Justification

Loose coupling enables independent testing of each component. Channel independence means adding a new channel requires only a new adapter conforming to the LROS contract, not modifications to existing code. Provider swapping (AI, storage, etc.) becomes a configuration change.

## Positive Consequences

- Components are independently testable with mock contracts
- New channels require zero changes to existing adapters
- AI provider swap is a configuration change, not a code change
- Runtime lifecycle (startup, shutdown, health) is centralized

## Negative Consequences

- Initial development overhead to define and enforce contracts
- Runtime indirection adds minimal latency per call
- Learning curve for developers unfamiliar with kernel architectures

## Rejected Alternatives

- **Direct imports**: Current state; proven to cause tight coupling and brittle tests
- **Message bus (RabbitMQ, Kafka)**: Overkill for in-process communication; adds operational complexity
- **REST between components**: Network overhead for in-process calls; serialization cost

## Affected Components

- All runtime components
- Channel adapters
- AI provider wrappers
- Storage layer
- Testing infrastructure

## Compliance Criteria

- No component imports another component's implementation directly
- All inter-component communication uses LROS contracts
- A channel adapter can be added without modifying any existing adapter
- AI provider swap requires only configuration change
- Each component has a unit test that mocks its LROS dependencies

## References

- ADR-006: Event-Driven Runtime
- ADR-009: Domain Runtime Boundaries
