# Geographic Data Quality Model — Geo Engine LAWIM

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** GEOGRAPHY_MODEL.md, RULE_INDEX.md (GEO-001 to GEO-011), GEOGRAPHY_EXECUTION_ARCHITECTURE.md

---

## 1. GPS Accuracy Levels and Confidence

### 1.1 Precision Level Definitions (V4 Standard — GEO-011)

| Level | Code | Threshold | Confidence Score | Description |
|-------|:----:|:---------:|:----------------:|-------------|
| HIGH | 1 | < 50m | 1.0 | Verified GPS, submeter to building-level accuracy |
| MEDIUM | 2 | 50-500m | 0.85 | Street-level accuracy, sufficient for neighborhood identification |
| LOW | 3 | > 500m | 0.60 | City-level accuracy, insufficient for precise proximity scoring |
| UNKNOWN | 4 | N/A | 0.30 | No precision metadata available |

### 1.2 Current Data Status

**Critical gap:** GPS metadata fields (source, confidence, verification status) are absent from all data files (GE-GAP-001). Precision levels are defined in the V4 standard but never stored alongside coordinates.

| Metric | Value | Impact |
|--------|:-----:|--------|
| Total districts | 382 | — |
| Districts with GPS | 239 (62.6%) | Remaining 143 districts cannot participate in distance-based scoring |
| GPS with precision metadata | **0** | Every GPS coordinate defaults to UNKNOWN confidence (0.30) |
| City-level GPS stored | 2/10 cities | Only Yaoundé and Douala have stored coordinates |

### 1.3 Accuracy Scoring

```
gps_accuracy_score:
  HIGH    = 1.0
  MEDIUM  = 0.85
  LOW     = 0.60
  UNKNOWN = 0.30
  NO_GPS  = 0.0

resolution_gps_factor = gps_accuracy_score × 1.0
```

---

## 2. Source Reliability

### 2.1 Source Classification

| Reliability Tier | Label | Confidence Factor | Sources |
|:----------------:|-------|:-----------------:|---------|
| 1 | OFFICIAL | 1.0 | `cities.json` (city GPS), verified administrative records |
| 2 | VALIDATED | 0.90 | Cross-validated from multiple recovered sources |
| 3 | RECOVERED | 0.75 | `gemini_recovered_gps.json` — single-source recovery |
| 4 | INFERRED | 0.50 | City-centroid approximation, region-level inference |
| 5 | UNKNOWN | 0.30 | No source metadata (current default for all GPS data) |

### 2.2 Source Reliability per Data File

| Data File | Type | Reliability Tier | Confidence Factor | Notes |
|-----------|------|:----------------:|:-----------------:|-------|
| `cities.json` | City GPS | OFFICIAL | 1.0 | City-level coordinates for Yaoundé and Douala only |
| `aliases.json` | District aliases | VALIDATED | 0.90 | 14 pairs, Douala-focused |
| `district_hierarchy.json` | Sub-district map | VALIDATED | 0.90 | 4 entries, Buea only |
| `neighborhood_gps.json` | District GPS | UNKNOWN | 0.30 | 5 neighborhoods, no source/confidence metadata |
| `gemini_recovered_gps.json` | District GPS | RECOVERED | 0.75 | Recovered coordinates, single source |
| `neighborhood_inventory_final.json` | District GPS | UNKNOWN | 0.30 | No source/confidence metadata |
| `cities.json` (aliases) | City aliases | OFFICIAL | 1.0 | 10 cities, verified aliases |
| `cities.json` (typos) | City typos | OFFICIAL | 1.0 | Verified typo patterns |
| `neighborhoods.json` | Neighborhood inventory | VALIDATED | 0.90 | 382 districts, verified counts |

### 2.3 Source Reliability in Confidence Calculation

```
source_reliability_factor:
  OFFICIAL  = 1.0
  VALIDATED = 0.90
  RECOVERED = 0.75
  INFERRED  = 0.50
  UNKNOWN   = 0.30

overall_confidence = resolution_confidence × gps_accuracy × source_reliability
```

---

## 3. Data Freshness Criteria

### 3.1 Freshness Tiers

