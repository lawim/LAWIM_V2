# MATCHING SCORE — Heritage Gold Readiness

**Audité par :** Matching Expert (H0.3)
**Date :** 2026-07-15

## Score global : 93/100

## Sous-dimensions

| # | Dimension | Score | Justification |
|---|-----------|:-----:|---------------|
| 1 | **Scoring criteria & weights** | 100 | Poids V1 (city=30, neighborhood=25, budget=25, type=15, title=5) parfaitement alignés avec property_matching_v1.json. |
| 2 | **Boost rules & conditions** | 100 | 5 boosts (+25/+20/+15/+10/+20) vérifiés exactement. |
| 3 | **Penalty rules** | 100 | 3 pénalités (-10/-10/-50) vérifiées exactement. |
| 4 | **Exclusion rules** | 95 | 4 exclusions par statut + blacklist. Principe "Rank don't filter" confirmé. |
| 5 | **Preference handling** | 85 | Couvert via boosts et ordre de priorité. Pas de modèle de préférences dédié correspondant au niveau 4 (compatibilité préférentielle) du Decision Engine. |
| 6 | **Proximity/voisinage** | 95 | 5 niveaux de scoring géographique + 3 modes de mobilité corrects. Manque : geographic_weight=20 et mobility_weight=20. |
| 7 | **Budget tolerance rules** | 100 | Location ±20%, Achat ±15%, Invest ±25% parfaitement alignés. |
| 8 | **Decision engine algorithm** | 70 | **Gap :** L'algorithme 10 étapes du Gold est attribué à 04-DECISION-ENGINE-REFERENCE.md mais le source contient un algorithme différent (Load→Check→Select→Eliminate→Score→Rank→Propose→Wait→Learn→Recalc). |
| 9 | **Rematching rules** | 90 | 6 déclencheurs corrects. Source en liste 19+ répartis en 4 catégories. Concept de rematching sélectif manquant. |
| 10 | **Lead temperature & routing** | 98 | Seuils V1/V5, scoring CRM 7 facteurs, boosts, pénalités, scores de base : tous vérifiés. Gap V1→V5 documenté. |

## Forces

- Meilleur domaine du Gold (93/100)
- Tous les poids, boosts et pénalités vérifiés
- Budget tolerance parfaitement aligné
- Lead temperature et routing excellents

## Faiblesses

- Algorithme décisionnel 10 étapes : source citée ne correspond pas
- Rematching : 19+ déclencheurs réels vs 6 documentés
- Modèle de préférences : niveau 4 manquant

## Conclusion

Le matching est le domaine le plus solide du Gold. Avec 93/100, il est quasiment prêt pour reconstruction. Les seuls gaps sont l'algorithme décisionnel (source erronée) et les détails de rematching. LAWIM_V2 peut reconstruire le matching à partir du Gold avec une confiance élevée.
