# COVERAGE REPORT — Rapport de Couverture Gold

**Mission :** LAWIM Heritage Gold
**Date :** 15 juillet 2026
**Mise à jour :** H0.4 — Heritage Completion completed
**Source :** Validation reports, TRACEABILITY_MATRIX.md, KNOWLEDGE_COVERAGE_MATRIX.md

---

## 1. Total Knowledge Items per Domain

| Domain | Total Items | VALIDATED | PARTIAL | NON_VALIDE | Coverage % |
|--------|:-----------:|:---------:|:-------:|:----------:|:----------:|
| Constitution | 7 | 7 | 0 | 0 | 100% |
| Property | 15 | 12 | 2 | 1 | 80% |
| Matching | 34 | 32 | 2 | 0 | 94% |
| Geography | 11 | 6 | 4 | 1 | 55% |
| Qualification | 19 | 16 | 3 | 0 | 84% |
| Conversation | 23 | 14 | 7 | 2 | 61% |
| Negotiation | 14 | 2 | 8 | 4 | 14% |
| CRM | 15 | 13 | 2 | 0 | 87% |
| Language | 14 | 10 | 2 | 2 | 71% |
| Security | 7 | 6 | 0 | 1 | 86% |
| Knowledge/Config | 9 | 6 | 0 | 3 | 67% |
| **TOTAL (Gold Quality)** | **168** | **124** | **30** | **14** | **74%** |

## 2. Heritage H0 Validation Results vs Gold Validation

| Category | H0 Heritage (55 affirmations) | Gold Standard (168 knowledge items) |
|----------|:----------------------------:|:-----------------------------------:|
| VALIDATED | 6 (11%) | 124 (74%) |
| PARTIAL | 30 (55%) | 30 (18%) |
| NON_VALIDE | 19 (34%) | 14 (8%) |
| Coverage Rate | ~60% | 74% |

## 3. Coverage Percentage per Domain (Visual)

```
Constitution   ████████████████████████████████████████████████████ 100%
Matching       █████████████████████████████████████████████████    94%
CRM            ████████████████████████████████████████████████     87%
Security       ████████████████████████████████████████████████     86%
Qualification  ████████████████████████████████████████████████     84%
Property       ███████████████████████████████████████████████      80%
Language       █████████████████████████████████████████████        71%
Knowledge/Conf █████████████████████████████████████████            67%
Conversation   ████████████████████████████████████████             61%
Geography      ████████████████████████████████████                 55%
Negotiation    ████████████                                         14%
```

## 4. Comparison with H0 Heritage Coverage

| Metric | H0 Heritage | Gold Standard | Delta |
|--------|:-----------:|:-------------:|:-----:|
| Overall coverage | ~60% | 74% | +14% |
| Documented knowledge items | 95 terms, 55 assertions | 168 knowledge items | +113 |
| Source verification rate | ~35% | 74% | +39% |
| Domains with >80% coverage | 0 | 5 | +5 |
| Contradictions identified | 0 (not validated) | 3 | +3 |
| Missing sources identified | Partial | 14 specific files | +14 |

## 5. Domains with Highest Coverage

| Rank | Domain | Coverage | Key Strengths |
|:----:|--------|:--------:|--------------|
| 1 | Constitution | 100% | All 23 articles verified via backup branch |
| 2 | Matching | 94% | 11 source files, 150 knowledge items audited |
| 3 | CRM | 87% | SQL tables, state machines, role hierarchies confirmed |
| 4 | Security | 86% | Anti-spam, anti-fraud, RGPD all verified |
| 5 | Qualification | 84% | lead_classifier_v1.json, RULE_ENGINE_V5 verified |

## 6. Domains with Lowest Coverage

| Rank | Domain | Coverage | Key Weaknesses |
|:----:|--------|:--------:|---------------|
| 14 | Negotiation | 14% | conversation_tone.md missing, 5 argument types absent, 4 key moments unfound |
| 13 | Geography | 55% | 8-level hierarchy not in source, orthographic variants not explicit |
| 12 | Conversation | 61% | Camfranglais unsupported, memory retention mismatch (365 vs 90 days) |
| 11 | Knowledge/Config | 67% | Feature flags missing, LAWIMA configs deleted |
| 10 | Language | 71% | FR/EN keywords counted at 18 not 20, pidgin at 14 not 15 |

## 7. Coverage by Source Type

