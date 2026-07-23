# LAWIM — Programme D Dependency Map

**Date:** 2026-07-23

---

## Dependency Matrix

| Source | Target | Dependency Type | Authorized | Justification |
|--------|--------|----------------|------------|---------------|
| All 8 domain `runtime.py` | `base/runtime.py` | Inheritance | YES | DomainRuntime ABC |
| All 8 domain `runtime.py` | `base/request.py` | Import | YES | DomainRuntimeRequest |
| All 8 domain `runtime.py` | `base/result.py` | Import | YES | DomainRuntimeResult/Status |
| All 8 domain `runtime.py` | `base/context.py` | Import | YES | DomainRuntimeContext |
| All 8 domain `runtime.py` | `base/errors.py` | Import | YES | DomainValidationError |
| All 8 domain `runtime.py` | own `models.py` | Import | YES | Domain models |
| All 8 domain `runtime.py` | own `events.py` | Import | YES | Domain events |
| All 8 domain `runtime.py` | own `metrics.py` | Import | YES | Domain metrics |
| All 8 domain `runtime.py` | own `repository.py` | Import | YES | Domain persistence |
| All 8 domain `handlers.py` | `base/handler.py` | Inheritance | YES | DomainRuntimeHandler ABC |
| All 8 domain `handlers.py` | `base/request.py` | Import | YES | DomainRuntimeRequest |
| All 8 domain `handlers.py` | `base/result.py` | Import | YES | DomainRuntimeResult/Status |
| All 8 domain `handlers.py` | `execution/context.py` | Import | YES | ActionExecutionContext |
| All 8 domain `handlers.py` | own `runtime.py` | Import | YES | Delegates to runtime |
| All 8 domain `policy.py` | `base/policy.py` | Import | YES | DomainRuntimePolicy |
| All 8 domain `events.py` | `base/events.py` | Import | YES | DomainEvent base |
| All 8 domain `models.py` | `base/request.py` | Import | YES | DomainRuntimeRequest for converters |
| All 8 domain `models.py` | `base/result.py` | Import | YES | DomainRuntimeResult for converters |
| All 8 domain `repository.py` | own `models.py` | Import | YES | Domain models |
| `registration.py` | All 8 domain `handlers` | Import | YES | Hub module |
| `registration.py` | `base/handler.py` | Import | YES | DomainRuntimeHandler |
| `registration.py` | `base/result.py` | Import | YES | DomainRuntimeStatus |
| `registration.py` | `execution/registry.py` | Import | YES | ActionHandlerRegistry |
| `registration.py` | `execution/context.py` | Import | YES | ActionExecutionContext |
| `registration.py` | `config.py` | Import | YES | DomainRuntimeConfig |

## Circular Dependencies

**NONE FOUND.** The dependency graph is a strict DAG:

```
execution/ ←─── registration ───→ base/ ───→ domain_runtime ───→ domain_models
                                                        │
                                                        └──→ domain_events
                                                        └──→ domain_metrics
                                                        └──→ domain_repository
```

## Cross-Domain Dependencies

**NONE.** No domain imports from another domain. Each domain is fully isolated.

## Forbidden Dependency Verification

| Check | Result |
|-------|--------|
| No domain imports LLM provider | PASS |
| No domain imports channel adapter | PASS |
| No domain imports another domain | PASS |
| No domain calls DecisionEngine/ProjectBrain directly | PASS |
| No domain calls ActionExecutionEngine directly | PASS |
| No domain modifies V2 state | PASS |
| `registration.py` is the sole aggregation point | PASS |
| `execution/` does NOT import from any domain | PASS |
| `base/` does NOT import from any domain | PASS |
