# WORKFLOW STATE CROSSWALK

**Semantic Harmonization between Heritage Gold (21 Workflows) and LAWIM_V2 State Machines**

**Version:** 1.0  
**Date:** 2026-07-15  
**Source:** STATE_MACHINE_CATALOG.md (Gold), property_domain.py / project_domain.py / conversation_domain.py / prisma/schema.prisma (V2)

---

## Mapping Status Legend

| Status | Code | Meaning |
|---|---|---|
| EXACT_MATCH | `🟢 EM` | States map 1:1 with identical semantics |
| NORMALIZED_MATCH | `🔵 NM` | States map 1:1 with naming/scope differences |
| ONE_TO_MANY | `🟡 O2M` | One Gold state maps to multiple V2 states |
| MANY_TO_ONE | `🟠 M2O` | Multiple Gold states collapse into one V2 state |
| PARTIAL_MATCH | `🟣 PM` | Partial overlap, significant gaps on both sides |
| EXTENSION_REQUIRED | `🔴 ER` | No V2 equivalent; new state machine needed |
| OBSOLETE | `⚪ OB` | Gold state no longer relevant |
| CONFLICT | `⛔ CF` | Incompatible transition/guard semantics |
| HUMAN_DECISION_REQUIRED | `⚠️ HD` | Cannot auto-resolve; human architect decision needed |
| UNMAPPED | `❓ UM` | No analysis performed yet |

---

## 1. Overview: 21 Heritage Gold Workflows vs LAWIM_V2 State Machines

| # | Workflow | Gold States | V2 States | Mapping Status | Gap Severity |
|---|---|---|---|---|---|
| 01 | Property Lifecycle | 13 | 5 (property) + 5 (availability) | `🟣 PM` | HIGH |
| 02 | Dossier/Case Lifecycle | 14 | 5 (project) + 5 (step) | `🟣 PM` | HIGH |
| 03 | Matching Lifecycle | 10 | 0 | `🔴 ER` | CRITICAL |
| 04 | Mise en Relation (Contact) | 6 | 0 (partial in conversation) | `🟣 PM` | HIGH |
| 05 | Visit Lifecycle | 9 | 0 | `🔴 ER` | CRITICAL |
| 06 | Negotiation Lifecycle | 8 | 6 (negotiation stages) | `🟣 PM` | MEDIUM |
| 07 | Transaction Lifecycle | 10 | 0 | `🔴 ER` | CRITICAL |
| 08 | Paid Services & Payment | 8 + 10 | 0 | `🔴 ER` | CRITICAL |
| 09 | Disputes, Claims & Incidents | 8 | 0 | `🔴 ER` | HIGH |
| 10 | Closure, Archiving & Retention | 4 | 1 (archived in each model) | `🟠 M2O` | MEDIUM |
| 11 | Mediation Workflow | 8 | 0 | `🔴 ER` | HIGH |
| 12 | User Identity Lifecycle | 7 | 1 (role string) | `🟣 PM` | MEDIUM |
| 13 | Organization/Agency Lifecycle | 8 | 1 (kind string) | `🔵 NM` | LOW |
| 14 | Agent Invitation Workflow | 7 | 0 | `🔴 ER` | HIGH |
| 15 | Publication (SIE-Enriched) | 11 | 0 | `🔴 ER` | HIGH |
| 16 | Redirection (SIE-Enriched) | 12 | 0 | `🔴 ER` | HIGH |
| 17 | Conversion & Attribution | 12 | 0 | `🔴 ER` | HIGH |
| 18 | CRM Pipeline | 8 | 0 | `🔴 ER` | CRITICAL |
| 19 | Agent Opt-In Workflow | 4 | 0 | `🔴 ER` | MEDIUM |
| 20 | Identity Resolution Workflow | 5 | 0 | `🔴 ER` | MEDIUM |
| 21 | Main Cross-cutting Workflow | 9 | 0 | `🔴 ER` | CRITICAL |

**Summary:**
- EXACT_MATCH: 0
- NORMALIZED_MATCH: 1 (Org/Agency)
- ONE_TO_MANY: 0
- MANY_TO_ONE: 1 (Closure/Archiving)
- PARTIAL_MATCH: 5 (Property, Dossier, Mise en Relation, Negotiation, User Identity)
- EXTENSION_REQUIRED: 14
- OBSOLETE: 0
- CONFLICT: 0
- HUMAN_DECISION_REQUIRED: 0
- UNMAPPED: 0

---

## 2. Workflow-by-Workflow Comparison

