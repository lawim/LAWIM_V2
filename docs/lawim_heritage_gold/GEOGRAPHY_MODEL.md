# GEOGRAPHY MODEL — LAWIM Heritage Gold (Validated)

**Mission :** LAWIM Heritage Gold — Validation des connaissances géographiques
**Date :** 2026-07-15
**Principe :** Contient UNIQUEMENT des connaissances validées avec sources. Les gaps et incertitudes sont explicitement documentés.

---

## 1. Territorial Hierarchy

**Source :** LAWIM `Directive/09-GEOLOCATION-REFERENCE.md` (analysé dans reaudit GOLD)

| Level | Name | Description | Data Populated |
|-------|------|-------------|----------------|
| 1 | Pays | Cameroon | Yes |
| 2 | Région | 10 regions | Yes |
| 3 | Département | Administrative department | Partial |
| 4 | Arrondissement | Sub-division | Partial |
| 5 | Commune | Municipality | Partial |
| 6 | Ville / City | Urban center | Yes (10 priority + 18 secondary) |
| 7 | Quartier / District | Neighborhood | Yes (382 total) |
| 8 | Sous-Quartier | Sub-neighborhood | Minimal (Buea only in district_hierarchy.json) |
| 9 | Point de repère / Landmark | Landmark or POI | **Zero landmarks stored** |
| 10 | Coordonnées GPS | GPS coordinates | 239/382 = 62.6% coverage |

**Source reference:** `09-GEOLOCATION-REFERENCE.md` §1.1 (territorial levels), `reports/lawim_heritage_gold/GEOGRAPHY_QUALIFICATION_MATCHING_REAUDIT.md` §1.1-1.2

**Notes:**
- The V4 document (`GEO_REFERENCE_MODEL_CAMEROON_V4.md`) defines a 6-level hierarchy: Market → Cluster → Subcluster → Neighborhood → Neighborhood Affinity → GPS
- The Alignment Plan (`GEO_MODEL_ALIGNMENT_PLAN.md`) defines a 7-level GeographicLevel enum: COUNTRY → REGION → DEPARTMENT → SUBDIVISION → CITY → DISTRICT → ZONE
- Levels SUBDIVISION and ZONE are declared in enums but have **zero seeded data** — this is a critical gap

---

## 2. LAWIM Zones

**Source :** LAWIMA `agents` table (zone field), reaudit GOLD §1.2

LAWIM Zones are functional groupings of neighborhoods/cities for agent routing. They are distinct from the administrative hierarchy.

| Aspect | Detail |
|--------|--------|
| Purpose | Agent assignment and lead routing |
| Data source | LAWIMA `agents` table (zone field) |
| Implementation | Referenced in code but ZONE level has 0 seeded entries |
| Gap | No explicit zone definitions exist in JSON data files |

---

## 3. Priority Cities (10)

**Source :** `knowledge_unified/geography/cities.json` (verified), `RECOVERED_KNOWLEDGE.md` KNW-SYSTEM-PROMPT-014

| Priority Rank | City | Region | Aliases | GPS Coordinates |
|---------------|------|--------|---------|-----------------|
| 1 | Yaoundé | Centre | Yaounde, Ydé, YDE, Yaoundé Ville, Yaounde Ville, Yaounde Centre, Yaounde City | 3.848032, 11.502075 |
| 2 | Douala | Littoral | Douala Ville, Douala Centre, DLA, Douala City | 4.051056, 9.767868 |
| 3 | Bamenda | North West | Bamenda Town, Bamenda City | Not stored |
| 4 | Bafoussam | West | Bafoussam Ville, Bafoussam Centre | Not stored |
| 5 | Buea | South West | Buea Town, UB City | Not stored |
| 6 | Kribi | South | Kribi Beach, Kribi Port, Kribi Centre | Not stored |
| 7 | Nkongsamba | Littoral | Nkongsamba Centre, Nkongsamba Ville | Not stored |
| 8 | Maroua | Far North | Maroua Ville, Maroua Centre | Not stored |
| 9 | Limbe | South West | Limbé, Limbe Town | Not stored |
| 10 | Garoua | North | Garoua Centre, Garoua Ville | Not stored |

