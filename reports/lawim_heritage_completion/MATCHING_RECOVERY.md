# MATCHING RECOVERY REPORT — LAWIM H0.4

**Date:** 15 July 2026
**Source:** 04-DECISION-ENGINE-REFERENCE.md, 04-MATCHING-REFERENCE.md, knowledge_unified/matching/

---

## What Was Recovered

| Concept | Details | Source |
|---------|---------|--------|
| 60+ matching rules | Complete rule set covering all versions | 04-DECISION-ENGINE |
| 16 per-type weightings | Residential Simple, Apartment, Furnished Apartment, House, Villa, Duplex, Building, Land, Agricultural, Commercial/Industrial Land, Shop, Office, Warehouse, Hotel, Agricultural Property, Industrial/Logistics, Mixed | 04-DECISION-ENGINE Ch42-58 |
| V1 scoring (5 dims) | City(30%), Neighborhood(25%), Budget(25%), Type(15%), Title(5%) | property_matching_v1.json |
| V4 scoring | Location+40, Budget tiers, Type+25, Cap 100 | property_matcher_supabase.py |
| V5 scoring | Location+40, Budget exact+50, <10%+35, <30%+20, <50%+10, Type+10, Cap 100 | property_matcher_v5.py |
| Star rating | ≥80=⭐⭐⭐⭐⭐, ≥60=⭐⭐⭐⭐, ≥40=⭐⭐⭐, ≥20=⭐⭐, <20=⭐ | property_matcher_v5.py |
| 4 compatibility levels | Critical, Functional, Comfort, Preferential | 04-DECISION-ENGINE Ch9 |
| 6 DE dimensions | Type(25%), Operation(20%), Budget(15%), Location(15%), Critical(15%), Recommended(10%) | 04-DECISION-ENGINE Ch26 |
| Transaction Success Score | 8 indicators (30/15/10/10/10/10/10/5) | 04-DECISION-ENGINE Ch90 |
| Trust Index | 5 levels (Très élevé→Très faible) | 04-DECISION-ENGINE Ch91 |
| 12 decision actions | Question→Closing | 04-DECISION-ENGINE Ch86 |
| Decision thresholds | 98%=immediate, 82%=if no better, 55%=hold, 25%=never | 04-DECISION-ENGINE Ch92 |
| All rematching triggers | Requester-side(7), Property-side(9), Holder-side(5), System-side(4) | 04-DECISION-ENGINE Ch65 |
| Learning from refusals | 3 refusals = priority change, dossier-specific adjustments | 04-DECISION-ENGINE Ch19,59,68 |
| Non-compensation rule | Land≠villa, pool≠incompatible budget, hotel≠wrong operation | 04-DECISION-ENGINE Ch61 |
| 10-step algorithm | Load→Verify→Select→Eliminate→Score→Rank→Propose→Decision→Learn→Recalculate | 04-DECISION-ENGINE |
| Reasoning pipeline (7 steps) | detect_intent→detect_city→detect_neighborhood→detect_budget→classify_lead→match_properties→rank_results | reasoning_rules_v1.json |
| Confidence threshold | 0.70 (70%) for automatic decisions | reasoning_rules_v1.json |
| Market Tension Index | Per city×neighborhood×type×operation | 04-DECISION-ENGINE Ch96 |
| Market Memory | Average sales time, rental time, time to first visit, etc. | 04-DECISION-ENGINE Ch95 |
| Unified V2.0 dimensions (7) | Geographic(20%), Mobility(20%), Type(15%), Budget(10%), Standing(10%), Services(10%), Freshness(15%) | knowledge_unified/matching/ |
| Freshness bonuses | 0-3d=+15, 4-7d=+12, 8-15d=+8, 16-30d=+4, >30d=0 | knowledge_unified/matching/ |

**Source:** docs/lawim_heritage_gold/MATCHING_MODEL.md + docs/lawim_heritage_gold/RULE_INDEX.md
