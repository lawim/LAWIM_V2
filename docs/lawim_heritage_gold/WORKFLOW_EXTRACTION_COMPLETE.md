# WORKFLOW EXTRACTION — LAWIM Heritage Completion Mission H0.4
## Comprehensive Business Workflow Knowledge Extraction

**Extraction Date:** 2026-07-15  
**Extraction Agent:** Workflow Historian  
**Status:** COMPLETE — All heritage sources explored

---

# TABLE OF CONTENTS

1. [Complete List of Workflows Discovered](#1-complete-list-of-workflows-discovered)
2. [Workflow: Property Lifecycle](#2-workflow-property-lifecycle)
3. [Workflow: Dossier (Case) Lifecycle](#3-workflow-dossier-case-lifecycle)
4. [Workflow: Matching Lifecycle](#4-workflow-matching-lifecycle)
5. [Workflow: Mise en Relation (Contact) Lifecycle](#5-workflow-mise-en-relation-contact-lifecycle)
6. [Workflow: Visit Lifecycle](#6-workflow-visit-lifecycle)
7. [Workflow: Negotiation Lifecycle](#7-workflow-negotiation-lifecycle)
8. [Workflow: Transaction Lifecycle](#8-workflow-transaction-lifecycle)
9. [Workflow: Paid Services & Payment Lifecycle](#9-workflow-paid-services--payment-lifecycle)
10. [Workflow: Disputes, Claims & Incidents Lifecycle](#10-workflow-disputes-claims--incidents-lifecycle)
11. [Workflow: Closure, Archiving & Retention Lifecycle](#11-workflow-closure-archiving--retention-lifecycle)
12. [Workflow: User Identity Lifecycle](#12-workflow-user-identity-lifecycle)
13. [Workflow: Publication (SIE-Enriched)](#13-workflow-publication-sie-enriched)
14. [Workflow: Redirection (SIE-Enriched)](#14-workflow-redirection-sie-enriched)
15. [Workflow: Conversion & Attribution (SIE-Enriched)](#15-workflow-conversion--attribution-sie-enriched)
16. [Workflow: Mediation](#16-workflow-mediation)
17. [Workflow: Organization (Agency) Lifecycle](#17-workflow-organization-agency-lifecycle)
18. [Workflow: Agent Invitation](#18-workflow-agent-invitation)
19. [Workflow: CRM Pipeline (8 Stages)](#19-workflow-crm-pipeline-8-stages)
20. [Next Best Action (NBA) Rules](#20-next-best-action-nba-rules)
21. [Progressive Search Expansion Rules](#21-progressive-search-expansion-rules)
22. [Continuous Market Surveillance Rules](#22-continuous-market-surveillance-rules)
23. [Health Scores Definitions](#23-health-scores-definitions)
24. [SLA Tables](#24-sla-tables)
25. [Business Rules Related to Workflows](#25-business-rules-related-to-workflows)
26. [State Machine Diagrams (Text-Based)](#26-state-machine-diagrams-text-based)
27. [Source References](#27-source-references)

---

# 1. COMPLETE LIST OF WORKFLOWS DISCOVERED

| # | Workflow Name | Source Document | Section |
|---|---|---|---|
| 1 | **Property Lifecycle** (Cycle de vie des biens) | 05-WORKFLOW-REFERENCE.md | Part 3 (Ch34-51) |
| 2 | **Dossier/Case Lifecycle** (Cycle de vie des dossiers) | 05-WORKFLOW-REFERENCE.md | Part 4 (Ch52-73) |
| 3 | **Matching Lifecycle** (Cycle de matching) | 05-WORKFLOW-REFERENCE.md | Part 1 (Ch5); 04-MATCHING-REFERENCE.md |
| 4 | **Mise en Relation / Contact Lifecycle** | 05-WORKFLOW-REFERENCE.md | Part 5 (Ch74-89) |
| 5 | **Visit Lifecycle** (Cycle des visites) | 05-WORKFLOW-REFERENCE.md | Part 6 (Ch90-108) |
| 6 | **Negotiation Lifecycle** (Cycle des négociations) | 05-WORKFLOW-REFERENCE.md | Part 7 (Ch109-127) |
| 7 | **Transaction Lifecycle** (Cycle des transactions) | 05-WORKFLOW-REFERENCE.md | Part 8 (Ch128-145) |
| 8 | **Paid Services & Payment Lifecycle** | 05-WORKFLOW-REFERENCE.md | Part 9 (Ch147-163) |
| 9 | **Disputes, Claims & Incidents Lifecycle** | 05-WORKFLOW-REFERENCE.md | Part 10 (Ch164-181) |
| 10 | **Closure, Archiving & Retention Lifecycle** | 05-WORKFLOW-REFERENCE.md | Part 11 (Ch182-194) |
| 11 | **Mediation Workflow** | 05-WORKFLOW-REFERENCE.md | Ch195 |
| 12 | **User Identity Lifecycle** | 08-ROLE-REFERENCE.md | Part 2 (Ch16-30) |
| 13 | **Organization/Agency Lifecycle** | 08-ROLE-REFERENCE.md | Part 6 (Ch75-89) |
| 14 | **Agent Invitation Workflow** | 08-ROLE-REFERENCE.md | Ch24, Ch82 |
| 15 | **Publication (SIE-Enriched)** | 05-WORKFLOW-REFERENCE.md | Ch212 |
| 16 | **Redirection (SIE-Enriched)** | 05-WORKFLOW-REFERENCE.md | Ch213 |
| 17 | **Conversion & Attribution** | 05-WORKFLOW-REFERENCE.md | Ch214 |
| 18 | **CRM Pipeline (8 stages)** | CRM_MODEL.md | Sec 1 |
| 19 | **Agent Opt-In Workflow** | CRM_MODEL.md | Sec 11 |
| 20 | **Identity Resolution Workflow** | CRM_MODEL.md | Sec 8 |
| 21 | **Main Cross-cutting Workflow** | 05-WORKFLOW-REFERENCE.md | Ch203 |

---

# 2. WORKFLOW: PROPERTY LIFECYCLE

**Source:** 05-WORKFLOW-REFERENCE.md — Part 3 (Ch34-51) — **Confidence: HIGH**

## States

```
Création (Creation)
    ↓
Qualification (Qualification)
    ↓
Validation (Validation)
    ↓
Publié (Published)
    ↓
Disponible (Available)
    ↓
Matching (Matching)
    ↓
Visites (Visits)
    ↓
Négociation (Negotiation)
    ↓
Réservé (Reserved)
    ↓
Transaction (Transaction)
    ↓
Indisponible (Unavailable)
    ↓
Réactivation éventuelle (Possible Reactivation)
    ↓
Archivé (Archived)
```

## Events & Transitions

| From | To | Event | Condition |
|---|---|---|---|
| Création | Qualification | Field completion | Champs obligatoires vérifiés (02-PROPERTY-REFERENCE.md) |
| Qualification | Validation | Enrichment complete | Property Health Score calculated |
| Validation | Publié | Validation success | Coherence, conformity, uniqueness, availability checks passed |
| Publié | Disponible | Status set | Availability declared |
| Disponible | Matching | Automatic | System computes compatible dossiers; Match Count, Avg Score, Attractiveness Score |
| Matching | Visites | Demandeur accepts | Proposition accepted |
| Visites | Négociation | Positive visit | Visitor satisfied |
| Négociation | Réservé | Agreement in principle | Price/terms agreed |
| Réservé | Transaction | Finalization | Sale or rental finalized |
| Transaction | Indisponible | Sold/rented | Status set to Vendu/Loué |
| Indisponible | Disponible | Reactivation | End of lease, cancellation, withdrawal of compromise |
| Indisponible/Disponible | Archivé | Archival request or rule | Owner request, obsolescence, archival rules reached |

## Availability Status Values

- Disponible (Available)
- Réservé (Reserved)
- Sous négociation (Under negotiation)
- Sous compromis (Under compromise)
- Loué (Rented)
- Vendu (Sold)
- Suspendu (Suspended)
- Archivé (Archived)

## SLA: Market Rotation by Property Type (Reference Values)

| Type | Normal Rotation |
|---|---|
| Chambre | 1-4 weeks |
| Studio | 2-8 weeks |
| Appartement | 1-4 months |
| Villa | 3-12 months |
| Terrain résidentiel | 3-18 months |
| Terrain agricole | 6-36 months |
| Commerce | 1-6 months |
| Bureau | 2-8 months |
| Hôtel | 6-36 months |

## NBA (Next Best Actions) for Property

- Demand confirmation of availability
- Suggest price reduction
- Recommend new photos
- Request additional information
- Broaden matching
- Propose premium visibility
- Temporarily suspend listing
- Archive property

## Corrective Actions (when commercialization exceeds normal duration)

System automatically triggers a diagnostic analyzing: price, photo quality, description, real availability, owner activity, match count, visit count, refusal count.

---

# 3. WORKFLOW: DOSSIER (CASE) LIFECYCLE

**Source:** 05-WORKFLOW-REFERENCE.md — Part 4 (Ch52-73) — **Confidence: HIGH**

## States

```
Création (Creation)
    ↓
Qualification (Qualification)
    ↓
Matching (Matching)
    ↓
Présentation (Presentation)
    ↓
Attente décision demandeur (Waiting for decision: demandeur)
    ↓
Contact détenteur (Contact holder)
    ↓
Attente décision détenteur (Waiting for decision: holder)
    ↓
Mise en relation (Contact established)
    ↓
Visite (Visit)
    ↓
Négociation (Negotiation)
    ↓
Accord (Agreement)
    ↓
Transaction (Transaction)
    ↓
Clôture (Closure)
    ↓
Archivage (Archiving)
```

## Key Rules

- Dossier is created when a user expresses a real estate need
- Creation sources: Web, WhatsApp, Telegram, Mobile App, LAWIM collaborator
- Each dossier receives: creation date, responsible (LAWIM AI), priority level, NBA
- Qualification collects progressively, never as a form
- Matching starts as soon as critical fields are known
- No state can be deleted
- Dossier can be reopened after closure (new search, cancelled transaction, return of need)

## NBA for Dossier

- Ask a question
- Launch matching
- Organize a visit
- Follow up with holder
- Wait for a response
- Open negotiation
- Close

## Reopening Conditions

- New search
- Transaction cancelled
- Return of a need

## SLA by State

| State | Max Delay |
|---|---|
| Matching | ≤ Immediate |
| Waiting for holder | Based on property type |
| Waiting for demandeur | Based on urgency level |
| Scheduled visit | Automatic follow-up until realization |

---

# 4. WORKFLOW: MATCHING LIFECYCLE

**Source:** 04-MATCHING-REFERENCE.md (full); 04-DECISION-ENGINE-REFERENCE.md (Part 3-6); 05-WORKFLOW-REFERENCE.md — **Confidence: HIGH**

## Core Algorithm

```
1. Load dossier
    ↓
2. Check critical fields
    ↓
3. Select compatible properties
    ↓
4. Eliminate incompatible properties
    ↓
5. Calculate scores
    ↓
6. Rank properties
    ↓
7. Propose the best
    ↓
8. Wait for decision
    ↓
9. Learn
    ↓
10. Recalculate if necessary
```

## Four Levels of Compatibility

| Level | Name | Description |
|---|---|---|
| 1 | **Critical** | Mandatory fields per 02-PROPERTY-REFERENCE.md. No match possible without these. |
| 2 | **Functional** | Meets core needs (bedrooms, surface, budget, property type) |
| 3 | **Comfort** | Appreciated but not indispensable (garage, borehole, garden, pool, balcony, terrace) |
| 4 | **Preferential** | Observed preferences (preferred neighborhood, orientation, view, school proximity, work proximity) |

## Triggers for Matching

- Dossier creation
- Correction
- Budget modification
- City change
- Property type change
- New property publication
- Property becomes available
- Refusal
- Visit
- Failed negotiation

## Triggers for Rematching

**Demandeur side:**
- Budget modification, city change, neighborhood change, property type change, new criteria, criterion removal, property refusal, visit abandonment, new preference

**Property side:**
- Publication, modification, price decrease/increase, availability change, photo addition, GPS addition, document addition, qualification improvement

**Holder side:**
- Acceptance, refusal, no response, temporary unavailability, return to availability

**System side:**
- New business rule, periodic recalculation, global learning, data correction

## Matching Scores (04-MATCHING-REFERENCE Part 3)

### Real Estate Score (Ch26)

| Criterion | Weight |
|---|---|
| Property Type | 25% |
| Operation | 20% |
| Budget | 15% |
| Location | 15% |
| Critical Characteristics | 15% |
| Recommended Characteristics | 10% |
| **Minimum threshold: 60%** | |

### Availability Score (Ch28)
- 100% = Available
- 70% = Reservation in progress
- 30% = Owner response pending
- 0% = Sold/Rented/Archived

### Document Score (Ch29)
- Titre foncier (Land title) = 100%
- En cours d'immatriculation = 80%
- Droit coutumier (Customary law) = 60%
- Documents inconnus = 40%

### Holder Reliability Score (Ch31)
- Average response time × Acceptance rate × Visits honored × Transactions completed

### Transaction Success Score (Ch90)

| Indicator | Weight |
|---|---|
| Real Estate Compatibility | 30% |
| Geographic Compatibility | 15% |
| Real Availability | 10% |
| Document Situation | 10% |
| Holder Reactivity | 10% |
| Demandeur History | 10% |
| Financial Feasibility | 10% |
| Negotiation Probability | 5% |

## Decision Engine Priority (Ch88)

| Priority | Action |
|---|---|
| 1 | Correct an incoherence |
| 2 | Complete a critical field |
| 3 | Matching |
| 4 | Present a property |
| 5 | Contact the holder |
| 6 | Organize a visit |
| 7 | Follow up |
| 8 | Notifications |
| 9 | Dossier optimization |

## Authorized Decision Engine Actions (Ch86)

1. Ask a question
2. Launch matching
3. Launch rematching
4. Present a property
5. Present several properties
6. Contact the holder
7. Organize a visit
8. Schedule a follow-up
9. Notify
10. Open negotiation
11. Request a document
12. Close the dossier

---

# 5. WORKFLOW: MISE EN RELATION (CONTACT) LIFECYCLE

**Source:** 05-WORKFLOW-REFERENCE.md — Part 5 (Ch74-89) — **Confidence: HIGH**

## Principles

- Double consent required: demandeur interested AND holder favorable
- LAWIM never transmits holder coordinates without rules
- Four objectives: protect demandeur, protect holder, maximize transaction chances, maintain traceability

## Mandatory Conditions

✓ Dossier active  
✓ Property available  
✓ Demandeur confirms interest  
✓ Holder accepts contact  

## Process

```
Matching
    ↓
Demandeur interested
    ↓
Holder contacted
    ↓
Holder decision (accept/refuse/delay/alternative/declare unavailable)
    ↓
Double consent obtained → Mise en relation
    ↓
Change of interlocutor visible (🤖 LAWIM AI → 👤 Propriétaire/🏢 Agence/etc.)
```

## Holder Silence Workflow

```
First reminder
    ↓
Second reminder
    ↓
Last reminder
    ↓
Property marked "to confirm"
    ↓
Rematching
```

## Interlocutor Identities Displayed

- 🤖 LAWIM AI
- 👤 Propriétaire (Owner)
- 🏢 Agence (Agency)
- 🤝 Introduceur (Introducer)
- 👨🏽‍💼 Conseiller LAWIM (LAWIM Advisor)
- 🛠 Support LAWIM

## Possible Outcomes

- Scheduled visit
- Request for additional information
- Negotiation
- Refusal
- Abandonment
- Rematching

---

# 6. WORKFLOW: VISIT LIFECYCLE

**Source:** 05-WORKFLOW-REFERENCE.md — Part 6 (Ch90-108) — **Confidence: HIGH**

## Preconditions

✓ Property available  
✓ Demandeur expressed interest  
✓ Holder accepts visit  
✓ Dossier active  

## Authorized Statuses

- Demandée (Requested)
- En attente de confirmation (Awaiting confirmation)
- Confirmée (Confirmed)
- Reportée (Postponed)
- Annulée (Cancelled)
- Réalisée (Realized)
- Refusée (Refused)
- Absence du demandeur (Demandeur absent)
- Absence du détenteur (Holder absent)

## Automatic Reminders

- 24 hours before visit
- 2 hours before visit
- Configurable additional reminders
- Sent to: demandeur, holder, concerned LAWIM collaborator

## Visit Result - Demandeur Satisfaction

- Très satisfait (Very satisfied)
- Satisfait (Satisfied)
- Mitigé (Mixed)
- Insatisfait (Dissatisfied)

## Post-Visit Decision (NBA)

- Open negotiation
- Schedule a second visit
- Propose another property
- Launch rematching
- Close this proposition

## Absence Handling

**Demandeur absent:** System records, informs holder, proposes new date  
**Holder absent:** System informs demandeur, decreases holder reliability score, proposes new date or alternative property

## Indicators

- Time before first visit
- Confirmation rate
- Cancellation rate
- Absence rate
- Satisfaction rate
- Transformation rate to negotiation

---

# 7. WORKFLOW: NEGOTIATION LIFECYCLE

**Source:** 05-WORKFLOW-REFERENCE.md — Part 7 (Ch109-127) — **Confidence: HIGH**

## Opening Conditions

✓ Satisfactory visit occurred  
OR  
✓ Both parties wish to negotiate without visit  
✓ Dossier active  
✓ Property available  

## States

```
Ouverte (Open)
    ↓
En discussion (In discussion)
    ↓
Offre (Offer)
    ↓
Contre-offre (Counter-offer)
    ↓
Accord de principe (Agreement in principle)
    ↓
Accord final (Final agreement)
    ↓
Transaction (Transaction)
    
    OR
    
Échec (Failure)
    ↓
Rematching
```

## Negotiable Elements

**Sale:** Price, payment terms, deadlines, included furniture, equipment, release date  
**Rental:** Rent, deposit, advance, lease duration, entry date, possible works  
**Land:** Price, boundary marking, documents, deadlines  
**Commercial:** Rent, key money, equipment, duration  

## Each Offer Contains

- Identifier, author, date, amount, optional comment, status

## Relances During Negotiation (on silence)

```
First reminder
    ↓
Second reminder
    ↓
Last reminder
    ↓
Automatic closure of negotiation
    ↓
Possible rematching
```

## Failure Conditions

- Parties end exchanges
- Max delay exceeded
- Property becomes unavailable
- Party withdraws

## Post-Failure: Automatic Rematching with Diagnostic

## Indicators

- Average duration, number of offers, number of counter-offers, agreement rate, failure rate, average gap between initial and final price

---

# 8. WORKFLOW: TRANSACTION LIFECYCLE

**Source:** 05-WORKFLOW-REFERENCE.md — Part 8 (Ch128-145) — **Confidence: HIGH**

## Types

- Location (Rental)
- Vente (Sale)
- Achat (Purchase)
- Bail professionnel (Professional lease)
- Bail commercial (Commercial lease)
- Location saisonnière (Seasonal rental)

## Opening Conditions

✓ Dossier active  
✓ Agreement exists  
✓ Property still available  
✓ Parties confirm intention  

## States

```
Accord (Agreement)
    ↓
Préparation (Preparation)
    ↓
Documents (Documents)
    ↓
Paiement (Payment)
    ↓
Signature (Signature)
    ↓
Remise des clés (Key handover)
    ↓
Confirmation (Confirmation)
    ↓
Transaction terminée (Transaction completed)
    ↓
Archivage (Archiving)
```

## Document Management

**Sale:** Land title, ID, possible power of attorney  
**Rental:** Contract, deposit, inventory of fixtures  

## Payment Tracking

- Deposit, caution, first rent, full payment, installments

## Failure Possible Reasons

- Payment abandoned
- Documents impossible to produce
- Party withdrawal

## Post-Transaction Follow-up

- Satisfaction confirmation
- Remaining commitments follow-up
- Statistics update
- Reliability score improvement

---

# 9. WORKFLOW: PAID SERVICES & PAYMENT LIFECYCLE

**Source:** 05-WORKFLOW-REFERENCE.md — Part 9 (Ch147-163) — **Confidence: HIGH**  
**Source:** CRM_MODEL.md — Sec 14 — **Confidence: HIGH**

## Monetized Services (13 documented)

| # | Service | Code | Price (FCFA) |
|---|---|---|---|
| 1 | Boost annonce 7 jours | boost_7j | 2,000 |
| 2 | Boost annonce 30 jours | boost_30j | 5,000 |
| 3 | Premium listing (visibilité max) | premium_listing | 10,000 |
| 4 | Abonnement Agent Pro (mensuel) | agent_pro | 10,000/mois |
| 5 | Abonnement Agent Business (mensuel) | agent_business | 25,000/mois |
| 6 | Lead Bronze (1 contact) | lead_bronze | 500 |
| 7 | Lead Silver (5 contacts) | lead_silver | 1,500 |
| 8 | Lead Gold (15 contacts) | lead_gold | 3,000 |
| 9 | Déblocage coordonnées propriétaire | deblocage_coordonnees | 500 |
| 10 | Demandeur Premium (visibilité prioritaire) | demandeur_premium | 1,000 |
| 11 | Diaspora Simple (accès biens vérifiés) | diaspora_simple | 25,000 |
| 12 | Diaspora Rapport (accompagnement + rapports) | diaspora_rapport | 50,000 |
| 13 | Diaspora Complet (accompagnement total) | diaspora_complet | 75,000 |

## Service Lifecycle States

```
Création (Creation)
    ↓
Proposition (Proposition)
    ↓
Acceptation (Acceptation)
    ↓
Paiement (Payment)
    ↓
Activation (Activation)
    ↓
Utilisation (Usage)
    ↓
Expiration (Expiration)
    ↓
Archivage (Archiving)
```

## Payment States

- `PAYMENT_CREATED`
- `PAYMENT_INITIATED`
- `PAYMENT_PENDING`
- `PAYMENT_CONFIRMED`
- `PAYMENT_FAILED`
- `PAYMENT_CANCELLED`
- `PAYMENT_EXPIRED`
- `PAYMENT_REFUNDED`
- `PAYMENT_RECONCILED`
- `PAYMENT_DISPUTED`

## Activation After Validation Examples

- Mise en relation payment → Authorize contact
- Contact access payment → Coordinates authorized
- Premium publication payment → Listing promoted
- Boost payment → Priority in results
- Verification payment → Control triggered
- Assistance payment → Accompaniment activated

## Key Rule

> LAWIM never deducts a percentage from the final transaction price. Revenue comes exclusively from platform services.

---

# 10. WORKFLOW: DISPUTES, CLAIMS & INCIDENTS LIFECYCLE

**Source:** 05-WORKFLOW-REFERENCE.md — Part 10 (Ch164-181) — **Confidence: HIGH**

## Incident Types

- Property became unavailable
- Inaccurate information
- Visit cancellation
- Participant absence
- Post-visit disagreement
- Non-respect of commitment
- Contested service payment
- Inappropriate behavior
- Identity theft
- Presumed fraud
- Fake documents
- Platform abuse

## Priority Levels

- 🔴 Critique — Immediate handling
- 🟠 Élevée (High) — < 24 hours
- 🟡 Normale (Normal) — < 72 hours
- 🟢 Faible (Low) — According to support availability

## Lifecycle States

```
Signalement (Report)
    ↓
Qualification (Qualification)
    ↓
Analyse (Analysis)
    ↓
Collecte des informations (Information gathering)
    ↓
Décision (Decision)
    ↓
Résolution (Resolution)
    ↓
Clôture (Closure)
    ↓
Archivage (Archiving)
```

## Fraud Suspicion Actions

- Temporarily suspend account
- Suspend property
- Suspend listing
- Suspend contact  
All suspensions are motivated, historized, and reversible after verification.

## User Incident Actions

- Send warning
- Request supporting docs
- Limit functionality
- Temporarily suspend account
- Forward to administrator

## Dossier Suspension Conditions

- Presumed fraud
- Major dispute
- Authority request
- Express party request

---

# 11. WORKFLOW: CLOSURE, ARCHIVING & RETENTION LIFECYCLE

**Source:** 05-WORKFLOW-REFERENCE.md — Part 11 (Ch182-194) — **Confidence: HIGH**

## Key Principle

> No business data is ever deleted in LAWIM.

## Objects Concerned

- Dossiers, properties, conversations, visits, negotiations, transactions, service payments, incidents, notifications, workflows

## Closure Conditions

✓ Objective achieved  
✓ Abandoned  
✓ Permanently without object  
✓ Administrative decision justified  

## Dossier Closure Verification

- No visit pending
- No open negotiation
- No blocked service payment
- No active critical incident

## Archiving States

1. **Archived** (operational) — Not modifiable, not in active workflows, available for audit/statistics/reporting/learning
2. **Long-term archiving** (after 3 years) — Same as archived but also removed from matching; reactivation possible only via authorized administrative procedure

## Reopening Possible

- Cancelled sale
- End of lease
- New request
- Administrative decision

---

# 12. WORKFLOW: USER IDENTITY LIFECYCLE

**Source:** 08-ROLE-REFERENCE.md — Part 2 (Ch16-30) — **Confidence: HIGH**

## States

- NEW_USER → SEARCHING_PROPERTY / PROPERTY_OWNER / INACTIVE
- SEARCHING_PROPERTY → LEAD_CREATED / INACTIVE
- PROPERTY_OWNER → LEAD_CREATED / INACTIVE
- AGENT → PREMIUM_AGENT / INACTIVE
- LEAD_CREATED → SEARCHING_PROPERTY / INACTIVE
- PREMIUM_AGENT → AGENT (if subscription expires)
- INACTIVE → NEW_USER (if reactivated)

## Automatic Evolution Paths

```
Demandeur → Publication of property → Propriétaire
Demandeur → Declaration of property management → Détenteur
Détenteur → Professional validation → Agent immobilier
Agent → Creation of validated agency → Responsable d'agence
```

## Registration Minimum Fields

- Full name
- Unique email
- Unique username
- WhatsApp number (mandatory)
- Password + confirmation
- Preferred language
- Terms acceptance

## Identity Verification Documents

- National ID Card (CNI)
- Passport
- Residence permit (per country)

## Trust Score Levels (6 levels)

| Level | Name | Criteria |
|---|---|---|
| 🔴 Niveau 1 | New account | Just created |
| 🟠 Niveau 2 | Phone verified | Phone confirmed |
| 🟡 Niveau 3 | Identity verified | ID documents validated |
| 🟢 Niveau 4 | Professional documents validated | RCCM, tax ID, etc. |
| 🔵 Niveau 5 | Verified professional/partner | Full professional check |
| ⭐ Niveau 6 | Reference account | Recognized by LAWIM |

## Role Hierarchy

```
Administrateur principal LAWIM
        │
Administrateur LAWIM
        │
Responsable opérationnel
        │
Conseiller / Médiateur
        │
Responsable d'agence
        │
Administrateur d'agence
        │
Agent immobilier
        │
Propriétaire / Détenteur
        │
Demandeur
```

## Family of Roles

**Users:** Demandeur, Détenteur, Propriétaire  
**Professionals:** Agent immobilier, Responsable d'agence, Administrateur d'agence  
**Partners:** Notaire, Géomètre, Banquier, Expert, Prestataire  
**LAWIM Team:** Assistant, Conseiller, Médiateur, Responsable opérationnel, Administrateur, Administrateur principal

---

# 13. WORKFLOW: PUBLICATION (SIE-ENRICHED)

**Source:** 05-WORKFLOW-REFERENCE.md — Ch212 — **Confidence: MEDIUM**

```
Création de la publication
    ↓
Validation
    ↓
Génération automatique du Reference Code via le SIE
    ↓
Association à une campagne éventuelle
    ↓
Association à un acteur
    ↓
Association à un ou plusieurs biens
    ↓
Association à un ou plusieurs services
    ↓
Publication sur le canal
    ↓
Journalisation
    ↓
Mise à jour des statistiques
    ↓
Disponibilité des dashboards
```

---

# 14. WORKFLOW: REDIRECTION (SIE-ENRICHED)

**Source:** 05-WORKFLOW-REFERENCE.md — Ch213 — **Confidence: MEDIUM**

```
Utilisateur
    ↓
Clic sur le lien
    ↓
Validation du Reference Code
    ↓
Contrôle d'intégrité
    ↓
Détection bot
    ↓
Détection doublon
    ↓
Journalisation
    ↓
Création éventuelle d'une session
    ↓
Redirection
    ↓
Mise à jour des statistiques
    ↓
Événement envoyé au Reporting
    ↓
Événement envoyé au Continuous Learning
```

---

# 15. WORKFLOW: CONVERSION & ATTRIBUTION (SIE-ENRICHED)

**Source:** 05-WORKFLOW-REFERENCE.md — Ch214 — **Confidence: MEDIUM**

```
Publication
    ↓
Clic
    ↓
Redirection
    ↓
Visite
    ↓
Création éventuelle du compte
    ↓
Conversation
    ↓
Matching
    ↓
Visite terrain
    ↓
Service LAWIM
    ↓
Paiement Campay confirmé
    ↓
Conversion
    ↓
Historisation
```

---

# 16. WORKFLOW: MEDIATION

**Source:** 05-WORKFLOW-REFERENCE.md — Ch195 — **Confidence: HIGH**

## Lifecycle

```
Incident
    ↓
Proposition de médiation
    ↓
Acceptation des parties
    ↓
Nomination du Médiateur LAWIM
    ↓
Échanges
    ↓
Proposition de solution
    ↓
Acceptation
    ↓
Clôture
```

## Mediator Role

- Listen to parties
- Facilitate dialogue
- Explain LAWIM procedures
- Seek amicable solution
- Document exchanges
- NEVER: impose decision, represent a party, modify dossier history, render legal judgment

## Possible Endings

- Amicable agreement
- Disagreement
- Abandonment
- Referral to competent authority

---

# 17. WORKFLOW: ORGANIZATION (AGENCY) LIFECYCLE

**Source:** 08-ROLE-REFERENCE.md — Part 6 (Ch75-89) — **Confidence: HIGH**

## Creation Workflow

```
Demande
    ↓
Saisie des informations
    ↓
Téléversement des justificatifs
    ↓
Contrôle automatique
    ↓
Contrôle LAWIM
    ↓
Validation
    ↓
Organisation active
```

## Agency Minimum Requirements

- CNI of responsible person
- Verified phone number
- Email address
- Physical address
- Optional: RCCM, tax ID, business license, logo, headquarters proof

## Agency Composition

- Responsable d'agence
- Administrateurs d'agence
- Agents immobiliers
- Optional collaborators

## Minimum Effective: 3 active agents for "fully operational" status

## Dissolution Checks

✓ Open dossiers  
✓ Managed properties  
✓ Services in progress  
✓ Payments  
✓ Legal obligations  

---

# 18. WORKFLOW: AGENT INVITATION

**Source:** 08-ROLE-REFERENCE.md — Ch24, Ch82 — **Confidence: HIGH**

```
Invitation
    ↓
Secure link
    ↓
Account creation
    ↓
Phone verified
    ↓
CNI
    ↓
LAWIM validation
    ↓
Agent active
```

## Member Departure Actions

- Remove organization-linked permissions
- Keep personal history
- Keep audit traces
- Transfer open dossiers per defined rules
- User account remains active

---

# 19. WORKFLOW: CRM PIPELINE (8 STAGES)

**Source:** CRM_MODEL.md — Sec 1 — **Confidence: HIGH**

| Stage | Input | Processing | Output |
|---|---|---|---|
| 1. incoming_message | Raw WhatsApp/TG message | Reception and formatting | Normalized message |
| 2. normalize_text | Normalized message | Orthographic normalization, typo, slang | Cleaned text |
| 3. extract_entities | Cleaned text | Entity extraction (budget, city, property type, phone) | Structured entities |
| 4. detect_intent | Entities + text | Intent classification (buy/rent/sell/invest) | Intent + confidence |
| 5. context_enrichment | Intent + entities | Context enrichment (history, profile, behavior) | Full context |
| 6. lead_scoring | Full context | Score calculation (base + boosters - penalties) | Numeric score |
| 7. lead_classification | Numeric score | HOT/WARM/COLD/LOW/SPAM classification | Class + priority |
| 8. crm_routing | Class + priority | Routing to agent, dashboard, or auto-response | CRM action |

## Lead Types with Base Scores

| Type | Base Score | Description |
|---|---|---|
| tenant | 40 | Potential renter |
| buyer | 60 | Potential buyer |
| seller | 50 | Seller |
| investor | 80 | Investor seeking returns |
| diaspora_investor | 95 | Diaspora investor (high purchasing power + security need) |

## Classification Thresholds

**V1 (Numeric):** HOT ≥ 80, WARM ≥ 60, COLD ≥ 40, LOW < 40, SPAM < 40+patterns  
**V5 (Normalized 0-1):** HOT ≥ 0.8, WARM ≥ 0.5, COLD ≥ 0.3, LOW < 0.3, SPAM ≥ 0.2 (spam rules)

## Recommended Actions per Class

| Class | Priority Action | Delay | Channel |
|---|---|---|---|
| HOT | call_immediately | < 1h | Phone + WhatsApp |
| WARM | send_listings | < 24h | WhatsApp |
| COLD | request_budget | < 48h | WhatsApp |
| LOW | follow_up (periodic) | J+7 / J+30 / J+90 | WhatsApp |
| SPAM | ignore + block if persistent | Immediate | None |

## Lead Priority

| Priority | Types | SLA |
|---|---|---|
| P0 | diaspora_investor, buyer > 50M FCFA | < 30 min |
| P1 | seller, land_buyer | < 2h |
| P2 | standard buyer, standard investor | < 24h |
| P3 | tenant, non-qualified prospect | J+1 to J+7 |

## Score Boosters

| Signal | Bonus |
|---|---|
| Budget detected | +15 |
| City detected | +10 |
| Neighborhood detected | +10 |
| Urgency expressed | +20 |
| Diaspora detected | +25 |
| Cash purchase | +15 |
| Message > 20 chars | +30 |
| Budget present | +25 |
| Location present | +25 |
| Property type present | +20 |
| Visit requested | +20 |
| Document requested | +15 |
| External reference | +10 |

## Score Penalties

| Signal | Malus |
|---|---|
| Missing budget | -10 |
| Unclear location | -10 |
| Spam-like message | -50 |
| Message too short (< 10 chars) | -20 |
| External links | -30 |
| Repetitive behavior | -25 |
| Incomplete contact info | -15 |
| Intent not detected | -20 |

## Behaviors Tracked (CRM)

- message_history
- response_time
- budget_changes
- visit_requests
- property_views
- document_requests
- call_attempts
- referral_source

---

# 20. NEXT BEST ACTION (NBA) RULES

**Source:** 05-WORKFLOW-REFERENCE.md — Ch11, Ch69, Ch160, Ch201 — **Confidence: HIGH**  
**Source:** 04-DECISION-ENGINE-REFERENCE.md — Ch83-88 — **Confidence: HIGH**

## Core Principle

Every business object always has a next optimal action. This action is recalculated after every event. A workflow without a next action is considered defective.

## NBA Calculation Logic (Decision Engine)

The engine applies strict priority order:

```
1. Correct an incoherence
2. Complete a critical field
3. Matching
4. Present a property
5. Contact the holder
6. Organize a visit
7. Follow up (relance)
8. Notifications
9. Dossier optimization
```

## NBA Examples by Object

| Object | Examples of NBA |
|---|---|
| **Property** | Confirm availability, suggest price reduction, recommend photos, broaden matching, propose premium, suspend, archive |
| **Dossier** | Ask question, launch matching, organize visit, follow up holder, wait, open negotiation, close |
| **Visit** | Confirm visit, send reminder, register result, propose negotiation, schedule second visit, rematch |
| **Negotiation** | Send reminder, prepare documents, propose counter-offer, close negotiation, rematch |
| **Transaction** | Prepare documents, verify identity, track payment, register signature, confirm completion |
| **Payment Service** | Wait for payment, activate service, follow up client, verify validation, expire service |

## Decision Engine Reaction Events

**Demandeur:** new message, correction, new criterion, refusal, acceptance, visit, negotiation  
**Property:** publication, modification, price decrease, withdrawal, sale, rental, new availability  
**Holder:** response, refusal, acceptance, unavailability, silence  
**System:** deadline expiration, scheduled reminder, periodic recalculation, learning

## Absolute Rule

> No active dossier, no published property, no transaction shall remain without action beyond the applicable SLA. If exceeded, LAWIM MUST trigger an appropriate action. Inaction is considered an operational anomaly.

---

# 21. PROGRESSIVE SEARCH EXPANSION RULES

**Source:** 05-WORKFLOW-REFERENCE.md — Ch23-24 — **Confidence: HIGH**  
**Source:** 04-MATCHING-REFERENCE.md — Ch12, Ch14 — **Confidence: HIGH**

## Dossier Without Match: Automatic Stages

```
1. Normal search
    ↓
2. Expanded search
    ↓
3. Intelligent search
    ↓
4. Continuous search (surveillance)
    ↓
5. Notification of demandeur
    ↓
6. Automatic follow-up
```

## Progressive Expansion Dimensions

The engine can progressively:
- **Widen the neighborhood** — search adjacent areas
- **Widen the distance** — use GPS real distance
- **Search neighboring districts** — similar characteristics
- **Propose compatible variants** — alternatives that match
- **Flexible criteria** — surface, distance, neighborhood, equipment, comfort

## Rules

- **Critical fields are NEVER modified** without demandeur agreement
- Budget: slight increase possible ONLY if other criteria are excellent OR demandeur has already accepted comparable properties
- Location: when requested neighborhood has no compatible properties, propose neighboring districts with similar characteristics
- The proposal must ALWAYS be explained

## Refused Property Reproposition Exceptions

A definitively refused property is NEVER reproposed UNLESS:
- Significant price decrease
- Major modification
- Changed need
- Explicit demandeur request

---

# 22. CONTINUOUS MARKET SURVEILLANCE RULES

**Source:** 05-WORKFLOW-REFERENCE.md — Ch10, Ch27, Ch79 — **Confidence: HIGH**  
**Source:** 04-MATCHING-REFERENCE.md — Ch79 (Surveillance continue) — **Confidence: HIGH**

## What Is Monitored

Even without user interaction, LAWIM continuously monitors:
- New publications
- Price decreases
- Returns to availability
- New neighborhoods
- New compatible listings
- Property statuses
- Dossiers
- Documents
- Prices
- Holder responses
- Market events

## Market Intelligence Indicators (Decision Engine Ch95-96)

| Indicator | Description |
|---|---|
| Average sale time by city | Data-driven market knowledge |
| Average rental time | Data-driven market knowledge |
| Average time before first visit | Engagement metric |
| Most requested neighborhoods | Demand heatmap |
| Most searched property types | Demand trends |
| Seasonality | Temporal patterns |
| **Market Tension Index** | For each City × Neighborhood × Property Type × Operation combination |

### Market Tension Index

- 95% = Very tense market → Properties are rare
- 25% = Relaxed market → Many properties available

The engine adapts recommendations accordingly.

## Surveillance Continuity

Surveillance is continuous as long as the dossier is active. Any significant change triggers a new matching.

## Demandeur Follow-up (if no results found within SLA)

LAWIM re-contacts the demandeur:

> "I am actively pursuing your search. Since our last exchange, no property exactly matches your criteria. Would you like to maintain your search as-is or explore some alternatives?"

## Holder Follow-up (if no response)

```
First reminder
    ↓
Second reminder
    ↓
Last reminder
    ↓
Property marked inactive
    ↓
Rematching
```

---

# 23. HEALTH SCORES DEFINITIONS

**Source:** 05-WORKFLOW-REFERENCE.md — Ch30-31 — **Confidence: HIGH**

## Dossier Health Score

### Criteria
- Recent activity
- Responses
- Number of propositions
- Progression
- Interactions

### Levels
- 🟢 Excellent
- 🟡 Normal
- 🟠 To monitor
- 🔴 Critical

Critical dossiers become priority.

## Property Health Score

### Criteria
- Confirmed availability
- Listing age
- Number of views
- Number of matches
- Number of visits
- Refusals
- Documentary quality

### Automatic Actions for Low Health
- Confirmation of availability
- Listing improvement
- Photo addition
- Price verification
- Archival if necessary

## Data Quality Score (CRM_MODEL Sec 9)

```
Quality Score = (Completeness × 0.6) + (Reliability × 0.4)
```

### Completeness Weight by Field
- Title: 10%
- Description: 15%
- Price: 15%
- Location: 15%
- Type: 15%
- Images: 15% (max 3 pts/image)

### Source Reliability
| Source | Score |
|---|---|
| agent | 90 |
| google_form | 85 |
| import | 70 |
| whatsapp | 50 |
| unknown | 30 |

### Quality Grading
| Grade | Score | Label |
|---|---|---|
| A+ | ≥ 80 | Excellent |
| A | ≥ 60 | Good |
| B | ≥ 40 | Average |
| C | ≥ 20 | Weak |
| D | < 20 | To verify |

## Trust Score (6 levels - 08-ROLE-REFERENCE Ch63)

| Level | Name |
|---|---|
| 🔴 1 | New account |
| 🟠 2 | Phone verified |
| 🟡 3 | Identity verified |
| 🟢 4 | Professional docs validated |
| 🔵 5 | Verified professional/partner |
| ⭐ 6 | Reference account |

---

# 24. SLA TABLES

## SLA by Property Type (Ch22 - Default Values)

| Property Type | First Matching | First Rematching | First Follow-up |
|---|---|---|---|
| Chambre | Immediate | 24 h | 48 h |
| Chambre moderne | Immediate | 24 h | 48 h |
| Studio | Immediate | 48 h | 72 h |
| Appartement | Immediate | 72 h | 5 days |
| Maison | Immediate | 5 days | 7 days |
| Villa | Immediate | 7 days | 10 days |
| Duplex | Immediate | 7 days | 10 days |
| Terrain résidentiel | Immediate | 10 days | 15 days |
| Terrain agricole | Immediate | 15 days | 20 days |
| Terrain industriel | Immediate | 20 days | 30 days |
| Commerce | Immediate | 7 days | 10 days |
| Bureau | Immediate | 10 days | 15 days |
| Entrepôt | Immediate | 15 days | 20 days |
| Hôtel | Immediate | 30 days | 45 days |
| Immeuble | Immediate | 30 days | 45 days |

## Lead Priority SLAs

| Priority | SLA |
|---|---|
| P0 (diaspora_investor, buyer > 50M) | < 30 min |
| P1 (seller, land_buyer) | < 2 h |
| P2 (standard buyer/investor) | < 24 h |
| P3 (tenant, non-qualified) | J+1 to J+7 |

## Recommended Action SLAs by Lead Class

| Class | Delay |
|---|---|
| HOT | < 1 h |
| WARM | < 24 h |
| COLD | < 48 h |
| LOW | J+7 / J+30 / J+90 |
| SPAM | Immediate (ignore) |

## Incident Priority SLAs

| Priority | Handling Delay |
|---|---|
| 🔴 Critique | Immediate |
| 🟠 Élevée (High) | < 24 h |
| 🟡 Normale (Normal) | < 72 h |
| 🟢 Faible (Low) | According to support availability |

## Visit Reminder SLA

- 24 hours before visit
- 2 hours before visit (configurable additional reminders)

## Follow-up Intervals (Commercial)

| Priority | Interval | Channel |
|---|---|---|
| URGENT | Within hours | WhatsApp/Telegram |
| HIGH | Daily | WhatsApp |
| NORMAL | Every 3 days | WhatsApp/Telegram |
| LOW | Weekly | Telegram |

## Follow-up Cadence (Long-term)

- J1 (24h)
- J7 (168h)
- J30 (720h)
- J90 (2160h)

## Dossier Health SLA

> A dossier must never remain without significant event beyond the applicable SLA. If exceeded, system MUST: launch rematching, follow up a party, propose an adjustment, or escalate to LAWIM collaborator.

---

# 25. BUSINESS RULES RELATED TO WORKFLOWS

**All rules with VALIDATED/PARTIAL confidence from RULE_INDEX.md**

## Constitutional Rules

| Rule ID | Description |
|---|---|
| CONST-001 | Zero commission on real estate transactions |
| CONST-002 | LAWIM finances via services and paid contact |
| CONST-004 | WhatsApp as primary channel |
| CONST-005 | Multi-channel strategy |
| CONST-006 | Matching as engine core |
| CONST-007 | Qualification as experience foundation |
| CONST-008 | Agents and clients at center of model |
| CONST-010 | DeepSeek as primary AI engine |

## Property Lifecycle Rules

| Rule ID | Description |
|---|---|
| PROP-001 | 7 property families: Residential, Commercial, Industrial, Land, Agricultural, Hotel, Project |
| PROP-003 | 5 states: available, pending, rented, sold, archived |
| PROP-004 | Transitions: available→pending/archived, pending→rented/sold/available/archived, rented/sold→archived, archived→available |
| PROP-005 | Auto-archival after 90 days of inactivity |
| PROP-006 | Data Quality Score = completeness*0.6 + reliability*0.4 |

## Matching Rules

| Rule ID | Description |
|---|---|
| MATCH-002 | DE Dimensions: Type=25%, Operation=20%, Budget=15%, Location=15%, Critical=15%, Recommended=10% |
| MATCH-003 | Budget tolerances: rent=20%, buy=15%, invest=25% |
| MATCH-009 | Minimum match threshold = 60/100 |
| MATCH-010 | Max results: 10 (V1), max 5 at first matching (DE) |
| MATCH-012 | 4 compatibility levels: Critical, Functional, Comfort, Preferential |
| MATCH-013 | Non-compensation principle (terrain doesn't compensate villa) |
| MATCH-014 | Learning from refusals: 3 refusals → prioritization |
| MATCH-015 | Rematching never starts from zero |
| MATCH-017 | Definitively refused property → never reproposed (except exceptions) |
| MATCH-018 | Exceptions: price drop, major modification, changed need, explicit request |
| MATCH-032 | Diversity: avoid near-identical properties (3 same-building apartments → 1 presented) |
| MATCH-033 | Explainability: top 3 criteria explained for each proposition |
| MATCH-034 | Absolute rules: never incompatible property, never sold property, never twice after refusal |

## Negotiation Rules

| Rule ID | Description |
|---|---|
| NEGO-001 | 4 buyer profiles: national, diaspora, investor, young professional |
| NEGO-002 | 3 seller profiles: individual, promoter, lessor |
| NEGO-005 | 6 LAWIM arguments: zero commission, contact, smart matching, accompaniment, WhatsApp, verified agents |
| NEGO-011 | Follow-up calendar: J1, J7, J30, J90 |

## CRM Rules

| Rule ID | Description |
|---|---|
| CRM-001 | 7 role levels 1-7: demandeur(1), seller(2), agent(3), agency(4), assistant(5), vice_master(6), master(7) |
| CRM-003 | 7 user states: NEW_USER, SEARCHING_PROPERTY, PROPERTY_OWNER, AGENT, LEAD_CREATED, PREMIUM_AGENT, INACTIVE |
| CRM-004 | 11 event types (see System Events below) |
| CRM-005 | Agent Opt-In: 4 steps (detection → request → log → share) |
| CRM-007 | Default lead price: 500 FCFA |
| CRM-014 | CRM scoring V5: 7 weighted factors (total=1.0) |

## Workflow Transition Rules (Ch7)

- A transition must always respect: business rules, user rights, official repositories
- Invalid transition is FORBIDDEN
- Examples of invalid transitions: Transaction → Creation (forbidden), Visit → Matching (forbidden), Matching → Visit (authorized)
- Every transition is recorded: old state, new state, author, date, reason, possible comments
- History is NEVER deleted

## Double Consent Rule

> Contact (Mise en relation) requires double consent: demandeur interested AND holder favorable. No exceptions.

## Quality Scoring Rules (per property type)

**Residential Simple (Chambre/Studio):** Type=20%, Location=25%, Budget=25%, Operation=10%, Shower/Kitchen/Furnished=10%, Availability=5%, Quality=5%  
**Appartement:** Type=15%, Location=20%, Budget=20%, Bedrooms=15%, Kitchen/Shower=8%, Parking/Balcony=5%, Availability=4%, Quality=3%  
**Maison:** Type=15%, Location=18%, Budget=18%, Bedrooms=15%, Yard/Fence=10%, Shower/Kitchen=6%, Parking/Borehole=5%, Quality=3%  
**Villa:** Type=12%, Location=18%, Budget=17%, Bedrooms=15%, Yard/Fence/Barrier=10%, Dependence/Garage=8%, Forage/Security=5%, Pool/Garden=4%, Quality=3%  
**Terrain Résidentiel:** Type=15%, Location=18%, Price=17%, Surface=15%, Legal Situation=12%, Access=7%, Water/Electricity=4%, GPS/Boundary=4%  
**Terrain Agricole:** Type=15%, Location=15%, Price=15%, Surface=20%, Legal=12%, Ag Activity=8%, Access/Water=8%, Quality=7%  
**Bureau/Coworking:** Type=15%, Location=20%, Budget=20%, Surface=12%, Accessibility=10%, Parking=8%, Internet/AC=5%, Floor/Elevator=5%, Quality=5%  
**Hôtel/Auberge:** Type=12%, Location=15%, Price=15%, Bedrooms=18%, Operating State=10%, Occupancy/Revenue=10%, Parking/Restaurant=8%, Docs=5%, Quality=7%

## System Event Types (CRM_MODEL Sec 17 & 05-WORKFLOW Ch199)

| Event | Trigger | System Action |
|---|---|---|
| `message.received` | Incoming WhatsApp/Telegram message | Normalization, pipeline routing |
| `intent.detected` | Intent identified (buy/rent/sell/invest) | Scoring, classification |
| `user.created` | New user registered | Default profile, onboarding |
| `property.created` | New property added | Indexation, matching |
| `lead.created` | Qualified lead generated | Agent routing, notification |
| `match.generated` | Lead × property correspondence | Lead notification |
| `payment.success` | Payment successful | Service activation |
| `subscription.renewed` | Subscription renewed | Access update |
| `boost.applied` | Ad boost activated | Increased visibility |
| `access.granted` | Access permission granted | Feature unlock |
| `user.state_changed` | User state change | State machine update |
| `feedback.submitted` | Feedback received | Rating update |
| `fraud.detected` | Fraud suspected | Blocking, admin alert |

## Anti-Fraud Layers (CRM_MODEL Sec 7)

| Layer | Detection | Action |
|---|---|---|
| broker_spam | Repeated promotional messages, multiple solicitation | 60 min block, broker flag |
| duplicate_listing | Same property published by multiple accounts | Merge, warning |
| fake_price | Abnormally low/high price vs market | Flag, manual verification |
| suspicious_urgency | Artificial pressure for quick payment | Alert, enhanced verification |

---

# 26. STATE MACHINE DIAGRAMS (TEXT-BASED)

## A. Main Cross-Cutting Workflow (Ch203)

```
Projet immobilier (Real Estate Project)
    ↓
Création du dossier (Dossier Creation)
    ↓
Qualification (Qualification)
    ↓
Matching (Matching)
    ↓
Mise en relation (Contact)
    ↓
Visite (Visit)
    ↓
Négociation (Negotiation)
    ↓
Transaction (Transaction)
    ↓
Clôture (Closure)
    ↓
Archivage (Archiving)
```

## B. Property Lifecycle

```
Création ──→ Qualification ──→ Validation ──→ Publié ──→ Disponible
                                                              │
                                                              ├──→ Matching ──→ Visites ──→ Négociation ──→ Réservé ──→ Transaction ──→ Indisponible
                                                              │                                                                                │
                                                              └──→ Réactivation ←──────────────────────────────────────────────────────────────┘
                                                                                                │
                                                                                                └──→ Archivé
```

## C. Dossier Lifecycle

```
Création ──→ Qualification ──→ Matching ──→ Présentation ──→ Attente décision demandeur
                                                                    │
                                                                    ├──→ Contact détenteur ──→ Attente décision détenteur
                                                                    │                              │
                                                                    │                              ├──→ Mise en relation ──→ Visite ──→ Négociation ──→ Accord ──→ Transaction ──→ Clôture ──→ Archivage
                                                                    │                              │
                                                                    │                              └──→ Rematching
                                                                    │
                                                                    └──→ Refus ──→ Rematching
```

## D. Negotiation Finite State Machine

```
Ouverte → En discussion → Offre → Contre-offre → Accord de principe → Accord final → Transaction
                                                     │
                                                     └──→ Échec → Rematching
```

## E. Transaction States

```
Accord → Préparation → Documents → Paiement → Signature → Remise des clés → Confirmation → Transaction terminée → Archivage
                                                                                                        │
                                                                                                        └──→ Échec → [Négociation | Rematching]
```

## F. Paid Service Lifecycle

```
Création → Proposition → Acceptation → Paiement → Activation → Utilisation → Expiration → Archivage
                                                │
                                                └──→ [Failed | Cancelled | Refunded]
```

## G. Payment States

```
PAYMENT_CREATED → PAYMENT_INITIATED → PAYMENT_PENDING → PAYMENT_CONFIRMED → [Service Activation]
                                       │                      │
                                       ├──→ PAYMENT_FAILED    └──→ PAYMENT_RECONCILED
                                       ├──→ PAYMENT_CANCELLED
                                       ├──→ PAYMENT_EXPIRED
                                       └──→ PAYMENT_DISPUTED → PAYMENT_REFUNDED
```

## H. Incident Lifecycle

```
Signalement → Qualification → Analyse → Collecte informations → Décision → Résolution → Clôture → Archivage
```

## I. Mediation Workflow

```
Incident → Proposition médiation → Acceptation → Nomination Médiateur → Échanges → Proposition solution → Acceptation → Clôture
                                                                                                                │
                                                                                                                └──→ [Refus → Workflow normal]
```

## J. User Identity State Machine

```
                    ┌──────────────────────────────────────────────────┐
                    │                                                  │
                    ↓                                                  │
NEW_USER ──→ SEARCHING_PROPERTY ──→ LEAD_CREATED ──→ [back to SEARCHING]
    │              │                       │
    │              ↓                       │
    │          INACTIVE ←──────────────────┘
    │              │
    └──────────────┘ (reactivation)

NEW_USER ──→ PROPERTY_OWNER ──→ LEAD_CREATED
                                    │
                                    ↓
                                INACTIVE

NEW_USER ──→ AGENT ──→ PREMIUM_AGENT ──→ AGENT (subscription expires)
                │
                ↓
            INACTIVE
```

## K. Organization (Agency) Creation Workflow

```
Demande → Saisie infos → Téléversement justificatifs → Contrôle auto → Contrôle LAWIM → Validation → Organisation active
```

## L. Agent Invitation Workflow

```
Invitation → Lien sécurisé → Création compte → Téléphone vérifié → CNI → Validation LAWIM → Agent actif
```

## M. CRM Pipeline (8 stages)

```
Message brut → normalize_text → extract_entities → detect_intent → context_enrichment → lead_scoring → lead_classification → crm_routing
```

## N. Holder Silence Workflow

```
Premier rappel → Deuxième rappel → Dernier rappel → Bien marqué "à confirmer" → Rematching
```

## O. Progressive Search Expansion

```
Recherche normale → Recherche élargie → Recherche intelligente → Recherche continue → Notification → Relance auto
```

## P. SIE-Enriched Publication Workflow

```
Création publication → Validation → Génération Reference Code → Association campagne → Association acteur → Association biens → Association services → Publication → Journalisation → Stats → Dashboard
```

---

# 27. SOURCE REFERENCES

| Finding | Source File | Confidence |
|---|---|---|
| **Workflow Architecture & Principles** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 1 (Ch1-13) | **HIGH** |
| **Active Workflows, SLA & Proactive Management** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 2 (Ch20-33) | **HIGH** |
| **Property Lifecycle** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 3 (Ch34-51) | **HIGH** |
| **Dossier Lifecycle** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 4 (Ch52-73) | **HIGH** |
| **Mise en Relation Lifecycle** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 5 (Ch74-89) | **HIGH** |
| **Visit Lifecycle** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 6 (Ch90-108) | **HIGH** |
| **Negotiation Lifecycle** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 7 (Ch109-127) | **HIGH** |
| **Transaction Lifecycle** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 8 (Ch128-145) | **HIGH** |
| **Paid Services & Payment Lifecycle** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 9 (Ch147-163) | **HIGH** |
| **Disputes, Claims & Incidents Lifecycle** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 10 (Ch164-181) | **HIGH** |
| **Closure, Archiving & Retention** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 11 (Ch182-194) | **HIGH** |
| **Mediation Workflow** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Ch195 | **HIGH** |
| **Cross-cutting Workflows & Consistency** | `docs/Directive/05-WORKFLOW-REFERENCE.md` — Part 12 (Ch196-214) | **HIGH** |
| **Matching Engine Fundamentals** | `docs/Directive/04-MATCHING-REFERENCE.md` (357 lines) | **HIGH** |
| **Matching Algorithm, Scoring, Weights by Type** | `docs/Directive/04-DECISION-ENGINE-REFERENCE.md` — Part 1-4 | **HIGH** |
| **Rematching & Continuous Learning** | `docs/Directive/04-DECISION-ENGINE-REFERENCE.md` — Part 5 | **HIGH** |
| **Decision Engine** | `docs/Directive/04-DECISION-ENGINE-REFERENCE.md` — Part 6 (Ch83-100) | **HIGH** |
| **Matching Weights by Property Type** | `docs/Directive/04-DECISION-ENGINE-REFERENCE.md` — Part 4 (Ch40-62) | **HIGH** |
| **User Identity Lifecycle** | `docs/Directive/08-ROLE-REFERENCE.md` — Part 2 (Ch16-30) | **HIGH** |
| **Role Reference & Families** | `docs/Directive/08-ROLE-REFERENCE.md` — Part 3 (Ch31-46) | **HIGH** |
| **Permissions & Access Control** | `docs/Directive/08-ROLE-REFERENCE.md` — Part 4 (Ch47-60) | **HIGH** |
| **Trust Framework, Verifications & Badges** | `docs/Directive/08-ROLE-REFERENCE.md` — Part 5 (Ch61-74) | **HIGH** |
| **Organizations, Agencies & Structures** | `docs/Directive/08-ROLE-REFERENCE.md` — Part 6 (Ch75-89) | **HIGH** |
| **Role Governance & Delegation** | `docs/Directive/08-ROLE-REFERENCE.md` — Part 7 (Ch90-104) | **HIGH** |
| **Role Engine, Audit & Absolute Rules** | `docs/Directive/08-ROLE-REFERENCE.md` — Part 8 (Ch105-129) | **HIGH** |
| **Sales Playbook (commercial positioning, scripts, objections)** | `docs/Directive/48-LAWIM-SALES-PLAYBOOK.md` | **HIGH** |
| **Sales Process: 8 steps** | `docs/Directive/48-LAWIM-SALES-PLAYBOOK.md` — Sec 15 | **HIGH** |
| **Commercial KPI definitions** | `docs/Directive/48-LAWIM-SALES-PLAYBOOK.md` — Sec 18 | **HIGH** |
| **CRM Pipeline (8 stages)** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 1 | **HIGH** |
| **Lead Types, Base Scores, Boosters, Penalties** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 2-4 | **HIGH** |
| **Classification Thresholds (V1 & V5)** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 4 | **HIGH** |
| **Lead Priority (P0-P3) with SLAs** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 5 | **HIGH** |
| **Behavior Tracking (8 behaviors)** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 6 | **HIGH** |
| **Anti-Fraud Layers & Signal Weights** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 7 | **HIGH** |
| **Identity Resolution Rules** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 8 | **HIGH** |
| **Data Quality Engine** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 9 | **HIGH** |
| **Anti-Spam System** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 10 | **HIGH** |
| **Agent Opt-In System (4 steps)** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 11 | **HIGH** |
| **Agent Rating System** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 12 | **HIGH** |
| **Monetized Services (13 items with prices)** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 14 | **HIGH** |
| **Feature Flags (core ON, advanced OFF)** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 15 | **HIGH** |
| **System Event Types (13 events)** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 17 | **HIGH** |
| **User States (7 states with transitions)** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 18 | **HIGH** |
| **CRM Database Tables (20+ tables)** | `docs/lawim_heritage_gold/CRM_MODEL.md` — Sec 19 | **HIGH** |
| **Rule Index (99+ business rules)** | `docs/lawim_heritage_gold/RULE_INDEX.md` | **HIGH** |
| **Closing Techniques & Conversion Path** | `knowledge_unified/commercial/closing_techniques.md` | **HIGH** |
| **Conversation Tone Guide** | `knowledge_unified/commercial/conversation_tone.md` | **HIGH** |
| **Follow-up Strategies (intervals, rules)** | `knowledge_unified/commercial/follow_up_strategies.md` | **HIGH** |
| **Negotiation Techniques (Cameroon market)** | `knowledge_unified/commercial/negotiation_techniques.md` | **HIGH** |
| **Objection Handling (buyer/seller fears)** | `knowledge_unified/commercial/objection_handling.md` | **HIGH** |
| **Source Inventory (~220 files cataloged)** | `knowledge_unified/sources/SOURCE_INVENTORY.md` | **HIGH** |
| **Traceability Matrix (73 entries)** | `knowledge_unified/sources/TRACEABILITY_MATRIX.md` | **HIGH** |

---

## Extraction Summary

| Category | Count |
|---|---|
| **Workflows discovered** | 21 |
| **Total states across all workflows** | ~95+ |
| **SLA definitions** | 6 categories (15 property types, lead priorities, lead classes, incidents, visits, follow-ups) |
| **NBA rules** | 12 official actions + priority matrix |
| **Business rules extracted** | 99+ (from RULE_INDEX.md) |
| **Health scores defined** | 5 (Dossier Health, Property Health, Data Quality, Trust Score, Holder Reliability) |
| **Feature flags** | 11 (4 ON, 7 OFF for future phases) |
| **Monetized services** | 13 |
| **System events** | 13 |
| **User states** | 7 |
| **Role levels** | 7 (1-7 hierarchy) |
| **Trust levels** | 6 |
| **Source files explored** | 10 primary + directories |
| **Payment states** | 10 |
| **Visit statuses** | 9 |
| **Property availability statuses** | 8 |

---

*Extraction completed 2026-07-15 for LAWIM Heritage Completion Mission H0.4 — All business workflow knowledge from heritage sources has been extracted, organized, and cross-referenced with source confidence levels.*
