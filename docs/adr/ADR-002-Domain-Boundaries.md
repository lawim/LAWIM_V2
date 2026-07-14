# Frontieres De Domaines

Statut: Accepted
Date: 2026-07-14
Commit: d30d61e1d89427ece9c180cec4639cce77fdcba3

## Contexte
LAWIM_V2 contient plusieurs visions documentaires et des rapports qui ont parfois ete utilises comme specifications. Les validations live ont montre que certains composants annonces comme valides ne prouvent pas la conformite metier.

## Probleme
Sans decision explicite, le depot conserve plusieurs realites actives et rend la Mission 2 risquee.

## Decision
Les domaines canoniques, dependances autorisees et dependances interdites sont fixes par 03_DOMAIN_BOUNDARIES.

## Consequences
La specification canonique prime sur les anciens rapports. Les suppressions documentaires sont assumees par Git. Le code existant peut etre conserve, nettoye, supprime ou reconstruit selon la matrice canonique.

## Alternatives rejetees
Laisser les modules actuels definir les domaines.

## Impacts
Documentation, exigences, API cibles, tests et plans de decommissionnement doivent pointer vers `docs/canonical/`.