**Source:** `knowledge_unified/geography/cities.json:8-103`

---

## 4. Secondary Cities (18)

**Source :** `knowledge_unified/geography/cities.json:104-109`

All 18 secondary cities have **empty district data — critical gap**:

| # | City | District Data | GPS Data |
|---|------|---------------|----------|
| 1 | Ebolowa | None | None |
| 2 | Mbalmayo | None | None |
| 3 | Ngaoundéré | None | None |
| 4 | Dschang | None | None |
| 5 | Foumban | None | None |
| 6 | Mbouda | None | None |
| 7 | Bertoua | None | None |
| 8 | Kumba | None | None |
| 9 | Edéa | None | None |
| 10 | Meiganga | None | None |
| 11 | Batouri | None | None |
| 12 | Ambam | None | None |
| 13 | Kousseri | None | None |
| 14 | Mora | None | None |
| 15 | Kaélé | None | None |
| 16 | Guider | None | None |
| 17 | Tiko | None | None |
| 18 | Mutengene | None | None |

**Note:** Ngaoundéré and Bertoua are listed as primary in `city-affinity-matrix.md` but classified as secondary in `cities.json` with zero district data — this is a documented discrepancy.

---

## 5. GPS Coverage

**Source :** `reports/lawim_heritage_gold/GEOGRAPHY_QUALIFICATION_MATCHING_REAUDIT.md` §1.7

| Metric | Value |
|--------|-------|
| Total districts (neighborhood inventory) | 382 |
| Districts with GPS | 239 |
| GPS coverage | 62.6% (239/382) |
| Districts without GPS (from file) | 239 |
| GPS metadata (source, confidence, verification) | **Absent** |

**GPS Precision Levels** (defined in V4 but not stored in data):

| Level | Description | Threshold |
|-------|-------------|-----------|
| HIGH | High precision | <50m |
| MEDIUM | Medium precision | 50-500m |
| LOW | Low precision | >500m |
| UNKNOWN | No precision data | N/A |

**Critical Gap:** GPS metadata fields (source, confidence level, verification status) are absent from all data files. The `neighborhood_gps.json` file only covers 2 cities (Douala, Yaoundé) with 5 neighborhoods.

---

## 6. Neighborhood Inventory

**Source :** `knowledge_unified/geography/neighborhoods.json` (verified)

| City | Neighborhood Count | Confirmed |
|------|-------------------|-----------|
| Yaoundé | ~111 | `knowledge_unified/geography/neighborhoods.json:18` |
| Douala | ~104 | `knowledge_unified/geography/neighborhoods.json:19` |
| Buea | ~51 | `knowledge_unified/geography/neighborhoods.json:19` |
| Bafoussam | 33 | `knowledge_unified/geography/neighborhoods.json:19` |
| Limbe | ~41 | `knowledge_unified/geography/neighborhoods.json:19` |
| Kribi | 12 | `knowledge_unified/geography/neighborhoods.json:19` |
| Maroua | 15 | `knowledge_unified/geography/neighborhoods.json:19` |
| Bamenda | 10 | `knowledge_unified/geography/neighborhoods.json:19` |
| Garoua | 6 | `knowledge_unified/geography/neighborhoods.json:19` |
| Nkongsamba | 3 | `knowledge_unified/geography/neighborhoods.json:19` |
| **Total** | **382** | |

---

## 7. Normalization & Levenshtein Threshold

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-RULE-ENGINE-V2-002

| Parameter | Value |
|-----------|-------|
| Algorithm | Levenshtein distance |
| Max threshold | 3 |
| Fallback | Supabase `location_synonyms` table |
| Source | `location_normalizer.py` |

