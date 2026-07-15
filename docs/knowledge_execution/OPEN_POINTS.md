# OPEN POINTS — Knowledge Execution Architecture (H1)

**Mission:** LAWIM H1 — Knowledge Execution Architecture
**Date:** 2026-07-15
**Status:** Open points documented for future resolution

---

## 1. Heritage Gold Divergences Carried Forward

| ID | Heritage Gold Reference | Issue | Impact | Proposed Resolution |
|----|------------------------|-------|--------|-------------------|
| OP-001 | GEO-001 (9-level hierarchy) | Source backup shows 9 levels, current hierarchy has 8 levels | Geographic resolution may fail for level 9 locations | Align to 8 levels for implementation; document level 9 for future expansion |
| OP-002 | CONV-013 (memory retention) | Documented 90 days, code implements 365 days | Consistency gap between spec and implementation | Adopt 365 days (code behavior) in execution model |
| OP-003 | MATCH scoring (V1 vs V5) | No documented conversion rule between V1 (0-100) and V5 (0-1.0) thresholds | Risk of inconsistent lead classification | Define conversion formula: V5 = V1 / 100 |
| OP-004 | MATCH-001 vs MATCH-002 (dimension weights) | V1 dimensions (city=30%) differ from DE dimensions (Type=25%) | Inconsistent matching behavior across versions | Use DE dimensions (MATCH-002) as canonical; V1 weights for backward compatibility |
| OP-005 | LANG-012 (pidgin keywords) | 12 in source vs 14 in detector | Partial detection coverage | Use 14 keywords (code behavior) |
| OP-006 | G-KNOW-001 (Feature flags) | Feature flags definitively lost | Cannot restore original configuration | Document 4 ON / 15 OFF flags as known limitation |
| OP-007 | G-KNOW-006 (Ancienne structure) | Legacy directory structure definitively lost | Cannot reference deleted sources | Accept as permanent gap |

## 2. Architecture Design Decisions

| ID | Decision | Rationale | Alternatives Considered |
|----|----------|-----------|------------------------|
| OP-101 | NBA Engine defined as separate component within Decision Engine | NBA requires cross-domain awareness; separation enables independent optimization | Could embed NBA in each domain engine — rejected due to cross-domain coupling |
| OP-102 | Progressive Search Expansion has 9 levels (L0-L8) | Covers exact match to professional search per Heritage Gold | Could use 5 levels — rejected as insufficient granularity |
| OP-103 | Dual scoring system (V1 integer + V5 float) preserved | Heritage Gold contains both; migration requires both systems | Could drop V1 — rejected due to backward compatibility requirements |
| OP-104 | 8-level geographic hierarchy adopted | Matches current reference implementation | 9-level hierarchy from backup documented for future |
| OP-105 | Event privacy model uses 4 levels (public/internal/confidential/restricted) | Supports RGPD compliance and operational security | Simpler public/private model rejected as insufficient |
| OP-106 | Consent model requires double consent (demandeur + holder) | Matches Heritage Gold anonymity principle | Single consent rejected — violates anonymity requirement |

## 3. Missing Knowledge (Irrecoverable)

| ID | Missing Item | Source | Impact | Mitigation |
|----|-------------|--------|--------|------------|
| OP-201 | 27 engine Python files (LAWIMA/03_ENGINE/) | Deleted from source backup | Business logic extracted only via descriptions | Documented in SOURCE_INDEX |
| OP-202 | 6 configuration files | Deleted | Feature flag details lost | Feature flags reconstructed from secondary sources |
| OP-203 | 20+ database tables | Deleted | Complete table schemas lost | Schema reconstructed from implement_all.sql |
| OP-204 | 2 SQL scripts | Deleted | Migration scripts lost | Logic extracted from remaining SQL |

## 4. Future Implementation Risks

| ID | Risk | Likelihood | Mitigation |
|----|------|-----------|------------|
| OP-301 | Rule conflict resolution may produce unexpected results when multiple engines claim same trigger | Medium | Priority matrix defined in GLOBAL_EXECUTION_ARCHITECTURE.md; conflict resolver tests required |
| OP-302 | NBA Engine may produce infinite loops (action → state change → same action) | Low | Loop detection with max iteration count defined |
| OP-303 | Event volume may exceed storage capacity at scale | Medium | Retention policy per privacy level; volume estimation in EVENT_EXECUTION_ARCHITECTURE.md |
| OP-304 | Geographic resolution quality varies by city (GPS coverage gaps) | High | Documented in GEOGRAPHIC_DATA_QUALITY_MODEL.md |
| OP-305 | Dual scoring system (V1 + V5) increases maintenance burden | Medium | Migration plan to single system recommended post-H1 |

## 5. Validation Exclusions

| ID | Item | Reason for Exclusion |
|----|------|---------------------|
| OP-401 | Feature flag values beyond documented 4 ON / 15 OFF | Feature flags definitively lost (G-KNOW-001) |
| OP-402 | Exact SQL table column types | 20+ tables deleted; schema reconstructed from implement_all.sql |
| OP-403 | Old LAWIMA engine business logic details | 27 Python files deleted; logic extracted from descriptions only |

## 6. Architecture Decisions Requiring Business Validation

| ID | Item | Type |
|----|------|------|
| OP-501 | NBA priority matrix weights | ARCHITECTURE_DECISION |
| OP-502 | Consent SLA defaults (48h/24h-30d/90d) | ARCHITECTURE_DECISION |
| OP-503 | Phone masking pattern | ARCHITECTURE_DECISION |
| OP-504 | Data retention durations | LEGAL_VALIDATION_REQUIRED |
| OP-505 | Commercial scripts | HUMAN_VALIDATION_REQUIRED |
| OP-506 | Qualification matrices | **RESOLVED** — Integrated from `docs/lawim_heritage_gold/qualification_matrices/`. Matrices loaded from `qualification_matrices.json`, fields from `field_dictionary.json`, readiness from `readiness_rules.json`, questions from `question_rules.json`, matching from `matching_semantics.json`. See QUALIFICATION_MATRIX_CONTRACT.md §0, READINESS_MODEL.md §0 |

---

*Document Gold — Open points for H1 Knowledge Execution Architecture*
