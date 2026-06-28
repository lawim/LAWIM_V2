# Sprint 008 - Conversation Engine

- Date: 2026-06-28
- Scope: Sprint 008 execution controlee
- Status: CLOTURE

## Objectif
Permettre les echanges tracables entre utilisateurs et partenaires.

## Decision
GO AVEC RESERVES

## Portee
- conversations, threads, participants et statuts;
- messages, lectures, livraison et historique;
- pieces jointes et audit trail;
- alignement avec les references officielles de conversation, base de donnees, notification, stockage et tests;
- aucun secret reel.

## Tickets
- T08.01 - Conversation model
- T08.02 - Messaging flow
- T08.03 - Attachments and history

## Dependances
- Sprint 007 cloture et PCC coherent.
- T07.03.
- `docs/Directive/03-CONVERSATION-REFERENCE.md`.
- `docs/Directive/06-DATABASE-REFERENCE.md`.
- `docs/Directive/10-NOTIFICATION-REFERENCE.md`.
- `docs/Directive/14-STORAGE-REFERENCE.md`.
- `docs/Directive/12-TESTS-REFERENCE.md`.

## Chemin critique
- Decision DG d'ouverture -> T08.01 -> T08.02 -> T08.03 -> cloture Sprint 008.

## Risques d'entree
- spam ou bruit conversationnel;
- perte de contexte ou de fil;
- conversations orphelines;
- pieces jointes mal tracees.

## Avancement
- T08.01: ferme
- T08.02: ferme
- T08.03: ferme
- Tickets couverts: 3/3

## Cloture
- Rapport de cloture: reports/sprint-008/SPRINT-008-CLOSURE-REPORT.md
- Decision proposee: GO AVEC RESERVES
- Sprint 009: non ouvert
