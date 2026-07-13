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

## Events

- conversation.started
- conversation.intent_identified
- conversation.qualification_completed
- conversation.search_started
- conversation.results_presented
- conversation.relationship_requested
- conversation.follow_up_scheduled
- conversation.closed
- conversation.reopened

