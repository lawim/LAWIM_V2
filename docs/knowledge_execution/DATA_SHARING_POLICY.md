# DATA SHARING POLICY

**Domain:** Data Protection & Sharing — Relationship Engine
**Version:** 1.0
**Status:** CANONICAL
**Source:** Heritage Gold — CRM_MODEL.md, WORKFLOW_EXTRACTION_COMPLETE.md, ROLE_MODEL.md
**Prerequisite:** CONSENT_EXECUTION_CONTRACT.md, RELATIONSHIP_EXECUTION_ARCHITECTURE.md

---

## 0. H0.5 Integration — Privacy & Sensitive Field Alignment

### 0.1 H0.5 Privacy Level Mapping

The H0.5 qualification matrices classify all fields into four privacy levels (from `PRIVACY_AND_SENSITIVE_FIELDS.md`). This policy aligns its data sharing rules with those classifications:

| H0.5 Privacy Level | Code | This Policy's Visibility | Examples |
|--------------------|------|--------------------------|----------|
| **Public** | 0 | Shared freely with any party | city, property_type, neighborhood, chambres, cuisine |
| **Private** | 1 | Shared only after consent with matched counterparty | nom, telephone, budget_max, email |
| **Sensitive** | 2 | Explicit consent required before collection or sharing | revenus, financing, apport, garanties |
| **Confidential** | 3 | Never shared without legal basis; strict need-to-know | num_titre, litiges_connus, hypotheque |

Source: `docs/lawim_heritage_gold/qualification_matrices/PRIVACY_AND_SENSITIVE_FIELDS.md`

### 0.2 H0.5 Sensitive/Confidential Fields Alignment

The lifecycle stages in this policy (§2) are aligned with H0.5 privacy levels:

| Lifecycle Stage | H0.5 Privacy Level Limit | Enforcement |
|-----------------|-------------------------|-------------|
| Pre-Proposition | PUBLIC only | SENSITIVE and CONFIDENTIAL fields never shared pre-consent |
| Demandeur Consent (pending) | PUBLIC + PRIVATE (with consent) | PRIVATE fields shared per-field consent |
| Double Consent (active) | PUBLIC + PRIVATE + SENSITIVE (with explicit consent) | SENSITIVE fields require explicit opt-in per sharing event |
| Transaction/Notary | CONFIDENTIAL (with NDA/legal basis) | CONFIDENTIAL fields only shared with legal professionals under NDA |

### 0.3 H0.5 Field-Level Privacy → Data Sharing Rules

Each data field in §2 (Data Visibility by Lifecycle Stage) maps to an H0.5 privacy classification:

| Data Field | H0.5 Privacy Level | Sharing Rule |
|------------|-------------------|--------------|
| Property address (exact) | PRIVATE | Shared post-consent per §2.2 |
| Property address (approximate) | PUBLIC | Always shared per §2.1 |
| Holder identity | PUBLIC (role) / PRIVATE (name) | Masked pre-consent, revealed post-consent |
| Holder phone | PRIVATE | Conditional per §2.3 |
| Demandeur identity | PRIVATE | Masked pre-consent, revealed post-consent |
| Demandeur phone | PRIVATE | Conditional per §2.3 |
| Budget info | PRIVATE | Post-consent (§2.3) |

### 0.4 H0.5 Per-Matrix Sensitive Fields

Each matrix in `qualification_matrices.json` defines its own `sensitive_fields` array. For example:

| Matrix | Sensitive Fields |
|--------|-----------------|
| MATRIX-RES-SEARCH-001 (Chambre Simple) | telephone, nom, budget_max, email |
| MATRIX-RES-SEARCH-006 (Appartement Non Meublé) | telephone, nom, budget_max, financing |
| LAND_SEARCH_TERRAIN_TITRE_001 (Titled Land) | num_titre, litiges_connus, hypotheque_charge |

The Data Sharing Policy's `max_visibility` per lifecycle stage must respect the most restrictive field in the active matrix.

### 0.5 Alignment Verification

