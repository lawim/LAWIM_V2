# LAWIM — Programme D File Justification Matrix

**Date:** 2026-07-23
**Reviewer:** Independent Architecture Review (Programme D.5)

---

## Summary

| Category | Count |
|----------|-------|
| Total files added | 127 |
| JUSTIFIED | 121 |
| DUPLICATED | 1 (EventCollector in base/events.py) |
| EMPTY_OR_TRIVIAL | 2 (base/policy.py DomainRuntimePolicy unused by runtime, base/metrics.py MetricsCollector unused by production) |
| MISPLACED | 0 |
| INCOMPLETE | 3 (v2 adapters never wired to production pipeline) |
| INCOHERENT | 2 (base/policy.py feature_flag field never read, PaymentRuntime += 0 no-op — FIXED) |
| UNUSED | 3 (adapters never called from production code, base/metrics.py MetricsCollector) |

## Per-File Status

### Base Contracts (11 files)

| File | Lines | Responsibility | Status | Justification |
|------|-------|---------------|--------|---------------|
| `base/__init__.py` | 1 | Package init | JUSTIFIED | Required for Python package |
| `base/runtime.py` | 67 | DomainRuntime ABC | JUSTIFIED | Core abstraction for all 8 runtimes |
| `base/request.py` | 15 | DomainRuntimeRequest | JUSTIFIED | Input contract, consumed by all runtimes |
| `base/result.py` | 51 | DomainRuntimeResult + Status | JUSTIFIED | Output contract, consumed by all runtimes |
| `base/context.py` | 17 | DomainRuntimeContext | JUSTIFIED | Execution context for domain ops |
| `base/handler.py` | 29 | DomainRuntimeHandler | JUSTIFIED | Bridges ActionHandler to DomainRuntime |
| `base/registry.py` | 31 | DomainRuntimeRegistry | JUSTIFIED | Runtime discovery (parallel to C.5 registry) |
| `base/errors.py` | 23 | Domain errors | JUSTIFIED | Typed error hierarchy |
| `base/events.py` | 40 | DomainEvent + EventCollector | DUPLICATED | EventCollector duplicates execution/events.py |
| `base/metrics.py` | 57 | MetricsCollector + DomainMetrics | UNUSED | Not imported by any production code; only tests |
| `base/policy.py` | 16 | DomainRuntimePolicy | TRIVIAL | Feature_flag field never read at runtime |

### Domain Runtimes (64 files — 8 domains × 8 files)

#### Matching (8 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `matching/__init__.py` | 13 | JUSTIFIED | Package exports |
| `matching/runtime.py` | 238 | JUSTIFIED | Real matching logic with scoring, validation, verification |
| `matching/models.py` | 109 | JUSTIFIED | MatchingRequestData, MatchingResult, MatchingStatus |
| `matching/policy.py` | 10 | JUSTIFIED | MATCHING_POLICY constants |
| `matching/repository.py` | 75 | JUSTIFIED | In-memory storage with property/survey tables |
| `matching/events.py` | 37 | JUSTIFIED | MatchingEventType enum |
| `matching/metrics.py` | 30 | JUSTIFIED | MatchingMetrics counters |
| `matching/handlers.py` | 70 | JUSTIFIED | ActionHandler that delegates to MatchingRuntime |

#### Visit (8 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `visit/__init__.py` | 13 | JUSTIFIED | Package exports |
| `visit/runtime.py` | 185 | JUSTIFIED | Real visit lifecycle with dedup, state transitions |
| `visit/models.py` | 145 | JUSTIFIED | VisitRecord with 7 statuses |
| `visit/policy.py` | 10 | JUSTIFIED | VISIT_POLICY constants |
| `visit/repository.py` | 60 | JUSTIFIED | In-memory visit storage |
| `visit/events.py` | 43 | JUSTIFIED | VisitEventType enum |
| `visit/metrics.py` | 33 | JUSTIFIED | VisitMetrics counters |
| `visit/handlers.py` | 70 | JUSTIFIED | ActionHandler for visit operations |

