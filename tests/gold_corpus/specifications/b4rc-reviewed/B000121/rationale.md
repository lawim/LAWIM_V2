# Rationale — B000121

## Dialogue Summary

- **USER:** Location maison à Douala, 100 000 FCFA, Bonamoussadi, septembre.
- **ASSISTANT:** Je récapitule : location, maison, à Douala, budget 100 000 FCFA, 1 chambre(s), zones Bonamoussadi, entrée septembre. Souhaitez-vous enregistrer ?
- **USER:** Pas encore. Je veux finalement 2 chambres.
- **ASSISTANT:** Nombre de chambres corrigé. Nouveau récapitulatif : location, maison, à Douala, budget 100 000 FCFA, 2 chambre(s), zones Bonamoussadi, entrée septembre. Enregistrer ?
- **USER:** Et l'entrée doit être en novembre, pas septembre.
- **ASSISTANT:** Date corrigée. Nouveau récapitulatif : location, maison, à Douala, budget 100 000 FCFA, 2 chambre(s), zones Bonamoussadi, entrée novembre. Enregistrer ?
- **USER:** Oui.
- **ASSISTANT:** Votre recherche a bien été enregistrée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"house"`
- `city` = `"Douala"`
- `budget` = `2`
- `preferred_areas` = `["Bonamoussadi"]`
- `move_in_date` = `"Septembre"`
- `bedrooms` = `2`

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