| Tier | Label | Max Age | Score |
|:----:|-------|:-------:|:-----:|
| 1 | CURRENT | < 30 days | 1.0 |
| 2 | RECENT | 30-90 days | 0.90 |
| 3 | MODERATE | 90-180 days | 0.75 |
| 4 | OLD | 180-365 days | 0.50 |
| 5 | STALE | > 365 days | 0.25 |
| 6 | UNKNOWN | No date | 0.30 |

### 3.2 Data Freshness by Artifact

| Artifact | Version | Date | Freshness Tier | Score |
|----------|:-------:|:----:|:--------------:|:-----:|
| `cities.json` | 3.0 | 2026-07-15 | CURRENT | 1.0 |
| `neighborhoods.json` | 2.0 | 2026-07-15 | CURRENT | 1.0 |
| `aliases.json` | 3.0 | 2026-07-15 | CURRENT | 1.0 |
| `proximity_rules.json` | 1.0 | 2026-07-15 | CURRENT | 1.0 |
| `neighborhood_gps.json` | Unknown | Unknown | UNKNOWN | 0.30 |
| `gemini_recovered_gps.json` | Unknown | Unknown | UNKNOWN | 0.30 |
| `neighborhood_inventory_final.json` | Unknown | Unknown | UNKNOWN | 0.30 |

### 3.3 Freshness Score Calculation

```
freshness_score:
  if data_date is None:  return 0.30  (UNKNOWN)
  age_days = (current_date - data_date).days
  
  if age_days <= 30:     return 1.0
  if age_days <= 90:     return 0.90
  if age_days <= 180:    return 0.75
  if age_days <= 365:    return 0.50
  else:                  return 0.25
```

---

## 4. Coverage Gaps Documentation

### 4.1 Gap Register

| Gap ID | Gap | Affected Assets | Impact |
|--------|-----|----------------|--------|
| GG-GPS-META-001 | GPS metadata (source, confidence, verification) absent | All GPS files | Cannot assess GPS reliability |
| GG-SUBZONE-001 | Neighborhood sub-zones (Bastos Haut, etc.) referenced but not in data | V4 scoring rules | V4 rules reference non-existent data |
| GG-NGAOUNDERE-001 | Ngaoundéré and Bertoua in affinity matrix but zero district data | `city-affinity-matrix.md` | Matching cannot operate on these cities |
| GG-HIER-001 | SUBDIVISION and ZONE levels declared but empty | `GEO_MODEL_ALIGNMENT_PLAN.md` | Cannot route by zone or subdivision |
| GG-LANDMARK-001 | Zero landmarks stored | All geography files | No POI-based matching possible |
| GG-NEARBY-001 | Zero nearby district links | All geography files | Cannot score neighboring districts |
| GG-ALLN-001 | `all_neighborhoods.json` empty | `all_neighborhoods.json` | Aggregated view unavailable |
| GG-CITY-ORDER-001 | 4 different city priority orderings across documents | Cross-document | Inconsistent city ranking |

### 4.2 Coverage Gap — GPS

| City | Total Districts | GPS Coverage | Coverage % | Gap |
|------|:--------------:|:------------:|:----------:|:---:|
| Yaoundé | ~111 | Partial | ~50% | ~55 districts without GPS |
| Douala | ~104 | Partial | ~50% | ~52 districts without GPS |
| Buea | ~51 | Partial | ~50% | ~25 districts without GPS |
| Bafoussam | 33 | **None** | 0% | All 33 districts |
| Limbe | ~41 | **None** | 0% | All 41 districts |
| Kribi | 12 | **None** | 0% | All 12 districts |
| Maroua | 15 | **None** | 0% | All 15 districts |
| Bamenda | 10 | **None** | 0% | All 10 districts |
| Garoua | 6 | **None** | 0% | All 6 districts |
| Nkongsamba | 3 | **None** | 0% | All 3 districts |
| **Total** | **382** | **239** | **62.6%** | **143 without GPS** |

### 4.3 Coverage Gap — Aliases

| Data Type | Count | Coverage | Gap |
|-----------|:-----:|:--------:|:---:|
| City aliases | ~50 | 10/10 cities | None |
| City typos | ~40 | 10/10 cities | None |
| District aliases | 14 pairs | Douala-focused | Zero for Yaoundé, Bafoussam, etc. |
| District hierarchy | 4 entries | Buea only | Zero for all other cities |
| Landmarks | 0 | 0% | **Total gap** |

