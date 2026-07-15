# GEOGRAPHY EXECUTION ARCHITECTURE — Geo Engine LAWIM

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** GEOGRAPHY_MODEL.md, RULE_INDEX.md (GEO-001 to GEO-011), PROXIMITY_SCORING_MODEL.md, GEO_RESOLUTION_CONTRACT.md

---

## 1. Geographic Resolution Pipeline

The Geo Engine consumes raw location strings from user messages through a 7-stage deterministic pipeline:

```
raw_location (string)
    │
    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 1. RAW LOCATION EXTRACTION     (GEO-005)                            │
│    Patterns: à [lieu], dans [lieu], quartier [lieu]                 │
│    Confidence: min(100, occurrences × 20)  (GEO-006)                │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2. NORMALIZATION               (GEO-004)                            │
│    Levenshtein distance ≤ 3                                        │
│    Typo correction, case folding, diacritic normalization           │
│    Fallback: location_synonyms table, typo_database/                │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3. ALIAS RESOLUTION                                                 │
│    City aliases → canonical city_id (CM-YAO, CM-DLA, ...)           │
│    District aliases → canonical district name (aliases.json)        │
│    Social variants, abbreviations (Ydé→Yaoundé, DLA→Douala)         │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 4. CANONICAL IDENTIFICATION    (GEO-001, GEO-002)                   │
│    Resolve to canonical hierarchy path:                             │
│    Pays → Région → Département → Arrondissement → Commune →        │
│    Ville → District → Quartier                                      │
│    Assign canonical_id from cities.json / neighborhoods.json        │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 5. GPS LOOKUP                  (GEO-007)                            │
│    Lookup GPS coordinates from:                                     │
│    - neighborhood_gps.json (Douala, Yaoundé — 5 neighborhoods)      │
│    - gemini_recovered_gps.json                                      │
│    - neighborhood_inventory_final.json                              │
│    Coverage: 239/382 = 62.6%                                        │
│    On miss: infer from parent city GPS, set confidence reduced      │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 6. PROXIMITY SCORING           (GEO-010, GEO-011)                   │
│    Real distance (not straight-line) via road network / Haversine   │
│    Geographic score: city + neighborhood + GPS + real distance      │
│                      + travel time                                  │
│    Mobility context: walking, driving, public transit               │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 7. CONFIDENCE CALCULATION                                           │
│    Composite confidence from:                                       │
│    - Resolution quality (exact/alias/fuzzy/unresolved)              │
│    - GPS accuracy level (HIGH/MEDIUM/LOW/UNKNOWN)                   │
│    - Source reliability (official/recovered/inferred)               │
│    - Ambiguity detection (multiple matches)                         │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.1 Stage Details

#### Stage 1 — Raw Location Extraction (GEO-005, GEO-006)

| Pattern | Regex | Example | Priority |
|---------|-------|---------|----------|
| Direct location | `à\s+([A-Za-zéèêëàâùûüôöîïç\-]+)` | "à Bastos" | High |
| Enclosed location | `dans\s+([A-Za-zéèêëàâùûüôöîïç\-]+)` | "dans Bonamoussadi" | High |
| Explicit neighborhood | `quartier\s+([A-Za-zéèêëàâùûüôöîïç\-]+)` | "quartier Akwa" | Highest |
| Multi-word with modifiers | extended NER (Bigram/Trigram) | "à Bastos Haut" | Medium |

Confidence per extraction (GEO-006):
```
extraction_confidence = min(100, occurrences × 20)
```
After 5 mentions, confidence reaches 100%.

#### Stage 2 — Normalization (GEO-004)

| Operation | Detail |
|-----------|--------|
| **Algorithm** | Levenshtein distance |
| **Maximum threshold** | 3 (GEO-004) |
| **Case folding** | Lowercase normalization |
| **Diacritic normalization** | é→e, è→e, ê→e, ë→e, à→a, â→a, û→u, ù→u, ô→o, ö→o, î→i, ï→i, ç→c |
| **Typo databases** | `typo_database/cities.json`, `typo_database/neighborhoods.json` |
| **Social variant normalization** | `yde`→`Yaoundé`, `dla`→`Douala`, `ub`→`UB City` |
| **Fallback** | `location_synonyms` table (Supabase) |

#### Stage 3 — Alias Resolution

Alias sources and priority:

| Source | Scope | Priority | Confidence Impact |
|--------|-------|----------|-------------------|
| City aliases (`cities.json`) | 10 cities, ~5 variants each | Highest | +0.0 (exact) |
| City typos (`cities.json`) | 10 cities, ~4 typos each | High | −0.05 |
| District aliases (`aliases.json`) | 14 pairs (Douala-focused) | High | −0.05 |
| Social variants (`cities.json`) | 10 cities | Medium | −0.10 |
| Sub-district hierarchy (`aliases.json`) | 4 entries (Buea only) | Medium | −0.10 |

#### Stage 4 — Canonical Identification (GEO-001, GEO-002)

Resolve to canonical hierarchy. The 8-level hierarchy consumed by execution:

| Level | Name | Canonical ID Prefix | Data Populated | Source |
|-------|------|---------------------|----------------|--------|
| 1 | Pays | `CM` | Yes (Cameroon) | GEO-001 |
| 2 | Région | `REG-` | Yes (10 regions) | GEO-001 |
| 3 | Département | `DEP-` | Partial | GEO-001 |
| 4 | Arrondissement | `ARR-` | Partial | GEO-001 |
| 5 | Commune | `COM-` | Partial | GEO-001 |
| 6 | Ville / City | `CM-XXX` | Yes (10 priority + 18 secondary) | GEO-002 |
| 7 | District / Quartier | `QTR-` | Yes (382 total) | GEO-003 |
| 8 | Sous-Quartier | `SUB-` | Minimal (Buea only) | GEO-001 |

**Note:** The source model defines 10 levels (including Landmark and GPS). The execution hierarchy collapses to 8 operational levels since Landmarks (level 9) have zero data and GPS (level 10) is treated as coordinate metadata, not a hierarchy level.

#### Stage 5 — GPS Lookup (GEO-007)

| Source | Records | Cities Covered | Quality |
|--------|---------|----------------|---------|
| `neighborhood_gps.json` | 5 neighborhoods | Douala, Yaoundé | Unknown (no metadata) |
| `gemini_recovered_gps.json` | Recovered | Various | Inferred |
| `neighborhood_inventory_final.json` | Inventory | Various | Unknown |
| `cities.json` (city-level GPS) | 2/10 cities | Yaoundé, Douala | Official |

**Critical gap:** GPS metadata fields (source, confidence level, verification status) are absent from all data files (GE-GAP-001).

Fallback GPS chain:
```
1. neighborhood GPS (exact district)
2. neighborhood centroid (inferred from boundaries)
3. city GPS coordinates (from cities.json)
4. region GPS centroid
5. no GPS → set gps_accuracy = UNKNOWN
```

#### Stage 6 — Proximity Scoring (GEO-010, GEO-011)

See `PROXIMITY_SCORING_MODEL.md` for full specification.

#### Stage 7 — Confidence Calculation

Composite confidence formula:
```
resolution_confidence = base × alias_factor × gps_factor × ambiguity_factor

