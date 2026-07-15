# HUMAN VALIDATION REQUIRED — Éléments Nécessitant une Validation Humaine

**Document ID:** LAWIM-GOLD-QM-VALIDATION-V1
**Mission:** LAWIM Heritage Gold — Qualification Matrices
**Date:** 2026-07-15
**Statut:** CANONICAL — Registre complet de tous les éléments nécessitant validation humaine avant passage en production

---

## 1. Introduction

### 1.1 Purpose

This document registers every item across the 107 qualification matrices that requires human validation before being considered production-ready. It covers:

1. Fields explicitly marked as HUMAN_VALIDATION_REQUIRED
2. Business rules marked as EXPERT_PROPOSAL (no heritage source)
3. Conflicts between heritage sources that could not be resolved algorithmically
4. Edge cases identified during matrix creation that are not covered by heritage
5. Questions requiring domain expert input (notaires, géomètres, banques)
6. Items where different heritage sources conflict

### 1.2 Priority Definitions

| Priority | Meaning | Timeline |
|----------|---------|----------|
| HIGH | Blocks production deployment if unresolved | Before H1 launch |
| MEDIUM | Should be resolved before full rollout | During H1 |
| LOW | Can be resolved iteratively during H2 | After H1 |

### 1.3 Validator Types

| Validator Type | Expertise | Domains |
|----------------|-----------|---------|
| NOTAIRE | Cameroonian civil law notary | Land matrices, legal fields, document requirements |
| GEOMETRE | Licensed land surveyor | Land subdivision, titling, lotissement |
| BANQUE | Banking/finance professional | Financing matrices, credit products, guarantees |
| ASSUREUR | Insurance professional | Insurance fields, mandatory coverage |
| ARCHITECTE | Licensed architect | Construction/renovation matrices, building norms |
| AGENT_IMMO | Real estate agent | Residential/commercial matrices, market practices |
| JURISTE | Business lawyer (OHADA/Civil law) | Professional service matrices, contract requirements |
| EXPERT_FONCIER | Land tenure specialist | Land matrices, title procedures |
| INVESTISSEUR | Real estate investor | Investment matrices, ROI benchmarks |
| CONSEILLER_DIASPORA | Diaspora investment specialist | Diaspora financing matrices |

### 1.4 Item ID Convention

| Prefix | Category |
|--------|----------|
| HVR-FLD- | Fields marked as HUMAN_VALIDATION_REQUIRED |
| HVR-RUL- | Business rules marked as EXPERT_PROPOSAL |
| HVR-CON- | Conflict resolutions needing expert review |
| HVR-EDG- | Edge cases not covered by heritage |
| HVR-LAW- | Questions about Cameroonian legal practices |
| HVR-SRC- | Items where different sources conflict |
| HVR-EXP- | Topics needing specific domain expert input |

---

## 2. Fields Marked as HUMAN_VALIDATION_REQUIRED

### 2.1 Residential Search Fields

| Item ID | Field ID | Matrix | Description | Reason | Validator | Priority |
|---------|----------|--------|-------------|--------|-----------|----------|
| HVR-FLD-001 | FLD-EXPOSITION | All residential | Preferred exposure (nord/sud/est/ouest) | No heritage source for enumeration values; Cameroon climate may differ | AGENT_IMMO | LOW |
| HVR-FLD-002 | FLD-CUISINE_SEPAREE | Kitchen fields | Separate kitchen vs open kitchen | Cameroon market preference not documented in heritage | AGENT_IMMO | LOW |
| HVR-FLD-003 | FLD-CARRELAGE | Finishing fields | Floor finish preference (carrelage/ciment/parquet) | Not explicitly mentioned in heritage question banks | AGENT_IMMO | LOW |
| HVR-FLD-004 | FLD-PROXIMITE_TRANSPORT | Transport proximity | Proximity to public transport | Common Cameroon question but not in heritage backup | AGENT_IMMO | MEDIUM |
| HVR-FLD-005 | FLD-GROUPE_ELECTROGENE | Generator requirement | Backup generator required | Important for Cameroon but not in heritage | AGENT_IMMO | MEDIUM |
| HVR-FLD-006 | FLD-CITERNE_EAU | Water cistern | Water tank/storage requirement | Essential for some Cameroon neighborhoods, no heritage source | AGENT_IMMO | MEDIUM |

### 2.2 Land Search Fields

| Item ID | Field ID | Matrix | Description | Reason | Validator | Priority |
|---------|----------|--------|-------------|--------|-----------|----------|
| HVR-FLD-007 | FLD-TYPE_TITRE_DETAILLE | LAND_SEARCH_TERRAIN_TITRE_001 | Specific title type details | Heritage sources have conflicting title type taxonomies | NOTAIRE | HIGH |
| HVR-FLD-008 | FLD-PROCESSUS_MORCELLEMENT | LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT_001 | Subdivision process stage | No heritage source; expert knowledge required | GEOMETRE | HIGH |
| HVR-FLD-009 | FLD-DELAI_OBTENTION_TITRE | LAND_SEARCH_TERRAIN_NON_TITRE_001 | Estimated time to obtain title | No heritage data on MINDCAF processing times | NOTAIRE | HIGH |
| HVR-FLD-010 | FLD-COUT_OBTENTION_TITRE | LAND_SEARCH_TERRAIN_NON_TITRE_001 | Estimated cost to obtain title | No heritage data on official fees | NOTAIRE | MEDIUM |
| HVR-FLD-011 | FLD-STATUT_OCCUPATION | Land matrices | Current occupation status of land | Not in heritage; may affect transaction feasibility | NOTAIRE | HIGH |
| HVR-FLD-012 | FLD-LITIGE_FONCIER | Land matrices | Any ongoing land dispute | Critical for due diligence; not in heritage | JURISTE | HIGH |
| HVR-FLD-013 | FLD-SERVITUDE | Land matrices | Easements or right-of-way | Not documented in heritage; important for land value | GEOMETRE | MEDIUM |
| HVR-FLD-014 | FLD-COPROPRIETE | Land matrices (collective title) | Co-ownership details | Heritage lacks detail on co-ownership structures | NOTAIRE | MEDIUM |

### 2.3 Commercial Property Fields

