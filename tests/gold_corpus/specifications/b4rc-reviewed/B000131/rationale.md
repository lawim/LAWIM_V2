# Rationale — B000131

## Dialogue Summary

- **USER:** Je cherche un terrain à louer à Kribi.
- **ASSISTANT:** Quel est votre budget de location ?
- **USER:** 100 000 FCFA par mois.
- **ASSISTANT:** Souhaitez-vous préciser un quartier ?
- **USER:** Dombe
- **ASSISTANT:** Je récapitule : location, terrain, à Kribi, budget 100 000 FCFA, zones Dombe, entrée septembre. Enregistrer ?
- **USER:** Finalement je veux acheter, pas louer.
- **ASSISTANT:** D'accord, je remplace la location par un achat. Quel est votre budget d'achat ?
- **USER:** 12 000 000 FCFA.
- **ASSISTANT:** Nouveau récapitulatif : achat, terrain, à Kribi, budget 12 000 000 FCFA, zones Dombe. Souhaitez-vous enregistrer la recherche d'achat ?
- **USER:** Oui.
- **ASSISTANT:** La recherche d'achat a été enregistrée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"land"`
- `city` = `"Kribi"`
- `budget` = `12000`
- `preferred_areas` = `["Dombe"]`

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