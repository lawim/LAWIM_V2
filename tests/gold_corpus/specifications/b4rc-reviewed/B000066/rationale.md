# Rationale — B000066

## Dialogue Summary

- **USER:** Je cherche quelque chose de bien et pas cher.
- **ASSISTANT:** Cherchez-vous à louer ou à acheter ?
- **USER:** À louer.
- **ASSISTANT:** Quel type de bien recherchez-vous ?
- **USER:** Un petit logement.
- **ASSISTANT:** Par exemple un studio, une chambre moderne ou un appartement ?
- **USER:** Un studio.
- **ASSISTANT:** Dans quelle ville ?
- **USER:** Yaoundé
- **ASSISTANT:** Quel budget maximal ?
- **USER:** 100 000 FCFA.
- **ASSISTANT:** Quel quartier préférez-vous ?
- **USER:** Melen
- **ASSISTANT:** Quand souhaitez-vous emménager ?
- **USER:** Dès que possible.
- **ASSISTANT:** Souhaitez-vous que j’enregistre cette recherche de studio ?
- **USER:** Oui.
- **ASSISTANT:** La recherche a bien été enregistrée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"studio"`
- `city` = `"Yaoundé"`
- `budget` = `100000`
- `preferred_areas` = `["Melen"]`
- `move_in_date` = `"ASAP"`

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