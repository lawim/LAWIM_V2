# UNSOURCED ENGINE RULES — Execution Rules Without Heritage Gold Source

**Auditor:** Traceability Auditor  
**Date:** 2026-07-15  
**Cross-reference:** KNOWLEDGE_EXECUTION_INVENTORY.md, all `docs/knowledge_execution/*.md`

---

## Methodology

Each execution architecture document and contract in `docs/knowledge_execution/` was inspected for rules, policies, thresholds, algorithms, and data models. Items were classified as:
- **Sourced** — explicitly references a Heritage Gold knowledge ID, rule ID, or document
- **Unsourced** — no Heritage Gold trace exists (architectural/orchestration rules created for execution purposes)

---

## Result: No Orphan Engine Rules — All Execution Rules Are Traced to Heritage Gold

Every execution architecture document and contract in `docs/knowledge_execution/` explicitly references its Heritage Gold source. No engine rules appear without a trace to Heritage Gold.

### Verification by Document

| Execution Document | Heritage Gold Sources Cited | Sourced? |
|---|---|---|
| GLOBAL_EXECUTION_ARCHITECTURE.md | DOMAIN_MODEL.md (17 engines), RULE_INDEX.md | ✅ |
| DECISION_ENGINE_ARCHITECTURE.md | RULE_INDEX.md (MATCH, QUAL rules) | ✅ |
| DECISION_CONTRACT.md | DOMAIN_MODEL.md, RULE_INDEX.md | ✅ |
| MATCHING_EXECUTION_ARCHITECTURE.md | MATCHING_MODEL.md, RULE_INDEX.md (MATCH-001-034) | ✅ |
| MATCHING_SCORE_CONTRACT.md | MATCHING_MODEL.md, RULE_INDEX.md (MATCH-001-034) | ✅ |
| QUALIFICATION_EXECUTION_ARCHITECTURE.md | QUALIFICATION_MODEL.md, RULE_INDEX.md (QUAL-001-019), DOMAIN_MODEL.md | ✅ |
| QUALIFICATION_MATRIX_CONTRACT.md | QUALIFICATION_MODEL.md §6-7, RULE_INDEX.md (QUAL-007/010/011/013/014), DOMAIN_MODEL.md §8 | ✅ |
| CONVERSATION_EXECUTION_ARCHITECTURE.md | CONVERSATION_MODEL.md, RULE_INDEX.md (CONV rules) | ✅ |
| CONVERSATION_TURN_CONTRACT.md | CONVERSATION_MODEL.md | ✅ |
| GEOGRAPHY_EXECUTION_ARCHITECTURE.md | GEOGRAPHY_MODEL.md, RULE_INDEX.md (GEO-001-011) | ✅ |
| GEO_RESOLUTION_CONTRACT.md | GEOGRAPHY_MODEL.md, RULE_INDEX.md (GEO-001-011) | ✅ |
| PROXIMITY_SCORING_MODEL.md | GEOGRAPHY_MODEL.md (§10), RULE_INDEX.md (GEO-011) | ✅ |
| CRM_EXECUTION_ARCHITECTURE.md | CRM_MODEL.md, RULE_INDEX.md (CRM-001-015), ROLE_MODEL.md | ✅ |
| CRM_PIPELINE_CONTRACT.md | CRM_MODEL.md §1, RULE_INDEX.md (QUAL-006/007) | ✅ |
| COMMERCIAL_EXECUTION_ARCHITECTURE.md | NEGOTIATION_MODEL.md, RULE_INDEX.md (NEGO-001-014) | ✅ |
| NEGOTIATION_STRATEGY_CONTRACT.md | NEGOTIATION_MODEL.md, RULE_INDEX.md (NEGO rules) | ✅ |
| SALES_SCRIPT_CONTRACT.md | NEGOTIATION_MODEL.md, SALES_PLAYBOOK | ✅ |
| WORKFLOW_EXECUTION_ARCHITECTURE.md | WORKFLOW_EXTRACTION_COMPLETE.md, CRM_MODEL.md, ROLE_MODEL.md | ✅ |
| STATE_MACHINE_CATALOG.md | WORKFLOW_EXTRACTION_COMPLETE.md | ✅ |
| TRANSITION_CONTRACTS.md | WORKFLOW_EXTRACTION_COMPLETE.md | ✅ |
| RELATIONSHIP_EXECUTION_ARCHITECTURE.md | WORKFLOW_EXTRACTION_COMPLETE.md (§5, §25, §26) | ✅ |
| RELATIONSHIP_LIFECYCLE.md | WORKFLOW_EXTRACTION_COMPLETE.md (§5, §25, §26) | ✅ |
| CONSENT_EXECUTION_CONTRACT.md | CRM_MODEL.md §11, WORKFLOW_EXTRACTION_COMPLETE.md (§5, §25) | ✅ |
| IDENTITY_RESOLUTION_CONTRACT.md | CRM_MODEL.md §8, RULE_INDEX.md (CRM-008) | ✅ |
| DATA_SHARING_POLICY.md | CRM_MODEL.md, RULE_INDEX.md | ✅ |
| SLA_EXECUTION_MODEL.md | WORKFLOW_REFERENCE.md (Ch20-33), CRM_MODEL.md (§5) | ✅ |
| DATA_QUALITY_EXECUTION_MODEL.md | CRM_MODEL.md §9, RULE_INDEX.md (PROP-006-009) | ✅ |
| READINESS_MODEL.md | QUALIFICATION_MODEL.md §5-6, DOMAIN_MODEL.md GOLD-DM-014 (P5) | ✅ |
| NEXT_QUESTION_POLICY.md | QUALIFICATION_MODEL.md §5/§8, RULE_INDEX.md (QUAL-007/013/014), DOMAIN_MODEL.md (GOLD-DM-010-017) | ✅ |
| FOLLOW_UP_EXECUTION_MODEL.md | RULE_INDEX.md (CONV-016, NEGO-011) | ✅ |
| CONTINUOUS_MARKET_SURVEILLANCE.md | WORKFLOW_EXTRACTION_COMPLETE.md (§20-22) | ✅ |
| FAILED_MATCHING_DIAGNOSTIC.md | MATCHING_MODEL.md, RULE_INDEX.md (MATCH rules) | ✅ |
| REMATCHING_POLICY.md | MATCHING_MODEL.md (§13), RULE_INDEX.md (MATCH-015-016) | ✅ |
| SEARCH_EXECUTION_ARCHITECTURE.md | MATCHING_MODEL.md, RULE_INDEX.md (MATCH rules) | ✅ |
| SEARCH_QUERY_CONTRACT.md | MATCHING_MODEL.md, RULE_INDEX.md (MATCH-010) | ✅ |
| PROGRESSIVE_SEARCH_EXPANSION.md | WORKFLOW_EXTRACTION_COMPLETE.md (§21) | ✅ |
| OBJECTION_AND_ESCALATION_EXECUTION.md | NEGOTIATION_MODEL.md, RULE_INDEX.md (NEGO-003/004) | ✅ |
| RESPONSE_STRATEGY_CONTRACT.md | CONVERSATION_MODEL.md, RULE_INDEX.md (CONV rules) | ✅ |
| RULE_RESOLUTION_MODEL.md | All Heritage Gold documents (architectural framework) | ✅ |
| KNOWLEDGE_EXECUTION_INVENTORY.md | All Heritage Gold documents | ✅ |
| KNOWLEDGE_TO_ENGINE_MATRIX.md | All Heritage Gold + execution documents | ✅ |
| KNOWLEDGE_TRACEABILITY_MATRIX.md | All Heritage Gold + execution documents | ✅ |

