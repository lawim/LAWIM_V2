# FINANCING REQUEST QUALIFICATION MATRICES — LAWIM Cameroon

**Document:** Qualification matrices for all financing request types
**Version:** 1.0
**Statut:** Gold Standard — Validated
**Mission:** LAWIM Heritage Gold

---

## TABLE OF MATRICES

| # | Matrix ID | Financing Type | Page |
|---|-----------|----------------|------|
| 1 | MATRIX-FIN-001 | credit_immobilier (Mortgage/Real Estate Loan) | 2 |
| 2 | MATRIX-FIN-002 | financement_acquisition (Acquisition Financing) | 3 |
| 3 | MATRIX-FIN-003 | financement_construction (Construction Financing) | 4 |
| 4 | MATRIX-FIN-004 | financement_renovation (Renovation Financing) | 5 |
| 5 | MATRIX-FIN-005 | financement_promotion_immobiliere (Real Estate Development Financing) | 6 |
| 6 | MATRIX-FIN-006 | pret_adosse_bien (Property-Backed Loan) | 7 |
| 7 | MATRIX-FIN-007 | recherche_investisseur (Investor Search) | 8 |
| 8 | MATRIX-FIN-008 | cofinancement (Co-Financing) | 9 |
| 9 | MATRIX-FIN-009 | apport_diaspora (Diaspora Contribution) | 10 |
| 10 | MATRIX-FIN-010 | financement_professionnel (Professional/Business Financing) | 11 |

---

## COMMON FIELDS REFERENCE (ALL FINANCING TYPES)

These fields apply to all financing request matrices and are referenced by field_id throughout.

### CORE FINANCIAL FIELDS

| field_id | label | description | data_type | validation_rules | question_priority | matching_role | privacy_level | source | confidence |
|----------|-------|-------------|-----------|------------------|-------------------|---------------|---------------|--------|------------|
| FIN-COMMON-001 | objet_financement | Purpose of the financing request | enum | required; one of: achat, construction, renovation, promotion, fonds_roulement, equipement, refinancement, investissement | P0 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-002 | montant_recherche | Amount of financing needed | number | required; min 100000; max 10000000000; integer | P0 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-003 | cout_total_projet | Total cost of the project | number | required; montant_recherche <= cout_total_projet | P0 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-COMMON-004 | apport_disponible | Available down payment / equity contribution | number | required; apport_disponible >= 0; apport_disponible < cout_total_projet | P0 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-005 | devise | Currency for all monetary amounts | enum | required; allowed: FCFA, EUR, USD | P0 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-006 | delai_souhaite | Desired timeline for obtaining financing | enum | required; allowed: urgent, 1_semaine, 2_semaines, 1_mois, 2_mois, 3_mois, 6_mois, pas_de_delai | P1 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-007 | localisation_projet | Location of the property or project | string | required; min_length 2; max_length 200 | P0 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-008 | type_bien_projet | Type of property involved | enum | required; allowed: appartement, maison, villa, terrain, terrain_constructible, immeuble, commercial, industriel, agricole, hotelier, projet_immobilier | P0 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-009 | statut_acquisition | Status of the property acquisition | enum | required; allowed: deja_acquise, en_cours_negociation, pas_encore_trouve | P1 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-COMMON-010 | profil_demandeur | Requester profile type | enum | required; allowed: salarie, independant, entreprise, investisseur, diaspora, promoteur | P0 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-011 | duree_souhaitee | Desired loan duration / repayment period | enum | required; allowed: 6_mois, 1_an, 2_ans, 3_ans, 5_ans, 7_ans, 10_ans, 15_ans, 20_ans, 25_ans | P1 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-012 | taux_remboursement_souhaite | Desired monthly repayment capacity | number | optional; min 0; max 100000000 | P2 | MATCHING_FINANCEUR | SENSITIVE | lead_input | MEDIUM |

### INCOME & FINANCIAL HEALTH FIELDS

| field_id | label | description | data_type | validation_rules | question_priority | matching_role | privacy_level | source | confidence |
|----------|-------|-------------|-----------|------------------|-------------------|---------------|---------------|--------|------------|
| FIN-COMMON-013 | revenus_mensuels | Total monthly income | number | conditional (if profil_demandeur != entreprise); min 0; mandatory_when: profil_demandeur == salarie or independant | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | HIGH |
| FIN-COMMON-014 | revenus_net | Net monthly income after tax | number | conditional (if profil_demandeur != entreprise); min 0; mandatory_when: profil_demandeur == salarie or independant | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | HIGH |
| FIN-COMMON-015 | source_revenus | Source(s) of income | enum[] | required; allowed: salaire, honoraires, chiffre_affaires, loyers, dividendes, pensions, transferts_diaspora, autres | P1 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-COMMON-016 | autres_engagements | Other existing financial commitments | number | optional; min 0 | P2 | MATCHING_FINANCEUR | SENSITIVE | lead_input | MEDIUM |
| FIN-COMMON-017 | capacite_remboursement | Derived repayment capacity (revenus - engagements) | number | derived; calculated as revenus_mensuels - autres_engagements; automatically computed | P0 | MATCHING_FINANCEUR | SENSITIVE | derived | HIGH |
| FIN-COMMON-018 | garanties_disponibles | Types of guarantees available | enum[] | required; allowed: titre_foncier, hypotheque, caution, nantissement, caution_solidaire, assurance, depot_garantie, pas_de_garantie | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | MEDIUM |
| FIN-COMMON-019 | documents_disponibles | Documents the requester can provide | enum[] | required; allowed: piece_identite, passeport, titre_foncier, acte_vente, plan_borne, devis, factures_proforma, releves_bancaires, bilan_comptable, avis_imposition, promesse_vente, permis_construire, fiche_paie, contrat_travail, attestation_ressources | P2 | MATCHING_FINANCEUR | SENSITIVE | lead_input | MEDIUM |
| FIN-COMMON-020 | email_contact | Email address for follow-up | string | required; format email; max_length 100 | P2 | COMMERCIAL | PRIVATE | lead_input | MEDIUM |
| FIN-COMMON-021 | telephone_contact | Phone number for follow-up | string | required; format phone; min_length 8; max_length 20 | P2 | COMMERCIAL | PRIVATE | lead_input | MEDIUM |
| FIN-COMMON-022 | ville_projet | City where the project is located | string | required; min_length 2; max_length 100 | P0 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-COMMON-023 | quartier_projet | Neighborhood of the project | string | optional; min_length 2; max_length 100 | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-COMMON-024 | accepte_taux_variable | Whether variable interest rate is acceptable | boolean | optional; default true | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-COMMON-025 | montant_recherche_min | Minimum financing amount acceptable | number | optional; min 0; must be <= montant_recherche | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |

### SALARIED EMPLOYEE SPECIFIC FIELDS

| field_id | label | description | data_type | validation_rules | question_priority | matching_role | privacy_level | source | confidence |
|----------|-------|-------------|-----------|------------------|-------------------|---------------|---------------|--------|------------|
| FIN-SAL-001 | employeur | Current employer name | string | mandatory_when: profil_demandeur == salarie; min_length 2; max_length 150 | P1 | MATCHING_FINANCEUR | PRIVATE | lead_input | HIGH |
| FIN-SAL-002 | anciennete_emploi | Tenure at current employer | enum | mandatory_when: profil_demandeur == salarie; allowed: moins_6_mois, 6_12_mois, 1_3_ans, 3_5_ans, 5_10_ans, plus_10_ans | P1 | MATCHING_FINANCEUR | PRIVATE | lead_input | HIGH |
| FIN-SAL-003 | revenu_mensuel_brut | Gross monthly salary | number | mandatory_when: profil_demandeur == salarie; min 0 | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | HIGH |
| FIN-SAL-004 | revenu_net_mensuel | Net monthly salary | number | mandatory_when: profil_demandeur == salarie; min 0 | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | HIGH |
| FIN-SAL-005 | type_contrat | Employment contract type | enum | mandatory_when: profil_demandeur == salarie; allowed: cdi, cdd, fonctionnaire, interim, stagiaire | P1 | MATCHING_FINANCEUR | PRIVATE | lead_input | MEDIUM |
| FIN-SAL-006 | secteur_employeur | Sector of employer | enum | optional; allowed: public, prive, para_public, international, ong | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-SAL-007 | domiciliation_bancaire | Whether salary is banked at the lending institution | boolean | optional; may increase matching score | P3 | MATCHING_FINANCEUR | SENSITIVE | lead_input | LOW |
| FIN-SAL-008 | banque_principale | Primary bank name | string | optional; min_length 2; max_length 100 | P3 | MATCHING_FINANCEUR | PRIVATE | lead_input | LOW |

### SELF-EMPLOYED / COMPANY SPECIFIC FIELDS

| field_id | label | description | data_type | validation_rules | question_priority | matching_role | privacy_level | source | confidence |
|----------|-------|-------------|-----------|------------------|-------------------|---------------|---------------|--------|------------|
| FIN-SE-001 | activite | Type of business activity | string | mandatory_when: profil_demandeur == independant or entreprise; min_length 3; max_length 200 | P1 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-SE-002 | anciennete_activite | How long the business has been operating | enum | mandatory_when: profil_demandeur == independant or entreprise; allowed: moins_1_an, 1_2_ans, 2_5_ans, 5_10_ans, plus_10_ans | P1 | MATCHING_FINANCEUR | PRIVATE | lead_input | HIGH |
| FIN-SE-003 | chiffre_affaires_mensuel | Average monthly turnover | number | mandatory_when: profil_demandeur == independant or entreprise; min 0 | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | HIGH |
| FIN-SE-004 | chiffre_affaires_annuel | Annual turnover | number | mandatory_when: profil_demandeur == entreprise; min 0 | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | HIGH |
| FIN-SE-005 | resultat_mensuel | Average monthly net result | number | mandatory_when: profil_demandeur == independant; min 0 | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | HIGH |
| FIN-SE-006 | formalisation | Legal registration status | enum | mandatory_when: profil_demandeur == independant or entreprise; allowed: entreprise_individuelle, sarl, sa, succursale, etablissement, cooperative, informel, en_cours_immatriculation | P1 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-SE-007 | numero_rccm | RCCM (Trade and Personal Property Credit Register) number | string | optional; format rccm; max_length 50 | P2 | MATCHING_FINANCEUR | PRIVATE | lead_input | LOW |
| FIN-SE-008 | numero_contribuable | Taxpayer identification number | string | optional; format niu; max_length 50 | P2 | MATCHING_FINANCEUR | PRIVATE | lead_input | LOW |
| FIN-SE-009 | documents_fiscaux | Tax documents available | enum[] | mandatory_when: profil_demandeur == entreprise; allowed: bilan_annuel, compte_resultat, liasses_fiscales, avis_imposition, declaration_tva, pas_de_documents_fiscaux | P2 | MATCHING_FINANCEUR | SENSITIVE | lead_input | MEDIUM |
| FIN-SE-010 | releves_bancaires | Bank statements availability | enum | optional; allowed: 3_derniers_mois, 6_derniers_mois, 12_derniers_mois, pas_disponible | P2 | MATCHING_FINANCEUR | SENSITIVE | lead_input | LOW |
| FIN-SE-011 | promoteurs_associes | Associated promoters / partners | string | optional; max_length 500; description: names and roles of co-promoters if applicable | P3 | MATCHING_FINANCEUR | PRIVATE | lead_input | LOW |
| FIN-SE-012 | effectif_employes | Number of employees | integer | optional; min 0; max 10000 | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |

### CONSTRUCTION / PROJECT SPECIFIC FIELDS

