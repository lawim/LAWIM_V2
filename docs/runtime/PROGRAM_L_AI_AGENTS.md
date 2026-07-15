# Program L — AI Agent Platform

**Document ID:** LAWIM-PROGRAM-L-V1
**Status:** CANONICAL
**Date:** 2026-07-15

---

## L1 — Agent Platform Foundation

- **Agent Registry**: 16 agents (Orchestrator, Conversation, Qualification, RealEstate, Search, Matching, Commercial, Relationship, Document, LegalAssistance, Financial, Payment, Support, Administration, Director, Learning)
- **Capability Registry**: 18 capabilities (CONVERSE, QUALIFY_REQUEST, SEARCH_PROPERTIES, MATCH_PROPERTIES, CREATE_VISIT_REQUEST, PREPARE_TRANSACTION, ANALYZE_DOCUMENT, PREPARE_DOCUMENT, EXPLAIN_PAYMENT, INITIATE_PAYMENT_REQUEST, ESCALATE_TO_HUMAN, SUMMARIZE_CASE, ANALYZE_ANALYTICS, REVIEW_LEARNING_PROPOSAL, EXPLAIN_CONTRACT, MANAGE_RELATIONSHIP, PROVIDE_SUPPORT, ADMINISTER_SYSTEM)
- **Runtime**: Invocation lifecycle (CREATED→RUNNING→COMPLETED/FAILED/TIMED_OUT/ESCALATED), actions, responses, audit
- **Memory**: Working, conversation, case, user preference, relationship, agent working, knowledge reference, learning reference
- **Tool Governance**: 7 risk levels (READ_ONLY to IRREVERSIBLE), permission-based

## L2 — Customer Interaction Agents

Conversation, Qualification, Relationship, Support, Human Handover

## L3 — Real Estate Execution Agents

Real Estate, Search, Matching, Commercial, Visit and Transaction Assistance

## L4 — Document, Legal and Financial Agents

Document, Legal Assistance (limitations stated), Financial, Payment (uses Campay)

## L5 — Administration, Direction and Learning Agents

Administration, Director (uses J analytics), Learning (no auto-publication)

## L6 — Multi-Agent Orchestration

- **Router**: Keyword-based deterministic routing
- **Safety**: 5 decisions (ALLOW, ALLOW_WITH_MASKING, ALLOW_WITH_CONFIRMATION, HANDOVER_REQUIRED, DENY)
- **Delegation**: Tracked with parent/child relationships
- **Loop prevention**: max depth, max calls, duplicate detection

## Feature Flags

19 flags, all disabled by default: agent_platform_enabled, conversation_agent_enabled, qualification_agent_enabled, real_estate_agent_enabled, search_agent_enabled, matching_agent_enabled, commercial_agent_enabled, relationship_agent_enabled, document_agent_enabled, legal_assistance_agent_enabled, financial_agent_enabled, payment_agent_enabled, support_agent_enabled, administration_agent_enabled, director_agent_enabled, learning_agent_enabled, multi_agent_orchestration_enabled, agent_memory_enabled, agent_admin_controls_enabled
