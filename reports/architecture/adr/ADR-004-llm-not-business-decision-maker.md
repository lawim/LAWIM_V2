# ADR-004: LLM Is Not the Business Decision Maker

**Status:** Accepted
**Date:** 2026-07-22

## Context

LLMs produce plausible but sometimes incorrect business decisions. Using an LLM to determine qualification status, property availability, visit scheduling, or payment status introduces non-determinism and unreliability into core business logic. Stakeholders cannot audit or trust LLM-driven business decisions.

## Decision

The LLM performs only two functions: extraction (converting unstructured text into structured data) and formulation (converting structured data into natural language responses). The business logic engine determines qualification, conversation state, next action, property availability, and all other business decisions. The LLM never sets a business state field directly.

## Justification

Deterministic business logic produces consistent, auditable, and testable outcomes. The LLM excels at natural language tasks but is unsuitable for reliable business decisions. Separating these concerns also reduces LLM token consumption since business logic requires no LLM call.

## Positive Consequences

- All business decisions are deterministic and auditable
- Test coverage is meaningful (not dependent on LLM output variance)
- LLM token costs are limited to extraction and formulation
- Business logic can be unit-tested without LLM dependency
- Audit trail contains deterministic decision reasons, not LLM justifications

## Negative Consequences

- Extraction errors from the LLM propagate into business logic
- More code to maintain for extraction schemas and validation
- Business logic must handle edge cases the LLM would have glossed over

## Rejected Alternatives

- **LLM decides everything**: Non-deterministic, unauditable, high cost
- **LLM with human validation**: Slow, expensive, still non-deterministic
- **Hybrid with LLM override for edge cases**: Blurred boundary, hard to audit

## Affected Components

- ConversationEngine
- ProjectBrain
- All business logic components
- AIOrchestrator
- Prompt templates

## Compliance Criteria

- No business state field is set directly by an LLM response
- Every business decision has a deterministic code path
- LLM output is always validated against a schema before business use
- Test suite covers business logic without calling any LLM
- Audit log shows deterministic reason for every business state change

## References

- ADR-005: Decision-Execution Separation
- Conversation Contract (docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md)