base = 1.0 (exact match) | 0.85 (alias) | 0.70 (fuzzy/Levenshtein) | 0.0 (unresolved)
alias_factor = 1.0 (verified) | 0.90 (unverified) | 0.80 (typo)
gps_factor = 1.0 (HIGH) | 0.85 (MEDIUM) | 0.60 (LOW) | 0.30 (UNKNOWN)
ambiguity_factor = 1.0 (unique) | 0.50 (multiple matches, resolved)
```

---

## 2. GEO-001 to GEO-011 Rule Consumption

| Rule ID | Component | Consumption |
|---------|-----------|-------------|
| GEO-001 | HierarchyResolver | Defines the 8-level hierarchy. Maps every resolved location to its canonical path. Levels SUBDIVISION and ZONE declared but empty (GG-HIER-001). |
| GEO-002 | CityDetector | 10 priority cities with priority_rank. Used for city validation, lead routing, and stop conditions (QUAL-015). Distinguishes priority (10) from secondary (18). |
| GEO-003 | NeighborhoodResolver | 382 neighborhoods across priority cities. Validates neighborhood against city. Empty district data for all 18 secondary cities — critical gap. |
| GEO-004 | LocationNormalizer | Levenshtein distance ≤ 3. Applied before alias resolution. Fallback to Supabase `location_synonyms` table. |
| GEO-005 | LocationExtractor | Regex patterns `à [lieu]`, `dans [lieu]`, `quartier [lieu]`. Multi-token NER for compound names ("Bastos Haut", "Bonamoussadi Cité"). |
| GEO-006 | ConfidenceCalculator | `min(100, occurrences × 20)`. After 5 mentions → 100% extraction confidence. Applied per-session per-location. |
| GEO-007 | GPSProvider | Coordinates from 3 GPS files. 62.6% coverage (239/382). GPS precision levels defined but not stored in data. |
| GEO-008 | AffinityScorer | City affinity matrix. City exact → Neighborhood exact → Strong affinity → Validation → WAITLISTED. See Section 6. |
| GEO-009 | ProhibitionEnforcer | Geographic prohibitions: Soa→Obala, Soa→Bafia, Yaoundé→Soa, Douala→Dibombari. Prevents matching across prohibited pairs. |
| GEO-010 | RealDistanceCalculator | Actual road distance (Haversine as fallback when road data unavailable). Used in geographic score. Never straight-line. |
| GEO-011 | GeographicScorer | Composite score: city + neighborhood + GPS + real distance + travel time. See Section 7. |

---

## 3. Hierarchy: 8 Operational Levels

The execution hierarchy collapses the 10-level source model to 8 operational levels:

```
Level 1:  Pays          (Cameroon — implicit)
Level 2:  Région        (10 régions)
Level 3:  Département   (partial data)
Level 4:  Arrondissement (partial data)
Level 5:  Commune       (partial data)
Level 6:  Ville         (28 cities: 10 priority + 18 secondary)
Level 7:  Quartier      (382 districts total)
Level 8:  Sous-Quartier (Buea only — 4 entries)
```

**Execution invariant:** Every resolved location MUST produce its full parent chain up to Pays. If any parent level has no data, the chain is truncated at the highest populated level.

**Critical gaps:**
- SUBDIVISION and ZONE levels declared in enums but zero data seeded (GG-HIER-001)
- Sous-Quartier only populated for Buea (GG-SUBZONE-001)
- Levels 3-5 (Département, Arrondissement, Commune) are partial

---

## 4. 10 Priority Cities with Neighborhoods

| Priority | City | ID | Region | GPS | Neighborhoods | GPS Coverage |
|:--------:|------|:--:|--------|:---:|:-------------:|:------------:|
| 1 | Yaoundé | CM-YAO | Centre | 3.848032, 11.502075 | ~111 | Partial |
| 2 | Douala | CM-DLA | Littoral | 4.051056, 9.767868 | ~104 | Partial |
| 3 | Bamenda | CM-BDA | North West | Not stored | 10 | None |
| 4 | Bafoussam | CM-BFS | West | Not stored | 33 | None |
| 5 | Buea | CM-BUE | South West | Not stored | ~51 | None |
| 6 | Kribi | CM-KRI | South | Not stored | 12 | None |
| 7 | Nkongsamba | CM-NKS | Littoral | Not stored | 3 | None |
| 8 | Maroua | CM-MRA | Far North | Not stored | 15 | None |
| 9 | Limbe | CM-LIM | South West | Not stored | ~41 | None |
| 10 | Garoua | CM-GAR | North | Not stored | 6 | None |

**Total neighborhoods:** 382 across all cities.

**Critical gap:** GPS coordinates stored for only 2 of 10 priority cities (Yaoundé, Douala) at city level.

---

## 5. City Affinity Matrix

### 5.1 Affinity Scoring Priority (GEO-008)

```
1. Ville exacte (exact city match)            → maximal score
2. Quartier exact (exact neighborhood match)  → maximal + boost
3. Affinité forte (strong affinity)           → high score
4. Validation (user confirms)                 → proceed
5. WAITLISTED (no match available)            → hold
```

### 5.2 Documented Affinity Pairs

| City | Documented Pairs | Coverage |
|------|:----------------:|:---------|
| Yaoundé | 74 | Full |
| Douala | 51 | Full |
| Bafoussam | 0 | **Empty** |
| Bamenda | 0 | **Empty** |
| Buea | 0 | **Empty** |
| Kribi | 0 | **Empty** |
| Nkongsamba | 0 | **Empty** |
| Maroua | 0 | **Empty** |
| Limbe | 0 | **Empty** |
| Garoua | 0 | **Empty** |

**Critical gap:** Only 2/10 priority cities have seeded affinity data.

### 5.3 Neighborhood Affinity (aliases.json)

| Type | Pairs | Source |
|------|-------|--------|
| Compatible | Bastos Haut ↔ Golf, Santa Barbara, Omnisports Haut Bastos | `aliases.json` |
| Compatible | Soa ↔ Nkoabang, Mbankomo, Mbankomo Proche | `aliases.json` |
| Incompatible | Bastos Haut ↛ Omnisports Popular, Mokolo Marché | `aliases.json` |
| Incompatible | Golf ↛ Omnisports Popular | `aliases.json` |

---

## 6. Geographic Prohibitions (GEO-009)

These are hard exclusion rules. Under no circumstances should a property in the prohibition target be matched to a search in the prohibition source.

| Source | Target | Rationale |
|--------|--------|-----------|
| Soa | Obala | Incompatible zone |
| Soa | Bafia | Incompatible zone |
| Yaoundé | Soa | Different city, low affinity |
| Douala | Dibombari | Different city, low affinity |

**Additional rejection pairs from Geography Model:**
| Source | Target | Rule |
|--------|--------|------|
| Yaoundé | Obala | Incompatible zone |
| Douala | Edéa | Different city, low affinity |
| Buea | Limbe | Different city, low affinity |

### Prohibition enforcement logic

```
match_possible(source, target):
  if prohibition_exists(source, target):
    return FALSE, "GEO-009: Geographic prohibition [source] → [target]"
  if source_city != target_city:
    return FALSE, "GEO-002: Different city, cannot match"
  return TRUE, ""
