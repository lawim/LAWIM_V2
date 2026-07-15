# RAPPORT DE RÉAUDIT GOLD — GÉOGRAPHIE / QUALIFICATION / MATCHING

**Date :** 2026-07-15
**Contexte :** Audit complet des sources LAWIM/LAWIMA (backup 20260608)
**Objectif :** Vérification GOLD de cohérence, complétude et exactitude

---

## TABLE DES MATIÈRES

1. [GÉOGRAPHIE](#1-géographie)
2. [QUALIFICATION](#2-qualification)
3. [MATCHING](#3-matching)
4. [ANOMALIES TRANSVERSES](#4-anomalies-transverses)
5. [RECOMMANDATIONS GOLD](#5-recommandations-gold)

---

## 1. GÉOGRAPHIE

### 1.1 Hiérarchie des 8 niveaux — VÉRIFICATION

**Source :** `GEO_REFERENCE_MODEL_CAMEROON_V4.md` §1.1 + `GEO_MODEL_ALIGNMENT_PLAN.md`

La hiérarchie documentée est de **6 niveaux** (pas 8) :

```
Market → Cluster → Subcluster → Neighborhood → Neighborhood Affinity → GPS
```

Le plan d'alignement (`GEO_MODEL_ALIGNMENT_PLAN.md`) définit un `GeographicLevel` enum avec **7 niveaux** :

```
COUNTRY → REGION → DEPARTMENT → SUBDIVISION → CITY → DISTRICT → ZONE
```

| Problème | Détail |
|----------|--------|
| **Incohérence de comptage** | V4 dit 6 niveaux, Alignment Plan dit 7, nulle part on trouve 8 |
| **Fusion conceptuelle** | Les 2 hiérarchies (métier V4 vs administrative Alignment) ne sont pas alignées |
| **Subdivision/Zone** | Existent dans l'enum `GeographicLevel` (`SUBDIVISION`, `ZONE`) mais n'ont **aucune donnée** seedée |
| **Subdivision manquante** | Absente de tout fichier JSON (district_hierarchy.json, neighborhood_inventory_final.json) |
| **Zone manquante** | Absente de tout fichier JSON |

**Verdict :** ❌ Les niveaux Subdivision et Zone sont déclarés mais vides. La hiérarchie à 8 niveaux est un artefact de documentation ; seuls 6 niveaux métier (V4) ou 5 niveaux administratifs (Alignment) sont réellement renseignés.

---

### 1.2 Niveaux Subdivision/Zone — EXISTENCE RÉELLE

| Niveau | Existe dans code/enum | Existe dans données | Fichier |
|--------|----------------------|-------------------|---------|
| SUBDIVISION | Oui (enum `GeographicLevel`) | Non (0 entrées) | `GEO_MODEL_ALIGNMENT_PLAN.md:54` |
| ZONE | Oui (enum `GeographicLevel`) | Non (0 entrées) | `GEO_MODEL_ALIGNMENT_PLAN.md:55` |
| DISTRICT | Oui | Oui (dans district_hierarchy.json) | `district_hierarchy.json` |
| CITY | Oui | Oui (10 villes prioritaires) | `cameroon_cities.json` |

**Règle extraite GOLD #1 :**
- **ID :** GEO-HIER-001
- **Titre :** Niveaux SUBDIVISION et ZONE non implémentés
- **Description :** Les enums existent dans le plan d'alignement mais aucun seed, migration ou fichier JSON ne peuple ces niveaux. Impossible de faire un matching sur SUBDIVISION ou ZONE.
- **Source :** `GEO_MODEL_ALIGNMENT_PLAN.md` lignes 48-56 (enum GeographicLevel) ; `neighborhood_inventory_final.json` ; `district_hierarchy.json`
- **Confiance :** TRÈS HAUTE

---

### 1.3 Variantes orthographiques — LOCALISATION

**Sources :**
1. `location_normalizer.py` — Utilise Supabase (`location_synonyms` table) + Levenshtein (distance max 3)
2. `district_aliases.json` — 14 paires (Bependa Omnisport→Bepanda Omnisports, etc.)
3. `douala.json` — 12 quartiers avec `aliases` + `typos` par quartier
4. `yaounde.json` — 7 quartiers avec `aliases` + `typos` par quartier
5. `cameroon_cities.json` — 10 villes avec `aliases` + `typos` + `social_variants`

| Source | Nb variantes | Portée |
|--------|-------------|--------|
| location_normalizer.py | Illimité (Supabase) | Dynamique via base de données |
| district_aliases.json | 14 | Douala principalement |
| douala.json | 12 quartiers × ~3 alias/typo | Douala (12 quartiers sur 103 listés) |
| yaounde.json | 7 quartiers × ~3 alias/typo | Yaoundé (7 quartiers sur 102 listés) |
| cameroon_cities.json | 10 villes × ~5 variantes | National |

**Problème :**
- **Couverture partielle :** `douala.json` ne couvre que 12/103 quartiers (~12%). `yaounde.json` couvre 7/102 quartiers (~7%). Les 9 autres villes prioritaires n'ont pas de fichier de quartiers.
- **Dédoublement :** `district_aliases.json` contient des alias aussi présents dans `douala.json` (ex: "Bependa Omnisport" → "Bepanda Omnisports" dans les deux).
- **location_normalizer.py** est le seul à avoir un fallback flou (Levenshtein), mais sa source Supabase (`location_synonyms`) n'est pas dans le backup.

**Règle extraite GOLD #2 :**
- **ID :** GEO-ALIAS-001
- **Titre :** Couverture partielle des variantes orthographiques
- **Description :** Seuls 12/103 quartiers Douala et 7/102 quartiers Yaoundé ont des alias/typos documentés dans les fichiers JSON. Les 9 autres villes prioritaires n'ont aucun fichier quartier avec variantes.
- **Source :** `neighborhoods/douala.json`, `neighborhoods/yaounde.json`, `district_aliases.json`
- **Confiance :** TRÈS HAUTE

**Règle extraite GOLD #3 :**
- **ID :** GEO-ALIAS-002
- **Titre :** Dédoublement des alias entre fichiers
- **Description :** `district_aliases.json` et `douala.json`/`yaounde.json` contiennent des alias redondants (ex: Bependa Omnisport, Messa Administratif, etc.) sans règle de priorité claire.
- **Source :** `district_aliases.json:2-14` vs `douala.json:162-166` (Bepanda)
- **Confiance :** HAUTE

---

### 1.4 Quartier Bonabéri — EXISTENCE

**Oui, Bonabéri existe** dans les données :

| Source | Entrée | Ligne |
|--------|--------|-------|
| `neighborhood_inventory_final.json` | Douala → Bonabéri | Ligne 17 |
| `douala.json` | `"official_name": "Bonaberi"` (quartier structuré avec alias "Beri", typos, landmarks) | Lignes 212-227 |

**Mais attention :** L'orthographe diffère entre les deux fichiers :
- `neighborhood_inventory_final.json` : `Bonabéri` (avec accent)
- `douala.json` : `Bonaberi` (sans accent)

**Règle extraite GOLD #4 :**
- **ID :** GEO-BONABERI-001
- **Titre :** Incohérence orthographique Bonabéri/Bonaberi
- **Description :** Le quartier Bonabéri existe dans les deux inventaires mais avec des accents différents. Aucune règle de normalisation explicite.
- **Source :** `neighborhood_inventory_final.json:17` vs `douala.json:212`
- **Confiance :** HAUTE

---

### 1.5 10 Villes Prioritaires — VÉRIFICATION

**Source `system_prompt_v1.md` lignes 35-44 :**

```
1. Douala
2. Yaoundé
3. Bafoussam
4. Bamenda
5. Buea
6. Limbe
7. Kribi
8. Nkongsamba
9. Garoua
10. Maroua
```

**Source `cameroon_cities.json` :**
Mêmes 10 villes avec `priority_rank` 1-10 dans le même ordre.

**Source `city-affinity-matrix.md` ligne 22 :**
```
Yaoundé, Douala, Bafoussam, Kribi, Limbe, Garoua, Bamenda, Maroua, Ngaoundéré, Bertoua.
```
⚠️ **DIFFÉRENCE :** La matrice d'affinité cite **Ngaoundéré et Bertoua** au lieu de **Nkongsamba et Buea**.

**Règle extraite GOLD #5 :**
- **ID :** GEO-CITY-001
- **Titre :** Incohérence des villes prioritaires entre documents
- **Description :** `city-affinity-matrix.md` liste Ngaoundéré et Bertoua (inclus) mais omet Nkongsamba et Buea (présents dans system_prompt_v1.md et cameroon_cities.json).
- **Source :** `city-affinity-matrix.md:22` vs `system_prompt_v1.md:35-44` vs `cameroon_cities.json`
- **Confiance :** TRÈS HAUTE

---

### 1.6 Fichiers districts manquants — VÉRIFICATION

Trois fichiers `.txt` existent au chemin indiqué (`LAWIM/`) :

| Fichier | Contenu | Lignes |
|---------|---------|--------|
| `districts_missing_157.txt` | 157 quartiers manquants (format `Ville|Quartier`) | 157 |
| `districts_not_found.txt` | 73 quartiers non trouvés (format `[N] Quartier, Ville, Cameroon`) | 73 |
| `districts_without_gps.txt` | 239 quartiers sans GPS (format `Ville => Quartier`) | 239 |

**Analyse :**
- `districts_missing_157.txt` : Ces 157 quartiers existent dans `neighborhood_inventory_final.json` (inventaire final) mais manquent de GPS ou d'autres données.
- `districts_not_found.txt` : Ces 73 quartiers posent problème car ils sont listés comme "not found" mais plusieurs existent dans `neighborhood_inventory_final.json` (ex: "Nouvelle zone d'Akwa Nord", "Bonamouti-Akwa 2", etc.).
- `districts_without_gps.txt` : 239 quartiers sans coordonnées GPS (couvrent toutes les villes).

**Règle extraite GOLD #6 :**
- **ID :** GEO-FILES-001
- **Titre :** districts_not_found.txt contient des quartiers en réalité présents
- **Description :** Au moins 10 quartiers listés comme "not found" existent dans neighborhood_inventory_final.json (ex: Nouvelle zone d'Akwa Nord, Bonamouti-Akwa 2, Plateau Joss, etc.).
- **Source :** `districts_not_found.txt` vs `neighborhood_inventory_final.json`
- **Confiance :** HAUTE

---

### 1.7 GPS — FORMAT ET STRUCTURE

**Source :** `neighborhood_gps.json`

```json
{
  "Douala": {
    "Bonamoussadi": {
      "lat": 4.094354,
      "lng": 9.7393663,
      "radius_km": 2
    },
    ...
  },
  "Yaoundé": {
    "Bastos": { "lat": 3.8940184, "lng": 11.5108818, "radius_km": 2 },
    "Melen": { "lat": 3.8645891, "lng": 11.4963994, "radius_km": 2 }
  }
}
```

**Problèmes :**
- **Couverture :** Seulement **2 villes** (Douala, Yaoundé) et **5 quartiers** (Bonamoussadi, Kotto, Makepe, Bastos, Melen) sur 10 villes × ~400 quartiers.
- **Format :** `lng` au lieu de `lon`/`longitude` — cohérent en interne mais non standard.
- **radius_km** fixe à 2 km pour tous — pas de variation par type de quartier.
- **Aucune source/confiance** associée aux coordonnées (pas de `gps_confidence`).

Comparaison avec les 239 quartiers listés dans `districts_without_gps.txt` :
- 5/239 quartiers ont un GPS (~2%).
- 0 quartier hors Douala/Yaoundé a un GPS.

**Règle extraite GOLD #7 :**
- **ID :** GEO-GPS-001
- **Titre :** Couverture GPS quasi nulle
- **Description :** Seuls 5 quartiers sur ~400 ont des coordonnées GPS. Aucun quartier hors Douala/Yaoundé n'est couvert. Pas de niveau de confiance associé.
- **Source :** `neighborhood_gps.json`, `district_hierarchy.json`, `districts_without_gps.txt`
- **Confiance :** TRÈS HAUTE

---

### 1.8 district_hierarchy.json — ANALYSE

Le fichier contient **5 entrées** seulement (Buea principalement) :

```json
{
  "Muea": ["Lower Muea", "Upper Muea"],
  "Great Soppo": ["Small Soppo-Wonganga", "Small Soppo-Woteke", "Small Soppo-Wovila"],
  "Government Residential Area": ["Federal Quarters", "Clerk's Quarter", "Old-Government Station"],
  "Bolifamba": ["Lower Bolifamba"],
  ...
}
```

**Problème :** Ce fichier ne contient que 5 hiérarchies très locales (Buea). Aucune hiérarchie pour Douala, Yaoundé, ou les 8 autres villes. Le mapping sous-quartier→quartier est quasi inexistant.

**Règle extraite GOLD #8 :**
- **ID :** GEO-HIER-002
- **Titre :** district_hierarchy.json ne couvre que Buea
- **Description :** Sur les 10 villes prioritaires, seule Buea a une hiérarchie district→sous-quartier. Douala, Yaoundé et les autres villes n'ont pas de hiérarchie renseignée.
- **Source :** `district_hierarchy.json` (5 lignes, seulement Buea)
- **Confiance :** TRÈS HAUTE

---

### 1.9 all_neighborhoods.json — ANALYSE

```json
{
  "source": "generated",
  "cities": []
}
```

**Verdict :** ❌ Fichier vide/généré à blanc. Aucune donnée. Inutilisable.

**Règle extraite GOLD #9 :**
- **ID :** GEO-ALLN-001
- **Titre :** all_neighborhoods.json est vide
- **Description :** Le fichier censé contenir tous les quartiers nationalement ne contient qu'un objet vide avec `cities: []`.
- **Source :** `all_neighborhoods.json`
- **Confiance :** TRÈS HAUTE

---

## 2. QUALIFICATION

### 2.1 Scores de base par type d'utilisateur

**Source :** `lead_classifier_v1.json` lignes 2-27

| Type d'utilisateur | Base Score | Intention |
|--------------------|-----------|-----------|
| tenant (locataire) | **40** | RENT_PROPERTY |
| buyer (acheteur) | **60** | BUY_PROPERTY |
| seller (vendeur) | **50** | SELL_PROPERTY |
| investor (investisseur) | **80** | INVESTOR_INTENT |
| diaspora_investor | **95** | INVESTOR_INTENT |

**Règle extraite GOLD #10 :**
- **ID :** QUAL-SCORE-001
- **Titre :** Scores de base V1 par type de lead
- **Description :** Tenant=40, Buyer=60, Seller=50, Investor=80, Diaspora_Investor=95
- **Source :** `lead_classifier_v1.json:2-27`
- **Confiance :** TRÈS HAUTE

### 2.2 Boosters et Pénalités — LOCALISATION RÉELLE

**Source :** `lead_classifier_v1.json` lignes 29-42

**Boosters :**

| Booster | Valeur |
|---------|--------|
| budget_detected | +15 |
| city_detected | +10 |
| neighborhood_detected | +10 |
| urgent_request | +20 |
| diaspora_detected | +25 |
| cash_purchase | +15 |

**Pénalités :**

| Pénalité | Valeur |
|----------|--------|
| missing_budget | -10 |
| unclear_location | -10 |
| spam_like_message | -50 |

**Implémentation :** `lead_scorer.py` lignes 38-63 implémente exactement ces boosters/penalties.

**Règle extraite GOLD #11 :**
- **ID :** QUAL-BOOST-001
- **Titre :** Boosters et pénalités définis dans lead_classifier_v1.json
- **Description :** 6 boosters (+10 à +25) et 3 pénalités (-10 à -50) définis et implémentés dans lead_scorer.py.
- **Source :** `lead_classifier_v1.json:29-42`, `lead_scorer.py:38-63`
- **Confiance :** TRÈS HAUTE

---

### 2.3 Seuils V1 et V5 — COMPARAISON

**Seuils V1 (`lead_classifier_v1.json` lignes 44-46) :**

| Température | Seuil |
|-------------|-------|
| HOT | ≥ 80 |
| WARM | ≥ 60 |
| COLD | ≥ 40 |
| LOW | < 40 |

**Seuils V5 (`RULE_ENGINE_V5.json` lignes 43-48) :**

| Température | Seuil |
|-------------|-------|
| hot | ≥ 0.8 |
| warm | ≥ 0.5 |
| cold | ≥ 0.3 |
| spam_risk | < 0.3 |

**Problème :** Les seuils V1 sont sur 0-100, les seuils V5 sont sur 0-1.0. Les noms diffèrent ("spam_risk" V5 vs "LOW" V1). **Aucune règle de conversion** documentée.

**Règle extraite GOLD #12 :**
- **ID :** QUAL-THRESHOLD-001
- **Titre :** Discontinuité des seuils entre V1 et V5
- **Description :** V1 utilise des seuils entiers 0-100 (HOT≥80, WARM≥60, COLD≥40). V5 utilise 0-1.0 (hot≥0.8, warm≥0.5, cold≥0.3). Aucun mapping de conversion documenté.
- **Source :** `lead_classifier_v1.json:44-46`, `RULE_ENGINE_V5.json:43-48`
- **Confiance :** TRÈS HAUTE

---

### 2.4 Pipeline 8 étapes — VÉRIFICATION

**Source :** `RULE_ENGINE_V5.json` lignes 6-15

| # | Étape | Existe dans code | Notes |
|---|-------|-----------------|-------|
| 1 | incoming_message | Oui (knowledge_builder.py) | `process_message()` |
| 2 | normalize_text | Partiel | `location_normalizer.py` pour adresses |
| 3 | extract_entities | Partiel | `knowledge_builder._extract_info_from_message()` |
| 4 | detect_intent | Partiel | `lead_scorer_supabase.calculate_score()` implicite |
| 5 | context_enrichment | Non | Aucun service dédié |
| 6 | lead_scoring | Oui | `lead_scorer.py`, `lead_scorer_supabase.py` |
| 7 | lead_classification | Oui | `lead_classifier_v1.json` |
| 8 | crm_routing | Non | Aucun service de routage implémenté |

**Verdict :** Seules 5/8 étapes sont réellement implémentées dans le code Python. Les étapes 5 (contexte) et 8 (routage CRM) sont documentées mais non codées.

**Règle extraite GOLD #13 :**
- **ID :** QUAL-PIPE-001
- **Titre :** Pipeline 8 étapes implémenté à 62%
- **Description :** 5/8 étapes documentées dans RULE_ENGINE_V5.json sont codées. Les étapes `context_enrichment` et `crm_routing` sont absentes.
- **Source :** `RULE_ENGINE_V5.json:6-15`, `lead_scorer.py`, `knowledge_builder.py`
- **Confiance :** HAUTE

---

### 2.5 32 Champs Knowledge Builder — VÉRIFICATION

**Source :** `knowledge_builder.py` lignes 24-45

**USER_FIELDS (27 champs) :**
```
name, phone, email, city, country, username, channel,
preferred_budget, preferred_location, preferred_property_type,
preferred_intent, urgency, surface, rooms, bedrooms,
has_parking, has_elevator, is_furnished, is_negotiable,
available_from, proximity_school, proximity_market,
proximity_transport, proximity_hospital, phone_source,
is_contact_complete
```
**Compte : 26 champs** (pas 32)

**PROPERTY_FIELDS (16 champs) :**
```
title, description, price, location, property_type,
status, surface, rooms, bedrooms, bathrooms,
has_parking, has_elevator, is_furnished, is_negotiable,
available_from, images, boost_level, verification_status,
diaspora_ready, quality_score
```
**Compte : 20 champs**

**LEAD_FIELDS (10 champs) :**
```
message, intent, budget, location, property_type,
urgency, score, status, priority, diaspora_flag
```
**Compte : 10 champs**

**Total unique : 26 + 20 + 10 = 56 champs** (mais avec recouvrements entre USER_FIELDS et PROPERTY_FIELDS). Les champs effectivement utilisés dans `_get_complete_user_profile()` sont les **26 USER_FIELDS**.

**Règle extraite GOLD #14 :**
- **ID :** QUAL-KB-001
- **Titre :** 26 champs utilisateur effectifs (au lieu de 32)
- **Description :** knowledge_builder.py définit 26 USER_FIELDS, 20 PROPERTY_FIELDS, 10 LEAD_FIELDS. Le nombre "32" n'est pas vérifié dans le code. 26 champs sont activement utilisés pour le profil utilisateur.
- **Source :** `knowledge_builder.py:24-45`
- **Confiance :** HAUTE

---

### 2.6 4 Comportements Traqués — VÉRIFICATION

**Source :** `RULE_ENGINE_V5.json` lignes 50-55

```json
"behavior_tracking": {
    "message_history": true,
    "response_time_tracking": true,
    "budget_changes_tracking": true,
    "visit_requests_tracking": true
}
```

**Verdict :** Ces 4 flags sont déclarés mais **aucune implémentation** n'existe dans les fichiers Python lus :
- `knowledge_builder.py` ne tracke pas l'historique des messages
- `lead_scorer.py` ne mesure pas le temps de réponse
- `lead_scorer_supabase.py` ne tracke pas les changements de budget
- Aucun fichier ne tracke les demandes de visite

**Règle extraite GOLD #15 :**
- **ID :** QUAL-BEHAV-001
- **Titre :** 4 comportements traqués documentés mais non implémentés
- **Description :** `message_history`, `response_time_tracking`, `budget_changes_tracking`, `visit_requests_tracking` sont déclarés dans RULE_ENGINE_V5 mais aucun code ne les implémente.
- **Source :** `RULE_ENGINE_V5.json:50-55`
- **Confiance :** TRÈS HAUTE

---

### 2.7 Indicateurs Diaspora — VÉRIFICATION

**Source :** `diaspora_filter.py` lignes 17-26

```python
indicators = [
    "france", "paris", "lyon", "etats-unis", "usa", "canada",
    "allemagne", "belgique", "suisse", "uk", "londres",
    "diaspora", "international", "+33", "+1", "+44", "+49"
]
```

**Règle extraite GOLD #16 :**
- **ID :** QUAL-DIASP-001
- **Titre :** 17 indicateurs diaspora exacts
- **Description :** 9 pays, 4 villes, 1 mot-clé général, 4 indicatifs téléphoniques. Détection par `in` (sous-chaîne, pas regex ni NLP).
- **Source :** `diaspora_filter.py:19-21`
- **Confiance :** TRÈS HAUTE

**Problèmes identifiés :**
- Détection par `in` = faux positifs possibles (ex: "paris" dans "parisien", "usa" dans "usage")
- Pas de détection de numéros internationaux autres que +33, +1, +44, +49
- Pas de gestion des pays africains non diaspora (ex: Gabon, Côte d'Ivoire)
- `diaspora_investor` est un type de lead dédié dans `lead_classifier_v1.json` avec score 95

**Règle extraite GOLD #17 :**
- **ID :** QUAL-DIASP-002
- **Titre :** Détection diaspora par sous-chaîne seulement
- **Description :** La méthode `in` operator crée des faux positifs. Aucune regex, aucun pays africain hors diaspora géré.
- **Source :** `diaspora_filter.py:23-25`
- **Confiance :** HAUTE

---

## 3. MATCHING

### 3.1 Dimensions et poids exacts

**Version V1 (JSON) — `property_matching_v1.json` lignes 2-8 :**

| Dimension | Poids |
|-----------|-------|
| city | 30 |
| neighborhood | 25 |
| budget | 25 |
| property_type | 15 |
| title_status | 5 |

**Version V5 (GEO V4) — `GEO_REFERENCE_MODEL_CAMEROON_V4.md` §5.2 :**

| Dimension | Poids |
|-----------|-------|
| Affinity_Score | 0.40 (40%) |
| Cluster_Compatibility | 0.25 (25%) |
| Product_Compatibility | 0.20 (20%) |
| GPS_Adjustment | 0.15 (15%) |

**Version V1 Implementation Report :**

| Dimension | Poids |
|-----------|-------|
| Neighborhood | 40% |
| Cluster | 25% |
| GPS | 15% |
| District | 10% |
| City | 10% |

**Règle extraite GOLD #18 :**
- **ID :** MATCH-WEIGHT-001
- **Titre :** 3 systèmes de poids différents selon la version
- **Description :** V1 JSON (city=30, neighborhood=25, budget=25, type=15, title=5), GEO V4 (affinity=40%, cluster=25%, product=20%, gps=15%), V1 Report (neighborhood=40%, cluster=25%, gps=15%, district=10%, city=10%). Ces 3 systèmes sont incohérents entre eux.
- **Source :** `property_matching_v1.json:2-8`, `GEO_REFERENCE_MODEL_CAMEROON_V4.md:574-581`, `MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md:96-104`
- **Confiance :** TRÈS HAUTE

---

### 3.2 Tolérances budgétaires exactes

**Source :** `property_matching_v1.json` lignes 10-14

| Transaction | Tolérance |
|-------------|-----------|
| rent | 20% (±20%) |
| buy | 15% (±15%) |
| invest | 25% (±25%) |

**Règle extraite GOLD #19 :**
- **ID :** MATCH-BUDGET-001
- **Titre :** Tolérances budgétaires V1
- **Description :** Rent ±20%, Buy ±15%, Invest ±25%. Ces valeurs ne sont utilisées que par la config JSON ; l'implémentation V5 (property_matcher_v5.py) utilise des seuils absolus (diff=0→+50, diff<10%→+35, diff<30%→+20) et non des pourcentages par type.
- **Source :** `property_matching_v1.json:10-14`
- **Confiance :** TRÈS HAUTE

---

### 3.3 Boosts et règles de priorité exacts

**Source :** `property_matching_v1.json` lignes 16-41

| Règle | Boost |
|-------|-------|
| exact_neighborhood_match | +25 |
| exact_city_match | +20 |
| budget_within_range | +15 |
| title_foncier | +10 |
| diaspora_investor | +20 |

**Règle extraite GOLD #20 :**
- **ID :** MATCH-BOOST-001
- **Titre :** 5 boosts de priorité V1
- **Description :** exact_neighborhood_match +25, exact_city_match +20, budget_within_range +15, title_foncier +10, diaspora_investor +20.
- **Source :** `property_matching_v1.json:16-41`
- **Confiance :** TRÈS HAUTE

---

### 3.4 Scoring étoiles — ALGORITHME EXACT

**Source :** `property_matcher_v5.py` lignes 30-39

```python
def score_to_stars(self, score):
    if score >= 80: return "⭐⭐⭐⭐⭐ (5/5)"
    elif score >= 60: return "⭐⭐⭐⭐ (4/5)"
    elif score >= 40: return "⭐⭐⭐ (3/5)"
    elif score >= 20: return "⭐⭐ (2/5)"
    else: return "⭐ (1/5)"
```

**Règle extraite GOLD #21 :**
- **ID :** MATCH-STARS-001
- **Titre :** Scoring étoiles V5 avec seuils 80/60/40/20
- **Description :** 5 étoiles ≥80, 4 étoiles ≥60, 3 étoiles ≥40, 2 étoiles ≥20, 1 étoile <20.
- **Source :** `property_matcher_v5.py:30-39`
- **Confiance :** TRÈS HAUTE

---

### 3.5 Algorithme V4 vs V5 — DIFFÉRENCES

**V4 (`property_matcher_supabase.py`) :**

| Critère | Points | Note |
|---------|--------|------|
| Location match (city in location) | +40 | |
| Budget exact (diff=0) | +50 | |
| Budget < 10% | +35 | |
| Budget < 30% | +20 | |
| Property type in message | +25 | |

**V5 (`property_matcher_v5.py`) :**

| Critère | Points | Note |
|---------|--------|------|
| Location match (city in location) | +40 | Identique V4 |
| Budget exact (diff=0) | +50 | Identique V4 |
| Budget < 10% | +35 | Identique V4 |
| Budget < 30% | +20 | Identique V4 |
| Budget < 50% | +10 | **Nouveau V5** |
| Property type in message | +10 | **V5: 10 vs V4: 25** |

**Différences clés :**
1. V5 ajoute un pallier budget < 50% (+10)
2. V5 réduit le poids du property_type match (25→10)
3. V5 ajoute le scoring étoiles (1-5)
4. V5 limite à 5 résultats vs V4 à 5 aussi (identique)
5. V5 et V4 tous deux plafonnent à 100 (`min(score, 100)`)

**Règle extraite GOLD #22 :**
- **ID :** MATCH-ALGO-001
- **Titre :** Évolution V4→V5 : nouveau pallier budget et réduction poids type
- **Description :** V5 ajoute un pallier budget <50% (+10) et réduit le poids du property_type de 25 à 10.
- **Source :** `property_matcher_supabase.py:50-71` vs `property_matcher_v5.py:48-72`
- **Confiance :** TRÈS HAUTE

---

### 3.6 Minimum Match Score

**Sources :**

| Source | Seuil | Contexte |
|--------|-------|----------|
| `property_matching_v1.json:43` | **60** | minimum_match_score (V1) |
| `MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md:53` | **60** | Lead generation threshold |
| `MATCHING_ENGINE_V1_SUMMARY.md:106` | **60** | Lead eligible threshold |
| `GEO_REFERENCE_MODEL_CAMEROON_V4.md:903` | **40-60** | Proposition secondaire (règle 6) |

**Règle extraite GOLD #23 :**
- **ID :** MATCH-MIN-001
- **Titre :** Seuil minimum de match à 60
- **Description :** Le seuil de match minimum est 60/100. En dessous, pas de lead généré. Score 40-60 = proposition alternative possible sans lead.
- **Source :** `property_matching_v1.json:43`, `MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md:53`, `MATCHING_ENGINE_V1_SUMMARY.md:106`
- **Confiance :** TRÈS HAUTE

---

### 3.7 Affinités détaillées V4 (GEO_REFERENCE_MODEL)

La matrice d'affinité dans `GEO_REFERENCE_MODEL_CAMEROON_V4.md` §6 contient :

**Yaoundé :** 74 paires documentées (lignes 636-723)
**Douala :** 51 paires documentées (lignes 739-819)
**Autres villes :** Aucune paire seedée (juste des instructions ligne 825-832)

**Règle extraite GOLD #24 :**
- **ID :** MATCH-AFF-001
- **Titre :** Matrice d'affinité : 125 paires Yaoundé/Douala, 0 pour les autres villes
- **Description :** 74 paires Yaoundé + 51 paires Douala documentées. Bafoussam, Bamenda, Buea, Limbe, Kribi, Garoua, Maroua, Ngaoundéré, Bertoua : instructions mais 0 paires seedées.
- **Source :** `GEO_REFERENCE_MODEL_CAMEROON_V4.md:636-723` (Yaoundé), `739-819` (Douala), `825-832` (autres villes)
- **Confiance :** TRÈS HAUTE

---

### 3.8 Règles de rejet — INVENTAIRE COMPLET

**Source :** `GEO_REFERENCE_MODEL_CAMEROON_V4.md` §7

| # | Règle | Severité | Score | Référence |
|---|-------|----------|-------|-----------|
| R1 | Incompatibilité de ville indépendante | AUTOMATIC | 0 | Lignes 840-855 |
| R2 | Incompatibilité de produit absolue | AUTOMATIC | 0 | Lignes 859-866 |
| R3 | Incompatibilité de standing extrême | AUTOMATIC | 0 | Lignes 870-875 |
| R4 | Distance extrême + affinité faible | WEAK | 20 | Lignes 881-886 |
| R5 | Quartier commercial pour résidentiel | WEAK | 30 | Lignes 890-895 |
| R6 | Cluster différent mais compatible | MEDIUM | 40-60 | Lignes 900-905 |

**Règle extraite GOLD #25 :**
- **ID :** MATCH-REJECT-001
- **Titre :** 6 règles de rejet documentées dans GEO V4
- **Description :** 3 rejets automatiques (score=0), 2 rejets faibles (score 20-30), 1 rejet moyen (score 40-60).
- **Source :** `GEO_REFERENCE_MODEL_CAMEROON_V4.md:835-905`
- **Confiance :** TRÈS HAUTE

---

## 4. ANOMALIES TRANSVERSES

### 4.1 Multiples versions de scoring non alignées

| Document | Dimensions | Pondération | Type de score |
|----------|-----------|-------------|---------------|
| property_matching_v1.json | 5 (city, neighborhood, budget, type, title) | Additif (30+25+25+15+5) | 0-100 |
| GEO V4 §5.2 | 4 (affinity, cluster, product, gps) | Pondéré (40+25+20+15) | 0-100 |
| Implémentation Report | 5 (neighborhood, cluster, gps, district, city) | Pondéré (40+25+15+10+10) | 0-100 |
| property_matcher_v5.py | 3 (location, budget, type) | Additif (40+50+10) | 0-100 (plafonné) |

**Aucun alignement entre ces 4 systèmes.**

### 4.2 Écart entre documentation et code

| Concept | Documenté | Implémenté | Écart |
|---------|-----------|------------|-------|
| Pipeline 8 étapes | `RULE_ENGINE_V5.json` | 5/8 | 3 étapes manquantes |
| 4 comportements traqués | `RULE_ENGINE_V5.json:50-55` | 0/4 | Aucun tracking codé |
| GPS Confidence Model | `GEO V4 §4` | Aucun | Pas de `gps_confidence` en données |
| Neighborhood Segments | `GEO V4 §2` | Aucun | Omnisports non segmenté en données |
| SUBDIVISION/ZONE | `GEO_MODEL_ALIGNMENT_PLAN.md` | 0 entrées | Enum sans données |
| 32 champs KB | Documentation orale | 26 | 6 champs manquants |

### 4.3 Fichiers orphelins ou vides

| Fichier | Problème |
|---------|----------|
| `all_neighborhoods.json` | Vide (`"cities": []`) |
| `district_hierarchy.json` | Seulement Buea (5 hiérarchies) |
| `neighborhood_gps.json` | Seulement 5 quartiers sur 400+ |
| `location_normalizer.py` | Dépend de Supabase — pas de fallback local |

---

## 5. RECOMMANDATIONS GOLD

### Priorité Haute (bloquant pour le matching)

1. **GEO-HIER-001** : Implémenter une migration Prisma pour les 8 niveaux hiérarchiques avec données seedées
2. **MATCH-WEIGHT-001** : Choisir UN système de pondération et l'appliquer uniformément (recommandé : GEO V4 §5.2)
3. **GEO-GPS-001** : Étendre la couverture GPS à toutes les villes prioritaires (minimum 5 quartiers/ville)
4. **MATCH-AFF-001** : Seed la matrice d'affinité pour les 8 villes non couvertes

### Priorité Moyenne

5. **GEO-ALIAS-001** : Compléter les alias pour tous les quartiers des 10 villes (actuellement ~10% couvert)
6. **QUAL-PIPE-001** : Implémenter les 3 étapes manquantes du pipeline (context_enrichment, crm_routing)
7. **QUAL-BEHAV-001** : Coder les 4 trackers de comportement déclarés
8. **GEO-CITY-001** : Aligner `city-affinity-matrix.md` avec `system_prompt_v1.md` et `cameroon_cities.json`
9. **MATCH-REJECT-001** : Coder les 6 règles de rejet dans le Matching Engine (actuellement 0 implémentées)

### Priorité Faible

10. **GEO-BONABERI-001** : Uniformiser l'orthographe Bonabéri/Bonaberi
11. **GEO-ALLN-001** : Peupler ou supprimer `all_neighborhoods.json`
12. **QUAL-THRESHOLD-001** : Documenter la règle de conversion V1→V5 des seuils
13. **QUAL-DIASP-002** : Améliorer la détection diaspora (regex, pays africains)
14. **GEO-HIER-002** : Étendre `district_hierarchy.json` aux 10 villes

---

## ANNEXE A : INDEX DES RÈGLES EXTRAITES

| # | ID | Titre | Confiance |
|---|-----|-------|-----------|
| 1 | GEO-HIER-001 | Niveaux SUBDIVISION et ZONE non implémentés | TRÈS HAUTE |
| 2 | GEO-ALIAS-001 | Couverture partielle des variantes orthographiques | TRÈS HAUTE |
| 3 | GEO-ALIAS-002 | Dédoublement des alias entre fichiers | HAUTE |
| 4 | GEO-BONABERI-001 | Incohérence orthographique Bonabéri/Bonaberi | HAUTE |
| 5 | GEO-CITY-001 | Incohérence des villes prioritaires entre documents | TRÈS HAUTE |
| 6 | GEO-FILES-001 | districts_not_found.txt contient des quartiers présents | HAUTE |
| 7 | GEO-GPS-001 | Couverture GPS quasi nulle | TRÈS HAUTE |
| 8 | GEO-HIER-002 | district_hierarchy.json ne couvre que Buea | TRÈS HAUTE |
| 9 | GEO-ALLN-001 | all_neighborhoods.json est vide | TRÈS HAUTE |
| 10 | QUAL-SCORE-001 | Scores de base V1 par type de lead | TRÈS HAUTE |
| 11 | QUAL-BOOST-001 | Boosters et pénalités V1 | TRÈS HAUTE |
| 12 | QUAL-THRESHOLD-001 | Discontinuité des seuils V1→V5 | TRÈS HAUTE |
| 13 | QUAL-PIPE-001 | Pipeline 8 étapes implémenté à 62% | HAUTE |
| 14 | QUAL-KB-001 | 26 champs utilisateur effectifs (vs 32) | HAUTE |
| 15 | QUAL-BEHAV-001 | 4 comportements traqués non implémentés | TRÈS HAUTE |
| 16 | QUAL-DIASP-001 | 17 indicateurs diaspora exacts | TRÈS HAUTE |
| 17 | QUAL-DIASP-002 | Détection diaspora par sous-chaîne seulement | HAUTE |
| 18 | MATCH-WEIGHT-001 | 3 systèmes de poids différents | TRÈS HAUTE |
| 19 | MATCH-BUDGET-001 | Tolérances budgétaires V1 | TRÈS HAUTE |
| 20 | MATCH-BOOST-001 | 5 boosts de priorité V1 | TRÈS HAUTE |
| 21 | MATCH-STARS-001 | Scoring étoiles V5 avec seuils 80/60/40/20 | TRÈS HAUTE |
| 22 | MATCH-ALGO-001 | Évolution V4→V5 | TRÈS HAUTE |
| 23 | MATCH-MIN-001 | Seuil minimum de match à 60 | TRÈS HAUTE |
| 24 | MATCH-AFF-001 | Matrice d'affinité : 125 paires sur 10 villes | TRÈS HAUTE |
| 25 | MATCH-REJECT-001 | 6 règles de rejet documentées | TRÈS HAUTE |

## ANNEXE B : FICHIERS AUDITÉS (25)

| Fichier | Taille | Status |
|---------|--------|--------|
| LAWIM/KNOWLEDGE/geography/district_hierarchy.json | 6 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/geography/district_aliases.json | 15 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/geography/neighborhood_gps.json | 31 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/geography/neighborhood_inventory_final.json | 401 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/neighborhoods/all_neighborhoods.json | 4 lignes | ✅ Lu (vide) |
| LAWIM/KNOWLEDGE/neighborhoods/douala.json | 294 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/neighborhoods/yaounde.json | 296 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/cities/cameroon_cities.json | 237 lignes | ✅ Lu |
| LAWIMA/03_ENGINE/location_normalizer.py | 57 lignes | ✅ Lu |
| LAWIMA/06_AI_MODELS/prompts/system_prompt_v1.md | 73 lignes | ✅ Lu |
| LAWIMA/06_AI_MODELS/matching_engine/property_matching_v1.json | 46 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/city-affinity-matrix.md | 38 lignes | ✅ Lu |
| LAWIM/GEO_REFERENCE_MODEL_CAMEROON_V4.md | 1246 lignes | ✅ Lu |
| LAWIM/GEO_MODEL_ALIGNMENT_PLAN.md | 872 lignes | ✅ Lu |
| LAWIM/districts_missing_157.txt | 157 lignes | ✅ Lu |
| LAWIM/districts_not_found.txt | 73 lignes | ✅ Lu |
| LAWIM/districts_without_gps.txt | 239 lignes | ✅ Lu |
| LAWIMA/06_AI_MODELS/lead_classifier/lead_classifier_v1.json | 47 lignes | ✅ Lu |
| LAWIMA/03_ENGINE/lead_scorer/lead_scorer.py | 95 lignes | ✅ Lu |
| LAWIMA/03_ENGINE/lead_scorer/lead_scorer_supabase.py | 83 lignes | ✅ Lu |
| LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V5.json | 89 lignes | ✅ Lu |
| LAWIMA/03_ENGINE/diaspora_filter.py | 45 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/conversation-qualification-questions.md | 199 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/minimum-fields-request.md | 296 lignes | ✅ Lu |
| LAWIM/KNOWLEDGE/minimum-fields-property.md | 195 lignes | ✅ Lu |
| LAWIMA/03_ENGINE/knowledge_builder.py | 225 lignes | ✅ Lu |
| LAWIMA/03_ENGINE/property_matcher/property_matcher_v5.py | 93 lignes | ✅ Lu |
| LAWIMA/03_ENGINE/property_matcher/property_matcher_supabase.py | 92 lignes | ✅ Lu |
| LAWIM/MATCHING_ENGINE_IMPLEMENTATION_ROADMAP.md | 118 lignes | ✅ Lu |
| LAWIM/MATCHING_ENGINE_PHASE0_ARCHITECTURE.md | 1430 lignes | ✅ Lu |
| LAWIM/MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md | 464 lignes | ✅ Lu |
| LAWIM/MATCHING_ENGINE_V1_SUMMARY.md | 225 lignes | ✅ Lu |
