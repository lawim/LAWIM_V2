# LAWIM_V2 — Platform Cartography

**Document ID:** LAWIM-OPS-CARTO-V1
**Status:** OPERATIONAL
**Date:** 2026-07-15

---

## 1. Platform Overview

LAWIM_V2 is a real estate platform mediating between property seekers, owners, agents, agencies, and professional service providers across Cameroon.

### 1.1 Architecture Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Web)                             │
│  Static HTML/JS · Admin Dashboard · Agent Portal               │
├─────────────────────────────────────────────────────────────────┤
│                     API & WEBHOOK LAYER                         │
│  HTTP Server · REST API v2 · Webhooks                          │
│  WhatsApp (Green API) · Telegram Bot · Campay Callbacks         │
├─────────────────────────────────────────────────────────────────┤
│                     APPLICATION CORE                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │ Program H│ │ Program J│ │ Program K│ │ Program L        │   │
│  │ Knowledge│ │ Identity │ │ Learning │ │ AI Agents        │   │
│  │ Runtime  │ │ Tracking │ │ Machine  │ │ Platform         │   │
│  │ Wizard   │ │ Analytics│ │ Gov      │ │ Orchestration    │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                       DATA LAYER                                │
│  SQLite/PostgreSQL · Prisma · JSON Knowledge Packs             │
│  File Storage · Media · Documents                               │
├─────────────────────────────────────────────────────────────────┤
│                    EXTERNAL INTEGRATIONS                         │
│  Green API (WhatsApp) · Telegram Bot API · Campay (MTN/Orange) │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Service Inventory

| Service | Type | Language | Entry Point | Port | Dependencies |
|---------|------|----------|-------------|------|--------------|
| HTTP Server | Backend | Python | `code/lawim_v2/server.py` | 8080 | PostgreSQL/SQLite |
| Static Frontend | Frontend | HTML/JS | `static/` | 8080 | HTTP Server |
| Knowledge Runtime | Library | Python | `code/lawim_v2/knowledge_runtime/` | — | None |
| Program J Core | Library | Python | `code/lawim_v2/program_j/` | — | H Runtime |
| Program K Core | Library | Python | `code/lawim_v2/program_k/` | — | H, J |
| Program L Core | Library | Python | `code/lawim_v2/program_l/` | — | H, J, K |
| Analytics | Library | Python | `code/lawim_v2/analytics/` | — | Database |
| Communication | Library | Python | `code/lawim_v2/communication/` | — | Database |
| CRM | Library | Python | `code/lawim_v2/crm/` | — | Database |
| AI | Library | Python | `code/lawim_v2/ai/` | — | Database |
| Source Intelligence | Library | Python | `code/lawim_v2/source_intelligence/` | — | Database |

## 3. Database Inventory

| Schema | Tables | Purpose |
|--------|--------|---------|
| v7 | intelligent | Project recommendations, trust scores |
| v8 | ecosystem | Partner profiles, trust |
| v11 | knowledge_platform | Knowledge sources, ranking |
| v13 | real_estate_intelligence | Property intelligence, verification |
| v14 | crm | CRM, contacts, leads, campaigns, satisfaction |
| v17 | communication | Messages, notifications, templates, campaigns |
| v18 | analytics | Metrics, KPIs, dashboards, scores |
| v19 | core | Users, organizations, sessions, properties, conversations |
| v20 | conversation_v2 | Conversation sessions, facts, decisions |

## 4. External Dependencies

| Dependency | Purpose | Protocol | Credentials Required |
|-----------|---------|----------|---------------------|
| Green API | WhatsApp messaging | HTTPS/JSON | API Token |
| Telegram Bot API | Telegram messaging | HTTPS/JSON | Bot Token |
| Campay | Mobile money payments | HTTPS/JSON | Username + Password |
| PostgreSQL | Production database | TCP | Connection string |
| SMTP | Email sending | SMTP | Server + credentials |

## 5. Feature Flags Inventory (44 total)

| Prefix | Count | Domain |
|--------|-------|--------|
| knowledge_runtime_* | 1 | Program H |
| unified_conversation_*, actor_registry_*, etc. | 9 | Program J |
| learning_events_*, outcome_*, feedback_*, dataset_*, etc. | 15 | Program K |
| agent_platform_*, conversation_agent_*, etc. | 19 | Program L |

All 44 flags default to `false`. Activation follows documented rollout procedures.