---

## 8. Knowledge Extraction Patterns

**Source :** `RECOVERED_KNOWLEDGE.md` KNW-RULE-ENGINE-V2-002, `location_normalizer.py`

| Pattern | Example | Purpose |
|---------|---------|---------|
| `à [lieu]` | "à Bastos" | Direct location mention |
| `dans [lieu]` | "dans Bonamoussadi" | Enclosed location |
| `quartier [lieu]` | "quartier Akwa" | Explicit neighborhood |

**Location Extraction Confidence Formula:**
```
Confidence = min(100, occurrences × 20)
```
After 5 mentions, confidence reaches 100%.

---

## 9. City Affinity Rules

**Source :** `GEO_REFERENCE_MODEL_CAMEROON_V4.md` (analysé in reaudit), `city-affinity-matrix.md`

**Rejection Pairs (documented in V4):**

| City | Rejection Target | Rule |
|------|-----------------|------|
| Yaoundé | ↛ Obala | Incompatible zone |
| Douala | ↛ Edéa | Different city, low affinity |
| Buea | ↛ Limbe | Different city, low affinity |

**Affinity Matrix Coverage:**
- Yaoundé: 74 documented pairs
- Douala: 51 documented pairs
- Other 8 priority cities: **0 pairs seeded**

---

## 10. V4 Geo Scoring Formula

**Source :** `GEO_REFERENCE_MODEL_CAMEROON_V4.md` §5.2, reaudit GOLD §3.1

| Component | Weight | Description |
|-----------|--------|-------------|
| Affinity Score | 40% | City/neighborhood affinity match |
| Cluster Compatibility | 25% | Cluster/zone compatibility |
| Product Compatibility | 20% | Property type match |
| GPS Adjustment | 15% | GPS coordinate proximity |

**Formula:** `Geo_Score = (Affinity × 0.40) + (Cluster × 0.25) + (Product × 0.20) + (GPS × 0.15)`

---

## 11. Visibility Levels

**Source :** `09-GEOLOCATION-REFERENCE.md` (6 visibility levels defined)

| Level | Name | Description |
|-------|------|-------------|
| 1 | PUBLIC | Visible to all users |
| 2 | PRIVATE | Restricted visibility |
| 3 | INTERNAL | Internal use only |
| 4 | CONFIDENTIAL | Confidential |
| 5 | SECRET | Secret |
| 6 | TOP_SECRET | Maximum restriction |

*Note: These visibility levels are defined in the geolocation reference but their implementation status in data is unverified.*

---

## 12. district_hierarchy.json — Coverage

**Source :** `knowledge_unified/geography/aliases.json:35-40`, reaudit GOLD §1.8

Only **4 entries** covering **Buea only**:

| Parent District | Sub-Districts |
|-----------------|---------------|
| Muea | Lower Muea, Upper Muea |
| Great Soppo | Small Soppo-Wonganga, Small Soppo-Woteke, Small Soppo-Wovila |
| Government Residential Area | Federal Quarters, Clerk's Quarter, Old-Government Station |
| Bolifamba | Lower Bolifamba |

**Zero hierarchy data** for Douala, Yaoundé, or any other city.

---

## 13. Aliases & Landmarks — Documented Gaps

**Source :** `knowledge_unified/geography/cities.json`, `knowledge_unified/geography/aliases.json`, reaudit GOLD §1.3

| Artifact | Status | Detail |
|----------|--------|--------|
| City aliases | ✅ Present | 10 cities, ~5 variants each in `cities.json` |
| City typos | ✅ Present | 10 cities, ~4 typos each in `cities.json` |
| District aliases | ✅ Partial | 14 pairs in `aliases.json` (Douala-focused) |
| **Landmarks stored** | ❌ **Zero** | No landmark data exists in any file |
| **Nearby district links** | ❌ **Zero** | No proximity/neighbor relationships stored |
| **Aliases in main geography JSON** | ❌ **Zero** | `neighborhoods.json` has no alias fields per district |

