# IDENTITY & ROLE EXTENSION MODEL

**Document ID:** LAWIM-H13-IDENTITY-ROLE-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §2 (User/Role/Profile), §11 (CRM Pipeline), §12 (Identity Model), §13 (Organization Model), §14 (Permission/Security Model)
**Source Crosswalks:** ROLE_CROSSWALK.md, required_extensions.json (trust_levels, badges, agency_structure)

---

## Table of Contents

1. [Role Type Distinctions](#1-role-type-distinctions)
2. [Trust Level Model](#2-trust-level-model)
3. [Badge System](#3-badge-system)
4. [Agency Hierarchy Roles](#4-agency-hierarchy-roles)
5. [Identity Resolution Service](#5-identity-resolution-service)
6. [GDPR Deletion Workflow](#6-gdpr-deletion-workflow)
7. [61 Role Concepts Mapped to User Model Extensions](#7-61-role-concepts-mapped-to-user-model-extensions)
8. [Role Classification Rules](#8-role-classification-rules)
9. [Multi-Role Persona Model](#9-multi-role-persona-model)
10. [Complete Extension Mapping Table](#10-complete-extension-mapping-table)

---

## 1. Role Type Distinctions

The unified model recognizes 9 distinct role categories. Each governs a different semantic domain and has unique storage, lifecycle, and enforcement rules.

| # | Role Category | Definition | Persistence | Scoped To | Example Values |
|---|--------------|------------|-------------|-----------|----------------|
| 1 | **system_role** | Platform-wide permission level; gates access to system resources and administrative functions. Maps to V2's 5 official roles. | Permanent on User record | Global (platform) | `admin`, `manager`, `operator`, `partner`, `user` |
| 2 | **business_role** | Functional role within a real estate transaction or business process. Derived from intent detection or explicit selection. | Contextual per Project/Transaction | Transaction/Project | `buyer`, `seller`, `tenant`, `landlord`, `investor`, `demandeur`, `holder` |
| 3 | **user_typology** | Classification of the user's relationship to the platform (who they are as a platform participant). | Permanent on User record | Global (platform) | `particular` (individual), `professional` (agent/agency), `institution` (bank, notary), `diaspora` |
| 4 | **professional_category** | The specific profession or trade the user practices. Used for professional service discovery and qualification. | Semi-permanent on User record | Global (platform) | `agent_immobilier`, `notaire`, `geometre`, `evaluateur`, `architecte`, `courtier`, `macon`, `menuisier` |
| 5 | **transaction_participant_role** | The specific legal/financial role a user plays in a given transaction. May involve legal liability, signature authority, or payment obligations. | Contextual per Transaction | Transaction | `buyer`, `seller`, `lessor`, `lessee`, `guarantor`, `co-signer`, `beneficiary` |
| 6 | **organization_role** | (aka agency_role) Role within an agency/organization. Governs intra-org permissions, lead access, and reporting lines. | Stored on OrganizationMember | Organization | `responsible`, `admin`, `agent`, `assistant` |
| 7 | **CRM_status** | User's current standing in the CRM pipeline. Used for lead management, agent assignment, and SLA enforcement. | Contextual per Lead | Lead/CRM | `hot`, `warm`, `cold`, `low`, `spam`, `lead`, `contact`, `opportunity`, `client` |
| 8 | **permission_scope** | The data scope a user can operate on with a given permission level. Determines visibility of records. | Derived from system_role + agency_role | Per-resource | `own`, `managed`, `org`, `all` |
| 9 | **onboarding_status** | The user's progress through the platform onboarding/activation workflow. Precedes full system_role assignment. | Transitional on User record | Platform lifecycle | `invited`, `account_created`, `phone_verified`, `cni_uploaded`, `validated`, `active` |

### 1.1 Role Interaction Rules

- **system_role** is the gatekeeper: a user must have at least `user` system_role to hold any other role.
- **organization_role** is independent of **system_role**: an `admin` system_role user may be an `agent` in an organization, or no organization member at all.
- **professional_category** is orthogonal to **system_role**: a `user` system_role may have `notaire` professional_category.
- **CRM_status** is always scoped to a specific Lead and does not affect the User's permanent record.
- **business_role** and **transaction_participant_role** may overlap: a user can be `buyer` (business_role) and `buyer` (transaction_participant_role) simultaneously, but these are stored on different entities (Project vs Transaction).

### 1.2 Storage Ownership

| Role Category | Primary Entity | Field |
|--------------|----------------|-------|
| system_role | User | `role` (enum) |
| business_role | Project | `project_type` implies role |
| user_typology | User | `user_type` (new enum) |
| professional_category | User | `business_profiles[]` |
| transaction_participant_role | Transaction | `demandeur_id`, `holder_id`, `agent_id`, `notaire_id` |
| organization_role | OrganizationMember | `agency_role` (enum) |
| CRM_status | Lead | `classification` (enum) |
| permission_scope | (derived) | Computed from system_role + organization_role |
| onboarding_status | User | `onboarding_status` (enum) |

---

## 2. Trust Level Model

Six graduated trust levels. Each level unlocks specific platform capabilities and contributes to the user's trust score. Trust levels are cumulative — a user at Level 4 has satisfied all verification requirements of Levels 1-3.

### 2.1 Trust Level Definitions

| Level | Name | Code | Verification Required | Unlocks | Auto/Manual | Human Decision |
|-------|------|------|----------------------|---------|-------------|----------------|
| 1 | Nouveau compte (New Account) | `new_account` | Email confirmation | Basic browsing, profile creation | Auto on signup | — |
| 2 | Téléphone vérifié (Phone Verified) | `phone_verified` | OTP phone verification | Enhanced platform access, property contact, lead submission | Auto on OTP | — |
| 3 | Identité vérifiée (Identity Verified) | `identity_verified` | CNI/passport document upload + admin validation | Trust badge, higher match confidence, full listing creation | Manual (admin validation) | Y — admin validation threshold |
| 4 | Documents pro validés (Professional Docs Validated) | `pro_docs_validated` | Professional credentials (RCCM, diploma, license) validation | Professional qualification unlocked, pro trust badge | Manual (admin validation) | Y — acceptance criteria |
| 5 | Professionnel vérifié (Verified Professional) | `professional_verified` | Complete professional verification (docs + background + interview) | Pro-tier platform features, CRM segment "professional", priority matching | Manual (admin validation) | Y — verification criteria |
| 6 | Compte de référence (Reference Account) | `reference_account` | Admin-granted; no additional verification | Maximum trust, reference badge, premium qualification access, super-priority | Manual (admin grant only) | Y — admin-only grant policy |

### 2.2 Trust Level Transition Rules

```
L1 (new_account)
  ↓  [OTP verified]
L2 (phone_verified)
  ↓  [CNI/passport uploaded + admin validated]
L3 (identity_verified)
  ↓  [Professional docs uploaded + admin validated]
L4 (pro_docs_validated)
  ↓  [Complete verification workflow + admin approval]
L5 (professional_verified)
  ↓  [Admin manually grants]
L6 (reference_account)
```

- A user cannot skip levels (must satisfy all preceding requirements).
- A user can be downgraded by admin action (fraud, violation of TOS).
- Trust level is independent of system_role: a `user` role can be L5 if professionally verified.
- Trust level is scoped per-user, not per-organization (organization has its own trust_level).

### 2.3 Trust Score Calculation

| Component | Weight | Source |
|-----------|--------|--------|
| Trust level base | 60% | 10 pts per level (L1=10, L2=20, ... L6=60) |
| Profile completeness | 15% | % of filled profile fields |
| Activity recency | 10% | Days since last login (decay) |
| Positive interactions | 10% | Completed visits, transactions |
| Negative interactions | -5% | No-shows, complaints, fraud flags |

Trust Score = (trust_level_base × 0.60) + (profile_completeness × 0.15) + (activity_recency × 0.10) + (positive_interactions × 0.10) − (negative_interactions × 0.05)

### 2.4 Trust Level Storage on User

```
trust_level: Int (1-6)          // Current trust level
phone_verified: Boolean          // L2 gate
email_verified: Boolean          // L1 gate
identity_verified: Boolean       // L3 gate
professional_docs_verified: Boolean // L4 gate
professional_verified: Boolean   // L5 gate
reference_account: Boolean       // L6 gate
trust_score: Float               // Computed 0-100
trust_score_factors: JSON        // Contributing factors
```

---

## 3. Badge System

Eight badges derived from trust level and verification state. Badges are visual indicators displayed on user profiles and property listings.

### 3.1 Badge Catalog

| # | Badge | ID | Derivation Rule | Source Field | Human Decision | Display Context |
|---|-------|----|----------------|-------------|----------------|-----------------|
| B1 | Téléphone vérifié | `phone_verified` | Displayed when `phone_verified == true` | `phone_verified` | N | User profile |
| B2 | E-mail vérifié | `email_verified` | Displayed when `email_verified == true` | `email_verified` | N | User profile |
| B3 | Identité vérifiée | `identity_verified` | Displayed when `identity_verified == true` | `identity_verified` | N | User profile, property listings |
| B4 | Propriétaire vérifié | `owner_verified` | Displayed when `owner_verified == true` (ownership proof validated) | `owner_verified` | Y — ownership proof criteria | Property listings |
| B5 | Agence vérifiée | `agency_verified` | Displayed when `agency_verified == true` on user's Organization | `Organization.agency_verified` | Y — agency verification criteria | User profile, property listings |
| B6 | Partenaire LAWIM | `partner_lawim` | Displayed when `professional_verified == true` AND `business_profiles` includes a partner type (notaire, géomètre, banque) | `professional_verified` + `business_profiles[]` | N | User profile |
| B7 | Professionnel vérifié | `professional_verified` | Displayed when `professional_verified == true` (L5) | `professional_verified` | N | User profile, property listings |
| B8 | Agent actif | `agent_active` | Displayed when `is_active_agent == true` (fully onboarded + active) | `is_active_agent` | Y — active agent criteria | User profile, agent directory |

### 3.2 Badge Derivation Rules

- **Automatic badges** (B1, B2, B3, B7): Derived directly from boolean fields. No human decision required.
- **Manual badges** (B4, B5, B8): Require admin validation of supporting documents or criteria.
- **Composite badge** (B6): Derived from combination of `professional_verified` AND `business_profiles` membership.
- Badges are read-only computed properties — they are never directly set, only derived.
- Badge rendering is a presentation-layer concern; the backend provides the derivation API.
- A badge is removed automatically when its source condition becomes false.

### 3.3 Badge Display Priority

When displaying badges on a profile, use this order:
1. B8 — Agent actif (most operationally significant)
2. B7 — Professionnel vérifié
3. B5 — Agence vérifiée
4. B6 — Partenaire LAWIM
5. B3 — Identité vérifiée
6. B4 — Propriétaire vérifié
7. B1 — Téléphone vérifié
8. B2 — E-mail vérifié

### 3.4 Badge Storage

Badges are NOT stored as separate records. They are derived at query time via a badge calculation service:

```
function computeBadges(user):
  badges = []
  if user.phone_verified: badges.append("phone_verified")
  if user.email_verified: badges.append("email_verified")
  if user.identity_verified: badges.append("identity_verified")
  if user.owner_verified: badges.append("owner_verified")
  if user.professional_verified:
    badges.append("professional_verified")
    if hasPartnerProfile(user.business_profiles):
      badges.append("partner_lawim")
  if user.is_active_agent: badges.append("agent_active")
  if user.organization?.agency_verified: badges.append("agency_verified")
  return badges
```

---

## 4. Agency Hierarchy Roles

Four-tier hierarchy within an organization. Stored on the `OrganizationMember` join entity.

### 4.1 Role Definitions

| Role | Code | Description | Permissions | Can Manage | Typical Count per Org |
|------|------|-------------|-------------|------------|----------------------|
| Responsable | `responsible` | Agency owner/CEO. Full control over agency, members, leads, and financial data. | All agency operations | All org members | 1 |
| Admin | `admin` | Agency administrator. Operational management but not owner-level financial/legal control. | Member management, lead routing, zone assignment, reporting | Agents, assistants | 1-2 |
| Agent | `agent` | Front-line real estate agent. Manages leads, visits, transactions. | Lead management, property listing, client communication | — | 3+ |
| Assistant | `assistant` | Administrative support. Limited operational role. | Read access to shared leads, scheduling support | — | 0-3 |

### 4.2 Permission Matrix (Agency Context)

| Capability | responsible | admin | agent | assistant |
|------------|-------------|-------|-------|-----------|
| View agency leads | All | All | Assigned only | Shared only |
| Purchase leads | Y | Y | Y | N |
| List properties | Y | Y | Y | N |
| Manage members | Y | Y | N | N |
| Assign zones | Y | Y | N | N |
| View financial data | Y | N | N | N |
| Dissolve agency | Y | N | N | N |
| Configure routing | Y | Y | N | N |
| Access agent credits | Y | Y | Own only | N |

### 4.3 Onboarding Flow

```
Invitation (by responsible/admin)
  → Secure link generated
  → Account creation
  → Phone verification (OTP)
  → CNI/document upload
  → Admin validation (by responsible/admin)
  → Active (agency_role assigned)
```

Onboarding states stored on User: `invited → account_created → phone_verified → cni_uploaded → validated → active`

---

## 5. Identity Resolution Service

### 5.1 Duplicate Detection Signals

| Signal | Weight | Matching Method | Threshold |
|--------|--------|----------------|-----------|
| Phone match | 0.40 | Exact match on `phone_normalized` (E.164) | Exact |
| Email match | 0.35 | Case-insensitive exact match | Exact |
| Name similarity | 0.15 | Fuzzy string matching (Levenshtein ≤ 2 on normalized name) | ≥ 0.80 similarity |
| Device fingerprint | 0.10 | Same device ID (if available) | Exact |

### 5.2 Matching Algorithm

```
Input: User attributes (phone, email, name, device_id)
Output: Potential duplicate matches with confidence score

For each existing user:
  score = 0.0
  if phone_normalized matches: score += 0.40
  if email matches: score += 0.35
  if name_similarity >= 0.80: score += 0.15 × similarity_ratio
  if device_id matches: score += 0.10

  if score >= 0.90 AND phone_match:
    AUTO_MERGE candidate
  elif score >= 0.70:
    FLAG_FOR_REVIEW (human decision required)
  else:
    NO_MATCH (safe to create new)
```

### 5.3 Merge Algorithm

```
1. Identify survivor account (most recent active account wins)
2. On survivor:
   a. Merge properties (reassign property.owner_id → survivor)
   b. Merge projects (reassign project.user_id → survivor)
   c. Merge conversations (reassign conversation participants)
   d. Merge documents (reassign document.uploaded_by → survivor)
   e. Keep highest trust_level, merge badges
   f. Keep most complete profile fields
3. On consumed account:
   a. Set merged_into_id = survivor.id
   b. Set identity_confidence = match_score
   c. Anonymize PII (email → merged_{id}@lawim.anonymized, phone → null)
   d. Record merge_history entry on both accounts
4. Log identity_merge event in audit trail
```

### 5.4 Resolution States

```
no_match → (new user created)
potential_match (0.70-0.89) → human_review → merge / reject_merge / split
auto_merge (≥ 0.90 + phone) → merge_completed → audit_logged
```

### 5.5 Identity Resolution Storage

```
User.phone_normalized: String (E.164)
User.identity_confidence: Float (0.0-1.0)
User.merged_into_id: UUID? (self-referential)
User.merge_history: JSON[]
```

---

## 6. GDPR Deletion Workflow

### 6.1 Workflow States

```
none
  → [User requests deletion]
requested
  → [Admin verifies identity]
processing
  → [Data anonymization]
  → [Account deactivation]
  → [Data deletion except legal holds]
completed
```

### 6.2 State Machine

| State | Entry Condition | Actions | Exit Condition |
|-------|----------------|---------|----------------|
| `none` | Default state | — | User submits deletion request |
| `requested` | Deletion request submitted | Log event, notify admin | Identity verified |
| `processing` | Identity confirmed by admin | Anonymize PII, deactivate account, delete non-hold data | All steps completed |
| `completed` | Deletion finalized | Send confirmation to user, record completion timestamp | — |

### 6.3 Data Deletion Rules

| Data Category | Action | Legal Exception |
|--------------|--------|-----------------|
| Email | Anonymize | — |
| Phone | Anonymize | — |
| Name | Anonymize | — |
| Password hash | Delete | — |
| Properties owned | Keep (reassign to org/null) | Transaction history |
| Projects | Keep (anonymize creator reference) | Transaction history |
| Conversations | Keep (anonymize participant) | Contractual record |
| Transactions | Keep (anonymize party references) | Legal/accounting hold (5 years) |
| Documents | Keep (anonymize uploader) | Legal/accounting hold |
| Payments | Keep | Accounting hold (10 years) |
| Messages | Keep (anonymize sender) | Contractual record |
| Audit logs | Keep | System integrity |

Anonymization replaces PII with `[deleted_{uuid}]` placeholder.

### 6.4 Storage Fields

```
User.gdpr_deletion_requested_at: DateTime?
User.gdpr_deletion_completed_at: DateTime?
User.gdpr_deletion_status: Enum (none | requested | processing | completed)
User.anonymized_at: DateTime?
```

---

## 7. 61 Role Concepts Mapped to User Model Extensions

The 61 roles from Heritage Gold are mapped to the unified User model through 4 enrichment mechanisms:

### 7.1 Mapping Mechanisms

| Mechanism | Number of Roles | Storage | Examples |
|-----------|----------------|---------|----------|
| **system_role** (V2 enum) | 5 | `User.role` | `admin`, `manager`, `operator`, `partner`, `user` |
| **professional_category** (business_profiles) | 27 | `User.business_profiles[]` | `agent_immobilier`, `notaire`, `evaluateur` |
| **agency_role** (enum) | 4 | `OrganizationMember.agency_role` | `responsible`, `admin`, `agent`, `assistant` |
| **business_role** (derived from intent) | 9 | Project/Transaction context | `buyer`, `seller`, `tenant`, `investor` |
| **transaction_participant_role** (contextual) | 8 | Transaction fields | `buyer`, `seller`, `guarantor`, `co-signer` |
| **user_typology** (new enum) | 4 | `User.user_type` | `particular`, `professional`, `institution`, `diaspora` |
| **CRM_classification** (lead status) | 5 | `Lead.classification` | `hot`, `warm`, `cold`, `low`, `spam` |

### 7.2 Complete Role Inventory

| # | Gold Role | V2 Equivalent | Unified Classification | Storage |
|---|-----------|--------------|-----------------------|---------|
| 1 | Administrateur LAWIM | admin | system_role | User.role |
| 2 | Gestionnaire LAWIM | manager | system_role | User.role |
| 3 | Opérateur LAWIM | operator | system_role | User.role |
| 4 | Partenaire LAWIM | partner | system_role | User.role |
| 5 | Utilisateur standard | user | system_role | User.role |
| 6 | Responsable d'agence | — | agency_role | OrganizationMember.agency_role |
| 7 | Admin d'agence | — | agency_role | OrganizationMember.agency_role |
| 8 | Agent immobilier | — | agency_role | OrganizationMember.agency_role |
| 9 | Assistant d'agence | — | agency_role | OrganizationMember.agency_role |
| 10 | Demandeur (buyer/tenant) | — | business_role | Project context |
| 11 | Détenteur (seller/landlord) | — | business_role | Project context |
| 12 | Investisseur | — | business_role | Project context |
| 13 | Visiteur | — | business_role | Project context |
| 14 | Client (find/service) | — | business_role | Project context |
| 15 | Agent immobilier (pro) | partner | professional_category | User.business_profiles[] |
| 16 | Notaire | — | professional_category | User.business_profiles[] |
| 17 | Géomètre | — | professional_category | User.business_profiles[] |
| 18 | Évaluateur / Expert immobilier | — | professional_category | User.business_profiles[] |
| 19 | Architecte | — | professional_category | User.business_profiles[] |
| 20 | Courtier | — | professional_category | User.business_profiles[] |
| 21 | Maçon | — | professional_category | User.business_profiles[] |
| 22 | Menuisier | — | professional_category | User.business_profiles[] |
| 23 | Peintre | — | professional_category | User.business_profiles[] |
| 24 | Carreleur | — | professional_category | User.business_profiles[] |
| 25 | Couvreur | — | professional_category | User.business_profiles[] |
| 26 | Plombier | — | professional_category | User.business_profiles[] |
| 27 | Électricien | — | professional_category | User.business_profiles[] |
| 28 | Syndic | — | professional_category | User.business_profiles[] |
| 29 | Gardiennage / Sécurité | — | professional_category | User.business_profiles[] |
| 30 | Prestataire administratif | — | professional_category | User.business_profiles[] |
| 31 | Vidéaste / Drone | — | professional_category | User.business_profiles[] |
| 32 | Photographe | — | professional_category | User.business_profiles[] |
| 33 | Agent de nettoyage | — | professional_category | User.business_profiles[] |
| 34 | Agent d'entretien | — | professional_category | User.business_profiles[] |
| 35 | Déménageur | — | professional_category | User.business_profiles[] |
| 36 | Conseiller juridique | — | professional_category | User.business_profiles[] |
| 37 | Conseiller fiscal | — | professional_category | User.business_profiles[] |
| 38 | Assureur | — | professional_category | User.business_profiles[] |
| 39 | Banque / Institution financière | — | professional_category | User.business_profiles[] |
| 40 | Promoteur immobilier | — | professional_category | User.business_profiles[] |
| 41 | Syndic de copropriété | — | professional_category | User.business_profiles[] |
| 42 | HÔTELIER | — | professional_category | User.business_profiles[] |
| 43 | Particulier | — | user_typology | User.user_type |
| 44 | Professionnel | — | user_typology | User.user_type |
| 45 | Institution | — | user_typology | User.user_type |
| 46 | Diaspora | — | user_typology | User.user_type |
| 47 | Lead HOT | — | CRM_classification | Lead.classification |
| 48 | Lead WARM | — | CRM_classification | Lead.classification |
| 49 | Lead COLD | — | CRM_classification | Lead.classification |
| 50 | Lead LOW | — | CRM_classification | Lead.classification |
| 51 | Lead SPAM | — | CRM_classification | Lead.classification |
| 52 | Acheteur (buyer legal) | — | transaction_participant_role | Transaction.demandeur_id |
| 53 | Vendeur (seller legal) | — | transaction_participant_role | Transaction.holder_id |
| 54 | Preneur (lessee) | — | transaction_participant_role | Transaction.demandeur_id |
| 55 | Bailleur (lessor) | — | transaction_participant_role | Transaction.holder_id |
| 56 | Garant (guarantor) | — | transaction_participant_role | Transaction.guarantor_id |
| 57 | Co-signataire (co-signer) | — | transaction_participant_role | Transaction.co_signer_id |
| 58 | Bénéficiaire (beneficiary) | — | transaction_participant_role | Transaction.beneficiary_id |
| 59 | Mandataire (agent legal rep) | — | transaction_participant_role | Transaction.agent_id |
| 60 | Invité (not onboarded) | — | onboarding_status | User.onboarding_status |
| 61 | Actif (fully onboarded) | — | onboarding_status | User.onboarding_status |

---

## 8. Role Classification Rules

### 8.1 Permanent vs Contextual Role

| Property | Permanent Role | Contextual Role |
|----------|---------------|-----------------|
| **Definition** | Attached to User record indefinitely | Scoped to a specific Project, Transaction, or Lead |
| **Examples** | system_role, user_typology, professional_category, agency_role | business_role, transaction_participant_role, CRM_status |
| **Lifetime** | Until explicitly changed by admin or user | Until the scoping entity is completed/archived |
| **Authorization** | Admin assignment or self-declaration (with verification) | Derived from user action (creating a project, entering a transaction) |
| **Storage** | Fields on User or OrganizationMember | Foreign keys on Project, Transaction, Lead |

### 8.2 Verified vs Declared Role

| Property | Verified Role | Declared Role |
|----------|--------------|---------------|
| **Definition** | Backed by validated documentary evidence | Self-reported without mandatory verification |
| **Examples** | `identity_verified`, `professional_verified`, `owner_verified` | `business_profiles[]`, `user_typology` |
| **Evidence required** | CNI/passport, professional certificate, title deed | None (or minimal: email confirmation) |
| **Trust impact** | Contributes to trust score, unlocks badges | Does not affect trust score |
| **Display** | Shows verification badge | Shows as profile info without badge |

### 8.3 Individual vs Organizational Role

| Property | Individual Role | Organizational Role |
|----------|----------------|---------------------|
| **Scope** | Personal to the natural person | Tied to membership in an organization |
| **Examples** | system_role, user_typology, professional_category, business_role | agency_role (responsible/admin/agent/assistant) |
| **Portability** | Follows the user across organizations | Lost when user leaves the organization |
| **Authorization** | Self-registration or platform admin | Organization responsible/admin assigns |
| **Verification** | Individual document verification | Organization-level verification (RCCM, tax ID) |

### 8.4 Validity Dates

Not all roles have expiry, but where applicable:

| Role Type | Validity Period | Extension/Renewal |
|-----------|----------------|-------------------|
| system_role | Indefinite (revocable by admin) | — |
| agency_role | Indefinite while member of organization | — |
| professional_category | Linked to professional document expiry (1-3 years typical) | Re-verify on expiry |
| business_role | Duration of Project | — |
| transaction_participant_role | Duration of Transaction | — |
| CRM_status | Duration of Lead (max 90 days without activity) | Re-classify on new activity |
| trust_level L6 (reference_account) | Indefinite (revocable by admin) | Annual review recommended |

### 8.5 Source (Provenance)

Every role assignment should track its source:

| Source Type | Description | Examples |
|-------------|-------------|----------|
| `self_declared` | User declared this themselves | business_profiles, user_typology |
| `system_assigned` | Automatically assigned by the system | system_role default, business_role from intent |
| `admin_assigned` | Platform admin manually assigned | system_role upgrade, trust_level L6 |
| `org_assigned` | Organization responsible/admin assigned | agency_role, zone assignment |
| `verified` | Backed by document verification | identity_verified, professional_verified |

Storage: Each role-carrying entity stores a `source` field where applicable (e.g., `User.source` for user_typology).

### 8.6 Proof

| Role Type | Acceptable Proof | Verification Method |
|-----------|-----------------|---------------------|
| identity_verified | CNI (National ID), Passport, Residence permit | Admin visual validation of document photo |
| professional_verified | Professional license, Diploma, RCCM, Order registration | Admin validation + optional background check |
| owner_verified | Land title, Tax receipt, Notarized deed | Admin validation against public records |
| agency_verified | RCCM, Tax ID, CNI of responsible | Admin validation |
| email_verified | OTP to email address | Automatic |
| phone_verified | OTP via SMS | Automatic |

### 8.7 Derived Permissions

Permissions are derived from the intersection of system_role, agency_role, and permission_scope:

```
effective_permission = f(system_role, agency_role, resource_type, scope)

Examples:
- User(role=operator) + agent in org → Can edit own properties + org properties
- User(role=user) + no org → Can edit own properties only
- User(role=admin) + responsible in org → Can edit all properties + manage members
```

The 4 permission levels (R=Read, C=Create, E=Edit, A=Approve) and their scope (own, managed, org, all) are defined in the Permission Matrix (see UDM §14).

### 8.8 Required Consent

| Consent Type | Required For | Collection Method | Revocable |
|-------------|-------------|-------------------|-----------|
| Platform TOS | Account creation | Checkbox during signup | Termination only |
| Data processing (GDPR) | Account creation | Explicit checkbox | Y — triggers deletion |
| Marketing opt-in | Marketing communications | Optional checkbox | Y — unsubscribe |
| Agent opt-in | Lead routing to agent | Explicit consent during onboarding | Y — stop routing |
| Data sharing for matching | Inclusion in matching pool | Explicit consent during project creation | Y — pause matching |
| Double consent (contact) | Contact between parties | Each party must explicitly consent | Y — withdraw consent |
| Professional verification | Verification process | Explicit consent + document upload | Y — withdraw docs |
| Agency membership | Joining organization | Accept invitation | Y — leave organization |

---

## 9. Multi-Role Persona Model

A single natural person can simultaneously hold multiple roles across different dimensions. This section demonstrates the flexibility of the model.

### 9.1 Example Persona: Mr. Kamga

| Context | Role(s) Held | Role Category | Validity |
|---------|-------------|--------------|----------|
| Platform authentication | Authenticated user (`user`) | system_role | Permanent |
| Property ownership | Owner of 3 properties | business_role (holder) | Per property |
| Transaction: selling Apt A | Seller | business_role + transaction_participant_role | Per transaction |
| Transaction: buying Land B | Buyer | business_role + transaction_participant_role | Per transaction |
| Investment portfolio | Investor in 2 rental properties | business_role | Per project |
| Agency membership | Agent at "LAWIM Immobilier Yaoundé" | agency_role (agent) | Per organization |
| Professional standing | Licensed real estate agent | professional_category | Verified (L5) |
| Trust level | Level 5 — Professionnel vérifié | trust_level | Permanent |
| Organization membership | Member of "Association des Agents Agréés" | organization_role (member) | Per organization |

### 9.2 Role Resolution Rules

When determining "what role does this user have in this context":

1. **Platform context** → Check `system_role` (User.role)
2. **Project context** → Check if user is `project.user_id` (creator/demandeur) or `project.holder_id` (holder) → derived business_role
3. **Transaction context** → Check if user is referenced in Transaction party fields → transaction_participant_role
4. **Organization context** → Check `OrganizationMember.agency_role` for the user's active organization
5. **Professional context** → Check `business_profiles[]` for professional_category
6. **Lead context** → Check `Lead.user_id` for CRM_status

### 9.3 Role Conflict Detection

| Conflict Type | Description | Resolution |
|--------------|-------------|------------|
| Agent vs Buyer in same transaction | User is both the agent and the buyer in the same deal | Flag as conflict of interest; require disclosure |
| Responsible in two agencies | User is listed as responsible for two competing agencies | Flag; require one to designate a different responsible |
| Seller vs Buyer same property | User attempts to both buy and sell the same property | Reject as impossible |
| Owner vs Agent with conflict | User is both owner and agent on the same property listing | Flag; require disclosure on listing |

---

## 10. Complete Extension Mapping Table

All identity/role extensions from `required_extensions.json` mapped to proposed entities.

### 10.1 Trust Level Extensions (6)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-RL-TRUST-001 | Niveau 1 — Nouveau compte | User | `trust_level` (Int, default 1) | P1 |
| EXT-RL-TRUST-002 | Niveau 2 — Téléphone vérifié | User | `phone_verified` (Boolean) + OTP flow | P1 |
| EXT-RL-TRUST-003 | Niveau 3 — Identité vérifiée | User | `identity_verified` (Boolean) + doc upload + admin validation | P1 |
| EXT-RL-TRUST-004 | Niveau 4 — Documents pro validés | User | `professional_docs_verified` (Boolean) + pro doc workflow | P2 |
| EXT-RL-TRUST-005 | Niveau 5 — Professionnel vérifié | User | `professional_verified` (Boolean) + full verification | P2 |
| EXT-RL-TRUST-006 | Niveau 6 — Compte de référence | User | `reference_account` (Boolean) + admin grant | P3 |

### 10.2 Badge Extensions (8)

| Extension ID | Concept | Proposed Entity | Derivation | Priority |
|-------------|---------|----------------|------------|----------|
| EXT-RL-BADGE-001 | Badge: Téléphone vérifié | Badge (derived) | From `phone_verified` | P2 |
| EXT-RL-BADGE-002 | Badge: E-mail vérifié | Badge (derived) | From `email_verified` | P2 |
| EXT-RL-BADGE-003 | Badge: Identité vérifiée | Badge (derived) | From `identity_verified` | P2 |
| EXT-RL-BADGE-004 | Badge: Propriétaire vérifié | Badge (derived) | From `owner_verified` | P2 |
| EXT-RL-BADGE-005 | Badge: Agence vérifiée | Badge (derived) | From `Organization.agency_verified` | P2 |
| EXT-RL-BADGE-006 | Badge: Partenaire LAWIM | Badge (derived) | From `professional_verified` + `business_profiles` | P2 |
| EXT-RL-BADGE-007 | Badge: Professionnel vérifié | Badge (derived) | From `professional_verified` | P2 |
| EXT-RL-BADGE-008 | Badge: Agent actif | Badge (derived) | From `is_active_agent` | P3 |

### 10.3 Agency Structure Extensions (9)

| Extension ID | Concept | Proposed Entity | Target Fields | Priority |
|-------------|---------|----------------|--------------|----------|
| EXT-RL-AGENCY-001 | Agent onboarding flow | User | `onboarding_status` enum | P2 |
| EXT-RL-AGENCY-002 | Minimum 3 agents rule | Organization | `min_agents_required`, `agent_count`, `is_operational` | P3 |
| EXT-RL-AGENCY-003 | Lead routing by zone | OrganizationMember | `zones` (String[]) + routing engine | P2 |
| EXT-RL-AGENCY-004 | Lead cost (500 FCFA) | LeadPurchase | `price_per_lead` | P1 |
| EXT-RL-AGENCY-005 | Agent credits & boosts | AgentCredit | `balance`, `total_purchased`, `total_consumed` | P1 |
| EXT-RL-AGENCY-006 | Agent rating (1-5) | User | `agent_rating` (Float) | P2 |
| EXT-RL-AGENCY-007 | Agency hierarchy roles | OrganizationMember | `agency_role` enum | P2 |
| EXT-RL-AGENCY-008 | Agency trust & validation | Organization | `trust_level`, `verification_status`, `agency_verified` | P2 |
| EXT-RL-AGENCY-009 | Registration fields (RCCM, CNI, tax ID) | Organization | `rccm`, `tax_id`, `cni_document_id`, `registration_document_id` | P2 |

---

*End of IDENTITY_ROLE_EXTENSION_MODEL.md — 23 identity/role extensions mapped, 9 role categories distinguished, 61 role concepts inventoried.*
