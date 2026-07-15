# Proximity Scoring Model — Geo Engine LAWIM

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** GEOGRAPHY_MODEL.md, RULE_INDEX.md (GEO-008, GEO-010, GEO-011), proximity_rules.json

---

## 1. Distance Calculation Rules (GEO-010)

**Rule GEO-010:** Distance must be calculated as real (road) distance, never as straight-line (as-the-crow-flies) distance.

### 1.1 Priority of Distance Methods

```
Method 1: ROAD DISTANCE (primary)
  - Real driving distance via road network
  - Source: OpenStreetMap / routing engine
  - Used when: road data available for both locations

Method 2: HAVERSINE DISTANCE (fallback)
  - Great-circle distance between GPS coordinates
  - Formula: d = 2 × R × arcsin(√(sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)))
  - R = 6371 km (Earth's radius)
  - Used when: road data unavailable, GPS coordinates present

Method 3: CITY-CENTROID DISTANCE (degraded)
  - Distance between city centers
  - Used when: no district-level GPS available

Method 4: AFFINITY-BASED DISTANCE (minimum)
  - No GPS available at all
  - Distance inferred from affinity matrix (compatible = near, incompatible = far)
```

### 1.2 Haversine Formula (Fallback)

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × atan2(√a, √(1-a))
d = R × c

Where:
  R  = 6371 km
  lat1, lon1 = origin GPS (radians)
  lat2, lon2 = destination GPS (radians)
  Δlat = lat2 - lat1
  Δlon = lon2 - lon1
```

### 1.3 Distance Labels

| Distance Range | Label | Score Factor | Legal/Factual Note |
|:--------------:|-------|:------------:|--------------------|
| < 1 km | Immediate vicinity | 1.0 | — |
| 1-3 km | Nearby | 0.85 | — |
| 3-5 km | Short distance | 0.70 | — |
| 5-10 km | Moderate distance | 0.50 | — |
| 10-20 km | Long distance | 0.30 | Yaoundé↛Soa prohibition applies at ~12km |
| 20-50 km | Distant | 0.15 | Douala↛Dibombari prohibition (~30km) |
| > 50 km | Very distant | 0.05 | Different city, GEO-002 blocks matching |

---

## 2. Geographic Score Formula (GEO-011)

### 2.1 V4 Formula (Reference)

```
Geo_Score = (Affinity × 0.40) + (Cluster × 0.25) + (Product × 0.20) + (GPS × 0.15)
```

**Note:** The `Cluster` and `Product` components are cross-domain (not purely geographic). The GEO engine computes the geographic sub-score; the full Geo_Score is computed by the Matching Engine.

### 2.2 Geographic Sub-Score (GEO Engine)

The Geo Engine computes a geographic-only score for proximity assessment:

```
Geographic_Score = (city_score × 0.30) + (neighborhood_score × 0.25)
                 + (gps_proximity × 0.20) + (real_distance_score × 0.15)
                 + (travel_time_score × 0.10)
```

Where:

| Component | Weight | Calculation |
|-----------|:------:|-------------|
| `city_score` | 30% | Same city = 100, same region diff city = 50, different region = 0 |
| `neighborhood_score` | 25% | Exact = 100, compatible = 75, same city diff neighborhood = 50, incompatible = 0 |
| `gps_proximity` | 20% | Normalized proximity: `max(0, 100 − (distance_km × 10))` |
| `real_distance_score` | 15% | See Section 1.3 — distance label factor × 100 |
| `travel_time_score` | 10% | < 15 min = 100, 15-30 min = 75, 30-60 min = 50, > 60 min = 25 |

### 2.3 Example: Yaoundé Bastos → Golf

```
city_score:        100  (same city: Yaoundé)
neighborhood_score: 75  (compatible: Bastos ↔ Golf per aliases.json)
gps_proximity:      88  (distance 1.2 km: max(0, 100 − 1.2 × 10))
real_distance_score: 85  (1.2 km → "Nearby" → 0.85)
travel_time_score:  100 (< 15 min driving)

Geographic_Score = (100 × 0.30) + (75 × 0.25) + (88 × 0.20) + (85 × 0.15) + (100 × 0.10)
                 = 30.0 + 18.75 + 17.6 + 12.75 + 10.0
                 = 89.1
```

### 2.4 Example: Douala Bonanjo → Akwa

```
city_score:        100  (same city: Douala)
neighborhood_score: 50  (different neighborhood, no incompatibility)
gps_proximity:      70  (distance ~3 km)
real_distance_score: 70  ("Short distance" → 0.70)
travel_time_score:  75  (15-30 min driving)

Geographic_Score = (100 × 0.30) + (50 × 0.25) + (70 × 0.20) + (70 × 0.15) + (75 × 0.10)
                 = 30.0 + 12.5 + 14.0 + 10.5 + 7.5
                 = 74.5
