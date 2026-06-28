# Sprint 008 Planning Report

- Sprint: Sprint 008
- Date: 2026-06-28
- Scope: Preparation only
- Statut propose: READY_FOR_DG_OPENING

## 1. Resume du Sprint 007 herite

Sprint 007 est cloture officiellement. Les trois tickets planifies sont couverts, le risque bloquant reste false et le PCC est coherent avec la trace de cloture. Le socle medias, documents et geolocalisation est consolide et la suite peut se concentrer sur le moteur de conversation.

## 2. Objectif du Sprint 008

Permettre les echanges tracables entre utilisateurs et partenaires. Ce sprint correspond au bloc S008 du plan directeur d implementation et reste aligne avec les references `03-CONVERSATION-REFERENCE.md`, `06-DATABASE-REFERENCE.md`, `10-NOTIFICATION-REFERENCE.md`, `14-STORAGE-REFERENCE.md` et `12-TESTS-REFERENCE.md`.

## 3. Liste des tickets

| Ticket | Titre | Entree | Sortie | Dependances |
| --- | --- | --- | --- | --- |
| T08.01 | Conversation model | Sprint 007 cloture, PCC coherent, T07.03 valide, references conversation et database disponibles | Threads, participants et statuts de conversation | T07.03, 03-CONVERSATION-REFERENCE.md, 06-DATABASE-REFERENCE.md |
| T08.02 | Messaging flow | T08.01 ferme, contrat conversation confirme | Envoi, reception, lecture et livraison des messages | T08.01, 03-CONVERSATION-REFERENCE.md, 10-NOTIFICATION-REFERENCE.md |
| T08.03 | Attachments and history | T08.02 ferme, flux de messages confirme | Pieces jointes, historique et audit trail | T08.02, 14-STORAGE-REFERENCE.md, 12-TESTS-REFERENCE.md |

## 4. Ordre recommande

1. T08.01 - Conversation model.
2. T08.02 - Messaging flow.
3. T08.03 - Attachments and history.

T08.01 est le gate dur du sprint. T08.02 et T08.03 ne peuvent pas demarrer avant la structuration de la conversation.

## 5. Dependances

- Decision DG d ouverture du Sprint 008.
- Confirmation de cloture Sprint 007 et validation PCC.
- T07.03 comme gate technique.
- `03-CONVERSATION-REFERENCE.md` pour la structure des conversations.
- `06-DATABASE-REFERENCE.md` pour la persistance et les relations.
- `10-NOTIFICATION-REFERENCE.md` pour la livraison et les etats de message.
- `14-STORAGE-REFERENCE.md` pour les pieces jointes.
- `12-TESTS-REFERENCE.md` pour la validation et la non-regression.

## 6. Chemin critique

Confirmation de cloture Sprint 007 -> Decision DG d ouverture -> T08.01 -> T08.02 -> T08.03 -> cloture Sprint 008.

T08.01 est le gate dur. T08.02 et T08.03 ne peuvent pas demarrer avant lui et doivent tous deux etre disponibles avant qu'un lancement du sprint soit considere coherent.

## 7. Risques

- Un bruit conversationnel ou du spam pourrait degrader les echanges.
- Une perte de contexte pourrait casser le fil de conversation.
- Des conversations orphelines pourraient devenir difficiles a gouverner.
- Des pieces jointes mal tracees pourraient brouiller l audit trail.

## 8. Recommandations

- Reutiliser les references conversation, base de donnees, notification, stockage et tests avant toute creation de logique.
- Garder la conversation, les messages et les pieces jointes explicitement traces.
- Conserver l historique et la livraison comme contractuels.
- Maintenir T08.01 comme gate dur pour la suite du sprint.

## 9. Etat du PCC

- Sprint 007: TERMINE.
- Tickets Sprint 007: 3/3 couverts.
- Blocking risk: false.
- PCC: coherent avec la cloture et les fondations heritees.
- Sprint 008: prepare, non ouvert.
- Aucun ticket Sprint 008 n existe encore.
- Les registres dependances et risques restent alignes avec l'ouverture preparee.

## 10. Decision proposee au Directeur General

GO AVEC RESERVES. Le Sprint 008 peut etre ouvert une fois la decision DG tracee, sous reserve de garder les conversations, les messages et les pieces jointes strictement alignes avec les references officielles.

```yaml
sprint: 008
status: READY_FOR_DG_OPENING
planning: PASS
dependencies: VERIFIED
risks: ACCEPTABLE
blocking_risk: false
next_ticket: T08.01
decision_required: true
```
