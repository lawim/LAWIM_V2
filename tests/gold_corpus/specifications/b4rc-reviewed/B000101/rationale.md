# Rationale — B000101

## Dialogue Summary

- **USER:** Je cherche un maison à louer à Douala, budget 100 000 FCFA.
- **ASSISTANT:** Combien de chambres souhaitez-vous ?
- **USER:** 1 chambre(s).
- **ASSISTANT:** Quel quartier préférez-vous à Douala ?
- **USER:** Bonamoussadi
- **ASSISTANT:** Quand souhaitez-vous emménager ?
- **USER:** En septembre.
- **ASSISTANT:** Je récapitule : location, maison, à Douala, budget 100 000 FCFA, 1 chambre(s), zones Bonamoussadi, entrée septembre. Souhaitez-vous enregistrer ?
- **USER:** Non, corrigez seulement le budget : 120 000 FCFA.
- **ASSISTANT:** Budget corrigé. Nouveau récapitulatif : location, maison, à Douala, budget 120 000 FCFA, 1 chambre(s), zones Bonamoussadi, entrée septembre. Souhaitez-vous enregistrer ?
- **USER:** Oui.
- **ASSISTANT:** La recherche corrigée a été enregistrée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"house"`
- `city` = `"Douala"`
- `budget` = `120000`
- `move_in_date` = `"Septembre"`
- `bedrooms` = `1`
- `preferred_areas` = `["Bonamoussadi"]`

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