```

### 2.5 Geographic Scoring Levels (proximity_rules.json)

| Level | Label | Score Range | Description |
|:-----:|-------|:-----------:|-------------|
| 1 | Exact neighborhood | 90-100 | Property in exact requested neighborhood |
| 2 | Accepted alternative | 75-89 | Property in explicitly accepted alternative |
| 3 | Neighboring district | 50-74 | Property in neighboring district, same city |
| 4 | Same city distant | 25-49 | Same city but far from requested zone |
| 5 | Incompatible zone | 0-24 | Incompatible zone (GEO-009 prohibition or low affinity) |

---

## 3. City Affinity Matrix Consumption

### 3.1 Affinity Scoring

The Geo Engine consumes the city affinity matrix to determine compatibility between cities and neighborhoods.

| Affinity Level | Score | Condition |
|----------------|:-----:|-----------|
| Exact same city | 100 | `city_a == city_b` |
| Strong affinity | 85 | Documented compatible pair |
| Same region | 60 | Different city, same region |
| Low affinity | 30 | Different city, same country |
| Prohibited | 0 | GEO-009 prohibition pair |

### 3.2 Documented Affinities (from aliases.json)

| Source | Compatible Targets | Score |
|--------|-------------------|:-----:|
| Bastos Haut (Yaoundé) | Golf, Santa Barbara, Omnisports Haut Bastos | 85 |
| Soa | Nkoabang, Mbankomo, Mbankomo Proche | 85 |

| Source | Incompatible Targets | Score |
|--------|---------------------|:-----:|
| Bastos Haut (Yaoundé) | Omnisports Popular, Mokolo Marché | 0 |
| Golf (Yaoundé) | Omnisports Popular | 0 |

### 3.3 Consumption Rules

```
affinity_score(source, target):
  if source.city != target.city:
    return 0  (GEO-002: different city prohibition)
  
  if prohibition_exists(source, target):
    return 0  (GEO-009: hard prohibition)
  
  if source.neighborhood == target.neighborhood:
    return 100  (exact match)
  
  if compatible(source.neighborhood, target.neighborhood):
    return 85  (strong affinity)
  
  if incompatible(source.neighborhood, target.neighborhood):
    return 0  (incompatible)
  
  return 50  (same city, different neighborhood, no documented affinity)
