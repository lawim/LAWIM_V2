# ADR-006: Event-Driven Runtime

**Status:** Accepted
**Date:** 2026-07-22

## Context

Actions produce side effects that other components need to observe. Currently, components poll for state changes or rely on direct calls, creating tight coupling. When a property status changes, the matching engine, notification service, and CRM all need to react. Without events, each integration requires explicit code in the producing component.

## Decision

The runtime produces events after every meaningful state change. ProjectBrain subscribes to relevant events to re-evaluate its decisions. Other components (notifications, CRM, matching) subscribe to events they need. Events are the primary mechanism for inter-component communication after a state change.

## Justification

Events decouple producers from consumers. Adding a new consumer requires no changes to the producer — only a new subscription. The audit trail is enriched by the event stream, providing a complete record of state changes over time. ProjectBrain re-evaluation is naturally triggered by the events it cares about.

## Positive Consequences

- Producers and consumers are fully decoupled
- Adding new event consumers requires zero producer changes
- Complete audit trail of all state changes via event stream
- ProjectBrain re-evaluation is event-driven, not poll-based
- Event replay enables state reconstruction for debugging or migration

## Negative Consequences

- Event schema must be stable or versioned
- Event delivery guarantees require infrastructure (retry, DLQ)
- Debugging async flows is harder than synchronous request-response
- Event volume must be monitored and controlled

## Rejected Alternatives

- **Direct calls from producer to consumer**: Current state; tight coupling
- **Polling**: Wasteful, high latency, scales poorly
- **Shared database as integration point**: Implicit coupling, no audit trail

## Affected Components

- LROS kernel (event bus)
- ProjectBrain (subscriber)
- All domain runtimes (producers)
- NotificationService (subscriber)
- CRMService (subscriber)
- AuditService (subscriber)

## Compliance Criteria

- Every state-changing operation produces at least one event
- No component calls another component directly after a state change
- Event schema includes type, timestamp, correlation_id, and actor
- ProjectBrain re-evaluation is triggered exclusively by events
- Event replay can reconstruct any project's state history

## References

- ADR-002: LROS Runtime Kernel
- ADR-005: Decision-Execution Separation
- ADR-009: Domain Runtime Boundaries