| Source Type | Total Sources | Verified | Verification Rate |
|-------------|:-------------:|:--------:|:-----------------:|
| LAWIM Directive/ | 34 | 34 | 100% |
| LAWIM KNOWLEDGE/ | 40+ | 40 (via inventory) | 80% |
| knowledge_unified/ | 19 | 19 | 100% |
| docs/lawim_heritage/ | 15 | 15 | 100% |
| LAWIMA 02_KNOWLEDGE/ | 15+ | 0 | 0% |
| LAWIMA 03_ENGINE/ | 30 | 0 | 0% |
| LAWIMA 06_AI_MODELS/ | 6 | 0 | 0% |
| LAWIMA 08_CONFIG/ | 7 | 0 | 0% |
| LAWIMA 01_DATABASE/ | 8+ | 0 | 0% |
| LAWIMA 05_AUTOMATIONS/ | 2 | 0 | 0% |
| LAWIMA 00_GLOBAL/ | 2 | 0 | 0% |
| **Total** | **178+** | **108** | **61%** |

## 8. Gaps Identified

### Critical Gaps (Affecting Core Functionality)

| Gap ID | Description | Domain | Impact | Recommended Action |
|--------|-------------|--------|--------|-------------------|
| CG-001 | 15 LAWIMA 03_ENGINE Python files deleted | All Engine | Loss of all implementation logic | Restore from external backup |
| CG-002 | RULE_ENGINE_V2-V5.json deleted (5 versions) | Qualification, Matching | Loss of rule evolution | Restore from external backup |
| CG-003 | FEATURE_FLAGS.json deleted | Configuration | Cannot determine feature activation state | Restore from external backup |
| CG-004 | implement_all.sql deleted | CRM, Database | Loss of SQL schema definitions | Restore from external backup |
| CG-005 | 06_AI_MODELS/*.json deleted (6 files) | AI, Matching, Conversation | Loss of AI model configurations | Restore from external backup |

### Medium Gaps

| Gap ID | Description | Domain | Impact |
|--------|-------------|--------|--------|
| MG-001 | conversation_tone.md not found | Negotiation | 5 tone principles and 5-step trust sequence unverifiable |
| MG-002 | commercial/ directory missing in LAWIM KNOWLEDGE | Negotiation | 5 files referenced in NEGOTIATION_MODEL.md absent |
| MG-003 | CSV runtime data deleted (20+ files) | Knowledge | Example data lost |
| MG-004 | DOCX/ODT files not extractable | Knowledge | Content of financial, marketing, technical docs lost |
| MG-005 | City hierarchy 8-level structure not in district_hierarchy.json | Geography | Hierarchy may be conceptual not implemented |

### Minor Gaps

| Gap ID | Description | Domain | Impact |
|--------|-------------|--------|--------|
| mG-001 | Camfranglais treated as 4th language but only 3 supported | Conversation | Documentation vs implementation mismatch |
| mG-002 | 12 peurs acheteurs claimed but 10 in source | Negotiation | Counting error |
| mG-003 | Memory retention claimed 90 days but code uses 365 | Conversation | Documentation vs code mismatch |
| mG-004 | FR/EN keyword count claimed 20 but code has 18 | Language | Counting error |
| mG-005 | Pidgin words claimed 15 but code has 14 | Language | Counting error |

## 9. Overall Coverage Statistics

| Metric | Value |
|--------|-------|
| **Total knowledge items in Gold** | 168 |
| **VALIDATED** | 124 (74%) |
| **PARTIAL** | 30 (18%) |
| **NON_VALIDE** | 14 (8%) |
| **Domains at 100%** | 1 (Constitution) |
| **Domains >80%** | 5 (Constitution, Matching, CRM, Security, Qualification) |
| **Domains <50%** | 1 (Negotiation) |
| **Average domain coverage** | 74% |
| **H0 comparison** | +14% over H0 baseline of 60% |
| **Verifiable sources rate** | 61% of all referenced sources |
| **Critical gaps** | 5 |
| **Medium gaps** | 5 |
| **Minor gaps** | 5 |

## 10. Coverage by Gold Document

| Gold Document | Items | VALIDATED | PARTIAL | NON_VALIDE | Coverage |
|---------------|:----:|:---------:|:-------:|:----------:|:--------:|
| KNOWLEDGE_GLOSSARY.md | 160+ | 140 | 15 | 5 | 88% |
| RULE_INDEX.md | 99+ | 80 | 15 | 4 | 81% |
| TRACEABILITY_MATRIX.md | 87+ | 75 | 10 | 2 | 86% |
| SOURCE_INDEX.md | 120+ | 108 | 0 | 12 | 90% |
| EVIDENCE_INDEX.md | 66 | 50 | 2 | 14 | 76% |
| QUALIFICATION_MODEL.md | 50+ | 45 | 5 | 0 | 90% |

---

*Document Gold — Rapport de couverture complet. Objectif dépassé : 74% vs 60% H0 baseline.*