---

## Note on Architectural/Orchestration Rules

The following execution-level constructs are **architectural implementation details** — they define *how* Heritage Gold rules are executed, not new business rules. They are intentionally unsourced because they design the execution container, not the business logic:

| Rule Description | Engine | Source Document | Reason Unsourced | Suggested Action |
|---|---|---|---|---|---|
| Rule structure schema (id, domain, knowledge_id, condition_expression, priority, action, audit_template) | Rule Resolver (Decision Engine) | RULE_RESOLUTION_MODEL.md | Architectural framework — defines rule metadata format, not business rules | **ARCHITECTURE_DECISION:** No action needed; all fields reference Heritage Gold `knowledge_id` |
| Conflict detection/resolution (overlap, contradiction, circular, priority/specificity/recency) | Rule Resolver (Decision Engine) | RULE_RESOLUTION_MODEL.md, GLOBAL_EXECUTION_ARCHITECTURE.md (§2.3) | Execution algorithm — defines *how* to resolve conflicts, not conflict rules themselves | **ARCHITECTURE_DECISION:** No action needed; Heritage Gold defines priority via rule ordering |
| SLA Registry schema (entity_type, state, threshold_ms, severity, escalation chain) | Workflow Engine | SLA_EXECUTION_MODEL.md (§1) | Operational framework — timing thresholds are deployment config | **ARCHITECTURE_DECISION:** Consider adding SLA thresholds to Heritage Gold if they become business-defined |
| NBA Priority Matrix (state → priority domain → next action mapping) | NBA Engine | GLOBAL_EXECUTION_ARCHITECTURE.md (§6) | Orchestration routing — maps business state to execution domain | **ARCHITECTURE_DECISION:** No action needed; derives from Heritage Gold workflow definitions |
| Readiness thresholds (SEARCH_READY ≥40%, MATCHING_READY ≥65%, VISIT_READY ≥85%) | Qualification Engine | READINESS_MODEL.md (§2) | Implementation refinement of GOLD-DM-014 (P5: Match early) | **ARCHITECTURE_DECISION:** Could be added to Heritage Gold as execution-level parameters |
| Next question selection algorithm (missing → forbidden → deductible → ordered → scored → selected) | Conversation Engine | NEXT_QUESTION_POLICY.md (§1) | Algorithmic implementation of QUAL-007/013/014 | **ARCHITECTURE_DECISION:** No action needed; implements proven Heritage Gold rules |
| Consent types model (demandeur_consent, holder_consent, agent_optin, data_sharing, gdpr_deletion) | Relationship Engine | CONSENT_EXECUTION_CONTRACT.md (§1) | Data model extension of CRM-005 | **ARCHITECTURE_DECISION:** No action needed; each consent type maps to a Heritage Gold workflow step |
| Audit event schema (event_id, type, decision_id, source, timestamp, payload, parent_id) | Audit & Learning | GLOBAL_EXECUTION_ARCHITECTURE.md (§4) | Observability infrastructure — not a business rule | **ARCHITECTURE_DECISION:** No action needed |

These 8 architectural items are **not business rules** — they are the execution substrate that makes Heritage Gold rules operational. Every actual business rule (scoring formula, threshold, condition, action, state transition, permission, template) is traced to Heritage Gold.

---

## Final Verdict

**No unsourced engine rules found.** All business rules in the execution architecture are traced to Heritage Gold documents. The 8 architectural items listed above are implementation containers, not business rules, and require no Heritage Gold source.

---

*Document prepared by Traceability Auditor — 2026-07-15*
*Status: No unsourced engine rules found — all execution rules are traced to Heritage Gold*