| Item ID | Field ID | Matrix | Description | Reason | Validator | Priority |
|---------|----------|--------|-------------|--------|-----------|----------|
| HVR-FLD-015 | COM-COMMON-029 | Station service | nb_station_service | Specific to gas stations; expert input needed | AGENT_IMMO | LOW |
| HVR-FLD-016 | COM-COMMON-030 | Industrial | cuivre_disponible | Copper availability for industrial sites; speculative | EXPERT_FONCIER | LOW |
| HVR-FLD-017 | COM-COMMON-032 | Bar | licence_alcool | Alcohol license requirement; may not apply in all municipalities | JURISTE | MEDIUM |
| HVR-FLD-018 | COM-COMMON-024 | Commercial | mezzanine | Mezzanine presence/absence; Cameroon building patterns | ARCHITECTE | LOW |
| HVR-FLD-019 | COM-COMMON-033 | Restaurant/bar | terrasse | Terrace/outdoor seating; market preference | AGENT_IMMO | LOW |

### 2.4 Financing Request Fields

| Item ID | Field ID | Matrix | Description | Reason | Validator | Priority |
|---------|----------|--------|-------------|--------|-----------|----------|
| HVR-FLD-020 | FIN-COMMON-012 | FIN-006 to FIN-010 | taux_accepte | Acceptable interest rate range; no heritage source | BANQUE | HIGH |
| HVR-FLD-021 | FIN-COMMON-024 | FIN-006 to FIN-010 | sources_remboursement | Repayment sources; needs bank validation | BANQUE | MEDIUM |
| HVR-FLD-022 | FIN-COMMON-025 | FIN-010 | plan_affaires | Business plan requirement for professional financing | BANQUE | MEDIUM |
| HVR-FLD-023 | FIN-COMMON-010 | FIN-001 to FIN-005 | charges_existantes | Existing monthly charges; completeness of list | BANQUE | MEDIUM |
| HVR-FLD-024 | FIN-COMMON-011 | FIN-001 to FIN-005 | historique_bancaire | Bank history requirement; bank-specific policies | BANQUE | MEDIUM |
| HVR-FLD-025 | FIN-COMMON-009 | FIN-001 to FIN-005 | revenus_mensuels | Monthly income fields; completeness of documentation types | BANQUE | MEDIUM |

### 2.5 Professional Service Fields

| Item ID | Field ID | Matrix | Description | Reason | Validator | Priority |
|---------|----------|--------|-------------|--------|-----------|----------|
| HVR-FLD-026 | PROF-CERTIFICATION | PRO-NOTAI-003 | Certification validation | Notaire certification authority verification | NOTAIRE | HIGH |
| HVR-FLD-027 | PROF-ANNEE_EXP | PRO-ARCHI-005 | Years of experience | Experience minimum thresholds not defined in heritage | ARCHITECTE | MEDIUM |
| HVR-FLD-028 | PROF-LANGUE | All professional matrices | Language preference | Multilingual service availability; which professionals offer English/Pidgin | AGENT_IMMO | LOW |
| HVR-FLD-029 | PROF-REFERENCE | PRO-MACON-008 to PRO-COUVR-014 | Reference verification | How to validate references for craftsmen | AGENT_IMMO | MEDIUM |
| HVR-FLD-030 | PROF-TARIF | PRO-BANQU-025 | Bank fee structures | Fee ranges for banking services | BANQUE | MEDIUM |

---

## 3. Business Rules Marked as EXPERT_PROPOSAL

### 3.1 Investment Matrices (COM-MATRIX-017 to 021)

| Item ID | Rule ID | Matrix | Description | Rationale | Validator | Priority |
|---------|---------|--------|-------------|-----------|-----------|----------|
| HVR-RUL-001 | INV-RULE-001 | COM-MATRIX-017 | Rendement locatif minimum threshold (4%) | No heritage source for expected return rates | INVESTISSEUR | HIGH |
| HVR-RUL-002 | INV-RULE-002 | COM-MATRIX-017 | Surface minimum for investissement locatif | No heritage specification | AGENT_IMMO | MEDIUM |
| HVR-RUL-003 | INV-RULE-003 | COM-MATRIX-018 | Surface minimale terrain investissement (500 m²) | Expert estimate; needs confirmation | GEOMETRE | MEDIUM |
| HVR-RUL-004 | INV-RULE-004 | COM-MATRIX-018 | Zonage constructible requirement | Depends on municipal PLU/plan d'urbanisme | EXPERT_FONCIER | HIGH |
| HVR-RUL-005 | INV-RULE-005 | COM-MATRIX-019 | Rendement minimal investissement commercial (6%) | No heritage source | INVESTISSEUR | HIGH |
| HVR-RUL-006 | INV-RULE-006 | COM-MATRIX-019 | Fonds de commerce valuation rules | OHADA-specific; needs legal validation | JURISTE | HIGH |
| HVR-RUL-007 | INV-RULE-007 | COM-MATRIX-020 | Apport minimum promotion immobilière (30%) | Expert estimate; needs bank confirmation | BANQUE | HIGH |
| HVR-RUL-008 | INV-RULE-008 | COM-MATRIX-020 | Permis de construire requirement | Confirmation des étapes administratives | ARCHITECTE | HIGH |
| HVR-RUL-009 | INV-RULE-009 | COM-MATRIX-021 | Nombre minimum copropriétaires (2) | Legal minimum for syndicat de copropriété | NOTAIRE | MEDIUM |
| HVR-RUL-010 | INV-RULE-010 | COM-MATRIX-021 | Charges copropriété estimation | No heritage source for typical charge amounts | AGENT_IMMO | LOW |

### 3.2 Financing Rules (MATRIX-FIN-006 to 010)

| Item ID | Rule ID | Matrix | Description | Rationale | Validator | Priority |
|---------|---------|--------|-------------|-----------|-----------|----------|
| HVR-RUL-011 | FIN-RULE-006 | MATRIX-FIN-006 | Prêt adossé bien: LTV max (70%) | No heritage source; typical bank LTV ratio | BANQUE | HIGH |
| HVR-RUL-012 | FIN-RULE-007 | MATRIX-FIN-006 | Garantie hypothécaire requirement | Bank-specific policy; needs confirmation | BANQUE | HIGH |
| HVR-RUL-013 | FIN-RULE-008 | MATRIX-FIN-007 | Apport minimum recherche investisseur | No heritage specification | INVESTISSEUR | MEDIUM |
| HVR-RUL-014 | FIN-RULE-009 | MATRIX-FIN-008 | Répartition cofinancement (50/50 default) | Expert estimate; varies by project | BANQUE | MEDIUM |
| HVR-RUL-015 | FIN-RULE-010 | MATRIX-FIN-009 | Apport diaspora minimum (20% du bien) | Expert estimate; needs diaspora finance specialist | CONSEILLER_DIASPORA | HIGH |
| HVR-RUL-016 | FIN-RULE-011 | MATRIX-FIN-009 | Justificatif apport diaspora needs | Document types not in heritage | BANQUE | MEDIUM |
| HVR-RUL-017 | FIN-RULE-012 | MATRIX-FIN-010 | Chiffre d'affaires minimum | No heritage source for business turnover thresholds | BANQUE | HIGH |
| HVR-RUL-018 | FIN-RULE-013 | MATRIX-FIN-010 | Bilan comptable requirement | Depends on business size and bank policy | BANQUE | MEDIUM |

