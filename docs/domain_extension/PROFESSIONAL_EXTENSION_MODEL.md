# PROFESSIONAL EXTENSION MODEL

**Document ID:** LAWIM-H13-PROFESSIONAL-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §1 (Identity Model), §3 (Service Model), §12 (Organization Model), §10 (CRM Pipeline)
**Source Crosswalks:** required_extensions.json (professional), CRM_EXTENSION_MODEL.md §9 (Agent Rating), QUALIFICATION_EXTENSION_MODEL.md §10.6 (Professional Matrices), SERVICE_TAXONOMY_EXTENSION_MODEL.md

---

## Table of Contents

1. [Professional Profile Entity](#1-professional-profile-entity)
2. [Professional Categories](#2-professional-categories)
3. [Service Capability Model](#3-service-capability-model)
4. [License and Certification Tracking](#4-license-and-certification-tracking)
5. [Geographic Coverage Model](#5-geographic-coverage-model)
6. [Availability and Scheduling](#6-availability-and-scheduling)
7. [Rating System](#7-rating-system)
8. [Verification Workflow](#8-verification-workflow)
9. [Pricing Models per Professional Type](#9-pricing-models-per-professional-type)
10. [SLA per Professional Type](#10-sla-per-professional-type)
11. [Organization Membership Hierarchy](#11-organization-membership-hierarchy)
12. [Complete Extension Mapping Table](#12-complete-extension-mapping-table)

---

## 1. Professional Profile Entity

The professional profile transforms a User from a simple CRM contact into a full service provider with capabilities, credentials, and availability. A professional is defined by what they can do, where they operate, and how they deliver.

### 1.1 Core Professional Profile Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `user_id` | UUID | Reference to User (the person behind the professional) |
| `professional_type` | Enum | Primary category (see §2) |
| `secondary_types` | Enum[] | Additional professional categories |
| `professional_name` | String | Business name / professional name |
| `professional_email` | String? | Professional contact email |
| `professional_phone` | String? | Professional contact phone |
| `business_address` | String? | Registered business address |
| `website` | String? | Professional website |
| `social_links` | JSON? | Social media profiles `{linkedin, facebook, instagram, whatsapp_business}` |
| `bio` | Text? | Professional summary / biography |
| `years_experience` | Int | Years of professional experience |
| `employee_count` | Int? | Number of employees (for agencies/enterprises) |
| `professional_status` | Enum | `active \| inactive \| suspended \| archived` |
| `is_verified` | Boolean | Whether the professional has been verified |
| `verified_at` | DateTime? | Verification completion timestamp |
| `verification_level` | Enum? | `basic \| document \| field \| premium` |
| `profile_completeness` | Float | Percentage of required profile fields filled (0.0-1.0) |
| `search_visible` | Boolean | Whether the professional is visible in public search |
| `accepting_new_clients` | Boolean | Whether currently accepting new clients |
| `featured_until` | DateTime? | Featured listing expiration |
| `created_at` | DateTime | Profile creation |
| `updated_at` | DateTime | Last profile update |

### 1.2 Professional Profile Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User | 1:1 | The person who owns this professional profile |
| ProfessionalCategory | N:M | Categories this professional belongs to |
| ServiceCapability | 1:N | Services this professional can perform |
| License | 1:N | Professional licenses held |
| Certification | 1:N | Certifications earned |
| GeographicCoverage | 1:N | Areas where the professional operates |
| Availability | 1:N | Schedule and availability windows |
| Rating | 1:N | Ratings received (from CRM feedback) |
| OrganizationMember | 1:N | Organization memberships |
| ServiceOrder | 1:N | Services ordered through this professional |
| Portfolio | 1:N | Portfolio items (past work evidence) |

---

## 2. Professional Categories

A typed taxonomy of all professional roles supported by the platform. Each professional may belong to one primary and multiple secondary categories.

### 2.1 Category Definitions

| Category Code | Label (FR) | Label (EN) | Domain | Description |
|--------------|------------|------------|--------|-------------|
| `agent_immobilier` | Agent Immobilier | Real Estate Agent | real_estate | Licensed property transaction intermediary |
| `notaire` | Notaire | Notary | legal | Legal officer for property deeds and contracts |
| `geometre` | Géomètre | Surveyor | technical | Land surveying and boundary delineation |
| `architecte` | Architecte | Architect | technical | Building design and construction oversight |
| `ingenieur_civil` | Ingénieur Génie Civil | Civil Engineer | technical | Structural engineering and construction |
| `electricien` | Électricien | Electrician | construction | Electrical installation and repair |
| `plombier` | Plombier | Plumber | construction | Plumbing systems and water supply |
| `macon` | Maçon | Mason | construction | Masonry, brickwork, and concrete structures |
| `menuisier` | Menuisier | Carpenter | construction | Woodwork, framing, and carpentry |
| `peintre` | Peintre | Painter | construction | Interior and exterior painting |
| `carreleur` | Carreleur | Tiler | construction | Tile installation for floors and walls |
| `couvreur` | Couvreur | Roofer | construction | Roofing installation and repair |
| `expert_immobilier` | Expert Immobilier | Real Estate Expert | real_estate | Property valuation and market analysis |
| `evaluateur` | Évaluateur | Appraiser | real_estate | Formal property appraisal |
| `syndic` | Syndic de Copropriété | Condo Manager | real_estate | Condominium association management |
| `videaste_drone` | Vidéaste Drone | Drone Videographer | media | Aerial photography and videography |
| `courtier` | Courtier | Broker | real_estate | Mortgage and insurance brokerage |
| `gardiennage` | Gardiennage/Sécurité | Security Guard | security | Property security and surveillance |
| `prestataire_administratif` | Prestataire Administratif | Admin Service Provider | administrative | Administrative document processing |
| `avocat` | Avocat | Lawyer | legal | Legal representation and advice |
| `comptable` | Comptable | Accountant | financial | Accounting and bookkeeping services |
| `assurance` | Agent d'Assurance | Insurance Agent | financial | Insurance products and policies |
| `banquier` | Banquier | Banker | financial | Banking and financing services |
| `promoteur` | Promoteur Immobilier | Property Developer | real_estate | Real estate development and construction |
| `decorateur` | Décorateur | Interior Decorator | design | Interior design and decoration |
| `jardinier` | Jardinier | Gardener | maintenance | Landscaping and garden maintenance |
| `pisciniste` | Pisciniste | Pool Builder | construction | Swimming pool construction and maintenance |

### 2.2 Category Hierarchy

| Level | Description | Examples |
|-------|-------------|----------|
| **Domain** | Top-level industry domain | `real_estate`, `construction`, `legal`, `technical`, `financial`, `security`, `administrative`, `media`, `design`, `maintenance` |
| **Category** | Professional category | `macon`, `electricien`, `architecte` |
| **Specialty** | Sub-specialty within category | For `macon`: `fondation`, `briquetage`, `crepissage`, `beton_arme` |
| **Skill** | Specific skill or trade | For `electricien`: `installation_residentielle`, `tableau_electrique`, `cablage` |

### 2.3 Category Assignment Rules

| Rule | Description |
|------|-------------|
| One primary category | Each professional must have exactly one primary category |
| Multiple secondary | Professional may have 0-N secondary categories |
| Domain compatibility | Secondary categories should share the same domain or a compatible domain |
| Verification scope | Verification is performed per professional_type, not globally |
| Category-based search | Search filters by primary + secondary categories |
| License requirements | Each category may require specific licenses to practice |

---

## 3. Service Capability Model

Defines the specific services a professional can deliver. A capability is a typed, priced, and schedulable service unit that a professional offers.

### 3.1 Service Capability Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `professional_id` | UUID | Reference to ProfessionalProfile |
| `capability_code` | String | Service capability code (e.g., `ELEC-INSTALL-RES`) |
| `name` | JSON | Multilingual capability name |
| `description` | JSON | Multilingual capability description |
| `category` | Enum | Primary professional category this capability belongs to |
| `service_type` | String | Type of service (from SERVICE_TAXONOMY) |
| `is_active` | Boolean | Whether this capability is currently offered |
| `typical_duration_minutes` | Int? | Estimated duration |
| `requires_verification` | Boolean | Whether verification is required before offering |
| `pricing_model` | Enum | `fixed \| hourly \| per_unit \| estimate \| negotiable` |
| `default_price` | Decimal? | Default price for this capability |
| `price_currency` | String | Currency code (default: `XAF`) |
| `price_unit` | String? | Unit for per_unit pricing (e.g., `m²`, `room`, `hour`) |
| `deposit_required` | Boolean | Whether a deposit is required |
| `deposit_percentage` | Float? | Deposit percentage (0.0-1.0) |
| `is_online_bookable` | Boolean | Whether clients can book online |
| `lead_time_hours` | Int? | Required lead time before service delivery |
| `created_at` | DateTime | Capability creation |

### 3.2 Capability Matching Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `min_project_budget` | Decimal? | Minimum project budget the professional accepts |
| `max_project_budget` | Decimal? | Maximum project budget capacity |
| `preferred_project_size` | Enum | `small \| medium \| large \| enterprise` |
| `languages_spoken` | String[] | ISO language codes |
| `service_radius_km` | Int? | Maximum distance willing to travel |
| `equipment_available` | JSON[]? | Equipment/tools the professional possesses |
| `team_available` | Boolean | Whether the professional can deploy a team |
| `team_size_min` | Int? | Minimum team size |
| `team_size_max` | Int? | Maximum team size |
| `emergency_service` | Boolean | Whether emergency/urgent services are offered |
| `after_hours_service` | Boolean | Whether after-hours services are offered |
| `mobile_service` | Boolean | Whether service is delivered at client location |

### 3.3 Service Capability Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| ProfessionalProfile | N:1 | Owning professional |
| License | N:M | Licenses required for this capability |
| Certification | N:M | Certifications relevant to this capability |
| PricingTier | 1:N | Pricing variations for this capability |
| ServiceOrder | 1:N | Orders fulfilled using this capability |

---

## 4. License and Certification Tracking

Professional credentials tracking separate from the user's identity. Licenses are regulatory permissions; certifications are skill endorsements.

### 4.1 License Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `professional_id` | UUID | Reference to ProfessionalProfile |
| `license_type` | Enum | `professional_card \| trade_license \| RCCM \| business_permit \| municipal_license \| sector_specific` |
| `license_number` | String | Official license registration number |
| `license_name` | String | Name of the license |
| `issuing_authority` | String | Government or regulatory body that issued the license |
| `category` | String? | Professional category this license applies to |
| `issued_at` | DateTime | License issue date |
| `expires_at` | DateTime? | License expiration date |
| `is_renewable` | Boolean | Whether the license can be renewed |
| `renewal_reminder_days` | Int? | Days before expiry to send renewal reminder |
| `status` | Enum | `active \| expired \| suspended \| revoked \| pending_renewal` |
| `verification_status` | Enum | `unverified \| pending \| verified \| rejected` |
| `verified_by` | UUID? | Admin who verified the license |
| `verified_at` | DateTime? | Verification timestamp |
| `document_url` | String? | Uploaded license document |
| `document_type` | String? | Document format (pdf, jpg, png) |
| `rejection_reason` | Text? | Reason if verification was rejected |
| `metadata` | JSON? | Additional license-specific data |
| `created_at` | DateTime | Record creation |

### 4.2 Certification Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `professional_id` | UUID | Reference to ProfessionalProfile |
| `certification_name` | String | Name of the certification |
| `certification_code` | String? | Official certification code |
| `issuing_body` | String | Organization that issued the certification |
| `category` | String? | Professional category this cert applies to |
| `level` | Enum? | `beginner \| intermediate \| advanced \| expert \| master` |
| `skills_covered` | String[] | Skills validated by this certification |
| `obtained_at` | DateTime | Date obtained |
| `expires_at` | DateTime? | Expiration date (if any) |
| `credential_id` | String? | External credential ID from issuing body |
| `verifiable_url` | String? | URL where credential can be verified |
| `status` | Enum | `active \| expired \| revoked` |
| `verification_status` | Enum | `unverified \| pending \| verified \| rejected` |
| `verified_by` | UUID? | Admin who verified the certification |
| `document_url` | String? | Uploaded certificate document |
| `created_at` | DateTime | Record creation |

### 4.3 License and Certification Rules

| Rule | Description |
|------|-------------|
| License required by category | Certain professional categories require specific licenses (e.g., notary, architect) |
| Certification optional | Certifications are endorsements, not requirements (unless market-specific) |
| Auto-reminder | System sends renewal reminders based on `renewal_reminder_days` |
| Verification required for search | Professional must have at least `basic` verification to appear in public search |
| Document retention | License/cert documents stored immutably for audit |
| Expiry action | License expiry → professional automatically unfiltered from search for that category |

---

## 5. Geographic Coverage Model

Defines where a professional operates. A professional may cover multiple geographic zones at different levels of granularity.

### 5.1 Geographic Coverage Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `professional_id` | UUID | Reference to ProfessionalProfile |
| `coverage_type` | Enum | `primary \| secondary \| dispatch` |
| `geographic_unit_id` | String | Reference to GeographicUnit.canonical_id |
| `level` | Enum | Coverage granularity: `city \| neighborhood \| zone \| axis \| region \| department \| municipality` |
| `is_home_base` | Boolean | Whether this is the professional's home base |
| `travel_distance_km` | Int? | Max travel distance from this location |
| `additional_fee` | Decimal? | Additional fee for service outside home base |
| `is_active` | Boolean | Whether coverage is currently active |
| `created_at` | DateTime | Coverage record creation |

### 5.2 Coverage Patterns by Professional Type

| Professional Type | Typical Coverage | Radius | Notes |
|-------------------|-----------------|--------|-------|
| Agent Immobilier | City-wide, zone-specific | 10-30 km | Assigned to specific zones for lead routing |
| Notaire | City-wide | Unlimited | Regional administrative boundaries |
| Géomètre | Department-wide | 50+ km | Administrative jurisdiction |
| Architecte | City-wide | 30-50 km | Project-based |
| Électricien | City + suburbs | 20-30 km | Service radius |
| Plombier | City + suburbs | 15-25 km | Emergency radius smaller |
| Maçon | City + region | 30-50 km | Project-based travel |
| Menuisier | City + suburbs | 20-40 km | Workshop-based, delivery radius |
| Peintre | City + suburbs | 20-30 km | Service radius |
| Carreleur | City + suburbs | 20-30 km | Service radius |
| Couvreur | City + region | 30-50 km | Project-based travel |
| Expert Immobilier | City-wide | 30-50 km | Market-wide |
| Évaluateur | City-wide | 30-50 km | Appraisal radius |
| Syndic | Condominium-specific | N/A | Property-bound |
| Vidéaste Drone | City + region | 50+ km | Project-based |
| Courtier | City-wide | Unlimited | Digital/phone-based |
| Gardiennage | City + suburbs | 20-30 km | Site-based |
| Prestataire Administratif | Digital | Unlimited | Remote service |

### 5.3 Coverage Matching Rules

| Rule | Description |
|------|-------------|
| Coverage intersection | Match demandeur location ↔ professional coverage geographic units |
| Distance filter | Apply `travel_distance_km` constraint |
| Zone-based routing | For agents, use zone assignments from GEOGRAPHY model |
| Multiple coverage | Professional may have primary + secondary coverage zones |
| Coverage priority | Within same geographic unit, professionals with `is_home_base=true` rank higher |

---

## 6. Availability and Scheduling

Manages when a professional is available for work and enables client booking.

### 6.1 Availability Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `professional_id` | UUID | Reference to ProfessionalProfile |
| `day_of_week` | Enum | `monday \| tuesday \| wednesday \| thursday \| friday \| saturday \| sunday` |
| `start_time` | Time | Availability start time |
| `end_time` | Time | Availability end time |
| `timezone` | String | IANA timezone (e.g., `Africa/Douala`) |
| `is_recurring` | Boolean | Whether this is a recurring weekly slot |
| `specific_date` | Date? | For non-recurring availability |
| `slot_duration_minutes` | Int | Booking slot duration (default: 60) |
| `max_bookings_per_slot` | Int | Max concurrent bookings in same slot |
| `is_available` | Boolean | Whether this slot is available |
| `notes` | String? | Internal notes about this availability |
| `created_at` | DateTime | Record creation |

### 6.2 Availability Patterns by Professional Type

| Professional Type | Typical Availability | Booking Model | Lead Time |
|-------------------|---------------------|---------------|-----------|
| Agent Immobilier | Mon-Sat 8h-18h | Slot-based visits | 2-4 hours |
| Notaire | Mon-Fri 8h-17h | Appointment | 24-48 hours |
| Géomètre | Mon-Fri 7h-17h | Project-based | 3-7 days |
| Architecte | Mon-Fri 8h-18h, Sat 9h-13h | Project-based | 1-2 weeks |
| Électricien | Mon-Sat 7h-19h | Emergency + scheduled | 2-24 hours |
| Plombier | Mon-Sat 7h-20h | Emergency + scheduled | 1-4 hours (emergency) |
| Maçon | Mon-Sat 6h-17h | Project-based | 3-14 days |
| Peintre | Mon-Sat 7h-18h | Scheduled | 2-5 days |
| Expert Immobilier | Mon-Fri 8h-18h | Appointment | 24-48 hours |
| Syndic | Mon-Fri 8h-17h | Office hours | 24 hours |

### 6.3 Scheduling Constraints

| Constraint | Description |
|------------|-------------|
| `max_concurrent_projects` | Maximum number of active projects at once |
| `max_concurrent_visits` | Maximum number of visits per day |
| `min_notice_hours` | Minimum advance notice for booking |
| `blackout_dates` | Dates when unavailable (JSON array) |
| `preferred_project_duration` | Preferred project duration range |
| `weekend_available` | Whether weekend work is accepted |
| `holiday_policy` | `standard \| limited \| full` |

---

## 7. Rating System

Rating system for professionals, extending the CRM agent rating mechanism (§9 of CRM_EXTENSION_MODEL.md). Ratings are sourced from post-service feedback and integrated into the professional's public profile.

### 7.1 Professional Rating Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `professional_id` | UUID | Reference to ProfessionalProfile |
| `service_order_id` | UUID? | Reference to completed ServiceOrder |
| `client_user_id` | UUID | Reference to User (client providing rating) |
| `rating` | Int | 1-5 rating |
| `category_ratings` | JSON | Per-category ratings `{quality: Int, punctuality: Int, communication: Int, professionalism: Int, value: Int}` |
| `review_text` | Text? | Free-form review |
| `is_public` | Boolean | Whether review is publicly visible |
| `response_text` | Text? | Professional's response to review |
| `responded_at` | DateTime? | When the professional responded |
| `verified_purchase` | Boolean | Whether this was a verified service order |
| `helpful_count` | Int | Count of users who found this review helpful |
| `reported` | Boolean | Whether review was reported for violation |
| `reported_reason` | String? | Reason for report |
| `status` | Enum | `published \| pending \| hidden \| removed` |
| `created_at` | DateTime | Review creation |

### 7.2 Professional Rating Calculation

```
professional_rating = weighted_average(
    quality_weight * quality_score +
    punctuality_weight * punctuality_score +
    communication_weight * communication_score +
    professionalism_weight * professionalism_score +
    value_weight * value_score
)

Where:
- Standard weights: quality=0.25, punctuality=0.20, communication=0.15, professionalism=0.25, value=0.15
- Recent reviews (last 90 days) weighted 2×
- Verified purchase reviews weighted 1.5×
- Ratings decay: reviews older than 365 days contribute 50% weight
```

### 7.3 Rating Display Rules

| Context | Display |
|---------|---------|
| Profile header | `professional_rating` (1 decimal) + star visualization + total_review_count |
| Search results | Rating badge with count (e.g., "4.3 (127)") |
| Service listing | Rating alongside pricing |
| Booking confirmation | Rating shown during professional selection |
| Public reviews | Top 5 most helpful reviews displayed, sortable by date/rating |

### 7.4 Rating Thresholds and Badges

| Threshold | Badge | Criteria |
|-----------|-------|----------|
| 4.5+ | Top Professional | Min 20 reviews, avg 4.5+ |
| 4.0+ | Recommended | Min 10 reviews, avg 4.0+ |
| 3.5+ | Reliable | Min 5 reviews, avg 3.5+ |
| < 3.5 | Needs Improvement | Below threshold |
| N/A | New | Fewer than 5 reviews |

---

## 8. Verification Workflow

Multi-level verification ensures professional authenticity and capability before appearing in search results.

### 8.1 Verification Levels

| Level | Requirements | Privileges | Review Type |
|-------|-------------|------------|-------------|
| **None** | No verification | Cannot appear in public search | — |
| **Basic** | Phone verified, email verified, identity document submitted | Appears in search, limited visibility | Automated (document scan) |
| **Document** | Basic + license verification, professional documents, business registration (RCCM) | Full search visibility, can receive ServiceOrders | Manual (admin review) |
| **Field** | Document + in-person verification, site visit, reference check | Featured listings, higher matching priority | Field agent + admin review |
| **Premium** | Field + insurance verification, bank guarantee, criminal record check | Top placement, premium badges, enterprise trust | Comprehensive review |

### 8.2 Verification State Machine

```
unverified → pending_documents → documents_received → under_review
    → [approved] → verified
    → [rejected] → rejection_notified → resubmitted → under_review
        → [repeated_rejection] → permanently_blocked
    → [escalated] → manual_review → [approved | rejected]

verified → periodic_review → [approved → remain_verified | 
                              rejected → suspend_verification]
suspend_verification → resubmitted → under_review → ...
```

### 8.3 Verification Entities

#### 8.3.1 VerificationRequest

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `professional_id` | UUID | Professional being verified |
| `requested_level` | Enum | Target verification level |
| `current_level` | Enum | Current level before this request |
| `status` | Enum | `draft \| submitted \| under_review \| approved \| rejected \| escalated` |
| `reviewed_by` | UUID? | Admin reviewer |
| `reviewed_at` | DateTime? | Review decision timestamp |
| `rejection_reason` | Text? | Reason for rejection |
| `admin_notes` | Text? | Internal admin notes |
| `resubmission_count` | Int | Number of resubmissions |
| `submitted_at` | DateTime | Submission timestamp |
| `completed_at` | DateTime? | Decision timestamp |

#### 8.3.2 VerificationDocument

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `verification_request_id` | UUID | Parent verification request |
| `document_type` | Enum | `identity_card \| passport \| driver_license \| professional_card \| RCCM \| business_license \| insurance_cert \| diploma \| reference_letter \| criminal_record \| bank_guarantee \| tax_clearance \| utility_bill` |
| `document_url` | String | Secure document storage URL |
| `document_hash` | String | SHA-256 hash for integrity verification |
| `file_type` | String | MIME type |
| `file_size_bytes` | Int | File size |
| `status` | Enum | `pending \| valid \| invalid \| expired \| suspicious` |
| `validation_notes` | Text? | Document reviewer notes |
| `validated_by` | UUID? | Admin who validated |
| `validated_at` | DateTime? | Validation timestamp |
| `expires_at` | DateTime? | Document expiration date |
| `created_at` | DateTime | Upload timestamp |

### 8.4 Verification Rules

| Rule | Description |
|------|-------------|
| Mandatory for search | Professional must have at least `basic` verification to appear in search |
| Re-verification | Documents expiring trigger re-verification request |
| Grace period | 30-day grace period before verification suspension |
| Automatic rejection | Automated document scan fails → rejected |
| Manual escalation | Complex cases escalated to senior admin |
| Fraud detection | Document hash checking against known fraudulent documents |
| Cross-reference | License number validated against issuing authority database (where available) |

---

## 9. Pricing Models per Professional Type

Each professional category supports specific pricing models that reflect industry practices.

### 9.1 Pricing Model Definitions

| Pricing Model | Code | Description | Typical Categories |
|---------------|------|-------------|-------------------|
| Fixed Price | `fixed` | Single fixed price for defined service | Électricien (install prise), Plombier (déboucher évier), Peintre (peindre pièce) |
| Per Unit | `per_unit` | Price per measurable unit (m², room, hour) | Peintre (m²), Carreleur (m²), Maçon (m³), Agent (commission %) |
| Hourly | `hourly` | Hourly rate | Architecte, Géomètre, Expert Immobilier, Consultant |
| Daily | `daily` | Daily rate | Maçon (équipe), Menuisier |
| Percentage | `percentage` | Percentage of transaction/project value | Agent Immobilier (commission), Courtier |
| Estimate | `estimate` | Custom quote based on site visit | Most construction trades |
| Subscription | `subscription` | Recurring monthly/annual fee | Syndic, Gardiennage, Prestataire Administratif |
| Tiered | `tiered` | Multiple service tiers at different prices | Vidéaste Drone (basic/standard/premium packages) |
| Negotiable | `negotiable` | Open to negotiation | Large construction projects |
| Retainer | `retainer` | Monthly retainer for ongoing service | Avocat, Comptable, Syndic |

### 9.2 Pricing Tier Model

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `capability_id` | UUID | Reference to ServiceCapability |
| `tier_name` | String | Tier label (e.g., "Basic", "Standard", "Premium") |
| `description` | JSON | Tier description |
| `pricing_model` | Enum | Pricing model for this tier |
| `price` | Decimal | Price amount |
| `currency` | String | Currency (default: XAF) |
| `unit` | String? | Unit for per-unit pricing (e.g., `m²`, `heure`, `jour`) |
| `min_quantity` | Float? | Minimum quantity for per-unit pricing |
| `max_quantity` | Float? | Maximum quantity for per-unit pricing |
| `is_promotional` | Boolean | Whether this is a promotional price |
| `promotion_ends_at` | DateTime? | Promotion end date |
| `deposit_required` | Boolean | Whether deposit is required for this tier |
| `deposit_percentage` | Float? | Deposit percentage |
| `includes_materials` | Boolean | Whether materials are included in price |
| `includes_travel` | Boolean | Whether travel costs are included |
| `is_active` | Boolean | Whether this tier is active |

### 9.3 Pricing by Professional Type (Reference Table)

| Professional Type | Primary Model | Typical Range (XAF) | Deposit | Notes |
|-------------------|---------------|--------------------|---------|-------|
| Agent Immobilier | Percentage | 3-8% commission | N/A | Seller-paid or buyer-paid |
| Notaire | Fixed + Percentage | Fixed fee + % of transaction | N/A | Regulated by law |
| Géomètre | Per Unit (m²) | 50-500/m² | 30-50% | Varies by land size |
| Architecte | Percentage | 8-15% of construction cost | 30% | Staged payments |
| Électricien | Fixed + Hourly | 15,000-50,000 + 5,000-10,000/h | 0-30% | Emergency premium |
| Plombier | Fixed + Hourly | 10,000-40,000 + 5,000-10,000/h | 0-30% | Emergency +50% |
| Maçon | Per Unit (m²/m³) | 3,000-8,000/m² | 30-50% | Material cost separate |
| Menuisier | Fixed + Per Unit | 50,000-500,000 | 50% | Material cost separate |
| Peintre | Per Unit (m²) | 800-2,500/m² | 30-50% | Includes prep work |
| Carreleur | Per Unit (m²) | 2,000-5,000/m² | 40% | Material cost separate |
| Couvreur | Per Unit (m²) | 3,000-8,000/m² | 40% | Height premium |
| Expert Immobilier | Fixed + Hourly | 50,000-200,000 | 50% | Report-based |
| Évaluateur | Fixed | 50,000-150,000 | 50% | Per appraisal |
| Syndic | Subscription | 50,000-200,000/mois | N/A | Per building |
| Vidéaste Drone | Tiered | 50,000-300,000 | 50% | Package-based |
| Courtier | Percentage | 1-3% of loan | N/A | Lender-paid |
| Gardiennage | Subscription | 150,000-500,000/mois | N/A | Per site |
| Prestataire Administratif | Fixed + Subscription | 10,000-100,000 | 0-50% | Document-based |
| Avocat | Hourly + Retainer | 50,000-200,000/h | Varies | Case-based |
| Comptable | Subscription | 50,000-200,000/mois | N/A | Monthly retainer |
| Promoteur | Project-based | Negotiable | Varies | Per project |

---

## 10. SLA per Professional Type

Service Level Agreements define expected response and delivery times for each professional category.

### 10.1 SLA Definition Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `professional_type` | Enum | Professional category this SLA applies to |
| `sla_tier` | Enum | `standard \| premium \| enterprise` |
| `response_time_hours` | Int | Max hours to respond to new client inquiry |
| `quote_time_hours` | Int | Max hours to provide a quote |
| `site_visit_time_hours` | Int? | Max hours to schedule site visit |
| `service_start_days` | Int? | Max days to start service after confirmation |
| `completion_buffer_percentage` | Float | Buffer % for estimated completion time |
| `emergency_response_minutes` | Int? | Emergency response time in minutes |
| `communication_channel` | Enum[] | `whatsapp \| telegram \| phone \| email \| dashboard` |
| `reporting_frequency` | Enum? | `daily \| weekly \| biweekly \| monthly \| per_milestone` |
| `penalty_rate` | Decimal? | Penalty per hour/day of SLA breach |
| `escalation_contact` | String? | Escalation contact for SLA breaches |
| `is_active` | Boolean | Whether this SLA is active |
| `created_at` | DateTime | SLA definition creation |

### 10.2 SLA Standards by Professional Type

| Professional Type | Response (Std) | Quote (Std) | Site Visit | Start (Std) | Emergency |
|-------------------|---------------|-------------|------------|-------------|-----------|
| Agent Immobilier | < 1h | < 2h | < 24h | < 48h | N/A |
| Notaire | < 4h | < 24h | < 48h | < 72h | N/A |
| Géomètre | < 4h | < 24h | < 48h | < 7d | N/A |
| Architecte | < 8h | < 48h | < 72h | < 14d | N/A |
| Électricien | < 1h | < 2h | < 4h | < 24h | < 60min |
| Plombier | < 1h | < 2h | < 4h | < 24h | < 45min |
| Maçon | < 4h | < 24h | < 48h | < 7d | N/A |
| Menuisier | < 4h | < 24h | < 48h | < 14d | N/A |
| Peintre | < 2h | < 8h | < 24h | < 3d | N/A |
| Carreleur | < 4h | < 24h | < 48h | < 7d | N/A |
| Couvreur | < 2h | < 8h | < 24h | < 3d | < 4h |
| Expert Immobilier | < 4h | < 24h | < 48h | < 7d | N/A |
| Évaluateur | < 4h | < 24h | < 48h | < 7d | N/A |
| Syndic | < 2h | < 8h | < 72h | < 7d | N/A |
| Vidéaste Drone | < 4h | < 24h | < 48h | < 7d | N/A |
| Courtier | < 2h | < 8h | N/A (digital) | < 48h | N/A |
| Gardiennage | < 2h | < 24h | < 48h | < 7d | N/A |
| Prestataire Admin | < 1h | < 4h | N/A (digital) | < 24h | N/A |
| Avocat | < 4h | < 24h | < 48h | < 7d | N/A |
| Comptable | < 4h | < 24h | N/A | < 7d | N/A |

### 10.3 SLA Breach Handling

| Breach Type | Standard Tier | Premium Tier | Enterprise Tier |
|-------------|---------------|--------------|-----------------|
| Response SLA breach | Client notification + $5 penalty credit | Client notification + $10 penalty credit | Escalation to account manager |
| Quote SLA breach | Client notification + auto-waive booking fee | Direct manager contact | Account manager escalation |
| Service start delay | Notification + 5% discount | Notification + 10% discount | Escalation + SLA review |
| Emergency no-show | Client compensation + mandatory review | Compensation + suspension | Escalation + potential termination |

---

## 11. Organization Membership Hierarchy

Professionals may belong to organizations (agencies, firms, enterprises) with role-based hierarchies.

### 11.1 Organization Membership for Professionals

Extends the OrganizationMember model from LAWIM_UNIFIED_DOMAIN_MODEL §12:

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `organization_id` | UUID | Reference to Organization |
| `professional_id` | UUID | Reference to ProfessionalProfile |
| `role` | Enum | `owner \| partner \| manager \| senior \| member \| intern \| subcontractor` |
| `join_date` | DateTime | Membership start date |
| `is_active` | Boolean | Whether membership is active |
| `commission_rate` | Float? | Commission rate for this member (0.0-1.0) |
| `revenue_share` | Float? | Revenue share percentage |
| `reporting_to` | UUID? | References another OrganizationMember (manager) |
| `permissions` | JSON[] | Additional role-based permissions |
| `created_at` | DateTime | Membership creation |

### 11.2 Hierarchy Levels

| Level | Role | Description | Can Manage |
|-------|------|-------------|------------|
| 1 | `owner` | Organization owner / founder | All levels |
| 2 | `partner` | Co-owner or equity partner | Manager, Senior, Member, Intern, Subcontractor |
| 3 | `manager` | Department or team manager | Senior, Member, Intern, Subcontractor |
| 4 | `senior` | Senior professional | Member, Intern |
| 5 | `member` | Standard team member | None (self only) |
| 6 | `intern` | Trainee / probationary | None |
| 7 | `subcontractor` | External contractor | None |

### 11.3 Organization Types for Professionals

| Organization Type | Description | Typical Members |
|-------------------|-------------|-----------------|
| `agency` | Real estate agency | Agents, managers |
| `firm` | Professional firm (architect, notary, law) | Partners, associates |
| `enterprise` | Construction/Service company | Multiple trade teams |
| `cooperative` | Professional cooperative | Member professionals |
| `sole_proprietorship` | Individual practitioner | Owner only |
| `freelance` | Independent professional | Self |

### 11.4 Team-Based Service Delivery

| Attribute | Type | Description |
|-----------|------|-------------|
| `team_id` | UUID | Team identifier |
| `team_name` | String | Team name |
| `team_lead` | UUID | Reference to OrganizationMember (team lead) |
| `members` | UUID[] | Team member references |
| `specialization` | String? | Team specialization |
| `max_project_size` | Enum | `small \| medium \| large` |
| `availability_status` | Enum | `available \| partial \| fully_booked` |

---

## 12. Complete Extension Mapping Table

### 12.1 Professional Extensions

| Extension ID | Source Concept | Target Entity | Proposed Structure | Priority | Human Decision |
|-------------|---------------|---------------|-------------------|----------|----------------|
| EXT-PRO-001 | Professional Profile (full entity with capabilities) | ProfessionalProfile | ProfessionalProfile entity with user_id, professional_type, verification, bio, years_experience, employee_count, business info, search visibility flags | P1 | Y — field definitions |
| EXT-PRO-002 | Professional categories (27 categories) | ProfessionalCategory | Typed category taxonomy with domain hierarchy, primary/secondary assignment, category-specific licensing requirements, 27 categories from agent to pisciniste | P1 | Y — category list |
| EXT-PRO-003 | Service capability model | ServiceCapability | Typed, priced, schedulable service unit; capability_code, pricing_model, default_price, deposit, booking flags, language/equipment/team attributes | P1 | Y — pricing model per type |
| EXT-PRO-004 | License tracking | License | License entity with type, number, issuing_authority, expiry, status, verification workflow; category-specific license requirements | P1 | N |
| EXT-PRO-005 | Certification tracking | Certification | Certification entity with name, issuing_body, level, skills_covered, expiry, verification; optional skill endorsements | P2 | N |
| EXT-PRO-006 | Geographic coverage model | GeographicCoverage | Coverage entity with type, geographic_unit_id, level, travel_distance, additional_fee; coverage patterns by professional type | P1 | Y — coverage radius |
| EXT-PRO-007 | Availability and scheduling | Availability | Availability entity with day_of_week, time window, recurring/specific, slot_duration, max_bookings, booking constraints | P2 | Y — slot configuration |
| EXT-PRO-008 | Professional rating system | ProfessionalRating | Rating entity with per-category scoring (quality, punctuality, communication, professionalism, value), weighted calculation, verified purchase, badge system | P2 | Y — rating weights |
| EXT-PRO-009 | Verification workflow (4 levels) | VerificationRequest + VerificationDocument | Multi-level verification (basic/doc/field/premium), state machine, document upload with hash verification, admin review, re-verification cycle | P2 | Y — verification levels |
| EXT-PRO-010 | Pricing models per type | PricingTier | 10 pricing models (fixed, per_unit, hourly, daily, percentage, estimate, subscription, tiered, negotiable, retainer); pricing references per category | P1 | Y — pricing defaults |
| EXT-PRO-011 | SLA per professional type | SLAProfessionnel | SLA definition per professional_type + tier; response/quote/visit/start/emergency SLAs, breach handling, penalty model | P2 | Y — SLA thresholds |
| EXT-PRO-012 | Organization membership hierarchy | OrganizationMember (extended) | Professional organization hierarchy with owner/partner/manager/senior/member/intern/subcontractor roles, commission, reporting line, team-based delivery | P2 | Y — hierarchy levels |

### 12.2 All Professional Fields Extension Table

| Field | Entity | Type | Extension Source | Description |
|-------|--------|------|------------------|-------------|
| `professional_type` | ProfessionalProfile | Enum | EXT-PRO-001 | Primary professional category |
| `secondary_types` | ProfessionalProfile | Enum[] | EXT-PRO-001 | Additional categories |
| `professional_name` | ProfessionalProfile | String | EXT-PRO-001 | Business name |
| `professional_email` | ProfessionalProfile | String? | EXT-PRO-001 | Professional contact email |
| `professional_phone` | ProfessionalProfile | String? | EXT-PRO-001 | Professional contact phone |
| `business_address` | ProfessionalProfile | String? | EXT-PRO-001 | Registered business address |
| `years_experience` | ProfessionalProfile | Int | EXT-PRO-001 | Years of experience |
| `employee_count` | ProfessionalProfile | Int? | EXT-PRO-001 | Number of employees |
| `professional_status` | ProfessionalProfile | Enum | EXT-PRO-001 | active/inactive/suspended/archived |
| `is_verified` | ProfessionalProfile | Boolean | EXT-PRO-009 | Verification flag |
| `verification_level` | ProfessionalProfile | Enum? | EXT-PRO-009 | basic/document/field/premium |
| `profile_completeness` | ProfessionalProfile | Float | EXT-PRO-001 | 0.0-1.0 completeness |
| `search_visible` | ProfessionalProfile | Boolean | EXT-PRO-001 | Public search visibility |
| `accepting_new_clients` | ProfessionalProfile | Boolean | EXT-PRO-001 | Client acceptance flag |
| `capability_code` | ServiceCapability | String | EXT-PRO-003 | Unique capability identifier |
| `pricing_model` | ServiceCapability | Enum | EXT-PRO-010 | fixed/hourly/per_unit/estimate/etc |
| `default_price` | ServiceCapability | Decimal? | EXT-PRO-010 | Default price for capability |
| `deposit_required` | ServiceCapability | Boolean | EXT-PRO-010 | Deposit requirement |
| `license_number` | License | String | EXT-PRO-004 | Official license number |
| `issuing_authority` | License | String | EXT-PRO-004 | Regulatory body |
| `license_status` | License | Enum | EXT-PRO-004 | active/expired/suspended/revoked |
| `license_verification_status` | License | Enum | EXT-PRO-004 | unverified/pending/verified/rejected |
| `certification_name` | Certification | String | EXT-PRO-005 | Certification title |
| `issuing_body` | Certification | String | EXT-PRO-005 | Certifying organization |
| `certification_level` | Certification | Enum? | EXT-PRO-005 | beginner/intermediate/advanced/expert/master |
| `coverage_type` | GeographicCoverage | Enum | EXT-PRO-006 | primary/secondary/dispatch |
| `geographic_unit_id` | GeographicCoverage | String | EXT-PRO-006 | Covered geographic unit |
| `travel_distance_km` | GeographicCoverage | Int? | EXT-PRO-006 | Max travel distance |
| `day_of_week` | Availability | Enum | EXT-PRO-007 | monday-sunday |
| `start_time` | Availability | Time | EXT-PRO-007 | Availability start |
| `end_time` | Availability | Time | EXT-PRO-007 | Availability end |
| `slot_duration_minutes` | Availability | Int | EXT-PRO-007 | Booking slot duration |
| `professional_rating` | ProfessionalProfile | Float | EXT-PRO-008 | Computed rating 1.0-5.0 |
| `total_reviews` | ProfessionalProfile | Int | EXT-PRO-008 | Count of published reviews |
| `rating_badge` | ProfessionalProfile | String? | EXT-PRO-008 | Top Professional/Recommended/Reliable/New |
| `verification_request_status` | VerificationRequest | Enum | EXT-PRO-009 | draft/submitted/under_review/approved/rejected |
| `document_type` | VerificationDocument | Enum | EXT-PRO-009 | Document category |
| `document_hash` | VerificationDocument | String | EXT-PRO-009 | SHA-256 integrity hash |
| `tier_name` | PricingTier | String | EXT-PRO-010 | Basic/Standard/Premium |
| `price` | PricingTier | Decimal | EXT-PRO-010 | Tier price |
| `currency` | PricingTier | String | EXT-PRO-010 | Currency code |
| `sla_tier` | SLAProfessionnel | Enum | EXT-PRO-011 | standard/premium/enterprise |
| `response_time_hours` | SLAProfessionnel | Int | EXT-PRO-011 | Max response time |
| `organization_role` | OrganizationMember | Enum | EXT-PRO-012 | owner/partner/manager/senior/member/intern/subcontractor |
| `commission_rate` | OrganizationMember | Float? | EXT-PRO-012 | Commission percentage |
| `reporting_to` | OrganizationMember | UUID? | EXT-PRO-012 | Manager reference |

### 12.3 New Entities

| Entity | Description | Extensions |
|--------|-------------|------------|
| `ProfessionalProfile` | Central professional entity; transforms User into full service provider with capabilities, credentials, and availability | EXT-PRO-001, EXT-PRO-002, EXT-PRO-008, EXT-PRO-009 |
| `ServiceCapability` | Typed, priced, schedulable service unit that a professional offers | EXT-PRO-003, EXT-PRO-010 |
| `License` | Regulatory professional license with verification workflow | EXT-PRO-004 |
| `Certification` | Optional skill endorsement and credential | EXT-PRO-005 |
| `GeographicCoverage` | Geographic areas where professional operates | EXT-PRO-006 |
| `Availability` | Schedule and booking slot configuration | EXT-PRO-007 |
| `ProfessionalRating` | Per-service rating with multi-category scoring | EXT-PRO-008 |
| `VerificationRequest` | Multi-level verification workflow request | EXT-PRO-009 |
| `VerificationDocument` | Document submitted as part of verification | EXT-PRO-009 |
| `PricingTier` | Pricing variation for a service capability | EXT-PRO-010 |
| `SLAProfessionnel` | Service Level Agreement definition per professional type | EXT-PRO-011 |

---

*End of PROFESSIONAL_EXTENSION_MODEL.md — 12 sections, 12 professional extensions, 27 professional categories, 10 pricing models, 4 verification levels, 11 new entities defined.*
