# Sprint 006 - Coeur immobilier

- Date: 2026-06-28
- Scope: Sprint 006 execution controlee
- Status: EN COURS

## Objectif
Construire le socle des biens, attributs et prix de LAWIM_V2.

## Decision
GO AVEC RESERVES

## Portee
- biens immobiliers, attributs, prix et variations;
- publication, validation et archivage des biens;
- normalisation des attributs et des valeurs de prix;
- alignement avec les references officielles de biens, d'attributs, de prix, de workflow et de tests;
- aucun secret reel.

## Tickets
- T06.01 - Property domain schema
- T06.02 - Pricing alignment
- T06.03 - Publication guardrails

## Dependances
- Sprint 005 cloture et PCC coherent.
- T05.03.
- `docs/Directive/02-PROPERTY-REFERENCE.md`.
- `docs/Directive/02H-ATTRIBUTE-CATALOG.md`.
- `docs/Directive/02I-PRICING-REFERENCE.md`.
- `docs/Directive/11-REPORTING-REFERENCE.md`.
- `docs/Directive/05-WORKFLOW-REFERENCE.md`.
- `docs/Directive/12-TESTS-REFERENCE.md`.

## Chemin critique
- Decision DG d'ouverture -> T06.01 -> T06.02 -> T06.03 -> cloture Sprint 006.

## Risques d entree
- donnees incoherentes ou incompletes;
- confusion entre types de biens;
- variation de prix non normalisee;
- publication incoherente ou prematuree.

## Validation DG
- en attente.

## Avancement
- T06.01: ferme
- T06.02: ferme
- T06.03: en attente
- Tickets couverts: 2/3
