# Rationale — B000056

## Dialogue Summary

- **USER:** Je cherche un appartement à louer à Yaoundé, budget 150 000 FCFA, deux chambres à Bastos.
- **ASSISTANT:** À partir de quand souhaitez-vous emménager ?
- **USER:** En octobre.
- **ASSISTANT:** Je récapitule : appartement à Bastos, deux chambres, budget 150 000 FCFA, entrée en octobre. Souhaitez-vous enregistrer ?
- **USER:** Non, corrigez : mon budget est 200 000 FCFA et je préfère Melen, pas Bastos.
- **ASSISTANT:** Correction prise en compte : budget 200 000 FCFA, zone Melen. Souhaitez-vous maintenant enregistrer la recherche ?
- **USER:** Oui.
- **ASSISTANT:** La recherche corrigée a bien été enregistrée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"apartment"`
- `city` = `"Yaoundé"`
- `budget` = `200000`
- `bedrooms` = `1`
- `preferred_areas` = `["Melen", "Bastos"]`
- `move_in_date` = `"Octobre"`

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