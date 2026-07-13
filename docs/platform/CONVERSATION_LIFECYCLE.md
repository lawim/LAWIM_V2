# Conversation Lifecycle

LAWIM conversations are stateful and continue across channels.

## Canonical states

- NEW
- WELCOME
- DISCOVERY
- INTENT_IDENTIFIED
- QUALIFICATION
- MINIMUM_DATA_COMPLETE
- SEARCH_READY
- SEARCHING
- RESULTS_AVAILABLE
- SELECTION_PENDING
- CONSENT_PENDING
- RELATIONSHIP_REQUESTED
- VISIT_PENDING
- VISIT_SCHEDULED
- VISIT_COMPLETED
- OFFER_PENDING
- OFFER_SUBMITTED
- NEGOTIATION
- DOCUMENT_REVIEW
- PAYMENT_PENDING
- FOLLOW_UP_PENDING
- RESOLVED
- CLOSED
- REOPENED
- HUMAN_HANDOVER_REQUESTED
- HUMAN_ACTIVE

## Rules

- Keep one conversation thread per user journey.
- Preserve the current state, previous state, transition time, actor, and reason.
- Reopening must resume from persisted context, not from a blank prompt.
- Channel changes must not create a new business thread.
- Once the minimum qualification threshold is reached, search or matching should start instead of extending the questionnaire.
- The conversation should keep a single next action and a single responsible actor at any time.
- Human handover must be explicit and visible to the user.

## Events

- conversation.started
- conversation.intent_identified
- conversation.qualification_completed
- conversation.search_started
- conversation.results_presented
- conversation.selection_made
- conversation.consent_requested
- conversation.relationship_requested
- conversation.visit_scheduled
- conversation.visit_completed
- conversation.offer_submitted
- conversation.negotiation_started
- conversation.document_review_started
- conversation.payment_pending
- conversation.follow_up_scheduled
- conversation.closed
- conversation.reopened