### 2.01 Property Lifecycle

**Entity:** `property`  
**Gold States (13):** Création → Qualification → Validation → Publié → Disponible → Matching → Visites → Négociation → Réservé → Transaction → Indisponible → Réactivation éventuelle → Archivé  
**V2 States (5):** draft, open, closed, published, archived  
**V2 Availability (5):** available, reserved, sold, rented, unavailable

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| Création | draft | `🟣 PM` | Draft covers creation but lacks qualification sub-states |
| Qualification | (embedded in draft→open) | `🟠 M2O` | No dedicated qualification state |
| Validation | (embedded in open→published) | `🟠 M2O` | No dedicated validation state |
| Publié | published | `🔵 NM` | Direct match, naming differs |
| Disponible | available | `🔵 NM` | Direct match via availability field |
| Matching | (none) | `🔴 ER` | No matching state machine |
| Visites | (none) | `🔴 ER` | No visit lifecycle |
| Négociation | (via conversation negotiation_stage) | `🟣 PM` | Delegated to conversation model |
| Réservé | reserved | `🔵 NM` | Direct match via availability field |
| Transaction | (none) | `🔴 ER` | No transaction state machine |
| Indisponible | unavailable, sold, rented | `🔵 NM` | Split across 3 availability values |
| Réactivation éventuelle | (none) | `🔴 ER` | No reactivation workflow |
| Archivé | archived | `🟢 EM` | Direct match |

**Transitions Preserved:**
- draft → published (maps to Création→Publié)
- published → closed/archived (maps to Publié→Indisponible/Archivé)
- available → reserved (via availability)

**Transitions Lost:**
- Création → Qualification → Validation → Publié (enrichment pipeline)
- Disponible → Matching → Visites → Négociation (full commercial pipeline)
- Réservé → Transaction (transaction handoff)
- Indisponible → Disponible (reactivation)
- Any state → Réactivation éventuelle

**Transitions New (V2 only):**
- draft → open, draft → closed (direct non-published transitions)
- open → published, open → closed, open → archived
- closed → archived

**Guards:**
- Gold: Property Health Score, coherence/conformity/uniqueness/availability checks, double consent
- V2: `can_publish()` (title, city, price_min/max, not deleted)

**SLA:**
- Gold: Per property type rotation SLA (24h→1095d), time-in-state thresholds, auto-archival at 90d inactivity
- V2: None

**NBA:**
- Gold: State-specific NBA (complete fields, suggest price reduction, broaden matching, etc.)
- V2: None

**Events:**
- Gold: 12 audit events (property.qualified, .published, .available, .matching, .reserved, etc.)
- V2: Generic Event model (kind, payload — no property-specific event types)

---

### 2.02 Dossier/Case Lifecycle

**Entity:** `dossier` → maps to `project`  
**Gold States (14):** Création → Qualification → Matching → Présentation → Attente décision demandeur → Contact détenteur → Attente décision détenteur → Mise en relation → Visite → Négociation → Accord → Transaction → Clôture → Archivage  
**V2 States (5):** draft, active, paused, completed, archived  
**V2 Step States (5):** pending, in_progress, completed, skipped, blocked

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| Création | draft | `🟣 PM` | Project creation maps to dossier creation |
| Qualification | active + step:pending | `🟠 M2O` | Qualification is a step in the journey |
| Matching | (none) | `🔴 ER` | No matching lifecycle |
| Présentation | (none) | `🔴 ER` | No presentation concept |
| Attente décision demandeur | (none) | `🔴 ER` | No wait states |
| Contact détenteur | (none) | `🔴 ER` | No contact workflow |
| Attente décision détenteur | (none) | `🔴 ER` | No wait states |
| Mise en relation | (none) | `🔴 ER` | No mise en relation |
| Visite | active + step:visit | `🟣 PM` | Visit journey step exists but no visit state machine |
| Négociation | active + step:negotiation | `🟣 PM` | Negotiation step exists but no negotiation state machine |
| Accord | active + step:closing | `🟠 M2O` | Agreement → closing step |
| Transaction | active + step:closing | `🟠 M2O` | Transaction → closing step |
| Clôture | completed | `🔵 NM` | Direct match |
| Archivage | archived | `🟢 EM` | Direct match |

**Transitions Preserved:**
- Création→Qualification (maps to draft→active with step progression)
- Clôture→Archivage (maps to completed→archived)

**Transitions Lost:**
- Full demandeur/holder decision wait chain (6 states)
- Double consent workflow
- Rematching on refusal
- Mise en relation → Visite → Négociation → Accord → Transaction pipeline

