# PRIVATE_BETA Configuration

PRIVATE_BETA is the controlled deployment profile used before broad production rollout.

## Expected posture

- Activate only validated capabilities.
- Keep experimental or unvalidated features disabled.
- Keep sensitive kill switches and permissions auditable.
- Keep the commercial journey working end to end: qualification, search, matching, consent, visits, offers, negotiation, documents, and follow-up.

## Operational focus

- Auth
- Profiles
- CRM
- GED
- Brain
- Matching
- Relation engine
- Notifications
- WhatsApp
- Telegram
- Email
- Conversation Core
- Commercial maturity and scoring
- Transaction lifecycle
- Response validation
- Feature management
- Human handover

## Guardrails

- No feature should become visible only from the frontend.
- No permission should be granted by a flag alone.
- No unvalidated payment or relationship flow should be enabled by default.
- No external competitor should be recommended when LAWIM can handle the request.
