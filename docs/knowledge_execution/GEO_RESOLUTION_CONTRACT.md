# Geographical Resolution Contract — Geo Engine

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** GEOGRAPHY_EXECUTION_ARCHITECTURE.md, GEOGRAPHY_MODEL.md, RULE_INDEX.md (GEO-001 to GEO-011)

---

This document defines the formal input and output contracts for the geographical resolution engine. Every component that consumes geographic data MUST adhere to these shapes.

---

## 1. Input Contract

### 1.1 Primary Input

```json
{
  "raw_location": "à Bastos",
  "message_id": "msg_<uuid>",
  "session_id": "ses_<uuid>",
  "channel": "whatsapp|telegram|dashboard|api",
  "context": {
    "known_city": "Yaoundé",
    "known_region": "Centre",
    "previous_locations": ["Messa", "Centre"],
    "session_occurrences": 3
  }
}
```

### 1.2 Input Field Specification

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `raw_location` | `string` | Yes | Raw location string extracted from user message |
| `message_id` | `string` | Yes | Source message identifier for traceability |
| `session_id` | `string` | Yes | Session identifier for occurrence tracking |
| `channel` | `enum` | Yes | Communication channel |
| `context.known_city` | `string` | No | Previously qualified city (if any) |
| `context.known_region` | `string` | No | Previously qualified region (if any) |
| `context.previous_locations` | `string[]` | No | Location mentions in current session |
| `context.session_occurrences` | `int` | Yes | Number of times this location was mentioned (for GEO-006 confidence) |

### 1.3 Input Validation Rules

| Rule | Validation | Error |
|------|-----------|-------|
| `raw_location` non-empty | Must be non-null, non-empty string | `invalid_input: empty_location` |
| `raw_location` length | Must be ≤ 200 characters | `invalid_input: location_too_long` |
| `channel` valid | Must be one of: `whatsapp, telegram, dashboard, api` | `invalid_input: unknown_channel` |
| `session_occurrences` ≥ 1 | Must be ≥ 1 | `invalid_input: invalid_occurrence_count` |

---

## 2. Processing Pipeline

```
Input: raw_location + context
    │
    ▼
┌────────────────────────────────────────────────────────────┐
│ Stage 1: EXTRACT                                          │
│ Apply GEO-005 patterns to isolate location substring      │
│ Output: extracted_text, pattern_matched, extraction_conf   │
└────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────┐
│ Stage 2: NORMALIZE                                        │
│ GEO-004: Levenshtein ≤ 3, typo correction, case folding   │
│ Output: normalized_text, normalization_distance            │
└────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────┐
│ Stage 3: ALIAS RESOLUTION                                  │
│ Match against city aliases → district aliases → typos      │
│ Output: canonical_name, aliases_matched[], alias_confidence │
└────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────┐
│ Stage 4: HIERARCHY RESOLUTION (GEO-001, GEO-002, GEO-003)  │
│ Resolve full parent chain: Pays→Région→...→Quartier       │
│ Validate city in priority/secondary list (GEO-002)         │
│ Validate neighborhood belongs to city (GEO-003)            │
│ Output: canonical_id, level, parent_chain                  │
└────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────┐
│ Stage 5: GPS RESOLUTION (GEO-007)                          │
│ Lookup coordinates with fallback chain                     │
│ Output: gps (lat/lng), gps_source, gps_accuracy            │
└────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────┐
│ Stage 6: CONFIDENCE                                        │
│ Composite from extraction + normalization + alias + GPS    │
│ Output: confidence (0.0-1.0)                               │
└────────────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────────────┐
│ Stage 7: PROXIMITY (GEO-008, GEO-009, GEO-010, GEO-011)   │
│ Calculate distances to known properties, score proximity   │
│ Output: nearby_locations[], mobility_context, geo_score     │
└────────────────────────────────────────────────────────────┘
    │
    ▼
Output: GeoResolutionResult
```

---

## 3. Output Contract

### 3.1 Success Output

