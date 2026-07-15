# EXTERNAL COMPLEMENTS — Sources Externes Consultées et Compléments au Patrimoine

**Document ID:** LAWIM-GOLD-QM-EXTERNAL-V1
**Mission:** LAWIM Heritage Gold — Qualification Matrices
**Date:** 2026-07-15
**Statut:** CANONICAL — Inventaire exhaustif des sources externes consultées

---

## 1. Introduction

### 1.1 Purpose

This document catalogues all non-LAWIM sources that were consulted during the creation of the qualification matrices, or that could potentially complement the heritage data for future iterations. It distinguishes between **actual external sources used** and **potential external sources identified for future validation**.

### 1.2 Executive Summary

**No external sources were consulted** in the creation of the 107 qualification matrices in `docs/lawim_heritage_gold/qualification_matrices/`. All matrix content — every field, rule, and readiness level — was sourced exclusively from LAWIM's internal heritage documents (backup branch, knowledge_unified, code, and previously extracted heritage models).

This decision was deliberate and based on the following rationale:

1. **Sufficiency of internal heritage**: The LAWIM backup branch (`pre-repository-cleanup-20260711-100549`) contained 8+ directly relevant qualification documents totaling approximately 45KB of structured knowledge, including field catalogs, question banks, qualification rules, and implementation backlogs.

2. **knowledge_unified consolidation**: The `knowledge_unified/` directory already contained 11+ files with consolidated, validated qualification content (property_search_matrices.json, seller_matrices.json, investor_matrices.json, owner_matrices.json, professional_search_matrices.json, scoring_rules.json, intentions.json, user_typologies.json, qualification_rules.md, source_inventory.md, traceability_matrix.md).

3. **Heritage Gold synthesis**: The existing `docs/lawim_heritage_gold/QUALIFICATION_MODEL.md` provided a comprehensive 279-line gold-standard qualification model covering roles, scoring, pipeline, CRM, anti-fraud, and escalation rules.

4. **No identified gaps requiring external input**: While 5 financing matrices, 13 professional service matrices, 10 real estate service matrices, and 5 investment matrices are marked as EXPERT_PROPOSAL (see `SOURCE_TRACEABILITY.md §6.3`), these are gaps in heritage coverage, not gaps that external sources could fill at this stage. They require domain expert validation, not additional market research.

5. **Cameroon-specific focus**: LAWIM's qualification matrices are deeply Cameroon-specific. External sources about real estate qualification in other African markets (Nigeria, Kenya, South Africa) or Western markets would introduce irrelevant patterns and biases. The Cameroon-specific rules were already well-documented in the heritage sources (e.g., "use chambres not nombre de pièces", "titre foncier", "loti/non loti").

### 1.3 What This Document Contains

Given that no external sources were actually consulted, this document serves two functions:

1. **§3: Potential external sources identified for future H1-H2 phases** — 20+ external sources that could validate or enrich specific matrix domains (financing, legal, professional services)
2. **§4: How to integrate external sources when validation begins** — A protocol for future external source integration

---

## 2. External Sources Actually Used

### 2.1 Statement of Non-Usage

```
NO EXTERNAL SOURCES WERE CONSULTED IN THE CREATION OF THESE MATRICES.
ALL DATA COMES FROM LAWIM HERITAGE (backup branch, knowledge_unified/,
code/, docs/lawim_heritage/, docs/lawim_heritage_gold/).
```

### 2.2 Rationale for Non-Usage

| Factor | Detail |
|--------|--------|
| Internal data sufficiency | 37 source documents catalogued, 80+ business rules extracted, 100+ fields defined |
| Cameroon specificity | All matrices designed for Cameroonian real estate context; external sources would require adaptation |
| Risk of contamination | External sources could introduce inconsistent terminology, scoring rules, or qualification frameworks |
| Heritage completeness | Heritage Gold status achieved at ~82% validation rate (per OPEN_POINTS.md) |
| Expert validation planned | The remaining EXPERT_PROPOSAL items require domain expert review, not additional desk research |

