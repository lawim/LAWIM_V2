# Canaux Et Omnicanal

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Definition
Web, WhatsApp, Telegram et Email sont des adaptateurs techniques autour d'une logique metier centralisee.

## Interdictions
Un canal ne possede aucune logique de decision, memoire metier, choix de dossier, qualification, matching, relation ou reponse autonome.

## Exigences
- Identite de canal liee a User ou profil provisoire.
- Verification du canal avant action sensible.
- Idempotence des webhooks.
- Normalisation des messages entrants.
- Continuites cross-channel sans perte d'etat.
- Handover humain coherent entre canaux.