```

---

## 7. Integration with Other Engines

### 7.1 Understanding Engine

| What | How |
|------|-----|
| Extract raw locations | GEO-005 patterns applied to user message |
| Resolve ambiguities | Multiple matches → request clarification from user |
| Infer missing locations | Context enrichment from session history |

### 7.2 Qualification Engine

| What | How |
|------|-----|
| Validate city coverage | GEO-002: 10 priority cities + 18 secondary |
| Validate neighborhood | GEO-003: neighborhood must belong to detected city |
| Stop condition | City not covered → halt qualification (QUAL-015) |
| Boost scoring | `city_detected` +10, `neighborhood_detected` +10 (QUAL-002) |

### 7.3 Search Engine

| What | How |
|------|-----|
| Filter by city | Exact city match only |
| Filter by neighborhood | Exact or affinity match |
| Budget tolerance | ±20% rent, ±15% buy, ±25% invest (MATCH-003) |

### 7.4 Matching Engine

| What | How |
|------|-----|
| Location scoring | 30% weight in V1 (MATCH-001), 15% in Decision Engine (MATCH-024) |
| Exact neighborhood boost | +25 (MATCH-004) |
| Exact city boost | +20 (MATCH-005) |
| GEO-009 prohibitions | Hard filter — excluded candidates |
| Affinity scoring | Via city affinity matrix |

### 7.5 Pricing Engine

| What | How |
|------|-----|
| Neighborhood-based price ranges | Median price per neighborhood in same city |
| GPS-adjusted valuation | Proximity to amenities, transportation |
| Affinity-based elasticity | Compatible neighborhoods share price bands |

### 7.6 Visits Engine

| What | How |
|------|-----|
| Distance calculation | GEO-010 real distance for travel time estimation |
| Mobility context | Walking, driving, public transit route planning |
| Proximity scoring | Nearby properties (within threshold) eligible for grouped visits |

---

## 8. Location Fuzzy Matching (GEO-004)

| Parameter | Value |
|-----------|-------|
| Algorithm | Levenshtein distance |
| Maximum threshold | 3 |
| Compare target | Canonical names + aliases + typos |
| Case-sensitive | No (lowercased before comparison) |
| Diacritic-sensitive | No (normalized before comparison) |
| Fallback on failure | Supabase `location_synonyms` table |

Implementation notes:
- All reference strings are pre-normalized (lowercase, diacritics removed) for comparison
- If multiple candidates within threshold, select by lowest distance
- If tie, select by priority rank (priority city > secondary city)
- Distance 0 = exact match (highest confidence)
- Distance 1-2 = strong fuzzy match
- Distance 3 = weak fuzzy match (lowest acceptable)

---

## 9. Location Extraction Patterns (GEO-005)

| Pattern | Regex | Example | Capture Group |
|---------|-------|---------|---------------|
| Direct `à` | `/\b[àa]\s+([A-Za-zéèêëàâùûüôöîïç\-]+(?:\s+[A-Za-zéèêëàâùûüôöîïç\-]+){0,2})\b/i` | "à Bonamoussadi" | full name |
| Inside `dans` | `/\bdans\s+(?:le\s+)?([A-Za-zéèêëàâùûüôöîïç\-]+(?:\s+[A-Za-zéèêëàâùûüôöîïç\-]+){0,2})\b/i` | "dans le quartier Akwa" | full name |
| Quartier prefix | `/\bquartier\s+([A-Za-zéèêëàâùûüôöîïç\-]+(?:\s+[A-Za-zéèêëàâùûüôöîïç\-]+){0,2})\b/i` | "quartier Bastos" | full name |
| Cité suffix | `/\b([A-Za-zéèêëàâùûüôöîïç\-]+)\s+(cité|cite)\b/i` | "Bonamoussadi Cité" | base name |
| Ville suffix | `/\b([A-Za-zéèêëàâùûüôöîïç\-]+)\s+(ville|town|city)\b/i` | "Douala Ville" | base name |

Multi-token support: Patterns allow up to 3 tokens (e.g., "Nouvelle zone d'Akwa Nord") by extending capture to `{0,2}` additional words.

---

## 10. GPS Data Sources and Confidence

### 10.1 Source Inventory

| Source | Coverage | Type | Reliability |
|--------|----------|------|-------------|
| `neighborhood_gps.json` | 5 neighborhoods (Douala, Yaoundé) | Lat/Lng pairs | UNKNOWN (no metadata) |
| `gemini_recovered_gps.json` | Recovered coordinates | Lat/Lng pairs | RECOVERED |
| `neighborhood_inventory_final.json` | Inventory coordinates | Lat/Lng pairs | UNKNOWN |
| `cities.json` | 2 cities (Yaoundé, Douala) | City-level GPS | OFFICIAL |

### 10.2 GPS Precision Levels (V4 Standard)

| Level | Description | Threshold | Confidence Factor |
|-------|-------------|:---------:|:-----------------:|
| HIGH | High precision | < 50m | 1.0 |
| MEDIUM | Medium precision | 50-500m | 0.85 |
| LOW | Low precision | > 500m | 0.60 |
| UNKNOWN | No precision data | N/A | 0.30 |

**Critical gap:** GPS metadata fields (source, confidence, verification status) are absent from all data files (GE-GAP-001). Precision levels are defined in V4 standard but never stored alongside coordinates.

### 10.3 GPS Resolution Strategy

```
resolve_gps(neighborhood, city):
  1. Lookup neighborhood in neighborhood_gps.json
     → if found: return coordinates + UNKNOWN precision (no metadata)
  2. Lookup neighborhood in gemini_recovered_gps.json
     → if found: return coordinates + RECOVERED precision
  3. Lookup neighborhood in neighborhood_inventory_final.json
     → if found: return coordinates + UNKNOWN precision
  4. Infer from city GPS (cities.json)
     → if found: return city coordinates + LOW precision
  5. No GPS available
     → return null + UNKNOWN precision + confidence 0.30
