# Sprint 005 - Utilisateurs, roles, organizations

- Date: 2026-06-28
- Scope: Sprint 005 execution controlee
- Status: EN COURS

## Objectif
Organiser les utilisateurs, les roles, les organisations et la matrice de permissions de LAWIM_V2.

## Decision
GO AVEC RESERVES

## Portee
- utilisateurs, profils, statuts et transitions;
- organisations, agences, partenaires et equipes;
- roles, permissions et visibilite des ressources;
- alignement avec les references officielles de role, administration, architecture et securite;
- aucun secret reel.

## Tickets
- T05.01 - User lifecycle
- T05.02 - Organization model
- T05.03 - Permissions matrix

## Dependances
- Sprint 004 cloture et PCC coherent.
- T04.03.
- `docs/Directive/08-ROLE-REFERENCE.md`.
- `docs/Directive/19-ADMINISTRATION-REFERENCE.md`.
- `docs/Directive/13-ARCHITECTURE-GOVERNANCE-REFERENCE.md`.
- `docs/Directive/15-SECURITY-REFERENCE.md`.
- `docs/Directive/06-DATABASE-REFERENCE.md`.

## Chemin critique
- Decision DG d ouverture -> T05.01 -> T05.02 -> T05.03 -> cloture Sprint 005.

## Risques d entree
- duplication d identites ou de profils;
- confusion sur les rattachements organisationnels;
- matrice de permissions trop large ou insuffisamment explicite;
- confusion entre contrat documentaire et implementation sensible.

## Avancement
- T05.01: ferme;
- Tickets couverts: 1/3.

## Validation DG
- en attente.