| field_id | label | description | data_type | validation_rules | question_priority | matching_role | privacy_level | source | confidence |
|----------|-------|-------------|-----------|------------------|-------------------|---------------|---------------|--------|------------|
| FIN-CONS-001 | terrain_disponible | Whether land is already available | boolean | mandatory_when: objet_financement == construction or promotion; default false | P1 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-CONS-002 | statut_juridique_terrain | Legal status of the land | enum | mandatory_when: terrain_disponible == true; allowed: titre_foncier, promesse_vente, acte_vente, certificat_occupation, bail_emphyteotique, terrain_familial, pas_de_titre, ne_sais_pas | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | HIGH |
| FIN-CONS-003 | surface_terrain | Land surface area in m² | number | mandatory_when: objet_financement == construction or promotion; min 1; max 1000000 | P2 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-CONS-004 | surface_construite | Built-up area in m² | number | conditional; min 1; max 500000 | P2 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-CONS-005 | plans_disponibles | Whether architectural plans are available | boolean | mandatory_when: objet_financement == construction or promotion; default false | P2 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-CONS-006 | type_plans | Type of plans available | enum[] | conditional (if plans_disponibles); allowed: plan_architectural, plan_façade, plan_etage, plan_coupe, plan_electrique, plan_plomberie, plan_structure | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-CONS-007 | permis_autorisations | Building permits and authorizations | enum[] | mandatory_when: objet_financement == construction or promotion; allowed: permis_construire, certificat_conformite, autorisation_urbanisme, permis_developer, pas_encore, ne_sais_pas | P1 | MATCHING_FINANCEUR | SENSITIVE | lead_input | HIGH |
| FIN-CONS-008 | numero_permis_construire | Building permit reference number | string | conditional (if permis_construire in permis_autorisations); max_length 50 | P3 | MATCHING_FINANCEUR | PRIVATE | lead_input | LOW |
| FIN-CONS-009 | devis_disponibles | Whether detailed quotes/estimates are available | boolean | mandatory_when: objet_financement == construction or renovation; default false | P2 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-CONS-010 | montant_devis | Total amount of available quotes | number | conditional (if devis_disponibles); min 0 | P2 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-CONS-011 | entreprise_maitre_oeuvre | Construction company or project manager | string | optional; max_length 200 | P3 | MATCHING_FINANCEUR | PRIVATE | lead_input | LOW |
| FIN-CONS-012 | maitre_oeuvre_qualifie | Whether the builder/contractor is certified | boolean | optional; default false | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-CONS-013 | calendrier_travaux | Construction timeline | enum | mandatory_when: objet_financement == construction or promotion; allowed: demarrage_immediat, 1_mois, 3_mois, 6_mois, 12_mois, plus_12_mois | P2 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-CONS-014 | duree_chantier_estimee | Estimated construction duration | enum | optional; allowed: 3_mois, 6_mois, 12_mois, 18_mois, 24_mois, 36_mois | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |
| FIN-CONS-015 | niveau_avancement | Current level of construction progress | enum | conditional (if objet_financement == construction or renovation); allowed: pas_commence, fondations, gros_oeuvre, second_oeuvre, finitions, renovation_partielle, renovation_complete | P1 | MATCHING_FINANCEUR | PUBLIC | lead_input | HIGH |
| FIN-CONS-016 | tranches_financement | Number of planned disbursement tranches | integer | optional; min 1; max 20; description: number of disbursement tranches requested | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-CONS-017 | montant_premiere_tranche | Amount needed for first tranche | number | conditional (if tranches_financement > 1); min 0 | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-CONS-018 | cout_main_oeuvre | Labor cost component | number | optional; min 0; part of cout_total_projet breakdown | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-CONS-019 | cout_materiaux | Materials cost component | number | optional; min 0; part of cout_total_projet breakdown | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | LOW |
| FIN-CONS-020 | cout_terrain | Land cost component | number | conditional (if objet_financement == construction or promotion); min 0; part of cout_total_projet breakdown | P3 | MATCHING_FINANCEUR | PUBLIC | lead_input | MEDIUM |

### DIASPORA SPECIFIC FIELDS

| field_id | label | description | data_type | validation_rules | question_priority | matching_role | privacy_level | source | confidence |
|----------|-------|-------------|-----------|------------------|-------------------|---------------|---------------|--------|------------|
| FIN-DIA-001 | pays_residence | Country of residence | string | mandatory_when: profil_demandeur == diaspora; min_length 2; max_length 100 | P1 | MATCHING_FINANCEUR | PRIVATE | lead_input | HIGH |
| FIN-DIA-002 | statut_residence | Residence status in host country | enum | optional; allowed: resident_permanent, citoyen, visa_travail, visa_etudiant, sans_papiers | P3 | MATCHING_FINANCEUR | PRIVATE | lead_input | LOW |
| FIN-DIA-003 | relay_local_cameroun | Local relay/representative in Cameroon | string | optional; max_length 200 | P2 | COMMERCIAL | PRIVATE | lead_input | LOW |
| FIN-DIA-004 | compte_bancaire_cameroun | Whether requester has a Cameroonian bank account | boolean | optional; default false | P2 | MATCHING_FINANCEUR | SENSITIVE | lead_input | MEDIUM |
| FIN-DIA-005 | transfert_regulier | Whether regular transfers are made to Cameroon | boolean | optional; may increase matching score | P3 | MATCHING_FINANCEUR | SENSITIVE | lead_input | LOW |
| FIN-DIA-006 | justificatif_revenus_diaspora | Type of income proof available | enum[] | optional; allowed: fiche_paie_etranger, avis_imposition_etranger, releves_bancaires_etrangers, contrat_travail_etranger, declaration_fiscale | P2 | MATCHING_FINANCEUR | SENSITIVE | lead_input | LOW |

---

## MATRIX 1: CREDIT IMMOBILIER (MORTGAGE / REAL ESTATE LOAN)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-001 |
| canonical_name | Crédit Immobilier |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | credit_immobilier |
| requester_typology | individual |
| journey_stage | SEARCH |
| description | Demande de crédit immobilier pour l'acquisition d'un bien résidentiel auprès d'une banque ou microfinance au Cameroun |

### Minimum Intake Fields

These fields MUST be collected before any processing begins.

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Quel est l'objet de votre demande de financement ? | always |
| FIN-COMMON-002 | montant_recherche | Quel montant souhaitez-vous emprunter ? | always |
| FIN-COMMON-004 | apport_disponible | Quel apport personnel pouvez-vous apporter ? | always |
| FIN-COMMON-005 | devise | Dans quelle devise ? (FCFA, EUR, USD) | always |
| FIN-COMMON-007 | localisation_projet | Où se situe le bien que vous souhaitez financer ? | always |
| FIN-COMMON-008 | type_bien_projet | De quel type de bien s'agit-il ? | always |
| FIN-COMMON-010 | profil_demandeur | Quel est votre profil ? (salarié, indépendant, entreprise) | always |
| FIN-COMMON-022 | ville_projet | Dans quelle ville se trouve le projet ? | always |

### Minimum Search Fields

Fields required to search for matching financing products.

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Quel montant souhaitez-vous emprunter ? | always |
| FIN-COMMON-004 | apport_disponible | Quel apport personnel pouvez-vous apporter ? | always |
| FIN-COMMON-011 | duree_souhaitee | Sur quelle durée souhaitez-vous rembourser ? | always |
| FIN-COMMON-008 | type_bien_projet | De quel type de bien s'agit-il ? | always |
| FIN-COMMON-022 | ville_projet | Dans quelle ville ? | always |
| FIN-COMMON-009 | statut_acquisition | Le bien est-il déjà acquis ou êtes-vous en recherche ? | always |

### Minimum Matching Fields

Fields required for matching with potential lenders.

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant recherché | always |
| FIN-COMMON-004 | apport_disponible | Apport personnel disponible | always |
| FIN-COMMON-011 | duree_souhaitee | Durée de remboursement souhaitée | always |
| FIN-COMMON-013 | revenus_mensuels | Quels sont vos revenus mensuels ? | profil_demandeur == salarie or independant |
| FIN-COMMON-018 | garanties_disponibles | Quelles garanties pouvez-vous offrir ? | always |
| FIN-COMMON-022 | ville_projet | Ville du projet | always |
| FIN-COMMON-003 | cout_total_projet | Quel est le coût total du projet ? | always |

### Minimum Introduction Fields

Fields required before connecting with a lender.

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Quelle est votre adresse email ? | always |
| FIN-COMMON-021 | telephone_contact | Quel est votre numéro de téléphone ? | always |
| FIN-COMMON-014 | revenus_net | Quel est votre revenu net mensuel ? | always |
| FIN-COMMON-017 | capacite_remboursement | Capacité de remboursement estimée | always (derived) |

### Minimum Transaction Fields

Fields required before submitting a formal application to a lender.

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-SAL-001 | employeur | Quel est le nom de votre employeur ? | profil_demandeur == salarie |
| FIN-SAL-002 | anciennete_emploi | Depuis combien de temps travaillez-vous chez cet employeur ? | profil_demandeur == salarie |
| FIN-SAL-005 | type_contrat | Quel est votre type de contrat ? | profil_demandeur == salarie |
| FIN-SE-001 | activite | Quel est votre domaine d'activité ? | profil_demandeur == independant |
| FIN-SE-002 | anciennete_activite | Depuis combien de temps exercez-vous cette activité ? | profil_demandeur == independant |
| FIN-SE-003 | chiffre_affaires_mensuel | Quel est votre chiffre d'affaires mensuel moyen ? | profil_demandeur == independant |
| FIN-SE-005 | resultat_mensuel | Quel est votre résultat net mensuel ? | profil_demandeur == independant |
| FIN-SE-006 | formalisation | Quelle est votre forme juridique ? | profil_demandeur == independant |
| FIN-COMMON-019 | documents_disponibles | Quels documents pouvez-vous fournir ? | always |

### Recommended Fields

| field_id | label | question_template (FR) | recommendation_reason |
|----------|-------|------------------------|------------------------|
| FIN-COMMON-006 | delai_souhaite | Dans quel délai souhaitez-vous obtenir ce financement ? | Improves matching timeliness |
| FIN-COMMON-016 | autres_engagements | Avez-vous d'autres engagements financiers en cours ? | Required for accurate capacite_remboursement |
| FIN-COMMON-024 | accepte_taux_variable | Accepteriez-vous un taux variable ? | Expands matching options |
| FIN-SAL-006 | secteur_employeur | Dans quel secteur travaille votre employeur ? | Some lenders prefer public sector |
| FIN-SAL-007 | domiciliation_bancaire | Votre salaire est-il domicilié dans une banque ? | May improve matching score |
| FIN-COMMON-023 | quartier_projet | Dans quel quartier précisément ? | Refines location matching |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-025 | montant_recherche_min | Quel est le montant minimum acceptable ? |
| FIN-SAL-008 | banque_principale | Quelle est votre banque principale ? |
| FIN-SE-011 | promoteurs_associes | Y a-t-il des co-promoteurs ou associés ? |
| FIN-COMMON-012 | taux_remboursement_souhaite | Quelle capacité de remboursement mensuelle visez-vous ? |

### Conditional Fields

| field_id | label | condition | question_template (FR) |
|----------|-------|-----------|------------------------|
| FIN-SE-007 | numero_rccm | profil_demandeur == entreprise | Quel est votre numéro RCCM ? |
| FIN-SE-008 | numero_contribuable | profil_demandeur == entreprise | Quel est votre numéro de contribuable (NIU) ? |
| FIN-SE-009 | documents_fiscaux | profil_demandeur == entreprise | Quels documents fiscaux pouvez-vous fournir ? |
| FIN-SE-010 | releves_bancaires | profil_demandeur == independant or entreprise | Pouvez-vous fournir des relevés bancaires ? |
| FIN-COMMON-019 | documents_disponibles | additional documentation needed | Quels documents pouvez-vous fournir ? |
| FIN-CONS-002 | statut_juridique_terrain | type_bien_projet == terrain_constructible | Quel est le statut juridique du terrain ? |

