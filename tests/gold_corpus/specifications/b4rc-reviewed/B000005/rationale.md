# Rationale — B000005

## Dialogue Summary

- **USER:** Bonjour, je cherche un maison à louer à Yaoundé.
- **ASSISTANT:** Quel budget mensuel souhaitez-vous consacrer à cette location ?
- **USER:** Mon budget maximum est de 200 000 FCFA.
- **ASSISTANT:** Combien de chambres souhaitez-vous ?
- **USER:** 2 chambres.
- **ASSISTANT:** Quels quartiers préférez-vous à Yaoundé ?
- **USER:** Melen ou Ngoa-Ekellé.
- **ASSISTANT:** À partir de quand souhaitez-vous emménager ?
- **USER:** En septembre.
- **ASSISTANT:** Récapitulatif : maison à louer à Yaoundé, budget 200 000 FCFA, 2, zones Melen ou Ngoa-Ekellé, entrée en septembre. Souhaitez-vous que j’enregistre cette recherche ?
- **USER:** Oui, enregistrez-la.
- **ASSISTANT:** Votre demande de recherche a bien été enregistrée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"house"`
- `city` = `"Yaoundé"`
- `move_in_date` = `"Septembre"`
- `budget` = `2`
- `bedrooms` = `2`
- `preferred_areas` = `["Melen", "Ngoa-Ekellé"]`

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