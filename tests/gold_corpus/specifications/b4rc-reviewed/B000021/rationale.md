# Rationale — B000021

## Dialogue Summary

- **USER:** Je veux acheter un maison à Yaoundé.
- **ASSISTANT:** Quel est votre budget d’achat ?
- **USER:** Je peux aller jusqu’à 12 000 000 FCFA.
- **ASSISTANT:** Avez-vous des quartiers préférés ?
- **USER:** Bastos ou Mvan.
- **ASSISTANT:** Combien de chambres minimum ?
- **USER:** Trois chambres minimum.
- **ASSISTANT:** Je récapitule : achat d’un maison à Yaoundé, budget maximal 12 000 000 FCFA, zones Bastos ou Mvan, trois chambres minimum. Souhaitez-vous enregistrer cette recherche ?
- **USER:** Oui.
- **ASSISTANT:** La recherche d’achat a bien été enregistrée.

## Expected Facts

- `transaction_type` = `"buy"`
- `property_type` = `"house"`
- `city` = `"Yaoundé"`
- `move_in_date` = `"Mai"`
- `budget` = `12000`
- `preferred_areas` = `["Bastos", "Mvan"]`
- `bedrooms` = `3`

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