---

## 5. Alias Quality

### 5.1 Alias Classification

| Quality Tier | Label | Confidence Factor | Criteria |
|:------------:|-------|:-----------------:|----------|
| 1 | VERIFIED | 1.0 | Manually verified, multiple sources confirm |
| 2 | DOCUMENTED | 0.90 | Found in documentation, single source |
| 3 | RECOVERED | 0.75 | Recovered from code analysis or inference |
| 4 | GENERATED | 0.50 | Auto-generated (e.g., deduplication patterns) |
| 5 | UNVERIFIED | 0.30 | Present but no confirmation source |

### 5.2 Alias Quality by Source

| Source | Count | Quality | Confidence Factor |
|--------|:-----:|:-------:|:-----------------:|
| City aliases (`cities.json`) | ~50 | VERIFIED | 1.0 |
| City typos (`cities.json`) | ~40 | DOCUMENTED | 0.90 |
| Social variants (`cities.json`) | ~30 | VERIFIED | 1.0 |
| District aliases (`aliases.json`) | 14 pairs | DOCUMENTED | 0.90 |
| Sub-district hierarchy (`aliases.json`) | 4 entries | DOCUMENTED | 0.90 |
| Neighborhood affinities (`aliases.json`) | 4 pairs | RECOVERED | 0.75 |

### 5.3 Alias Quality Impact

```
alias_quality_factor:
  VERIFIED    = 1.0
  DOCUMENTED  = 0.90
  RECOVERED   = 0.75
  GENERATED   = 0.50
  UNVERIFIED  = 0.30

normalization_factor:
  exact_match (Levenshtein = 0)      = 1.0
  alias_match (verified)             = 0.95
  alias_match (documented)           = 0.85
  alias_match (recovered)            = 0.75
  typo_match                         = 0.70
  fuzzy_match (Levenshtein = 1-3)    = max(0.50, 1.0 − (distance × 0.15))
```

---

## 6. Hierarchy Completeness

### 6.1 Hierarchy Population Status

| Level | Name | Data Status | Population % | Confidence |
|:-----:|------|:-----------:|:------------:|:----------:|
| 1 | Pays | ✅ Complete | 100% | VERY HIGH |
| 2 | Région | ✅ Complete (10/10) | 100% | VERY HIGH |
| 3 | Département | ⚠️ Partial | Unknown | PARTIAL |
| 4 | Arrondissement | ⚠️ Partial | Unknown | PARTIAL |
| 5 | Commune | ⚠️ Partial | Unknown | PARTIAL |
| 6 | Ville | ✅ Complete (28/28) | 100% | VERY HIGH |
| 7 | Quartier | ✅ Complete (382/382) | 100% | VERY HIGH |
| 8 | Sous-Quartier | ❌ Minimal (Buea only) | ~1% | VERY HIGH (confirming gap) |

### 6.2 Completeness Scoring

```
hierarchy_completeness:
  level_1 (Pays):         1.0
  level_2 (Région):       1.0
  level_3 (Département):  0.50  (partial)
  level_4 (Arrondissement): 0.50 (partial)
  level_5 (Commune):       0.50  (partial)
  level_6 (Ville):         1.0
  level_7 (Quartier):      1.0
  level_8 (Sous-Quartier): 0.01  (minimal)

overall_hierarchy_score = average of all levels = (1.0 + 1.0 + 0.5 + 0.5 + 0.5 + 1.0 + 1.0 + 0.01) / 8
                        = 5.51 / 8
                        = 0.689
```

### 6.3 Gap Impact by Level

| Level | Gap | Impact on Execution |
|-------|-----|---------------------|
| Département | Partial | Cannot filter or route by department |
| Arrondissement | Partial | Cannot filter or route by sub-division |
| Commune | Partial | Cannot filter or route by municipality |
| Sous-Quartier | Minimal | Sub-neighborhood precision unavailable for most cities |
| Landmark | Zero | No POI-based location resolution |
| Sub-zone | Zero | V4 sub-zone scoring cannot execute (GG-SUBZONE-001) |

---

## 7. Quality Scoring

### 7.1 Composite Quality Score

