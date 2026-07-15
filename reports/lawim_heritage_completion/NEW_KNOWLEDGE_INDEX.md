# NEW KNOWLEDGE INDEX — LAWIM H0.4 Heritage Completion

**Date:** 15 July 2026
**Purpose:** Index of all new knowledge items discovered during H0.4

---

## Workflow Knowledge (New)

| ID | Concept | Source | Section |
|----|---------|--------|---------|
| WK-001 | 21 business workflows | 05-WORKFLOW-REFERENCE.md | §1 |
| WK-002 | Next Best Action (NBA) — 12 actions | 05-WORKFLOW-REFERENCE.md | §20 |
| WK-003 | Progressive Search Expansion (6 levels) | 05-WORKFLOW-REFERENCE.md | §21 |
| WK-004 | Continuous Market Surveillance | 05-WORKFLOW-REFERENCE.md | §22 |
| WK-005 | Health Scores (5 types) | 05-WORKFLOW-REFERENCE.md | §23 |
| WK-006 | SLA by property type (15 types) | 05-WORKFLOW-REFERENCE.md | §24 |
| WK-007 | ~95 business states across all workflows | 05-WORKFLOW-REFERENCE.md | §26 |
| WK-008 | Active workflow principle | 05-WORKFLOW-REFERENCE.md | Ch10 |

## Matching Knowledge (New / Detailed)

| ID | Concept | Source |
|----|---------|--------|
| MK-001 | 16 per-type weightings (complete details) | 04-DECISION-ENGINE Ch42-58 |
| MK-002 | Transaction Success Score — 8 indicators | 04-DECISION-ENGINE Ch90 |
| MK-003 | Trust Index — 5 levels | 04-DECISION-ENGINE Ch91 |
| MK-004 | 12 official Decision Actions | 04-DECISION-ENGINE Ch86 |
| MK-005 | Decision Matrix (Ch87) | 04-DECISION-ENGINE |
| MK-006 | Action Priority (Ch88) | 04-DECISION-ENGINE |
| MK-007 | Automatic Decision Thresholds (Ch92) | 04-DECISION-ENGINE |
| MK-008 | Market Tension Index | 04-DECISION-ENGINE Ch96 |
| MK-009 | Market Memory / Global Learning | 04-DECISION-ENGINE Ch95 |
| MK-010 | Negotiation AI (Ch97) | 04-DECISION-ENGINE |
| MK-011 | Unified V2.0 7 dimensions | knowledge_unified/matching/ |
| MK-012 | 5 geo scoring levels, 3 mobility modes | knowledge_unified/matching/ |
| MK-013 | Freshness bonuses (0-30+ days) | knowledge_unified/matching/ |
| MK-014 | 6 rejection rules (V4) | GEO_REFERENCE_MODEL_V4 |

## CRM Knowledge (New)

| ID | Concept | Source |
|----|---------|--------|
| CK-001 | 45 CRM rules (CRM-001 to CRM-045) | CRM_MODEL.md + 08-ROLE-REFERENCE |
| CK-002 | 5 lead types with intent mapping | lead_classifier_v1.json |
| CK-003 | 13 boosters, 8 penalties | lead_classifier_v1.json |
| CK-004 | V2 scoring engine details | lead_scoring.json |
| CK-005 | Identity resolution 5 criteria | identity_resolution.py |
| CK-006 | 5-step merge algorithm | identity_resolution.py |
| CK-007 | 8-stage commercial pipeline | CRM_MODEL.md |
| CK-008 | 6 external partner types | 08-ROLE-REFERENCE |
| CK-009 | 31 CRM V2 tables | CRM_MODEL.md |

## Negotiation Knowledge (New)