**Transitions New (V2 only):**
- active ↔ paused (no pause in Gold)

**Guards:**
- Gold: Minimum fields for qualification, score >= 60% for matching, double consent
- V2: None (step status transitions are free-form)

**SLA:**
- Gold: Per-state SLAs (24h qualify, 48h critical fields, 72h decision, etc.)
- V2: None

**NBA:**
- Gold: State-specific NBA (ask qualifying questions, present properties, contact holder, etc.)
- V2: `derive_next_actions()` lists pending steps

**Events:**
- Gold: 14 audit events (dossier.qualifying, .matching, .presented, .contact_established, etc.)
- V2: Generic Event model

---

### 2.03 Matching Lifecycle

**Entity:** `match`  
**Gold States (10):** Load Dossier → Check Critical Fields → Select Compatible Properties → Eliminate Incompatible → Calculate Scores → Rank Properties → Propose Best → Wait for Decision → Learn → Recalculate if Necessary  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 10 states | (none) | `🔴 ER` | No matching engine or state machine exists |

**V2 Equivalent Check:**
- H1 contracts exist at `code/lawim_v2/matching.py` but no state machine
- No match entity in Prisma schema
- No score calculation, ranking, or presentation logic

**Action Required:** Full matching lifecycle implementation with:
- Score dimensions (Real Estate, Availability, Document, Holder Reliability, Transaction Success)
- 4 compatibility levels
- Rematching rules on refusal
- Learning from acceptance/refusal patterns

---

### 2.04 Mise en Relation / Contact Lifecycle

**Entity:** `contact`  
**Gold States (6):** Matching Complete → Demandeur Interested → Holder Contacted → Holder Decision → Double Consent Obtained → Mise en Relation Established  
**V2 States:** None (partial via conversation model)

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| Matching Complete | (none) | `🔴 ER` | No matching lifecycle |
| Demandeur Interested | conversation status:open | `🟣 PM` | Conversation creation implies interest |
| Holder Contacted | (none) | `🔴 ER` | No holder contact workflow |
| Holder Decision | (none) | `🔴 ER` | No holder decision tracking |
| Double Consent Obtained | (none) | `🔴 ER` | No consent mechanism |
| Mise en Relation Established | (none) | `🔴 ER` | No contact establishment |

**Key Gap:** Double consent workflow is entirely missing. Gold requires MANDATORY double consent — demandeur interested AND holder favorable — before any contact is established.

**Holder Silence Escalation (Gold):**
1. First reminder → 2. Second reminder → 3. Last reminder → 4. Property marked "to confirm" → 5. Rematching

**Interlocutor Shift:** After Mise en Relation, the interlocutor changes from LAWIM AI to the property owner/agency. This concept does not exist in V2.

---

### 2.05 Visit Lifecycle

**Entity:** `visit`  
**Gold States (9):** Demandée → En attente de confirmation → Confirmée → Reportée → Annulée → Réalisée → Refusée → Absence du demandeur → Absence du détenteur  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 9 states | (none) | `🔴 ER` | No visit entity or state machine |

**V2 Equivalent Check:**
- Visit journey step exists in project_domain.py but is just a step label
- No Visit model in Prisma schema
- No visit scheduling, confirmation, cancellation, absence tracking

**Action Required:** Complete visit lifecycle with:
- Visit scheduling with party confirmation
- Rescheduling (reportée) flow
- No-show tracking for both parties
- Post-visit satisfaction recording
- NBA based on satisfaction level

---

### 2.06 Negotiation Lifecycle

**Entity:** `negotiation`  
**Gold States (8):** Ouverte → En discussion → Offre → Contre-offre → Accord de principe → Accord final → Transaction / Échec  
**V2 States (6):** inquiry, offer, counter, accepted, declined, closed

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| Ouverte | inquiry | `🔵 NM` | Both represent negotiation initiation |
| En discussion | (none) | `🔴 ER` | No discussion state |
| Offre | offer | `🟢 EM` | Direct match |
| Contre-offre | counter | `🟢 EM` | Direct match |
| Accord de principe | (none) | `🔴 ER` | No agreement-in-principle stage |
| Accord final | accepted | `🟣 PM` | Partial — Gold has 2-tier agreement |
| Transaction | closed | `🟠 M2O` | Gold separates transaction from negotiation end |
| Échec | declined / closed | `🟣 PM` | Gold has explicit failure terminal |