| This Policy Section | H0.5 Alignment | Notes |
|--------------------|----------------|-------|
| §1 Policy Principles | ✅ Aligned | Data Minimization, Progressive Disclosure, Consent-Based all match H0.5 PRIVACY_AND_SENSITIVE_FIELDS §3 |
| §2 Data Visibility by Lifecycle | ✅ Aligned | Pre-proposition = PUBLIC only, matches H0.5 §3 Rule 1 |
| §3 Masked Data Rules | ✅ Aligned | Masking for PRIVATE/contact fields per H0.5 §3 Rule 2 |
| §4 Authorized Data Sharing | ✅ Aligned | Sharing triggers match H0.5 §6 consent management |
| §5 Data Retention | ✅ Aligned | Retention periods per H0.5 §5 (90d qual, 5yr transaction) |
| §6 Anonymization | ✅ Aligned | Methods match H0.5 §9.3 anonymization for matching engine |
| §9 Role-Based Access | ✅ Aligned | Access matrix matches H0.5 §5.3 access control matrix |

---

## 1. H1 Heritage Layer — Policy Principles

| Principle | Description |
|---|---|
| **Data Minimization** | Only the minimum necessary data is shared at each lifecycle stage |
| **Progressive Disclosure** | Data visibility increases as consent is obtained |
| **Purpose Limitation** | Shared data is used only for the intended relationship purpose |
| **Consent-Based** | No data sharing without explicit consent |
| **Auditable** | Every data access and sharing event is logged |
| **Time-Bound** | Data sharing is limited to the relationship duration |
| **Revocable** | Data sharing can be withdrawn at any time |

---

## 2. Data Visibility by Lifecycle Stage

### 2.1 Before Demandeur Consent (Pre-Proposition)

| Data Field | Demandeur Sees | Holder Sees | LAWIM Sees |
|---|---|---|---|
| Property photos | All public | All public | All |
| Property address | Approximate (neighborhood) | Full | Full |
| Property price | Full | Full | Full |
| Property description | Full | Full | Full |
| Holder identity | "Propriétaire" / "Agence" | Full | Full |
| Holder phone | Hidden | Full | Full |
| Demandeur identity | Full | Hidden | Full |
| Demandeur phone | Full | Hidden | Full |

### 2.2 After Demandeur Consent (Holder Contact Stage)

| Data Field | Demandeur Sees | Holder Sees | LAWIM Sees |
|---|---|---|---|
| Property address | Full | Full | Full |
| Holder identity | "Propriétaire" / "Agence" | Full | Full |
| Holder phone | Hidden | Full | Full |
| Demandeur identity | Full | Masked ("Personne intéressée") | Full |
| Demandeur phone | Full | Hidden | Full |

### 2.3 After Double Consent (Relationship Active)

| Data Field | Demandeur Sees | Holder Sees | LAWIM Sees |
|---|---|---|---|
| Property address | Full | Full | Full |
| Holder identity | Full (name) | Full | Full |
| Holder phone | Conditional* | Full | Full |
| Holder email | Conditional* | Full | Full |
| Demandeur identity | Full | Full (name) | Full |
| Demandeur phone | Full | Conditional* | Full |
| Demandeur email | Full | Conditional* | Full |

*Conditional: Shared only if both parties have granted data sharing consent OR a paid service (`deblocage_coordonnees`, 500 FCFA) has unlocked the coordinates.

### 2.4 Agent Opt-In Active

| Data Field | Demandeur Sees | Agent Sees | LAWIM Sees |
|---|---|---|---|
| Demandeur identity | Full | Full | Full |
| Demandeur phone | Full | Conditional (opt-in) | Full |
| Demandeur dossier | Full | Full | Full |
| Agent identity | Full (name + agency) | Full | Full |
| Agent phone | Conditional* | Full | Full |

*Conditional: Agent phone shared to demandeur only if agent has accepted data sharing or paid service.

---

## 3. Masked Data Rules

### 3.1 Identity Masking

Pre-consent masking follows these rules:

| Role | Masked Name Display | Rationale |
|---|---|---|
| Holder (owner) | "Propriétaire" | Generic role, no identity leak |
| Holder (agency) | "🏢 Agence immobilière" | Generic agency label |
| Holder (introducer) | "🤝 Introduceur" | Generic introducer label |
| Demandeur | "Personne intéressée" / "👤 Demandeur" | Generic seeker label |
| Agent | "🏢 Agent partenaire" | Generic agent label (pre-opt-in) |

