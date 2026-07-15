# PRIVACY AND SENSITIVE FIELDS — Data Protection Framework

**Document ID:** LAWIM-GOLD-QM-PRIVACY-V1
**Status:** CANONICAL — Complete privacy framework covering all field classifications, handling rules, and legal basis
**Date:** 2026-07-15

---

## Table of Contents

1. [Privacy Level Definitions](#1-privacy-level-definitions)
2. [Sensitive Fields by Category](#2-sensitive-fields-by-category)
3. [Privacy Rules](#3-privacy-rules)
4. [Field-by-Field Privacy Classification](#4-field-by-field-privacy-classification)
5. [Data Handling Requirements](#5-data-handling-requirements)
6. [Consent Management](#6-consent-management)
7. [Channel-Specific Privacy Rules](#7-channel-specific-privacy-rules)
8. [Legal & Regulatory Compliance](#8-legal--regulatory-compliance)
9. [Implementation Guide](#9-implementation-guide)
10. [Appendix: Complete Privacy Matrix](#10-appendix-complete-privacy-matrix)

---

## 1. Privacy Level Definitions

### The Four Privacy Levels

| Level | Code | Definition | Examples | Sharing Rules | Storage Rules |
|-------|------|------------|----------|---------------|---------------|
| **Public** | 0 | Information that can be shared freely without restriction | City, property_type, neighborhood, number of rooms | Can be shared with any party, any channel | Standard storage, no encryption required |
| **Private** | 1 | Information shared only with parties directly involved in the transaction | Name, phone number, email, budget | Shared only with matched counterparty after consent | Encrypted at rest; access limited to authorized personnel |
| **Sensitive** | 2 | Information that requires explicit consent before collection or sharing | Income, financing details, title number, gender preference | Must have explicit opt-in consent; shared only with verified parties | Encrypted at rest and in transit; access logged |
| **Confidential** | 3 | Information that is never shared without legal basis and strict need-to-know | Government ID numbers, bank details, legal disputes, property deeds | Only shared with legal/notary professionals under NDA; never exposed to platform | Encrypted (AES-256); strict access control; audit trail required |

### Privacy Level Decision Tree

```
For each field:
├── Does it directly identify a person? → PRIVATE or CONFIDENTIAL
├── Is it financial information? → SENSITIVE (income) or PRIVATE (budget)
├── Is it legal/documentary? → CONFIDENTIAL
├── Is it biometric/location? → PRIVATE (address) or SENSITIVE (photos)
├── Is it demographic/preference? → PUBLIC (rooms) or SENSITIVE (gender)
└── Default → PUBLIC
```

---

## 2. Sensitive Fields by Category

### 2.1 Identity Information

| field_id | Field | Privacy Level | Rationale |
|----------|-------|---------------|-----------|
| FLD-NOM | Nom (Name) | PRIVATE | Direct personal identifier |
| FLD-TELEPHONE | Téléphone (Phone) | PRIVATE | Direct contact information |
| FLD-EMAIL | Email | PRIVATE | Contact information |
| FLD-CANAL_PREFERE | Canal préféré | PRIVATE | Communication preference |
| FLD-LANGUE | Langue | PRIVATE | Personal preference |
| FIN-COMMON-020 | email_contact | PRIVATE | Contact for financing follow-up |
| FIN-COMMON-021 | telephone_contact | PRIVATE | Contact for financing follow-up |
| PRO-COMMON-014 | Canal contact | PRIVATE | Communication channel preference |

### 2.2 Financial Information

| field_id | Field | Privacy Level | Rationale |
|----------|-------|---------------|-----------|
| FLD-BUDGET_MAX | Budget maximum | PRIVATE | Financial capacity indicator |
| FLD-BUDGET_MIN | Budget minimum | PRIVATE | Financial capacity indicator |
| FLD-BUDGET_NEGOTIABLE | Négociable | PRIVATE | Financial strategy indicator |
| FLD-APPORT | Apport personnel | SENSITIVE | Down payment = financial position |
| FLD-REVENUS | Revenus (Income) | SENSITIVE | Personal financial data |
| FLD-REVENUS_SOURCE | Source de revenus | SENSITIVE | Income source = personal data |
| FLD-GARANTIES | Garanties | SENSITIVE | Financial guarantee details |
| FLD-CAUTION | Caution (Deposit) | CONFIDENTIAL | Actual deposit amount |
| FLD-FINANCING | Financement | SENSITIVE | Financing method reveals financial status |
| FLD-SOURCE_FINANCEMENT | Source de financement | SENSITIVE | Funding source origin |
| FIN-COMMON-013 | revenus_mensuels | SENSITIVE | Monthly income — encrypted |
| FIN-COMMON-014 | revenus_net | SENSITIVE | Net income — encrypted |
| FIN-COMMON-016 | autres_engagements | SENSITIVE | Other commitments — encrypted |
| FIN-COMMON-018 | garanties_disponibles | SENSITIVE | Guarantees — encrypted |
| FIN-SAL-003 | revenu_mensuel_brut | SENSITIVE | Gross salary — encrypted |
| FIN-SAL-004 | revenu_net_mensuel | SENSITIVE | Net salary — encrypted |
| FIN-SAL-007 | domiciliation_bancaire | SENSITIVE | Banking info — encrypted |
| FIN-SE-003 | chiffre_affaires_mensuel | SENSITIVE | Business revenue — encrypted |
| FIN-SE-004 | chiffre_affaires_annuel | SENSITIVE | Annual revenue — encrypted |
| FIN-SE-005 | resultat_mensuel | SENSITIVE | Monthly result — encrypted |
| FIN-SE-009 | documents_fiscaux | SENSITIVE | Tax documents — encrypted |
| FIN-SE-010 | releves_bancaires | SENSITIVE | Bank statements — encrypted |
| FIN-COMMON-012 | taux_remboursement_souhaite | SENSITIVE | Repayment capacity |
| INV-COMMON-001 | budget_investissement | SENSITIVE | Investment budget |
| INV-COMMON-003 | horizon_investissement | PRIVATE | Investment horizon |
| INV-COMMON-009 | source_financement | SENSITIVE | Funding source |

### 2.3 Legal Information

| field_id | Field | Privacy Level | Rationale |
|----------|-------|---------------|-----------|
| FLD-TITRE_REQUIS | Titre requis | PUBLIC | Yes/no preference — public |
| FLD-TYPE_TITRE | Type de titre | SENSITIVE | Reveals legal situation |
| FLD-NUM_TITRE | Numéro titre foncier | CONFIDENTIAL | Direct property identifier |
| FLD-LITIGES_CONNUS | Litiges connus | CONFIDENTIAL | Legal dispute — highly sensitive |
| FLD-HYPOTHEQUE | Hypothèque | CONFIDENTIAL | Financial encumbrance |
| FLD-PROCURATION | Procuration | CONFIDENTIAL | Legal delegation |
| FLD-SERVITUDES | Servitudes | SENSITIVE | Legal encumbrance |
| FLD-IDENTITE_SIGNATAIRES | Identité signataires | CONFIDENTIAL | Identity of co-owners |
| FLD-SIGNATAIRES_NOMBRE | Nombre signataires | SENSITIVE | Number of co-owners |
| FIN-CONS-002 | statut_juridique_terrain | SENSITIVE | Land legal status — encrypted |
| FIN-CONS-007 | permis_autorisations | SENSITIVE | Permit status — encrypted |
| LAND-COMMON-type_document | Type de document | SENSITIVE | Document type |
| LAND-COMMON-certificat_propriete | Certificat de propriété | CONFIDENTIAL | Property certificate |

### 2.4 Documentary Information

| field_id | Field | Privacy Level | Rationale |
|----------|-------|---------------|-----------|
| FIN-COMMON-019 | documents_disponibles | CONFIDENTIAL | Document list — never shared |
| FIN-SE-009 | documents_fiscaux | CONFIDENTIAL | Tax documents — never shared |
| FIN-SE-010 | releves_bancaires | CONFIDENTIAL | Bank statements — never shared |
| PRO-COMMON-010 | qualification_agrement | SENSITIVE | Certification documents |
| PRO-COMMON-015 | nature_operation | SENSITIVE | Legal operation nature |
| LAND-COMMON-plan_bornage | Plan de bornage | SENSITIVE | Boundary survey plan |
| LAND-COMMON-pv_bornage | PV de bornage | CONFIDENTIAL | Official boundary minutes |
| LAND-COMMON-certificat_urbanisme | Certificat d'urbanisme | CONFIDENTIAL | Town planning cert |

### 2.5 Exact Location Information

| field_id | Field | Privacy Level | Rationale |
|----------|-------|---------------|-----------|
| FLD-ADRESSE_EXACTE | Adresse exacte | PRIVATE | Exact address — only shared with consent |
| FLD-COORDONNEES_GPS | Coordonnées GPS | PRIVATE | GPS coordinates — shared before visit only |
| FLD-PROXIMITY_PREFERENCES | Proximité | PUBLIC | General proximity, not exact |
| SVC-COMMON-localisation_bien | Localisation bien | PRIVATE | Property location |
| SVC-COMMON-adresse_chantier | Adresse chantier | PRIVATE | Construction site address |

### 2.6 Biometric & Visual Information

| field_id | Field | Privacy Level | Rationale |
|----------|-------|---------------|-----------|
| FLD-PHOTO_TERRAIN | Photo du terrain | SENSITIVE | Visual property record |
| FLD-VIDEO_TERRAIN | Video du terrain | SENSITIVE | Visual property record |
| SVC-COMMON-photos_bien | Photos du bien | SENSITIVE | Property photos — owner consent needed |
| SVC-COMMON-video_bien | Video du bien | SENSITIVE | Property video — owner consent needed |
| SVC-COMMON-portfolio_photos | Portfolio photos | SENSITIVE | Professional portfolio |

### 2.7 Preference & Demographic Information

| field_id | Field | Privacy Level | Rationale |
|----------|-------|---------------|-----------|
| FLD-GENRE_PREFERENCE | Préférence genre | SENSITIVE | Gender preference — potentially discriminatory |
| FLD-AGE_RANGE | Tranche d'âge | SENSITIVE | Age preference — potentially discriminatory |
| FLD-BOURSE | Bourse | SENSITIVE | Financial aid — personal information |
| PRO-COMMON-016 | type_projet | PUBLIC | Project type |
| PRO-COMMON-017 | type_travaux | PUBLIC | Work type |

---

## 3. Privacy Rules

### Rule 1: Requester Anonymous Until Holder Accepts Relationship

**Statement**: The requester's identity MUST NOT be disclosed to the property holder until the holder has accepted the relationship (expressed interest in the match).

**Implementation**:
```
1. Qualification phase: requester = anonymous UUID
2. Matching phase: requester = anonymous profile (city, budget, criteria)
3. Interest phase: holder sees "Someone is interested in your property"
4. Acceptance: holder accepts → requester identity revealed
5. Double consent: ask both parties before sharing contact info
```

**Exceptions**:
- Requester explicitly gives permission to share identity early
- Both parties are known to each other (e.g., referral)

### Rule 2: Minimum Necessary Principle

**Statement**: Only collect and share the minimum information necessary for the current stage of the transaction.

**Implementation**:

| Stage | Information Shared with Counterparty |
|-------|--------------------------------------|
| Search/Qualification | Anonymous profile (criteria only) |
| Match notification | "Interested party" — no identity |
| Introduction | Name + preferred channel (with consent) |
| Visit | Phone number (with consent) |
| Transaction | Full identity (as required by notary/law) |

**Checklist for each data sharing request**:
- [ ] Is this information necessary for the current step?
- [ ] Has the user consented to share this specific information?
- [ ] Is there a less sensitive alternative?
- [ ] Can the information be minimized (e.g., city instead of address)?

### Rule 3: Never Disclose Exact Address Before Authorization

**Statement**: The exact address of a property MUST NOT be shared with a potential tenant/buyer until they have explicitly confirmed they want to visit.

**Implementation**:
```
Before visit confirmation:
  - Share neighborhood, zone, nearby landmarks
  - Share approximate location (e.g., "near the market")
  - NOT the exact street number

After visit confirmation:
  - Share exact address privately
  - Include access instructions
  - Send GPS coordinates if needed
```

**Exception**: Commercial properties where address is public (storefronts, offices) may share general location earlier.

### Rule 4: Never Share Sensitive Documents Without Explicit Consent

**Statement**: Sensitive and confidential documents (identity documents, bank statements, tax records, title deeds) MUST NEVER be shared through the platform. They are exchanged directly between parties or through professional intermediaries.

**Implementation**:
```
CANNOT share via platform:
  - Identity documents (passport, national ID)
  - Bank statements
  - Tax returns
  - Title deeds (full copies)
  - Signed contracts

CAN share via platform (with consent):
  - Name, phone, email
  - Budget range
  - Property criteria
  - Availability

MUST use external channels:
  - Notary-to-notary document exchange
  - Bank-to-bank verification
  - Lawyer-to-lawyer contract review
```

### Rule 5: Data Minimization in Storage

**Statement**: Store only what is needed, for only as long as needed.

**Storage Duration**:
- Qualification data: 90 days after last interaction
- Transaction data: 5 years (legal requirement)
- Financial data: 5 years after transaction
- Anonymized data: Indefinite (de-identified)

**Deletion**:
- User can request deletion at any time ("SUPPRIMER MES DONNÉES")
- Deletion must be completed within 7 days
- Anonymized data may be retained

---

## 4. Field-by-Field Privacy Classification

### 4.1 Transaction & Intent Fields

| field_id | Label | Privacy Level | Justification |
|----------|-------|---------------|---------------|
| FLD-TRANSACTION | Transaction | PUBLIC | Intent to transact — not personal |
| FLD-INTENT | Intention | PUBLIC | Search intent — not personal |
| FLD-PROPERTY_TYPE | Type de bien | PUBLIC | Property preference |
| FLD-REQUEST_FAMILY | Famille demande | PUBLIC | System category |
| FLD-JOURNEY_STAGE | Étape parcours | PUBLIC | Progress indicator |
| FLD-USAGE | Usage | PUBLIC | Property usage intent |
| FLD-INTENT_CONFIDENCE | Confiance intention | PUBLIC | System metadata |

### 4.2 Location Fields

| field_id | Label | Privacy Level | Justification |
|----------|-------|---------------|---------------|
| FLD-CITY | Ville | PUBLIC | City-level — not identifying |
| FLD-NEIGHBORHOOD | Quartier | PUBLIC | Neighborhood-level — low sensitivity |
| FLD-ZONE | Zone | PUBLIC | Broad zone description |
| FLD-CITY_ALTERNATIVES | Autres villes | PUBLIC | Alternative cities |
| FLD-NEIGHBORHOOD_ALTERNATIVES | Autres quartiers | PUBLIC | Alternative neighborhoods |
| FLD-PROXIMITY_PREFERENCES | Proximité | PUBLIC | General proximity |
| FLD-MOBILITY | Mobilité | PUBLIC | Flexibility level |
| FLD-COORDONNEES_GPS | Coordonnées GPS | PRIVATE | Exact location — shared with consent |
| FLD-ADRESSE_EXACTE | Adresse exacte | PRIVATE | Exact address — shared with consent |

### 4.3 Budget & Financial Fields

| field_id | Label | Privacy Level | Justification |
|----------|-------|---------------|---------------|
| FLD-BUDGET_MAX | Budget maximum | PRIVATE | Financial capacity |
| FLD-BUDGET_MIN | Budget minimum | PRIVATE | Financial range |
| FLD-BUDGET_TYPE | Type de budget | PUBLIC | Budget category |
| FLD-BUDGET_CURRENCY | Devise | PUBLIC | Currency type |
| FLD-BUDGET_NEGOTIABLE | Négociable | PRIVATE | Negotiation strategy |
| FLD-CAUTION | Caution | CONFIDENTIAL | Actual deposit amount |
| FLD-CHARGES | Charges | PUBLIC | Utility inclusion |
| FLD-FINANCING | Financement | SENSITIVE | Financing method |
| FLD-APPORT | Apport personnel | SENSITIVE | Down payment amount |
| FLD-REVENUS | Revenus | SENSITIVE | Personal income |
| FLD-REVENUS_SOURCE | Source revenus | SENSITIVE | Income origin |
| FLD-GARANTIES | Garanties | SENSITIVE | Guarantee types |
| FLD-MONTANT_RECHERCHE | Montant recherche | PRIVATE | Amount sought |
| FLD-COUT_TOTAL_PROJET | Coût total projet | PRIVATE | Project cost |
| FLD-RENDEMENT_ATTENDU | Rendement attendu | PRIVATE | Target yield |
| FLD-RISQUE_ACCEPTE | Risque accepté | PRIVATE | Risk tolerance |

### 4.4 Property Characteristic Fields

| field_id | Label | Privacy Level | Justification |
|----------|-------|---------------|---------------|
| FLD-CHAMBRES | Chambres | PUBLIC | Room count |
| FLD-DOUCHES | Douches | PUBLIC | Bathroom count |
| FLD-SALONS | Salons | PUBLIC | Living room count |
| FLD-CUISINE | Cuisine | PUBLIC | Kitchen type |
| FLD-MEUBLE | Meublé | PUBLIC | Furnishing status |
| FLD-SURFACE | Surface | PUBLIC | Area size |
| FLD-SURFACE_TERRAIN | Surface terrain | PUBLIC | Land area |
| FLD-ETAGE | Étage | PUBLIC | Floor level |
| FLD-ASCENSEUR | Ascenseur | PUBLIC | Elevator |
| FLD-PARKING | Parking | PUBLIC | Parking |
| FLD-COUR | Cour | PUBLIC | Courtyard |
| FLD-CLOTURE | Clôture | PUBLIC | Fencing |
| FLD-BALCON | Balcon | PUBLIC | Balcony |
| FLD-JARDIN | Jardin | PUBLIC | Garden |
| FLD-PISCINE | Piscine | PUBLIC | Pool |
| FLD-CLIMATISATION | Climatisation | PUBLIC | AC |
| FLD-GROUPE_ELECTROGENE | Groupe électrogène | PUBLIC | Generator |
| FLD-FORAGE | Forage | PUBLIC | Water well |
| FLD-INTERNET | Internet | PUBLIC | Internet |
| FLD-SECURITE | Sécurité | PUBLIC | Security |
| FLD-GARDIENNAGE | Gardiennage | PUBLIC | Guard service |
| FLD-EAU | Eau | PUBLIC | Water supply |
| FLD-ELECTRICITE | Électricité | PUBLIC | Electricity |
| FLD-ACCES_ROUTE | Accès route | PUBLIC | Road access |
| FLD-DEPENDANCES | Dépendances | PUBLIC | Outbuildings |
| FLD-ETAT_PROPRIETE | État du bien | PUBLIC | Condition |

### 4.5 Timing Fields

| field_id | Label | Privacy Level | Justification |
|----------|-------|---------------|---------------|
| FLD-DISPONIBILITE | Disponibilité | PRIVATE | Move-in date — personal schedule |
| FLD-DELAI | Délai | PRIVATE | Time horizon — personal |
| FLD-URGENCE | Urgence | PUBLIC | Urgency level |
| FLD-DATE_ARRIVEE | Date arrivée | PRIVATE | Arrival date — personal |
| FLD-DATE_DEPART | Date départ | PRIVATE | Departure date — personal |
| FLD-DUREE_LOCATION | Durée location | PRIVATE | Rental duration |
| FLD-DUREE_SEJOUR | Durée séjour | PUBLIC | Stay duration |
| FLD-DATE_SOUHAITEE | Date souhaitée | PRIVATE | Desired date |

### 4.6 Land-Specific Fields

| field_id | Label | Privacy Level | Justification |
|----------|-------|---------------|---------------|
| FLD-TITRE_REQUIS | Titre requis | PUBLIC | Preference indicator |
| FLD-TYPE_TITRE | Type de titre | SENSITIVE | Reveals legal situation |
| FLD-NUM_TITRE | Numéro titre | CONFIDENTIAL | Direct property identifier |
| FLD-SURFACE_TERRAIN_M2 | Surface terrain m2 | PUBLIC | Land measurement |
| FLD-USAGE_PREVU | Usage prévu | PUBLIC | Land use intent |
| FLD-TERRAIN_LOTI | Terrain loti | PUBLIC | Servicing status |
| FLD-TERRAIN_CONSTRUCTIBLE | Constructible | PUBLIC | Zoning status |
| FLD-LOTISSEMENT_APPROUVE | Lotissement approuvé | PUBLIC | Subdivision approval |
| FLD-INONDABLE | Inondable | PUBLIC | Flood risk |
| FLD-TOPOGRAPHIE | Topographie | PUBLIC | Terrain shape |
| FLD-OCCUPATION_ACTUELLE | Occupation actuelle | PUBLIC | Current use |
| FLD-ACCESSIBILITE_ROUTE | Accessibilité route | PUBLIC | Road access |
| FLD-DISTANCE_ROUTE | Distance route | PUBLIC | Road distance |
| FLD-SERVITUDES | Servitudes | SENSITIVE | Legal encumbrance |
| FLD-LITIGES_CONNUS | Litiges connus | CONFIDENTIAL | Legal dispute |
| FLD-HYPOTHEQUE | Hypothèque | CONFIDENTIAL | Mortgage/charge |
| FLD-SIGNATAIRES_NOMBRE | Nombre signataires | SENSITIVE | Co-owner count |
| FLD-IDENTITE_SIGNATAIRES | Identité signataires | CONFIDENTIAL | Co-owner identity |
| FLD-PROCURATION | Procuration | CONFIDENTIAL | Power of attorney |
| FLD-BORNAGE | Bornage | PUBLIC | Boundary marking |
| FLD-CERTIFICAT_URBANISME | Certificat d'urbanisme | SENSITIVE | Town planning cert |

### 4.7 Professional Service Fields

| field_id | Label | Privacy Level | Justification |
|----------|-------|---------------|---------------|
| PRO-COMMON-001 | Type prestation | PUBLIC | Service type |
| PRO-COMMON-002 | Localisation | PUBLIC | Service location |
| PRO-COMMON-003 | Description besoin | PUBLIC | Need description |
| PRO-COMMON-004 | Urgence | PUBLIC | Urgency |
| PRO-COMMON-005 | Budget fourchette | PRIVATE | Budget range |
| PRO-COMMON-006 | Date souhaitée | PRIVATE | Desired date |
| PRO-COMMON-010 | Qualification | SENSITIVE | Certification proof |
| PRO-COMMON-015 | Nature opération | SENSITIVE | Legal operation |
| PRO-AGENT-001 | identite_professionnel | PRIVATE | Professional identity |
| PRO-AGENT-001 | numero_carte_pro | SENSITIVE | Professional card |
| PRO-AGENT-001 | coordonnees_bancaires | CONFIDENTIAL | Bank details |
| PRO-AGENT-001 | situation_fiscale | CONFIDENTIAL | Tax situation |
| PRO-NOTAI-003 | identite_complete_parties | CONFIDENTIAL | Party identity |
| PRO-NOTAI-003 | montant_transaction | SENSITIVE | Transaction amount |
| PRO-NOTAI-003 | numero_titre_foncier | CONFIDENTIAL | Title number |

### 4.8 Derived Fields

| field_id | Label | Privacy Level | Justification |
|----------|-------|---------------|---------------|
| FLD-DERIVED-STANDING | Standing estimé | PUBLIC | Deduced from public data |
| FLD-DERIVED-BUDGET_COHERENCE | Cohérence budget | PUBLIC | Budget validation |
| FLD-DERIVED-URGENCE_REELLE | Urgence réelle | PUBLIC | Deduced urgency |
| FLD-DERIVED-PROFIL_ACHETEUR | Profil acheteur | PRIVATE | Inferred profile |
| FLD-DERIVED-PRIX_M2_ESTIME | Prix au m² estimé | PUBLIC | Price per m2 |
| FLD-DERIVED-COMPATIBILITE | Compatibilité | PUBLIC | Compatibility |
| FLD-DERIVED-PROFIL | Profil demandeur | PRIVATE | Requester profile |
| FLD-DERIVED-RISQUE_JURIDIQUE | Risque juridique | SENSITIVE | Legal risk assessment |
| FLD-DERIVED-CAPACITE_REMBOURSEMENT | Capacité remboursement | SENSITIVE | Derived from sensitive data |
| FLD-DERIVED-TAUX_ENDETTEMENT | Taux endettement | SENSITIVE | Debt ratio |

---

## 5. Data Handling Requirements

### 5.1 Storage Requirements by Level

| Level | Encryption | Access Control | Audit Trail | Retention |
|-------|-----------|---------------|-------------|-----------|
| PUBLIC | None required | Any authenticated user | Not required | Indefinite |
| PRIVATE | AES-256 at rest | Authorized personnel only | Optional | 90 days after last interaction |
| SENSITIVE | AES-256 at rest + TLS in transit | Role-based access | Required (access logged) | 90 days or transaction + 5yr |
| CONFIDENTIAL | AES-256 at rest + TLS in transit + field-level encryption | Named individuals only | Required (full audit trail) | Transaction + 5yr (legal) |

### 5.2 Encryption Requirements

| Data State | Standard | Implementation |
|------------|----------|----------------|
| At rest (database) | AES-256 | Column-level encryption for SENSITIVE and CONFIDENTIAL fields |
| At rest (backups) | AES-256 | Backup encryption with separate key |
| In transit (API) | TLS 1.3 | All API communication over HTTPS |
| In transit (database) | TLS 1.3 | Database connections encrypted |
| Key management | KMS | Key rotation every 90 days for CONFIDENTIAL |

### 5.3 Access Control Matrix

| Role | PUBLIC | PRIVATE | SENSITIVE | CONFIDENTIAL |
|------|--------|---------|-----------|--------------|
| User (self) | READ | READ, UPDATE | READ, UPDATE | READ, UPDATE (own) |
| User (other) | READ | NONE | NONE | NONE |
| Agent | READ | READ (matched) | READ (with consent) | NONE |
| Notary/Legal | READ | READ | READ | READ (with NDA) |
| Matching Engine | READ | READ (score only) | READ (score only) | NONE |
| Admin | READ | READ | READ (audit) | READ (audit only) |
| System | READ, WRITE | READ, WRITE | READ, WRITE (encrypted) | READ, WRITE (encrypted) |

### 5.4 Data Sharing Limits

| Sharing Scenario | PUBLIC | PRIVATE | SENSITIVE | CONFIDENTIAL |
|-----------------|--------|---------|-----------|--------------|
| To matched counterparty | Always | With consent | With explicit consent | Never via platform |
| To agent | Always | With user consent | With explicit consent | Never |
| To notary/legal | Always | Always (transaction) | Always (transaction) | With NDA |
| To matching engine | Always | Hashed/anonymized | Anonymized only | Never |
| To analytics | Aggregated only | Aggregated only | Never | Never |
| To third parties | Never | Never | Never | Never |

---

## 6. Consent Management

### 6.1 Types of Consent

| Consent Type | Required For | Duration | Withdrawal |
|-------------|--------------|----------|------------|
| General consent | Participating in platform | Until withdrawn | Anytime → deletion within 7 days |
| Contact sharing | Sharing phone/email with counterparty | Per-match | Withdraw before match accepted |
| Document sharing | Sharing sensitive documents | Per-document | Before document is opened |
| Location sharing | Sharing exact address | Per-visit | Anytime before visit |
| Financial verification | Income/guarantee verification | Per-application | Anytime before application |

### 6.2 Consent Collection

```
For PRIVATE fields:
  "Puis-je partager votre [field] avec [counterparty] ?"
  [YES] [NO]

For SENSITIVE fields:
  "Nous avons besoin de votre consentement explicite pour collecter
   [field]. Ceci est nécessaire pour [purpose]."
  [J'ACCEPTE] [JE REFUSE]

For CONFIDENTIAL fields:
  "Ces informations seront partagées uniquement avec [professional]
   sous accord de confidentialité. Voulez-vous continuer ?"
  [OUI, CONTINUER] [NON]
```

### 6.3 Consent Records

Each consent event MUST record:
- User ID
- Field ID
- Consent type (share/collect/store)
- Counterparty (who gets access)
- Timestamp
- IP/Location of consent
- Consent text shown to user
- Expiry date

### 6.4 Double Consent Protocol

```python
def share_contact(requester_id, holder_id):
    # Step 1: Ask requester
    requester_consent = ask_consent(requester_id, "Share contact?")
    if not requester_consent:
        return "Cannot proceed without your consent."
    
    # Step 2: Ask holder
    holder_consent = ask_consent(holder_id, 
        f"Someone is interested in your property. Share their contact?")
    if not holder_consent:
        notify(requester_id, "The owner is not ready to connect yet.")
        return
    
    # Step 3: Both consented → share
    share_bidirectional(requester_id, holder_id)
    notify_both("You are now connected!")
```

---

## 7. Channel-Specific Privacy Rules

### 7.1 WhatsApp

| Rule | Description |
|------|-------------|
| Never send sensitive data in messages | WhatsApp is encrypted but LAWIM policy is to not transmit SENSITIVE or CONFIDENTIAL info |
| No document attachments | Do not request or accept identity documents via WhatsApp |
| Consent must be explicit | "Puis-je partager vos coordonnées ? OUI/NON" format |
| One consent question at a time | Ask about name, then phone, then email separately |

### 7.2 Telegram

| Rule | Description |
|------|-------------|
| Slightly more permissive | Can share PRIVATE fields (name, phone) with structured consent |
| No sensitive documents | Same as WhatsApp — no document exchange |
| Consent can be batched | Ask for name + phone consent together |

### 7.3 Dashboard

| Rule | Description |
|------|-------------|
| Full consent framework | All consent types available with records |
| Document upload | Secure upload with encryption at rest |
| Access control | Role-based access to fields by level |
| Audit trail | Full logging of all field access |
| Data export | User can export their data on request |

### 7.4 SMS

| Rule | Description |
|------|-------------|
| Minimal data only | Never send PRIVATE or higher via SMS |
| No links to documents | No document download links |
| Consent not requested via SMS | Use WhatsApp/Telegram/Dashboard for consent |

### 7.5 Phone/Voice

| Rule | Description |
|------|-------------|
| Agent guidelines | Agents are trained not to ask for sensitive info unless necessary |
| Consent recorded | Verbal consent logged in CRM |
| No document request | Agents do not request documents by phone |

---

## 8. Legal & Regulatory Compliance

### 8.1 Cameroon Data Protection Law

LAWIM operates primarily in Cameroon. The key legal framework:

| Requirement | Implementation |
|-------------|----------------|
| Law No. 2013/021 on Cybersecurity | Encryption standards, breach notification |
| Law No. 2010/012 on Consumer Protection | Transparent data practices |
| OHADA Uniform Act | Contract and transaction data retention (5 years) |
| CEMAC Regulation | Cross-border data transfer restrictions |

### 8.2 GDPR Compliance (for EU Users)

For users accessing LAWIM from EU jurisdictions:

| Right | Implementation |
|-------|----------------|
| Right to be informed | Privacy policy at onboarding |
| Right of access | Data export feature |
| Right to rectification | User can update own fields |
| Right to erasure | "SUPPRIMER MES DONNÉES" command |
| Right to restrict processing | Opt-out of analytics |
| Right to data portability | JSON export available |
| Right to object | Object to profiling |
| Rights re automated decisions | Human review for automated rejections |

### 8.3 Data Breach Response

```
TIER 1: PUBLIC data exposed
  - Internal notification within 24h
  - Fix vulnerability within 72h
  - No external notification required

TIER 2: PRIVATE data exposed
  - Internal notification immediately
  - Affected users notified within 48h
  - Fix within 24h
  - Report to authority within 72h

TIER 3: SENSITIVE or CONFIDENTIAL data exposed
  - Emergency response immediately
  - Affected users notified within 24h
  - Authority notified within 24h
  - Forensic investigation
  - Legal counsel engaged
```

### 8.4 Data Retention Schedule

| Data Category | Active Retention | Archive Retention | Deletion |
|---------------|-----------------|-------------------|----------|
| Qualification data | 90 days | N/A | After 90 days |
| Contact info | Until consent withdrawn | N/A | 7 days after request |
| Transaction data | 5 years | 10 years | After 10 years |
| Financial data | 5 years | N/A | After 5 years |
| Legal documents | 10 years | 30 years | After 30 years |
| Anonymized data | Indefinite | N/A | N/A |
| Logs/audit trails | 1 year | 3 years | After 3 years |

---

## 9. Implementation Guide

### 9.1 Data Classification at Ingestion

```python
def classify_data(field_id, value, context):
    level = PRIVACY_REGISTRY.get(field_id, PRIVACY_PUBLIC)
    
    # Override based on context
    if level == PRIVACY_PUBLIC:
        return level  # Public is always public
    
    # Check user consent
    if not has_consent(context.user, field_id):
        if level == PRIVACY_PRIVATE:
            return ANONYMIZE  # Store anonymized
        elif level >= PRIVACY_SENSITIVE:
            return REJECT  # Don't collect without consent
    
    return level
```

### 9.2 Field-Level Encryption

```python
def store_sensitive_field(user_id, field_id, value):
    if PRIVACY_REGISTRY[field_id] >= PRIVACY_SENSITIVE:
        encrypted = encrypt_aes256(value, user_specific_key(user_id))
        store_encrypted(user_id, field_id, encrypted)
        log_access(user_id, field_id, 'WRITE')
    else:
        store_plaintext(user_id, field_id, value)

def read_sensitive_field(requestor_id, target_user_id, field_id):
    if not has_access(requestor_id, target_user_id, field_id):
        return None
    if PRIVACY_REGISTRY[field_id] >= PRIVACY_SENSITIVE:
        encrypted = read_encrypted(target_user_id, field_id)
        log_access(requestor_id, field_id, 'READ')
        return decrypt_aes256(encrypted, user_specific_key(target_user_id))
    return read_plaintext(target_user_id, field_id)
```

### 9.3 Anonymization for Matching Engine

```python
def anonymize_for_matching(user_profile):
    return {
        'city': user_profile.city,
        'neighborhood': user_profile.neighborhood,
        'budget_max': user_profile.budget_max,
        'budget_min': user_profile.budget_min,
        'property_type': user_profile.property_type,
        'chambres': user_profile.chambres,
        'transaction': user_profile.transaction,
        # NO identity fields, NO exact address
        # NO financial details beyond budget
        # NO legal/document information
    }
```

### 9.4 Consent Verification Before Sharing

```python
def can_share(user_id, field_id, counterparty_id):
    consent = get_consent(user_id, field_id)
    if not consent:
        return False, "Consent not provided"
    if consent.expired():
        return False, "Consent has expired"
    if not consent.covers(counterparty_id):
        return False, "Consent does not cover this party"
    return True, None
```

### 9.5 Privacy-First UI Rules

- Always show privacy level indicator next to fields in Dashboard
- Use lock icons for SENSITIVE and CONFIDENTIAL fields
- Show consent history for each field
- Provide "What will be shared" summary before introduction
- Never pre-fill SENSITIVE or CONFIDENTIAL fields
- Show clear "Why we need this" explanation for each sensitive field

---

## 10. Appendix: Complete Privacy Matrix

### Privacy Level Summary by Matrix Family

| Family | % PUBLIC | % PRIVATE | % SENSITIVE | % CONFIDENTIAL |
|--------|----------|-----------|-------------|----------------|
| RESIDENTIAL_SEARCH | 65% | 25% | 7% | 3% |
| LAND_SEARCH | 50% | 10% | 20% | 20% |
| COMMERCIAL_SEARCH | 70% | 20% | 8% | 2% |
| FINANCING_REQUEST | 35% | 20% | 35% | 10% |
| PROFESSIONAL_SEARCH | 40% | 30% | 20% | 10% |
| REAL_ESTATE_SERVICES | 55% | 25% | 15% | 5% |

### Fields That Change Privacy by Context

| field_id | Default | Changes To | When |
|----------|---------|------------|------|
| FLD-BUDGET_MAX | PRIVATE | PUBLIC | When user says "budget is not sensitive" |
| FLD-DISPONIBILITE | PRIVATE | PUBLIC | When becomes known to counterparty |
| FLD-LANGUE | PRIVATE | PUBLIC | After user agrees to communication |
| FLD-REVENUS | SENSITIVE | CONFIDENTIAL | When shared with lender (financing) |
| PRO-COMMON-005 | PRIVATE | PUBLIC | When negotiating service price |

### Enforcement Matrix

| Violation | Public | Private | Sensitive | Confidential |
|-----------|--------|---------|-----------|--------------|
| Unauthorized access | Warning | Written warning | Suspension | Immediate termination |
| Unauthorized sharing | Warning | Suspension | Termination | Legal action |
| Failed encryption | Fix immediately | Fix immediately | Incident report | Emergency + legal |
| Missing consent | Warning | Block operation | Block + notify | Block immediately |
| Retention breach | Internal fix | Internal fix + notice | Notice + audit | Legal review |

---

**End of PRIVACY_AND_SENSITIVE_FIELDS.md**
