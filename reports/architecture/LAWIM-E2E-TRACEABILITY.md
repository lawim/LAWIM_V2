# LAWIM End-to-End Traceability

**Date:** 2026-07-23
**Certification:** Program E.5

## Correlation Model

Every interaction turn produces a `correlation_id` that links all downstream entities:

```
correlation_id
  -> interaction_id (InteractionEnvelope)
  -> session_id (InteractionSession)
  -> project_id (ProjectProfile)
  -> decision_id (DecisionResult)
  -> execution_id (ActionExecutionResult)
  -> delivery_id (DeliveryResult)
  -> response_plan_id (InteractionResponsePlan)
```

## CorrelationManager

- `create(correlation_id)` - creates a trace record
- `update(correlation_id, **fields)` - links entities to the trace
- `trace(correlation_id)` - retrieves the full trace
- `get(correlation_id)` - returns the complete record

## Traceable Fields Per Entity

| Entity | Identifiers |
|--------|-------------|
| InteractionEnvelope | interaction_id, correlation_id, causation_id |
| InteractionSession | session_id, user_id, active_project_id |
| ProjectResolutionResult | resolution_id, project_id |
| DecisionResult | decision_id, project_id |
| ActionExecutionRequest | execution_request_id, correlation_id, idempotency_key |
| ActionExecutionResult | execution_id, correlation_id, idempotency_key |
| DomainRuntimeResult | request_id, action_code |
| InteractionResponsePlan | response_plan_id, correlation_id |
| DeliveryResult | delivery_id, correlation_id |
| DivergenceRecord | record_id, correlation_id |
| AuditEntry | entry_id, correlation_id |

## Verification

The correlation trace test validates that from a single `correlation_id`, all downstream entities can be retrieved:
- interaction_id: int-001
- session_id: sess-001
- project_id: proj-001
- Full record accessible via `CorrelationManager.trace(correlation_id)`
