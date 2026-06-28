# Sprint 005 Planning Report

- Sprint: Sprint 005
- Date: 2026-06-28
- Scope: Preparation only
- Statut propose: READY_FOR_DG_OPENING

## 1. Resume du Sprint 004 herite

Sprint 004 est cloture officiellement. Les trois tickets planifies sont couverts, le risque bloquant reste false et le PCC est coherent avec la trace de cloture. Le socle authentification, jetons et MFA reste la reference technique immediate.

## 2. Objectif du Sprint 005

Organiser les utilisateurs, les roles, les organisations et la matrice de permissions de LAWIM_V2. Ce sprint correspond au bloc S005 du plan directeur d implementation et reste aligne avec les references `08-ROLE-REFERENCE.md`, `19-ADMINISTRATION-REFERENCE.md`, `13-ARCHITECTURE-GOVERNANCE-REFERENCE.md`, `15-SECURITY-REFERENCE.md` et `06-DATABASE-REFERENCE.md`.

## 3. Liste des tickets

| Ticket | Titre | Entree | Sortie | Dependances |
| --- | --- | --- | --- | --- |
| T05.01 | User lifecycle | Sprint 004 cloture, PCC coherent, T04.03 valide, references role et database disponibles | Comptes, profils, statuts et transitions utilisateur | T04.03, 08-ROLE-REFERENCE.md, 06-DATABASE-REFERENCE.md |
| T05.02 | Organization model | T05.01 ferme, contrat utilisateur confirme | Arbre organisationnel, agences, partenaires et equipes | T05.01, 19-ADMINISTRATION-REFERENCE.md, 13-ARCHITECTURE-GOVERNANCE-REFERENCE.md |
| T05.03 | Permissions matrix | T05.02 ferme, modele organisationnel confirme | RBAC/ABAC, visibilite et acces aux ressources | T05.02, 08-ROLE-REFERENCE.md, 15-SECURITY-REFERENCE.md |

## 4. Ordre recommande

1. T05.01 - User lifecycle.
2. T05.02 - Organization model.
3. T05.03 - Permissions matrix.

T05.02 et T05.03 peuvent etre prepares apres T05.01, mais T05.01 reste le gate dur du sprint.

## 5. Dependances

- Decision DG d ouverture du Sprint 005.
- Confirmation de cloture Sprint 004 et validation PCC.
- T04.03 comme gate technique.
- `08-ROLE-REFERENCE.md` pour les statuts et les matrices de roles.
- `19-ADMINISTRATION-REFERENCE.md` pour l organisation et les rattachements.
- `13-ARCHITECTURE-GOVERNANCE-REFERENCE.md` pour les conventions de structure.
- `15-SECURITY-REFERENCE.md` pour la matrice d acces.
- `06-DATABASE-REFERENCE.md` pour le modele de persistance.

## 6. Chemin critique

Confirmation de cloture Sprint 004 -> Decision DG d ouverture -> T05.01 -> T05.02 -> T05.03 -> cloture Sprint 005.

T05.01 est le gate dur. T05.02 et T05.03 ne peuvent pas demarrer avant lui et doivent tous deux etre disponibles avant qu un lancement du sprint soit considere coherent.

## 7. Risques

- Une duplication d identites pourrait créer des comptes incoherents.
- Une structure organisationnelle mal alignee pourrait casser les rattachements agences / partenaires / equipes.
- Une matrice de permissions insuffisamment explicite pourrait exposer des ressources sensibles.
- Des secrets reels ou des droits trop larges ne sont pas acceptables dans ce sprint.

## 8. Recommandations

- Reutiliser les references role, administration et architecture avant toute creation de logique de comptes.
- Garder la matrice de permissions strictement alignee avec le modele canonique.
- Conserver les secrets et les politiques d acces hors depot et hors perimetre non trace.
- Maintenir T05.01 comme gate dur pour la suite du sprint.

## 9. Etat du PCC

- Sprint 004: TERMINE.
- Tickets Sprint 004: 3/3 couverts.
- Blocking risk: false.
- PCC: coherent avec la cloture et les fondations heritees.
- Sprint 005: prepare, non ouvert.
- Aucun ticket Sprint 005 n existe encore.
- Les registres dependances et risques restent alignes avec l ouverture preparee.

## 10. Decision proposee au Directeur General

GO AVEC RESERVES. Le Sprint 005 peut etre ouvert une fois la decision DG tracee, sous reserve de conserver les contrats d utilisateurs, d organisations et de permissions strictement alignes avec les references officielles.

```yaml
sprint: 005
status: READY_FOR_DG_OPENING
planning: PASS
dependencies: VERIFIED
risks: ACCEPTABLE
blocking_risk: false
next_ticket: T05.01
decision_required: true
```