### Sensitive Fields

| field_id | label | handling_rule |
|----------|-------|---------------|
| FIN-COMMON-013 | revenus_mensuels | Store encrypted; never display to unauthorized users; mark confidential |
| FIN-COMMON-014 | revenus_net | Store encrypted; never display to unauthorized users |
| FIN-COMMON-016 | autres_engagements | Store encrypted; never display to unauthorized users |
| FIN-COMMON-018 | garanties_disponibles | Store encrypted; access restricted to matching engine |
| FIN-SAL-003 | revenu_mensuel_brut | Store encrypted; mark confidential |
| FIN-SAL-004 | revenu_net_mensuel | Store encrypted; mark confidential |
| FIN-SAL-007 | domiciliation_bancaire | Store encrypted; sensitive banking information |
| FIN-SE-003 | chiffre_affaires_mensuel | Store encrypted; sensitive business data |
| FIN-SE-004 | chiffre_affaires_annuel | Store encrypted; sensitive business data |
| FIN-SE-005 | resultat_mensuel | Store encrypted; sensitive business data |
| FIN-SE-009 | documents_fiscaux | Store encrypted; never share without explicit consent |
| FIN-SE-010 | releves_bancaires | Store encrypted; never share without explicit consent |
| FIN-CONS-002 | statut_juridique_terrain | Store encrypted; sensitive legal data |
| FIN-CONS-007 | permis_autorisations | Store encrypted; sensitive legal data |

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Votre prêt est approuvé" | LAWIM ne promet jamais l'approbation d'un prêt - matching only on compatibilité apparente |
| "Garantie de remboursement" | Ne pas garantir le remboursement |
| "Taux d'intérêt garanti" | Les taux sont variables selon les financeurs; LAWIM ne fixe pas les taux |
| "Accepté à 100%" | Jamais de promesse d'acceptation |
| "Prêt sans intérêts" | Trompeur; ne pas suggérer des prêts sans intérêts sauf explicite du financeur |
| "Besoin de votre code bancaire" | Ne jamais demander des codes bancaires ou mots de passe |
| "Envoyez-nous votre carte d'identité" | Attendre que le demandeur propose les documents |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | compatibilité_apparente, critères_éligibilité, type_financeur, montant, apport, durée, garanties, zone |
| final_decision | Le financeur seul (banque/microfinance) décide de l'octroi du crédit |
| derived_fields | capacite_remboursement = revenus_mensuels - autres_engagements |
| scoring_weight_montant | 0.25 |
| scoring_weight_apport | 0.15 |
| scoring_weight_duree | 0.10 |
| scoring_weight_revenus | 0.20 |
| scoring_weight_garanties | 0.15 |
| scoring_weight_zone | 0.15 |

---

## MATRIX 2: FINANCEMENT ACQUISITION (ACQUISITION FINANCING)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-002 |
| canonical_name | Financement Acquisition |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | financement_acquisition |
| requester_typology | individual / investor |
| journey_stage | SEARCH |
| description | Demande de financement pour l'acquisition d'un bien immobilier (terrain, maison, appartement, immeuble) |

### Minimum Intake Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Quel est l'objet de votre demande de financement ? | always |
| FIN-COMMON-002 | montant_recherche | Quel montant de financement recherchez-vous ? | always |
| FIN-COMMON-003 | cout_total_projet | Quel est le coût total d'acquisition du bien ? | always |
| FIN-COMMON-004 | apport_disponible | Quel apport personnel pouvez-vous apporter ? | always |
| FIN-COMMON-005 | devise | Dans quelle devise ? | always |
| FIN-COMMON-007 | localisation_projet | Où se situe le bien à acquérir ? | always |
| FIN-COMMON-008 | type_bien_projet | De quel type de bien s'agit-il ? | always |
| FIN-COMMON-022 | ville_projet | Dans quelle ville ? | always |

### Minimum Search Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement recherché | always |
| FIN-COMMON-004 | apport_disponible | Apport personnel | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-008 | type_bien_projet | Type de bien | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-COMMON-009 | statut_acquisition | Le bien est-il déjà identifié ? | always |

### Minimum Matching Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement | always |
| FIN-COMMON-004 | apport_disponible | Apport disponible | always |
| FIN-COMMON-011 | duree_souhaitee | Durée de remboursement souhaitée | always |
| FIN-COMMON-013 | revenus_mensuels | Revenus mensuels | profil_demandeur != entreprise |
| FIN-COMMON-018 | garanties_disponibles | Garanties disponibles | always |
| FIN-COMMON-022 | ville_projet | Ville du projet | always |
| FIN-COMMON-010 | profil_demandeur | Profil du demandeur | always |

### Minimum Introduction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Votre adresse email | always |
| FIN-COMMON-021 | telephone_contact | Votre numéro de téléphone | always |
| FIN-COMMON-014 | revenus_net | Revenu net mensuel | profil_demandeur != entreprise |
| FIN-COMMON-017 | capacite_remboursement | Capacité de remboursement | always (derived) |

### Minimum Transaction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-SAL-001 | employeur | Nom de l'employeur | profil_demandeur == salarie |
| FIN-SAL-002 | anciennete_emploi | Ancienneté dans l'emploi | profil_demandeur == salarie |
| FIN-SAL-005 | type_contrat | Type de contrat de travail | profil_demandeur == salarie |
| FIN-SE-001 | activite | Domaine d'activité | profil_demandeur == independant or entreprise |
| FIN-SE-002 | anciennete_activite | Ancienneté de l'activité | profil_demandeur == independant or entreprise |
| FIN-SE-003 | chiffre_affaires_mensuel | Chiffre d'affaires mensuel | profil_demandeur == independant |
| FIN-SE-006 | formalisation | Forme juridique | profil_demandeur == independant or entreprise |
| FIN-COMMON-019 | documents_disponibles | Documents disponibles | always |
| FIN-COMMON-009 | statut_acquisition | Statut de l'acquisition | always |
| FIN-CONS-002 | statut_juridique_terrain | Statut juridique du terrain | type_bien_projet == terrain or terrain_constructible |

### Recommended Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-006 | delai_souhaite | Dans quel délai ? |
| FIN-COMMON-016 | autres_engagements | Autres engagements financiers ? |
| FIN-COMMON-023 | quartier_projet | Quartier précis ? |
| FIN-SAL-003 | revenu_mensuel_brut | Revenu mensuel brut ? |
| FIN-SE-004 | chiffre_affaires_annuel | Chiffre d'affaires annuel ? |
| FIN-SE-005 | resultat_mensuel | Résultat net mensuel ? |
| FIN-SE-007 | numero_rccm | Numéro RCCM ? |
| FIN-COMMON-024 | accepte_taux_variable | Taux variable acceptable ? |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-025 | montant_recherche_min | Montant minimum acceptable ? |
| FIN-SAL-006 | secteur_employeur | Secteur de l'employeur ? |
| FIN-SAL-008 | banque_principale | Banque principale ? |
| FIN-SE-008 | numero_contribuable | Numéro de contribuable ? |
| FIN-SE-011 | promoteurs_associes | Co-promoteurs ? |
| FIN-SE-012 | effectif_employes | Effectif des employés ? |
| FIN-COMMON-012 | taux_remboursement_souhaite | Capacité de remboursement mensuelle visée ? |

### Conditional Fields

| field_id | label | condition |
|----------|-------|-----------|
| FIN-SE-009 | documents_fiscaux | profil_demandeur == entreprise |
| FIN-SE-010 | releves_bancaires | profil_demandeur == independant or entreprise |
| FIN-CONS-002 | statut_juridique_terrain | type_bien_projet == terrain or terrain_constructible |
| FIN-CONS-003 | surface_terrain | type_bien_projet == terrain or terrain_constructible |
| FIN-CONS-020 | cout_terrain | type_bien_projet == terrain or terrain_constructible |

### Sensitive Fields

All fields from FIN-COMMON-013 through FIN-COMMON-018, FIN-SAL-003, FIN-SAL-004, FIN-SAL-007, FIN-SE-003 through FIN-SE-005, FIN-SE-009, FIN-SE-010, FIN-CONS-002, FIN-CONS-007.

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Avez-vous déjà été refusé par une banque ?" | Ne pas présumer d'antécédents négatifs |
| "Votre crédit est pré-approuvé" | LAWIM ne pré-approuve pas les crédits |
| "Quel est votre solde bancaire actuel ?" | Trop intrusif; demande non appropriée |
| "Pouvez-vous payer des frais de dossier maintenant ?" | LAWIM ne perçoit pas de frais de dossier |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | compatibilité_apparente, critères_éligibilité, montant, apport, durée, garanties, zone, type_bien |
| final_decision | Le financeur seul décide de l'octroi |
| derived_fields | capacite_remboursement, taux_endettement = (autres_engagements / revenus_mensuels * 100) |
| scoring_weight_montant | 0.20 |
| scoring_weight_apport_ratio | 0.20 (apport / cout_total_projet) |
| scoring_weight_duree | 0.10 |
| scoring_weight_revenus | 0.20 |
| scoring_weight_garanties | 0.15 |
| scoring_weight_type_bien | 0.15 |

---

## MATRIX 3: FINANCEMENT CONSTRUCTION (CONSTRUCTION FINANCING)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-003 |
| canonical_name | Financement Construction |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | financement_construction |
| requester_typology | individual / investor / company |
| journey_stage | SEARCH |
| description | Demande de financement pour la construction d'un bien immobilier neuf (maison, villa, immeuble) |

### Minimum Intake Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Quel est l'objet de votre demande de financement ? | always; value: construction |
| FIN-COMMON-002 | montant_recherche | Quel montant de financement pour la construction ? | always |
| FIN-COMMON-003 | cout_total_projet | Quel est le coût total du projet de construction ? | always |
| FIN-COMMON-004 | apport_disponible | Quel apport personnel pouvez-vous apporter ? | always |
| FIN-COMMON-005 | devise | Dans quelle devise ? | always |
| FIN-COMMON-007 | localisation_projet | Où se situera la construction ? | always |
| FIN-COMMON-008 | type_bien_projet | Quel type de construction ? | always |
| FIN-COMMON-022 | ville_projet | Dans quelle ville ? | always |
| FIN-CONS-001 | terrain_disponible | Disposez-vous déjà d'un terrain ? | always |
| FIN-CONS-015 | niveau_avancement | Quel est le niveau d'avancement actuel ? | always |

### Minimum Search Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement construction | always |
| FIN-COMMON-004 | apport_disponible | Apport personnel | always |
| FIN-COMMON-003 | cout_total_projet | Coût total de la construction | always |
| FIN-COMMON-008 | type_bien_projet | Type de construction | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-CONS-001 | terrain_disponible | Terrain disponible ? | always |
| FIN-CONS-015 | niveau_avancement | Niveau d'avancement | always |

### Minimum Matching Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement | always |
| FIN-COMMON-004 | apport_disponible | Apport disponible | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-011 | duree_souhaitee | Durée de remboursement souhaitée | always |
| FIN-COMMON-013 | revenus_mensuels | Revenus mensuels | profil_demandeur != entreprise |
| FIN-COMMON-018 | garanties_disponibles | Garanties disponibles | always |
| FIN-COMMON-022 | ville_projet | Ville de la construction | always |
| FIN-CONS-001 | terrain_disponible | Terrain disponible ? | always |
| FIN-CONS-002 | statut_juridique_terrain | Statut juridique du terrain | terrain_disponible == true |
| FIN-CONS-007 | permis_autorisations | Permis et autorisations obtenus ? | always |
| FIN-CONS-013 | calendrier_travaux | Calendrier prévisionnel des travaux | always |

### Minimum Introduction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Votre adresse email | always |
| FIN-COMMON-021 | telephone_contact | Votre numéro de téléphone | always |
| FIN-COMMON-014 | revenus_net | Revenu net mensuel | profil_demandeur != entreprise |
| FIN-COMMON-017 | capacite_remboursement | Capacité de remboursement | always (derived) |

