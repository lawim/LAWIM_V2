# GEOGRAPHY RECOVERY REPORT — LAWIM H0.4

**Date:** 15 July 2026
**Source:** 09-GEOLOCATION-REFERENCE.md, knowledge_unified/geography/

---

## What Was Recovered

| Concept | Details | Source |
|---------|---------|--------|
| 9-level territorial hierarchy | Pays→Région→Département→Arrondissement→Commune→Ville→Quartier→Secteur→Point de repère (+ GPS) | 09-GEOLOCATION-REFERENCE Ch13 |
| 6 precision levels | Niveau 1 (Pays) à Niveau 6 (Coordonnées GPS) | 09-GEOLOCATION-REFERENCE Ch6 |
| V4 Geo Scoring Formula | Affinité(40%) + Cluster(25%) + Produit(20%) + GPS(15%) | GEO_REFERENCE_MODEL_V4 |
| 35 absolute geo rules | Never delete active city, never modify without historization, etc. | 09-GEOLOCATION-REFERENCE |
| Geo Engine responsibilities | 12 responsibilities defined | 09-GEOLOCATION-REFERENCE |
| 125 neighborhood affinity pairs | 74 Yaoundé + 51 Douala | knowledge_unified/ |
| 4 rejection pairs + interdictions | Soa↛Obala, Soa↛Bafia, Yaoundé↛Soa, Douala↛Dibombari | city-affinity-matrix |
| 3 mobility modes | STRICT, FLEXIBLE, VERY_FLEXIBLE | knowledge_unified/ |
| 5 proximity scoring levels | Exact→Accepted→Neighboring→Distant→Incompatible | knowledge_unified/ |
| 6 V4 rejection rules | From automatic(0) to weak(20-30) to medium(40-60) | GEO_REFERENCE_MODEL_V4 |
| Location extraction patterns | `à [lieu]`, `dans [lieu]`, `quartier [lieu]` | location_normalizer.py |
| 6 fuzzy location expressions | barrage, carrefour, derrière station, axe principal, etc. | location_normalizer.py |

## Gaps Still Open

| Gap | Impact |
|-----|--------|
| SUBDIVISION and ZONE levels declared but 0 entries | Cannot route by zone |
| 8/10 cities have 0 affinity pairs | Matching cross-city limited |
| Only 2/10 priority cities have GPS | Geographic scoring incomplete |
| GPS metadata (source, confidence) absent | Cannot assess GPS reliability |
| 0 landmarks stored | Missing location reference points |
| Zone routing non-functional | Agent assignment by zone broken |

**Source:** docs/lawim_heritage_gold/GEOGRAPHY_MODEL.md + knowledge_unified/geography/*.json
