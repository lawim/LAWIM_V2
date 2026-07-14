# Evenements Observabilite Et Audit

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Evenements canoniques
`user.created`, `channel.verified`, `project.created`, `dossier.selected`, `fact.confirmed`, `search.requested`, `match.proposed`, `consent.requested`, `consent.granted`, `relationship.created`, `visit.scheduled`, `offer.submitted`, `payment.created`, `notification.sent`, `feature_flag.changed`, `audit.security_event`.

## Regles
Les evenements transportent identifiant, domaine source, correlation id, acteur, horodatage, payload minimal et niveau de sensibilite. L'observabilite technique ne remplace pas l'audit metier.