### 3.2 Coordinate Masking

| Coordinate Type | Pre-Consent Display | Post-Consent Display | Unlocked Display |
|---|---|---|---|
| Phone | `+237 XXXXXXXX` (last 4 digits) | `+237 6XX XXX XX` (masked middle) | Full |
| Email | `u***@domain.com` | `user@domain.com` | Full |
| Address | "Douala, Bonapriso" (city + hood) | Full address | Full |

### 3.3 Masking Implementation Rules

| Rule | Behavior |
|---|---|
| Masking is server-enforced | Data is NEVER sent unmasked to unauthorized parties |
| Masking is role-based | Same data may have different visibility per role |
| Masking is state-dependent | Same role sees different data at different lifecycle stages |
| Masking is irreversible post-consent | Once consent is granted, data is revealed permanently (unless revoked) |

> **ARCHITECTURE_DECISION:** Phone masking pattern (last 4 digits visible pre-consent) is an architecture-defined default. Full coordinate unlocking via paid service (500 FCFA) references GOLD-DM-072.

---

## 4. Authorized Data Sharing

### 4.1 Sharing Trigger Events

| Event | Data Shared | Between | Consent Required |
|---|---|---|---|
| Double consent granted | Identity + basic profile | Demandeur ↔ Holder | Both |
| Data sharing consent | Phone + email | Demandeur ↔ Holder | Both |
| Paid coordinate unlock (`deblocage_coordonnees`) | Phone | Holder → Demandeur | Holder (paid service) |
| Agent opt-in accepted | Demandeur profile + dossier | Demandeur → Agent | Demandeur |
| Agent opt-in accepted | Agent profile | Agent → Demandeur | Agent |
| Visit scheduling | Phone (temporary) | Demandeur ↔ Holder | Both (implicit) |
| Negotiation | Contact details | Demandeur ↔ Holder | Both |

### 4.2 Sharing Scope Per Role

#### Demandeur

| Data Field | Shared With Holder | Shared With Agent | Shared With LAWIM |
|---|---|---|---|
| Full name | Post-consent | Post-opt-in | Always |
| Phone | Conditional | Conditional | Always |
| Email | Conditional | Conditional | Always |
| WhatsApp ID | Post-consent | Post-opt-in | Always |
| Search criteria | N/A | Post-opt-in | Always |
| Visit history | Post-consent | Post-opt-in | Always |
| Budget info | Post-consent | Post-opt-in | Always |

#### Holder

| Data Field | Shared With Demandeur | Shared With Agent | Shared With LAWIM |
|---|---|---|---|
| Full name | Post-consent | Per agency | Always |
| Phone | Conditional | Per agency | Always |
| Property address | Post-consent | Per agency | Always |
| Property details | Always | Per agency | Always |
| Holder reliability score | Never | Never | Always |

#### Agent

| Data Field | Shared With Demandeur | Shared With LAWIM |
|---|---|---|
| Full name | Post-opt-in | Always |
| Agency name | Post-opt-in | Always |
| Phone | Conditional | Always |
| Rating | Post-opt-in | Always |
| Zone expertise | Always | Always |

### 4.3 Sharing Scope Per Relationship Type

| Relationship Type | Standard Shared Fields | Additional (Paid/Consent) |
|---|---|---|
| `buy` (sale) | Identity, property details | Phone, email, documents |
| `rent` (rental) | Identity, property details | Phone, email, lease terms |
| `invest` (investment) | Identity, property details | Phone, email, financial data |

---

## 5. Data Retention Rules

### 5.1 Retention Periods

| Data Category | Active Retention | Archived Retention | Legal Minimum |
|---|---|---|---|
| Relationship records | Duration of relationship + 90 days | 3 years | 5 years (tax) |
| Consent records | Duration + 1 year | Permanent | Permanent (audit) |
| Conversation history | Duration + 90 days | 3 years | 5 years |
| Identity data | Until account closure | 0 (anonymized) | Per RGPD |
| Financial records | 5 years | 10 years | 10 years (legal) |
| Activity logs | 90 days | 3 years | 1 year |
| Anonymized data | Permanent | Permanent | Permanent |