```

---

## 4. Nearby Location Determination

### 4.1 Definition

A location is "nearby" if it meets ALL of:
1. Same city (GEO-002 compliance)
2. Real distance ≤ 5 km (GEO-010)
3. Not a prohibition pair (GEO-009 clearance)
4. Mobility-context feasible (walkable ≤ 2 km, drivable ≤ 5 km)

### 4.2 Nearby Location Scoring

| Distance | Score | Classification |
|:--------:|:-----:|:--------------|
| < 0.5 km | 100 | Immediate walking |
| 0.5-1 km | 90 | Walking distance |
| 1-2 km | 80 | Short walk/drive |
| 2-3 km | 70 | Short drive |
| 3-5 km | 60 | Moderate drive |
| > 5 km | 0 | Not nearby |

### 4.3 Example: Yaoundé Bastos Nearby Locations

| Location | Distance | Affinity | Score |
|----------|:--------:|:--------:|:-----:|
| Omnisports Haut Bastos | 0.8 km | Compatible | 90 |
| Golf | 1.2 km | Compatible | 80 |
| Santa Barbara | 1.8 km | Compatible | 80 |
| Messa | 2.5 km | None documented | 70 |
| Centre | 3.5 km | None documented | 60 |

---

## 5. Mobility Context

### 5.1 Mode Selection

| Mode | Speed | Max Distance | When Used |
|------|:-----:|:------------:|-----------|
| Walking | 5 km/h | ≤ 2 km | Nearby search, short distances |
| Driving | 30 km/h urban | ≤ 50 km | Standard matching |
| Public transit | 15 km/h | ≤ 30 km | Alternative commute, large cities |

### 5.2 Travel Time Calculation

```
travel_time_min = distance_km / speed_kph × 60
```

| Mode | 1 km | 3 km | 5 km | 10 km |
|:-----|:----:|:----:|:----:|:-----:|
| Walking | 12 min | 36 min | 60 min | — |
| Driving | 2 min | 6 min | 10 min | 20 min |
| Transit | 4 min | 12 min | 20 min | 40 min |

### 5.3 Travel Time Score (GEO-011 Component)

| Travel Time | Score |
|:-----------:|:-----:|
| < 15 min | 100 |
| 15-30 min | 75 |
| 30-60 min | 50 |
| > 60 min | 25 |

---

## 6. Proximity Thresholds by Context

### 6.1 Search Context

| Parameter | Value | Rationale |
|-----------|:-----:|-----------|
| Max distance (same neighborhood) | All properties in neighborhood | GEO-003: neighborhood inventory |
| Max distance (same city) | City boundary | GEO-002: same city only |
| Max distance (different city) | Prohibited | GEO-002 rule |
| Max results | 10 | MATCH-010 |

### 6.2 Visit Context

| Parameter | Value | Rationale |
|-----------|:-----:|-----------|
| Max walking distance (grouped visits) | 1 km | Practical walk between viewings |
| Max driving distance (grouped visits) | 5 km | Practical drive between viewings |
| Min travel time between visits | 15 min | Allow preparation/transition |

### 6.3 Neighborhood Context

| Parameter | Value | Rationale |
|-----------|:-----:|-----------|
| Nearby radius | ≤ 3 km | GEO-010: real distance |
| Walking radius | ≤ 2 km | Walking mobility mode |
| Compatible radius | ≤ 5 km | Maximum for neighborhood affinity |
| Different city | 0 km | Not allowed (GEO-002) |

---

## 7. Mobility Mode Priority (proximity_rules.json)

| Mode | Behavior | Used When |
|------|----------|-----------|
| STRICT | Requested neighborhood only | User specified exact neighborhood |
| FLEXIBLE | Alternative neighborhoods accepted | User open to suggestions |
| VERY_FLEXIBLE | Expanded zone (nearby + compatible) | User wants all options |

### Mobility score adjustment

```
STRICT:     score = geographic_score (unmodified)
FLEXIBLE:   score = geographic_score × 0.95 (slight reduction for alternatives)
VERY_FLEXIBLE: score = geographic_score × 0.85 (reduced for expanded zone)
```

---

## 8. Examples: Douala and Yaoundé Neighborhoods

### 8.1 Douala: Bonanjo as Reference

| Target Neighborhood | Distance (km) | Real Distance | Affinity | Geographic Score | Classification |
|---------------------|:-------------:|:-------------:|:--------:|:----------------:|:--------------|
| Bonanjo (exact) | 0 | 0 km | Exact | 100 | Level 1 |
| Akwa | 2.5 | 2.5 km | None | 74.5 | Level 3 |
| Bonamoussadi | 5.0 | 5.0 km | None | 55.3 | Level 4 |
| Deido | 3.5 | 3.5 km | None | 68.1 | Level 3 |
| Bepanda | 3.0 | 3.0 km | Compatible | 77.2 | Level 2 |
| Makepe | 4.5 | 4.5 km | None | 60.5 | Level 3 |
| Bali | 2.8 | 2.8 km | None | 71.8 | Level 3 |
| New-Bell | 1.5 | 1.5 km | Compatible | 83.6 | Level 2 |
| Bonapriso | 0.8 | 0.8 km | None | 89.5 | Level 2 |
| Douala Centre | 1.2 | 1.2 km | None | 86.4 | Level 2 |
| Dibombari | ~30 | ~30 km | Prohibited | 0 | Prohibited (GEO-009) |

### 8.2 Yaoundé: Bastos as Reference

| Target Neighborhood | Distance (km) | Real Distance | Affinity | Geographic Score | Classification |
|---------------------|:-------------:|:-------------:|:--------:|:----------------:|:--------------|
| Bastos (exact) | 0 | 0 km | Exact | 100 | Level 1 |
| Golf | 1.2 | 1.2 km | Compatible | 89.1 | Level 2 |
| Santa Barbara | 1.8 | 1.8 km | Compatible | 83.6 | Level 2 |
| Omnisports Haut Bastos | 0.8 | 0.8 km | Compatible | 92.3 | Level 1 |
| Messa | 2.5 | 2.5 km | None | 74.5 | Level 3 |
| Centre | 3.5 | 3.5 km | None | 68.1 | Level 3 |
| Mfoundi | 4.0 | 4.0 km | None | 63.2 | Level 3 |
| Mokolo | 5.0 | 5.0 km | None | 55.3 | Level 4 |
| Nlongkak | 3.0 | 3.0 km | None | 71.8 | Level 3 |
| Mvog-Mbi | 6.0 | 6.0 km | None | 48.5 | Level 4 |
| Soa | ~12 | ~12 km | Prohibited | 0 | Prohibited (GEO-009) |

### 8.3 Yaoundé: Soa as Reference (GEO-009 Prohibitions)

| Target | Distance | Verdict | Rule |
|--------|:--------:|---------|------|
| Nkoabang | ~5 km | Compatible (affinity) | — |
| Mbankomo | ~8 km | Compatible (affinity) | — |
| Obala | ~35 km | **PROHIBITED** | GEO-009 |
| Bafia | ~65 km | **PROHIBITED** | GEO-009 |
| Yaoundé Centre | ~12 km | **PROHIBITED** | GEO-009 |

---

## 9. Integration with Matching Engine

The ProximityScorer feeds into the Matching Engine as follows:

```
MatchingEngine.compute_score(lead, property):
  ├── city_score         (30% V1, weighted per MATCH-001)
  │     └── from GeoEngine → city_match (exact/different)
  ├── neighborhood_score (25% V1)
  │     └── from GeoEngine → proximity_level (1-5)
  ├── budget_score       (25% V1)
  ├── property_type_score(15% V1)
  └── title_status_score (5% V1)
        └── boosted by:
              exact_neighborhood_match = +25 (MATCH-004)
              exact_city_match         = +20 (MATCH-005)
```

---

*Document Architecture Gold — 2026-07-15 — Référence complète GEO-008, GEO-010, GEO-011*