### Minimum Transaction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-SAL-001 | employeur | Nom de l'employeur | profil_demandeur == salarie |
| FIN-SAL-002 | anciennete_emploi | Ancienneté | profil_demandeur == salarie |
| FIN-SE-001 | activite | Domaine d'activité | profil_demandeur == independant or entreprise |
| FIN-SE-002 | anciennete_activite | Ancienneté de l'activité | profil_demandeur == independant or entreprise |
| FIN-SE-003 | chiffre_affaires_mensuel | Chiffre d'affaires mensuel | profil_demandeur == independant |
| FIN-SE-006 | formalisation | Forme juridique | profil_demandeur == independant or entreprise |
| FIN-CONS-002 | statut_juridique_terrain | Statut juridique du terrain | terrain_disponible == true |
| FIN-CONS-005 | plans_disponibles | Disposez-vous des plans architecturaux ? | always |
| FIN-CONS-007 | permis_autorisations | Permis de construire obtenu ? | always |
| FIN-CONS-009 | devis_disponibles | Avez-vous des devis pour les travaux ? | always |
| FIN-CONS-013 | calendrier_travaux | Calendrier des travaux | always |
| FIN-CONS-015 | niveau_avancement | Niveau d'avancement actuel | always |
| FIN-COMMON-019 | documents_disponibles | Documents disponibles | always |

### Recommended Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-006 | delai_souhaite | Délai souhaité pour le financement ? |
| FIN-COMMON-016 | autres_engagements | Autres engagements financiers ? |
| FIN-CONS-003 | surface_terrain | Surface du terrain (m²) ? |
| FIN-CONS-004 | surface_construite | Surface à construire (m²) ? |
| FIN-CONS-010 | montant_devis | Montant total des devis ? |
| FIN-CONS-014 | duree_chantier_estimee | Durée estimée du chantier ? |
| FIN-CONS-011 | entreprise_maitre_oeuvre | Entreprise ou maître d'œuvre prévu ? |
| FIN-CONS-016 | tranches_financement | Nombre de tranches de décaissement souhaitées ? |
| FIN-CONS-012 | maitre_oeuvre_qualifie | Le maître d'œuvre est-il qualifié/agréé ? |
| FIN-SE-007 | numero_rccm | Numéro RCCM (si entreprise) ? |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-023 | quartier_projet | Quartier précis ? |
| FIN-CONS-006 | type_plans | Quels types de plans sont disponibles ? |
| FIN-CONS-008 | numero_permis_construire | Numéro du permis de construire ? |
| FIN-CONS-017 | montant_premiere_tranche | Montant de la première tranche ? |
| FIN-CONS-018 | cout_main_oeuvre | Coût estimé de la main-d'œuvre ? |
| FIN-CONS-019 | cout_materiaux | Coût estimé des matériaux ? |
| FIN-CONS-020 | cout_terrain | Coût du terrain ? |
| FIN-COMMON-012 | taux_remboursement_souhaite | Capacité de remboursement mensuelle visée ? |
| FIN-COMMON-024 | accepte_taux_variable | Taux variable acceptable ? |

### Conditional Fields

| field_id | label | condition |
|----------|-------|-----------|
| FIN-CONS-002 | statut_juridique_terrain | terrain_disponible == true |
| FIN-CONS-003 | surface_terrain | terrain_disponible == true |
| FIN-CONS-006 | type_plans | plans_disponibles == true |
| FIN-CONS-008 | numero_permis_construire | permis_construire in permis_autorisations |
| FIN-CONS-010 | montant_devis | devis_disponibles == true |
| FIN-CONS-017 | montant_premiere_tranche | tranches_financement > 1 |
| FIN-CONS-018 | cout_main_oeuvre | optional breakdown |
| FIN-CONS-019 | cout_materiaux | optional breakdown |
| FIN-CONS-020 | cout_terrain | terrain_disponible == true |
| FIN-SE-009 | documents_fiscaux | profil_demandeur == entreprise |
| FIN-SE-004 | chiffre_affaires_annuel | profil_demandeur == entreprise |
| FIN-SE-012 | effectif_employes | profil_demandeur == entreprise |

### Sensitive Fields

All standard sensitive fields plus FIN-CONS-002 (statut juridique terrain), FIN-CONS-007 (permis et autorisations), FIN-CONS-008 (numéro permis construire).

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Votre construction est garantie" | LAWIM ne garantit pas les projets de construction |
| "Pouvez-vous commencer sans permis ?" | Encourager des travaux sans permis est illégal |
| "Êtes-vous sûr que le terrain est à vous ?" | Formulation accusatoire; demander poliment les documents |
| "Avez-vous les moyens de financer la différence ?" | Formulation dégradante; préférer une question neutre sur l'apport |
| "Le chantier est-il déjà en retard ?" | Formulation négative; demander le calendrier de façon neutre |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | compatibilité_apparente, type_financeur, montant, apport, durée, garanties, zone, type_construction, niveau_avancement, terrain_status |
| final_decision | Le financeur seul décide |
| derived_fields | capacite_remboursement, ratio_apport = apport_disponible / cout_total_projet |
| scoring_weight_montant | 0.20 |
| scoring_weight_apport_ratio | 0.20 |
| scoring_weight_garanties | 0.15 |
| scoring_weight_terrain_status | 0.15 |
| scoring_weight_permis | 0.15 |
| scoring_weight_avancement | 0.10 |
| scoring_weight_zone | 0.05 |

---

## MATRIX 4: FINANCEMENT RENOVATION (RENOVATION FINANCING)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-004 |
| canonical_name | Financement Rénovation |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | financement_renovation |
| requester_typology | individual |
| journey_stage | SEARCH |
| description | Demande de financement pour la rénovation, réhabilitation ou extension d'un bien immobilier existant |

### Minimum Intake Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Quel est l'objet de votre demande de financement ? | always; value: renovation |
| FIN-COMMON-002 | montant_recherche | Quel montant pour les travaux de rénovation ? | always |
| FIN-COMMON-003 | cout_total_projet | Quel est le coût total du projet de rénovation ? | always |
| FIN-COMMON-004 | apport_disponible | Quel apport personnel ? | always |
| FIN-COMMON-005 | devise | Dans quelle devise ? | always |
| FIN-COMMON-007 | localisation_projet | Où se situe le bien à rénover ? | always |
| FIN-COMMON-008 | type_bien_projet | De quel type de bien s'agit-il ? | always |
| FIN-COMMON-022 | ville_projet | Dans quelle ville ? | always |
| FIN-CONS-015 | niveau_avancement | Quel est le niveau d'avancement des travaux ? | always |

### Minimum Search Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement rénovation | always |
| FIN-COMMON-004 | apport_disponible | Apport personnel | always |
| FIN-COMMON-003 | cout_total_projet | Coût total de la rénovation | always |
| FIN-CONS-015 | niveau_avancement | Niveau d'avancement | always |
| FIN-COMMON-008 | type_bien_projet | Type de bien | always |
| FIN-COMMON-022 | ville_projet | Ville | always |

### Minimum Matching Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement | always |
| FIN-COMMON-004 | apport_disponible | Apport disponible | always |
| FIN-COMMON-003 | cout_total_projet | Coût total de la rénovation | always |
| FIN-COMMON-011 | duree_souhaitee | Durée de remboursement | always |
| FIN-COMMON-013 | revenus_mensuels | Revenus mensuels | profil_demandeur == salarie or independant |
| FIN-COMMON-018 | garanties_disponibles | Garanties disponibles | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-CONS-015 | niveau_avancement | Niveau d'avancement des travaux | always |
| FIN-CONS-009 | devis_disponibles | Devis disponibles pour les travaux ? | always |

### Minimum Introduction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Votre adresse email | always |
| FIN-COMMON-021 | telephone_contact | Votre numéro de téléphone | always |
| FIN-COMMON-014 | revenus_net | Revenu net mensuel | profil_demandeur != entreprise |
| FIN-COMMON-017 | capacite_remboursement | Capacité de remboursement | always (derived) |

### Minimum Transaction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-SAL-001 | employeur | Nom de l'employeur | profil_demandeur == salarie |
| FIN-SAL-002 | anciennete_emploi | Ancienneté | profil_demandeur == salarie |
| FIN-SAL-005 | type_contrat | Type de contrat | profil_demandeur == salarie |
| FIN-SE-001 | activite | Domaine d'activité | profil_demandeur == independant |
| FIN-SE-002 | anciennete_activite | Ancienneté de l'activité | profil_demandeur == independant |
| FIN-SE-003 | chiffre_affaires_mensuel | Chiffre d'affaires mensuel | profil_demandeur == independant |
| FIN-SE-005 | resultat_mensuel | Résultat net mensuel | profil_demandeur == independant |
| FIN-SE-006 | formalisation | Forme juridique | profil_demandeur == independant or entreprise |
| FIN-CONS-009 | devis_disponibles | Devis disponibles ? | always |
| FIN-COMMON-019 | documents_disponibles | Documents disponibles | always |

### Recommended Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-006 | delai_souhaite | Délai souhaité pour le financement ? |
| FIN-COMMON-016 | autres_engagements | Autres engagements financiers ? |
| FIN-CONS-004 | surface_construite | Surface concernée par la rénovation (m²) ? |
| FIN-CONS-010 | montant_devis | Montant total des devis ? |
| FIN-CONS-011 | entreprise_maitre_oeuvre | Entreprise prévue pour les travaux ? |
| FIN-CONS-013 | calendrier_travaux | Calendrier des travaux ? |
| FIN-CONS-014 | duree_chantier_estimee | Durée estimée du chantier ? |
| FIN-COMMON-023 | quartier_projet | Quartier ? |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-CONS-018 | cout_main_oeuvre | Coût de la main-d'œuvre ? |
| FIN-CONS-019 | cout_materiaux | Coût des matériaux ? |
| FIN-COMMON-012 | taux_remboursement_souhaite | Capacité de remboursement visée ? |
| FIN-COMMON-024 | accepte_taux_variable | Taux variable acceptable ? |

### Conditional Fields

| field_id | label | condition |
|----------|-------|-----------|
| FIN-CONS-010 | montant_devis | devis_disponibles == true |
| FIN-CONS-011 | entreprise_maitre_oeuvre | devis_disponibles == true or optional |
| FIN-CONS-013 | calendrier_travaux | optional but recommended |
| FIN-CONS-014 | duree_chantier_estimee | optional |
| FIN-SE-009 | documents_fiscaux | profil_demandeur == entreprise |
| FIN-CONS-002 | statut_juridique_terrain | type_bien_projet == terrain_constructible (unlikely for renovation) |

### Sensitive Fields

Standard sensitive fields: FIN-COMMON-013, FIN-COMMON-014, FIN-COMMON-016, FIN-COMMON-018, FIN-SAL-003, FIN-SAL-004, FIN-SE-003, FIN-SE-005, FIN-SE-009, FIN-SE-010.

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Votre maison est-elle en mauvais état ?" | Formulation dévalorisante; demander plutôt les travaux nécessaires |
| "Avez-vous les moyens de rembourser ?" | Formulation intrusive; utiliser la capacité de remboursement dérivée |
| "Êtes-vous sûr que les travaux en valent la peine ?" | Jugement de valeur; ne pas commenter la pertinence du projet |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | compatibilité_apparente, montant, apport, durée, garanties, type_travaux, zone |
| final_decision | Le financeur seul décide |
| derived_fields | capacite_remboursement |
| scoring_weight_montant | 0.20 |
| scoring_weight_apport_ratio | 0.20 |
| scoring_weight_garanties | 0.20 |
| scoring_weight_devis_disponibles | 0.15 |
| scoring_weight_revenus | 0.15 |
| scoring_weight_zone | 0.10 |