### 5.2 Retention Enforcement

| Action | Schedule | Scope |
|---|---|---|
| Periodic archival | Monthly | Relationships inactive > 90 days |
| Long-term archival | Quarterly | Relationships inactive > 3 years |
| Anonymization | On request | GDPR deletion requests |
| Purging | Never | LAWIM does not delete business data |

> LAWIM principle: "No business data is ever deleted." — Heritage Gold WORKFLOW_EXTRACTION_COMPLETE.md §11
> Exception: GDPR deletion requests, where personal data is anonymized (not deleted from audit trail).

### 5.3 Archival State Behavior

| Capability | Archived | Long-Term Archived |
|---|---|---|
| Readable | Yes | Yes |
| Modifiable | No | No |
| In active workflows | No | No |
| In matching | No | No |
| In statistics | Yes | Yes |
| In audit | Yes | Yes |
| Reactivatable | Yes (admin) | Yes (admin procedure) |

---

## 6. Anonymization Rules

### 6.1 Anonymization Methods

| Method | Description | Use Case |
|---|---|---|
| **Pseudonymization** | Replace identity with persistent hash | Statistical analysis |
| **Aggregation** | Group data into statistical buckets | Reporting, dashboards |
| **Masking** | Hide portions of data (e.g., phone) | Pre-consent display |
| **Irreversible Anonymization** | Replace PII with non-reversible hash | GDPR deletion |
| **Differential Privacy** | Add noise to aggregate queries | Market intelligence |

### 6.2 GDPR Anonymization Process

| Step | Action | Data After |
|---|---|---|
| 1 | Replace name with `ANONYMIZED_[hash]` | No name |
| 2 | Replace phone with `+237 XXXXXXXX` | No phone |
| 3 | Replace email with `anon-[hash]@anonymized.lawim` | No email |
| 4 | Replace WhatsApp ID with hash | No WA ID |
| 5 | Remove profile photo | No photo |
| 6 | Disassociate from contact channels | No contact |
| 7 | Mark `persons.anonymized = TRUE` | Flag set |

### 6.3 What Is NOT Anonymized

| Data | Reason |
|---|---|
| Property records | Belong to property, not person |
| Transaction amounts | Financial audit requirement |
| Relationship timeline (without identities) | System integrity |
| Consent event metadata (without identities) | Audit requirement |
| Aggregated statistics | Business intelligence |

---

## 7. Data Access Logging Requirements

### 7.1 Logged Events

| Event | Data Logged | Retention |
|---|---|---|
| `data.shared` | What data, between whom, when, consent ref | 5 years |
| `data.accessed` | Who accessed what, when, purpose | 3 years |
| `data.masked` | What was masked, for whom, lifecycle stage | 3 years |
| `data.unmasked` | What was revealed, consent ref | 5 years |
| `data.anonymized` | What was anonymized, request ref | Permanent |
| `data.exported` | What was exported, by whom, purpose | 3 years |

### 7.2 Access Control

| Role | Read Consent Records | Read Relationship Data | Read Anonymized Data |
|---|---|---|---|
| Demandeur | Own only | Own only | N/A |
| Holder | Own only | Own only | N/A |
| Agent | Opt-in records only | Routed leads only | N/A |
| LAWIM Admin | All | All | All |
| LAWIM Auditor | All | All | All |
| System (automated) | As authorized | As authorized | As authorized |

### 7.3 Access Log Structure

```json
{
  "log_id": "UUID",
  "event_type": "data.shared",
  "timestamp": "2026-07-15T10:30:00Z",
  "actor_id": "UUID",
  "actor_role": "demandeur|holder|agent|system|admin",
  "data_category": "phone|email|identity|address",
  "data_fields": ["phone", "email"],
  "target_party_id": "UUID",
  "consent_id": "UUID",
  "purpose": "relationship_facilitation",
  "lifecycle_stage": "active",
  "ip_address": "optional",
  "user_agent": "optional"
}
```

---

## 8. Legal Compliance (RGPD)

### 8.1 RGPD Rights Mapping