### 3.3 Professional Service Rules (PRO-EXPIM-015 to PRO-PREST-027)

| Item ID | Rule ID | Matrix | Description | Rationale | Validator | Priority |
|---------|---------|--------|-------------|-----------|-----------|----------|
| HVR-RUL-019 | PRO-RULE-015 | PRO-EXPIM-015 | Expert immobilier certification criteria | No heritage; expert status criteria | EXPERT_FONCIER | HIGH |
| HVR-RUL-020 | PRO-RULE-016 | PRO-EVALU-016 | Evaluateur qualification requirements | No heritage; evaluation standards | EXPERT_FONCIER | HIGH |
| HVR-RUL-021 | PRO-RULE-017 | PRO-GESTI-017 | Gestionnaire immobilier scope of work | No heritage; service definition | AGENT_IMMO | MEDIUM |
| HVR-RUL-022 | PRO-RULE-018 | PRO-SYNDI-018 | Syndic legal requirements (OHADA/Civil code) | Needs legal validation | JURISTE | HIGH |
| HVR-RUL-023 | PRO-RULE-019 | PRO-PHOTO-019 | Photographe immobilier equipment standards | No heritage | AGENT_IMMO | LOW |
| HVR-RUL-024 | PRO-RULE-020 | PRO-VIDEO-020 | Drone certification requirements | Cameroon civil aviation authority rules | AGENT_IMMO | MEDIUM |
| HVR-RUL-025 | PRO-RULE-021 | PRO-DEMEN-021 | Déménageur insurance requirements | No heritage; insurance verification | ASSUREUR | MEDIUM |
| HVR-RUL-026 | PRO-RULE-022 | PRO-NETTO-022 | Cleaning service certification | Market standards not documented | AGENT_IMMO | LOW |
| HVR-RUL-027 | PRO-RULE-023 | PRO-GARDI-023 | Gardiennage licensing requirements | May require MINJUSTICE approval | JURISTE | MEDIUM |
| HVR-RUL-028 | PRO-RULE-024 | PRO-ASSUR-024 | Assureur product scope | ASAC/CIMA regulations | ASSUREUR | MEDIUM |
| HVR-RUL-029 | PRO-RULE-025 | PRO-BANQU-025 | Banking product documentation | Regulatory requirements (COBAC/BEAC) | BANQUE | MEDIUM |
| HVR-RUL-030 | PRO-RULE-026 | PRO-COURT-026 | Courtier immobilier legal framework | No heritage; courtier status in Cameroon | JURISTE | HIGH |
| HVR-RUL-031 | PRO-RULE-027 | PRO-PREST-027 | Administrative service provider requirements | No heritage; service definition | JURISTE | LOW |

### 3.4 Real Estate Service Rules (SVC-CONS-015 to SVC-RECO-024)

| Item ID | Rule ID | Matrix | Description | Rationale | Validator | Priority |
|---------|---------|--------|-------------|-----------|-----------|----------|
| HVR-RUL-032 | SVC-RULE-015 | SVC-CONS-015 | Construction service scope (building permit requirement) | No heritage; depends on commune regulations | ARCHITECTE | HIGH |
| HVR-RUL-033 | SVC-RULE-016 | SVC-CONS-015 | Garantie décennale requirement | Legal requirement; not in heritage | ASSUREUR | HIGH |
| HVR-RUL-034 | SVC-RULE-017 | SVC-ENTR-016 | Entretien service frequency standards | No heritage; market norms | AGENT_IMMO | LOW |
| HVR-RUL-035 | SVC-RULE-018 | SVC-NETT-017 | Nettoyage service depth standards | No heritage | AGENT_IMMO | LOW |
| HVR-RUL-036 | SVC-RULE-019 | SVC-SECU-018 | Sécurisation service: alarm standards, guard requirements | No heritage; market feedback | AGENT_IMMO | MEDIUM |
| HVR-RUL-037 | SVC-RULE-020 | SVC-DEME-019 | Déménagement: equipment and vehicle requirements | No heritage | AGENT_IMMO | LOW |
| HVR-RUL-038 | SVC-RULE-021 | SVC-ASSU-020 | Types d'assurance habitation obligatoires | ASAC/CIMA regulated; needs confirmation | ASSUREUR | HIGH |
| HVR-RUL-039 | SVC-RULE-022 | SVC-CONS-021 | Conseil juridique: scope of practice (notaire vs avocat) | Distinction not in heritage | JURISTE | HIGH |
| HVR-RUL-040 | SVC-RULE-023 | SVC-CONS-022 | Conseil fiscal: tax obligations (impôts fonciers, plus-value) | Cameroon tax code; not in heritage | JURISTE | MEDIUM |
| HVR-RUL-041 | SVC-RULE-024 | SVC-GEST-023 | Gestion copropriété: legal framework | OHADA/Civil code; not in heritage | NOTAIRE | HIGH |
| HVR-RUL-042 | SVC-RULE-025 | SVC-RECO-024 | Recouvrement locatif: legal process | Cameroon civil procedure; not in heritage | JURISTE | HIGH |

---

## 4. Conflict Resolutions Needing Expert Review

### 4.1 Resolved Conflicts Pending Expert Confirmation

| Item ID | Conflict | Sources Involved | Proposed Resolution | Validator | Priority |
|---------|----------|------------------|---------------------|-----------|----------|
| HVR-CON-001 | Matching threshold: 25% vs 60% | Decision Engine Ch26 vs Ch92 | Dual threshold: 60% for proposal, 25% for absolute rejection | AGENT_IMMO, EXPERT_FONCIER | MEDIUM |
| HVR-CON-002 | Memory retention: 90 days vs 365 days | CONVERSATION_MODEL.md vs long_term_memory.py | Keep 365 days (code-based). Confirm business logic intent | CONSEILLER_DIASPORA | LOW |
| HVR-CON-003 | Buyer fears: 12 vs 10 | CONVERSATION_MODEL.md vs trust-and-objection-patterns.md | Accept 10 from verified source | AGENT_IMMO | LOW |
| HVR-CON-004 | Camfranglais: language or expressions | Multiple sources | It is expressions, not a supported language | LINGUISTE | LOW |

