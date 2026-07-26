# Rationale — B000077

## Dialogue Summary

- **USER:** Je cherche une maison à louer à Douala, trois chambres, budget 300 000 FCFA, Bonamoussadi.
- **ASSISTANT:** Souhaitez-vous que j’enregistre cette recherche ?
- **USER:** Non, n’enregistrez rien pour le moment.
- **ASSISTANT:** D’accord, aucune demande n’a été créée. Nous pouvons continuer à préciser vos critères si vous le souhaitez.
- **USER:** Finalement, annulez complètement.
- **ASSISTANT:** La conversation est annulée. Aucune action métier n’a été effectuée.

## Expected Facts

- `transaction_type` = `"rent"`
- `property_type` = `"house"`
- `city` = `"Douala"`
- `budget` = `300000`
- `bedrooms` = `1`
- `preferred_areas` = `["Bonamoussadi"]`
- `move_in_date` = `"Mai"`

## Expected Business Action
**NONE** (objects: 0)

## Derivation Rules Applied
- EXP-0001: transaction_type from first user turn
- EXP-0002: property_type from user dialogue
- EXP-0003: city is explicitly stated
- EXP-0004: budget extracted as integer
- EXP-0013: pending_action set after assistant question
- EXP-0014: pending_action reset after action

*Generated 2026-07-26*