**Transitions Preserved:**
- inquiry → offer (Ouverte → Offre)
- offer → counter (Offre → Contre-offre)
- counter → offer (Contre-offre → Offre)
- accepted → closed (Accord final → Transaction → ...)

**Transitions Lost:**
- Ouverte → En discussion (no discussion phase)
- Contre-offre → Accord de principe (no agreement-in-principle)
- Accord de principe → Accord final (two-tier agreement)
- Any → Échec (explicit failure terminal)
- Transaction lifecycle handoff

**Transitions New (V2 only):**
- closed → open (reopening)
- declined → closed (V2 has 2-way from declined)

**Guards:**
- Gold: Valid offer (amount, terms), max delay, party withdrawal, property unavailable
- V2: None

**SLA:**
- Gold: Follow-up intervals J1, J7, J30, J90; silence escalation (3 reminders → auto-close → rematching)
- V2: None

**NBA:**
- Gold: Per-state action guidance
- V2: None

**Negotiable Elements (Gold):**
- Sale: Price, payment terms, deadlines, included furniture, equipment, release date
- Rental: Rent, deposit, advance, lease duration, entry date, possible works
- Land: Price, boundary marking, documents, deadlines
- Commercial: Rent, key money, equipment, duration

---

### 2.07 Transaction Lifecycle

**Entity:** `transaction`  
**Gold States (10):** Accord → Préparation → Documents → Paiement → Signature → Remise des clés → Confirmation → Transaction terminée → Archivage / Échec  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 10 states | (none) | `🔴 ER` | No transaction entity exists |

**V2 Equivalent Check:**
- No Transaction model in Prisma
- No payment processing
- No document management workflow
- No key handover or post-transaction confirmation

**Action Required:** Full transaction lifecycle with:
- Document preparation and verification per transaction type
- Payment processing (sale/rental)
- Contract signing workflow
- Key handover tracking
- Post-transaction satisfaction confirmation
- 5 transaction types defined: Location, Vente, Achat, Bail professionnel, Bail commercial, Location saisonnière

---

### 2.08 Paid Services & Payment Lifecycle

**Entity:** `paid_service`  
**Gold States (8):** Création → Proposition → Acceptation → Paiement → Activation → Utilisation → Expiration → Archivage  
**Gold Payment Sub-states (10):** PAYMENT_CREATED, PAYMENT_INITIATED, PAYMENT_PENDING, PAYMENT_CONFIRMED, PAYMENT_FAILED, PAYMENT_CANCELLED, PAYMENT_EXPIRED, PAYMENT_REFUNDED, PAYMENT_RECONCILED, PAYMENT_DISPUTED  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 18 states | (none) | `🔴 ER` | No payment or service system |

**V2 Equivalent Check:**
- PRD-015 (Paid Services & Payment) referenced in canonical docs but not implemented
- 13 monetized services defined in Gold but none in V2
- Revenue model: LAWIM never deducts % from transactions

**Action Required:** Full paid services implementation with:
- Service catalog (Boost, Premium, Agent Pro/Business, Leads, Diaspora packages)
- Payment sub-state machine with 10 states
- Campay integration for payments (Cameroonian payment processor)

---

### 2.09 Disputes, Claims & Incidents Lifecycle

**Entity:** `incident`  
**Gold States (8):** Signalement → Qualification → Analyse → Collecte des informations → Décision → Résolution → Clôture → Archivage  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 8 states | (none) | `🔴 ER` | No incident management system |

**Priority Levels (Gold):**
- Critique: Immediate handling
- Élevée: < 24h
- Normale: < 72h
- Faible: Per support availability

**Incident Types (Gold):** Property unavailable, inaccurate info, visit cancellation, participant absence, post-visit disagreement, non-respect of commitment, contested payment, inappropriate behavior, identity theft, presumed fraud, fake documents, platform abuse

---

### 2.10 Closure, Archiving & Retention Lifecycle

**Entity:** `archived_object`  
**Gold States (4):** Active → Closed → Archived (Operational) → Long-term Archiving  
**V2 States (1):** archived (in each model)

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| Active | (all non-archived) | `🔵 NM` | Implicit — any non-archived state |
| Closed | closed / completed | `🟣 PM` | V2 has entity-specific "closed" |
| Archived (Operational) | archived | `🟣 PM` | Single archive level only |
| Long-term Archiving | (none) | `🔴 ER` | No multi-tier archiving |

**Key Gap:** Gold has 2-tier archiving (operational vs long-term at 3 years). V2 has a single `archived` state. No retention policies or auto-archival exist in V2.

