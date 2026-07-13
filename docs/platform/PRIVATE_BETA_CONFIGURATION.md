# PRIVATE_BETA Configuration

PRIVATE_BETA is the controlled deployment profile used before broad production rollout.

## Expected posture

- Activate only validated capabilities.
- Keep experimental or unvalidated features disabled.
- Keep sensitive kill switches and permissions auditable.

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

## Guardrails

- No feature should become visible only from the frontend.
- No permission should be granted by a flag alone.
- No unvalidated payment or relationship flow should be enabled by default.

