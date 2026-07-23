# LAWIM End-to-End Interaction Flow

**Date:** 2026-07-23
**Certification:** Program E.5

## Canonical Path

```
Channel (WhatsApp / Telegram / Web/API)
  -> ChannelAdapter.parse_webhook()
  -> InteractionEnvelope
  -> InteractionGateway.validate_envelope()
  -> InteractionDeduplicator.check()
  -> MessageNormalizer.normalize()
  -> IdentityResolver.resolve()
  -> SessionManager.resume_or_create()
  -> ProjectResolver.resolve()
  -> [DeterministicExtractor | Programme F LLM]
  -> CandidateUpdate[]
  -> ProfilePatch
  -> ProjectProfile.set_field()
  -> QualificationEngine.evaluate()
  -> DecisionEngine.decide()
  -> ProjectBrain.evaluate()
  -> ActionExecutionEngine.execute()
  -> DomainRuntime.execute()
  -> ProjectBrain re-evaluate
  -> InteractionResponsePlan
  -> ResponseWriter.write()
  -> DeliveryManager.deliver()
  -> ChannelAdapter.send()
  -> Channel delivery
```

## Verified Via E2E Tests

| Scenario | Components Traversed | Result |
|----------|---------------------|--------|
| E2E-01 Project Creation | Envelope, Gateway, Dedup, Normalizer, Identity, Session, Project, Extractor, Profile, QualEngine, DecisionEngine, Brain, ResponsePlan, Writer, Delivery | PASS |
| E2E-02 Multiturn | Same profile across 6 turns, no field loss, session continuity | PASS |
| E2E-03 Session Resume | Session expiry, new session, same project | PASS |
| E2E-04 Multichannel | WhatsApp + Telegram, same user, same project | PASS |
| E2E-05 Matching Success | MatchingRuntime with 3 properties, ranked by score | PASS |
| E2E-06 Matching Insufficient | Missing 2+ criteria, INSUFFICIENT_DATA detected | PASS |
| E2E-07 Visit Full Flow | Create, Schedule, Confirm, Complete, Cancel | PASS |
| E2E-09 Document & Verification | DocumentRuntime + VerificationRuntime | PASS |
| E2E-10 Transaction Preconditions | TransactionRuntime rejects without preconditions | PASS |
| E2E-11 Payment Idempotency | Same request twice, no double execution | PASS |
| Full Integration Pipeline | 12 components chained end-to-end with metrics | PASS |

## Non-Canonical Paths Detected

None. All bypasses identified in the V2 channel audit are properly isolated. Legacy V2 code paths remain operational but are separate from the V3 canonical pipeline.