---

## 14. City Priority Order Discrepancies

**Source :** reaudit GOLD §1.5, `city-affinity-matrix.md`, `cities.json`, `system_prompt_v1.md`

Four different orderings exist across documents:

| Source | Order | Includes Ngaoundéré/Bertoua? |
|--------|-------|------------------------------|
| `knowledge_unified/geography/cities.json` | Yaoundé(1)→Douala(2)→Bamenda(3)→Bafoussam(4)→Buea(5)→Kribi(6)→Nkongsamba(7)→Maroua(8)→Limbe(9)→Garoua(10) | No |
| `system_prompt_v1.md` | Douala(1)→Yaoundé(2)→Bafoussam(3)→Bamenda(4)→Buea(5)→Limbe(6)→Kribi(7)→Nkongsamba(8)→Garoua(9)→Maroua(10) | No |
| `city-affinity-matrix.md` | Yaoundé, Douala, Bafoussam, Kribi, Limbe, Garoua, Bamenda, Maroua, **Ngaoundéré, Bertoua** | **Yes** — Ngaoundéré and Bertoua replace Nkongsamba and Buea |
| `GEO_REFERENCE_MODEL_CAMEROON_V4.md` | Douala, Yaoundé, Bafoussam, Bamenda, Buea, Limbe, Kribi, Garoua, Maroua, Nkongsamba | No (different order from both) |

---

## 15. Critical Gaps Summary

**Source :** reaudit GOLD, file analysis

| ID | Gap | Impact | Source |
|----|-----|--------|--------|
| GG-GPS-META-001 | GPS metadata (source, confidence, verification) absent | Cannot assess GPS reliability | `neighborhood_gps.json` |
| GG-SUBZONE-001 | Neighborhood sub-zones (e.g., Bastos Haut) used in V4 logic but not in data | V4 rules reference non-existent data | `GEO_REFERENCE_MODEL_CAMEROON_V4.md` |
| GG-NGAOUNDERE-001 | Ngaoundéré and Bertoua listed as primary in affinity matrix with zero district data | Matching cannot operate on these cities | `city-affinity-matrix.md:22` |
| GG-HIER-001 | SUBDIVISION and ZONE levels declared but empty | Cannot route by zone or subdivision | `GEO_MODEL_ALIGNMENT_PLAN.md:54-55` |
| GG-LANDMARK-001 | Zero landmarks stored | No POI-based matching possible | All geography files |
| GG-NEARBY-001 | Zero nearby district links | Cannot score neighboring districts | All geography files |
| GG-ALLN-001 | `all_neighborhoods.json` is empty | Aggregated view unavailable | `all_neighborhoods.json` |
| GG-CITY-ORDER-001 | 4 different city priority orderings | Inconsistent city ranking | Cross-document analysis |

---

## 16. Gold Knowledge Register — Geography