---

## MATRIX 5: FINANCEMENT PROMOTION IMMOBILIERE (REAL ESTATE DEVELOPMENT FINANCING)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-005 |
| canonical_name | Financement Promotion Immobilière |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | financement_promotion_immobiliere |
| requester_typology | company / investor / promoteur |
| journey_stage | SEARCH |
| description | Demande de financement pour un projet de promotion immobilière (construction de plusieurs lots, immeuble locatif, lotissement) |

### Minimum Intake Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Quel est l'objet de votre demande ? | always; value: promotion |
| FIN-COMMON-002 | montant_recherche | Quel montant de financement pour la promotion ? | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet de promotion | always |
| FIN-COMMON-004 | apport_disponible | Apport personnel/investissement | always |
| FIN-COMMON-005 | devise | Devise | always |
| FIN-COMMON-007 | localisation_projet | Localisation du projet | always |
| FIN-COMMON-008 | type_bien_projet | Type de projet de promotion | always |
| FIN-COMMON-022 | ville_projet | Ville du projet | always |
| FIN-CONS-001 | terrain_disponible | Terrain disponible pour la promotion ? | always |
| FIN-CONS-007 | permis_autorisations | Permis et autorisations obtenus ? | always |
| FIN-COMMON-010 | profil_demandeur | Profil du demandeur | always |

### Minimum Search Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement promotion | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Apport disponible | always |
| FIN-COMMON-008 | type_bien_projet | Type de promotion | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-CONS-001 | terrain_disponible | Terrain disponible ? | always |
| FIN-CONS-007 | permis_autorisations | Permis obtenus ? | always |
| FIN-CONS-013 | calendrier_travaux | Calendrier du projet | always |

### Minimum Matching Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Apport disponible | always |
| FIN-COMMON-011 | duree_souhaitee | Durée de remboursement | always |
| FIN-SE-004 | chiffre_affaires_annuel | Chiffre d'affaires annuel | profil_demandeur == entreprise |
| FIN-SE-006 | formalisation | Forme juridique | always for entreprise |
| FIN-COMMON-018 | garanties_disponibles | Garanties | always |
| FIN-COMMON-022 | ville_projet | Ville du projet | always |
| FIN-CONS-001 | terrain_disponible | Terrain disponible ? | always |
| FIN-CONS-002 | statut_juridique_terrain | Statut juridique du terrain | terrain_disponible == true |
| FIN-CONS-007 | permis_autorisations | Permis obtenus ? | always |
| FIN-CONS-003 | surface_terrain | Surface totale du terrain (m²) | always |
| FIN-CONS-004 | surface_construite | Surface totale construite prévue | always |
| FIN-CONS-011 | entreprise_maitre_oeuvre | Maître d'œuvre / promoteur | always |
| FIN-CONS-013 | calendrier_travaux | Calendrier du projet | always |

### Minimum Introduction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Adresse email professionnelle | always |
| FIN-COMMON-021 | telephone_contact | Numéro de téléphone | always |
| FIN-SE-007 | numero_rccm | Numéro RCCM de l'entreprise | profil_demandeur == entreprise |
| FIN-SE-008 | numero_contribuable | Numéro de contribuable (NIU) | profil_demandeur == entreprise |
| FIN-SE-009 | documents_fiscaux | Documents fiscaux disponibles | profil_demandeur == entreprise |
| FIN-SE-012 | effectif_employes | Effectif de l'entreprise | profil_demandeur == entreprise |

### Minimum Transaction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-SE-001 | activite | Domaine d'activité détaillé | always |
| FIN-SE-002 | anciennete_activite | Ancienneté du promoteur/entreprise | always |
| FIN-SE-004 | chiffre_affaires_annuel | Chiffre d'affaires annuel | entreprise |
| FIN-SE-006 | formalisation | Forme juridique | always |
| FIN-SE-009 | documents_fiscaux | Documents fiscaux | entreprise |
| FIN-SE-010 | releves_bancaires | Relevés bancaires | entreprise |
| FIN-CONS-002 | statut_juridique_terrain | Statut juridique du terrain | always |
| FIN-CONS-005 | plans_disponibles | Plans du projet disponibles ? | always |
| FIN-CONS-007 | permis_autorisations | Permis et autorisations | always |
| FIN-CONS-009 | devis_disponibles | Devis disponibles | always |
| FIN-CONS-010 | montant_devis | Montant des devis | devis_disponibles == true |
| FIN-CONS-011 | entreprise_maitre_oeuvre | Maître d'œuvre identifié | always |
| FIN-CONS-012 | maitre_oeuvre_qualifie | Maître d'œuvre qualifié ? | always |
| FIN-CONS-013 | calendrier_travaux | Calendrier détaillé | always |
| FIN-CONS-014 | duree_chantier_estimee | Durée totale estimée | always |
| FIN-CONS-016 | tranches_financement | Tranches de décaissement | always |
| FIN-COMMON-019 | documents_disponibles | Documents disponibles | always |
| FIN-SE-011 | promoteurs_associes | Promoteurs associés | if applicable |

### Recommended Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-006 | delai_souhaite | Délai souhaité pour le financement ? |
| FIN-COMMON-016 | autres_engagements | Autres engagements financiers ? |
| FIN-CONS-006 | type_plans | Types de plans disponibles ? |
| FIN-CONS-008 | numero_permis_construire | Numéro du permis de construire ? |
| FIN-CONS-017 | montant_premiere_tranche | Montant de la première tranche ? |
| FIN-CONS-018 | cout_main_oeuvre | Coût de la main-d'œuvre ? |
| FIN-CONS-019 | cout_materiaux | Coût des matériaux ? |
| FIN-CONS-020 | cout_terrain | Coût du terrain ? |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-023 | quartier_projet | Quartier précis ? |
| FIN-COMMON-024 | accepte_taux_variable | Taux variable acceptable ? |
| FIN-COMMON-012 | taux_remboursement_souhaite | Capacité de remboursement mensuelle ? |
| FIN-COMMON-025 | montant_recherche_min | Montant minimum acceptable ? |

### Conditional Fields

| field_id | label | condition |
|----------|-------|-----------|
| FIN-CONS-006 | type_plans | plans_disponibles == true |
| FIN-CONS-008 | numero_permis_construire | permis_construire in permis_autorisations |
| FIN-CONS-010 | montant_devis | devis_disponibles == true |
| FIN-CONS-017 | montant_premiere_tranche | tranches_financement > 1 |
| FIN-CONS-018 | cout_main_oeuvre | optional breakdown |
| FIN-CONS-019 | cout_materiaux | optional breakdown |
| FIN-CONS-020 | cout_terrain | terrain_disponible == true |
| FIN-SE-011 | promoteurs_associes | if co-promoteurs exist |

### Sensitive Fields

All sensitive fields for company profile (FIN-SE-003 through FIN-SE-005, FIN-SE-009, FIN-SE-010) plus project legal documents (FIN-CONS-002, FIN-CONS-007, FIN-CONS-008).

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Votre projet est-il rentable ?" | LAWIM n'évalue pas la rentabilité des projets |
| "Avez-vous déjà fait faillite ?" | Question discriminatoire |
| "Êtes-vous un promoteur sérieux ?" | Jugement de valeur |
| "Combien d'investisseurs avez-vous perdus ?" | Formulation négative inappropriée |
| "Le projet est-il déjà financé ailleurs ?" | Question sur d'autres financements = normale, mais formulation neutre |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | compatibilité_apparente, type_financeur_projet, montant, apport, garanties, permis_status, terrain_status, calendrier, experience_promoteur |
| final_decision | Le financeur seul décide |
| derived_fields | ratio_apport, duree_totale_projet |
| scoring_weight_montant | 0.15 |
| scoring_weight_apport_ratio | 0.20 |
| scoring_weight_permis_terrain | 0.20 |
| scoring_weight_experience | 0.15 |
| scoring_weight_garanties | 0.15 |
| scoring_weight_calendrier | 0.10 |
| scoring_weight_zone | 0.05 |

---

## MATRIX 6: PRET ADOSSE BIEN (PROPERTY-BACKED LOAN)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-006 |
| canonical_name | Prêt Adossé à un Bien |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | pret_adosse_bien |
| requester_typology | individual / company |
| journey_stage | SEARCH |
| description | Demande de prêt garanti par un bien immobilier existant en garantie hypothécaire (crédit sur gage immobilier) |

### Minimum Intake Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Quel est l'objet de votre demande de prêt ? | always |
| FIN-COMMON-002 | montant_recherche | Quel montant souhaitez-vous emprunter ? | always |
| FIN-COMMON-005 | devise | Devise | always |
| FIN-COMMON-007 | localisation_projet | Où se situe le bien donné en garantie ? | always |
| FIN-COMMON-008 | type_bien_projet | Type de bien donné en garantie | always |
| FIN-COMMON-022 | ville_projet | Ville du bien | always |
| FIN-COMMON-010 | profil_demandeur | Profil du demandeur | always |
| FIN-COMMON-018 | garanties_disponibles | Quelles garanties pouvez-vous offrir ? | always |

### Minimum Search Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant souhaité | always |
| FIN-COMMON-007 | localisation_projet | Localisation du bien en garantie | always |
| FIN-COMMON-008 | type_bien_projet | Type de bien en garantie | always |
| FIN-COMMON-018 | garanties_disponibles | Garanties offertes | always |
| FIN-COMMON-022 | ville_projet | Ville | always |

### Minimum Matching Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du prêt | always |
| FIN-COMMON-011 | duree_souhaitee | Durée de remboursement | always |
| FIN-COMMON-013 | revenus_mensuels | Revenus mensuels | profil_demandeur != entreprise |
| FIN-COMMON-018 | garanties_disponibles | Garanties disponibles | always |
| FIN-COMMON-022 | ville_projet | Ville du bien | always |
| FIN-COMMON-008 | type_bien_projet | Type de bien en garantie | always |

### Minimum Introduction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Votre email | always |
| FIN-COMMON-021 | telephone_contact | Votre téléphone | always |
| FIN-COMMON-014 | revenus_net | Revenu net | profil_demandeur != entreprise |
| FIN-COMMON-017 | capacite_remboursement | Capacité de remboursement | always (derived) |

### Minimum Transaction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-SAL-001 | employeur | Employeur | profil_demandeur == salarie |
| FIN-SAL-002 | anciennete_emploi | Ancienneté | profil_demandeur == salarie |
| FIN-SAL-005 | type_contrat | Type de contrat | profil_demandeur == salarie |
| FIN-SE-001 | activite | Activité | profil_demandeur == independant or entreprise |
| FIN-SE-002 | anciennete_activite | Ancienneté | profil_demandeur == independant or entreprise |
| FIN-SE-003 | chiffre_affaires_mensuel | Chiffre d'affaires | profil_demandeur == independant |
| FIN-SE-006 | formalisation | Forme juridique | profil_demandeur == independant or entreprise |
| FIN-CONS-002 | statut_juridique_terrain | Statut juridique du bien en garantie | always (for land/property guarantee) |
| FIN-COMMON-019 | documents_disponibles | Documents disponibles (titre foncier, etc.) | always |

### Recommended Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-003 | cout_total_projet | Valeur estimée du bien en garantie ? |
| FIN-COMMON-004 | apport_disponible | Apport disponible ? |
| FIN-COMMON-006 | delai_souhaite | Délai souhaité ? |
| FIN-COMMON-016 | autres_engagements | Autres engagements ? |
| FIN-COMMON-023 | quartier_projet | Quartier du bien ? |
| FIN-CONS-003 | surface_terrain | Surface du terrain (m²) ? |
| FIN-CONS-004 | surface_construite | Surface construite (m²) ? |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-024 | accepte_taux_variable | Taux variable acceptable ? |
| FIN-COMMON-012 | taux_remboursement_souhaite | Capacité de remboursement visée ? |
| FIN-COMMON-025 | montant_recherche_min | Montant minimum acceptable ? |
| FIN-SAL-006 | secteur_employeur | Secteur de l'employeur ? |