**Gold Principle:** No business data is ever deleted — only archived.

---

### 2.11 Mediation Workflow

**Entity:** `mediation`  
**Gold States (8):** Incident → Proposition de médiation → Acceptation des parties → Nomination du Médiateur LAWIM → Échanges → Proposition de solution → Acceptation / Clôture  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 8 states | (none) | `🔴 ER` | No mediation system |

**Mediator Role (Gold):** Listen, facilitate, explain procedures, seek amicable solution, document exchanges. NEVER impose decision, represent a party, modify dossier history, or render legal judgment.

---

### 2.12 User Identity Lifecycle

**Entity:** `user`  
**Gold States (7):** NEW_USER → SEARCHING_PROPERTY / PROPERTY_OWNER / AGENT / PREMIUM_AGENT → LEAD_CREATED / INACTIVE  
**V2 States:** 0 (role is a free string field)

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| NEW_USER | user.role="user" | `🟣 PM` | Basic user created, no lifecycle tracking |
| SEARCHING_PROPERTY | (none) | `🔴 ER` | No user intent tracking |
| PROPERTY_OWNER | (none) | `🔴 ER` | No owner role distinction |
| AGENT | user.role="agent" | `🔵 NM` | Matches naming |
| PREMIUM_AGENT | (none) | `🔴 ER` | No subscription/premium system |
| LEAD_CREATED | (none) | `🔴 ER` | No CRM lead system |
| INACTIVE | (none) | `🔴 ER` | No user inactivity lifecycle |

