# GEOGRAPHY EXTENSION MODEL

**Document ID:** LAWIM-H13-GEOGRAPHY-V1  
**Status:** CANONICAL DOMAIN EXTENSION  
**Date:** 2026-07-15  
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §3 (Domain Boundaries), §10 (CRM Pipeline), §5 (Search & Matching)  
**Source Crosswalks:** GEOGRAPHY_MODEL.md (Gold), GEOGRAPHY_EXECUTION_ARCHITECTURE.md, required_extensions.json (geography), PROXIMITY_SCORING_MODEL.md, GEO_RESOLUTION_CONTRACT.md

---

## Table of Contents

1. [Geographic Unit Model](#1-geographic-unit-model)
2. [Geographic Hierarchy & Administrative Levels](#2-geographic-hierarchy--administrative-levels)
3. [Geographic Aliases System](#3-geographic-aliases-system)
4. [Zone-Based Routing for CRM](#4-zone-based-routing-for-crm)
5. [Geographic Scoring Levels](#5-geographic-scoring-levels)
6. [Mobility Modes](#6-mobility-modes)
7. [Geographic Relations](#7-geographic-relations)
8. [Market Equivalents](#8-market-equivalents)
9. [Complete Extension Mapping Table](#9-complete-extension-mapping-table)

---

## 1. Geographic Unit Model

Every geographic entity across all levels shares a common base structure. This unified model replaces scattered city/neighborhood/zone fields with a single extensible unit registry.

### 1.1 Core Geographic Unit Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `canonical_id` | String | Yes | Unique hierarchical identifier (e.g., `CM.CTR.YAO.BST` for Bastos, Yaoundé) |
| `name` | String | Yes | Primary canonical name (e.g., "Yaoundé") |
| `aliases` | String[] | No | Alternative names, historical names, common misspellings |
| `level` | Enum | Yes | Geographic level: `country \| region \| department \| municipality \| district \| city \| neighborhood \| zone \| axis \| landmark \| village \| cluster \| gps_point \| geographic_alias` |
| `parent_id` | String | No | `canonical_id` of parent geographic unit (e.g., city for neighborhood) |
| `coordinates` | GeoJSON Point | No | GPS coordinates `{type: "Point", coordinates: [lng, lat]}` |
| `geometry` | GeoJSON Geometry | No | Polygon or MultiPolygon boundary geometry for areal units |
| `source` | Enum | Yes | `official \| recovered \| inferred \| user_provided \| ai_generated` |
| `confidence` | Float | Yes | Confidence score 0.0-1.0 (based on source reliability and verification) |
| `last_verified_at` | DateTime? | No | Last verification timestamp |
| `status` | Enum | Yes | `active \| deprecated \| draft \| pending_verification` |

### 1.2 Geographic Unit Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| GeographicUnit (parent) | 1:N | Parent-child hierarchy (e.g., city contains neighborhoods) |
| GeographicUnit (relation) | M:N | Cross-unit relations via GeographicRelation join table |
| Property | N:1 | Property belongs to a geographic unit (city, neighborhood) |
| Lead | N:1 | Lead references detected geographic unit |
| OrganizationMember | N:M | Agent assigned to geographic zones |
| User | N:1 | User's preferred/custom geography |

### 1.3 Canonical ID Convention

```
{country_code}.{region_code}.{department_code}.{city_code}.{neighborhood_code}
```

Examples:
- `CM.CTR.YAO` — Yaoundé city
- `CM.CTR.YAO.BST` — Bastos neighborhood in Yaoundé
- `CM.LIT.DLA.AKW` — Akwa neighborhood in Douala
- `CM.OUW.BFS` — Bafoussam city

---

## 2. Geographic Hierarchy & Administrative Levels

A 14-level hierarchy covering all geographic units needed for African real estate operations. The model supports both administrative boundaries (official government divisions) and operational boundaries (LAWIM-specific groupings).

### 2.1 Complete Level Definitions

| Level | Code | Category | Description | Example | Parent | Cardinality |
|-------|------|----------|-------------|---------|--------|-------------|
| 1 | `country` | Administrative | Sovereign state | Cameroon (CM) | — | 1 |
| 2 | `region` | Administrative | First-level administrative division | Centre, Littoral | country | 10 per country |
| 3 | `department` | Administrative | Second-level administrative division | Mfoundi, Wouri | region | 58 per country |
| 4 | `municipality` | Administrative | Legal municipal entity | Yaoundé VI | department | 360 per country |
| 5 | `district` | Administrative | Sub-municipal administrative district | District de Bastos | municipality | ~1500 per country |
| 6 | `city` | Operational | Urban settlement (may span multiple municipalities) | Yaoundé | region | ~200 per country |
| 7 | `neighborhood` | Operational | Named residential/commercial area within city | Bastos | city | ~4000 per country |
| 8 | `zone` | Operational | LAWIM-defined grouping of neighborhoods for routing | Yaoundé Nord | city/neighborhood | Configurable |
| 9 | `axis` | Operational | Linear geographic corridor (road, boulevard) | Axe Bastos-Mvog-Mbi | city/neighborhood | Configurable |
| 10 | `landmark` | Operational | Notable point of interest (market, hospital, school) | Marché Mfoundi | neighborhood | Configurable |
| 11 | `village` | Operational | Rural settlement outside municipal boundaries | Nkoabang | district | Configurable |
| 12 | `cluster` | Operational | Group of geographically related units for matching | Cluster Yaoundé Nord | zone | Configurable |
| 13 | `gps_point` | Reference | Precise GPS coordinate reference | 3.848032, 11.502075 | any | Unbounded |
| 14 | `geographic_alias` | Reference | Non-hierarchical alias entry for name resolution | "Ydé" → Yaoundé | any | Unbounded |

### 2.2 Cameroon-Specific Level Mapping

| Level | Cameroon Implementation | Data Status | Coverage |
|-------|------------------------|-------------|----------|
| `country` | Cameroon (CM) | Complete | 100% |
| `region` | 10 regions | Complete | 100% |
| `department` | 58 departments | Partial | ~60% |
| `municipality` | 360 communes | Partial | ~40% |
| `district` | ~1,500 districts | Partial | ~30% |
| `city` | 28 cities (10 priority + 18 secondary) | Complete | 100% |
| `neighborhood` | ~4,000 neighborhoods | Partial | ~10% (382 documented) |
| `zone` | LAWIM-defined routing zones | Draft | Configurable |
| `axis` | Major urban axes | Minimal | N/A |
| `landmark` | Notable landmarks | Minimal | N/A |
| `village` | Rural settlements | Sparse | N/A |
| `cluster` | Matching clusters | Draft | Configurable |
| `gps_point` | Reference coordinates | Partial | 62.6% coverage |
| `geographic_alias` | Alias entries | Partial | Limited |

### 2.3 Hierarchy Invariants

- Every geographic unit MUST have exactly one parent (except `country` which has none).
- The parent chain MUST be traceable to the `country` level.
- An operational unit (zone, axis, cluster) may have multiple parent candidates; the binding is context-dependent.
- `gps_point` and `geographic_alias` are reference levels and MAY exist outside the strict hierarchy (they serve as resolvers into the hierarchy).

---

## 3. Geographic Aliases System

A comprehensive alias system resolves user-provided location names to canonical geographic units. This enables fuzzy matching across variant spellings, abbreviations, social variants, and legacy names.

### 3.1 Alias Types

| Type | Description | Example | Confidence Impact | Resolution Priority |
|------|-------------|---------|-------------------|---------------------|
| `canonical` | Primary official name | "Yaoundé" | +0.00 | 1 (Highest) |
| `official_alias` | Recognized alternative official name | "Yáundé" | -0.02 | 2 |
| `common_variant` | Common local spelling variant | "Youndé" | -0.05 | 3 |
| `social_variant` | Social media / SMS abbreviation | "Ydé", "Yao" | -0.10 | 4 |
| `typo` | Known typographical error | "Yaunde" | -0.15 | 5 |
| `historical` | Historical name no longer in official use | "Jáunde" (German colonial) | -0.10 | 6 |
| `compound` | Compound name with extra qualifier | "Yaoundé Ville" | -0.05 | 3 |
| `legacy` | Legacy system name from Heritage Gold | "YAOUNDE_CAPITALE" | -0.10 | 7 |
| `translation` | Name in another language | "Jaunde" (German) | -0.15 | 8 |
| `phonetic` | Phonetic approximation | "Yaonday" | -0.20 | 9 (Lowest) |

### 3.2 Alias Resolution Pipeline

```
user_input (string)
  │
  ▼
┌─────────────────────────────────────┐
│ 1. Normalization                    │
│    - Lowercase                      │
│    - Unicode normalization (NFD)    │
│    - Remove diacritics              │
│    - Collapse whitespace            │
└──────────┬──────────────────────────┘
           ▼
┌─────────────────────────────────────┐
│ 2. Exact Match                      │
│    Match against canonical names +  │
│    all alias entries                │
│    → if match: resolve, stop        │
└──────────┬──────────────────────────┘
           ▼ (no exact match)
┌─────────────────────────────────────┐
│ 3. Fuzzy Match                      │
│    Levenshtein distance ≤ 3         │
│    Match against:                   │
│    - canonical names                │
│    - all alias entries              │
│    - location_synonyms table        │
│    → if unique match: resolve       │
│    → if multiple: select by highest │
│      priority + lowest distance     │
└──────────┬──────────────────────────┘
           ▼ (no fuzzy match)
┌─────────────────────────────────────┐
│ 4. Compound Extraction              │
│    Strip known qualifiers:          │
│    "quartier", "ville", "cité",     │
│    "axe", "zone", "carrefour"       │
│    Retry exact + fuzzy match        │
│    → if match: resolve              │
└──────────┬──────────────────────────┘
           ▼ (no match)
┌─────────────────────────────────────┐
│ 5. Knowledge Learning               │
│    Store as candidate_alias for     │
│    admin review                     │
│    Increment occurrence counter     │
│    At 5 occurrences: auto-create    │
│    alias with confidence = 0.50     │
│    Return unresolved (confidence 0) │
└─────────────────────────────────────┘
```

### 3.3 Alias Storage

```typescript
interface GeographicAlias {
  id: UUID;
  canonical_unit_id: String;       // References GeographicUnit.canonical_id
  alias: String;                    // The alias string
  alias_type: AliasType;            // canonical | official_alias | common_variant | ...
  language: String?;                // ISO 639-1 code (fr, en, pid, de)
  source: String;                   // Origin of this alias (knowledge_base, user_submitted, ai_discovered)
  confidence: Float;                // 0.0-1.0
  occurrences: Int;                 // How many times this alias has been observed
  last_seen_at: DateTime?;          // Last observation timestamp
  created_at: DateTime;
  status: Enum;                     // active | deprecated | pending_review
}
```

### 3.4 Location Synonym Table (Supabase)

| Column | Type | Description |
|--------|------|-------------|
| `input_text` | String | Raw user input |
| `canonical_id` | String | Resolved canonical unit ID |
| `match_type` | Enum | `exact \| fuzzy \| compound \| manual` |
| `match_distance` | Int | Levenshtein distance (0 for exact) |
| `confidence` | Float | Resolution confidence |
| `occurrences` | Int | Usage count |
| `last_matched_at` | DateTime | Last successful match |

---

## 4. Zone-Based Routing for CRM

Zones are LAWIM-defined groupings of geographic units used to route leads to appropriate agents. Unlike administrative levels, zones are purely operational and configurable per organization.

### 4.1 Zone Model

| Field | Type | Description |
|-------|------|-------------|
| `zone_id` | String | Zone identifier (e.g., `ZONE-YAO-NORD`) |
| `name` | String | Display name (e.g., "Yaoundé Nord") |
| `organization_id` | UUID | Organization that owns this zone definition |
| `member_ids` | UUID[] | Agents assigned to this zone |
| `geographic_unit_ids` | String[] | Geographic units (cities, neighborhoods) covered by this zone |
| `is_active` | Boolean | Whether this zone is active for routing |
| `routing_priority` | Int | Priority order when multiple zones match (lower = higher) |
| `max_leads_per_agent` | Int | Max concurrent leads per agent in this zone |
| `created_at` | DateTime | Zone creation timestamp |

### 4.2 Zone Routing Decision Tree

```
Lead detected with city/neighborhood
  │
  ▼
Resolve to canonical geographic unit(s)
  │
  ▼
Find matching zones for organization:
  - Zone.geographic_unit_ids CONTAINS resolved unit
  - Zone.is_active = true
  │
  ├── Single zone match → Route within zone (lowest load agent wins)
  │
  ├── Multiple zone matches → Select by routing_priority (lowest number)
  │                            → Route within selected zone
  │
  └── No zone match → Fallback to availability-based routing
                       → Route to any active agent with capacity
                       → If no agent available, escalate to admin
```

### 4.3 Multi-Level Zone Assignment

An agent may be assigned to zones at different geographic levels:

| Level | Example | Use Case |
|-------|---------|----------|
| City-wide | `ZONE-YAO` | Agent covers all Yaoundé |
| Neighborhood cluster | `ZONE-YAO-NORD` | Agent covers northern neighborhoods |
| Specific neighborhoods | `ZONE-BASTOS-GOLF` | Agent covers Bastos + Golf only |
| Axis | `ZONE-AXE-BASTOS` | Agent covers properties along Bastos axis |
| Cross-city | `ZONE-YAO-DLA` | Agent covers both Yaoundé and Douala |

### 4.4 Routing Rules by Zone

| Rule | Description |
|------|-------------|
| Agent must have `is_active_agent = true` AND consent to routing in assigned zone |
| Agent must have `current_leads < max_leads` for the zone |
| SPAM-classified leads are never routed |
| Within a zone, round-robin distribution among eligible agents |
| If no agent responds within SLA, re-route to next eligible agent in same zone |
| After 3 failed routing attempts, escalate to admin |

---

## 5. Geographic Scoring Levels

Five graduated scoring levels for geographic matching. Each level represents the precision of a geographic match between a demandeur's stated preference and available properties.

### 5.1 Scoring Levels

| Level | Code | Score Weight | Description | Example |
|-------|------|:------------:|-------------|---------|
| 1 — Exact | `geo_exact` | 1.00 | Exact geographic match | Neighborhood "Bastos" ↔ Property in "Bastos" |
| 2 — High | `geo_high` | 0.85 | Same zone or compatible axis | Neighborhood "Bastos" ↔ Property in "Golf" (same zone) |
| 3 — Medium | `geo_medium` | 0.60 | Same city, compatible cluster | Neighborhood "Bastos" ↔ Property in "Mvog-Mbi" (same cluster) |
| 4 — Low | `geo_low` | 0.30 | Same city, different cluster | Neighborhood "Bastos" ↔ Property in "Ngoa-Ekellé" |
| 5 — Minimal | `geo_minimal` | 0.10 | Compatible city (affinity) | City "Yaoundé" ↔ Property city "Yaoundé" (no neighborhood match) |

### 5.2 Score Application

```
geo_score = base_weight × geo_level_weight

Where:
- base_weight = geographic contribution to total match score (configurable, default 30%)
- geo_level_weight = weight from the level table above

Example:
- Location contributes 30% of total match score
- Exact neighborhood match: 0.30 × 1.00 = 0.30 contribution
- Same city, different cluster: 0.30 × 0.30 = 0.09 contribution
```

### 5.3 Level Determination Logic

```typescript
function determineGeoLevel(demandeurLocation, propertyLocation): GeoLevel {
  // Level 1: Exact match on neighborhood
  if (demandeurLocation.neighborhood_id === propertyLocation.neighborhood_id) {
    return 'geo_exact';
  }

  // Level 2: Same zone or compatible axis
  if (shareZone(demandeurLocation, propertyLocation) ||
      shareAxis(demandeurLocation, propertyLocation)) {
    return 'geo_high';
  }

  // Level 3: Same cluster
  if (shareCluster(demandeurLocation, propertyLocation)) {
    return 'geo_medium';
  }

  // Level 4: Same city, different clusters
  if (demandeurLocation.city_id === propertyLocation.city_id) {
    return 'geo_low';
  }

  // Level 5: City affinity match
  if (hasAffinity(demandeurLocation.city_id, propertyLocation.city_id)) {
    return 'geo_minimal';
  }

  // No match
  return null;
}
```

### 5.4 Geographic Score in Matching

| Component | Weight | Level Mapping |
|-----------|--------|---------------|
| City match | 30% of geo score | Level 4-5 |
| Neighborhood match | 40% of geo score | Level 1-2 |
| Zone/Cluster match | 20% of geo score | Level 2-3 |
| Proximity (GPS) | 10% of geo score | All levels (distance-based) |

---

## 6. Mobility Modes

Three mobility modes define the travel thresholds used in proximity matching and commute compatibility assessment.

### 6.1 Mode Definitions

| Mode | Code | Max Distance | Typical Speed | Description |
|------|------|:------------:|:-------------:|-------------|
| Low (Walk) | `mobility_low` | 5 km | 5 km/h | Walking distance — properties within walkable range |
| Medium (Drive) | `mobility_medium` | 20 km | 30 km/h (urban) | Short driving distance — standard commute range |
| High (Regional) | `mobility_high` | 50+ km | 80 km/h (inter-urban) | Regional commuting — acceptable for investment properties |

### 6.2 Mobility Context Selection

| Condition | Selected Mode | Rationale |
|-----------|---------------|-----------|
| Demandeur explicitly requests "walking distance" | `mobility_low` | User preference |
| Demandeur requests proximity without specifying | `mobility_medium` | Default standard |
| Investment property type | `mobility_high` | Investors accept longer distance |
| Diaspora investor | `mobility_high` | Diaspora less sensitive to local commute |
| Urgent rental (student, worker) | `mobility_low` | Tenant needs daily commute |
| Commercial property search | `mobility_medium` | Commercial viability within drive range |

### 6.3 Mobility Scoring Integration

```
mobility_score = match_distance < mode_max_distance ? 1.0 : decay_factor

Where:
- If property is within the mode's max distance → full score (1.0)
- If beyond max distance → score decays: max(0, 1 - (excess_km / mode_max_distance))
- Hard cutoff at 2× mode_max_distance (score = 0 beyond that)

Example:
- Medium mode (20 km max)
- Property is 25 km away
- Within 2× cutoff (40 km)
- mobility_score = 1 - (5/20) = 0.75
```

### 6.4 COMMUTE_COMPATIBLE Relation

The `COMMUTE_COMPATIBLE` relation between geographic units is derived from mobility mode thresholds:

| Pair Type | Mobility Mode | Example |
|-----------|---------------|---------|
| Same neighborhood | Low (5 km) | Bastos ↔ Bastos Haut |
| Same cluster | Medium (20 km) | Bastos ↔ Mvog-Mbi (8 km) |
| Same city | Medium (20 km) | Yaoundé neighborhoods |
| Affinity cities | High (50+ km) | Yaoundé ↔ Mbalmayo (45 km) |
| Cross-region | High (50+ km) | Douala ↔ Yaoundé (200 km) — requires special handling |

---

## 7. Geographic Relations

Relationships between geographic units captured in a dedicated join table with typed edges.

### 7.1 Relation Types

| Relation | Code | Symmetric | Description | Cardinality |
|----------|------|:---------:|-------------|:-----------:|
| NEARBY | `nearby` | Yes | Geographic units in close proximity (walking distance) | N:M |
| CONTAINS | `contains` | No | Parent-child containment relationship | 1:N |
| ADJACENT | `adjacent` | Yes | Units sharing a border or immediately adjacent | N:M |
| SAME_AXIS | `same_axis` | Yes | Units along the same major road/axis | N:M |
| SAME_CLUSTER | `same_cluster` | Yes | Units in the same LAWIM-defined cluster | N:M |
| COMMUTE_COMPATIBLE | `commute_compatible` | Yes | Units within acceptable commute distance | N:M |
| ADMINISTRATIVE_PARENT | `administrative_parent` | No | Official administrative hierarchy relationship | 1:N |
| MARKET_EQUIVALENT | `market_equivalent` | Yes | Cross-market equivalent units (see §8) | N:M |

### 7.2 Geographic Relation Model

```typescript
interface GeographicRelation {
  id: UUID;
  source_unit_id: String;            // GeographicUnit.canonical_id
  target_unit_id: String;            // GeographicUnit.canonical_id
  relation_type: RelationType;       // nearby | contains | adjacent | same_axis | ...
  direction: Enum;                   // bidirectional | source_to_target | target_to_source
  weight: Float;                     // Relation strength (0.0-1.0)
  metadata: JSON?;                   // {distance_km, estimated_travel_time, road_quality, ...}
  source: String;                    // Origin of relation data (official, inferred, manual)
  valid_from: DateTime;
  valid_until: DateTime?;
  status: Enum;                      // active | deprecated
}
```

### 7.3 Relation Usage by Component

| Component | Relations Used | Purpose |
|-----------|----------------|---------|
| Matching Engine | `nearby`, `same_axis`, `same_cluster`, `commute_compatible`, `market_equivalent` | Geographic match scoring |
| CRM Routing | `contains`, `adjacent` | Zone-based agent routing |
| Search Engine | `contains`, `nearby`, `market_equivalent` | Expand/restrict search radius |
| Qualification | `contains` | Validate city/neighborhood membership |
| Proximity Scoring | `nearby`, `adjacent`, `commute_compatible` | Distance-based scoring |
| Price Estimation | `market_equivalent` | Cross-market price comparison |
| Visit Planning | `nearby`, `adjacent` | Grouped visit optimization |

### 7.4 Relation Inference Rules

| Rule | Description |
|------|-------------|
| `CONTAINS` is derived from the `parent_id` hierarchy | If unit A has parent_id = unit B, then B CONTAINS A |
| `ADJACENT` is inferred from shared borders in geometry | If geometry polygons share an edge, units are adjacent |
| `SAME_AXIS` is manually curated | Axes are defined per city (e.g., "Axe Bastos-Mvog-Mbi") |
| `SAME_CLUSTER` is manually curated | Clusters group neighborhoods with high affinity |
| `NEARBY` is computed from GPS proximity (≤ 2 km) | Automatically generated for units with GPS data |
| `COMMUTE_COMPATIBLE` is computed from mobility mode | Within mobility_low (5 km), mobility_medium (20 km), or mobility_high (50+ km) |
| `MARKET_EQUIVALENT` is manually curated | Cross-market equivalence requires expert validation |

---

## 8. Market Equivalents

Market equivalents are geographic units from different markets (cities, regions, or countries) that share similar characteristics for real estate purposes. They enable cross-market matching, price estimation, and investment recommendations.

### 8.1 Market Equivalent Dimensions

| Dimension | Weight | Description |
|-----------|:------:|-------------|
| Population density | 25% | Population per km² |
| Economic activity | 20% | Commercial and business activity level |
| Real estate price tier | 20% | Average price per m² |
| Infrastructure level | 15% | Roads, utilities, public services |
| Urbanization pattern | 10% | Urban vs suburban vs rural character |
| Demographic profile | 10% | Income levels, age distribution, household size |

### 8.2 Market Equivalent Examples

| Source Unit | Equivalent Unit | Similarity Score | Rationale |
|-------------|----------------|:----------------:|-----------|
| Bastos (Yaoundé) | Bonapriso (Douala) | 0.85 | Both upscale residential, similar price tier |
| Mvog-Mbi (Yaoundé) | Deido (Douala) | 0.75 | Both middle-class residential |
| Odza (Yaoundé) | Makepe (Douala) | 0.70 | Both developing residential areas |
| Akwa (Douala) | Bastos (Yaoundé) | 0.80 | Both commercial + upscale residential |
| Bonamoussadi (Douala) | Biyem-Assi (Yaoundé) | 0.75 | Both large mixed residential zones |
| Briqueterie (Yaoundé) | Ndogbong (Douala) | 0.65 | Both working-class neighborhoods |

### 8.3 Cross-Market Matching Workflow

```
User requests property in "Bastos, Yaoundé"
  │
  ▼
Search properties in Bastos (exact match)
  │
  ├── Properties found → Return results
  │
  └── No properties in Bastos → Trigger market equivalent expansion
        │
        ▼
      Find MARKET_EQUIVALENT relations for Bastos
        │
        ├── Bonapriso (Douala) — Score 0.85 → Include with weight 0.85
        ├── Akwa (Douala) — Score 0.80 → Include with weight 0.80
        │
        ▼
      Present expanded results with equivalent annotation:
      "Aucun bien trouvé à Bastos. Biens similaires dans
       des quartiers équivalents : Bonapriso (Douala) — 85% compatible"
```

### 8.4 Market Equivalent Lifecycle

| Stage | Description | Trigger |
|-------|-------------|---------|
| `suggested` | AI-suggested equivalence, pending review | Algorithmic detection of similar profiles |
| `validated` | Human-expert validated equivalence | Admin/domain expert review |
| `active` | Active for cross-market matching | Manual activation after validation |
| `deprecated` | No longer considered equivalent | Market changes or expert override |

---

## 9. Complete Extension Mapping Table

### 9.1 Geography Extensions

| Extension ID | Source Concept | Target Entity | Proposed Structure | Priority | Human Decision |
|-------------|---------------|---------------|-------------------|----------|----------------|
| EXT-GEO-001 | Geographic unit model (14 levels) | GeographicUnit | Unified unit registry with canonical_id, name, aliases[], level, parent_id, coordinates, geometry, source, confidence, last_verified_at, status | P1 | Y — level definitions |
| EXT-GEO-002 | Geographic hierarchy (admin + operational) | GeographicUnit | 14-level hierarchy: country → region → department → municipality → district → city → neighborhood → zone → axis → landmark → village → cluster → gps_point → geographic_alias | P1 | Y — hierarchy scope |
| EXT-GEO-003 | Geographic aliases system | GeographicAlias | Alias registry: 10 alias types, resolution pipeline (exact → fuzzy → compound → learning), Levenshtein ≤ 3 matching | P1 | Y — fuzzy thresholds |
| EXT-GEO-004 | Zone-based routing for CRM | Zone (OrganizationMember) | Zone model with geographic_unit_ids, member_ids, routing_priority; multi-level zone assignment; 4 routing methods | P1 | Y — routing strategy |
| EXT-GEO-005 | Geographic scoring levels (5) | MatchingEngine | 5-level geographic scoring: exact (1.00), high (0.85), medium (0.60), low (0.30), minimal (0.10) | P1 | Y — score weights |
| EXT-GEO-006 | Mobility modes (3) | ProximityScorer | 3 mobility modes: low/5km walk, medium/20km drive, high/50+km regional; context-based selection; scoring integration | P2 | Y — distance thresholds |
| EXT-GEO-007 | Geographic relations (8 types) | GeographicRelation | Relation join table: NEARBY, CONTAINS, ADJACENT, SAME_AXIS, SAME_CLUSTER, COMMUTE_COMPATIBLE, ADMINISTRATIVE_PARENT, MARKET_EQUIVALENT | P2 | N |
| EXT-GEO-008 | Market equivalents | GeographicRelation (MARKET_EQUIVALENT) | Cross-market equivalence with 6 similarity dimensions; lifecycle (suggested → validated → active → deprecated) | P2 | Y — equivalence criteria |
| EXT-GEO-009 | GPS point system | GeographicUnit (gps_point level) | GPS coordinate storage with precision levels (HIGH/MEDIUM/LOW/UNKNOWN), fallback chain, source metadata | P2 | N |
| EXT-GEO-010 | Geographic confidence calculation | GeographicUnit | Composite confidence from resolution quality + GPS accuracy + source reliability + ambiguity factor | P2 | N |
| EXT-GEO-011 | Location synonym table | LocationSynonym | Supabase table mapping raw input → canonical_id with match_type, distance, confidence, occurrences | P2 | Y — learning policy |
| EXT-GEO-012 | Relation inference engine | GeographicRelation | Automated inference: CONTAINS from hierarchy, ADJACENT from geometry, NEARBY from GPS, COMMUTE_COMPATIBLE from mobility | P2 | N |

### 9.2 All Geography Fields Extension Table

| Field | Entity | Type | Extension Source | Description |
|-------|--------|------|------------------|-------------|
| `canonical_id` | GeographicUnit | String | EXT-GEO-001 | Unique hierarchical identifier |
| `name` | GeographicUnit | String | EXT-GEO-001 | Primary canonical name |
| `aliases` | GeographicUnit | String[] | EXT-GEO-003 | Alternative names |
| `level` | GeographicUnit | Enum | EXT-GEO-001 | Geographic level (14 values) |
| `parent_id` | GeographicUnit | String? | EXT-GEO-002 | Parent canonical_id |
| `coordinates` | GeographicUnit | GeoJSON Point? | EXT-GEO-009 | GPS coordinates |
| `geometry` | GeographicUnit | GeoJSON? | EXT-GEO-001 | Boundary polygon |
| `source` | GeographicUnit | Enum | EXT-GEO-001 | Data source (official/recovered/inferred/user_provided/ai_generated) |
| `confidence` | GeographicUnit | Float | EXT-GEO-010 | Confidence score 0.0-1.0 |
| `last_verified_at` | GeographicUnit | DateTime? | EXT-GEO-001 | Last verification timestamp |
| `status` | GeographicUnit | Enum | EXT-GEO-001 | active/deprecated/draft/pending_verification |
| `alias` | GeographicAlias | String | EXT-GEO-003 | Alias string |
| `alias_type` | GeographicAlias | Enum | EXT-GEO-003 | Alias classification (10 types) |
| `alias_language` | GeographicAlias | String? | EXT-GEO-003 | ISO 639-1 language code |
| `alias_confidence` | GeographicAlias | Float | EXT-GEO-003 | Alias confidence 0.0-1.0 |
| `zone_id` | Zone | String | EXT-GEO-004 | Zone identifier |
| `geographic_unit_ids` | Zone | String[] | EXT-GEO-004 | Covered geographic units |
| `member_ids` | Zone | UUID[] | EXT-GEO-004 | Assigned agents |
| `routing_priority` | Zone | Int | EXT-GEO-004 | Zone priority for routing |
| `source_unit_id` | GeographicRelation | String | EXT-GEO-007 | Source geographic unit |
| `target_unit_id` | GeographicRelation | String | EXT-GEO-007 | Target geographic unit |
| `relation_type` | GeographicRelation | Enum | EXT-GEO-007 | Relation type (8 values) |
| `relation_weight` | GeographicRelation | Float | EXT-GEO-007 | Relation strength 0.0-1.0 |
| `geo_exact_score` | MatchingEngine | Float | EXT-GEO-005 | 1.00 neighborhood exact |
| `geo_high_score` | MatchingEngine | Float | EXT-GEO-005 | 0.85 zone/axis match |
| `geo_medium_score` | MatchingEngine | Float | EXT-GEO-005 | 0.60 cluster match |
| `geo_low_score` | MatchingEngine | Float | EXT-GEO-005 | 0.30 same city |
| `geo_minimal_score` | MatchingEngine | Float | EXT-GEO-005 | 0.10 city affinity |
| `mobility_mode` | ProximityScorer | Enum | EXT-GEO-006 | low/medium/high |
| `mobility_max_distance` | ProximityScorer | Int | EXT-GEO-006 | 5/20/50+ km |
| `mobility_score` | ProximityScorer | Float | EXT-GEO-006 | Computed proximity |
| `zones` | OrganizationMember | String[] | EXT-GEO-004 | Agent zone assignment |
| `input_text` | LocationSynonym | String | EXT-GEO-011 | Raw user input |
| `match_type` | LocationSynonym | Enum | EXT-GEO-011 | exact/fuzzy/compound/manual |
| `match_distance` | LocationSynonym | Int | EXT-GEO-011 | Levenshtein distance |

### 9.3 New Entities

| Entity | Description | Extensions |
|--------|-------------|------------|
| `GeographicUnit` | Central geography entity; represents any geographic location at any of 14 levels | EXT-GEO-001 through EXT-GEO-003, EXT-GEO-009, EXT-GEO-010 |
| `GeographicAlias` | Alternative name mapping for fuzzy location resolution | EXT-GEO-003 |
| `Zone` | LAWIM-defined operational grouping of geographic units for CRM routing | EXT-GEO-004 |
| `GeographicRelation` | Typed relationship between geographic units (8 relation types) | EXT-GEO-007, EXT-GEO-008, EXT-GEO-012 |
| `LocationSynonym` | Raw input → canonical mapping table for learned location resolution | EXT-GEO-011 |

---

*End of GEOGRAPHY_EXTENSION_MODEL.md — 12 geography extensions, 14 hierarchical levels, 10 alias types, 8 relation types, 5 scoring levels, 3 mobility modes defined.*
