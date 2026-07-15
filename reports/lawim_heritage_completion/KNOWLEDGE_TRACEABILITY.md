# KNOWLEDGE TRACEABILITY — LAWIM H0.4

**Date:** 15 July 2026
**Principle:** Every knowledge item traced to its source with confidence level

---

## Source-to-Knowledge Mapping

| Source File | Knowledge Domain | Items Extracted | Confidence |
|-------------|-----------------|----------------|------------|
| 05-WORKFLOW-REFERENCE.md | All workflows | 21 workflows, ~95 states, SLA, NBA | HIGH |
| 04-DECISION-ENGINE-REFERENCE.md | Matching | 60+ rules, 16 types, TSS, thresholds | HIGH |
| 04-MATCHING-REFERENCE.md | Matching | Core engine principles | HIGH |
| 03-CONVERSATION-REFERENCE.md | Conversation | Design, qualification, anonymity | HIGH |
| 48-LAWIM-SALES-PLAYBOOK.md | Negotiation | Sales, objections, profiles | HIGH |
| 08-ROLE-REFERENCE.md | CRM | Roles, permissions, trust | HIGH |
| 09-GEOLOCATION-REFERENCE.md | Geography | Hierarchy, scoring, rules | HIGH |
| 30-I18N-L10N-REFERENCE.md | Language | Internationalization | HIGH |
| 30A-BUSINESS-DICTIONARY-REFERENCE.md | Language | Business terms | HIGH |
| 30C-LANGUAGE-DETECTION-REFERENCE.md | Language | Detection rules | HIGH |
| 30D-MULTILINGUAL-SEARCH-REFERENCE.md | Language | Multi-search | HIGH |
| knowledge_unified/geography/ | Geography | Cities, neighborhoods, aliases | HIGH |
| knowledge_unified/matching/ | Matching | Dimensions, scoring, exclusions | HIGH |
| knowledge_unified/qualification/ | Qualification | Intentions, typologies, matrices | HIGH |
| knowledge_unified/language/ | Language | Expressions, variants, intents | HIGH |
| knowledge_unified/commercial/ | Negotiation | Tone, closing, objections, techniques, follow-up | HIGH |
| knowledge_unified/real_estate/ | Property | Property types | HIGH |
| docs/lawim_heritage/ (15 files) | All domains | Heritage baseline | MEDIUM |
| docs/lawim_heritage_gold/ (20+ files) | All domains | Gold standard | HIGH |

## Confidence Distribution

| Level | Count | % |
|-------|-------|---|
| HIGH | ~450 items | ~82% |
| MEDIUM | ~75 items | ~14% |
| LOW | ~20 items | ~4% |
| **Total** | **~545 items** | **100%** |

## Items Requiring Further Validation

| Item | Domain | Reason |
|------|--------|--------|
| FEATURE_FLAGS.json details | Config | File permanently deleted |
| Ancienne structure contents | Knowledge | Directory permanently deleted |
| Exact 25 USER_FIELDS list | Qualification | knowledge_builder.py deleted |
| 6 AI model JSON schemas | AI | Files deleted |
| 30 engine Python files code | Engine | Files deleted |

**Source:** docs/lawim_heritage_gold/TRACEABILITY_MATRIX.md + H0.4 extraction reports
