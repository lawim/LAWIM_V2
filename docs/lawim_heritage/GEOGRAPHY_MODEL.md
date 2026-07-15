# GEOGRAPHY MODEL — Modèle géographique LAWIM

**Sources :** LAWIM `KNOWLEDGE/geography/`, `KNOWLEDGE/neighborhoods/`, `KNOWLEDGE/cities/`, LAWIMA `02_KNOWLEDGE/geography/`, `02_KNOWLEDGE/neighborhoods/`, `location_normalizer.py`, LAWIM `Directive/09-GEOLOCATION-REFERENCE.md`
**Principe :** Documentation exhaustive des connaissances géographiques

---

## 1. Hiérarchie territoriale

**Source :** LAWIM `KNOWLEDGE/geography/district_hierarchy.json`

Hiérarchie à 8 niveaux :
1. **Pays** : Cameroun
2. **Région** (10 régions)
3. **Département**
4. **Arrondissement**
5. **Commune**
6. **Ville**
7. **District**
8. **Quartier**

### 1.1 Niveaux intermédiaires supplémentaires identifiés
- **Subdivision** (sous-ensemble de département)
- **Zone** (regroupement de quartiers, propre à LAWIM)

## 2. Villes

### 2.1 Villes officielles LAWIM

**Source :** LAWIM `KNOWLEDGE/cities/cameroon_cities.json`, LAWIMA `02_KNOWLEDGE/cities/cameroon_cities.json`

Liste complète des villes camerounaises dans les fichiers JSON.

### 2.2 Villes prioritaires (10)

**Source :** LAWIMA `06_AI_MODELS/prompts/system_prompt_v1.md`

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

### 2.3 Villes secondaires

**Source :** LAWIMA `02_KNOWLEDGE` (listées dans les données)

Ajoutent aux 10 prioritaires : villes additionnelles listées dans les fichiers de données.

### 2.4 Matrice d'affinité des villes

**Source :** LAWIM `KNOWLEDGE/city-affinity-matrix.md`

Document dédié à la matrice d'affinité entre villes camerounaises (non détaillé ici, voir la source).

## 3. Quartiers

### 3.1 Fichiers par ville

**Source :** LAWIM `KNOWLEDGE/neighborhoods/` (10 fichiers), LAWIMA `02_KNOWLEDGE/neighborhoods/` (11 fichiers)

Fichiers de quartiers disponibles :
- `all_neighborhoods.json` (agrégé)
- `douala.json`
- `yaounde.json`
- `bamenda.json`
- `bafoussam.json`
- `buea.json`
- `garoua.json`
- `kribi.json`
- `limbe.json`
- `maroua.json`
- `nkongsamba.json`

### 3.2 Quartiers documentés (exemples)

**Source :** LAWIMA `03_ENGINE/location_normalizer.py`

**Yaoundé :** bastos, essos, biyem assi, mvog, odza, nkoabang
**Douala :** akwa, bonapriso, bonamoussadi, makepe, deido, bonaberi

Voir les fichiers JSON pour la liste exhaustive par ville.

### 3.3 Types d'informations par quartier

**Source :** LAWIM `KNOWLEDGE/neighborhoods/` (structure des fichiers JSON)

Pour chaque quartier, les données peuvent inclure :
- Nom
- Coordonnées GPS
- Ville parente
- Type (résidentiel, commercial, mixte)
- Prix moyen au m²
- Niveau (standing)

## 4. Zones LAWIM

**Source :** LAWIMA `agents` table (zone field)

Regroupement de quartiers/villes par zone d'activité pour les agents. Les zones sont assignées aux agents pour le routage des leads.

## 5. Alias et normalisation

### 5.1 Alias de districts

**Source :** LAWIM `KNOWLEDGE/geography/district_aliases.json` (v1, v2, v3)

Trois versions d'alias de districts. Chaque entrée associe un nom officiel à ses variantes orthographiques.

### 5.2 Variantes orthographiques (location_normalizer)

**Source :** LAWIMA `03_ENGINE/location_normalizer.py`

Normalisation par distance de Levenshtein (seuil max 3).

**Exemples de variantes documentées :**
- bastos → bastos, basto, bastoss, bastos village
- essos → essos, esos, essoss
- biyem_assi → biyem, biyem-assi, biyemassi, biem assi
- odza → odza, odzaa, odja
- akwa → akwa, aqua, akwah
- bonamoussadi → bonamoussadi, bona moussadi, bonamussadi

### 5.3 Indicateurs de localisation flous

Expressions reconnues indiquant une localisation approximative :
- barrage, carrefour, derrière station
- axe principal, non loin de, axe, non loin

### 5.4 Synonymes de localisation

Stockés dans la table `location_synonyms` (base de connaissances). Correspondance par distance de Levenshtein (max 3) via `knowledge_entries(type="location")`.

## 6. Apprentissage de nouvelles localisations

**Source :** LAWIMA `03_ENGINE/knowledge_enricher.py`

### 6.1 Patterns d'extraction
- `à [lieu]`
- `dans [lieu]`
- `quartier [lieu]`

### 6.2 Calcul de confiance
`Confiance = min(100, occurrences × 20)`

Après 5 mentions, la confiance atteint 100%.

### 6.3 Stockage
Automatique dans `knowledge_entries` (table de connaissances persistante).

## 7. GPS et géocodage

### 7.1 Données GPS disponibles

**Source :** LAWIM `KNOWLEDGE/geography/`

- `neighborhood_gps.json` : Coordonnées GPS des quartiers
- `gemini_recovered_gps.json` : GPS récupéré via IA Gemini
- `neighborhood_inventory_final.json` : Inventaire final des quartiers avec GPS

### 7.2 Scripts de génération GPS

**Source :** LAWIM `scripts/`

- `generate_neighborhood_gps.js`
- `generate_city_gps.js`
- `generate_district_gps_test.js`
- `build_cameroon_geography.js` (v1 et v2)

Ces scripts contiennent les règles et algorithmes de génération de coordonnées GPS.

## 8. Hiérarchie administrative

**Source :** LAWIM `KNOWLEDGE/geography/district_hierarchy.json`

Structure hiérarchique complète : Région → Département → Subdivision → District.

**Fichiers de districts manquants :**
- `districts_missing_157.txt` : 157 districts non couverts
- `districts_not_found.txt` : Districts introuvables
- `districts_without_gps.txt` : Districts sans coordonnées GPS

## 9. Scoring géographique

**Source :** LAWIMA `06_AI_MODELS/matching_engine/property_matching_v1.json`

Pondération géographique dans le matching :
- **City match** : 30% du score total
- **Neighborhood match** : 25% du score total

## 10. Modèle de référence géographique

**Source :** LAWIM `GEO_REFERENCE_MODEL_CAMEROON_V4.md` (document racine)

Document V4 du modèle de référence géographique du Cameroun. Contient le plan d'alignement du modèle de données géographiques.

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