```
GeoDataQuality = resolution_confidence × 0.35
               + gps_accuracy × 0.25
               + coverage_score × 0.20
               + freshness_score × 0.10
               + hierarchy_score × 0.10
```

### 7.2 Component Definitions

#### Resolution Confidence
```
resolution_confidence:
  exact_match       = 1.0
  alias_match       = 0.85
  fuzzy_match_d1    = 0.80
  fuzzy_match_d2    = 0.75
  fuzzy_match_d3    = 0.70
  unresolved        = 0.0
```

#### GPS Accuracy
```
gps_accuracy:
  HIGH    = 1.0
  MEDIUM  = 0.85
  LOW     = 0.60
  UNKNOWN = 0.30
  NO_GPS  = 0.0
```

#### Coverage Score
```
coverage_score = districts_with_gps / total_districts = 239 / 382 = 0.626

Per-city coverage score:
  yaounde_coverage   = 0.50
  douala_coverage    = 0.50
  buea_coverage      = 0.50
  other_cities       = 0.0
```

#### Freshness Score
```
freshness_score:
  based on data file version dates (see Section 3)
  current overall: 0.75 (mix of CURRENT and UNKNOWN sources)
```

#### Hierarchy Score
```
hierarchy_score = 0.689 (see Section 6.2)
```

### 7.3 Current Overall Quality

| Component | Value | Weight | Contribution |
|-----------|:-----:|:------:|:------------:|
| resolution_confidence | Best-effort based on match quality | 0.35 | Depends on input |
| gps_accuracy | 0.30 (UNKNOWN — no metadata) | 0.25 | 0.075 |
| coverage_score | 0.626 (239/382) | 0.20 | 0.125 |
| freshness_score | 0.75 (mix CURRENT + UNKNOWN) | 0.10 | 0.075 |
| hierarchy_score | 0.689 | 0.10 | 0.069 |

**Estimated overall quality (at current state):**
```
GeoDataQuality = (1.0 × 0.35) + (0.30 × 0.25) + (0.626 × 0.20) + (0.75 × 0.10) + (0.689 × 0.10)
               = 0.35 + 0.075 + 0.125 + 0.075 + 0.069
               = 0.694
```

### 7.4 Quality Tiers

| Tier | Score Range | Label | Action |
|:----:|:-----------:|-------|--------|
| A | ≥ 0.90 | EXCELLENT | Full confidence, no degradation |
| B | ≥ 0.75 | GOOD | Standard processing |
| C | ≥ 0.50 | FAIR | Flag uncertainties in audit |
| D | ≥ 0.25 | POOR | Degraded mode, escalate gaps |
| F | < 0.25 | CRITICAL | Block processing, alert admin |

Current estimated tier: **C (FAIR)** — `0.694`

---

## 8. Quality Improvement Roadmap

### 8.1 Critical Improvements Needed

| Priority | Improvement | Target Component | Impact on Quality |
|:--------:|-------------|:----------------:|:-----------------:|
| P0 | Add GPS metadata (source, confidence, verification) to all GPS files | gps_accuracy | 0.30 → ~0.80 |
| P0 | Populate GPS for remaining 143 districts | coverage_score | 0.626 → 1.0 |
| P1 | Seed city GPS for remaining 8 priority cities | coverage_score | +0.05 |
| P1 | Add district aliases for all cities (not just Douala) | resolution_confidence | +0.05 |
| P2 | Add nearby district links (GG-NEARBY-001) | resolution_confidence | +0.03 |
| P2 | Seed hierarchy levels 3-5 (Département, Arrondissement, Commune) | hierarchy_score | 0.50 → 1.0 per level |
| P3 | Add landmark/POI data | resolution_confidence | +0.02 |
| P3 | Resolve city priority order discrepancy | — | Consistency |

### 8.2 Target Quality After Improvements

| Component | Current | Target | After Improvement |
|-----------|:-------:|:------:|:-----------------:|
| gps_accuracy | 0.30 | 0.85 | GPS metadata added |
| coverage_score | 0.626 | 1.0 | Full GPS coverage |
| freshness_score | 0.75 | 1.0 | All files dated |
| hierarchy_score | 0.689 | 0.85 | Levels 3-5 seeded |

**Target GeoDataQuality:** `0.88` (Tier B — GOOD, approaching A)

---

*Document Architecture Gold — 2026-07-15*
