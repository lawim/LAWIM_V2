# Sprint 002 - Infrastructure et environnements

- Date: 2026-06-28
- Scope: Sprint 002 execution controlee
- Status: EN COURS

## Objectif
Disposer d'un runtime local reproductible, d'une observabilite de base et d'un squelette CI minimal pour preparer l'execution controlee du programme.

## Decision
GO AVEC RESERVES

## Portee
- Docker baseline et conventions de build / tag.
- Runtime observability: logs, health checks et signaux de degradation.
- CI skeleton: build, lint et smoke tests.

## Tickets
- T02.01 - Docker baseline
- T02.02 - Runtime observability
- T02.03 - CI skeleton

## Ticket suivant
- T02.02 - Runtime observability

## Dependances
- Sprint 001 cloture et PCC coherent.
- T02.01 depend de T01.01, T01.02, T01.03, T01.04 et T01.05.
- T02.02 depend de T02.01, T01.09 et T01.10.
- T02.03 depend de T02.01, T01.07 et T01.08.

## Chemin critique
- Confirmation de cloture Sprint 001 -> Decision DG d'ouverture -> T02.01 -> T02.02 et T02.03.

## Risques d'entree
- Derive entre la base runtime et les conventions d'environnements heritees.
- Exposition accidentelle de secrets ou de donnees sensibles dans les traces d'execution.
- Activation prematuree du CI sans base runtime et observabilite suffisantes.

## Cadre
- La documentation officielle prime sur toute autre source.
- Un ticket ne couvre qu'une responsabilite principale.
- Une IA ne peut pas modifier seule les regles fondatrices.
- Toute decision sensible doit etre explicite, tracable et relue.
- Cette mission ne modifie ni la gouvernance, ni les contrats, ni les regles metier.