```

---

## 11. Mobility Context

| Mode | Speed (km/h) | Used For | Data Source |
|------|:------------:|----------|-------------|
| Walking | 5 | Nearby search (< 2km) | Default |
| Driving | 30 (urban) / 80 (inter-urban) | Standard matching | Road network |
| Public transit | 15 (urban bus) | Alternative commute | Route data (limited) |

Mobility context is selected based on:
- Distance between locations
- Known transport infrastructure
- User preference (if expressed)
- Default = driving (standard matching mode)

---

## 12. Geo Engine Architecture

```
GeoEngine
 ├── LocationExtractor        → GEO-005: Pattern-based extraction
 ├── LocationNormalizer        → GEO-004: Levenshtein ≤ 3, typo correction
 ├── AliasResolver             → City + district aliases from cities.json, aliases.json
 ├── HierarchyResolver         → GEO-001: Canonical path resolution
 ├── GPSProvider               → GEO-007: Coordinate lookup with fallback chain
 ├── ProximityScorer           → GEO-010, GEO-011: Distance + score calculation
 ├── AffinityScorer            → GEO-008: City affinity matrix
 ├── ProhibitionEnforcer       → GEO-009: Hard geographic exclusions
 ├── ConfidenceCalculator      → Composite confidence from all resolution stages
 └── AmbiguityDetector         → Multiple match resolution, clarification requests
```

---

## 13. Error States

| Error | Detection | Action |
|-------|-----------|--------|
| Unresolved location | No match after normalization + alias lookup | Return `unresolved`, confidence=0.0 |
| Ambiguous location | Multiple canonical matches within threshold | Return all candidates, request clarification |
| Uncovered city | City not in priority or secondary list | Return `uncovered`, trigger QUAL-015 stop |
| GPS unavailable | No coordinates after full fallback chain | Return null GPS, set accuracy=UNKNOWN |
| Hierarchy gap | Parent level has no data | Truncate chain at highest populated level |
| Prohibition hit | GEO-009 match | Hard reject, return prohibition reason |

---

*Document Architecture Gold — 2026-07-15 — Référence complète GEO-001 à GEO-011*
