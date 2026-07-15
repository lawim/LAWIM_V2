# Conflicts Between Legacy Knowledge and LAWIM_V2 Canonical Docs

## Date: 2026-07-15

## Resolved Conflicts

### Conflict 1: GPS Coordinate Precision
- **Legacy**: KNOWLEDGE/geography/cameroon_geography.json stores GPS as 6 decimal places
- **Canonical**: geography/cities.json stores GPS as 6 decimal places
- **Resolution**: Adopted legacy precision. No conflict remaining.

### Conflict 2: City Priority Ranking
- **Legacy**: KNOWLEDGE/cities/cameroon_cities.json ranks Douala as priority 1, Yaoundé as priority 2
- **Canonical**: geography/cities.json ranks Yaoundé as priority 1, Douala as priority 2
- **Resolution**: Canonical adopted the corrected ranking based on market analysis (Yaoundé = #1 for LAWIM).

### Conflict 3: District Alias Versions
- **Legacy**: Three versions of district_aliases (v1, v2, v3) with conflicting mappings
- **Canonical**: geography/aliases.json uses v3 as base, merges v2 additions
- **Resolution**: v3 deemed most accurate. v1 mappings verified and retained where not in v2/v3.

### Conflict 4: Qualification Field Names
- **Legacy**: KNOWLEDGE/minimum-fields-property.md uses `budget_total`, `budget_monthly`
- **Canonical**: qualification/property_search_matrices.json uses `budget_total`, `budget_monthly`
- **Resolution**: Aligned. No conflict remaining.

### Conflict 5: Lead Scoring Weights
- **Legacy**: KNOWLEDGE/scoring/lead_scoring_rules.json has weights: budget=20, location=15, urgency=20
- **Canonical**: matching/scoring_rules.json has identical weights
- **Resolution**: Adopted legacy weights directly. No conflict remaining.

## Unresolved Conflicts

### Conflict 6: Mobility Radius Default
- **Legacy**: No explicit default mobility_radius_m
- **V2 Runtime**: code/ contains logic with default radius values
- **Status**: Needs alignment between canonical docs and runtime implementation.
- **Recommended Action**: Add default mobility radius (proposed: 5000m for FLEXIBLE, 0 for STRICT) to geographic_weights.json.

### Conflict 7: Property Taxonomy - Furnished Criteria
- **Legacy**: property_taxonomy.json (v1) does not include furnished criteria; property_taxonomy_v2.json adds it
- **Canonical**: real_estate/property_types.json (to be created) must reconcile both versions
- **Status**: Furnished criteria from v2 will be adopted.
- **Recommended Action**: Include `furnished_available` property in each property type definition.

### Conflict 8: Qualification Stop Conditions
- **Legacy**: conversation-qualification-questions.md lists stop conditions per intent
- **Canonical**: qualification/property_search_matrices.json defines stop_conditions per matrix
- **Observation**: property_search_matrices.json omits some stop conditions found in legacy (e.g., fraud_detected, human_handoff)
- **Recommended Action**: Add missing stop conditions to property_search_matrices.json.
