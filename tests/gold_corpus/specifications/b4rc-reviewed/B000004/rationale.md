# Rationale — B000004

## Dialogue Summary

- **USER:** Bonjour, je cherche un appartement à louer à Kribi.
- **ASSISTANT:** Quel budget mensuel souhaitez-vous consacrer à cette location ?
- **USER:** Mon budget maximum est de 180 000 FCFA.
- **ASSISTANT:** Combien de chambres souhaitez-vous ?
- **USER:** 1 chambres.
- **ASSISTANT:** Quels quartiers préférez-vous à Kribi ?
- **USER:** Dombe ou Mpangou.
- **ASSISTANT:** À partir de quand souhaitez-vous emménager ?
- **USER:** En septembre.
- **ASSISTANT:** Récapitulatif : appartement à louer à Kribi, budget 180 000 FCFA, 1, zones Dombe ou Mpangou, entrée en septembre. Souhaitez-vous que j’enregistre cette recherche ?
- **USER:** Oui, enregistrez-la.
- **ASSISTANT:** Votre demande de recherche a bien été enregistrée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"apartment"`
- `city` = `"Kribi"`
- `budget` = `1`
- `bedrooms` = `1`
- `preferred_areas` = `["Dombe", "Mpangou"]`
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