# Rationale — B000090

## Dialogue Summary

- **USER:** I am looking for an apartment to rent in Douala.
- **ASSISTANT:** What is your maximum monthly budget?
- **USER:** 250,000 FCFA.
- **ASSISTANT:** How many bedrooms do you need?
- **USER:** Two bedrooms.
- **ASSISTANT:** Which area do you prefer?
- **USER:** Makepe
- **ASSISTANT:** When would you like to move in?
- **USER:** In October.
- **ASSISTANT:** Would you like me to register this search?
- **USER:** Yes, please register it.
- **ASSISTANT:** Your search request has been registered.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"apartment"`
- `city` = `"Douala"`
- `budget` = `250`
- `preferred_areas` = `["Makepe"]`
- `move_in_date` = `"October"`

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