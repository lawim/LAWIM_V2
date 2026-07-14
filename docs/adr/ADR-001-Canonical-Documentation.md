# Documentation Canonique

Statut: Accepted
Date: 2026-07-14
Commit: d30d61e1d89427ece9c180cec4639cce77fdcba3

## Contexte
LAWIM_V2 contient plusieurs visions documentaires et des rapports qui ont parfois ete utilises comme specifications. Les validations live ont montre que certains composants annonces comme valides ne prouvent pas la conformite metier.

## Probleme
Sans decision explicite, le depot conserve plusieurs realites actives et rend la Mission 2 risquee.

## Decision
La specification active est centralisee dans docs/canonical et les anciens referentiels contradictoires sont supprimes.

## Consequences
La specification canonique prime sur les anciens rapports. Les suppressions documentaires sont assumees par Git. Le code existant peut etre conserve, nettoye, supprime ou reconstruit selon la matrice canonique.

## Alternatives rejetees
Garder les anciens documents marques obsoletes.

## Impacts
Documentation, exigences, API cibles, tests et plans de decommissionnement doivent pointer vers `docs/canonical/`.