| RGPD Right | LAWIM Implementation | SLA |
|---|---|---|
| **Right to be informed** | Privacy notice at registration + consent request context | Immediate |
| **Right of access** | User can request their data via support | 30 days |
| **Right to rectification** | User can update profile data anytime | Immediate |
| **Right to erasure** | "SUPPRIMER MES DONNÉES" request with 7-day delay | 7 days |
| **Right to restrict processing** | Consent revocation pauses all processing | 24h |
| **Right to data portability** | User can export their data in JSON format | 30 days |
| **Right to object** | Opt-out of agent contact, marketing | Immediate |

### 8.2 Legal Basis for Processing

| Processing Activity | Legal Basis (RGPD Art.) |
|---|---|
| Relationship facilitation | Art. 6(1)(b) — Contract performance |
| Consent management | Art. 6(1)(a) — Consent |
| Agent routing | Art. 6(1)(a) — Consent |
| Data anonymization | Art. 6(1)(c) — Legal obligation |
| Audit trail retention | Art. 6(1)(c) — Legal obligation |
| Statistical analysis | Art. 6(1)(f) — Legitimate interest |
| Fraud detection | Art. 6(1)(f) — Legitimate interest |

### 8.3 Data Processing Register

| Processor | Purpose | Data Categories | Retention |
|---|---|---|---|
| LAWIM (internal) | Relationship management | Identity, contact, property | Per §5 |
| WhatsApp/Telegram | Communication channel | Messages, metadata | Per platform policy |
| Campay (future) | Payment processing | Financial, phone | Per payment regulation |
| Hosting provider | Infrastructure | All data | Per contract |

---

## 9. Role-Based Data Access Matrix

Per Heritage Gold ROLE_MODEL.md — Permission Matrix (Ch54):

| Data Domain | Demandeur | Holder | Agent | Agency Admin | LAWIM Admin |
|---|---|---|---|---|---|
| Property details | Read | Read/Write own | Read/Write mandate | Read/Write | Full |
| Demandeur profile | Read/Write own | Read (post-consent) | Read (post-opt-in) | Read (routed) | Full |
| Holder profile | Read (post-consent) | Read/Write own | Read (mandate) | Read (agency) | Full |
| Relationship state | Read own | Read own | Read (routed) | Read (agency) | Full |
| Consent records | Read own | Read own | Read (opt-in) | Read (agency) | Full |
| Conversation history | Read own | Read own | Read (routed) | Read (agency) | Full |
| Agent rating | Read | Read | Read/Write own | Read | Full |
| Anonymized data | No | No | No | No | Read (audit) |

---

## 10. Error States & Fallbacks

| Error | Fallback | Alert |
|---|---|---|
| Masking rule not found | Default to maximum restriction (hide all) | System log entry |
| Data sharing consent expired | Re-mask coordinates, notify parties | Notification to affected parties |
| Unauthorized access attempt | Block, log, flag for security review | Security alert |
| Data export exceeds size limit | Chunk export, notify user | None |
| GDPR deletion conflicts with legal hold | Retain until legal hold expires, notify user | Legal team notified |
| Data sharing during revoked consent | Block, revert data to masked state | Audit event logged |

---

## 11. References

| Reference | File |
|---|---|
| Heritage Gold — CRM Database Tables | `docs/lawim_heritage_gold/CRM_MODEL.md` §19 |
| Heritage Gold — Role Permission Matrix | `docs/lawim_heritage_gold/ROLE_MODEL.md` §2 |
| Heritage Gold — Anonymization Requests | `docs/lawim_heritage_gold/CRM_MODEL.md` §19.3 |
| Heritage Gold — GDPR Tables | `docs/lawim_heritage_gold/CRM_MODEL.md` §19.3 (anonymization_requests) |
| Heritage Gold — Trust Levels | `docs/lawim_heritage_gold/ROLE_MODEL.md` §3 |
| Consent Execution Contract | `docs/knowledge_execution/CONSENT_EXECUTION_CONTRACT.md` |
| Relationship Execution Architecture | `docs/knowledge_execution/RELATIONSHIP_EXECUTION_ARCHITECTURE.md` |
| Relationship Lifecycle | `docs/knowledge_execution/RELATIONSHIP_LIFECYCLE.md` |