| ID (GE-GOLD-) | Concept | Description | Source | Confidence |
|--------------|---------|-------------|--------|------------|
| GE-GEO-001 | Territorial Hierarchy (10 levels) | Pays→Région→Département→Arrondissement→Commune→Ville→Quartier→Sous-Quartier→Point de repère→GPS | `09-GEOLOCATION-REFERENCE.md` §1.1 | HIGH |
| GE-GEO-002 | LAWIM Zones | Functional groupings for agent routing | LAWIMA `agents` table | HIGH |
| GE-GEO-003 | 10 Priority Cities | Yaoundé(1) through Garoua(10) with priority_rank | `cities.json:8-103` | VERY HIGH |
| GE-GEO-004 | 18 Secondary Cities | Ebolowa through Mutengene with zero district data | `cities.json:104-109` | VERY HIGH |
| GE-GEO-005 | GPS Coverage 62.6% | 239/382 districts have GPS | Reaudit §1.7 | VERY HIGH |
| GE-GEO-006 | Neighborhood Inventory (382) | Counts per city from neighborhoods.json | `neighborhoods.json:18-22` | VERY HIGH |
| GE-GEO-007 | Levenshtein Threshold | Max distance 3 for normalization | `location_normalizer.py` | HIGH |
| GE-GEO-008 | Extraction Patterns | `à [lieu]`, `dans [lieu]`, `quartier [lieu]` | `location_normalizer.py` | HIGH |
| GE-GEO-009 | Confidence Formula | `min(100, occurrences × 20)` | `location_normalizer.py` | HIGH |
| GE-GEO-010 | City Affinity Rejection Pairs | Yaoundé↛Obala, Douala↛Edéa, Buea↛Limbe | `GEO_REFERENCE_MODEL_CAMEROON_V4.md` §7 | HIGH |
| GE-GEO-011 | GPS Precision Levels | HIGH(<50m), MEDIUM(50-500m), LOW(>500m), UNKNOWN | `GEO_REFERENCE_MODEL_CAMEROON_V4.md` §4 | HIGH |
| GE-GEO-012 | V4 Geo Scoring Formula | 40% Affinity + 25% Cluster + 20% Product + 15% GPS | `GEO_REFERENCE_MODEL_CAMEROON_V4.md` §5.2 | VERY HIGH |
| GE-GEO-013 | 6 Visibility Levels | PUBLIC through TOP_SECRET | `09-GEOLOCATION-REFERENCE.md` | MEDIUM |
| GE-GEO-014 | district_hierarchy.json Scope | Only covers Buea (4 entries) | `aliases.json:35-40` | VERY HIGH |
| GE-GEO-015 | Zero District Aliases in main JSON | `neighborhoods.json` has no alias fields | `neighborhoods.json` | VERY HIGH |
| GE-GEO-016 | Zero Landmarks | No landmark data stored | All geography files | VERY HIGH |
| GE-GEO-017 | Zero Nearby District Links | No proximity relationships stored | All geography files | VERY HIGH |
| GE-GEO-018 | City Priority Discrepancy | 4 different orderings across docs | Reaudit §1.5 | VERY HIGH |
| GE-GAP-001 | GPS metadata absent | No source/confidence/verification fields | `neighborhood_gps.json` | VERY HIGH |
| GE-GAP-002 | Sub-zones not in data | Bastos Haut, etc. referenced in V4 but absent | `GEO_REFERENCE_MODEL_CAMEROON_V4.md` | HIGH |
| GE-GAP-003 | Ngaoundéré/Bertoua no data | Listed as primary in affinity matrix but zero district data | `city-affinity-matrix.md:22` | VERY HIGH |
| GE-GAP-004 | SUBDIVISION/ZONE empty | Enum declared, zero seeded data | `GEO_MODEL_ALIGNMENT_PLAN.md:54-55` | VERY HIGH |

---

## 17. Source File Inventory

| File | Path (in knowledge_unified) | Status |
|------|---------------------------|--------|
| cities.json | `knowledge_unified/geography/cities.json` | ✅ Validated (v3.0) |
| neighborhoods.json | `knowledge_unified/geography/neighborhoods.json` | ✅ Validated (v2.0) |
| aliases.json | `knowledge_unified/geography/aliases.json` | ✅ Validated (v3.0) |
| proximity_rules.json | `knowledge_unified/geography/proximity_rules.json` | ✅ Validated (v1.0) |
| Reaudit GOLD | `reports/lawim_heritage_gold/GEOGRAPHY_QUALIFICATION_MATCHING_REAUDIT.md` | ✅ Validated |
| Recovered Knowledge | `reports/lawim_heritage_gold/RECOVERED_KNOWLEDGE.md` | ✅ Validated |

---

*Gold document — validated knowledge only. All gaps explicitly documented with sources.*
