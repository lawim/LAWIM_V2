# Platform Readiness

LAWIM_V2 readiness is centered on a single product identity, a shared conversation lifecycle, a central orchestrator, and a commercial journey that can actually progress a dossier.

## Current readiness targets

- LAWIM AI is the only official assistant identity.
- Web, WhatsApp, Telegram, and email must share the same conversation model.
- Qualification must reuse the canonical matrices already validated in the product.
- The system must ask one useful question at a time and stop asking once the minimum search threshold is reached.
- Search, matching, visits, offers, negotiation, and follow-up must remain on the LAWIM path.
- Responses must be validated before delivery.
- Feature flags and kill switches must control rollout safely.
- External competitors must never be suggested when LAWIM can handle the request.

## Operational anchors

- Official email: `contact@lawim.app`
- Official WhatsApp: `+237 686 822 667`
- Official Telegram bot: `@lawim_bot`

## Evidence sources

- `code/lawim_v2/persona.py`
- `code/lawim_v2/brain/*`
- `code/lawim_v2/ai/*`
- `frontend/apps/web/src/AdvisorPanel.tsx`
- `docs/platform/TRANSACTION_QUALIFICATION_AND_COMMERCIAL_FLOW.md`
- `docs/platform/PROPERTY_SEARCH_QUALIFICATION_MATRIX.md`
- `docs/platform/CONVERSATION_LIFECYCLE.md`