#### CRM (8 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `crm/__init__.py` | 13 | JUSTIFIED | Package exports |
| `crm/runtime.py` | 227 | JUSTIFIED | Lead/opportunity/handover lifecycle with repository |
| `crm/models.py` | 113 | JUSTIFIED | LeadData, OpportunityData, HandoverData |
| `crm/policy.py` | 10 | JUSTIFIED | CRM_POLICY constants |
| `crm/repository.py` | 62 | JUSTIFIED | CRMRepository with lead/opportunity/handover storage |
| `crm/events.py` | 43 | JUSTIFIED | CRMEventType enum |
| `crm/metrics.py` | 33 | JUSTIFIED | CRMMetrics counters |
| `crm/handlers.py` | 71 | JUSTIFIED | ActionHandler for CRM operations |

#### Notification (8 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `notification/__init__.py` | 13 | JUSTIFIED | Package exports |
| `notification/runtime.py` | 129 | JUSTIFIED | Notification lifecycle with dedup by project+template |
| `notification/models.py` | 97 | JUSTIFIED | NotificationData with 6 statuses |
| `notification/policy.py` | 10 | JUSTIFIED | NOTIFICATION_POLICY constants |
| `notification/repository.py` | 89 | JUSTIFIED | NotificationRepository with InMemory impl |
| `notification/events.py` | 42 | JUSTIFIED | NotificationEventType enum |
| `notification/metrics.py` | 30 | JUSTIFIED | NotificationMetrics counters |
| `notification/handlers.py` | 69 | JUSTIFIED | ActionHandler for notification operations |

#### Document (8 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `document/__init__.py` | 13 | JUSTIFIED | Package exports |
| `document/runtime.py` | 201 | JUSTIFIED | Document lifecycle with 7 statuses, repository |
| `document/models.py` | 93 | JUSTIFIED | DocumentData with DocumentStatus enum |
| `document/policy.py` | 10 | JUSTIFIED | DOCUMENT_POLICY constants |
| `document/repository.py` | 51 | JUSTIFIED | DocumentRepository with InMemory impl |
| `document/events.py` | 42 | JUSTIFIED | DocumentEventType enum |
| `document/metrics.py` | 30 | JUSTIFIED | DocumentMetrics counters |
| `document/handlers.py` | 70 | JUSTIFIED | ActionHandler for document operations |

#### Verification (8 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `verification/__init__.py` | 13 | JUSTIFIED | Package exports |
| `verification/runtime.py` | 213 | JUSTIFIED | Verification lifecycle, check aggregation, INCONCLUSIVE |
| `verification/models.py` | 99 | JUSTIFIED | VerificationData, VerificationCheck, 8 statuses |
| `verification/policy.py` | 10 | JUSTIFIED | VERIFICATION_POLICY constants |
| `verification/repository.py` | 58 | JUSTIFIED | VerificationRepository with InMemory impl |
| `verification/events.py` | 46 | JUSTIFIED | VerificationEventType enum |
| `verification/metrics.py` | 33 | JUSTIFIED | VerificationMetrics counters |
| `verification/handlers.py` | 70 | JUSTIFIED | ActionHandler for verification operations |

#### Transaction (8 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `transaction/__init__.py` | 13 | JUSTIFIED | Package exports |
| `transaction/runtime.py` | 234 | JUSTIFIED | Transaction lifecycle, negotiation, preconditions |
| `transaction/models.py` | 110 | JUSTIFIED | TransactionData, NegotiationEntry, 8 statuses |
| `transaction/policy.py` | 11 | JUSTIFIED | TRANSACTION_POLICY constants |
| `transaction/repository.py` | 53 | JUSTIFIED | TransactionRepository with InMemory impl |
| `transaction/events.py` | 39 | JUSTIFIED | TransactionEventType enum |
| `transaction/metrics.py` | 33 | JUSTIFIED | TransactionMetrics counters |
| `transaction/handlers.py` | 72 | JUSTIFIED | ActionHandler for transaction operations |

