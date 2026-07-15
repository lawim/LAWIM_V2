# CRM RECOVERY REPORT — LAWIM H0.4

**Date:** 15 July 2026
**Source:** CRM_MODEL.md, 08-ROLE-REFERENCE.md, implement_all.sql (via backup)

---

## What Was Recovered

| Concept | Details | Source |
|---------|---------|--------|
| 45 CRM rules | CRM-001 to CRM-045 | CRM_MODEL.md |
| 7 roles hierarchy | Master(7)→Vice-Master(6)→Assistant(5)→Agence(4)→Agent(3)→Vendeur(2)→Demandeur(1) | 08-ROLE-REFERENCE |
| 5 permission levels | None, Read, Write, Admin, Full | 08-ROLE-REFERENCE |
| 10 permission domains | Properties, Users, Leads, Transactions, etc. | 08-ROLE-REFERENCE |
| 7 user states | NEW_USER, SEARCHING_PROPERTY, PROPERTY_OWNER, AGENT, LEAD_CREATED, PREMIUM_AGENT, INACTIVE | USER_STATES.json |
| 13 event types | message.received, intent.detected, user.created, etc. | EVENT_TYPES.json |
| CRM Scoring V5 | 7 factors (total=1.0) | RULE_ENGINE_V5.json |
| Identity resolution | 5 criteria (phone=100, email=95, etc.) | identity_resolution.py |
| Agent management | Opt-in (4 steps), Rating (1-5), Pricing (500 FCFA/lead) | CRM_MODEL.md |
| 6 external partners | Notaire, architecte, géomètre, artisan, banque, assurance | 08-ROLE-REFERENCE |
| 8-stage commercial pipeline | Prospection→Fidélisation | CRM_MODEL.md |
| 20 legacy tables | persons, agents, properties, leads, disputes, etc. | implement_all.sql |
| 31 CRM V2 tables | Comprehensive schema | CRM_MODEL.md |

**Source:** docs/lawim_heritage_gold/CRM_MODEL.md + docs/lawim_heritage_gold/CRM_EXTRACTED_KNOWLEDGE.md
