# Program K — Learning Machine Foundation (Part 1)

**Document ID:** LAWIM-PROGRAM-K-FOUNDATION-V1
**Status:** CANONICAL
**Date:** 2026-07-15

---

## 1. Scope

Program K Part 1 delivers the Learning Machine Foundation:

- Learning Event Registry (canonical, immutable events from H and J)
- Outcome Registry (business results with status tracking)
- Feedback Engine (deterministic feedback collection and normalization)
- Services, feature flags, API contracts

No ML training, no prediction models, no automatic recommendations — this is the **data collection and normalization layer** only.

---

## 2. Learning Event Registry

### Event Types (24)

#### From Program H
- H_QUALIFICATION_STARTED, H_QUALIFICATION_COMPLETED, H_QUALIFICATION_ABANDONED, H_QUALIFICATION_ESCALATED
- H_READINESS_EVALUATED, H_NEXT_QUESTION_RESOLVED

#### From Program J
- J_CONVERSATION_STARTED, J_CONVERSATION_MESSAGE, J_CONVERSATION_CLOSED, J_CHANNEL_SESSION_ACTIVE
- J_PUBLICATION_CREATED, J_REDIRECT_RECORDED, J_TOUCHPOINT_RECORDED, J_ATTRIBUTION_CALCULATED
- J_EXCHANGE_INBOUND, J_EXCHANGE_OUTBOUND
- J_CONVERSION_RECORDED, J_MATCHING_CREATED, J_VISIT_REQUESTED, J_PAYMENT_INITIATED, J_PAYMENT_CONFIRMED

#### Internal
- OUTCOME_RECORDED, FEEDBACK_RECEIVED, FEEDBACK_AGGREGATED

### Event Structure

Each event: event_id, event_type, source, actor_id, conversation_id, property_id, transaction_id, channel, correlation_id, payload, event_version, confidence, timestamp, metadata.

Events are **immutable** — no deletion, no destructive modification. Anonymization removes sensitive fields (phone, email, raw_text, full_name).

---

## 3. Outcome Registry

### Outcome Statuses
- SUCCESS, FAILURE, ABANDONED, PENDING, UNKNOWN

### Outcome Types
- qualification, matching, visit, transaction, payment, conversation, conversion

Each outcome links to: event, actor, conversation, channel, property, transaction, payment, tracking_code, campaign, publication.

Success rate calculation: `successes / total * 100`.

---

## 4. Feedback Engine

### Origins (9)
USER, AGENT, ADMIN, BUSINESS_EVENT, PAYMENT, TRANSACTION, MATCHING, VISIT, SATISFACTION_SURVEY

### Targets (9)
AI_RESPONSE, MATCHING_RESULT, AGENT_PERFORMANCE, PROPERTY, SERVICE, CONVERSATION, RECOMMENDATION, PUBLICATION, CAMPAIGN

### Features
- Score normalization (0.0-1.0)
- Average score per target
- Confidence tracking
- Source event linking
- Deterministic, no ML involved

---

## 5. Feature Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `learning_events_enabled` | false | Learning event collection and API |
| `outcome_registry_enabled` | false | Outcome registration and query |
| `feedback_engine_enabled` | false | Feedback submission and retrieval |

---

## 6. Public Contracts

### Learning Events
- `GET /learning/events/types` — list event types
- `GET /learning/events/stats` — event statistics
- `GET /learning/events/{id}` — get event

### Outcomes
- `GET /learning/outcomes` — list outcomes by status
- `GET /learning/outcomes/stats` — outcome statistics
- `GET /learning/outcomes/success-rate/{type}` — success rate

### Feedback
- `GET /learning/feedback` — recent feedback items

All endpoints return `{"status": "disabled"}` when feature flag is off.

---

## 7. Traceability Matrix

| Event Type | Source Program | Domain | Component |
|-----------|---------------|--------|-----------|
| H_QUALIFICATION_STARTED | H | Knowledge Runtime | ProgressiveWizard |
| H_QUALIFICATION_COMPLETED | H | Knowledge Runtime | ProgressiveWizard |
| J_CONVERSATION_STARTED | J | Unified Conversation | ConversationService |
| J_CONVERSION_RECORDED | J | Conversion Chain | ConversionLinkingService |
| J_PAYMENT_CONFIRMED | J | Payment | ConversionEvent |
| J_REDIRECT_RECORDED | J | Tracking | RedirectLog |
| J_ATTRIBUTION_CALCULATED | J | Attribution | AttributionEngine |
| OUTCOME_RECORDED | K | Learning | OutcomeRegistryService |
| FEEDBACK_RECEIVED | K | Learning | FeedbackService |

---

## 8. Known Limitations

- Events are stored in-memory (no dedicated DB table yet)
- No ML models, no training, no predictions — pure data collection
- Feedback engine does not wire into existing CRM satisfaction surveys (future)
- Learning events are not yet published to an event bus
- No automated data quality pipeline for learning events
