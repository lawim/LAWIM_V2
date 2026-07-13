# Property Search Qualification Matrix

This matrix is the canonical source for search qualification across Web, WhatsApp, and Telegram.
It complements `docs/platform/TRANSACTION_QUALIFICATION_AND_COMMERCIAL_FLOW.md`.

## Core rules

- Reuse the existing product matrices.
- Do not redefine criteria per channel.
- Distinguish required, recommended, optional, derived, and already known fields.
- Ask only the next field that is actually missing.
- Once the minimum search threshold is met, move to search or matching instead of extending the questionnaire.
- Keep the same persona and the same LAWIM memory across channels.

## Transaction families

- `BUY`
- `SELL`
- `RENT`
- `RENT_OUT`
- `INVESTMENT`
- `LAND_ACQUISITION`
- `CONSTRUCTION`
- `PROFESSIONAL_SEARCH`
- `FUNDING`

## Typical fields

- Operation
- Property type
- Location
- Budget
- Timing
- Surface
- Rooms
- Preferences
- Legal or documentary constraints
- Decision maker
- Consent status

## Minimum search thresholds

- Rental studio: city, budget, property type
- Purchase: city, budget, property type
- Land purchase: city, budget, surface
- Construction: city, land status, budget
- Investment: city, budget, asset type
- Professional search: professional type, city
- Funding: amount, project type

## Commercial maturity

- `INFORMATION`: the need is being clarified.
- `EXPLORATION`: the user is comparing options.
- `ACTIVE`: the minimum threshold is complete and LAWIM can act.
- `IMMEDIATE`: the dossier is ready for visit, offer, consent, or conclusion steps.

## Qualification score

The internal score is based on:

- need clarity;
- location;
- budget coherence;
- financing or funds;
- deadline;
- decision maker;
- accepted conditions;
- availability for next action.

The score remains internal and can drive:

- dossier priority;
- search activation;
- matching activation;
- follow-up timing.

## Examples

- Rental studio: city, budget, property type, then bedroom count and neighborhood.
- Land purchase: city, budget, surface, then purpose and legal constraints.
- Construction: city, land status, budget, then building type and surface.

## Notes

- Search must stay inside LAWIM resources.
- Optional data can refine results later without blocking progress.
- A known field must never be requested twice.
