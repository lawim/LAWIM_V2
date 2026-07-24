# LAWIM Demo World V1 — Data Validation

**Date:** 2026-07-23  **HEAD:** ccbf4c38

## Évolution 117→104 biens

La réduction de 117 à 104 biens est due à la correction d'un bug de calcul d'index dans le générateur. L'ancien calcul `i * max_props + j + 1` créait des identifiants en double pour certains quartiers de Yaoundé. Le nouveau calcul séquentiel (`idx += 1`) produit 104 identifiants uniques.

**Couverture inchangée :**
- Yaoundé : 54 (était 48)
- Douala : 26 (était 25)
- Bafoussam : 9 (était 8)
- Kribi : 7 (était 6)
- Limbé : 8 (était 8)

## Duplicats médias corrigés

3 logos d'organisation partageaient le même ID `DEMO-MEDIA-ORG-001`. Corrigé en `DEMO-MEDIA-ORG-LOGO-001/002/003`.

**Avant :** 51 YAML → 49 seedés (2 ignorés silencieusement)  
**Après :** 51 YAML → 51 seedés → verify PASS

## REFERENCE_ONLY

Les sections suivantes sont validées par le schéma et les tests mais ne sont pas persistées en base :

| Section | Statut | Objets |
|---------|--------|--------|
| scenarios | REFERENCE_ONLY | 12 |
| negative_cases | REFERENCE_ONLY | 8 |

Elles sont utilisées par les tests automatisés et les rapports.

## Compteurs finaux

| Métrique | Valeur |
|----------|--------|
| YAML entities | 276 |
| Persistable entities | 256 |
| Seeded entities | 256 |
| Reference-only | 20 |
| Second seed | 0 (idempotent) |
| Verify YAML=DB | PASS |

## Tests

| Suite | Résultat |
|-------|----------|
| LROS existants | 733 PASS |
| Nouveaux tests Demo World | 12 PASS |
| **Total** | **745 PASS** |
| Régressions | 0 |