```json
{
  "resolution_id": "geo_res_<uuid>",
  "status": "resolved",
  "input": {
    "raw_location": "à Bastos",
    "extracted_text": "Bastos",
    "pattern_matched": "à [lieu]",
    "extraction_confidence": 1.0
  },
  "normalized_location": "Bastos",
  "normalization_distance": 0,
  "canonical_id": "QTR-YA-BASTOS",
  "level": "Quartier",
  "level_code": 7,
  "parent_chain": {
    "pays": { "id": "CM", "name": "Cameroon" },
    "region": { "id": "REG-CE", "name": "Centre" },
    "departement": { "id": "DEP-MFO", "name": "Mfoundi" },
    "arrondissement": null,
    "commune": null,
    "ville": { "id": "CM-YAO", "name": "Yaoundé" },
    "quartier": { "id": "QTR-YA-BASTOS", "name": "Bastos" },
    "sous_quartier": null
  },
  "city": {
    "id": "CM-YAO",
    "name": "Yaoundé",
    "priority_rank": 1,
    "type": "priority"
  },
  "neighborhood": {
    "id": "QTR-YA-BASTOS",
    "name": "Bastos",
    "city_id": "CM-YAO"
  },
  "aliases_matched": [],
  "confidence": {
    "resolution": 0.95,
    "extraction": 1.0,
    "normalization": 1.0,
    "gps": 0.60,
    "overall": 0.85
  },
  "gps": {
    "lat": 3.8612,
    "lng": 11.5178,
    "accuracy": "LOW",
    "source": "city_centroid"
  },
  "gps_source": "inferred_from_city_gps",
  "nearby_locations": [
    { "name": "Golf", "distance_km": 1.2, "affinity": "compatible" },
    { "name": "Santa Barbara", "distance_km": 1.8, "affinity": "compatible" },
    { "name": "Omnisports Haut Bastos", "distance_km": 0.8, "affinity": "compatible" }
  ],
  "mobility_context": {
    "primary_mode": "driving",
    "alternative_mode": "walking",
    "estimated_travel_time_min": null
  },
  "geographic_score": {
    "total": 78,
    "components": {
      "city_score": 30,
      "neighborhood_score": 25,
      "gps_score": 8,
      "distance_score": 10,
      "travel_time_score": 5
    }
  },
  "ambiguities": [],
  "prohibition_check": {
    "status": "clear",
    "violations": []
  }
}
```

