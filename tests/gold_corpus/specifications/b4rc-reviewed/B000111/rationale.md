# Rationale — B000111

## Dialogue Summary

- **USER:** Je veux louer un appartement à Kribi.
- **ASSISTANT:** Quel budget mensuel ?
- **USER:** 100 000 FCFA.
- **ASSISTANT:** Combien de chambres ?
- **USER:** 1.
- **ASSISTANT:** Quel quartier préférez-vous ?
- **USER:** Dombe
- **ASSISTANT:** Quand souhaitez-vous emménager ?
- **USER:** En octobre.
- **ASSISTANT:** Récapitulatif : location, appartement, à Kribi, budget 100 000 FCFA, 1 chambre(s), zones Dombe, entrée octobre. Enregistrer ?
- **USER:** Changez le budget à 120 000 FCFA et remplacez Dombe par Mboamanga.
- **ASSISTANT:** Les deux corrections sont prises en compte : location, appartement, à Kribi, budget 120 000 FCFA, 1 chambre(s), zones Mboamanga, entrée octobre. Enregistrer ?
- **USER:** Oui, enregistrez.
- **ASSISTANT:** La demande corrigée a été enregistrée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"apartment"`
- `city` = `"Kribi"`
- `budget` = `120000`
- `bedrooms` = `1`
- `preferred_areas` = `["Dombe", "Mboamanga"]`
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