### Conditional Fields

| field_id | label | condition |
|----------|-------|-----------|
| FIN-CONS-002 | statut_juridique_terrain | hypotheque in garanties_disponibles or titre_foncier in garanties_disponibles |
| FIN-CONS-003 | surface_terrain | if bien is terrain |
| FIN-CONS-004 | surface_construite | if bien has construction |
| FIN-SE-009 | documents_fiscaux | profil_demandeur == entreprise |

### Sensitive Fields

Standard sensitive fields. Particularly sensitive for pret_adosse_bien: FIN-COMMON-018 (garanties_disponibles), FIN-CONS-002 (statut juridique bien en garantie) as they involve the collateral property.

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Votre bien sera saisi si vous ne remboursez pas" | Menace déguisée; l'information sur l'hypothèque est donnée par le financeur |
| "Êtes-vous prêt à perdre votre bien ?" | Formulation agressive |
| "Votre bien vaut-il vraiment ce montant ?" | LAWIM n'évalue pas la valeur des biens |
| "Avez-vous d'autres dettes ?" | Demander les engagements de façon neutre plutôt |
| "Le titre foncier est-il authentique ?" | Formulation accusatoire; demander les documents |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | compatibilité_apparente, montant, garantie_type, bien_valeur_estimee, duree, revenus, zone |
| final_decision | Le financeur seul décide |
| derived_fields | capacite_remboursement, ratio_loan_to_value = montant_recherche / valeur_estimee_bien |
| scoring_weight_montant | 0.20 |
| scoring_weight_garantie_type | 0.25 |
| scoring_weight_revenus | 0.20 |
| scoring_weight_duree | 0.10 |
| scoring_weight_zone_bien | 0.10 |
| scoring_weight_valeur_bien | 0.15 |

---

## MATRIX 7: RECHERCHE INVESTISSEUR (INVESTOR SEARCH)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-007 |
| canonical_name | Recherche Investisseur |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | recherche_investisseur |
| requester_typology | company / promoteur / individual |
| journey_stage | SEARCH |
| description | Demande de mise en relation avec des investisseurs potentiels pour un projet immobilier nécessitant des fonds propres ou un partenariat |

### Minimum Intake Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Quel est l'objet de votre recherche d'investisseur ? | always |
| FIN-COMMON-002 | montant_recherche | Quel montant recherchez-vous auprès d'investisseurs ? | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Quel est votre apport dans le projet ? | always |
| FIN-COMMON-005 | devise | Devise | always |
| FIN-COMMON-007 | localisation_projet | Où se situe le projet ? | always |
| FIN-COMMON-008 | type_bien_projet | Type de projet proposé aux investisseurs | always |
| FIN-COMMON-010 | profil_demandeur | Profil du demandeur | always |
| FIN-COMMON-022 | ville_projet | Ville du projet | always |

### Minimum Search Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant recherché auprès d'investisseurs | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Apport du demandeur | always |
| FIN-COMMON-007 | localisation_projet | Localisation du projet | always |
| FIN-COMMON-008 | type_bien_projet | Type de projet | always |
| FIN-COMMON-022 | ville_projet | Ville | always |

### Minimum Matching Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant recherché | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Apport du demandeur | always |
| FIN-COMMON-007 | localisation_projet | Localisation | always |
| FIN-COMMON-008 | type_bien_projet | Type de projet | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-SE-006 | formalisation | Forme juridique du projet | toujours si entreprise |

### Minimum Introduction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Email de contact | always |
| FIN-COMMON-021 | telephone_contact | Téléphone de contact | always |
| FIN-SE-011 | promoteurs_associes | Présentation des promoteurs du projet | always |
| FIN-COMMON-019 | documents_disponibles | Documents de présentation du projet disponibles | always |

### Minimum Transaction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-SE-001 | activite | Description détaillée du projet | always |
| FIN-SE-002 | anciennete_activite | Depuis combien de temps le projet est en développement ? | always |
| FIN-SE-006 | formalisation | Structure juridique porteuse du projet | always |
| FIN-SE-011 | promoteurs_associes | Équipe et promoteurs | always |
| FIN-CONS-005 | plans_disponibles | Plans et documents du projet disponibles ? | if applicable |
| FIN-CONS-007 | permis_autorisations | Permis et autorisations obtenus ? | if applicable |
| FIN-CONS-013 | calendrier_travaux | Calendrier prévisionnel du projet | always |
| FIN-CONS-001 | terrain_disponible | Terrain/périmètre du projet identifié ? | if applicable |
| FIN-SE-009 | documents_fiscaux | Documents financiers du projet | if entreprise |
| FIN-COMMON-019 | documents_disponibles | Business plan, étude de marché, etc. | always |

### Recommended Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-006 | delai_souhaite | Délai de recherche d'investisseur ? |
| FIN-CONS-015 | niveau_avancement | Niveau d'avancement du projet ? |
| FIN-COMMON-016 | autres_engagements | Autres financements en cours pour ce projet ? |
| FIN-SE-007 | numero_rccm | RCCM de la structure ? |
| FIN-SE-012 | effectif_employes | Taille de l'équipe ? |
| FIN-CONS-003 | surface_terrain | Surface du terrain concerné ? |
| FIN-CONS-004 | surface_construite | Surface à construire/aménager ? |
| FIN-CONS-002 | statut_juridique_terrain | Statut juridique du terrain ? |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-023 | quartier_projet | Quartier précis ? |
| FIN-COMMON-024 | accepte_taux_variable | Type de retour attendu variable/souple ? |
| FIN-COMMON-012 | taux_remboursement_souhaite | Rentabilité attendue pour l'investisseur ? |
| FIN-CONS-018 | cout_main_oeuvre | Détail main-d'œuvre ? |
| FIN-CONS-019 | cout_materiaux | Détail matériaux ? |

### Conditional Fields

| field_id | label | condition |
|----------|-------|-----------|
| FIN-CONS-002 | statut_juridique_terrain | terrain_disponible == true |
| FIN-CONS-005 | plans_disponibles | if project has architectural plans |
| FIN-CONS-007 | permis_autorisations | if project requires permits |
| FIN-CONS-013 | calendrier_travaux | if construction project |
| FIN-SE-009 | documents_fiscaux | if formalised structure exists |
| FIN-CONS-016 | tranches_financement | if project is phased |

### Sensitive Fields

FIN-COMMON-016, FIN-SE-009, FIN-SE-010, FIN-CONS-002, FIN-CONS-007. Business plan details and financial projections are also sensitive.

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Combien d'argent avez-vous déjà perdu ?" | Formulation négative et intrusive |
| "Quel est votre salaire actuel ?" | Non pertinent pour la recherche d'investisseur |
| "Avez-vous des investisseurs prêts ?" | C'est ce qu'ils cherchent; question circulaire |
| "Pourquoi les banques vous ont refusé ?" | Présomption de refus |
| "Garantie de retour sur investissement" | LAWIM ne garantit aucun rendement |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | type_projet, montant, zone, profil_porteur, stade_projet, apport |
| final_decision | L'investisseur décide seul |
| derived_fields | ratio_apport_personnel = apport / cout_total_projet |
| scoring_weight_montant | 0.15 |
| scoring_weight_apport_ratio | 0.25 |
| scoring_weight_stade_projet | 0.20 |
| scoring_weight_formalisation | 0.15 |
| scoring_weight_zone | 0.10 |
| scoring_weight_type_projet | 0.15 |

---

## MATRIX 8: COFINANCEMENT (CO-FINANCING)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-008 |
| canonical_name | Cofinancement |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | cofinancement |
| requester_typology | individual / company / investor |
| journey_stage | SEARCH |
| description | Demande de cofinancement où plusieurs parties (banques, investisseurs, institutions) contribuent au financement d'un projet immobilier |

### Minimum Intake Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Objet du cofinancement | always |
| FIN-COMMON-002 | montant_recherche | Montant total du cofinancement recherché | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Apport du demandeur | always |
| FIN-COMMON-005 | devise | Devise | always |
| FIN-COMMON-007 | localisation_projet | Localisation du projet | always |
| FIN-COMMON-008 | type_bien_projet | Type de projet | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-COMMON-010 | profil_demandeur | Profil du demandeur | always |

### Minimum Search Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant total recherché | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Apport du demandeur | always |
| FIN-COMMON-007 | localisation_projet | Localisation | always |
| FIN-COMMON-008 | type_bien_projet | Type de projet | always |
| FIN-COMMON-022 | ville_projet | Ville | always |

### Minimum Matching Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant total | always |
| FIN-COMMON-003 | cout_total_projet | Coût total | always |
| FIN-COMMON-004 | apport_disponible | Apport | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-COMMON-008 | type_bien_projet | Type de projet | always |
| FIN-SE-006 | formalisation | Forme juridique | entreprise |

### Minimum Introduction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Email | always |
| FIN-COMMON-021 | telephone_contact | Téléphone | always |
| FIN-SE-011 | promoteurs_associes | Parties prenantes au cofinancement | always |
| FIN-COMMON-019 | documents_disponibles | Documents du projet | always |

### Minimum Transaction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-SE-001 | activite | Description du projet | always |
| FIN-SE-002 | anciennete_activite | Ancienneté du projet | always |
| FIN-SE-006 | formalisation | Structure juridique | always |
| FIN-SE-011 | promoteurs_associes | Parties prenantes identifiées | always |
| FIN-CONS-005 | plans_disponibles | Plans disponibles | if applicable |
| FIN-CONS-007 | permis_autorisations | Autorisations obtenues | if applicable |
| FIN-CONS-013 | calendrier_travaux | Calendrier | if applicable |
| FIN-CONS-001 | terrain_disponible | Terrain identifié | if applicable |
| FIN-COMMON-019 | documents_disponibles | Business plan, conventions | always |

### Recommended Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-006 | delai_souhaite | Délai de mise en place du cofinancement ? |
| FIN-CONS-015 | niveau_avancement | Avancement du projet ? |
| FIN-COMMON-016 | autres_engagements | Autres financements structurels ? |
| FIN-SE-007 | numero_rccm | RCCM ? |
| FIN-CONS-016 | tranches_financement | Comment le financement est-il structuré en tranches ? |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-023 | quartier_projet | Quartier ? |
| FIN-COMMON-024 | accepte_taux_variable | Conditions flexibles ? |
| FIN-CONS-018 | cout_main_oeuvre | Détail main-d'œuvre ? |
| FIN-CONS-019 | cout_materiaux | Détail matériaux ? |
| FIN-SE-012 | effectif_employes | Effectif ? |

### Conditional Fields

| field_id | label | condition |
|----------|-------|-----------|
| FIN-CONS-002 | statut_juridique_terrain | terrain_disponible == true |
| FIN-CONS-005 | plans_disponibles | if project has plans |
| FIN-CONS-007 | permis_autorisations | if permits needed |
| FIN-CONS-013 | calendrier_travaux | if construction involved |
| FIN-SE-009 | documents_fiscaux | if formal entity exists |
| FIN-CONS-016 | tranches_financement | if phased project |

### Sensitive Fields

FIN-COMMON-016, FIN-SE-009, FIN-SE-010, FIN-CONS-002, FIN-CONS-007.

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Quels sont les noms des autres co-financeurs ?" | Confidentialité des parties |
| "Combien chaque partie apporte-t-elle ?" | Trop détaillé; demander la structure globale |
| "Le projet est-il viable ?" | LAWIM n'évalue pas la viabilité |
| "Garantie de participation" | LAWIM ne garantit pas la participation de financeurs |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | type_projet, montant, structure_cofinancement, zone, profil_demandeur |
| final_decision | Chaque co-financeur décide individuellement |
| derived_fields | ratio_apport_personnel, structure_financement (parts) |
| scoring_weight_montant | 0.20 |
| scoring_weight_apport_ratio | 0.20 |
| scoring_weight_structure | 0.20 |
| scoring_weight_formalisation | 0.15 |
| scoring_weight_type_projet | 0.15 |
| scoring_weight_zone | 0.10 |

