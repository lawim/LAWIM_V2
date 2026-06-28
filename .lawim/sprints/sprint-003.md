# Sprint 003 - Base de donnees et stockage

- Date: 2026-06-28
- Scope: Sprint 003 execution controlee
- Status: EN COURS

## Objectif
Installer la persistance, la structure initiale et les capacites de sauvegarde.

## Decision
GO AVEC RESERVES

## Portee
- PostgreSQL et schema relationnel;
- Prisma baseline et conventions de migration;
- stockage, sauvegardes, restauration et archivage;
- cohérence avec les references officielles de donnees et de stockage.

## Tickets
- T03.01 - PostgreSQL foundation
- T03.02 - Prisma baseline
- T03.03 - Backup primitives

## Dependances
- Sprint 002 cloture et PCC coherent.
- T02.03.
- `docs/Directive/06-DATABASE-REFERENCE.md`.
- `docs/Directive/14-STORAGE-REFERENCE.md`.

## Chemin critique
- Decision DG d'ouverture -> T03.01 -> T03.02 et T03.03 -> cloture Sprint 003.

## Risques d'entree
- derive de schema ou de contrainte entre PostgreSQL et le modele canonique;
- derivation des migrations Prisma par rapport au modele documentaire;
- sauvegarde ou restauration incomplète;
- confusion entre persistance, archivage et stockage de reprise.

## Avancement
- T03.01: ferme;
- T03.02: a venir;
- T03.03: a venir;
- Tickets couverts: 1/3.

## Cloture
- Rapport de cloture: reports/sprint-003/SPRINT-003-CLOSURE-REPORT.md
- Decision proposee: GO AVEC RESERVES
- Sprint 004: non ouvert