**Gold Features Missing in V2:**
- 6-level Trust Score (New account → Phone verified → Identity verified → Professional docs → Verified professional → Reference account)
- Automatic evolution paths (Demandeur → Propriétaire → Détenteur → Agent → Responsable d'agence)
- Identity verification documents (CNI, Passport, Residence permit)
- Inactivity timeout and reactivation campaign

---

### 2.13 Organization/Agency Lifecycle

**Entity:** `organization`  
**Gold States (8):** Demande → Saisie des informations → Téléversement des justificatifs → Contrôle automatique → Contrôle LAWIM → Validation → Organisation active / Dissoute  
**V2 States:** None (organization.kind = "agency" string)

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 8 states | (none in state machine) | `🔵 NM` | Organization model exists but no lifecycle states |

**V2 Equivalent:**
- Prisma `Organization` model exists with: id, name, slug, kind, city
- No validation workflow, no document upload tracking, no agent minimum enforcement
- kind is a free string (no controlled vocabulary enforcement)

**Gold Requirements:**
- Minimum 3 active agents for "fully operational" status
- Document verification (CNI, RCCM, tax ID, business license)
- Automated + manual review workflow
- Dissolution checks for open dossiers, properties, services, payments

---

### 2.14 Agent Invitation Workflow

**Entity:** `agent_invitation`  
**Gold States (7):** Invitation → Secure Link → Account Creation → Phone Verified → CNI Uploaded → LAWIM Validation → Agent actif  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 7 states | (none) | `🔴 ER` | No agent invitation/onboarding workflow |

**Member Departure Rules (Gold):** Remove org permissions, keep personal history and audit traces, transfer open dossiers per defined rules, user account remains active.

---

### 2.15 Publication (SIE-Enriched)

**Entity:** `publication`  
**Gold States (11):** Création → Validation → Génération Reference Code → Association Campagne → Association Acteur → Association Biens → Association Services → Publication sur le canal → Journalisation → Mise à jour des statistiques → Disponibilité des dashboards  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 11 states | (none) | `🔴 ER` | No SIE publication pipeline |

**Key Concept:** SIE (Système d'Information Externalisé) reference code generation is a mandatory step before publication.

---

### 2.16 Redirection (SIE-Enriched)

**Entity:** `redirection`  
**Gold States (12):** Utilisateur → Clic sur le lien → Validation du Reference Code → Contrôle d'intégrité → Détection bot → Détection doublon → Journalisation → Création éventuelle d'une session → Redirection → Mise à jour des statistiques → Événement au Reporting → Événement au Continuous Learning  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 12 states | (none) | `🔴 ER` | No redirection/click tracking pipeline |

---

### 2.17 Conversion & Attribution (SIE-Enriched)

**Entity:** `conversion`  
**Gold States (12):** Publication → Clic → Redirection → Visite → Création éventuelle du compte → Conversation → Matching → Visite terrain → Service LAWIM → Paiement Campay → Conversion → Historisation  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 12 states | (none) | `🔴 ER` | No conversion attribution pipeline |

**Attribution Model:** Last-touch attribution (final conversion step before Historisation is the attributed source).

---

### 2.18 CRM Pipeline (8 Stages)

**Entity:** `lead`  
**Gold Stages (8):** incoming_message → normalize_text → extract_entities → detect_intent → context_enrichment → lead_scoring → lead_classification → crm_routing  
**V2 States:** None

| Gold Stage | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 8 stages | (none) | `🔴 ER` | No CRM pipeline |

**V2 Equivalent Check:**
- No Lead model in Prisma
- No lead scoring, classification, or routing
- Intent detection referenced but not implemented as pipeline

**Gold Lead Types with Base Scores:**
- tenant(40), buyer(60), seller(50), investor(80), diaspora_investor(95)

**Score Boosters:** Budget detected(+15), City detected(+10), Neighborhood(+10), Urgency(+20), Diaspora(+25), Cash purchase(+15)

**Score Penalties:** Missing budget(-10), Unclear location(-10), Spam-like(-50), Too short(-20), External links(-30)

**SLA by Priority:**
- P0 (diaspora_investor, buyer > 50M): < 30 min
- P1 (seller, land_buyer): < 2h
- P2 (standard buyer/investor): < 24h
- P3 (tenant, non-qualified): J+1 to J+7

---

### 2.19 Agent Opt-In Workflow

**Entity:** `agent_opt_in`  
**Gold States (4):** Detection → Opt-In Request → Opt-In Response Logged → Sharing Active  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 4 states | (none) | `🔴 ER` | No opt-in mechanism |

**Flow:** System detects agent from message patterns → Asks "Voulez-vous recevoir des leads?" → Logs response → Activates lead sharing if accepted.

---

### 2.20 Identity Resolution Workflow

**Entity:** `identity_resolution`  
**Gold States (5):** Potential Match Detected → Confidence Evaluation → Human Review (if needed) → Merged / False Positive Discarded  
**V2 States:** None

| Gold State | V2 Mapping | Status | Rationale |
|---|---|---|---|
| All 5 states | (none) | `🔴 ER` | No identity resolution |

**Matching Signals (Gold):** Phone, email, name, device fingerprint.

---

### 2.21 Main Cross-Cutting Workflow

**Entity:** `real_estate_project`  
**Gold States (9):** Projet immobilier → Création du dossier → Qualification → Matching → Mise en relation → Visite → Négociation → Transaction → Clôture → Archivage  
**V2 States:** None (distributed across project, property, conversation)

| Gold Stage | V2 Mapping | Status | Rationale |
|---|---|---|---|
| Projet immobilier | project:draft | `🟣 PM` | Project creation |
| Création du dossier | project:draft | `🟣 PM` | Same entity |
| Qualification | project step:qualification | `🟣 PM` | Journey step |
| Matching | (none) | `🔴 ER` | No orchestrator |
| Mise en relation | (none) | `🔴 ER` | No orchestrator |
| Visite | project step:visit | `🟣 PM` | Journey step only |
| Négociation | conversation stage | `🟣 PM` | Delegated |
| Transaction | (none) | `🔴 ER` | No orchestrator |
| Clôture | project:completed | `🟣 PM` | Partial |
| Archivage | project:archived | `🟣 PM` | Partial |

**Key Gap:** V2 has no orchestrator workflow. The project model has journey steps but no state machine that orchestrates the end-to-end real estate project lifecycle with delegation to sub-workflows. Gold defines this as the master workflow that delegates to all sub-workflows (Dossier, Matching, Contact, Visit, Negotiation, Transaction, Closure).

---

## 3. Cross-Cutting Workflow Mapping

| Cross-Cutting Concern | Gold | V2 | Status |
|---|---|---|---|
| Event Sourcing | 21 workflows emit typed audit events | Generic Event model (kind, payload) | `🟣 PM` |
| SLA Monitoring | Per-entity, per-state SLA registry with breach detection | None | `🔴 ER` |
| NBA Engine | 9-level priority NBA per state | `derive_next_actions()` only | `🔴 ER` |
| Health Scoring | Property Health Score, Dossier Health SLA | None | `🔴 ER` |
| Double Consent | Mandatory for contact establishment | None | `🔴 ER` |
| Holder Silence Escalation | 3-tier reminder → auto-close → rematch | None | `🔴 ER` |
| Rematching | Automatic on refusal, visit failure, negotiation failure | None | `🔴 ER` |
| Interlocutor Shift | AI → Human after Mise en Relation | None | `🔴 ER` |
| Retention Policies | 2-tier archive (operational + long-term at 3y) | Single archived state | `🔴 ER` |
| Trust Score | 6-level user trust | None | `🔴 ER` |
| Lead Scoring | Base + boosters - penalties = numeric score → class | None | `🔴 ER` |
| SIE Integration | Reference code, campaign, actor, property association | None | `🔴 ER` |
| Conversion Attribution | Last-touch attribution pipeline | None | `🔴 ER` |

---

## 4. SLA Comparison

| Entity | Gold SLAs | V2 SLAs | Gap |
|---|---|---|---|
| Property | 13 SLA rules per state + per property type rotation (24h→1095d) | None | `🔴 ER` |
| Dossier/Project | 8 SLA rules per state + per property type | None | `🔴 ER` |
| Lead | 5 classification SLAs + 4 priority SLAs (30min→7d) | None | `🔴 ER` |
| Incident | 4 priority SLAs (Immediate→72h) | None | `🔴 ER` |
| Visit | Pre-visit (24h, 2h), post-visit (24h) reminders | None | `🔴 ER` |
| User Identity | New user (7d), inactivity (90d), verification (24h→7d) | None | `🔴 ER` |
| Negotiation | Follow-up J1, J7, J30, J90 | None | `🔴 ER` |

**SLA Monitoring Infrastructure (Gold):**
- SLA Registry with configurable thresholds per entity type/state/property type
- Breach detection with configurable check frequency (1min→24h)
- 3-tier escalation per SLA (NOTIFY → NBA_RECALCULATE → ESCALATE)
- Breach history table
- Market rotation durations per property type (14 types)
- Constitutional rules: no entity shall remain without action beyond SLA

---

## 5. NBA (Next Best Action) Comparison

| Entity/State | Gold NBA | V2 NBA | Gap |
|---|---|---|---|
| Property - Création | Complete required fields | None | `🔴 ER` |
| Property - Disponible | Suggest price reduction, new photos, broaden matching, premium visibility | None | `🔴 ER` |
| Dossier - Création | Ask qualifying questions | None | `🔴 ER` |
| Dossier - Présentation | Present properties | None | `🔴 ER` |
| Dossier - Attente décision | Wait/Follow up | None | `🔴 ER` |
| Visit - Réalisée | Open negotiation / second visit / propose another / rematch | None | `🔴 ER` |
| General | 9-level NBA priority + SLA breach escalation | `derive_next_actions()` for pending steps | `🔴 ER` |

**Gold NBA Priority Levels:**
1. CORRECT_INCOHERENCE
2. COMPLETE_CRITICAL_FIELD
3. LAUNCH_MATCHING
4. PRESENT_PROPERTY
5. CONTACT_HOLDER
6. ORGANIZE_VISIT
7. FOLLOW_UP
8. NOTIFICATIONS
9. HUMAN_ESCALATION

---

## 6. Gap Analysis Summary

### Critical Gaps (Blocking Core Business Logic)

| # | Gap | Impact | Workflows Affected |
|---|---|---|---|
| 1 | No Matching Lifecycle | Platform cannot algorithmically match demandeurs with properties | 02, 03, 04, 21 |
| 2 | No Visit Lifecycle | Cannot schedule, confirm, track or follow up on visits | 01, 02, 05, 21 |
| 3 | No Transaction Lifecycle | Cannot process sale/rental transactions end-to-end | 01, 02, 06, 07, 21 |
| 4 | No CRM Pipeline | Cannot score, classify, or route leads | 12, 18, 19, 20 |
| 5 | No Cross-Cutting Orchestrator | No master workflow to coordinate sub-workflows | 21 (all) |
| 6 | No SLA Monitoring | No enforcement of timing guarantees | All 21 workflows |
| 7 | No NBA Engine | No intelligent next-action recommendation | All 21 workflows |
| 8 | No Payment Lifecycle | Cannot process platform service payments | 08 |

### High Priority Gaps

| # | Gap | Impact | Workflows Affected |
|---|---|---|---|
| 9 | No Double Consent Workflow | Cannot enforce consent before contact | 04 |
| 10 | No Disputes/Incidents System | Cannot handle claims, fraud, or disputes | 09, 11 |
| 11 | No SIE Integration Pipeline | No reference code generation or external system integration | 15, 16, 17 |
| 12 | No Conversion Attribution | Cannot track marketing ROI | 17 |
| 13 | Incomplete Property States | Missing qualification, validation, matching, reactivation states | 01 |
| 14 | Incomplete Dossier/Project States | Missing presentation, wait states, double consent | 02 |
| 15 | No Agent Onboarding Workflow | No structured agent invitation and validation | 14 |

### Medium Priority Gaps

| # | Gap | Impact | Workflows Affected |
|---|---|---|---|
| 16 | No User Identity Lifecycle | Cannot track user intent evolution or trust score | 12 |
| 17 | No Organization Validation Workflow | No structured agency creation and validation | 13 |
| 18 | No Multi-tier Archiving | No long-term retention policy enforcement | 10 |
| 19 | No Agent Opt-In | Cannot manage agent lead-sharing preferences | 19 |
| 20 | No Identity Resolution | Risk of duplicate user records | 20 |
| 21 | No Premium/Subscription Model | Cannot monetize agent services | 12 |

---

## 7. Recommended Implementation Priority

| Phase | Workflows | Effort | Dependencies |
|---|---|---|---|
| **Phase 1: Foundation** | 03 (Matching), 05 (Visit), 18 (CRM Pipeline) | High | Domain model extensions |
| **Phase 2: Core Business** | 01 (Property enrichment), 02 (Dossier), 06 (Negotiation), 07 (Transaction) | High | Phase 1 matching + visit |
| **Phase 3: Cross-Cutting** | 21 (Orchestrator), SLA, NBA | High | Phase 1 + 2 |
| **Phase 4: Monetization** | 08 (Paid Services), 12 (User Identity), 19 (Opt-In) | Medium | Phase 2 transactions |
| **Phase 5: Trust & Safety** | 09 (Incidents), 11 (Mediation), 20 (Identity Resolution) | Medium | Phase 1 + 2 |
| **Phase 6: Operations** | 10 (Archiving), 13 (Org Lifecycle), 14 (Agent Invitation) | Low | Phase 2 |
| **Phase 7: Analytics** | 15 (Publication), 16 (Redirection), 17 (Conversion) | Medium | SIE integration |

---

## Appendix A: V2 Current State Machine Definitions

### A.1 Property Statuses (property_domain.py)
```
PROPERTY_STATUSES = {draft, open, closed, published, archived}
AVAILABILITY_STATUSES = {available, reserved, sold, rented, unavailable}

STATUS_TRANSITIONS:
  draft → {draft, open, closed, published, archived}
  open → {open, published, closed, archived}
  published → {published, closed, archived}
  closed → {closed, archived}
  archived → {archived}
```

### A.2 Project Statuses (project_domain.py)
```
PROJECT_STATUSES = {draft, active, paused, completed, archived}
STEP_STATUSES = {pending, in_progress, completed, skipped, blocked}

STATUS_TRANSITIONS:
  draft → {draft, active, archived}
  active → {active, paused, completed, archived}
  paused → {paused, active, archived}
  completed → {completed, archived}
  archived → {archived}
```

### A.3 Conversation Statuses (conversation_domain.py)
```
CONVERSATION_STATUSES = {open, closed, archived}
NEGOTIATION_STAGES = {inquiry, offer, counter, accepted, declined, closed}

STATUS_TRANSITIONS:
  open → {open, closed, archived}
  closed → {closed, archived, open}
  archived → {archived}

STAGE_TRANSITIONS:
  inquiry → {inquiry, offer, declined, closed}
  offer → {offer, counter, accepted, declined, closed}
  counter → {counter, offer, accepted, declined, closed}
  accepted → {accepted, closed}
  declined → {declined, closed}
  closed → {closed}
```

## Appendix B: Mapping Status Distribution

| Status | Count | Workflows |
|---|---|---|
| 🟢 EXACT_MATCH | 0 | — |
| 🔵 NORMALIZED_MATCH | 1 | 13 (Organization/Agency) |
| 🟡 ONE_TO_MANY | 0 | — |
| 🟠 MANY_TO_ONE | 1 | 10 (Closure/Archiving) |
| 🟣 PARTIAL_MATCH | 5 | 01 (Property), 02 (Dossier), 04 (Mise en Relation), 06 (Negotiation), 12 (User Identity) |
| 🔴 EXTENSION_REQUIRED | 14 | 03, 05, 07, 08, 09, 11, 14, 15, 16, 17, 18, 19, 20, 21 |
| ⚪ OBSOLETE | 0 | — |
| ⛔ CONFLICT | 0 | — |
| ⚠️ HUMAN_DECISION | 0 | — |
| ❓ UNMAPPED | 0 | — |

**Total: 21 workflows mapped, 0 unresolved.**