#### Payment (8 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `payment/__init__.py` | 13 | JUSTIFIED | Package exports |
| `payment/runtime.py` | 236 | JUSTIFIED | Payment lifecycle, idempotency, reconciliation |
| `payment/models.py` | 112 | JUSTIFIED | PaymentData, PaymentIntent, 10 statuses |
| `payment/policy.py` | 11 | JUSTIFIED | PAYMENT_POLICY constants |
| `payment/repository.py` | 60 | JUSTIFIED | PaymentRepository with InMemory impl |
| `payment/events.py` | 44 | JUSTIFIED | PaymentEventType enum |
| `payment/metrics.py` | 36 | JUSTIFIED | PaymentMetrics counters |
| `payment/handlers.py` | 72 | JUSTIFIED | ActionHandler for payment operations |

### Adapters (9 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `adapters/__init__.py` | 21 | JUSTIFIED | Package exports for all adapters |
| `v2_matching.py` | 60 | JUSTIFIED | V2→V3 matching payload converter |
| `v2_visit.py` | 59 | JUSTIFIED | V2→V3 visit payload converter |
| `v2_crm.py` | 54 | JUSTIFIED | V2→V3 CRM payload converter |
| `v2_notification.py` | 60 | JUSTIFIED | V2→V3 notification payload converter |
| `v2_document.py` | 57 | JUSTIFIED | V2→V3 document payload converter |
| `v2_verification.py` | 55 | JUSTIFIED | V2→V3 verification payload converter |
| `v2_transaction.py` | 55 | JUSTIFIED | V2→V3 transaction payload converter |
| `v2_payment.py` | 56 | JUSTIFIED | V2→V3 payment payload converter |

### Infrastructure (2 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `config.py` | 34 | JUSTIFIED | DomainRuntimeConfig with feature flags, all disabled by default |
| `registration.py` | 171 | JUSTIFIED | Dynamic registration with shadow/real mode selection |

### Tests (12 files)

| File | Lines | Status | Justification |
|------|-------|--------|---------------|
| `tests/__init__.py` | 0 | JUSTIFIED | Package init |
| `tests/test_base.py` | 177 | JUSTIFIED | 15 contract tests for base abstractions |
| `tests/test_matching.py` | 113 | JUSTIFIED | 8 behavior + contract tests |
| `tests/test_visit.py` | 76 | JUSTIFIED | 6 behavior + contract tests |
| `tests/test_crm.py` | 83 | JUSTIFIED | 7 behavior + contract tests |
| `tests/test_notification.py` | 91 | JUSTIFIED | 7 behavior + contract tests |
| `tests/test_document.py` | 64 | JUSTIFIED | 5 behavior + contract tests |
| `tests/test_verification.py` | 65 | JUSTIFIED | 5 behavior + contract tests |
| `tests/test_transaction.py` | 82 | JUSTIFIED | 7 behavior + contract tests |
| `tests/test_payment.py` | 114 | JUSTIFIED | 9 behavior + contract tests |
| `tests/test_adapters.py` | 206 | JUSTIFIED | 18 adapter transform tests + divergence logging |
| `tests/test_registration.py` | 71 | JUSTIFIED | 4 registration + shadow mode tests |
| `tests/test_integration_scenarios.py` | 245 | JUSTIFIED | 8 cross-domain integration scenarios |

### Documentation and Scripts (29 files)

All JUSTIFIED — ADRs, reports, architecture docs, context validator.

## Recommendations

1. **CONSIDER removing** `EventCollector` from `base/events.py` and reusing the C.5 equivalent, OR keep as-is for domain-level isolation (recommend: keep, domains should be independent of C.5 internals)
2. **CONSIDER removing** `base/metrics.py` `MetricsCollector` class if not consumed by any runtime (tests only)
3. **NO ACTION**: `base/policy.py` is a valid extension point even if `feature_flag` field is unused
4. **WIRE** V2 Adapters into the production pipeline during Program E
