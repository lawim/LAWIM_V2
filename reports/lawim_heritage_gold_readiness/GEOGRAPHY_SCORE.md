# GEOGRAPHY SCORE — Heritage Gold Readiness

**Audité par :** Geography Expert (H0.3)
**Date :** 2026-07-15

## Score global : 46/100

## Sous-dimensions

| # | Dimension | Score | Justification |
|---|-----------|:-----:|---------------|
| 1 | **Cities coverage** | 72 | 28 villes (10 prioritaires + 18 secondaires). Les 10 prioritaires ont métadonnées complètes. Les 18 secondaires sont squelettiques (pas de districts, pas d'ID région). |
| 2 | **Neighborhood/quartier coverage** | 65 | 382 quartiers dans 10 villes. ZÉRO quartier pour les 18 villes secondaires. Distribution inégale (Yaoundé 109, Nkongsamba 3). |
| 3 | **GPS data coverage** | 48 | 239/382 = 62.6%. Note D. ZÉRO metadata (gps_source=null, confidence=0, last_verified=null pour tous les districts). |
| 4 | **Proximity/voisinage rules** | 15 | **Gap critique.** 0/382 districts ont des liens `nearby`. Données d'affinité seulement pour 2/10 villes. 8 villes prioritaires sans aucune donnée de voisinage. |
| 5 | **Geographic scoring** | 35 | Formule documentée mais 40% du poids dépend des données d'affinité qui n'existent que pour 2 villes. 25% du poids (cluster) n'a aucune donnée. |
| 6 | **Alias handling** | 45 | Villes : bon (5-9 alias + typos). Districts : 382/382 ont `aliases: []` (vide). Fichier district_aliases.json : 14 paires seulement (Douala). Levenshtein seuil 3 OK. |
| 7 | **Hierarchy levels** | 25 | 10 niveaux documentés mais seulement niveaux 6-7 bien remplis. Niveaux 3-5 partiels. Niveau 8 : 4 entrées (Buea). Niveau 9 : ZÉRO landmarks. Niveaux SUBDIVISION/ZONE déclarés mais ZÉRO données. |
| 8 | **Location extraction** | 62 | 3 patterns (à, dans, quartier) + Levenshtein + formule confiance. OK pour mots uniques. Pas d'extraction multi-mots. Portée limitée. |

## Forces

- 28 villes documentées avec coordonnées et priorités
- 382 quartiers dans 10 villes
- Normalisation Levenshtein fonctionnelle

## Faiblesses critiques

- Voisinage (15/100) : zéro lien nearby, affinité pour 2 villes seulement
- Hiérarchie (25/100) : 5 niveaux sur 10 vides ou presque
- Scoring (35/100) : formule sans données d'entrée
- GPS (48/100) : 62.6% sans aucune metadata de qualité
- Alias districts (45/100) : zéro alias dans le fichier principal

## Conclusion

La géographie est le domaine le plus faible. Les données de voisinage, nécessaires au matching, sont quasi inexistantes. LAWIM_V2 ne peut pas faire de matching géographique intelligent sans ces données.