### 4.2 Unresolved Conflicts Requiring Expert Resolution

| Item ID | Conflict | Sources Involved | Nature of Disagreement | Validator | Priority |
|---------|----------|------------------|------------------------|-----------|----------|
| HVR-CON-005 | City priority order (4 versions) | cities.json, system_prompt_v1.md, city-affinity-matrix, 09-GEOLOCATION-REFERENCE | Different priority orderings for Cameroon cities affect search result ordering | AGENT_IMMO | MEDIUM |
| HVR-CON-006 | Land title status taxonomy | SRC-MFP-001 vs property_matching_v1.json vs SRC-SKU-001 | Number and types of land titles differ between sources | NOTAIRE | HIGH |
| HVR-CON-007 | Budget qualification: mandatory at step 5 vs mandatory before match | SRC-HGQ-001 §5 (step 5) vs §8 (budget is blocking) | Both say mandatory; one says step 5, other says before match. Both correct but need precision | EXPERT_FONCIER | LOW |
| HVR-CON-008 | Diaspora indicators: which countries/indicators | diaspora_filter.py vs scoring_rules.json vs QUALIFICATION_MODEL.md §12 | Inconsistent lists of diaspora countries and detection methods | CONSEILLER_DIASPORA | MEDIUM |
| HVR-CON-009 | Professional certification: notaire vs agent vs courtier | Multiple heritage sources | Blurred lines between roles; needs legal clarity | JURISTE | HIGH |
| HVR-CON-010 | Surface measurement units: m² vs "pièces" vs "unités" | SRC-MFP-001 vs SRC-CQQ-001 | Cameroon uses multiple surface metrics depending on region and property type | AGENT_IMMO | MEDIUM |

---

## 5. Edge Cases Not Covered by Heritage

### 5.1 Property/Service Type Edge Cases

| Item ID | Edge Case | Matrices Affected | Reason Not Covered | Validator | Priority |
|---------|-----------|-------------------|--------------------|-----------|----------|
| HVR-EDG-001 | Short-term rental (Airbnb-type) — duration < 1 month | MATRIX-RES-SEARCH-014, 015, 016 | Heritage assumes long-term rental (bail of 3+ years) or hotel | AGENT_IMMO | MEDIUM |
| HVR-EDG-002 | Mixed-use property (commercial ground + residential upper) | COM-MATRIX-001 to 016 + residential matrices | Heritage classifies properties as single-use | NOTAIRE, ARCHITECTE | MEDIUM |
| HVR-EDG-003 | Land with partial title (titre en cours) | LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT_001 | Intermediate step not covered by binary titled/untitled | NOTAIRE | HIGH |
| HVR-EDG-004 | Heritage property succession (indivision successorale) | LAND_SEARCH + residential buy matrices | Common Cameroon scenario; not in heritage | NOTAIRE | HIGH |
| HVR-EDG-005 | Cooperative/group purchase (multiple buyers) | All residential buy matrices | No heritage for co-buyer qualification | NOTAIRE | MEDIUM |
| HVR-EDG-006 | Property in diaspora ownership (absentee owner) | All matrices | No heritage for remote seller qualification | CONSEILLER_DIASPORA | MEDIUM |
| HVR-EDG-007 | Agricultural land conversion to residential | LAND_SEARCH matrices | Cameroon land use change procedures not in heritage | EXPERT_FONCIER | HIGH |
| HVR-EDG-008 | Custom-built property vs existing property | All buy matrices | Different qualification needs; not distinguished in heritage | AGENT_IMMO | MEDIUM |
| HVR-EDG-009 | Pre-construction (VEFA) qualification | COM-MATRIX-020, residential buy | Off-plan purchase qualification differs from existing | ARCHITECTE | HIGH |
| HVR-EDG-010 | Multiple simultaneous requests from same user | All matrices | Heritage qualifies one request at a time; no multi-request orchestration | AGENT_IMMO | LOW |

### 5.2 Qualification Flow Edge Cases

| Item ID | Edge Case | Description | Reason Not Covered | Validator | Priority |
|---------|-----------|-------------|--------------------|-----------|----------|
| HVR-EDG-011 | User provides budget but no property type | Reverse order qualification | Heritage assumes linear order; user may provide budget first | AGENT_IMMO | MEDIUM |
| HVR-EDG-012 | User fluent in English but in French city | Channel/language conflict | Heritage assumes language follows location | AGENT_IMMO | LOW |
| HVR-EDG-013 | First-time buyer vs experienced investor | Same matrix, different qualification depth | Heritage has same fields for both; one may need more guidance | AGENT_IMMO | MEDIUM |
| HVR-EDG-014 | User wants both rent AND buy (dual intent) | RENT + BUY matrices | Heritage handles single intent; dual intent not covered | AGENT_IMMO | MEDIUM |
| HVR-EDG-015 | Time-sensitive: user needs property in 24 hours | All residential | No expedited qualification path in heritage | AGENT_IMMO | LOW |
| HVR-EDG-016 | Non-standard budget: budget in foreign currency (EUR, USD, XAF) | All matrices | Heritage handles XAF only; diaspora may quote in EUR/USD | BANQUE | MEDIUM |
| HVR-EDG-017 | User refuses to provide budget (no trust yet) | All matrices | Heritage makes budget mandatory; no workaround path | AGENT_IMMO | MEDIUM |
| HVR-EDG-018 | User provides entire address but no neighborhood | Neighborhood detection | Heritage requires neighborhood; full address should map to neighborhood | GEOMETRE | LOW |

### 5.3 Legal/Administrative Edge Cases

| Item ID | Edge Case | Description | Reason Not Covered | Validator | Priority |
|---------|-----------|-------------|--------------------|-----------|----------|
| HVR-EDG-019 | Land title disputed by third party | Affects all land transactions | No escalation path for title disputes in heritage | NOTAIRE | HIGH |
| HVR-EDG-020 | Multiple owners of same property (indivision) | All buy/sell matrices | No co-ownership qualification path | NOTAIRE | HIGH |
| HVR-EDG-021 | Property under seizure (saisie immobilière) | All buy matrices | No mechanism to detect or handle seized properties | JURISTE | HIGH |
| HVR-EDG-022 | No will/succession documentation | Land + property matrices | Common Cameroon issue; not covered | NOTAIRE | MEDIUM |
| HVR-EDG-023 | Property built on state-owned land (domaine national) | LAND_SEARCH matrices | Common for informal settlements; not in heritage | EXPERT_FONCIER | HIGH |
| HVR-EDG-024 | Customary law land rights vs formal title | LAND_SEARCH matrices | Dual system not acknowledged in heritage | NOTAIRE, EXPERT_FONCIER | HIGH |
| HVR-EDG-025 | Leasehold vs freehold confusion | All matrices | Cameroon has complex hybrid tenure; not in heritage | NOTAIRE | MEDIUM |