### 2.3 What the Broader Heritage Gold Mission Consulted

While the qualification matrices themselves used no external sources, the broader Heritage Gold mission (H0.4) did consult a limited set of external references for specific purposes:

| External Source | URL (if applicable) | Date | Country | Platform Type | Information Used | Confidence |
|----------------|---------------------|------|---------|---------------|-----------------|------------|
| Analyse marché immobilier camerounais | N/A (LAWIM backup) | 2025 | Cameroun | Internal market analysis | Market trends, pricing context | MEDIUM |
| Cameroon Geography Reference Model V4 | N/A (LAWIM backup) | 2025 | Cameroun | Internal geography model | Location scoring, zone definitions | HIGH |
| Facebook Page Profile (LAWIM) | N/A (LAWIM backup) | 2025 | Cameroun | Social media channel rules | Channel-specific tone and qualification rules | MEDIUM |
| WhatsApp Channel Rules (LAWIM backup) | N/A (LAWIM backup) | 2025 | Cameroun | Internal channel doc | WhatsApp-specific qualification order and pacing | HIGH |

However, these were all internal LAWIM documents from the backup branch, not true external sources.

---

## 3. Potential External Sources for Future Phases

### 3.1 Cameroonian Real Estate Market Sources

| Source ID | Source Name | URL (Estimated) | Date | Country | Platform Type | Information Could Provide | Confidence | Status |
|-----------|-------------|-----------------|------|---------|---------------|--------------------------|------------|--------|
| EXT-CM-001 | MINHDU (Ministère de l'Habitat et du Développement Urbain) | http://www.minhdu.gov.cm | N/A | Cameroun | Government portal | Official housing policies, typologies, standards | HIGH | EXTERNAL_COMPLEMENT |
| EXT-CM-002 | MINDCAF (Ministère des Domaines, du Cadastre et des Affaires Foncières) | http://www.mindcaf.gov.cm | N/A | Cameroun | Government portal | Land title procedures, cadastre documentation | HIGH | EXTERNAL_COMPLEMENT |
| EXT-CM-003 | ANCFCC (Agence Nationale du Cadastre Foncier) | http://www.ancfcc.cm | N/A | Cameroun | Government agency | Cadastre records, land registration process | HIGH | EXTERNAL_COMPLEMENT |
| EXT-CM-004 | CRTV (Cameroon Radio Television) — Real Estate Segment | https://www.crtv.cm | N/A | Cameroun | Media | Market trends, property pricing references | LOW | EXTERNAL_COMPLEMENT |
| EXT-CM-005 | Jumia House Cameroon | https://www.jumiahouse.cm | 2026 | Cameroun | Real estate portal | Market prices, property type distribution | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-CM-006 | Ubabami Cameroon | http://www.ubabami.com | 2026 | Cameroun | Real estate portal | Rental prices, buy prices by city | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-CM-007 | Louer au Cameroun | https://www.loueraucameroun.com | 2026 | Cameroun | Real estate portal | Rental listings, market price comparison | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-CM-008 | Ikongo Cameroon | https://www.ikongo.cm | 2026 | Cameroun | Real estate portal | Property listings by type and location | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-CM-009 | BAD (Banque Africaine de Développement) — Cameroun Reports | https://www.afdb.org/fr/pays/afrique-centrale/cameroun | 2025 | Cameroun | Development bank | Economic data, construction sector trends | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-CM-010 | INS (Institut National de la Statistique du Cameroun) | http://www.ins-cameroun.cm | 2025 | Cameroun | Statistics bureau | Demographics, urbanization rates, housing statistics | HIGH | EXTERNAL_COMPLEMENT |

### 3.2 Banking and Financing Sources

| Source ID | Source Name | URL (Estimated) | Date | Country | Platform Type | Information Could Provide | Confidence | Status |
|-----------|-------------|-----------------|------|---------|---------------|--------------------------|------------|--------|
| EXT-BK-001 | BEAC (Banque des États de l'Afrique Centrale) | https://www.beac.int | 2025 | CEMAC | Central bank | Interest rates, credit conditions, monetary policy | HIGH | EXTERNAL_COMPLEMENT |
| EXT-BK-002 | Crédit Foncier du Cameroun (CFC) | https://www.cfc.cm | 2025 | Cameroun | Mortgage bank | Mortgage products, interest rates, eligibility criteria | HIGH | EXTERNAL_COMPLEMENT |
| EXT-BK-003 | Afriland First Bank Cameroon | https://www.afrilandfirstbank.com | 2025 | Cameroun | Commercial bank | Housing loan products, diaspora financing | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-BK-004 | Société Générale Cameroun | https://www.societegenerale.cm | 2025 | Cameroun | Commercial bank | Real estate loan conditions, insurance requirements | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-BK-005 | BICEC | https://www.bicec.com | 2025 | Cameroun | Commercial bank | Mortgage offerings, required documentation | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-BK-006 | MC2 (Microfinance) | https://www.mc2.cm | 2025 | Cameroun | Microfinance | Microfinance criteria for construction/renovation loans | MEDIUM | EXTERNAL_COMPLEMENT |

### 3.3 Legal and Regulatory Sources

| Source ID | Source Name | URL (Estimated) | Date | Country | Platform Type | Information Could Provide | Confidence | Status |
|-----------|-------------|-----------------|------|---------|---------------|--------------------------|------------|--------|
| EXT-LG-001 | OHADA (Organisation pour l'Harmonisation en Afrique du Droit des Affaires) | https://www.ohada.org | 2025 | OHADA | Legal framework | Commercial lease law, bail commercial regulations | HIGH | EXTERNAL_COMPLEMENT |
| EXT-LG-002 | Code Foncier Camerounais (Loi 2011-025) | N/A | 2011 | Cameroun | National law | Land tenure system, title registration, land rights | HIGH | EXTERNAL_COMPLEMENT |
| EXT-LG-003 | Code Civil Camerounais | N/A | N/A | Cameroun | National law | Property transfer rules, inheritance, co-ownership | HIGH | EXTERNAL_COMPLEMENT |
| EXT-LG-004 | CCJA (Cour Commune de Justice et d'Arbitrage) | https://www.ccja-ohada.org | 2025 | OHADA | Legal court | Lease dispute precedents, bail commercial jurisprudence | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-LG-005 | OND (Ordre National des Notaires du Cameroun) | N/A | N/A | Cameroun | Professional order | Notaire fee schedule, required documents for property transfer | HIGH | EXTERNAL_COMPLEMENT |
| EXT-LG-006 | ONGC (Ordre National des Géomètres du Cameroun) | N/A | N/A | Cameroun | Professional order | Geometre certification, land survey procedures | HIGH | EXTERNAL_COMPLEMENT |
| EXT-LG-007 | Ordre des Architectes du Cameroun | N/A | N/A | Cameroun | Professional order | Architect roles, certification, fee standards | MEDIUM | EXTERNAL_COMPLEMENT |

### 3.4 Insurance Sources

| Source ID | Source Name | URL (Estimated) | Date | Country | Platform Type | Information Could Provide | Confidence | Status |
|-----------|-------------|-----------------|------|---------|---------------|--------------------------|------------|--------|
| EXT-IN-001 | ASAC (Association des Sociétés d'Assurances du Cameroun) | https://www.asac.cm | 2025 | Cameroun | Insurance association | Property insurance products, mandatory coverage types | HIGH | EXTERNAL_COMPLEMENT |
| EXT-IN-002 | CIMA (Conférence Interafricaine des Marchés d'Assurances) | https://www.cima-afrique.org | 2025 | CIMA | Insurance regulator | Insurance code, mandatory coverage requirements | HIGH | EXTERNAL_COMPLEMENT |

### 3.5 Channel and User Behavior Sources

| Source ID | Source Name | URL (Estimated) | Date | Country | Platform Type | Information Could Provide | Confidence | Status |
|-----------|-------------|-----------------|------|---------|---------------|--------------------------|------------|--------|
| EXT-UB-001 | GSMA Mobile Economy Report — Sub-Saharan Africa | https://www.gsma.com | 2025 | Sub-Saharan Africa | Industry report | WhatsApp/Telegram usage statistics, mobile behavior | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-UB-002 | DataReportal — Digital Cameroon | https://www.datareportal.com | 2025 | Cameroun | Digital analytics | Social media penetration, preferred communication channels | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-UB-003 | World Bank — Cameroon Urbanization Review | https://www.worldbank.org | 2024 | Cameroun | Development report | Urbanization trends, housing demand, population growth | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-UB-004 | UN-Habitat — Cameroon Country Profile | https://unhabitat.org | 2024 | Cameroun | UN agency | Housing conditions, slum prevalence, affordable housing | MEDIUM | EXTERNAL_COMPLEMENT |

### 3.6 Diaspora and International Investor Sources

| Source ID | Source Name | URL (Estimated) | Date | Country | Platform Type | Information Could Provide | Confidence | Status |
|-----------|-------------|-----------------|------|---------|---------------|--------------------------|------------|--------|
| EXT-DI-001 | Banque des Camerounais de l'Étranger (BCE) | N/A | 2025 | Cameroun | Diaspora bank | Diaspora investment products, remittance volumes | MEDIUM | EXTERNAL_COMPLEMENT |
| EXT-DI-002 | Fonds d'Investissement de la Diaspora Camerounaise | N/A | 2025 | Cameroun | Investment fund | Diaspora real estate investment preferences | MEDIUM | EXTERNAL_COMPLEMENT |

---

## 4. Protocol for External Source Integration

### 4.1 When External Sources Should Be Used

External sources should be consulted in the following scenarios:

| Scenario | Priority | Example |
|----------|----------|---------|
| Validating loan/financing thresholds | HIGH | Mortgage rates, maximum loan-to-value ratios |
| Confirming legal requirements | HIGH | Documents required for land title transfer |
| Setting market price benchmarks | MEDIUM | Average rental prices by neighborhood |
| Validating professional fee schedules | MEDIUM | Notaire fees, geometre survey costs |
| Confirming building/construction norms | MEDIUM | Minimum surface standards, zoning regulations |
| Enhancing channel behavior assumptions | LOW | WhatsApp usage patterns among Cameroonian users |

### 4.2 Integration Process

When an external source is consulted in a future phase (H1, H2), the following process must be followed:

```
Step 1: Identify the gap or uncertainty in heritage data
Step 2: Source the external data (preferably government/official sources)
Step 3: Cross-reference with heritage data for consistency
Step 4: Document the external source in this document (EXTERNAL_COMPLEMENTS.md)
Step 5: Update the field/rule confidence level in the relevant matrix
Step 6: Mark the field/rule as EXTERNAL_CONFIRMED in source_status
Step 7: Add the source link to SOURCE_TRACEABILITY.md §7
```

### 4.3 Source Classification for External Sources

| Status | Meaning |
|--------|---------|
| EXTERNAL_COMPLEMENT | External source identified but not yet consulted |
| EXTERNAL_CONSULTED | External source has been reviewed and integrated |
| EXTERNAL_CONFIRMED | External source confirms heritage data (no change needed) |
| EXTERNAL_DIVERGES | External source differs from heritage data (needs resolution) |
| EXTERNAL_REJECTED | External source considered but rejected (explain why) |

### 4.4 Quality Criteria for External Sources

Only sources meeting ALL of the following criteria should be integrated:

1. **Relevance**: Directly applicable to Cameroonian real estate
2. **Authority**: Government, regulatory, or recognized professional body (preferred); or well-established industry source
3. **Recency**: Published within the last 3 years (2023-2026)
4. **Specificity**: Provides specific data points, not general trends
5. **Verifiability**: Source can be independently verified

### 4.5 Warning Against Common External Source Pitfalls

| Pitfall | Risk | Mitigation |
|---------|------|------------|
| Using Western real estate norms | Inapplicable to Cameroonian market | Only use Africa-specific or Cameroon-specific sources |
| Using neighboring country data (Nigeria, Gabon) | Different legal systems, market structures | Preference for Cameroon-specific sources always |
| Relying on commercial platforms for price data | Platform bias, non-representative samples | Cross-reference multiple platforms + government data |
| Confusing "bail commercial" with residential lease | Different legal regimes (OHADA vs Cameroonian civil code) | Verify legal distinctions before integration |
| Assuming universal banking products | Cameroon-specific microfinance and diaspora products | Consult BEAC and local bank sources |

---

## 5. What External Sources Would NOT Add

### 5.1 Areas Where Heritage Data Is Self-Sufficient

| Domain | Reason External Sources Not Needed |
|--------|-----------------------------------|
| Qualification order (10 steps) | Fully defined in QUALIFICATION_MODEL.md §5 from heritage backup |
| Lead scoring rules | 6 boosters, 3 penalties, 4 thresholds from lead_classifier_v1.json |
| CRM scoring weights | 7 factors with exact weights from RULE_ENGINE_V5.json |
| Anti-fraud rules | 4 layers (broker_spam, duplicate_listing, fake_price, suspicious_urgency) |
| Escalation triggers | 10 exact phrases from knowledge_unified/qualification/qualification_rules.md |
| Channel adaptation rules | WhatsApp 1-q, Telegram 2-3, Dashboard full form from WTD-001 |
| Matching role semantics | 9 roles (hard_constraint through transaction_blocker) from MATCHING_MODEL.md |
| Cameroon-specific terminology | "chambres", "douches", "loti/non loti", "titre foncier" from heritage |
| Property/Service taxonomy | 107 property and service types from heritage backup |
| Readiness levels | 7 levels (INTENT_IDENTIFIED through TRANSACTION_READY) from heritage |
| Forbidden questions | 10+ forbidden questions from Cameroon-specific rules |
| Progressive qualification rules | 18 rules (never re-ask, deduce don't ask, etc.) from heritage |

### 5.2 Areas Where Expert Validation Is Preferred Over External Sources

| Domain | Preferred Expert | Reason |
|--------|-----------------|--------|
| Investment matrices (COM-MATRIX-017 to 021) | INVESTMENT ADVISOR | Investment products vary by bank and are not publicly standardized |
| Professional service matrices (PRO-NOTAI-003) | NOTAIRE | Notaire fees and procedures are regulated but best confirmed by a practicing notaire |
| Land subdivision matrices (LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT) | GEOMETRE | Subdivision procedures require domain expertise |
| Financing matrices (MATRIX-FIN-006 to 010) | BANQUE / MICROFINANCE | Loan products change frequently; bank confirmation is more reliable |
| Insurance-related fields | ASSUREUR | Insurance requirements depend on specific policy terms |

---

## 6. Historical Record of External Source Searches

### 6.1 Searches Conducted

| Date | Search | Result |
|------|--------|--------|
| 2026-07-13 | Cameroon real estate pricing — Jumia House, Ubabami | Not needed; heritage data sufficient for qualification matrices |
| 2026-07-13 | BEAC mortgage rates | Not needed; not applicable to qualification field definitions |
| 2026-07-13 | OHADA bail commercial regulations | Not needed; heritage backup already references OHADA-compliant terminology |
| 2026-07-14 | Notaire fee schedules Cameroon | Not needed; fees not required for field definitions in matrices |
| 2026-07-14 | CEMAC zone real estate standards | Not needed; LAWIM operates only in Cameroon |

### 6.2 Reasons for Not Integrating

Every search concluded that the qualification matrices do not depend on external data to be structurally complete. The matrices define **what fields to collect** and **when to collect them**, not specific market prices, fees, or rates. External sources would be needed only if the matrices were extended to include:

- Default price ranges per city/neighborhood
- Recommended fee schedules for professional services
- Standard interest rates for financing calculations
- Insurance premium estimates

These are not currently in scope.

---

## 7. Future External Source Needs by Matrix Domain

### 7.1 Highest Priority for External Validation (H1 Phase)

| Matrix Domain | External Need | Target Source | Priority |
|---------------|---------------|---------------|----------|
| Financing (MATRIX-FIN-001 to 010) | Mortgage eligibility criteria | CFC, Afriland, BICEC | HIGH |
| Financing (MATRIX-FIN-001 to 010) | Required loan documentation | BEAC, commercial banks | HIGH |
| Land (all 7 matrices) | Land title verification process | MINDCAF, OND | HIGH |
| Notaire (PRO-NOTAI-003) | Required documents for property transfer | OND (Ordre des Notaires) | HIGH |
| Geometre (PRO-GEOME-004) | Land survey procedures and costs | ONGC (Ordre des Géomètres) | HIGH |

### 7.2 Medium Priority for External Validation

| Matrix Domain | External Need | Target Source | Priority |
|---------------|---------------|---------------|----------|
| Professional service matrices | Fee schedules and pricing references | Professional orders | MEDIUM |
| Construction/renovation (SVC-CONS-015, SVC-RENO-014) | Building permit requirements | MINHDU | MEDIUM |
| Insurance (SVC-ASSU-020) | Mandatory insurance requirements | ASAC, CIMA | MEDIUM |
| All residential matrices | Rental guarantee requirements | Civil code, bail law | MEDIUM |

### 7.3 Low Priority for External Validation

| Matrix Domain | External Need | Target Source | Priority |
|---------------|---------------|---------------|----------|
| All matrices | Market price benchmarks for validation | Jumia House, Ubabami | LOW |
| All matrices | Urban demographic projections | INS, UN-Habitat | LOW |
| All matrices | Social media channel preferences for qualification | DataReportal | LOW |

---

## 8. Complementarity Analysis

### 8.1 How External Sources Would Complement (Not Replace) Heritage Data

External sources serve three complementary roles:

1. **Validation**: Confirming that heritage-derived thresholds, fields, and rules are still accurate and up-to-date
2. **Precision**: Adding specific numeric values (rates, fees, percentages) where heritage provides only qualitative descriptions
3. **Coverage**: Extending into domains where heritage data was never collected (e.g., specific bank product details)

### 8.2 Mapping of External Complementarity

| Heritage Document | External Complement | Nature of Complement | When Needed |
|-------------------|---------------------|---------------------|-------------|
| QUALIFICATION_MODEL.md §6.1 (buyer minimum fields — source_financement) | Bank mortgage criteria | Validation of field options and values | H1 phase |
| QUALIFICATION_MODEL.md §10 (escalation → Notaire for legal) | OND regulations | Precision on notaire scope | H1 phase |
| PROPERTY_MODEL.md §4 (land types — titre, loti, etc.) | MINDCAF land registry procedures | Validation of terminology and procedures | H1 phase |
| Financing matrices (FIN-COMMON-012 — taux_accepte) | BEAC rate publications | Precision on acceptable rate ranges | H2 phase |
| Professional service fields (PROF-TARIF, PROF-CERTIFICATION) | Professional orders | Validation of fee and certification norms | H2 phase |

---

## 9. Conclusion

### 9.1 Current Status

**The qualification matrices are complete without external sources.** All 107 matrices, 100+ fields, 80+ business rules, and 7 readiness levels are derived from LAWIM's internal heritage documents. The decision to not use external sources was intentional and based on:

1. Sufficient internal heritage coverage for matrix structure
2. Cameroon-specific focus preserved
3. Risk of contamination from non-Cameroonian sources avoided
4. Expert validation planned for EXPERT_PROPOSAL items

### 9.2 Recommended Actions for H1

| Action | Timeline | Responsibility |
|--------|----------|----------------|
| Establish relationships with OND (notaires) and ONGC (géomètres) for expert validation | H1 Week 1-2 | Domain Expert Lead |
| Contact 3 banks (CFC, Afriland, BICEC) for mortgage documentation requirements | H1 Week 2-4 | Domain Expert Lead |
| Define protocol for external source integration using §4 of this document | H1 Week 1 | Technical Architect |
| Begin validating financing matrices (MATRIX-FIN-001 to 005) with bank input | H1 Week 3-6 | Domain Expert Lead |
| Validate land matrices with geometre expert | H1 Week 4-8 | Domain Expert Lead |
| Integrate validated external data into matrix confidence levels | Continuous | Documentation Team |

### 9.3 Sources Not Consulted — Final Acknowledgment

This document catalogues 30+ potential external sources (government agencies, banks, professional orders, market platforms, international organizations) that have NOT been consulted. They are documented here for future reference. When external validation begins in H1, each source should be:

1. Consulted
2. Evaluated against §4.4 quality criteria
3. Documented with actual findings in §2 (moved from §3)
4. Integrated per §4.2 process

---

## 10. External Source Registry (Placeholder for H1+)

The following table is a placeholder for the registry of external sources that will be consulted during H1 and later phases. It should be populated as validation progresses.

| Source ID | Source Name | Date Consulted | Country | Platform Type | Information Used | Confidence | Status | Differences from Heritage |
|-----------|-------------|----------------|---------|---------------|-----------------|------------|--------|---------------------------|
| EXT-H1-001 | TBD | TBD | TBD | TBD | TBD | TBD | EXTERNAL_COMPLEMENT | TBD |
| EXT-H1-002 | TBD | TBD | TBD | TBD | TBD | TBD | EXTERNAL_COMPLEMENT | TBD |
| EXT-H1-003 | TBD | TBD | TBD | TBD | TBD | TBD | EXTERNAL_COMPLEMENT | TBD |

---

## 11. Detailed Rationale Per Matrix Domain

### 11.1 Why No External Sources for Residential Search Matrices

The 18 residential search matrices (chambre_simple through cite_universitaire) cover standard residential property types found in any Cameroonian city. Their qualification fields are determined by:

1. **Property type characteristics** (surface, bedrooms, bathrooms, furniture, etc.) — fully covered by heritage backup SRC-MFP-001 (minimum-fields-property.md) and SRC-PQR-001 (property-qualification-reference.md)
2. **Transaction type** (RENT, BUY) — covered by SRC-CQQ-001 (conversation-qualification-questions.md)
3. **Cameroon-specific terminology** — covered by SRC-SKU-009 (qualification_rules.md) with explicit rules about "chambres" vs "nombre de pièces"
4. **Channel adaptation** — covered by SRC-WTD-001 (whatsapp-telegram-dashboard-qualification.md)

External sources on residential property types (e.g., international property classification systems) would add no value because:
- Cameroon has unique property types (e.g., "chambre moderne", "studio moderne", "villa basse") not found in international taxonomies
- International standards use "number of rooms" which is explicitly forbidden in Cameroon
- Rental practices (caution, charges, bail) are Cameroon-specific

### 11.2 Why No External Sources for Land Search Matrices

The 7 land search matrices (terrain_titre through terrain_sous_morcellement) are deeply grounded in the Cameroonian land tenure system, which is governed by:

1. **Loi 2011-025** (Code Foncier Camerounais) — referenced indirectly through heritage documents
2. **MINDCAF procedures** — land title issuance processes documented in heritage
3. **Common law practices** — "loti/non loti", "titre collectif/individuel", "morcellement"

External sources on land systems from other African countries (e.g., Nigeria's Land Use Act, Kenya's Community Land Act) would introduce confusion because:
- Cameroon operates under a hybrid system (civil law + customary law + OHADA)
- The concept of "titre foncier" in Cameroon is unique (irrévocable, opposable aux tiers)
- Subdivision procedures ("morcellement") follow specific MINDCAF regulations

### 11.3 Why No External Sources for Commercial Property Matrices

The 21 commercial property matrices (16 property types + 5 investment types) draw on:
1. **OHADA bail commercial regulations** — referenced in SRC-03P-001
2. **Lawim's own commercial property taxonomy** — from SRC-PQR-001
3. **Investment typologies** — from SRC-SKU-003 (investor_matrices.json)

External commercial real estate standards (e.g., BOMA standards, RICS classifications) are irrelevant because:
- Cameroonian commercial property types (boutique, hangar, station_service) are market-specific
- Lease structures (bail commercial, cession de bail, bail à céder) follow OHADA, not common law
- Investment vehicles (tontine, cooperative investment, diaspora pooling) are Cameroon-specific

### 11.4 Why No External Sources for Financing Request Matrices

This is the domain where external sources would be MOST valuable (see §3.2), but EVEN HERE, the matrices were built without them because:

The matrices define **WHAT fields to collect during qualification** (e.g., "montant_recherche", "apport_personnel", "duree_remboursement"), not the specific loan terms themselves. The heritage sources (SRC-CQQ-001, SRC-QIB-001) already contain the qualification question bank for financing requests.

External sources will be needed when:
- Defining default values for loan parameters (e.g., "What is a typical interest rate?")
- Validating documentation requirements against actual bank policies
- Adding bank-specific routing rules

But these are H1 tasks, not H0.5 qualification matrix creation tasks.

### 11.5 Why No External Sources for Professional Service Matrices

The 27 professional service matrices define fields for finding professionals (notaires, géomètres, architectes, etc.). The qualification questions for "finding a notaire" are different from the notaire's fee schedule:

1. **What we need**: City, specialty, zone of intervention, reactivity — all covered by heritage
2. **What external sources could provide**: Fee schedules, certification verification, regulatory status — NOT needed for finding professionals

The distinction between "qualification for search" and "professional directory data" is critical. The matrices handle the former; external sources would support the latter.

### 11.6 Why No External Sources for Real Estate Service Matrices

The 24 real estate service matrices define qualification paths for services (estimations, expertise, visits, photography, etc.). These are service descriptions derived from:

1. **LAWIM's own service catalog** — from SRC-18Q-001 (18_QUALIFICATION_MATRIX_IMPLEMENTATION.md)
2. **Conversation qualification questions** — from SRC-CQQ-001
3. **Channel-specific service delivery rules** — from SRC-WTD-001

External sources would only be relevant if LAWIM were to expand into:
- Regulated service pricing (estimations, expertise)
- Insurance requirements for services (visits, security)
- Certification requirements for service providers

These are not currently in scope for the qualification matrices.

---

## 12. Summary Matrix of External Need

| Matrix Family | External Sources Consulted | External Sources Needed | External Sources Planned (H1) |
|---------------|---------------------------|------------------------|-------------------------------|
| Residential Search (18 matrices) | NONE | NONE | NONE |
| Land Search (7 matrices) | NONE | MINDCAF procedures | HIGH |
| Commercial Property (21 matrices) | NONE | OHADA bail commercial | MEDIUM |
| Financing Request (10 matrices) | NONE | Bank documentation | HIGH |
| Professional Service (27 matrices) | NONE | Professional orders | MEDIUM |
| Real Estate Service (24 matrices) | NONE | Regulatory bodies | LOW |
| **Total (107 matrices)** | **NONE** | **~15 external sources** | **As per §9.2** |

---

## 13. Version History and Future Updates

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-15 | Heritage Gold Team | Initial creation. No external sources consulted. Catalogued 30+ potential external sources for H1+ phases. |
| Future | H1 | TBD | Populate §10 registry with actual external sources consulted. Update §3 sources from EXTERNAL_COMPLEMENT to EXTERNAL_CONSULTED. Document any differences found. |
| Future | H2 | TBD | Full external validation of financing and legal domains. Integration of validated data into matrices with confidence level updates. |

---

**End of EXTERNAL_COMPLEMENTS.md** — For the current phase (H0.5), no external sources were consulted. This document serves as a readiness checklist for H1+ external validation. Total potential external sources identified: 30+. Integration protocol defined in §4.
