# FINANCING EXTENSION MODEL

**Document ID:** LAWIM-H13-FINANCING-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §6 (Dossier/Project Model), §7 (Matching Engine), §3 (Service Model)
**Source Crosswalks:** required_extensions.json (financing), QUALIFICATION_EXTENSION_MODEL.md §10.5 (Financing Matrices), CRM_EXTENSION_MODEL.md (Lead Scoring)

---

## Table of Contents

1. [Conceptual Architecture](#1-conceptual-architecture)
2. [Financing Request Entity](#2-financing-request-entity)
3. [Financing Product Catalog](#3-financing-product-catalog)
4. [Financing Provider Model](#4-financing-provider-model)
5. [Eligibility Rules Engine](#5-eligibility-rules-engine)
6. [Applicant Financial Profile](#6-applicant-financial-profile)
7. [Guarantee and Contribution Tracking](#7-guarantee-and-contribution-tracking)
8. [Repayment Capacity Calculation](#8-repayment-capacity-calculation)
9. [Document Requirements per Financing Type](#9-document-requirements-per-financing-type)
10. [Financing Match (Demandeur ↔ Product)](#10-financing-match-demarcheur--product)
11. [Financing Decision Tracking](#11-financing-decision-tracking)
12. [Complete Extension Mapping Table](#12-complete-extension-mapping-table)

---

## 1. Conceptual Architecture

LAWIM does **not** replace the financier — it facilitates the match between financing demandeurs and financing products. The platform acts as an intelligent intermediary: collecting applicant profiles, matching against product eligibility rules, preparing application dossiers, and tracking decisions.

### 1.1 Design Principles

| Principle | Description |
|-----------|-------------|
| **Facilitation, not origination** | LAWIM matches demandeurs to appropriate financing products but does not underwrite, approve, or disburse funds. All financing decisions remain with the provider. |
| **Multi-provider catalog** | Financing products from multiple banks, microfinance institutions, and other lenders are listed in a searchable, comparable catalog. |
| **Eligibility-first matching** | Matching prioritizes eligibility rules before scoring. A demandeur is only matched to products for which they meet hard eligibility constraints. |
| **Document-ready dossier** | The platform prepares a complete application dossier with all required documents, ready for provider submission. |
| **Decision transparency** | Every decision (approval, rejection, conditional approval) is tracked with reason codes and feedback for the demandeur. |
| **Commission model** | LAWIM earns referral/matching fees from providers upon successful funding, not from demandeurs. |

### 1.2 Entity Relationship Map

```
FinancingRequest (demandeur's application)
  ├── references Applicant (User)
  ├── references Project (property/project being financed)
  ├── has an ApplicantFinancialProfile (income, expenses, assets, liabilities)
  ├── has N Guarantee (collateral, personal guarantees)
  ├── has N Contribution (down payment, co-investment)
  ├── triggers N FinancingMatch attempts
  │     └── each match links 1 FinancingProduct
  │           └── product belongs to 1 FinancingProvider
  │                 └── provider has N EligibilityRule
  │                       └── rules reference DocumentRequirement
  └── results in 1 FinancingDecision per match attempt
        └── decision may trigger re-match or escalation
```

---

## 2. Financing Request Entity

A financing request is the demandeur's application for financing. It captures the demand, the purpose, the amount, and the context of the financing need.

### 2.1 Core Financing Request Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `user_id` | UUID | Reference to demandeur (User) |
| `project_id` | UUID? | Reference to Project being financed |
| `financing_type` | Enum | Type of financing needed: `mortgage_buy \| mortgage_construction \| mortgage_renovation \| personal_loan \| lease \| investment_financing \| construction_loan \| bridge_loan \| top_up_loan \| social_housing \| business_loan \| microfinance_loan` |
| `purpose_description` | Text | Free-text description of financing purpose |
| `requested_amount` | Decimal | Amount of financing requested |
| `currency` | String | Currency code (default: `XAF`) |
| `preferred_term_months` | Int? | Preferred repayment term in months |
| `preferred_interest_rate` | Decimal? | Preferred interest rate (percentage) |
| `monthly_payment_capacity` | Decimal? | Self-declared monthly payment capacity |
| `has_existing_loans` | Boolean | Whether applicant has existing loans |
| `existing_loan_total` | Decimal? | Total outstanding loan amount |
| `urgency` | Enum | `low \| medium \| high \| urgent` |
| `status` | Enum | `draft \| submitted \| matching \| matched \| documents_pending \| documents_submitted \| under_review \| approved \| rejected \| withdrawn \| funded \| closed` |
| `readiness_score` | Float? | Profile completeness / readiness score (0.0-1.0) |
| `submitted_at` | DateTime? | When the request was submitted |
| `matched_at` | DateTime? | When a match was found |
| `funded_at` | DateTime? | When financing was disbursed |
| `closed_at` | DateTime? | Request closure |
| `created_at` | DateTime | Request creation |

### 2.2 Financing Request Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| User (demandeur) | N:1 | Applicant who needs financing |
| Project | 0:1 | Property or project being financed |
| ApplicantFinancialProfile | 1:1 | Financial profile of the applicant |
| Guarantee | 1:N | Collateral and guarantees offered |
| Contribution | 1:N | Down payment and co-investment contributions |
| FinancingMatch | 1:N | Match attempts against products |
| FinancingDecision | 1:N | Decisions received from providers |
| DocumentRequirement | N:M | Required documents for this financing type |

---

## 3. Financing Product Catalog

A searchable catalog of financing products offered by registered providers. Each product is a loan type with specific terms, rates, and eligibility criteria.

### 3.1 Financing Product Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `provider_id` | UUID | Reference to FinancingProvider |
| `product_code` | String | Unique product code (e.g., `BICEC-MTG-STD-001`) |
| `product_name` | JSON | Multilingual product name |
| `description` | JSON | Multilingual product description |
| `financing_type` | Enum | Product type (matches financing request type) |
| `is_active` | Boolean | Whether the product is currently available |
| `min_amount` | Decimal | Minimum loan amount |
| `max_amount` | Decimal | Maximum loan amount |
| `currency` | String | Currency code |
| `min_term_months` | Int | Minimum repayment term |
| `max_term_months` | Int | Maximum repayment term |
| `interest_rate_type` | Enum | `fixed \| variable \| mixed \| tiered` |
| `interest_rate_min` | Decimal | Minimum interest rate (APR) |
| `interest_rate_max` | Decimal | Maximum interest rate (APR) |
| `effective_apr` | Decimal? | Effective annual percentage rate (illustrative) |
| `processing_fee_percentage` | Decimal? | Processing fee (percentage of loan) |
| `processing_fee_fixed` | Decimal? | Fixed processing fee |
| `insurance_required` | Boolean | Whether loan insurance is mandatory |
| `insurance_rate` | Decimal? | Insurance rate (percentage of loan) |
| `collateral_required` | Boolean | Whether collateral is required |
| `collateral_type` | Enum[]? | Accepted collateral types |
| `guarantor_required` | Boolean | Whether a guarantor is required |
| `min_guarantors` | Int? | Minimum number of guarantors |
| `max_funding_time_days` | Int | Maximum days to funding after approval |
| `prepayment_allowed` | Boolean | Whether early repayment is allowed |
| `prepayment_fee` | Decimal? | Prepayment penalty percentage |
| `target_market` | Enum[] | Target applicant segments: `individual \| professional \| enterprise \| diaspora \| civil_servant \| student` |
| `geographic_availability` | String[] | Geographic units where the product is available |
| `featured` | Boolean | Whether product is featured/promoted |
| `featured_until` | DateTime? | Featured promotion end |
| `created_at` | DateTime | Product creation |
| `updated_at` | DateTime | Last product update |

### 3.2 Loan Types Catalog

| Financing Type | Code | Description | Typical Term | Typical Rate (XAF) |
|---------------|------|-------------|-------------|-------------------|
| Mortgage Buy | `mortgage_buy` | Standard mortgage for property purchase | 60-240 months | 6-12% |
| Mortgage Construction | `mortgage_construction` | Financing for property construction | 60-240 months | 7-13% |
| Mortgage Renovation | `mortgage_renovation` | Financing for renovation/improvement | 36-120 months | 8-14% |
| Personal Loan | `personal_loan` | Unsecured personal loan for real estate | 12-60 months | 10-20% |
| Lease Financing | `lease` | Leasing/credit-bail for equipment or property | 24-84 months | 8-15% |
| Investment Financing | `investment_financing` | Financing for investment properties | 60-240 months | 7-12% |
| Construction Loan | `construction_loan` | Phased construction financing | 12-36 months | 8-14% |
| Bridge Loan | `bridge_loan` | Short-term bridge financing | 3-12 months | 12-18% |
| Top-Up Loan | `top_up_loan` | Additional loan on existing property | 12-60 months | 9-15% |
| Social Housing | `social_housing` | Subsidized financing for social housing | 120-240 months | 4-8% |
| Business Loan | `business_loan` | Commercial real estate financing | 36-120 months | 8-16% |
| Microfinance Loan | `microfinance_loan` | Small-scale microfinance for housing | 6-36 months | 15-30% |

### 3.3 Product Matching Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `min_income_monthly` | Decimal? | Minimum monthly income requirement |
| `max_debt_to_income_ratio` | Decimal? | Maximum debt-to-income ratio (0.0-1.0) |
| `min_contribution_percentage` | Decimal? | Minimum down payment as percentage |
| `max_loan_to_value_ratio` | Decimal? | Maximum loan-to-value ratio (0.0-1.0) |
| `min_age` | Int? | Minimum applicant age |
| `max_age` | Int? | Maximum applicant age at maturity |
| `employment_type_accepted` | Enum[]? | Accepted employment types |
| `min_years_in_business` | Int? | Minimum years in business (self-employed) |
| `nationality_required` | String[]? | Required nationality(ies) |
| `residency_required` | Boolean | Whether local residency is required |
| `min_credit_score` | Int? | Minimum credit score requirement |

---

## 4. Financing Provider Model

Models the financial institutions and lenders that offer financing products on the platform.

### 4.1 Financing Provider Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `provider_type` | Enum | `bank \| microfinance \| credit_union \| insurance_company \| government_agency \| fintech \| private_lender \| cooperative` |
| `provider_name` | String | Legal name of the financial institution |
| `provider_code` | String | Short code (e.g., `BICEC`, `AFRILAND`, `MC2`) |
| `registration_number` | String? | Regulatory registration number |
| `license_number` | String? | Banking/microfinance license |
| `regulatory_body` | String? | Supervisory authority (e.g., `COBAC`, `BEAC`) |
| `country` | String | Country of operations |
| `headquarters_address` | String? | Main office address |
| `contact_phone` | String? | Provider contact phone |
| `contact_email` | String? | Provider contact email |
| `website` | String? | Provider website |
| `logo_url` | String? | Provider logo |
| `description` | Text? | Provider description |
| `years_in_operation` | Int? | Years since founding |
| `total_branches` | Int? | Number of branches |
| `coverage_cities` | String[] | Cities where provider operates |
| `is_verified` | Boolean | Whether the provider is verified by LAWIM |
| `verification_status` | Enum | `unverified \| pending \| verified \| suspended` |
| `commission_model` | Enum | `fixed_per_loan \| percentage_of_loan \| success_fee \| subscription` |
| `commission_rate` | Decimal? | Commission rate/amount |
| `integration_type` | Enum | `api \| manual_email \| manual_portal \| paper_based` |
| `integration_status` | Enum | `not_connected \| active \| degraded \| disconnected` |
| `api_endpoint` | String? | API endpoint URL (if applicable) |
| `api_key_last_rotated` | DateTime? | Last API key rotation |
| `contact_person_name` | String? | Relationship manager name |
| `contact_person_email` | String? | Relationship manager email |
| `contact_person_phone` | String? | Relationship manager phone |
| `sla_response_days` | Int? | Standard response time in days |
| `max_concurrent_applications` | Int? | Maximum concurrent applications from platform |
| `monthly_application_limit` | Int? | Monthly application cap |
| `is_active` | Boolean | Whether the provider is active on the platform |
| `activated_at` | DateTime? | When the provider was activated |
| `created_at` | DateTime | Provider registration |

### 4.2 Provider Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| FinancingProduct | 1:N | Products offered by this provider |
| EligibilityRule | 1:N | Provider-level eligibility rules |
| FinancingDecision | 1:N | Decisions made by this provider |
| User (contact) | 1:N | Provider staff contacts |

### 4.3 Provider Types

| Type | Code | Description | Typical Products |
|------|------|-------------|------------------|
| Bank | `bank` | Commercial bank regulated by central bank | Mortgages, construction loans, personal loans |
| Microfinance | `microfinance` | Microfinance institution (MFI/EMF) | Micro-loans, small mortgages, group lending |
| Credit Union | `credit_union` | Member-owned cooperative credit union | Member loans, housing loans |
| Insurance Company | `insurance_company` | Insurance company offering investment/loan products | Policy-backed loans |
| Government Agency | `government_agency` | Government housing finance agency | Social housing loans, subsidies |
| Fintech | `fintech` | Digital lending platform | Fast online loans, bridge financing |
| Private Lender | `private_lender` | Private individual or company | Bridge loans, short-term financing |
| Cooperative | `cooperative` | Cooperative society | Member housing loans |

---

## 5. Eligibility Rules Engine

The eligibility rules engine evaluates whether an applicant qualifies for a financing product based on hard constraints. Rules are defined per product and evaluated before matching.

### 5.1 Eligibility Rule Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `product_id` | UUID? | Reference to FinancingProduct (product-level rule) |
| `provider_id` | UUID? | Reference to FinancingProvider (provider-level rule) |
| `rule_code` | String | Unique rule code (e.g., `MIN_INCOME_500K`, `MAX_DTI_40`) |
| `rule_name` | String | Human-readable rule name |
| `rule_type` | Enum | `income \| employment \| age \| residency \| nationality \| credit_score \| dti_ratio \| ltv_ratio \| contribution \| collateral \| guarantor \| business_age \| documentation \| geographic` |
| `operator` | Enum | `greater_than \| greater_than_or_equal \| less_than \| less_than_or_equal \| equal \| not_equal \| in \| not_in \| between \| contains \| matches_all \| matches_any \| custom_function` |
| `value` | JSON | Rule threshold value(s) |
| `unit` | String? | Unit of measurement (e.g., `XAF`, `years`, `percentage`, `ratio`) |
| `error_message` | JSON | Multilingual error message when rule fails |
| `severity` | Enum | `hard_block \| soft_warning \| info` |
| `priority` | Int | Rule evaluation priority (lower = evaluated first) |
| `is_active` | Boolean | Whether the rule is active |
| `effective_from` | DateTime | Rule effective date |
| `effective_until` | DateTime? | Rule expiration date |
| `created_at` | DateTime | Rule creation |

### 5.2 Eligibility Rule Categories

| Category | Code | Example Rules | Severity |
|----------|------|---------------|----------|
| Income | `income` | Min monthly income ≥ 500,000 XAF; Min household income ≥ 750,000 XAF | hard_block |
| Employment | `employment` | Employment type in {civil_servant, private_sector, self_employed}; Min years in business ≥ 2 | hard_block |
| Age | `age` | Age ≥ 21; Age at maturity ≤ 65; Age at maturity ≤ 70 | hard_block |
| Residency | `residency` | Resident of country = true; Residency permit valid | hard_block |
| Nationality | `nationality` | Nationality in {CM, FR, ...} (product-specific) | hard_block |
| Credit Score | `credit_score` | Min credit score ≥ 600; No history of default | hard_block |
| DTI Ratio | `dti_ratio` | Debt-to-income ratio ≤ 40%; Total monthly payments / income ≤ 0.45 | hard_block |
| LTV Ratio | `ltv_ratio` | Loan-to-value ≤ 80%; For construction: LTV ≤ 70% | hard_block |
| Contribution | `contribution` | Down payment ≥ 20% of property value; Own contribution ≥ 15% | hard_block |
| Collateral | `collateral` | Collateral type in {land_deed, property_title, bank_guarantee}; Collateral value ≥ loan amount × 1.5 | hard_block |
| Guarantor | `guarantor` | Guarantor required = true; Min 1 guarantor with income ≥ 300,000 XAF | soft_warning |
| Business Age | `business_age` | Business operating ≥ 2 years; Business registered (RCCM) | hard_block |
| Geographic | `geographic` | Property city in eligible cities list; Property located in covered region | hard_block |

### 5.3 Eligibility Evaluation Flow

```
FinancingRequest submitted
  │
  ▼
1. Identify candidate products (financing_type match + is_active)
  │
  ▼
2. Filter by geographic availability
  │
  ▼
3. Filter by target market (individual/professional/enterprise)
  │
  ▼
4. Evaluate hard_block rules:
   for each rule with severity=hard_block:
       evaluate rule against applicant profile
       → FAIL → product excluded from matching
       → PASS → continue to next rule
  │
  ▼
5. Evaluate soft_warning rules:
   for each rule with severity=soft_warning:
       evaluate rule against applicant profile
       → FAIL → flagged as warning (product still eligible)
       → PASS → continue
  │
  ▼
6. Scoring and ranking of eligible products
  │
  ▼
7. Present top N matches to demandeur
```

---

## 6. Applicant Financial Profile

A comprehensive financial profile of the applicant, built from self-declared data and optionally verified documents.

### 6.1 Applicant Financial Profile Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `financing_request_id` | UUID | Reference to FinancingRequest |
| `employment_status` | Enum | `civil_servant \| private_sector_employee \| self_employed \| business_owner \| freelancer \| retiree \| student \| unemployed \| homemaker` |
| `employer_name` | String? | Current employer name |
| `employer_sector` | Enum? | `public \| private \| ngos \| international \| informal` |
| `job_title` | String? | Current job title |
| `years_at_current_job` | Decimal? | Years at current employment |
| `monthly_income` | Decimal | Total monthly income (all sources) |
| `income_currency` | String | Currency (default XAF) |
| `income_sources` | JSON[] | Income breakdown `{source, amount, is_verified}` |
| `additional_income` | Decimal? | Additional income (bonuses, commissions, rental) |
| `additional_income_description` | String? | Description of additional income |
| `monthly_expenses` | Decimal | Total monthly expenses |
| `expense_breakdown` | JSON? | Expenses breakdown `{housing, transportation, food, education, utilities, other}` |
| `existing_loan_payments` | Decimal? | Total monthly loan payments |
| `total_assets` | Decimal? | Total estimated assets |
| `asset_breakdown` | JSON? | Assets `{real_estate, vehicles, savings, investments, other}` |
| `total_liabilities` | Decimal? | Total liabilities |
| `liability_breakdown` | JSON? | Liabilities `{loans, credit_cards, other_debts}` |
| `has_bank_account` | Boolean | Whether applicant has a bank account |
| `bank_name` | String? | Primary bank name |
| `account_type` | Enum? | `checking \| savings \| both` |
| `years_banking` | Decimal? | Years with primary bank |
| `has_credit_history` | Boolean | Whether applicant has credit history |
| `credit_score` | Int? | Credit score (if available) |
| `credit_score_source` | String? | Source of credit score |
| `has_mobile_money` | Boolean | Whether applicant uses mobile money |
| `mobile_money_provider` | String? | Mobile money provider (MTN, Orange, etc.) |
| `is_verified` | Boolean | Whether financial data has been verified |
| `verification_method` | Enum? | `self_declared \| payslip \| bank_statement \| tax_return \| employer_letter \| account_aggregator` |
| `verified_at` | DateTime? | Verification timestamp |
| `verified_by` | UUID? | Admin who verified |
| `created_at` | DateTime | Profile creation |
| `updated_at` | DateTime | Last update |

### 6.2 Financial Profile Verification

| Verification Method | Description | Trust Level |
|--------------------|-------------|-------------|
| `self_declared` | Applicant declares without proof | Low |
| `payslip` | Last 3 months payslips uploaded | Medium |
| `bank_statement` | Last 6 months bank statements uploaded | Medium-High |
| `tax_return` | Last tax return filed | High |
| `employer_letter` | Employer confirmation letter | Medium |
| `account_aggregator` | API-based account aggregation | High |

---

## 7. Guarantee and Contribution Tracking

Tracks collateral offered and own contributions (down payment) committed by the applicant.

### 7.1 Guarantee Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `financing_request_id` | UUID | Reference to FinancingRequest |
| `guarantee_type` | Enum | `property_mortgage \| land_deed \| bank_guarantee \| personal_guarantee \| corporate_guarantee \| life_insurance \| savings_account_lien \| securities_collateral \| vehicle_title \| equipment_lien \| guarantee_fund` |
| `description` | Text | Description of the guarantee |
| `estimated_value` | Decimal | Estimated value of the guarantee |
| `value_currency` | String | Currency |
| `valuation_method` | Enum? | `appraisal \| market_estimate \| tax_value \| self_declared` |
| `appraisal_document_url` | String? | Appraisal/valuation document |
| `owner_name` | String | Name of the guarantee owner |
| `owner_relationship` | Enum? | `self \| spouse \| parent \| sibling \| business_partner \| third_party` |
| `is_encumbered` | Boolean | Whether the guarantee is already pledged elsewhere |
| `existing_charges` | Decimal? | Amount already secured against this guarantee |
| `net_equity` | Decimal? | Estimated value - existing charges |
| `status` | Enum | `offered \| verified \| accepted \| rejected \| released` |
| `verification_status` | Enum | `unverified \| pending \| verified \| rejected` |
| `verified_by` | UUID? | Admin who verified |
| `verified_at` | DateTime? | Verification timestamp |
| `document_url` | String? | Supporting document |
| `notes` | Text? | Additional notes |
| `created_at` | DateTime | Record creation |

### 7.2 Contribution Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `financing_request_id` | UUID | Reference to FinancingRequest |
| `contribution_type` | Enum | `cash_down_payment \| existing_property_equity \| land_contribution \| material_contribution \| labor_contribution \| government_subsidy \| employer_assistance \| family_contribution \| cooperative_contribution` |
| `description` | Text | Description of the contribution |
| `amount` | Decimal | Cash equivalent value of contribution |
| `currency` | String | Currency |
| `percentage_of_total` | Float? | Percentage of total project cost (0.0-1.0) |
| `source_description` | Text? | Source of funds description |
| `source_verification` | Enum? | `unverified \| bank_statement \| sale_agreement \| gift_letter \| subsidy_letter \| payroll_deduction` |
| `availability_date` | DateTime? | When the contribution will be available |
| `is_committed` | Boolean | Whether the contribution is firmly committed |
| `commitment_proof_url` | String? | Proof of commitment document |
| `status` | Enum | `planned \| committed \| verified \| received \| refunded` |
| `created_at` | DateTime | Record creation |

### 7.3 Guarantee and Contribution Rules

| Rule | Description |
|------|-------------|
| Minimum contribution | Total contribution must meet product's min_contribution_percentage |
| Contribution verification | Contributions > 10M XAF require source verification |
| Guarantee coverage | Total guarantee value must meet product's collateral requirement |
| Multiple guarantees | Applicant may offer multiple guarantees for one request |
| Guarantee substitution | Applicant may substitute guarantees during application |
| Contribution release | Contributions are released to provider upon approval |

---

## 8. Repayment Capacity Calculation

Computes the applicant's ability to repay a loan based on income, expenses, and existing obligations.

### 8.1 Repayment Capacity Formula

```
repayment_capacity = monthly_net_income - monthly_expenses - existing_loan_payments

Where:
- monthly_net_income = monthly_income + additional_income (monthly average)
- monthly_expenses = sum of all expense categories
- existing_loan_payments = total monthly payments on existing loans

Debt-to-Income Ratio (DTI):
dti_ratio = (existing_loan_payments + proposed_monthly_payment) / monthly_net_income

Loan-to-Value Ratio (LTV):
ltv_ratio = loan_amount / property_appraised_value

Maximum Affordable Loan:
Based on DTI threshold (typically 40%):
max_affordable_monthly_payment = monthly_net_income × max_dti_ratio - existing_loan_payments
max_affordable_loan = present_value(max_affordable_monthly_payment, term_months, interest_rate)
```

### 8.2 Repayment Capacity Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `financing_request_id` | UUID | Reference to FinancingRequest |
| `monthly_net_income` | Decimal | Computed monthly net income |
| `monthly_expenses` | Decimal | Total monthly expenses |
| `existing_loan_payments` | Decimal | Total existing monthly loan payments |
| `disposable_income` | Decimal | Net income - expenses - existing payments |
| `proposed_monthly_payment` | Decimal? | Proposed monthly payment for requested loan |
| `dti_ratio` | Float | Computed debt-to-income ratio |
| `max_affordable_monthly_payment` | Decimal | Max monthly payment based on DTI threshold |
| `max_affordable_loan_amount` | Decimal | Max loan amount based on repayment capacity |
| `ltv_ratio` | Float? | Loan-to-value ratio (if property value known) |
| `repayment_capacity_score` | Enum | `excellent \| good \| fair \| weak \| insufficient` |
| `score_thresholds` | JSON | Thresholds used for scoring `{excellent, good, fair, weak, insufficient}` |
| `used_dti_threshold` | Float | DTI threshold applied (typically 0.40) |
| `used_interest_rate` | Decimal | Interest rate used in calculation |
| `used_term_months` | Int | Term used in calculation |
| `calculated_at` | DateTime | Calculation timestamp |
| `notes` | Text? | Calculation notes |

### 8.3 Repayment Capacity Scoring

| Score | DTI Ratio | Disposable Income | Description |
|-------|-----------|-------------------|-------------|
| Excellent | ≤ 20% | > 2× proposed payment | Strong capacity |
| Good | 21-30% | 1.5-2× proposed payment | Adequate capacity |
| Fair | 31-40% | 1-1.5× proposed payment | Marginal capacity |
| Weak | 41-50% | 0.75-1× proposed payment | Below threshold |
| Insufficient | > 50% | < 0.75× proposed payment | Cannot afford |

---

## 9. Document Requirements per Financing Type

Defines the documents required for each financing type. Documents are either mandatory (must be submitted) or conditional (required based on applicant profile or product terms).

### 9.1 Document Requirement Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `product_id` | UUID? | Reference to FinancingProduct (product-specific requirement) |
| `financing_type` | Enum? | Financing type requirement (type-level default) |
| `document_code` | String | Unique document code (e.g., `DOC-ID-CARD`, `DOC-PAYSLIP`) |
| `document_name` | JSON | Multilingual document name |
| `description` | JSON | Multilingual description of what is needed |
| `category` | Enum | `identity \| income \| employment \| property \| legal \| financial \| guarantee \| business \| personal` |
| `requirement_level` | Enum | `mandatory \| conditional \| recommended` |
| `condition_expression` | JSON? | JSON expression for conditional requirements |
| `accepts_alternatives` | Boolean | Whether alternative documents are accepted |
| `alternative_document_codes` | String[]? | Accepted alternative document codes |
| `max_age_months` | Int? | Maximum document age in months |
| `requires_notarization` | Boolean | Whether document must be notarized |
| `requires_translation` | Boolean | Whether document must be translated |
| `accepted_formats` | String[] | Accepted file formats (e.g., `pdf, jpg, png`) |
| `max_file_size_mb` | Int | Maximum file size (default 10 MB) |
| `is_active` | Boolean | Whether this requirement is active |
| `sort_order` | Int | Display order |
| `created_at` | DateTime | Requirement creation |

### 9.2 Document Requirements by Financing Type

| Document Code | Name (FR) | Category | Mortgage | Personal Loan | Construction | Bridge | Social Housing | Microfinance |
|--------------|-----------|----------|----------|---------------|--------------|--------|----------------|--------------|
| `DOC-ID-CARD` | Carte Nationale d'Identité | identity | M | M | M | M | M | M |
| `DOC-PASSPORT` | Passeport | identity | C | C | C | C | C | — |
| `DOC-RESIDENCE` | Carte de Séjour | identity | C | C | C | C | C | — |
| `DOC-PAYSLIP-3M` | Bulletins de Salaire (3 mois) | income | M | M | M | — | M | C |
| `DOC-BANK-STATEMENT-6M` | Relevés Bancaires (6 mois) | income | M | M | M | M | M | M |
| `DOC-TAX-RETURN` | Déclaration d'Impôts | income | M | C | M | C | M | — |
| `DOC-EMPLOYER-LETTER` | Attestation d'Emploi | employment | M | M | M | — | M | C |
| `DOC-RCCM` | Registre de Commerce (RCCM) | business | C | — | M | — | — | — |
| `DOC-BUSINESS-LICENSE` | Patente / Licence | business | C | — | M | — | — | — |
| `DOC-TAX-CLEARANCE` | Quitus Fiscal | business | — | — | M | C | — | — |
| `DOC-PROPERTY-TITLE` | Titre Foncier | property | M | C | M | M | M | C |
| `DOC-SALE-AGREEMENT` | Compromis de Vente | property | M | — | — | — | M | — |
| `DOC-CADASTRAL-PLAN` | Plan Cadastral | property | — | — | M | M | — | — |
| `DOC-CONSTRUCTION-PERMIT` | Permis de Construire | property | — | — | M | M | — | — |
| `DOC-APPRAISAL` | Rapport d'Évaluation | property | M | — | M | M | M | — |
| `DOC-DEED-OF-SALE` | Acte de Vente | legal | M | — | — | — | M | — |
| `DOC-MARRIAGE-CERT` | Acte de Mariage | legal | C | C | C | — | C | — |
| `DOC-GUARANTEE-LETTER` | Lettre de Garantie | guarantee | M | C | M | M | M | C |
| `DOC-CONTRIBUTION-PROOF` | Preuve d'Apport | financial | M | M | M | M | M | M |
| `DOC-INSURANCE` | Attestation d'Assurance | financial | M | C | M | M | — | — |

**Legend:** M = Mandatory, C = Conditional, — = Not Required

### 9.3 Document Submission Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `financing_request_id` | UUID | Reference to FinancingRequest |
| `document_requirement_id` | UUID | Reference to DocumentRequirement |
| `document_url` | String | Secure document storage URL |
| `document_hash` | String | SHA-256 integrity hash |
| `file_type` | String | MIME type |
| `file_size_bytes` | Int | File size |
| `status` | Enum | `pending \| uploaded \| validated \| rejected \| expired` |
| `uploaded_at` | DateTime | Upload timestamp |
| `validated_by` | UUID? | Admin who validated |
| `validated_at` | DateTime? | Validation timestamp |
| `rejection_reason` | Text? | Reason if rejected |
| `is_alternative` | Boolean | Whether this is an alternative document |
| `alternative_for_code` | String? | Original document code this replaces |
| `expires_at` | DateTime? | Document expiration date |
| `notes` | Text? | Additional notes |

---

## 10. Financing Match (Demandeur ↔ Product)

The match between a financing request and a financing product. Match is established after eligibility rules are satisfied and before a decision is rendered.

### 10.1 Financing Match Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `financing_request_id` | UUID | Reference to FinancingRequest |
| `product_id` | UUID | Reference to FinancingProduct |
| `provider_id` | UUID | Reference to FinancingProvider |
| `match_type` | Enum | `auto \| manual \| demandeur_selected \| agent_selected` |
| `match_score` | Float? | Compatibility score (0.0-1.0) |
| `eligibility_result` | Enum | `eligible \| conditionally_eligible \| ineligible` |
| `eligibility_details` | JSON | Detailed eligibility check results |
| `failed_rules` | JSON[] | Rules that failed (if conditionally_eligible) |
| `warnings` | JSON[] | Soft warnings triggered |
| `proposed_amount` | Decimal | Proposed loan amount based on eligibility |
| `proposed_term_months` | Int | Proposed term |
| `proposed_interest_rate` | Decimal | Proposed interest rate |
| `proposed_monthly_payment` | Decimal | Computed monthly payment |
| `total_cost_of_credit` | Decimal | Total cost including interest and fees |
| `effective_apr` | Decimal | Effective APR for this match |
| `status` | Enum | `pending \| selected \| submitted \| in_progress \| successful \| unsuccessful \| expired` |
| `selected_at` | DateTime? | When demandeur selected this match |
| `submitted_to_provider_at` | DateTime? | When dossier was submitted to provider |
| `provider_responded_at` | DateTime? | When provider responded |
| `expires_at` | DateTime? | Match offer expiration |
| `notes` | Text? | Match notes |
| `created_at` | DateTime | Match creation |

### 10.2 Match Scoring Algorithm

```
match_score = eligibility_weight × eligibility_score +
              capacity_weight × capacity_score +
              product_fit_weight × product_fit_score +
              preference_weight × preference_score

Where:
- eligibility_weight = 0.50 (binary: all hard rules pass or fail)
  - eligibility_score = 1.0 if all pass; 0.0 if any fail; 0.5 if conditionally eligible
- capacity_weight = 0.25
  - capacity_score = repayment_capacity_score mapped to {excellent=1.0, good=0.8, fair=0.6, weak=0.3, insufficient=0.0}
- product_fit_weight = 0.15
  - product_fit_score = composite of amount match (requested vs max), term match, rate competitiveness
- preference_weight = 0.10
  - preference_score = match against demandeur stated preferences (provider type, term, rate)
```

### 10.3 Match Lifecycle

```
Eligibility Check → [eligible] → Match Created → presented to demandeur
                                           → [selected] → Dossier Preparation
                                                       → documents uploaded
                                                       → submitted to provider
                                                       → provider review
                                                       → [approved | rejected | conditional]
                                                       → [funded | withdrawn | expired]
                    → [ineligible] → Demandeur notified with reasons
                                   → Alternative suggestions (if partial match)
                    → [conditional] → Warnings presented; demandeur decides to proceed
```

---

## 11. Financing Decision Tracking

Tracks the provider's decision on a submitted financing application.

### 11.1 Financing Decision Entity

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `financing_match_id` | UUID | Reference to FinancingMatch |
| `financing_request_id` | UUID | Reference to FinancingRequest |
| `provider_id` | UUID | Reference to FinancingProvider |
| `decision_type` | Enum | `approved \| rejected \| conditional \| pending_documents \| under_review \| withdrawn \| expired` |
| `decision_date` | DateTime | Decision date |
| `decision_reason_code` | String? | Standardized reason code |
| `decision_reason_text` | Text? | Provider's reason text |
| `decision_details` | JSON? | Detailed decision breakdown |
| `approved_amount` | Decimal? | Amount approved (if approved) |
| `approved_term_months` | Int? | Approved term (if approved) |
| `approved_interest_rate` | Decimal? | Approved interest rate (if approved) |
| `approved_conditions` | JSON? | Conditions for conditional approval |
| `rejection_category` | Enum? | `credit_history \| insufficient_income \| debt_ratio \| collateral \| documentation \| eligibility \| policy \| other` |
| `rejection_details` | JSON? | Detailed rejection breakdown |
| `counter_offer_amount` | Decimal? | Counter-offer amount (if applicable) |
| `counter_offer_terms` | JSON? | Counter-offer terms |
| `provider_reference` | String? | Provider's internal reference number |
| `provider_officer_name` | String? | Provider officer handling the file |
| `provider_officer_contact` | String? | Provider officer contact |
| `estimated_funding_date` | DateTime? | Estimated disbursement date |
| `funded_at` | DateTime? | Actual disbursement date |
| `funded_amount` | Decimal? | Actual amount disbursed |
| `commission_earned` | Decimal? | LAWIM commission earned |
| `commission_currency` | String | Commission currency |
| `commission_paid` | Boolean | Whether commission has been paid |
| `commission_paid_at` | DateTime? | Commission payment date |
| `demandeur_notified` | Boolean | Whether demandeur was notified of decision |
| `demandeur_notified_at` | DateTime? | Notification timestamp |
| `demandeur_feedback` | Enum? | `satisfied \| neutral \| dissatisfied` |
| `status` | Enum | `pending \| under_review \| decision_made \| funded \| closed \| appealed` |
| `created_at` | DateTime | Decision record creation |
| `updated_at` | DateTime | Last update |

### 11.2 Decision Reason Codes

| Code | Label (FR) | Category | Description |
|------|------------|----------|-------------|
| `INC-001` | Revenu insuffisant | insufficient_income | Monthly income below minimum requirement |
| `INC-002` | Revenu non vérifiable | insufficient_income | Income source cannot be verified |
| `DTI-001` | Ratio d'endettement trop élevé | debt_ratio | Debt-to-income ratio exceeds maximum |
| `DTI-002` | Capacité de remboursement insuffisante | debt_ratio | Disposable income insufficient |
| `CRD-001` | Historique de crédit défavorable | credit_history | Negative credit history |
| `CRD-002` | Score de crédit insuffisant | credit_history | Credit score below minimum |
| `CRD-003` | Défaut de paiement antérieur | credit_history | Previous default |
| `COL-001` | Garantie insuffisante | collateral | Collateral value below requirement |
| `COL-002` | Titre foncier non valide | collateral | Land title invalid or encumbered |
| `COL-003` | Garant non acceptable | collateral | Guarantor does not meet criteria |
| `DOC-001` | Documents incomplets | documentation | Required documents missing |
| `DOC-002` | Documents non conformes | documentation | Documents do not meet requirements |
| `DOC-003` | Documents expirés | documentation | Documents have expired |
| `ELG-001` | Âge hors limite | eligibility | Applicant age outside allowable range |
| `ELG-002` | Nationalité non éligible | eligibility | Nationality not accepted |
| `ELG-003` | Résidence non conforme | eligibility | Residency requirement not met |
| `ELG-004` | Type d'emploi non accepté | eligibility | Employment type not accepted |
| `POL-001` | Politique interne du prêteur | policy | Internal policy decline (non-specific) |
| `POL-002` | Plafond mensuel atteint | policy | Provider monthly quota reached |
| `OTH-001` | Autre raison | other | Other reason (requires explanation) |

### 11.3 Decision Lifecycle

```
Match submitted to provider
  → under_review (provider reviewing)
    → pending_documents (additional documents requested)
      → documents_received → under_review
    → approved (full approval)
      → conditions_met → funded
      → conditions_not_met → withdrawn
    → conditional (approval with conditions)
      → conditions_met → funded
      → conditions_not_met → rejected
    → rejected (full rejection)
      → appeal (re-submission with additional info)
        → under_review → ...
      → closed
    → counter_offer (alternative terms proposed)
      → accepted → funded
      → declined → closed
```

---

## 12. Complete Extension Mapping Table

### 12.1 Financing Extensions

| Extension ID | Source Concept | Target Entity | Proposed Structure | Priority | Human Decision |
|-------------|---------------|---------------|-------------------|----------|----------------|
| EXT-FIN-001 | Financing Request entity | FinancingRequest | Full request entity with financing_type, amount, preferred terms, status lifecycle, relationships to applicant, project, and financial profile | P1 | Y — financing types |
| EXT-FIN-002 | Financing Product catalog | FinancingProduct | Product entity with amount range, term range, interest rate, fees, collateral requirements, target market, geographic availability, matching attributes | P1 | Y — product fields |
| EXT-FIN-003 | Financing Provider model | FinancingProvider | Provider entity with provider_type (bank/microfinance/etc.), verification, commission model, integration type, SLA, API status | P1 | Y — provider types |
| EXT-FIN-004 | Eligibility rules engine | EligibilityRule | Rule entity with categories (income, employment, age, residency, DTI, LTV, collateral), operators, severity levels, evaluation flow; product-level and provider-level rules | P2 | Y — rules per product |
| EXT-FIN-005 | Applicant Financial Profile | ApplicantFinancialProfile | Comprehensive financial profile with employment, income, expenses, assets, liabilities, credit history, verification method | P1 | Y — verification methods |
| EXT-FIN-006 | Guarantee and Contribution tracking | Guarantee + Contribution | Guarantee entity (type, value, valuation, ownership, encumbrance); Contribution entity (type, amount, source, commitment status) | P2 | N |
| EXT-FIN-007 | Repayment Capacity calculation | RepaymentCapacity | Computed capacity based on DTI, LTV, disposable income; scoring excellent/good/fair/weak/insufficient; max affordable loan calculation | P1 | Y — DTI threshold |
| EXT-FIN-008 | Document Requirements per financing type | DocumentRequirement + DocumentSubmission | Requirement entity per financing type (mandatory/conditional); submission entity with upload, hash, validation, expiry tracking | P2 | Y — document lists |
| EXT-FIN-009 | Financing Match (Demandeur ↔ Product) | FinancingMatch | Match entity with eligibility result, match score, proposed terms, status lifecycle (eligible→selected→submitted→result); scoring algorithm weighted | P2 | Y — scoring weights |
| EXT-FIN-010 | Financing Decision tracking | FinancingDecision | Decision entity with decision_type, reason codes (standardized), approval terms, conditions, rejection categories, counter-offer handling, commission tracking | P2 | Y — reason codes |

### 12.2 All Financing Fields Extension Table

| Field | Entity | Type | Extension Source | Description |
|-------|--------|------|------------------|-------------|
| `financing_type` | FinancingRequest | Enum | EXT-FIN-001 | Type of financing requested |
| `requested_amount` | FinancingRequest | Decimal | EXT-FIN-001 | Amount requested |
| `preferred_term_months` | FinancingRequest | Int? | EXT-FIN-001 | Preferred repayment term |
| `monthly_payment_capacity` | FinancingRequest | Decimal? | EXT-FIN-001 | Self-declared capacity |
| `has_existing_loans` | FinancingRequest | Boolean | EXT-FIN-001 | Existing loans indicator |
| `financing_status` | FinancingRequest | Enum | EXT-FIN-001 | Request lifecycle status |
| `readiness_score` | FinancingRequest | Float? | EXT-FIN-001 | Profile completeness |
| `product_code` | FinancingProduct | String | EXT-FIN-002 | Unique product code |
| `product_name` | FinancingProduct | JSON | EXT-FIN-002 | Multilingual name |
| `financing_type` | FinancingProduct | Enum | EXT-FIN-002 | Product financing type |
| `min_amount` | FinancingProduct | Decimal | EXT-FIN-002 | Minimum loan amount |
| `max_amount` | FinancingProduct | Decimal | EXT-FIN-002 | Maximum loan amount |
| `min_term_months` | FinancingProduct | Int | EXT-FIN-002 | Minimum term |
| `max_term_months` | FinancingProduct | Int | EXT-FIN-002 | Maximum term |
| `interest_rate_type` | FinancingProduct | Enum | EXT-FIN-002 | fixed/variable/mixed/tiered |
| `interest_rate_min` | FinancingProduct | Decimal | EXT-FIN-002 | Minimum APR |
| `interest_rate_max` | FinancingProduct | Decimal | EXT-FIN-002 | Maximum APR |
| `effective_apr` | FinancingProduct | Decimal? | EXT-FIN-002 | Illustrative APR |
| `processing_fee_percentage` | FinancingProduct | Decimal? | EXT-FIN-002 | Processing fee |
| `collateral_required` | FinancingProduct | Boolean | EXT-FIN-002 | Collateral requirement |
| `guarantor_required` | FinancingProduct | Boolean | EXT-FIN-002 | Guarantor requirement |
| `target_market` | FinancingProduct | Enum[] | EXT-FIN-002 | Target segments |
| `geographic_availability` | FinancingProduct | String[] | EXT-FIN-002 | Available regions |
| `provider_type` | FinancingProvider | Enum | EXT-FIN-003 | bank/microfinance/etc |
| `provider_name` | FinancingProvider | String | EXT-FIN-003 | Legal name |
| `registration_number` | FinancingProvider | String? | EXT-FIN-003 | Regulatory registration |
| `verification_status` | FinancingProvider | Enum | EXT-FIN-003 | Provider verification |
| `commission_model` | FinancingProvider | Enum | EXT-FIN-003 | Commission model |
| `integration_type` | FinancingProvider | Enum | EXT-FIN-003 | API/manual/paper |
| `rule_code` | EligibilityRule | String | EXT-FIN-004 | Unique rule identifier |
| `rule_type` | EligibilityRule | Enum | EXT-FIN-004 | income/employment/age/etc |
| `operator` | EligibilityRule | Enum | EXT-FIN-004 | greater_than/less_than/etc |
| `value` | EligibilityRule | JSON | EXT-FIN-004 | Threshold value |
| `severity` | EligibilityRule | Enum | EXT-FIN-004 | hard_block/soft_warning/info |
| `employment_status` | ApplicantFinancialProfile | Enum | EXT-FIN-005 | civil_servant/private/self_employed |
| `monthly_income` | ApplicantFinancialProfile | Decimal | EXT-FIN-005 | Total monthly income |
| `monthly_expenses` | ApplicantFinancialProfile | Decimal | EXT-FIN-005 | Total monthly expenses |
| `existing_loan_payments` | ApplicantFinancialProfile | Decimal? | EXT-FIN-005 | Existing monthly payments |
| `total_assets` | ApplicantFinancialProfile | Decimal? | EXT-FIN-005 | Total assets |
| `total_liabilities` | ApplicantFinancialProfile | Decimal? | EXT-FIN-005 | Total liabilities |
| `credit_score` | ApplicantFinancialProfile | Int? | EXT-FIN-005 | Credit score |
| `guarantee_type` | Guarantee | Enum | EXT-FIN-006 | property_mortgage/land_deed/etc |
| `estimated_value` | Guarantee | Decimal | EXT-FIN-006 | Guarantee value |
| `net_equity` | Guarantee | Decimal? | EXT-FIN-006 | Value - existing charges |
| `guarantee_status` | Guarantee | Enum | EXT-FIN-006 | offered/verified/accepted/rejected |
| `contribution_type` | Contribution | Enum | EXT-FIN-006 | cash/equity/material/labor |
| `contribution_amount` | Contribution | Decimal | EXT-FIN-006 | Contribution amount |
| `contribution_status` | Contribution | Enum | EXT-FIN-006 | planned/committed/verified/received |
| `monthly_net_income` | RepaymentCapacity | Decimal | EXT-FIN-007 | Computed net income |
| `disposable_income` | RepaymentCapacity | Decimal | EXT-FIN-007 | Income - expenses - payments |
| `dti_ratio` | RepaymentCapacity | Float | EXT-FIN-007 | Debt-to-income ratio |
| `max_affordable_loan` | RepaymentCapacity | Decimal | EXT-FIN-007 | Max loan by capacity |
| `capacity_score` | RepaymentCapacity | Enum | EXT-FIN-007 | excellent/good/fair/weak/insufficient |
| `document_code` | DocumentRequirement | String | EXT-FIN-008 | Unique document code |
| `requirement_level` | DocumentRequirement | Enum | EXT-FIN-008 | mandatory/conditional/recommended |
| `max_age_months` | DocumentRequirement | Int? | EXT-FIN-008 | Max document age |
| `document_status` | DocumentSubmission | Enum | EXT-FIN-008 | pending/uploaded/validated/rejected |
| `document_hash` | DocumentSubmission | String | EXT-FIN-008 | SHA-256 integrity hash |
| `match_score` | FinancingMatch | Float? | EXT-FIN-009 | 0.0-1.0 compatibility |
| `eligibility_result` | FinancingMatch | Enum | EXT-FIN-009 | eligible/conditionally_eligible/ineligible |
| `proposed_amount` | FinancingMatch | Decimal | EXT-FIN-009 | Proposed loan amount |
| `proposed_interest_rate` | FinancingMatch | Decimal | EXT-FIN-009 | Proposed rate |
| `total_cost_of_credit` | FinancingMatch | Decimal | EXT-FIN-009 | Total cost with fees |
| `match_status` | FinancingMatch | Enum | EXT-FIN-009 | Match lifecycle |
| `decision_type` | FinancingDecision | Enum | EXT-FIN-010 | approved/rejected/conditional |
| `decision_reason_code` | FinancingDecision | String? | EXT-FIN-010 | Standardized reason |
| `rejection_category` | FinancingDecision | Enum? | EXT-FIN-010 | credit_history/income/etc |
| `approved_amount` | FinancingDecision | Decimal? | EXT-FIN-010 | Amount approved |
| `approved_interest_rate` | FinancingDecision | Decimal? | EXT-FIN-010 | Approved rate |
| `commission_earned` | FinancingDecision | Decimal? | EXT-FIN-010 | LAWIM commission |
| `funded_at` | FinancingDecision | DateTime? | EXT-FIN-010 | Disbursement date |

### 12.3 New Entities

| Entity | Description | Extensions |
|--------|-------------|------------|
| `FinancingRequest` | Central financing entity; represents a demandeur's application for financing with full lifecycle | EXT-FIN-001, EXT-FIN-006, EXT-FIN-007 |
| `FinancingProduct` | Financing product catalog entry with terms, rates, and eligibility criteria | EXT-FIN-002, EXT-FIN-004, EXT-FIN-008 |
| `FinancingProvider` | Financial institution offering financing products on the platform | EXT-FIN-003 |
| `EligibilityRule` | Hard/soft constraint evaluated against applicant profile during matching | EXT-FIN-004 |
| `ApplicantFinancialProfile` | Comprehensive financial profile of the financing applicant | EXT-FIN-005 |
| `Guarantee` | Collateral or guarantee offered to secure financing | EXT-FIN-006 |
| `Contribution` | Down payment or co-investment contribution | EXT-FIN-006 |
| `RepaymentCapacity` | Computed repayment capacity based on financial profile | EXT-FIN-007 |
| `DocumentRequirement` | Document requirement definition per financing type | EXT-FIN-008 |
| `DocumentSubmission` | Document uploaded as part of financing application | EXT-FIN-008 |
| `FinancingMatch` | Match between a FinancingRequest and a FinancingProduct | EXT-FIN-009 |
| `FinancingDecision` | Provider's decision on a submitted financing application | EXT-FIN-010 |

---

*End of FINANCING_EXTENSION_MODEL.md — 12 sections, 10 financing extensions, 12 financing types, 10 provider types, 11 eligibility rule categories, 12 new entities defined. LAWIM does not replace the financier — it facilitates the match.*