---

## MATRIX 9: APPORT DIASPORA (DIASPORA CONTRIBUTION)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-009 |
| canonical_name | Apport Diaspora |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | apport_diaspora |
| requester_typology | diaspora |
| journey_stage | SEARCH |
| description | Demande de contribution financière de la diaspora camerounaise pour un projet immobilier, incluant les services adaptés aux investisseurs de l'étranger |

### Minimum Intake Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Objet de votre apport ? | always |
| FIN-COMMON-002 | montant_recherche | Montant de votre apport ? | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Montant que vous souhaitez apporter | always |
| FIN-COMMON-005 | devise | Devise | always |
| FIN-COMMON-007 | localisation_projet | Localisation du projet au Cameroun | always |
| FIN-COMMON-008 | type_bien_projet | Type de bien/projet visé | always |
| FIN-COMMON-022 | ville_projet | Ville du projet au Cameroun | always |
| FIN-COMMON-010 | profil_demandeur | Profil | always; diaspora |
| FIN-DIA-001 | pays_residence | Dans quel pays résidez-vous ? | always |
| FIN-DIA-004 | compte_bancaire_cameroun | Avez-vous un compte bancaire au Cameroun ? | always |

### Minimum Search Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant de l'apport | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Montant de l'apport diaspora | always |
| FIN-COMMON-022 | ville_projet | Ville au Cameroun | always |
| FIN-COMMON-008 | type_bien_projet | Type de projet | always |
| FIN-DIA-001 | pays_residence | Pays de résidence | always |
| FIN-DIA-004 | compte_bancaire_cameroun | Compte bancaire au Cameroun ? | always |

### Minimum Matching Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant de l'apport | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet | always |
| FIN-COMMON-004 | apport_disponible | Apport disponible | always |
| FIN-COMMON-022 | ville_projet | Ville du projet | always |
| FIN-COMMON-008 | type_bien_projet | Type de bien/projet | always |
| FIN-DIA-001 | pays_residence | Pays de résidence | always |
| FIN-DIA-004 | compte_bancaire_cameroun | Compte bancaire au Cameroun ? | always |
| FIN-COMMON-013 | revenus_mensuels | Revenus mensuels (source étrangère) | always |
| FIN-DIA-006 | justificatif_revenus_diaspora | Justificatifs de revenus disponibles ? | always |

### Minimum Introduction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Votre email | always |
| FIN-COMMON-021 | telephone_contact | Votre téléphone (WhatsApp de préférence) | always |
| FIN-DIA-003 | relay_local_cameroun | Avez-vous un correspondant/local relay au Cameroun ? | always |
| FIN-COMMON-019 | documents_disponibles | Quels documents pouvez-vous fournir ? | always |

