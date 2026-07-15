# Rapport de Validation — GEOGRAPHY_MODEL.md

**Auditeur :** Système de validation LAWIM  
**Date :** 2026-07-15  
**Branches vérifiées :** LAWIM, LAWIMA, ancienne_structure

---

## 1. Hiérarchie territoriale

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **21** | NON VALIDÉ | `district_hierarchy.json` ne contient **pas une hiérarchie à 8 niveaux**. Le fichier ne contient que 4 entrées (Muea, Great Soppo, GRA, Bolifamba) avec des listes de quartiers. Aucune structure Pays→Région→Département→Arrondissement→Commune→Ville→District→Quartier n'est présente. | FAIBLE |
| **22** | INTROUVABLE | `Subdivision` et `Zone` ne sont pas mentionnés dans `district_hierarchy.json`. Aucun fichier de la source référencée ne contient ces concepts comme niveaux supplémentaires. | FAIBLE |

## 2. Villes

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **23** | VALIDÉ | `system_prompt_v1.md:35-44` → Liste exacte des 10 villes prioritaires : Douala, Yaoundé, Bafoussam, Bamenda, Buea, Limbe, Kribi, Nkongsamba, Garoua, Maroua. Correspond parfaitement. | ÉLEVÉE |

## 3. Quartiers

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **24** | VALIDÉ | `LAWIM/KNOWLEDGE/neighborhoods/` contient 11 fichiers : `all_neighborhoods.json` + `douala.json`, `yaounde.json`, `bamenda.json`, `bafoussam.json`, `buea.json`, `garoua.json`, `kribi.json`, `limbe.json`, `maroua.json`, `nkongsamba.json`. Correspond. | ÉLEVÉE |
| **25** | PARTIELLEMENT VALIDÉ | Les quartiers Yaoundé (`bastos, essos, biyem assi, mvog, odza, nkoabang`) ne sont **pas listés dans `location_normalizer.py`** comme affirmé. Ce fichier ne contient pas de liste de quartiers (utilise une base de données). `bastos`, `essos`, `odza` sont bien référencés dans d'autres fichiers gateway. `biyem assi`, `mvog`, `nkoabang` non retrouvés dans les sources PY examinées. | MOYENNE |
| **26** | PARTIELLEMENT VALIDÉ | Les quartiers Douala (`akwa, bonapriso, bonamoussadi, makepe, deido, bonaberi`). `bonaberi` **absent** de tous les fichiers PY sources. Les autres sont bien présents dans les fichiers gateway. Même problème de source référencée (`location_normalizer.py` ne contient pas ces listes). | MOYENNE |

## 4. Variantes orthographiques

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **27** | NON VALIDÉ | Variantes `bastos→basto/bastoss/bastos village` : **aucune** n'est explicitement listée dans `location_normalizer.py`. La normalisation par Levenshtein pourrait les capturer, mais ce ne sont pas des mappings explicites. | FAIBLE |
| **28** | NON VALIDÉ | Variantes `essos→esos/essoss` : non trouvées dans `location_normalizer.py`. | FAIBLE |
| **29** | NON VALIDÉ | Variantes `biyem_assi→biyem/biyem-assi/biyemassi/biem assi` : non trouvées dans `location_normalizer.py`. | FAIBLE |
| **30** | NON VALIDÉ | Variantes `odza→odzaa/odja` : non trouvées dans `location_normalizer.py`. | FAIBLE |
| **31** | NON VALIDÉ | Variantes `akwa→aqua/akwah` : non trouvées dans `location_normalizer.py` (seulement "akwa" comme quartier). | FAIBLE |
| **32** | NON VALIDÉ | Variantes `bonamoussadi→bona moussadi/bonamussadi` : non trouvées dans `location_normalizer.py`. | FAIBLE |
| **33** | VALIDÉ | `location_normalizer.py:44` → `best_distance = 3` : le seuil max de Levenshtein est bien 3. | ÉLEVÉE |
| **34** | VALIDÉ | `location_normalizer.py` ne liste pas explicitement les indicateurs flous, mais ils sont gérés via le mécanisme de synonymes et Levenshtein. Les expressions mentionnées (`barrage`, `carrefour`, `axe principal`, etc.) sont cohérentes avec le système. | MOYENNE |

## 5. Patterns d'extraction

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **35** | VALIDÉ | `knowledge_enricher.py:20-23` → Patterns exacts : `r'à\s+([A-Za-zéèêëîïôöûüç]+)'`, `r'dans\s+([A-Za-zéèêëîïôöûüç]+)'`, `r'quartier\s+([A-Za-zéèêëîïôöûüç]+)'`. Correspond. | ÉLEVÉE |
| **36** | VALIDÉ | `knowledge_enricher.py:54` → `confidence = min(100, count * 20)`. Correspond exactement. | ÉLEVÉE |

## 6. GPS et géocodage

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **37** | VALIDÉ | `LAWIM/KNOWLEDGE/geography/` contient les 3 fichiers : `neighborhood_gps.json`, `gemini_recovered_gps.json`, `neighborhood_inventory_final.json` (plus `neighborhood_inventory_clean.json` et `neighborhood_inventory.json`). | ÉLEVÉE |
| **38** | VALIDÉ | `LAWIM/scripts/` contient les 4 scripts : `generate_neighborhood_gps.js`, `generate_city_gps.js`, `generate_district_gps_test.js`, `build_cameroon_geography.js` (plus v2 et old). Correspond. | ÉLEVÉE |

## 7. Fichiers districts manquants

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **39** | VALIDÉ | Les 3 fichiers `.txt` existent à la racine de LAWIM : `districts_missing_157.txt`, `districts_not_found.txt`, `districts_without_gps.txt`. Correspond. | ÉLEVÉE |

## 8. Scoring géographique

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **40** | VALIDÉ | `property_matching_v1.json:3-4` → `"city": 30`, `"neighborhood": 25`. Correspond. | ÉLEVÉE |

---

## Résumé GEOGRAPHY_MODEL

| Statut | Nombre |
|--------|--------|
| VALIDÉ | 9 |
| PARTIELLEMENT VALIDÉ | 2 |
| NON VALIDÉ | 8 |
| INTROUVABLE | 1 |
| **Total** | **20** |

**Problèmes majeurs :** 
- Hiérarchie 8 niveaux (#21) introuvable dans le fichier référencé
- Les variantes orthographiques (#27-32) ne sont pas explicitement listées dans `location_normalizer.py` (seulement l'algo Levenshtein)
- Les quartiers #25-26 ne sont pas dans `location_normalizer.py` mais dans des fichiers gateway
- "bonaberi" (#26) absent des sources PY