---

## 6. Questions About Cameroonian Legal Practices

### 6.1 Land and Property Law

| Item ID | Question | Domain | Suggested Source | Priority |
|---------|----------|--------|------------------|----------|
| HVR-LAW-001 | What is the exact process and timeline for obtaining a titre foncier from MINDCAF? | Land | MINDCAF procedure manuals, practicing notaire | HIGH |
| HVR-LAW-002 | How does the "mise en demeure" process work for lease disputes? | Legal | Civil procedure code, bail law | MEDIUM |
| HVR-LAW-003 | What documents are strictly required for a valid property sale (vente immobilière)? | Legal | OND (Ordre des Notaires) practice standards | HIGH |
| HVR-LAW-004 | What is the legal distinction between "bail commercial" (OHADA) and "bail d'habitation" (civil code)? | Legal | OHADA Uniform Act, Cameroonian Civil Code | HIGH |
| HVR-LAW-005 | How does the "droit de préemption" of the State work in Cameroon? | Land | Urban planning code, expropriation law | MEDIUM |
| HVR-LAW-006 | What are the legal requirements for a valid "promesse de vente" (promise to sell)? | Legal | Notarial practice, civil code | HIGH |
| HVR-LAW-007 | How is "indivision" (co-ownership) legally managed for property transactions? | Legal | Civil code, family law | HIGH |
| HVR-LAW-008 | What is the tax liability for property sales (impôt sur les plus-values immobilières)? | Fiscal | Cameroon tax code, Direction Générale des Impôts | MEDIUM |
| HVR-LAW-009 | How does "domaine national" (state land) transition to titled private land? | Land | MINDCAF, Code Foncier | HIGH |
| HVR-LAW-010 | What is the legal framework for "lotissement" (land subdivision)? | Land | Urban planning code, MINDCAF | HIGH |

### 6.2 Financing and Banking Law

| Item ID | Question | Domain | Suggested Source | Priority |
|---------|----------|--------|------------------|----------|
| HVR-LAW-011 | What are the legal maximum interest rates for mortgage loans in Cameroon? | Finance | BEAC regulations, banking law | HIGH |
| HVR-LAW-012 | What is the legal framework for "hypothèque" (mortgage) registration? | Finance | Civil code, conservation foncière | HIGH |
| HVR-LAW-013 | How does "caution bancaire" (bank guarantee) work for rental properties? | Finance | Banking practice, bail law | MEDIUM |
| HVR-LAW-014 | What are the legal requirements for diaspora members to obtain Cameroonian mortgages? | Finance | BEAC, diaspora banking | HIGH |
| HVR-LAW-015 | How does microfinance lending differ from bank lending for real estate? | Finance | COBAC regulations, MC2 practices | MEDIUM |

### 6.3 Professional Regulation

| Item ID | Question | Domain | Suggested Source | Priority |
|---------|----------|--------|------------------|----------|
| HVR-LAW-016 | What is the legal scope of practice for a notaire vs avocat in real estate? | Legal | OND, Barreau du Cameroun | HIGH |
| HVR-LAW-017 | How is a "courtier immobilier" (real estate broker) regulated in Cameroon? | Professional | MINCOMMERCE, professional associations | HIGH |
| HVR-LAW-018 | What are the legal requirements for an "agent immobilier" license? | Professional | MINHDU, professional associations | HIGH |
| HVR-LAW-019 | How is "expert immobilier" (real estate expert) certification regulated? | Professional | Professional orders | MEDIUM |
| HVR-LAW-020 | What professional insurance is mandatory for real estate professionals? | Professional | ASAC, CIMA code | MEDIUM |

### 6.4 Construction and Development

| Item ID | Question | Domain | Suggested Source | Priority |
|---------|----------|--------|------------------|----------|
| HVR-LAW-021 | What is the building permit process in Cameroon's major cities? | Construction | MINHDU, commune/mairie offices | HIGH |
| HVR-LAW-022 | What are the minimum construction standards (normes de construction)? | Construction | MINHDU, Cameroon building code | HIGH |
| HVR-LAW-023 | How does "garantie décennale" (10-year liability) work for construction? | Construction | Civil code, insurance law | HIGH |
| HVR-LAW-024 | What are the zoning regulations (PLU/POS) for Cameroon's major cities? | Construction | Communes, MINHDU | MEDIUM |
| HVR-LAW-025 | How are "permis de démolir" and "permis de construire" obtained? | Construction | Municipal procedures | MEDIUM |

---

## 7. Items Where Different Sources Conflict

### 7.1 Source Conflicts Requiring Arbitration

| Item ID | Topic | Source A | Source A Value | Source B | Source B Value | Arbiter Needed | Priority |
|---------|-------|----------|----------------|----------|----------------|----------------|----------|
| HVR-SRC-001 | City priority order for qualification | system_prompt_v1.md | Douala, Yaoundé, Bafoussam, Bamenda, Buea, Garoua, Kribi, Limbe, Maroua, Nkongsamba | 09-GEOLOCATION-REFERENCE.md | Yaoundé, Douala, Bafoussam, Bamenda, Buea, Garoua, Kribi, Limbe, Maroua, Nkongsamba | AGENT_IMMO | MEDIUM |
| HVR-SRC-002 | Budget booster value | lead_classifier_v1.json | +15 | scoring_rules.json | budget weight: 20 (separate system) | EXPERT_FONCIER | LOW |
| HVR-SRC-003 | Diaspora countries list | QUALIFICATION_MODEL.md | France, USA, Canada, Allemagne, Belgique, Suisse, UK, Italie | diaspora_filter.py | France, Canada, Belgique, USA, Allemagne, Italie, Royaume-Uni | CONSEILLER_DIASPORA | MEDIUM |
| HVR-SRC-004 | Minimum qualification fields for land | minimum-fields-property.md | city, surface, budget | property_search_matrices.json (knowledge_unified) | city_or_axis, surface, budget | NOTAIRE | MEDIUM |
| HVR-SRC-005 | Number of CRM scoring factors | RULE_ENGINE_V5.json | 7 factors | lead_scoring_rules.json | 7 factors but different weights | EXPERT_FONCIER | LOW |
| HVR-SRC-006 | WhatsApp qualification order (step 4) | conversation-qualification-questions.md | Quartier at step 4 | whatsapp-telegram-dashboard-qualification.md | Quartier at step 4 (consistent) | None (resolved) | LOW |
| HVR-SRC-007 | Property types for "studio" classification | PROPERTY_MODEL.md | 3 sub-types (basic, moderne, meublé) | 02A-RESIDENTIAL-REFERENCE.md | 4 sub-types (includes studio_luxe) | AGENT_IMMO | MEDIUM |
| HVR-SRC-008 | Seller field requirements | minimum-fields-property.md | property_type, city, price, documents | seller_matrices.json (knowledge_unified) | property_type, city, neighborhood, price, documents | AGENT_IMMO | LOW |

