# Rationale — B000036

## Dialogue Summary

- **USER:** Je souhaite vendre mon maison situé à Melen, Yaoundé.
- **ASSISTANT:** Quel prix souhaitez-vous demander ?
- **USER:** 15 000 000 FCFA.
- **ASSISTANT:** Êtes-vous bien le propriétaire ou son mandataire autorisé ?
- **USER:** Oui, je suis le propriétaire.
- **ASSISTANT:** Par quel canal préférez-vous être recontacté ?
- **USER:** Par WhatsApp.
- **ASSISTANT:** Je récapitule : mise en vente d’un maison à Melen, Yaoundé, prix demandé 15 000 000 FCFA. Souhaitez-vous enregistrer cette demande ?
- **USER:** Oui, enregistrez.
- **ASSISTANT:** Votre demande de mise en vente a été enregistrée.

## Expected Facts

- `transaction_type` = `"sell"`
- `property_type` = `"house"`
- `city` = `"Yaoundé"`
- `preferred_areas` = `["Melen"]`
- `move_in_date` = `"Mai"`
- `budget` = `15000`
- `price` = `15000`
- `is_owner` = `true`

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