### Minimum Transaction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-DIA-001 | pays_residence | Pays de résidence détaillé | always |
| FIN-DIA-002 | statut_residence | Statut de résidence (optionnel mais utile) | optional |
| FIN-DIA-004 | compte_bancaire_cameroun | Compte bancaire au Cameroun | always |
| FIN-DIA-006 | justificatif_revenus_diaspora | Type de justificatif de revenus disponible | always |
| FIN-SAL-001 | employeur | Employeur (à l'étranger) | if salaried abroad |
| FIN-SAL-002 | anciennete_emploi | Ancienneté (à l'étranger) | if salaried abroad |
| FIN-SE-001 | activite | Activité (à l'étranger) | if self-employed abroad |
| FIN-COMMON-019 | documents_disponibles | Pièce d'identité, justificatif de domicile étranger, etc. | always |

### Recommended Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-006 | delai_souhaite | Délai de réalisation ? |
| FIN-COMMON-011 | duree_souhaitee | Durée d'investissement souhaitée ? |
| FIN-DIA-005 | transfert_regulier | Effectuez-vous des transferts réguliers vers le Cameroun ? |
| FIN-COMMON-023 | quartier_projet | Quartier visé ? |
| FIN-DIA-003 | relay_local_cameroun | Personne de confiance au Cameroun ? |
| FIN-SAL-008 | banque_principale | Banque principale (étrangère) ? |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-024 | accepte_taux_variable | Conditions flexibles ? |
| FIN-COMMON-012 | taux_remboursement_souhaite | Objectif de rentabilité ? |
| FIN-COMMON-016 | autres_engagements | Autres investissements ? |
| FIN-DIA-003 | relay_local_cameroun | Correspondant local (nom et contact) ? |

### Conditional Fields

| field_id | label | condition |
|----------|-------|-----------|
| FIN-DIA-002 | statut_residence | if pays_residence known |
| FIN-DIA-005 | transfert_regulier | if compte_bancaire_cameroun == true |
| FIN-DIA-003 | relay_local_cameroun | optional but recommended |
| FIN-CONS-001 | terrain_disponible | if objet is construction or acquisition |
| FIN-CONS-002 | statut_juridique_terrain | if terrain involved |
| FIN-SAL-001 | employeur | if profil == salarie |
| FIN-SE-001 | activite | if profil == independant |

### Sensitive Fields

FIN-COMMON-013, FIN-COMMON-014, FIN-COMMON-016, FIN-DIA-004, FIN-DIA-006, FIN-SAL-003, FIN-SAL-004.

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Êtes-vous citoyen camerounais ?" | Discriminatoire; la diaspora inclut les Camerounais de l'étranger et les binationaux |
| "Avez-vous des papiers en règle ?" | Intrusif sur le statut migratoire |
| "Payez-vous des impôts au Cameroun ?" | Non pertinent |
| "Quand rentrez-vous au Cameroun ?" | Présomption de retour |
| "Votre argent est-il déclaré ?" | Accusatoire; ne pas questionner la provenance des fonds |
| "Envoyez votre passeport" | Ne jamais demander de documents d'identité; laisser l'utilisateur proposer |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | pays_residence, montant, type_projet, ville, compte_cameroun, justificatifs |
| final_decision | Le financeur ou partenaire décide |
| derived_fields | capacite_apport, ratio_apport_projet |
| diaspora_score_bonus | +20 (matching bonus) |
| scoring_weight_montant | 0.20 |
| scoring_weight_pays | 0.15 |
| scoring_weight_compte_cameroun | 0.20 |
| scoring_weight_justificatifs | 0.15 |
| scoring_weight_type_projet | 0.15 |
| scoring_weight_ville | 0.15 |

---

## MATRIX 10: FINANCEMENT PROFESSIONNEL (PROFESSIONAL / BUSINESS FINANCING)

### Matrix Metadata

| Field | Value |
|-------|-------|
| matrix_id | MATRIX-FIN-010 |
| canonical_name | Financement Professionnel |
| request_family | FINANCING_REQUEST |
| transaction_type | FINANCE |
| property_or_service_type | financement_professionnel |
| requester_typology | company / professional / independant |
| journey_stage | SEARCH |
| description | Demande de financement pour un professionnel ou une entreprise pour un projet immobilier à usage professionnel (local commercial, bureau, entrepôt, investissement professionnel) |

### Minimum Intake Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-001 | objet_financement | Quel est l'objet de votre demande de financement professionnel ? | always |
| FIN-COMMON-002 | montant_recherche | Quel montant pour votre financement professionnel ? | always |
| FIN-COMMON-003 | cout_total_projet | Coût total du projet professionnel | always |
| FIN-COMMON-004 | apport_disponible | Apport de l'entreprise/professionnel | always |
| FIN-COMMON-005 | devise | Devise | always |
| FIN-COMMON-007 | localisation_projet | Localisation du projet professionnel | always |
| FIN-COMMON-008 | type_bien_projet | Type de bien professionnel | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-COMMON-010 | profil_demandeur | Profil (entreprise / professionnel) | always |

### Minimum Search Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement professionnel | always |
| FIN-COMMON-003 | cout_total_projet | Coût total | always |
| FIN-COMMON-004 | apport_disponible | Apport | always |
| FIN-COMMON-008 | type_bien_projet | Type de bien professionnel | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-SE-001 | activite | Domaine d'activité professionnelle | always |
| FIN-SE-006 | formalisation | Forme juridique | always |

### Minimum Matching Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-002 | montant_recherche | Montant du financement | always |
| FIN-COMMON-003 | cout_total_projet | Coût total | always |
| FIN-COMMON-004 | apport_disponible | Apport | always |
| FIN-COMMON-011 | duree_souhaitee | Durée de remboursement | always |
| FIN-COMMON-022 | ville_projet | Ville | always |
| FIN-SE-001 | activite | Domaine d'activité | always |
| FIN-SE-002 | anciennete_activite | Ancienneté de l'entreprise | always |
| FIN-SE-003 | chiffre_affaires_mensuel | Chiffre d'affaires mensuel | always |
| FIN-SE-004 | chiffre_affaires_annuel | Chiffre d'affaires annuel | entreprise |
| FIN-SE-006 | formalisation | Forme juridique | always |
| FIN-COMMON-018 | garanties_disponibles | Garanties professionnelles | always |

### Minimum Introduction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-COMMON-020 | email_contact | Email professionnel | always |
| FIN-COMMON-021 | telephone_contact | Téléphone professionnel | always |
| FIN-SE-007 | numero_rccm | Numéro RCCM | always |
| FIN-SE-008 | numero_contribuable | Numéro de contribuable (NIU) | always |
| FIN-SE-012 | effectif_employes | Effectif de l'entreprise | always |
| FIN-SE-009 | documents_fiscaux | Documents fiscaux disponibles | always |
| FIN-SE-010 | releves_bancaires | Relevés bancaires professionnels | always |

### Minimum Transaction Fields

| field_id | label | question_template (FR) | mandatory_when |
|----------|-------|------------------------|----------------|
| FIN-SE-001 | activite | Description détaillée de l'activité | always |
| FIN-SE-002 | anciennete_activite | Ancienneté de l'entreprise | always |
| FIN-SE-003 | chiffre_affaires_mensuel | CA mensuel moyen | always |
| FIN-SE-004 | chiffre_affaires_annuel | CA annuel | always |
| FIN-SE-005 | resultat_mensuel | Résultat net mensuel | always |
| FIN-SE-006 | formalisation | Forme juridique et pièces justificatives | always |
| FIN-SE-007 | numero_rccm | RCCM à jour | always |
| FIN-SE-008 | numero_contribuable | NIU | always |
| FIN-SE-009 | documents_fiscaux | Bilans, liasses fiscales | always |
| FIN-SE-010 | releves_bancaires | Relevés bancaires des 3 à 6 derniers mois | always |
| FIN-SE-012 | effectif_employes | Effectif | always |
| FIN-SE-011 | promoteurs_associes | Gérants et associés | always |
| FIN-CONS-002 | statut_juridique_terrain | Statut juridique du bien professionnel | if terrain involved |
| FIN-COMMON-019 | documents_disponibles | Ensemble des documents professionnels | always |

### Recommended Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-006 | delai_souhaite | Délai de décaissement souhaité ? |
| FIN-COMMON-016 | autres_engagements | Autres crédits professionnels en cours ? |
| FIN-COMMON-024 | accepte_taux_variable | Taux variable acceptable ? |
| FIN-CONS-005 | plans_disponibles | Plans du local professionnel ? |
| FIN-CONS-009 | devis_disponibles | Devis pour aménagement professionnel ? |
| FIN-COMMON-023 | quartier_projet | Quartier d'implantation ? |

### Optional Fields

| field_id | label | question_template (FR) |
|----------|-------|------------------------|
| FIN-COMMON-025 | montant_recherche_min | Montant minimum acceptable ? |
| FIN-COMMON-012 | taux_remboursement_souhaite | Capacité de remboursement visée ? |
| FIN-CONS-003 | surface_terrain | Surface terrain (m²) ? |
| FIN-CONS-004 | surface_construite | Surface du local (m²) ? |
| FIN-CONS-018 | cout_main_oeuvre | Coût aménagement main-d'œuvre ? |
| FIN-CONS-019 | cout_materiaux | Coût aménagement matériaux ? |

### Conditional Fields

| field_id | label | condition |
|----------|-------|-----------|
| FIN-CONS-002 | statut_juridique_terrain | if terrain or land involved |
| FIN-CONS-003 | surface_terrain | if terrain involved |
| FIN-CONS-004 | surface_construite | if commercial property with construction |
| FIN-CONS-005 | plans_disponibles | if aménagement professionnel |
| FIN-CONS-009 | devis_disponibles | if travaux d'aménagement |
| FIN-CONS-013 | calendrier_travaux | if aménagement professionnel planifié |
| FIN-SE-009 | documents_fiscaux | always for entreprise |
| FIN-SE-010 | releves_bancaires | always for entreprise |

### Sensitive Fields

All business financial data: FIN-SE-003, FIN-SE-004, FIN-SE-005, FIN-SE-009, FIN-SE-010. Also FIN-COMMON-016, FIN-COMMON-018, FIN-CONS-002.

### Forbidden Questions

| forbidden_question | rationale |
|--------------------|-----------|
| "Votre entreprise est-elle rentable ?" | Jugement de valeur; LAWIM ne qualifie pas la rentabilité |
| "Combien de dettes a votre entreprise ?" | Formulation brutale; demander les engagements poliment |
| "Avez-vous déjà été en défaut de paiement ?" | Présomption de défaut |
| "Quel est le salaire des dirigeants ?" | Non pertinent et intrusif |
| "L'entreprise est-elle en difficulté ?" | Formulation négative |
| "Donnez accès à votre compte bancaire" | Ne jamais demander d'accès aux comptes |
| "Quel est votre mot de passe bancaire ?" | Ne jamais demander de mots de passe |

### Scoring & Verification Rules

| Rule | Value |
|------|-------|
| verification_required | true |
| matching_basis | compatibilité_apparente, type_activite, montant, apport, duree, CA, resultat, formalisation, garanties, zone |
| final_decision | Le financeur seul décide |
| derived_fields | capacite_remboursement_pro = CA - charges, ratio_endettement |
| scoring_weight_montant | 0.15 |
| scoring_weight_apport_ratio | 0.15 |
| scoring_weight_chiffre_affaires | 0.20 |
| scoring_weight_anciennete | 0.15 |
| scoring_weight_formalisation | 0.15 |
| scoring_weight_garanties | 0.10 |
| scoring_weight_zone | 0.10 |

---

## GLOBAL RULES (APPLY TO ALL MATRICES)

### Rule 1: No Loan Approval Promise

LAWIM ne promet jamais l'approbation d'un prêt. Le matching se fait uniquement sur la base de la compatibilité apparente entre le demandeur et les critères d'éligibilité du financeur. La décision finale appartient exclusivement au financeur (banque, microfinance, investisseur).

### Rule 2: Verification Required

`verification_required = true` for ALL financing request types. Every field must be verified before being used for matching or introduction.

### Rule 3: Matching Criteria

For all financing types, matching is based on:
- compatibilité_apparente (apparent compatibility)
- critères_éligibilité (eligibility criteria)
- type_financeur (lender type)
- montant (amount)
- apport (down payment)
- durée (duration)
- garanties (guarantees)
- zone (geographic zone)

### Rule 4: Final Decision

The final decision belongs to the lender (bank/microfinance/investor). LAWIM only facilitates introduction and matching.

### Rule 5: Sensitive Data Handling

All fields marked SENSITIVE must be:
- Encrypted at rest
- Access-restricted to the matching engine only
- Never shared with third parties without explicit user consent
- Never displayed to unauthorized users
- Logged with access audit trail

### Rule 6: Derived Fields

- `capacite_remboursement` = revenus_mensuels - autres_engagements
- `ratio_apport` = apport_disponible / cout_total_projet (expressed as percentage)
- `ratio_endettement` = autres_engagements / revenus_mensuels * 100

### Rule 7: Forbidden Actions

| Action | Rationale |
|--------|-----------|
| Promettre une approbation de prêt | LAWIM ne peut pas approuver les prêts |
| Garantir un taux d'intérêt | Les taux sont fixés par les financeurs |
| Demander des codes bancaires / mots de passe | Sécurité et confidentialité |
| Partager des informations sensibles sans consentement | RGPD et confidentialité |
| Discriminer sur la base de l'origine, religion, genre | Loi camerounaise et éthique |
| Demander des documents d'identité de façon proactive | L'utilisateur doit proposer |

### Rule 8: Question Priority System

| Priority | Meaning | Behavior |
|----------|---------|----------|
| P0 | Critical | Must be asked immediately; blocks further processing |
| P1 | High | Asked early in the conversation |
| P2 | Medium | Asked after P0 and P1 are collected |
| P3 | Low | Asked only if contextually relevant or as follow-up |

### Rule 9: Privacy Level System

| Level | Meaning | Access |
|-------|---------|--------|
| PUBLIC | Non-sensitive, visible | Visible to all authenticated users |
| PRIVATE | Personal but not financial | Visible to matching engine and authorized agents |
| SENSITIVE | Financial or legal | Encrypted; restricted to matching engine; audit trail |

### Rule 10: Confidence Levels

| Level | Meaning |
|-------|---------|
| HIGH | Field is validated and reliable; from direct user input with verification |
| MEDIUM | Field is derived or inferred; may need confirmation |
| LOW | Field is optional or speculative; collected opportunistically |

---

## FIELD REFERENCE INDEX

All field_ids used across matrices:

| field_id | Defined In | Matrices Using |
|----------|-----------|----------------|
| FIN-COMMON-001 | Common | ALL |
| FIN-COMMON-002 | Common | ALL |
| FIN-COMMON-003 | Common | ALL |
| FIN-COMMON-004 | Common | ALL |
| FIN-COMMON-005 | Common | ALL |
| FIN-COMMON-006 | Common | ALL |
| FIN-COMMON-007 | Common | ALL |
| FIN-COMMON-008 | Common | ALL |
| FIN-COMMON-009 | Common | MATRIX-001, MATRIX-002 |
| FIN-COMMON-010 | Common | ALL |
| FIN-COMMON-011 | Common | ALL |
| FIN-COMMON-012 | Common | ALL |
| FIN-COMMON-013 | Common | ALL |
| FIN-COMMON-014 | Common | ALL |
| FIN-COMMON-015 | Common | ALL |
| FIN-COMMON-016 | Common | ALL |
| FIN-COMMON-017 | Common | ALL (derived) |
| FIN-COMMON-018 | Common | ALL |
| FIN-COMMON-019 | Common | ALL |
| FIN-COMMON-020 | Common | ALL |
| FIN-COMMON-021 | Common | ALL |
| FIN-COMMON-022 | Common | ALL |
| FIN-COMMON-023 | Common | ALL |
| FIN-COMMON-024 | Common | ALL |
| FIN-COMMON-025 | Common | ALL |
| FIN-SAL-001 | Salaried | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-004, MATRIX-006, MATRIX-009 |
| FIN-SAL-002 | Salaried | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-004, MATRIX-006, MATRIX-009 |
| FIN-SAL-003 | Salaried | MATRIX-001, MATRIX-002, MATRIX-003 |
| FIN-SAL-004 | Salaried | MATRIX-001, MATRIX-002, MATRIX-003 |
| FIN-SAL-005 | Salaried | MATRIX-001, MATRIX-002, MATRIX-004, MATRIX-006 |
| FIN-SAL-006 | Salaried | MATRIX-001, MATRIX-002 |
| FIN-SAL-007 | Salaried | MATRIX-001 |
| FIN-SAL-008 | Salaried | MATRIX-001, MATRIX-009 |
| FIN-SE-001 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-004, MATRIX-005, MATRIX-006, MATRIX-007, MATRIX-008, MATRIX-009, MATRIX-010 |
| FIN-SE-002 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-004, MATRIX-005, MATRIX-006, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-SE-003 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-004, MATRIX-006, MATRIX-010 |
| FIN-SE-004 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-005, MATRIX-010 |
| FIN-SE-005 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-004, MATRIX-010 |
| FIN-SE-006 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-004, MATRIX-005, MATRIX-006, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-SE-007 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-005, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-SE-008 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-005, MATRIX-010 |
| FIN-SE-009 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-004, MATRIX-005, MATRIX-006, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-SE-010 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-005, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-SE-011 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-005, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-SE-012 | Self-Employed | MATRIX-001, MATRIX-002, MATRIX-005, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-CONS-001 | Construction | MATRIX-003, MATRIX-005, MATRIX-007, MATRIX-008, MATRIX-009 |
| FIN-CONS-002 | Construction | MATRIX-001, MATRIX-002, MATRIX-003, MATRIX-005, MATRIX-006, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-CONS-003 | Construction | MATRIX-002, MATRIX-003, MATRIX-005, MATRIX-006, MATRIX-007, MATRIX-010 |
| FIN-CONS-004 | Construction | MATRIX-003, MATRIX-004, MATRIX-005, MATRIX-006, MATRIX-007, MATRIX-010 |
| FIN-CONS-005 | Construction | MATRIX-003, MATRIX-005, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-CONS-006 | Construction | MATRIX-003, MATRIX-005 |
| FIN-CONS-007 | Construction | MATRIX-003, MATRIX-005, MATRIX-007, MATRIX-008 |
| FIN-CONS-008 | Construction | MATRIX-003, MATRIX-005 |
| FIN-CONS-009 | Construction | MATRIX-003, MATRIX-004, MATRIX-005, MATRIX-010 |
| FIN-CONS-010 | Construction | MATRIX-003, MATRIX-004, MATRIX-005 |
| FIN-CONS-011 | Construction | MATRIX-003, MATRIX-004, MATRIX-005 |
| FIN-CONS-012 | Construction | MATRIX-003, MATRIX-005 |
| FIN-CONS-013 | Construction | MATRIX-003, MATRIX-004, MATRIX-005, MATRIX-007, MATRIX-008 |
| FIN-CONS-014 | Construction | MATRIX-003, MATRIX-004, MATRIX-005 |
| FIN-CONS-015 | Construction | MATRIX-003, MATRIX-004, MATRIX-007, MATRIX-008 |
| FIN-CONS-016 | Construction | MATRIX-003, MATRIX-005, MATRIX-007, MATRIX-008 |
| FIN-CONS-017 | Construction | MATRIX-003, MATRIX-005 |
| FIN-CONS-018 | Construction | MATRIX-001, MATRIX-003, MATRIX-004, MATRIX-005, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-CONS-019 | Construction | MATRIX-001, MATRIX-003, MATRIX-004, MATRIX-005, MATRIX-007, MATRIX-008, MATRIX-010 |
| FIN-CONS-020 | Construction | MATRIX-002, MATRIX-003, MATRIX-005 |
| FIN-DIA-001 | Diaspora | MATRIX-009 |
| FIN-DIA-002 | Diaspora | MATRIX-009 |
| FIN-DIA-003 | Diaspora | MATRIX-009 |
| FIN-DIA-004 | Diaspora | MATRIX-009 |
| FIN-DIA-005 | Diaspora | MATRIX-009 |
| FIN-DIA-006 | Diaspora | MATRIX-009 |

---

## REVISION HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-15 | LAWIM Heritage Gold | Creation of complete financing request qualification matrices for all 10 financing types |

---

*Document patrimonial Gold — Toute reconstruction doit respecter ce modèle validé.*