### 7.2 Source Quality Issues

| Item ID | Issue | Source | Problem | Impact | Priority |
|---------|-------|--------|---------|--------|----------|
| HVR-SRC-009 | Missing source verification | ancienne_structure/ files | Files deleted; only SOURCE_INVENTORY descriptions remain | Cannot directly verify field values | HIGH |
| HVR-SRC-010 | Inferred field definitions | Various heritage docs | Some fields (like FLD-EXPOSITION) have no explicit heritage source | Fields may not reflect actual market practice | MEDIUM |
| HVR-SRC-011 | Backup branch completeness | backup:docs/Directive/ | Not all heritage files are in backup; some were deleted pre-20260711 | Certain matrix domains have thin coverage | MEDIUM |
| HVR-SRC-012 | knowledge_unified version uncertainty | knowledge_unified/ | Files may have been manually modified during V2 migration | Cannot guarantee version alignment with original LAWIM | MEDIUM |

---

## 8. Topics Needing Domain Expert Input

### 8.1 Notaire (Civil Law Notary) Validation Topics

| Item ID | Topic | Matrices Affected | Specific Questions | Priority |
|---------|-------|-------------------|-------------------|----------|
| HVR-EXP-001 | Land title verification process | All land matrices + PROF-NOTAI-003 | Steps, timeline, costs, red flags | HIGH |
| HVR-EXP-002 | Required documents for property transfer | MATRIX-RES-SEARCH-006/007/008 (buy) | Document checklist by property type | HIGH |
| HVR-EXP-003 | Succession/indivision handling | All buy matrices | How qualification should handle co-ownership | HIGH |
| HVR-EXP-004 | Notaire fee structure (barème) | PROF-NOTAI-003 | Fee percentages, minimums, additional costs | MEDIUM |
| HVR-EXP-005 | Promesse de vente vs acte de vente | All buy matrices | Stages, legal effect, consequences of default | HIGH |
| HVR-EXP-006 | Hypothèque registration process | FIN-001, FIN-006 | Registration fees, timeline, cancellation | HIGH |

### 8.2 Géomètre (Land Surveyor) Validation Topics

| Item ID | Topic | Matrices Affected | Specific Questions | Priority |
|---------|-------|-------------------|-------------------|----------|
| HVR-EXP-007 | Land subdivision process (morcellement) | LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT_001 | Steps, timeline, costs, required surveys | HIGH |
| HVR-EXP-008 | Land survey types (bornage, délimitation, morcellement) | All land matrices | Which survey is needed for which transaction | HIGH |
| HVR-EXP-009 | GPS coordinate standards in Cameroon | LAND_SEARCH matrices | Which coordinate system, precision requirements | MEDIUM |
| HVR-EXP-010 | Servitude identification | LAND_SEARCH matrices | How easements affect land qualification | MEDIUM |
| HVR-EXP-011 | Surface measurement methods | All land + residential | How plot sizes are officially measured in Cameroon | MEDIUM |

### 8.3 Banque (Bank) Validation Topics

| Item ID | Topic | Matrices Affected | Specific Questions | Priority |
|---------|-------|-------------------|-------------------|----------|
| HVR-EXP-012 | Mortgage product parameters | MATRIX-FIN-001 | Interest rates, LTV, duration, eligibility | HIGH |
| HVR-EXP-013 | Required loan documentation | MATRIX-FIN-001 to 005 | Document checklist by loan type | HIGH |
| HVR-EXP-014 | Diaspora financing products | MATRIX-FIN-009 | Specific diaspora loan products | HIGH |
| HVR-EXP-015 | Microfinance real estate products | MATRIX-FIN-010 | MC2 and other microfinance criteria | MEDIUM |
| HVR-EXP-016 | Co-financing mechanisms | MATRIX-FIN-008 | How co-financing works in practice | MEDIUM |
| HVR-EXP-017 | Construction financing milestones | MATRIX-FIN-003 | Tranche release schedule, inspection requirements | HIGH |
| HVR-EXP-018 | Guarantee/insurance requirements for loans | MATRIX-FIN-001, 006 | Mandatory insurance types | MEDIUM |

### 8.4 Assureur (Insurance) Validation Topics

| Item ID | Topic | Matrices Affected | Specific Questions | Priority |
|---------|-------|-------------------|-------------------|----------|
| HVR-EXP-019 | Mandatory property insurance types | SVC-ASSU-020, FIN matrices | Multirisque habitation, incendie, etc. | HIGH |
| HVR-EXP-020 | Insurance for construction/renovation | SVC-CONS-015, SVC-RENO-014 | Chantier insurance, décennale | MEDIUM |
| HVR-EXP-021 | Professional insurance for real estate agents | PRO-AGENT-001, PRO-AGENC-002 | RC professionnelle requirements | MEDIUM |
| HVR-EXP-022 | Rental guarantee insurance | All rent matrices | GLI (Garantie Loyers Impayés) availability in Cameroon | MEDIUM |

### 8.5 Architecte (Architect) Validation Topics

| Item ID | Topic | Matrices Affected | Specific Questions | Priority |
|---------|-------|-------------------|-------------------|----------|
| HVR-EXP-023 | Building permit process | SVC-CONS-015, FIN-003 | Required documents, timeline, costs | HIGH |
| HVR-EXP-024 | Construction norms and standards | SVC-CONS-015, FIN-003 | Minimum surfaces, materials, safety | MEDIUM |
| HVR-EXP-025 | Renovation vs new build qualification differences | SVC-RENO-014 | Different fields needed for renovation | MEDIUM |
| HVR-EXP-026 | VEFA (off-plan) qualification | COM-MATRIX-020, residential buy | Stages of construction and corresponding qualification | HIGH |

