# Rationale — B000095

## Dialogue Summary

- **USER:** I wan rent house for Yaoundé.
- **ASSISTANT:** How much you fit pay every month?
- **USER:** Ma budget na 180 thousand.
- **ASSISTANT:** How many bedroom you need?
- **USER:** Na 2 bedroom.
- **ASSISTANT:** Which area you prefer?
- **USER:** Melen
- **ASSISTANT:** Which time you wan enter the house?
- **USER:** September.
- **ASSISTANT:** I don note am. You wan make I register this search?
- **USER:** Yes, register am.
- **ASSISTANT:** Your search don register well.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"house"`
- `city` = `"Yaoundé"`
- `budget` = `2`
- `bedrooms` = `2`
- `preferred_areas` = `["Melen"]`
- `move_in_date` = `"September"`

## Expected Business Action
**CREATE_SEARCH** (objects: 1)

## Derivation Rules Applied
- EXP-0001: transaction_type from first user turn
- EXP-0002: property_type from user dialogue
- EXP-0003: city is explicitly stated
- EXP-0004: budget extracted as integer
- EXP-0013: pending_action set after assistant question
- EXP-0014: pending_action reset after action

*Generated 2026-07-26*