### 3.2 Output Field Specification

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resolution_id` | `string` | Yes | Unique identifier: `geo_res_<uuid>` |
| `status` | `enum` | Yes | `resolved`, `unresolved`, `ambiguous`, `uncovered` |
| `input` | `InputSnapshot` | Yes | Input as received, plus extraction metadata |
| `normalized_location` | `string` | Yes | Normalized location string |
| `normalization_distance` | `int` | Yes | Levenshtein distance (0 = exact) |
| `canonical_id` | `string` | No | Canonical identifier if resolved |
| `level` | `string` | No | Hierarchy level: `Pays`, `Région`, `Département`, `Arrondissement`, `Commune`, `Ville`, `Quartier`, `Sous-Quartier` |
| `level_code` | `int` | No | Numeric level: 1-8 (1=Pays, 8=Sous-Quartier) |
| `parent_chain` | `ParentChain` | No | Full hierarchy chain from Pays down to resolved level |
| `city` | `CityRef` | No | Canonical city reference (if city-level resolution) |
| `neighborhood` | `NeighborhoodRef` | No | Canonical neighborhood reference (if district-level resolution) |
| `aliases_matched` | `string[]` | Yes | List of alias strings that matched |
| `confidence` | `ConfidenceBreakdown` | Yes | Component and overall confidence scores |
| `gps` | `GPSCoordinates` | No | GPS coordinates if available |
| `gps_source` | `string` | No | Source of GPS data: `exact`, `gemini_recovered`, `inferred_from_city_gps`, `unavailable` |
| `nearby_locations` | `NearbyLocation[]` | Yes | Nearby compatible/incompatible locations |
| `mobility_context` | `MobilityContext` | Yes | Mobility mode(s) and travel estimates |
| `geographic_score` | `GeoScore` | No | Computed geographic score (GEO-011) |
| `ambiguities` | `Ambiguity[]` | Yes | Ambiguous match candidates (empty if unique) |
| `prohibition_check` | `ProhibitionCheck` | Yes | GEO-009 prohibition check result |

### 3.3 Error Outputs

#### Unresolved Location

```json
{
  "resolution_id": "geo_res_<uuid>",
  "status": "unresolved",
  "input": {
    "raw_location": "Paris",
    "extracted_text": "Paris",
    "pattern_matched": null,
    "extraction_confidence": 0.6
  },
  "normalized_location": "Paris",
  "normalization_distance": 0,
  "canonical_id": null,
  "level": null,
  "level_code": null,
  "parent_chain": null,
  "city": null,
  "neighborhood": null,
  "aliases_matched": [],
  "confidence": {
    "resolution": 0.0,
    "extraction": 0.6,
    "normalization": 1.0,
    "gps": 0.0,
    "overall": 0.0
  },
  "gps": null,
  "gps_source": "unavailable",
  "nearby_locations": [],
  "mobility_context": {
    "primary_mode": "driving",
    "alternative_mode": null,
    "estimated_travel_time_min": null
  },
  "geographic_score": null,
  "ambiguities": [],
  "prohibition_check": {
    "status": "not_applicable",
    "violations": []
  },
  "error": {
    "code": "UNRESOLVED_LOCATION",
    "message": "Location 'Paris' not found in any geography dataset.",
    "details": "Not in city list, alias list, or neighborhood inventory."
  }
}
```

#### Ambiguous Location

```json
{
  "resolution_id": "geo_res_<uuid>",
  "status": "ambiguous",
  "input": {
    "raw_location": "Centre",
    "extracted_text": "Centre",
    "pattern_matched": "à [lieu]",
    "extraction_confidence": 1.0
  },
  "normalized_location": "Centre",
  "normalization_distance": 0,
  "canonical_id": null,
  "level": null,
  "level_code": null,
  "parent_chain": null,
  "city": null,
  "neighborhood": null,
  "aliases_matched": ["Centre", "Centre Ville"],
  "confidence": {
    "resolution": 0.0,
    "extraction": 1.0,
    "normalization": 1.0,
    "gps": 0.0,
    "overall": 0.0
  },
  "gps": null,
  "gps_source": "unavailable",
  "nearby_locations": [],
  "mobility_context": {
    "primary_mode": "driving",
    "alternative_mode": null,
    "estimated_travel_time_min": null
  },
  "geographic_score": null,
  "ambiguities": [
    {
      "candidate": "Centre (Yaoundé)",
      "type": "neighborhood",
      "city": "Yaoundé",
      "confidence": 0.70
    },
    {
      "candidate": "Centre (Douala)",
      "type": "neighborhood",
      "city": "Douala",
      "confidence": 0.70
    },
    {
      "candidate": "Centre (Region)",
      "type": "region",
      "region": "Centre",
      "confidence": 0.50
    }
  ],
  "prohibition_check": {
    "status": "not_applicable",
    "violations": []
  },
  "error": {
    "code": "AMBIGUOUS_LOCATION",
    "message": "Location 'Centre' matched 3 candidates.",
    "details": "Cannot resolve without additional context or user clarification."
  }
}
```

#### Multiple Matches

```json
{
  "resolution_id": "geo_res_<uuid>",
  "status": "resolved",
  "...": "...",
  "confidence": {
    "resolution": 0.50,
    "extraction": 1.0,
    "normalization": 0.70,
    "gps": 0.30,
    "overall": 0.50
  },
  "ambiguities": [
    {
      "candidate": "Bonamoussadi (Douala)",
      "type": "neighborhood",
      "city": "Douala",
      "confidence": 0.70
    },
    {
      "candidate": "Bonamouti (Douala)",
      "type": "neighborhood",
      "city": "Douala",
      "confidence": 0.65
    }
  ],
  "note": "Resolved with lowest-distance match. Ambiguity flagged for audit."
}
```

### 3.4 Error States Summary

| Error Code | Status | Description | Trigger | Action |
|-----------|--------|-------------|---------|--------|
| `UNRESOLVED_LOCATION` | `unresolved` | Location not found in any dataset | No match after full pipeline | Return null canonical_id, confidence 0.0, trigger QUAL-015 if city |
| `AMBIGUOUS_LOCATION` | `ambiguous` | Multiple candidates within threshold | ≥ 2 matches with same Levenshtein distance | Return candidates, request user clarification |
| `UNCOVERED_CITY` | `uncovered` | City not in LAWIM coverage | Not in priority or secondary list | Trigger stop condition (QUAL-015), WAITLISTED |
| `INVALID_INPUT` | `error` | Input fails validation | Empty, too long, or invalid channel | Return with error details |
| `PROHIBITED` | `prohibited` | GEO-009 match | Prohibition pair detected | Hard reject, return violation details |

---

## 4. Confidence Calculation

### 4.1 Component Confidence

```
resolution_confidence:
  exact_match       = 1.0
  alias_match       = 0.85
  fuzzy_match_d1    = 0.80  (Levenshtein = 1)
  fuzzy_match_d2    = 0.75  (Levenshtein = 2)
  fuzzy_match_d3    = 0.70  (Levenshtein = 3)
  unresolved        = 0.0

extraction_confidence:
  min(100, occurrences × 20) / 100   (GEO-006)

normalization_confidence:
  exact (d=0)       = 1.0
  typo_corrected    = 0.90
  lev_distance      = max(0, 1.0 - (distance × 0.10))

gps_confidence:
  HIGH (<50m)       = 1.0
  MEDIUM (50-500m)  = 0.85
  LOW (>500m)       = 0.60
  UNKNOWN           = 0.30
  no_gps            = 0.0
```

### 4.2 Overall Confidence

```
overall = resolution × extraction × normalization × gps

Example — exact match with city GPS:
  1.0 × 1.0 × 1.0 × 0.60 = 0.60

Example — alias match with no GPS:
  0.85 × 1.0 × 0.90 × 0.30 = 0.23
```

---

## 5. Contract Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-15 | Initial canonical contract |

---

*Document Architecture Gold — 2026-07-15*
