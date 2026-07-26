# Rationale — B000083

## Dialogue Summary

- **USER:** Je cherche un appartement à louer à Yaoundé.
- **ASSISTANT:** Quel budget mensuel ?
- **USER:** 180 000 FCFA.
- **ASSISTANT:** Combien de chambres ?
- **USER:** Deux chambres.
- **SYSTEM:** SERVICE_RESTART
- **USER:** Je préfère Melen ou Ngoa-Ekellé.
- **ASSISTANT:** À partir de quand souhaitez-vous emménager ?
- **USER:** En septembre.
- **ASSISTANT:** Souhaitez-vous enregistrer cette recherche ?
- **USER:** Oui.
- **ASSISTANT:** La recherche a été enregistrée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"apartment"`
- `city` = `"Yaoundé"`
- `budget` = `180000`
- `bedrooms` = `2`
- `preferred_areas` = `["Melen", "Ngoa-Ekellé"]`
- `move_in_date` = `"Septembre"`

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