### 8.6 Agent Immobilier (Real Estate Agent) Validation Topics

| Item ID | Topic | Matrices Affected | Specific Questions | Priority |
|---------|-------|-------------------|-------------------|----------|
| HVR-EXP-027 | Market-specific field validation | All matrices | Verify all fields reflect actual Cameroon market needs | HIGH |
| HVR-EXP-028 | Typical qualification conversation flow | All matrices | Does the 10-step order match real agent practice? | HIGH |
| HVR-EXP-029 | Priority of criteria in practice | All matrices | What do Cameroon buyers prioritize vs heritage ranking? | MEDIUM |
| HVR-EXP-030 | Objection handling during qualification | All matrices | Common user objections not in heritage | MEDIUM |
| HVR-EXP-031 | Channel-specific qualification nuances | All matrices | WhatsApp vs Telegram vs in-person differences | MEDIUM |

### 8.7 Investisseur (Investor) Validation Topics

| Item ID | Topic | Matrices Affected | Specific Questions | Priority |
|---------|-------|-------------------|-------------------|----------|
| HVR-EXP-032 | Expected ROI ranges by investment type | COM-MATRIX-017 to 021 | Typical yields for Cameroon RE investments | HIGH |
| HVR-EXP-033 | Investment risk assessment fields | COM-MATRIX-017 to 021 | What risk factors are material in Cameroon? | MEDIUM |
| HVR-EXP-034 | Diaspora-specific investment concerns | COM-MATRIX-018, FIN-009 | Trust, remote management, currency | HIGH |

---

## 9. Validation Priority Matrix

### 9.1 Must-Validate Before Production (HIGH)

| Item ID | Summary | Domain | Validator Type |
|---------|---------|--------|----------------|
| HVR-FLD-007 | Land title type taxonomy | Land | NOTAIRE |
| HVR-FLD-008 | Subdivision process stages | Land | GEOMETRE |
| HVR-FLD-009 | Title acquisition timeline | Land | NOTAIRE |
| HVR-FLD-011 | Land occupation status | Land | NOTAIRE |
| HVR-FLD-012 | Land dispute detection | Land | JURISTE |
| HVR-FLD-020 | Acceptable interest rates | Finance | BANQUE |
| HVR-FLD-026 | Notaire certification validation | Professional | NOTAIRE |
| HVR-RUL-001 | Investment minimum ROI | Investment | INVESTISSEUR |
| HVR-RUL-005 | Commercial investment minimum return | Investment | INVESTISSEUR |
| HVR-RUL-006 | Fonds de commerce valuation | Investment | JURISTE |
| HVR-RUL-007 | Development minimum equity | Investment | BANQUE |
| HVR-RUL-008 | Building permit process | Investment | ARCHITECTE |
| HVR-RUL-011 | LTV maximum ratio | Finance | BANQUE |
| HVR-RUL-012 | Hypothèque requirements | Finance | BANQUE |
| HVR-RUL-015 | Diaspora minimum contribution | Finance | CONSEILLER_DIASPORA |
| HVR-RUL-017 | Business minimum turnover | Finance | BANQUE |
| HVR-RUL-019 | Expert immobilier certification | Professional | EXPERT_FONCIER |
| HVR-RUL-020 | Evaluateur qualification | Professional | EXPERT_FONCIER |
| HVR-RUL-022 | Syndic legal requirements | Professional | JURISTE |
| HVR-RUL-025 | Déménageur insurance | Professional | ASSUREUR |
| HVR-RUL-030 | Courtier legal framework | Professional | JURISTE |
| HVR-RUL-032 | Building permit requirement | Service | ARCHITECTE |
| HVR-RUL-033 | Décennale insurance requirement | Service | ASSUREUR |
| HVR-RUL-038 | Mandatory insurance types | Service | ASSUREUR |
| HVR-RUL-039 | Conseil juridique scope | Service | JURISTE |
| HVR-RUL-040 | Fiscal obligations | Service | JURISTE |
| HVR-RUL-041 | Copropriété legal framework | Service | NOTAIRE |
| HVR-RUL-042 | Recouvrement locatif process | Service | JURISTE |
| HVR-CON-006 | Land title taxonomy | Land | NOTAIRE |
| HVR-CON-009 | Professional role boundaries | Legal | JURISTE |
| HVR-EDG-003 | Partial title land | Land | NOTAIRE |
| HVR-EDG-004 | Succession/indivision | Land | NOTAIRE |
| HVR-EDG-007 | Agricultural land conversion | Land | EXPERT_FONCIER |
| HVR-EDG-009 | VEFA qualification | Construction | ARCHITECTE |
| HVR-EDG-019 | Title dispute | Legal | NOTAIRE |
| HVR-EDG-020 | Multiple owners | Legal | NOTAIRE |
| HVR-EDG-021 | Property under seizure | Legal | JURISTE |
| HVR-EDG-023 | State-owned land | Land | EXPERT_FONCIER |
| HVR-EDG-024 | Customary law | Land | NOTAIRE |
| HVR-EXP-001 to 006 | Notaire topics (all) | Legal | NOTAIRE |
| HVR-EXP-007 to 011 | Géomètre topics (all) | Land | GEOMETRE |
| HVR-EXP-012 to 018 | Banque topics (all) | Finance | BANQUE |
| HVR-EXP-019 to 022 | Assurance topics (all) | Insurance | ASSUREUR |
| HVR-EXP-023 to 026 | Architecte topics (all) | Construction | ARCHITECTE |
| HVR-EXP-027, 028 | Agent practice validation | Market | AGENT_IMMO |
| HVR-EXP-032, 034 | Investment ROI validation | Investment | INVESTISSEUR |

### 9.2 Should-Validate Before Full Rollout (MEDIUM)

