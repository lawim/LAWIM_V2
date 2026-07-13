# Transaction Qualification and Commercial Flow

LAWIM converts an expressed property intent into a controlled commercial journey. This document complements:

- `docs/platform/LAWIM_AI_PERSONA.md`
- `docs/platform/CONVERSATION_LIFECYCLE.md`
- `docs/platform/PROPERTY_SEARCH_QUALIFICATION_MATRIX.md`
- `docs/platform/AI_TRANSPARENCY_AND_LIMITATIONS.md`

## Purpose

- Qualify the project progressively.
- Reach the minimum data threshold as early as possible.
- Launch search, matching, and follow-up from LAWIM capabilities first.
- Avoid generic advice and avoid external competitor redirection.
- Keep one conversation, one dossier, one memory, and one next action.

## LAWIM First

Priority order:

1. Deterministic LAWIM action
2. Existing LAWIM data
3. Existing dossier or project
4. Qualification matrix
5. Internal search
6. Internal document or guide
7. LAWIM professional or partner
8. Matching
9. Relationship / consent
10. Human LAWIM agent
11. Controlled general explanation

If LAWIM can act, it must act.

## Transaction families

- `BUY`
- `SELL`
- `RENT`
- `RENT_OUT`
- `FURNISHED_RENT`
- `TEMPORARY_RENT`
- `AUTHORIZED_SUBLET`
- `CUSTOM_SEARCH`
- `SALE_MANDATE`
- `RENTAL_MANDATE`
- `PROPERTY_MANAGEMENT`
- `VALUATION`
- `NEGOTIATION`
- `INVESTMENT`
- `LAND_ACQUISITION`
- `CONSTRUCTION`
- `TURNKEY_PROJECT`

## Qualification principle

The engine asks only what is useful now.

- One useful question at a time.
- Never ask twice for a known fact.
- Distinguish required, recommended, optional, derived, and eliminating fields.
- Preserve contradictions in history instead of overwriting silently.
- Keep the user informed of the next action.

## Minimum viable qualification

Examples of minimum search thresholds:

- Rental search: city, budget, property type
- Purchase search: city, budget, property type
- Land search: city, budget, surface
- Investment search: city, budget, asset type
- Construction: city, land status, budget
- Professional search: profession type, city
- Funding: amount, project type

Once the minimum threshold is met, search or matching should start. Optional fields may still refine the result.

## Commercial maturity

Recommended levels:

- `INFORMATION`
- `EXPLORATION`
- `ACTIVE`
- `IMMEDIATE`

Typical interpretation:

- `INFORMATION`: the user is still clarifying the need.
- `EXPLORATION`: the need is emerging, but key fields are still missing.
- `ACTIVE`: the minimum threshold is met and LAWIM can act.
- `IMMEDIATE`: the dossier is ready for visit, consent, offer, or conclusion steps.

## Qualification score

The score remains internal and configurable.

Suggested weighting:

- Need clearly defined
- Location known
- Budget coherent
- Funds or financing credible
- Deadline defined
- Decision maker identified
- Conditions accepted
- Availability for visit or next action

The score is used to:

- prioritize dossiers;
- select the next question;
- trigger search or matching;
- decide follow-up timing.

## Commercial flow

Canonical sequence:

1. Welcome
2. Identification
3. Project definition
4. Qualification
5. Verification
6. Search
7. Matching
8. Selection
9. Consent
10. Relationship
11. Visit
12. Feedback
13. Offer
14. Negotiation
15. Documentation
16. Payment
17. Conclusion
18. Follow-up

## Visits

- A visit must have a property, date, time, responsible actor, and status.
- Confirm, reschedule, cancel, complete, or close the visit explicitly.
- Ask for feedback after the visit whenever possible.

## Offers and negotiation

- Track offer amount, author, recipient, validity, and history.
- Distinguish offer draft, submitted offer, counter-offer, accepted-in-principle, rejected, expired, and withdrawn.
- Never present an oral agreement as a concluded transaction.

## Documentation

Before a conclusion that needs verification:

- identify the declared actor;
- collect the available documents;
- mark each document as declared, received, checked, or confirmed;
- never validate a document from a photo alone.

## Follow-up

Follow-up must be:

- linked to the dossier;
- based on a concrete next action;
- spaced according to the user state;
- stoppable on request;
- auditable.

## Channel behavior

- Web can display more detail.
- WhatsApp should stay short and action-oriented.
- Telegram can surface quick choices and commands.
- The business logic stays identical across channels.

## Safety

- Never invent a property, a professional, a price, a payment, or a visit.
- Never recommend external platforms when LAWIM can handle the request.
- Show the AI limitation reminder when the topic is sensitive.
- Keep the same persona across all channels.

## Related runtime components

- `code/lawim_v2/brain/progression.py`
- `code/lawim_v2/brain/accompaniment.py`
- `code/lawim_v2/conversation_core/service.py`
- `code/lawim_v2/real_estate_intelligence/service.py`