| ID | Concept | Source |
|----|---------|--------|
| NK-001 | 4 buyer profiles with full details | SALES-PLAYBOOK + knowledge_unified |
| NK-002 | 3 seller profiles with full details | SALES-PLAYBOOK + knowledge_unified |
| NK-003 | 10 buyer fears with responses | knowledge_unified/commercial/ |
| NK-004 | 8 seller fears with responses | knowledge_unified/commercial/ |
| NK-005 | 23 objection patterns with responses | knowledge_unified/commercial/ |
| NK-006 | 8 sales playbook objections | 48-LAWIM-SALES-PLAYBOOK |
| NK-007 | 6+ LAWIM arguments | knowledge_unified/commercial/ |
| NK-008 | 7 property arguments | knowledge_unified/commercial/ |
| NK-009 | 4 key seasonal moments | SALES-PLAYBOOK |
| NK-010 | 5-step trust sequence | knowledge_unified/commercial/ |
| NK-011 | 8-step commercial process | SALES-PLAYBOOK |
| NK-012 | Closing techniques and lines | knowledge_unified/commercial/ |
| NK-013 | 10 diaspora behavioral principles | knowledge_unified/commercial/ |
| NK-014 | 7-step diaspora trust journey | knowledge_unified/commercial/ |
| NK-015 | 6 price expressions (Cameroon) | knowledge_unified/commercial/ |

## Geography Knowledge (New)

| ID | Concept | Source |
|----|---------|--------|
| GK-001 | 9-level territorial hierarchy | 09-GEOLOCATION-REFERENCE |
| GK-002 | 35 absolute geo rules | 09-GEOLOCATION-REFERENCE |
| GK-003 | V4 Geo Scoring Formula (40/25/20/15) | GEO_REFERENCE_MODEL_V4 |
| GK-004 | 6 precision levels | 09-GEOLOCATION-REFERENCE |
| GK-005 | Geo Engine responsibilities (12 areas) | 09-GEOLOCATION-REFERENCE |
| GK-006 | 125 neighborhood affinity pairs | knowledge_unified/ |
| GK-007 | Mobility modes (STRICT/FLEXIBLE/VERY_FLEXIBLE) | knowledge_unified/ |

## Conversation Knowledge (New)

| ID | Concept | Source |
|----|---------|--------|
| CVK-001 | Complete tone rules (professional voice) | knowledge_unified/commercial/ |
| CVK-002 | 10 forbidden patterns | knowledge_unified/commercial/ |
| CVK-003 | 6 conversation intents + urgency | knowledge_unified/language/ |
| CVK-004 | Channel-specific behaviors (5 channels) | 03-CONVERSATION-REFERENCE |
| CVK-005 | 12 conversation events traceability | CONVERSATION_MODEL.md |
| CVK-006 | Emotional triggers for conversion | knowledge_unified/commercial/ |
| CVK-007 | Anti-patterns in closing | knowledge_unified/commercial/ |

## Language Knowledge (New)

| ID | Concept | Source |
|----|---------|--------|
| LK-001 | 14 pidgin words (IA detector) | language_detector_ia.py |
| LK-002 | 12 pidgin words (basic detector) | language_detector.py |
| LK-003 | 6 intent types + pattern matching | knowledge_unified/language/ |
| LK-004 | 26 marketing vocabulary entries (FR/EN/PID) | 30A-BUSINESS-DICTIONARY |
| LK-005 | 10 city abbreviations + 11 RE abbreviations | entity_linking data |

## Source References

| File | Type | Location |
|------|------|----------|
| WORKFLOW_EXTRACTION_COMPLETE.md | Extraction doc | docs/lawim_heritage_gold/ |
| QUALIFICATION_HERITAGE_EXTRACTION.md | Extraction doc | docs/lawim_heritage_gold/ |
| CRM_EXTRACTED_KNOWLEDGE.md | Extraction doc | docs/lawim_heritage_gold/ |
| LANGUAGE_BUSINESS_KNOWLEDGE.md | Extraction doc | docs/lawim_heritage_gold/ |
| KNOWLEDGE_RECOVERY_REPORT_H0.4.md | Recovery report | docs/lawim_heritage_gold/ |
| EVIDENCE_VALIDATION_REPORT_H0.4.md | Validation report | docs/lawim_heritage_gold/ |