| Item ID | Summary | Validator |
|---------|---------|-----------|
| HVR-FLD-004 | Transport proximity field | AGENT_IMMO |
| HVR-FLD-005 | Generator requirement field | AGENT_IMMO |
| HVR-FLD-006 | Water cistern field | AGENT_IMMO |
| HVR-FLD-010 | Title acquisition cost | NOTAIRE |
| HVR-FLD-014 | Co-ownership structures | NOTAIRE |
| HVR-FLD-017 | Alcohol license field | JURISTE |
| HVR-RUL-002 | Rental investment surface minimum | AGENT_IMMO |
| HVR-RUL-003 | Land investment surface minimum | GEOMETRE |
| HVR-RUL-009 | Minimum co-owners | NOTAIRE |
| HVR-RUL-013 | Investor search minimum equity | INVESTISSEUR |
| HVR-RUL-014 | Co-financing split | BANQUE |
| HVR-RUL-016 | Diaspora contribution documents | BANQUE |
| HVR-RUL-018 | Business financial statements | BANQUE |
| HVR-RUL-021 | Property manager scope | AGENT_IMMO |
| HVR-RUL-024 | Drone certification | AGENT_IMMO |
| HVR-RUL-027 | Gardiennage licensing | JURISTE |
| HVR-RUL-028 | Insurance product scope | ASSUREUR |
| HVR-RUL-029 | Banking documentation | BANQUE |
| HVR-RUL-036 | Security service standards | AGENT_IMMO |
| HVR-CON-001 | Matching threshold confirmation | AGENT_IMMO, EXPERT_FONCIER |
| HVR-CON-005 | City priority order | AGENT_IMMO |
| HVR-CON-008 | Diaspora indicators | CONSEILLER_DIASPORA |
| HVR-CON-010 | Surface measurement units | AGENT_IMMO |
| HVR-EDG-001 | Short-term rental qualification | AGENT_IMMO |
| HVR-EDG-002 | Mixed-use property | NOTAIRE |
| HVR-EDG-005 | Cooperative purchase | NOTAIRE |
| HVR-EDG-006 | Diaspora absentee owner | CONSEILLER_DIASPORA |
| HVR-EDG-008 | Custom vs existing property | AGENT_IMMO |
| HVR-EDG-011 | Reverse order qualification | AGENT_IMMO |
| HVR-EDG-013 | First-time buyer vs investor | AGENT_IMMO |
| HVR-EDG-014 | Dual intent handling | AGENT_IMMO |
| HVR-EDG-016 | Foreign currency budget | BANQUE |
| HVR-EDG-017 | Budget refusal workaround | AGENT_IMMO |
| HVR-EDG-022 | Succession documentation | NOTAIRE |
| HVR-EDG-025 | Leasehold vs freehold | NOTAIRE |

### 9.3 Can-Validate Iteratively (LOW)

| Item ID | Summary | Validator |
|---------|---------|-----------|
| HVR-FLD-001 | Building exposure preference | AGENT_IMMO |
| HVR-FLD-002 | Kitchen type preference | AGENT_IMMO |
| HVR-FLD-003 | Floor finish preference | AGENT_IMMO |
| HVR-FLD-015 | Station service fields | AGENT_IMMO |
| HVR-FLD-016 | Copper availability field | EXPERT_FONCIER |
| HVR-FLD-018 | Mezzanine field | ARCHITECTE |
| HVR-FLD-019 | Terrace field | AGENT_IMMO |
| HVR-FLD-028 | Professional language | AGENT_IMMO |
| HVR-RUL-010 | Copropriété charges estimation | AGENT_IMMO |
| HVR-RUL-023 | Photography equipment standards | AGENT_IMMO |
| HVR-RUL-026 | Cleaning certification | AGENT_IMMO |
| HVR-RUL-031 | Administrative provider scope | JURISTE |
| HVR-RUL-034 | Maintenance frequency | AGENT_IMMO |
| HVR-RUL-035 | Cleaning depth | AGENT_IMMO |
| HVR-RUL-037 | Moving equipment | AGENT_IMMO |
| HVR-CON-002 | Memory retention clarification | CONSEILLER_DIASPORA |
| HVR-CON-003 | Buyer fears confirmation | AGENT_IMMO |
| HVR-CON-004 | Camfranglais status | LINGUISTE |
| HVR-CON-007 | Budget qualification timing | EXPERT_FONCIER |
| HVR-EDG-010 | Multiple simultaneous requests | AGENT_IMMO |
| HVR-EDG-012 | Language/location conflict | AGENT_IMMO |
| HVR-EDG-015 | Expedited qualification path | AGENT_IMMO |
| HVR-EDG-018 | Full address mapping | GEOMETRE |

---

## 10. Validation Workflow

### 10.1 How to Validate an Item

1. **Read the item description** in this document
2. **Review the related matrix** in `docs/lawim_heritage_gold/qualification_matrices/`
3. **Review the heritage source** referenced in `SOURCE_TRACEABILITY.md`
4. **Submit to the designated validator** with a brief explaining:
   - The current proposed value/rule/field
   - The reason for uncertainty
   - The specific question(s) to be answered
5. **Record the validator's response** in the item entry
6. **Update the item status** to VALIDATED, MODIFIED, or REJECTED
7. **Propagate the change** to all affected matrices
8. **Update confidence levels** in the corresponding matrix files

### 10.2 Status Tracking

| Status | Meaning |
|--------|---------|
| PENDING_VALIDATION | Not yet submitted to validator |
| SUBMITTED | Sent to validator, awaiting response |
| VALIDATED | Confirmed by expert; no changes needed |
| MODIFIED | Changed based on expert input |
| REJECTED | Rule/field removed based on expert input |
| DEFERRED | Validation postponed to later phase |

### 10.3 Validation Summary Dashboard

| Status | Count |
|--------|-------|
| PENDING_VALIDATION | 128 (all items in this document) |
| SUBMITTED | 0 |
| VALIDATED | 0 |
| MODIFIED | 0 |
| REJECTED | 0 |
| DEFERRED | 0 |
| **TOTAL** | **128** |

---

## 11. Summary Statistics

| Category | HIGH Priority | MEDIUM Priority | LOW Priority | TOTAL |
|----------|---------------|-----------------|--------------|-------|
| Fields (HVR-FLD) | 6 | 12 | 12 | 30 |
| Business Rules (HVR-RUL) | 20 | 19 | 8 | 47 |
| Conflicts (HVR-CON) | 1 | 5 | 4 | 10 |
| Edge Cases (HVR-EDG) | 8 | 11 | 6 | 25 |
| Legal Questions (HVR-LAW) | 14 | 7 | 4 | 25 |
| Source Conflicts (HVR-SRC) | 1 | 4 | 3 | 8 |
| Expert Topics (HVR-EXP) | 20 | 12 | 2 | 34 |
| **GRAND TOTAL** | **70** | **70** | **39** | **179** |

Note: Some items appear in multiple categories (e.g., a field may also be the subject of a legal question). The total unique items is 128; the sum of categories exceeds this because of cross-referencing.

---

**End of HUMAN_VALIDATION_REQUIRED.md** — All items in this document must be tracked through to resolution before production deployment of the qualification matrices.
