# Construction and Renovation Qualification Matrices — LAWIM Heritage Gold

**Document ID:** LAWIM-GOLD-MATRICES-CONSTRUCTION-RENOVATION-V1
**Mission:** LAWIM Heritage Gold — Qualification des projets de construction et rénovation
**Date:** 2026-07-15
**Statut:** CANONICAL — Reference document for architecture H1

---

# Table of Contents

| # | Service Type | Matrix ID | Category |
|---|-------------|-----------|----------|
| 1 | construction_neuve | MATRIX-CONST-001 | CONSTRUCTION |
| 2 | construction_extension | MATRIX-CONST-002 | CONSTRUCTION |
| 3 | construction_sur_terrain_nu | MATRIX-CONST-003 | CONSTRUCTION |
| 4 | renovation_complete | MATRIX-CONST-004 | RENOVATION |
| 5 | renovation_partielle | MATRIX-CONST-005 | RENOVATION |
| 6 | renovation_facade | MATRIX-CONST-006 | RENOVATION |
| 7 | amenagement_interieur | MATRIX-CONST-007 | RENOVATION |
| 8 | finition | MATRIX-CONST-008 | RENOVATION |

---

# Common Rules for All Construction and Renovation Matrices

## Qualification Order

All construction/renovation matrices follow this qualification order:

| Order | Step | Field(s) |
|:-----:|------|----------|
| 1 | Identité déclarant | FLD-CONST-IDENTITE_DECLARANT |
| 2 | Type de projet | FLD-CONST-TYPE_PROJET |
| 3 | Localisation | FLD-CONST-LOCALISATION_VILLE, FLD-CONST-LOCALISATION_QUARTIER |
| 4 | Terrain / Bien concerné | FLD-CONST-TERRAIN_DISPO, FLD-CONST-SURFACE_TERRAIN, FLD-CONST-SURFACE_CONSTRUIRE |
| 5 | Description projet | FLD-CONST-DESCRIPTION |
| 6 | Budget | FLD-CONST-BUDGET_TOTAL, FLD-CONST-BUDGET_DEVISE |
| 7 | Calendrier | FLD-CONST-DATE_DEBUT, FLD-CONST-DELAI |
| 8 | Documents existants | FLD-CONST-PLANS, FLD-CONST-PERMIS, FLD-CONST-DEVI |
| 9 | Besoins spécifiques | FLD-CONST-BESOIN_ARCHITECTE, FLD-CONST-BESOIN_INGENIEUR |
| 10 | Contact | FLD-CONST-CONTACT_NOM, FLD-CONST-CONTACT_TELEPHONE |
| 11 | Confirmation | Récapitulatif |
| 12 | Escalade | Mise en relation avec professionnels |

## Matching Role Semantics

| Role | Description |
|------|-------------|
| hard_constraint | Must match exactly; otherwise excluded |
| soft_constraint | Strong preference but flexible |
| ranking_preference | Used to rank results only |
| verification_only | For verification purposes |
| informational_only | For display only |
| transaction_blocker | Must be resolved before execution |

## Source Status Definitions

| Status | Meaning |
|--------|---------|
| HERITAGE_VALIDATED | Explicit rule from LAWIM heritage documents |
| HERITAGE_NORMALIZED | Normalized from multiple heritage sources |
| EXTERNAL_CONFIRMED | Confirmed by non-LAWIM sources |
| EXPERT_PROPOSAL | Proposed by domain expert |

## Common Forbidden Questions (All Construction/Renovation)

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres voulez-vous ?" | Déduit des besoins, pas une question directe |
| 2 | "Quel style architectural ?" | Trop vague, demander plutôt des références |
| 3 | "Avez-vous déjà construit ?" | Non pertinent |
| 4 | "Êtes-vous propriétaire ?" | Déjà couvert par identité déclarant |
| 5 | "Combien de pièces ?" | Terme non canonique |
| 6 | "Quel est votre budget mensuel ?" | Budget projet, pas mensuel |
| 7 | "Avez-vous des voisins ?" | Non pertinent |
| 8 | "Pourquoi construire maintenant ?" | Hors scope |
| 9 | "Quel est votre matériau préféré ?" | À déduire du budget/projet |
| 10 | "Avez-vous un architecte en tête ?" | Proposé comme service, pas demandé |

---

## Master Field Catalog (Construction & Renovation)

| FIELD-ID | label | data_type | allowed_values | privacy | source | confidence |
|----------|-------|-----------|----------------|--------|--------|------------|
| FLD-CONST-IDENTITE_DECLARANT | Identité déclarant | enum | PROPRIETAIRE, MANDATAIRE, PROMOTEUR, ENTREPRISE, PARTICULIER | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-TYPE_PROJET | Type de projet | enum | CONSTRUCTION_NEUVE, EXTENSION, SUR_TERRAIN_NU, RENOVATION_COMPLETE, RENOVATION_PARTIELLE, RENOVATION_FACADE, AMENAGEMENT_INTERIEUR, FINITION | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-LOCALISATION_VILLE | Ville | string | LAWIM city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-LOCALISATION_QUARTIER | Quartier | string | Per-city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-LOCALISATION_ADRESSE | Adresse chantier | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-TERRAIN_DISPO | Terrain disponible | boolean | true, false | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Statut juridique terrain | enum | TITRE_FONCIER, PROMESSE_VENTE, ACTE_VENTE, CERTIFICAT_OCCUPATION, BAIL_EMPHYTEOTIQUE, TERRAIN_FAMILIAL, NE_SAIS_PAS | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-SURFACE_TERRAIN | Surface terrain m² | float | Positive float | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-SURFACE_CONSTRUIRE | Surface à construire m² | float | Positive float | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-SURFACE_EXISTANTE | Surface existante m² | float | Positive float | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-NOMBRE_ETAGES | Nombre d'étages | integer | 1-20 | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-DESCRIPTION | Description projet | text | Free text (min 20 chars) | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-BUDGET_TOTAL | Budget total | float | Positive float | private | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-BUDGET_CONSTRUCTION | Budget construction | float | Positive float | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-BUDGET_MATERIAUX | Budget matériaux | float | Positive float | private | EXPERT_PROPOSAL | LOW |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Budget main-d'oeuvre | float | Positive float | private | EXPERT_PROPOSAL | LOW |
| FLD-CONST-BUDGET_HONORAIRES | Budget honoraires | float | Positive float | private | EXPERT_PROPOSAL | LOW |
| FLD-CONST-BUDGET_DEVISE | Devise | enum | XAF, EUR, USD | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-BUDGET_NEGOCIABLE | Négociable | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-DATE_DEBUT | Date début souhaitée | date | Valid date | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-DELAI | Délai souhaité | enum | URGENT, 1_MOIS, 3_MOIS, 6_MOIS, 1_AN, 2_ANS, PAS_DE_DELAI | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-DUREE_ESTIMEE | Durée estimée chantier | enum | 1_MOIS, 3_MOIS, 6_MOIS, 9_MOIS, 12_MOIS, 18_MOIS, 24_MOIS, 36_MOIS | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-CONST-PLANS_DISPO | Plans disponibles | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-TYPE_PLANS | Type de plans | enum[] | PLAN_ARCHITECTURAL, PLAN_FACADE, PLAN_ETAGE, PLAN_COUPE, PLAN_ELECTRIQUE, PLAN_PLOMBERIE, PLAN_STRUCTURE | public | EXPERT_PROPOSAL | LOW |
| FLD-CONST-PERMIS_CONSTRUIRE | Permis de construire | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-NUMERO_PERMIS | Numéro permis | string | Alphanumeric | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-AUTORISATIONS | Autorisations obtenues | enum[] | PERMIS_CONSTRUIRE, CERTIFICAT_URBANISME, DECLARATION_PREALABLE, AUTORISATION_VOIRIE, AUTORISATION_COPROPRIETE | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-DEVIS_DISPO | Devis disponibles | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-MONTANT_DEVIS | Montant devis | float | Positive float | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | Maître d'oeuvre | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-CONST-BESOIN_ARCHITECTE | Besoin architecte | boolean | true, false | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-BESOIN_INGENIEUR | Besoin ingénieur génie civil | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-BESOIN_GEOMETRE | Besoin géomètre | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-BESOIN_NOTAIRE | Besoin notaire | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-NIVEAU_AVANCEMENT | Niveau avancement | enum | PAS_COMMENCE, FONDATIONS, GROS_OEUVRE, SECOND_OEUVRE, FINITIONS, TERMINE | public | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-PROFESSIONNELS_RECOMMANDES | Professionnels recommandés | boolean | true, false | public | EXPERT_PROPOSAL | LOW |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | array | URLs | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-PHOTOS_TERRAIN | Photos terrain | array | URLs | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références | array | URLs | public | EXPERT_PROPOSAL | LOW |
| FLD-CONST-FINANCEMENT_DISPO | Financement disponible | boolean | true, false | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-FINANCEMENT_TYPE | Type financement | enum | COMPTANT, CREDIT_BANCAIRE, TONTINE, DIASPORA, MIXTE | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-CONTACT_NOM | Nom contact | string | Free text | private | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-CONTACT_TELEPHONE | Téléphone | string | Valid phone | private | HERITAGE_VALIDATED | HIGH |
| FLD-CONST-CONTACT_EMAIL | Email | string | Valid email | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-CONTACT_CANAL | Canal préféré | enum | WHATSAPP, TELEGRAM, SMS, EMAIL, APPEL | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-CONTACT_DISPO | Disponibilité contact | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-CONST-URGENCE | Urgence | enum | URGENT, MODERE, PAS_URGENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-CONST-COMMENTAIRE | Commentaire libre | text | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-CONST-NIVEAU_VERIFICATION | Niveau vérification | enum | COMPLET, STANDARD, MINIMAL | confidential | HERITAGE_VALIDATED | HIGH |

---

## Derived Fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-CONST-DERIVED-BUDGET_M2 | Budget au m² | budget_total / surface_construire |
| FLD-CONST-DERIVED-TERRAIN_CONSTRUCTIBLE | Constructibilité terrain | statut_juridique + zone |
| FLD-CONST-DERIVED-PROJET_COMPLETUDE | Complétude projet | weighted(champs remplis) |
| FLD-CONST-DERIVED-BUDGET_COHERENCE | Cohérence budget | budget vs marché local type/surface |
| FLD-CONST-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message + contexte |
| FLD-CONST-DERIVED-COMPLEXITE | Complexité projet | type + étages + surface |
| FLD-CONST-DERIVED-PROFIL_MAITRE_OUVRAGE | Profil maître ouvrage | type déclarant + historique |
| FLD-CONST-DERIVED-NIVEAU_PREPARATION | Niveau préparation | plans + permis + devis |

---
## MATRIX 1: construction_neuve

### matrix_id
MATRIX-CONST-001

### canonical_name
Construction Neuve

### request_family
CONSTRUCTION_RENOVATION

### transaction_type
BUILD

### property_or_service_type
construction_neuve

### requester_typology
owner_or_project_owner

### journey_stage
PLANNING

### description
Nouvelle construction sur un terrain déjà acquis ou à acquérir. Tous aspects de la construction: fondations, gros oeuvre, second oeuvre, finitions.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous le propriétaire, un promoteur ou un mandataire ?" | 10 |
| FLD-CONST-TYPE_PROJET | Type de projet | always | "Quel type de projet de construction/rénovation ?" | 20 |
| FLD-CONST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le projet ?" | 30 |
| FLD-CONST-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ou zone ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_CONSTRUIRE | Surface à construire/rénover | always | "Quelle surface est concernée (m²) ?" | 40 |
| FLD-CONST-DESCRIPTION | Description projet | always | "Décrivez votre projet en quelques phrases" | 45 |
| FLD-CONST-BUDGET_TOTAL | Budget total | always | "Quel est le budget total estimé du projet ?" | 50 |
| FLD-CONST-DATE_DEBUT | Date début | always | "Quand souhaitez-vous commencer les travaux ?" | 55 |
| FLD-CONST-DELAI | Délai souhaité | always | "Quel est votre délai souhaité ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-TERRAIN_DISPO | Terrain disponible | always | "Le terrain est-il déjà disponible ?" | 65 |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Statut juridique terrain | when terrain available | "Quel est le statut juridique du terrain ?" | 70 |
| FLD-CONST-SURFACE_TERRAIN | Surface terrain | when terrain available | "Surface du terrain en m² ?" | 75 |
| FLD-CONST-NOMBRE_ETAGES | Nombre d'étages | always | "Combien d'étages prévoyez-vous ?" | 80 |
| FLD-CONST-PLANS_DISPO | Plans disponibles | always | "Avez-vous des plans architecturaux ?" | 85 |
| FLD-CONST-PERMIS_CONSTRUIRE | Permis de construire | always | "Le permis de construire est-il obtenu ?" | 90 |
| FLD-CONST-BESOIN_ARCHITECTE | Besoin architecte | if no plans | "Avez-vous besoin d'un architecte ?" | 95 |
| FLD-CONST-BESOIN_INGENIEUR | Besoin ingénieur | if complex | "Un ingénieur génie civil est-il nécessaire ?" | 100 |
| FLD-CONST-BUDGET_DEVISE | Devise | always | "Devise du budget ?" | 105 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-CONST-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-CONST-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-CONST-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-LOCALISATION_ADRESSE | Adresse chantier | always | "Adresse précise du chantier ?" | 130 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | when renovation | "Photos de l'état actuel ?" | 135 |
| FLD-CONST-PHOTOS_TERRAIN | Photos terrain | when terrain | "Photos du terrain ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-DUREE_ESTIMEE | Durée estimée | always | "Durée estimée des travaux ?" | 145 |
| FLD-CONST-DEVIS_DISPO | Devis disponibles | always | "Avez-vous déjà des devis ?" | 150 |
| FLD-CONST-FINANCEMENT_DISPO | Financement disponible | always | "Le financement est-il déjà disponible ?" | 155 |
| FLD-CONST-FINANCEMENT_TYPE | Type financement | when financed | "Type de financement ?" | 160 |
| FLD-CONST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 165 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-CONST-BUDGET_MATERIAUX | Budget matériaux | informational_only | 170 |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Budget main-d'oeuvre | informational_only | 175 |
| FLD-CONST-BUDGET_HONORAIRES | Budget honoraires | informational_only | 180 |
| FLD-CONST-BUDGET_NEGOCIABLE | Négociable | informational_only | 185 |
| FLD-CONST-TYPE_PLANS | Type de plans | informational_only | 190 |
| FLD-CONST-NUMERO_PERMIS | Numéro permis | verification_only | 195 |
| FLD-CONST-AUTORISATIONS | Autorisations | verification_only | 200 |
| FLD-CONST-MONTANT_DEVIS | Montant devis | informational_only | 205 |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | Maître d'oeuvre | informational_only | 210 |
| FLD-CONST-BESOIN_GEOMETRE | Besoin géomètre | informational_only | 215 |
| FLD-CONST-BESOIN_NOTAIRE | Besoin notaire | informational_only | 220 |
| FLD-CONST-PROFESSIONNELS_RECOMMANDES | Recommandations | informational_only | 225 |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références | informational_only | 230 |
| FLD-CONST-URGENCE | Urgence | informational_only | 235 |
| FLD-CONST-COMMENTAIRE | Commentaire | informational_only | 240 |
### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-CONST-BUDGET_CONSTRUCTION | Budget construction seul | informational_only |
| FLD-CONST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références visuels | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | terrain_dispo = true | verification_only |
| FLD-CONST-SURFACE_TERRAIN | terrain_dispo = true | informational_only |
| FLD-CONST-SURFACE_EXISTANTE | project type = renovation | informational_only |
| FLD-CONST-NUMERO_PERMIS | permis_construire = true | verification_only |
| FLD-CONST-AUTORISATIONS | copropriété or zone protégée | verification_only |
| FLD-CONST-TYPE_PLANS | plans_dispo = true | informational_only |
| FLD-CONST-MONTANT_DEVIS | devis_dispo = true | informational_only |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | devis_dispo = true | informational_only |
| FLD-CONST-FINANCEMENT_TYPE | financement_dispo = true | informational_only |
| FLD-CONST-BESOIN_INGENIEUR | 3+ étages or structure complexe | informational_only |
| FLD-CONST-BESOIN_GEOMETRE | terrain non borné | informational_only |
| FLD-CONST-PHOTOS_EXISTANT | renovation or extension | informational_only |
| FLD-CONST-PHOTOS_TERRAIN | construction on bare land | informational_only |
| FLD-CONST-NIVEAU_AVANCEMENT | renovation_partielle | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-CONST-CONTACT_TELEPHONE | Personal contact information |
| FLD-CONST-CONTACT_NOM | Personal identity |
| FLD-CONST-CONTACT_EMAIL | Personal contact |
| FLD-CONST-BUDGET_TOTAL | Financial information |
| FLD-CONST-BUDGET_CONSTRUCTION | Financial breakdown |
| FLD-CONST-BUDGET_MATERIAUX | Financial breakdown |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Financial breakdown |
| FLD-CONST-FINANCEMENT_TYPE | Financial information |
| FLD-CONST-LOCALISATION_ADRESSE | Exact address of property |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Legal land status |
| FLD-CONST-PERMIS_CONSTRUIRE | Legal permit status |
| FLD-CONST-NUMERO_PERMIS | Permit reference number |
| FLD-CONST-AUTORISATIONS | Legal authorizations |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-CONST-DERIVED-BUDGET_M2 | Budget au m² | budget_total / surface_construire |
| FLD-CONST-DERIVED-TERRAIN_CONSTRUCTIBLE | Constructibilité | statut_juridique + zone |
| FLD-CONST-DERIVED-PROJET_COMPLETUDE | Complétude | weighted fields |
| FLD-CONST-DERIVED-BUDGET_COHERENCE | Cohérence budget | vs marché local |
| FLD-CONST-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-CONST-DERIVED-COMPLEXITE | Complexité | type + étages + surface |
| FLD-CONST-DERIVED-NIVEAU_PREPARATION | Niveau préparation | plans + permis + devis |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Déduit des besoins, question trop directe |
| 2 | "Quel style ?" | Trop vague |
| 3 | "Avez-vous déjà construit ?" | Non pertinent |
| 4 | "Êtes-vous seul décideur ?" | Hors scope |
| 5 | "Pourquoi maintenant ?" | Hors scope |
| 6 | "Quels matériaux ?" | Déduit du budget/projet |
| 7 | "Combien de pièces ?" | Non canonique |
| 8 | "Quel est votre revenu ?" | Non pertinent |
| 9 | "Avez-vous un entrepreneur ?" | Proposé comme service |
| 10 | "Avez-vous visité d'autres constructions ?" | Hors scope |

---
## MATRIX 2: construction_extension

### matrix_id
MATRIX-CONST-002

### canonical_name
Extension / Agrandissement

### request_family
CONSTRUCTION_RENOVATION

### transaction_type
BUILD

### property_or_service_type
construction_extension

### requester_typology
owner_or_project_owner

### journey_stage
PLANNING

### description
Extension d'une construction existante: ajout de pièces, surélévation, agrandissement latéral. Connexion à l'existant requiert une attention particulière.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous le propriétaire, un promoteur ou un mandataire ?" | 10 |
| FLD-CONST-TYPE_PROJET | Type de projet | always | "Quel type de projet de construction/rénovation ?" | 20 |
| FLD-CONST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le projet ?" | 30 |
| FLD-CONST-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ou zone ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_CONSTRUIRE | Surface à construire/rénover | always | "Quelle surface est concernée (m²) ?" | 40 |
| FLD-CONST-DESCRIPTION | Description projet | always | "Décrivez votre projet en quelques phrases" | 45 |
| FLD-CONST-BUDGET_TOTAL | Budget total | always | "Quel est le budget total estimé du projet ?" | 50 |
| FLD-CONST-DATE_DEBUT | Date début | always | "Quand souhaitez-vous commencer les travaux ?" | 55 |
| FLD-CONST-DELAI | Délai souhaité | always | "Quel est votre délai souhaité ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-TERRAIN_DISPO | Terrain disponible | always | "Le terrain est-il déjà disponible ?" | 65 |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Statut juridique terrain | when terrain available | "Quel est le statut juridique du terrain ?" | 70 |
| FLD-CONST-SURFACE_TERRAIN | Surface terrain | when terrain available | "Surface du terrain en m² ?" | 75 |
| FLD-CONST-NOMBRE_ETAGES | Nombre d'étages | always | "Combien d'étages prévoyez-vous ?" | 80 |
| FLD-CONST-PLANS_DISPO | Plans disponibles | always | "Avez-vous des plans architecturaux ?" | 85 |
| FLD-CONST-PERMIS_CONSTRUIRE | Permis de construire | always | "Le permis de construire est-il obtenu ?" | 90 |
| FLD-CONST-BESOIN_ARCHITECTE | Besoin architecte | if no plans | "Avez-vous besoin d'un architecte ?" | 95 |
| FLD-CONST-BESOIN_INGENIEUR | Besoin ingénieur | if complex | "Un ingénieur génie civil est-il nécessaire ?" | 100 |
| FLD-CONST-BUDGET_DEVISE | Devise | always | "Devise du budget ?" | 105 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-CONST-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-CONST-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-CONST-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-LOCALISATION_ADRESSE | Adresse chantier | always | "Adresse précise du chantier ?" | 130 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | when renovation | "Photos de l'état actuel ?" | 135 |
| FLD-CONST-PHOTOS_TERRAIN | Photos terrain | when terrain | "Photos du terrain ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-DUREE_ESTIMEE | Durée estimée | always | "Durée estimée des travaux ?" | 145 |
| FLD-CONST-DEVIS_DISPO | Devis disponibles | always | "Avez-vous déjà des devis ?" | 150 |
| FLD-CONST-FINANCEMENT_DISPO | Financement disponible | always | "Le financement est-il déjà disponible ?" | 155 |
| FLD-CONST-FINANCEMENT_TYPE | Type financement | when financed | "Type de financement ?" | 160 |
| FLD-CONST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 165 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-CONST-BUDGET_MATERIAUX | Budget matériaux | informational_only | 170 |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Budget main-d'oeuvre | informational_only | 175 |
| FLD-CONST-BUDGET_HONORAIRES | Budget honoraires | informational_only | 180 |
| FLD-CONST-BUDGET_NEGOCIABLE | Négociable | informational_only | 185 |
| FLD-CONST-TYPE_PLANS | Type de plans | informational_only | 190 |
| FLD-CONST-NUMERO_PERMIS | Numéro permis | verification_only | 195 |
| FLD-CONST-AUTORISATIONS | Autorisations | verification_only | 200 |
| FLD-CONST-MONTANT_DEVIS | Montant devis | informational_only | 205 |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | Maître d'oeuvre | informational_only | 210 |
| FLD-CONST-BESOIN_GEOMETRE | Besoin géomètre | informational_only | 215 |
| FLD-CONST-BESOIN_NOTAIRE | Besoin notaire | informational_only | 220 |
| FLD-CONST-PROFESSIONNELS_RECOMMANDES | Recommandations | informational_only | 225 |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références | informational_only | 230 |
| FLD-CONST-URGENCE | Urgence | informational_only | 235 |
| FLD-CONST-COMMENTAIRE | Commentaire | informational_only | 240 |
### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-CONST-BUDGET_CONSTRUCTION | Budget construction seul | informational_only |
| FLD-CONST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références visuels | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | terrain_dispo = true | verification_only |
| FLD-CONST-SURFACE_TERRAIN | terrain_dispo = true | informational_only |
| FLD-CONST-SURFACE_EXISTANTE | project type = renovation | informational_only |
| FLD-CONST-NUMERO_PERMIS | permis_construire = true | verification_only |
| FLD-CONST-AUTORISATIONS | copropriété or zone protégée | verification_only |
| FLD-CONST-TYPE_PLANS | plans_dispo = true | informational_only |
| FLD-CONST-MONTANT_DEVIS | devis_dispo = true | informational_only |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | devis_dispo = true | informational_only |
| FLD-CONST-FINANCEMENT_TYPE | financement_dispo = true | informational_only |
| FLD-CONST-BESOIN_INGENIEUR | 3+ étages or structure complexe | informational_only |
| FLD-CONST-BESOIN_GEOMETRE | terrain non borné | informational_only |
| FLD-CONST-PHOTOS_EXISTANT | renovation or extension | informational_only |
| FLD-CONST-PHOTOS_TERRAIN | construction on bare land | informational_only |
| FLD-CONST-NIVEAU_AVANCEMENT | renovation_partielle | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-CONST-CONTACT_TELEPHONE | Personal contact information |
| FLD-CONST-CONTACT_NOM | Personal identity |
| FLD-CONST-CONTACT_EMAIL | Personal contact |
| FLD-CONST-BUDGET_TOTAL | Financial information |
| FLD-CONST-BUDGET_CONSTRUCTION | Financial breakdown |
| FLD-CONST-BUDGET_MATERIAUX | Financial breakdown |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Financial breakdown |
| FLD-CONST-FINANCEMENT_TYPE | Financial information |
| FLD-CONST-LOCALISATION_ADRESSE | Exact address of property |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Legal land status |
| FLD-CONST-PERMIS_CONSTRUIRE | Legal permit status |
| FLD-CONST-NUMERO_PERMIS | Permit reference number |
| FLD-CONST-AUTORISATIONS | Legal authorizations |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-CONST-DERIVED-BUDGET_M2 | Budget au m² | budget_total / surface_construire |
| FLD-CONST-DERIVED-TERRAIN_CONSTRUCTIBLE | Constructibilité | statut_juridique + zone |
| FLD-CONST-DERIVED-PROJET_COMPLETUDE | Complétude | weighted fields |
| FLD-CONST-DERIVED-BUDGET_COHERENCE | Cohérence budget | vs marché local |
| FLD-CONST-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-CONST-DERIVED-COMPLEXITE | Complexité | type + étages + surface |
| FLD-CONST-DERIVED-NIVEAU_PREPARATION | Niveau préparation | plans + permis + devis |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Déduit des besoins, question trop directe |
| 2 | "Quel style ?" | Trop vague |
| 3 | "Avez-vous déjà construit ?" | Non pertinent |
| 4 | "Êtes-vous seul décideur ?" | Hors scope |
| 5 | "Pourquoi maintenant ?" | Hors scope |
| 6 | "Quels matériaux ?" | Déduit du budget/projet |
| 7 | "Combien de pièces ?" | Non canonique |
| 8 | "Quel est votre revenu ?" | Non pertinent |
| 9 | "Avez-vous un entrepreneur ?" | Proposé comme service |
| 10 | "Avez-vous visité d'autres constructions ?" | Hors scope |

---
## MATRIX 3: construction_sur_terrain_nu

### matrix_id
MATRIX-CONST-003

### canonical_name
Construction sur Terrain Nu

### request_family
CONSTRUCTION_RENOVATION

### transaction_type
BUILD

### property_or_service_type
construction_sur_terrain_nu

### requester_typology
owner_or_project_owner

### journey_stage
PLANNING

### description
Construction complète sur un terrain nu sans aucune infrastructure. Inclut viabilisation, fondations et construction complète.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous le propriétaire, un promoteur ou un mandataire ?" | 10 |
| FLD-CONST-TYPE_PROJET | Type de projet | always | "Quel type de projet de construction/rénovation ?" | 20 |
| FLD-CONST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le projet ?" | 30 |
| FLD-CONST-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ou zone ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_CONSTRUIRE | Surface à construire/rénover | always | "Quelle surface est concernée (m²) ?" | 40 |
| FLD-CONST-DESCRIPTION | Description projet | always | "Décrivez votre projet en quelques phrases" | 45 |
| FLD-CONST-BUDGET_TOTAL | Budget total | always | "Quel est le budget total estimé du projet ?" | 50 |
| FLD-CONST-DATE_DEBUT | Date début | always | "Quand souhaitez-vous commencer les travaux ?" | 55 |
| FLD-CONST-DELAI | Délai souhaité | always | "Quel est votre délai souhaité ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-TERRAIN_DISPO | Terrain disponible | always | "Le terrain est-il déjà disponible ?" | 65 |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Statut juridique terrain | when terrain available | "Quel est le statut juridique du terrain ?" | 70 |
| FLD-CONST-SURFACE_TERRAIN | Surface terrain | when terrain available | "Surface du terrain en m² ?" | 75 |
| FLD-CONST-NOMBRE_ETAGES | Nombre d'étages | always | "Combien d'étages prévoyez-vous ?" | 80 |
| FLD-CONST-PLANS_DISPO | Plans disponibles | always | "Avez-vous des plans architecturaux ?" | 85 |
| FLD-CONST-PERMIS_CONSTRUIRE | Permis de construire | always | "Le permis de construire est-il obtenu ?" | 90 |
| FLD-CONST-BESOIN_ARCHITECTE | Besoin architecte | if no plans | "Avez-vous besoin d'un architecte ?" | 95 |
| FLD-CONST-BESOIN_INGENIEUR | Besoin ingénieur | if complex | "Un ingénieur génie civil est-il nécessaire ?" | 100 |
| FLD-CONST-BUDGET_DEVISE | Devise | always | "Devise du budget ?" | 105 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-CONST-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-CONST-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-CONST-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-LOCALISATION_ADRESSE | Adresse chantier | always | "Adresse précise du chantier ?" | 130 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | when renovation | "Photos de l'état actuel ?" | 135 |
| FLD-CONST-PHOTOS_TERRAIN | Photos terrain | when terrain | "Photos du terrain ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-DUREE_ESTIMEE | Durée estimée | always | "Durée estimée des travaux ?" | 145 |
| FLD-CONST-DEVIS_DISPO | Devis disponibles | always | "Avez-vous déjà des devis ?" | 150 |
| FLD-CONST-FINANCEMENT_DISPO | Financement disponible | always | "Le financement est-il déjà disponible ?" | 155 |
| FLD-CONST-FINANCEMENT_TYPE | Type financement | when financed | "Type de financement ?" | 160 |
| FLD-CONST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 165 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-CONST-BUDGET_MATERIAUX | Budget matériaux | informational_only | 170 |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Budget main-d'oeuvre | informational_only | 175 |
| FLD-CONST-BUDGET_HONORAIRES | Budget honoraires | informational_only | 180 |
| FLD-CONST-BUDGET_NEGOCIABLE | Négociable | informational_only | 185 |
| FLD-CONST-TYPE_PLANS | Type de plans | informational_only | 190 |
| FLD-CONST-NUMERO_PERMIS | Numéro permis | verification_only | 195 |
| FLD-CONST-AUTORISATIONS | Autorisations | verification_only | 200 |
| FLD-CONST-MONTANT_DEVIS | Montant devis | informational_only | 205 |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | Maître d'oeuvre | informational_only | 210 |
| FLD-CONST-BESOIN_GEOMETRE | Besoin géomètre | informational_only | 215 |
| FLD-CONST-BESOIN_NOTAIRE | Besoin notaire | informational_only | 220 |
| FLD-CONST-PROFESSIONNELS_RECOMMANDES | Recommandations | informational_only | 225 |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références | informational_only | 230 |
| FLD-CONST-URGENCE | Urgence | informational_only | 235 |
| FLD-CONST-COMMENTAIRE | Commentaire | informational_only | 240 |
### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-CONST-BUDGET_CONSTRUCTION | Budget construction seul | informational_only |
| FLD-CONST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références visuels | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | terrain_dispo = true | verification_only |
| FLD-CONST-SURFACE_TERRAIN | terrain_dispo = true | informational_only |
| FLD-CONST-SURFACE_EXISTANTE | project type = renovation | informational_only |
| FLD-CONST-NUMERO_PERMIS | permis_construire = true | verification_only |
| FLD-CONST-AUTORISATIONS | copropriété or zone protégée | verification_only |
| FLD-CONST-TYPE_PLANS | plans_dispo = true | informational_only |
| FLD-CONST-MONTANT_DEVIS | devis_dispo = true | informational_only |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | devis_dispo = true | informational_only |
| FLD-CONST-FINANCEMENT_TYPE | financement_dispo = true | informational_only |
| FLD-CONST-BESOIN_INGENIEUR | 3+ étages or structure complexe | informational_only |
| FLD-CONST-BESOIN_GEOMETRE | terrain non borné | informational_only |
| FLD-CONST-PHOTOS_EXISTANT | renovation or extension | informational_only |
| FLD-CONST-PHOTOS_TERRAIN | construction on bare land | informational_only |
| FLD-CONST-NIVEAU_AVANCEMENT | renovation_partielle | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-CONST-CONTACT_TELEPHONE | Personal contact information |
| FLD-CONST-CONTACT_NOM | Personal identity |
| FLD-CONST-CONTACT_EMAIL | Personal contact |
| FLD-CONST-BUDGET_TOTAL | Financial information |
| FLD-CONST-BUDGET_CONSTRUCTION | Financial breakdown |
| FLD-CONST-BUDGET_MATERIAUX | Financial breakdown |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Financial breakdown |
| FLD-CONST-FINANCEMENT_TYPE | Financial information |
| FLD-CONST-LOCALISATION_ADRESSE | Exact address of property |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Legal land status |
| FLD-CONST-PERMIS_CONSTRUIRE | Legal permit status |
| FLD-CONST-NUMERO_PERMIS | Permit reference number |
| FLD-CONST-AUTORISATIONS | Legal authorizations |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-CONST-DERIVED-BUDGET_M2 | Budget au m² | budget_total / surface_construire |
| FLD-CONST-DERIVED-TERRAIN_CONSTRUCTIBLE | Constructibilité | statut_juridique + zone |
| FLD-CONST-DERIVED-PROJET_COMPLETUDE | Complétude | weighted fields |
| FLD-CONST-DERIVED-BUDGET_COHERENCE | Cohérence budget | vs marché local |
| FLD-CONST-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-CONST-DERIVED-COMPLEXITE | Complexité | type + étages + surface |
| FLD-CONST-DERIVED-NIVEAU_PREPARATION | Niveau préparation | plans + permis + devis |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Déduit des besoins, question trop directe |
| 2 | "Quel style ?" | Trop vague |
| 3 | "Avez-vous déjà construit ?" | Non pertinent |
| 4 | "Êtes-vous seul décideur ?" | Hors scope |
| 5 | "Pourquoi maintenant ?" | Hors scope |
| 6 | "Quels matériaux ?" | Déduit du budget/projet |
| 7 | "Combien de pièces ?" | Non canonique |
| 8 | "Quel est votre revenu ?" | Non pertinent |
| 9 | "Avez-vous un entrepreneur ?" | Proposé comme service |
| 10 | "Avez-vous visité d'autres constructions ?" | Hors scope |

---
## MATRIX 4: renovation_complete

### matrix_id
MATRIX-CONST-004

### canonical_name
Rénovation Complète

### request_family
CONSTRUCTION_RENOVATION

### transaction_type
BUILD

### property_or_service_type
renovation_complete

### requester_typology
owner_or_project_owner

### journey_stage
PLANNING

### description
Rénovation intégrale d'un bien existant. Peut inclure démolition intérieure, remise à neuf complète des installations techniques.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous le propriétaire, un promoteur ou un mandataire ?" | 10 |
| FLD-CONST-TYPE_PROJET | Type de projet | always | "Quel type de projet de construction/rénovation ?" | 20 |
| FLD-CONST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le projet ?" | 30 |
| FLD-CONST-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ou zone ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_CONSTRUIRE | Surface à construire/rénover | always | "Quelle surface est concernée (m²) ?" | 40 |
| FLD-CONST-DESCRIPTION | Description projet | always | "Décrivez votre projet en quelques phrases" | 45 |
| FLD-CONST-BUDGET_TOTAL | Budget total | always | "Quel est le budget total estimé du projet ?" | 50 |
| FLD-CONST-DATE_DEBUT | Date début | always | "Quand souhaitez-vous commencer les travaux ?" | 55 |
| FLD-CONST-DELAI | Délai souhaité | always | "Quel est votre délai souhaité ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_EXISTANTE | Surface existante | when renovation | "Quelle est la surface existante concernée ?" | 65 |
| FLD-CONST-NIVEAU_AVANCEMENT | Niveau avancement | when partial | "Quel est le niveau d'avancement actuel ?" | 70 |
| FLD-CONST-PLANS_DISPO | Plans disponibles | always | "Avez-vous des plans du bien ?" | 75 |
| FLD-CONST-PERMIS_CONSTRUIRE | Permis nécessaire | always | "Un permis est-il nécessaire ?" | 80 |
| FLD-CONST-BESOIN_ARCHITECTE | Besoin architecte | always | "Avez-vous besoin d'un architecte ?" | 85 |
| FLD-CONST-BESOIN_INGENIEUR | Besoin ingénieur | if structural | "Un ingénieur est-il nécessaire ?" | 90 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | always | "Pouvez-vous partager des photos de l'existant ?" | 95 |
| FLD-CONST-BUDGET_DEVISE | Devise | always | "Devise du budget ?" | 100 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-CONST-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-CONST-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-CONST-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-LOCALISATION_ADRESSE | Adresse chantier | always | "Adresse précise du chantier ?" | 130 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | when renovation | "Photos de l'état actuel ?" | 135 |
| FLD-CONST-PHOTOS_TERRAIN | Photos terrain | when terrain | "Photos du terrain ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-DUREE_ESTIMEE | Durée estimée | always | "Durée estimée des travaux ?" | 145 |
| FLD-CONST-DEVIS_DISPO | Devis disponibles | always | "Avez-vous déjà des devis ?" | 150 |
| FLD-CONST-FINANCEMENT_DISPO | Financement disponible | always | "Le financement est-il déjà disponible ?" | 155 |
| FLD-CONST-FINANCEMENT_TYPE | Type financement | when financed | "Type de financement ?" | 160 |
| FLD-CONST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 165 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-CONST-BUDGET_MATERIAUX | Budget matériaux | informational_only | 170 |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Budget main-d'oeuvre | informational_only | 175 |
| FLD-CONST-BUDGET_HONORAIRES | Budget honoraires | informational_only | 180 |
| FLD-CONST-BUDGET_NEGOCIABLE | Négociable | informational_only | 185 |
| FLD-CONST-TYPE_PLANS | Type de plans | informational_only | 190 |
| FLD-CONST-NUMERO_PERMIS | Numéro permis | verification_only | 195 |
| FLD-CONST-AUTORISATIONS | Autorisations | verification_only | 200 |
| FLD-CONST-MONTANT_DEVIS | Montant devis | informational_only | 205 |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | Maître d'oeuvre | informational_only | 210 |
| FLD-CONST-BESOIN_GEOMETRE | Besoin géomètre | informational_only | 215 |
| FLD-CONST-BESOIN_NOTAIRE | Besoin notaire | informational_only | 220 |
| FLD-CONST-PROFESSIONNELS_RECOMMANDES | Recommandations | informational_only | 225 |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références | informational_only | 230 |
| FLD-CONST-URGENCE | Urgence | informational_only | 235 |
| FLD-CONST-COMMENTAIRE | Commentaire | informational_only | 240 |
### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-CONST-BUDGET_CONSTRUCTION | Budget construction seul | informational_only |
| FLD-CONST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références visuels | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | terrain_dispo = true | verification_only |
| FLD-CONST-SURFACE_TERRAIN | terrain_dispo = true | informational_only |
| FLD-CONST-SURFACE_EXISTANTE | project type = renovation | informational_only |
| FLD-CONST-NUMERO_PERMIS | permis_construire = true | verification_only |
| FLD-CONST-AUTORISATIONS | copropriété or zone protégée | verification_only |
| FLD-CONST-TYPE_PLANS | plans_dispo = true | informational_only |
| FLD-CONST-MONTANT_DEVIS | devis_dispo = true | informational_only |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | devis_dispo = true | informational_only |
| FLD-CONST-FINANCEMENT_TYPE | financement_dispo = true | informational_only |
| FLD-CONST-BESOIN_INGENIEUR | 3+ étages or structure complexe | informational_only |
| FLD-CONST-BESOIN_GEOMETRE | terrain non borné | informational_only |
| FLD-CONST-PHOTOS_EXISTANT | renovation or extension | informational_only |
| FLD-CONST-PHOTOS_TERRAIN | construction on bare land | informational_only |
| FLD-CONST-NIVEAU_AVANCEMENT | renovation_partielle | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-CONST-CONTACT_TELEPHONE | Personal contact information |
| FLD-CONST-CONTACT_NOM | Personal identity |
| FLD-CONST-CONTACT_EMAIL | Personal contact |
| FLD-CONST-BUDGET_TOTAL | Financial information |
| FLD-CONST-BUDGET_CONSTRUCTION | Financial breakdown |
| FLD-CONST-BUDGET_MATERIAUX | Financial breakdown |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Financial breakdown |
| FLD-CONST-FINANCEMENT_TYPE | Financial information |
| FLD-CONST-LOCALISATION_ADRESSE | Exact address of property |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Legal land status |
| FLD-CONST-PERMIS_CONSTRUIRE | Legal permit status |
| FLD-CONST-NUMERO_PERMIS | Permit reference number |
| FLD-CONST-AUTORISATIONS | Legal authorizations |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-CONST-DERIVED-BUDGET_M2 | Budget au m² | budget_total / surface_construire |
| FLD-CONST-DERIVED-TERRAIN_CONSTRUCTIBLE | Constructibilité | statut_juridique + zone |
| FLD-CONST-DERIVED-PROJET_COMPLETUDE | Complétude | weighted fields |
| FLD-CONST-DERIVED-BUDGET_COHERENCE | Cohérence budget | vs marché local |
| FLD-CONST-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-CONST-DERIVED-COMPLEXITE | Complexité | type + étages + surface |
| FLD-CONST-DERIVED-NIVEAU_PREPARATION | Niveau préparation | plans + permis + devis |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Déduit des besoins, question trop directe |
| 2 | "Quel style ?" | Trop vague |
| 3 | "Avez-vous déjà construit ?" | Non pertinent |
| 4 | "Êtes-vous seul décideur ?" | Hors scope |
| 5 | "Pourquoi maintenant ?" | Hors scope |
| 6 | "Quels matériaux ?" | Déduit du budget/projet |
| 7 | "Combien de pièces ?" | Non canonique |
| 8 | "Quel est votre revenu ?" | Non pertinent |
| 9 | "Avez-vous un entrepreneur ?" | Proposé comme service |
| 10 | "Avez-vous visité d'autres constructions ?" | Hors scope |

---
## MATRIX 5: renovation_partielle

### matrix_id
MATRIX-CONST-005

### canonical_name
Rénovation Partielle

### request_family
CONSTRUCTION_RENOVATION

### transaction_type
BUILD

### property_or_service_type
renovation_partielle

### requester_typology
owner_or_project_owner

### journey_stage
PLANNING

### description
Rénovation ciblée d'une ou plusieurs pièces/systèmes. Interventions limitées sans modification structurelle majeure.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous le propriétaire, un promoteur ou un mandataire ?" | 10 |
| FLD-CONST-TYPE_PROJET | Type de projet | always | "Quel type de projet de construction/rénovation ?" | 20 |
| FLD-CONST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le projet ?" | 30 |
| FLD-CONST-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ou zone ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_CONSTRUIRE | Surface à construire/rénover | always | "Quelle surface est concernée (m²) ?" | 40 |
| FLD-CONST-DESCRIPTION | Description projet | always | "Décrivez votre projet en quelques phrases" | 45 |
| FLD-CONST-BUDGET_TOTAL | Budget total | always | "Quel est le budget total estimé du projet ?" | 50 |
| FLD-CONST-DATE_DEBUT | Date début | always | "Quand souhaitez-vous commencer les travaux ?" | 55 |
| FLD-CONST-DELAI | Délai souhaité | always | "Quel est votre délai souhaité ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_EXISTANTE | Surface existante | when renovation | "Quelle est la surface existante concernée ?" | 65 |
| FLD-CONST-NIVEAU_AVANCEMENT | Niveau avancement | when partial | "Quel est le niveau d'avancement actuel ?" | 70 |
| FLD-CONST-PLANS_DISPO | Plans disponibles | always | "Avez-vous des plans du bien ?" | 75 |
| FLD-CONST-PERMIS_CONSTRUIRE | Permis nécessaire | always | "Un permis est-il nécessaire ?" | 80 |
| FLD-CONST-BESOIN_ARCHITECTE | Besoin architecte | always | "Avez-vous besoin d'un architecte ?" | 85 |
| FLD-CONST-BESOIN_INGENIEUR | Besoin ingénieur | if structural | "Un ingénieur est-il nécessaire ?" | 90 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | always | "Pouvez-vous partager des photos de l'existant ?" | 95 |
| FLD-CONST-BUDGET_DEVISE | Devise | always | "Devise du budget ?" | 100 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-CONST-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-CONST-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-CONST-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-LOCALISATION_ADRESSE | Adresse chantier | always | "Adresse précise du chantier ?" | 130 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | when renovation | "Photos de l'état actuel ?" | 135 |
| FLD-CONST-PHOTOS_TERRAIN | Photos terrain | when terrain | "Photos du terrain ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-DUREE_ESTIMEE | Durée estimée | always | "Durée estimée des travaux ?" | 145 |
| FLD-CONST-DEVIS_DISPO | Devis disponibles | always | "Avez-vous déjà des devis ?" | 150 |
| FLD-CONST-FINANCEMENT_DISPO | Financement disponible | always | "Le financement est-il déjà disponible ?" | 155 |
| FLD-CONST-FINANCEMENT_TYPE | Type financement | when financed | "Type de financement ?" | 160 |
| FLD-CONST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 165 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-CONST-BUDGET_MATERIAUX | Budget matériaux | informational_only | 170 |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Budget main-d'oeuvre | informational_only | 175 |
| FLD-CONST-BUDGET_HONORAIRES | Budget honoraires | informational_only | 180 |
| FLD-CONST-BUDGET_NEGOCIABLE | Négociable | informational_only | 185 |
| FLD-CONST-TYPE_PLANS | Type de plans | informational_only | 190 |
| FLD-CONST-NUMERO_PERMIS | Numéro permis | verification_only | 195 |
| FLD-CONST-AUTORISATIONS | Autorisations | verification_only | 200 |
| FLD-CONST-MONTANT_DEVIS | Montant devis | informational_only | 205 |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | Maître d'oeuvre | informational_only | 210 |
| FLD-CONST-BESOIN_GEOMETRE | Besoin géomètre | informational_only | 215 |
| FLD-CONST-BESOIN_NOTAIRE | Besoin notaire | informational_only | 220 |
| FLD-CONST-PROFESSIONNELS_RECOMMANDES | Recommandations | informational_only | 225 |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références | informational_only | 230 |
| FLD-CONST-URGENCE | Urgence | informational_only | 235 |
| FLD-CONST-COMMENTAIRE | Commentaire | informational_only | 240 |
### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-CONST-BUDGET_CONSTRUCTION | Budget construction seul | informational_only |
| FLD-CONST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références visuels | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | terrain_dispo = true | verification_only |
| FLD-CONST-SURFACE_TERRAIN | terrain_dispo = true | informational_only |
| FLD-CONST-SURFACE_EXISTANTE | project type = renovation | informational_only |
| FLD-CONST-NUMERO_PERMIS | permis_construire = true | verification_only |
| FLD-CONST-AUTORISATIONS | copropriété or zone protégée | verification_only |
| FLD-CONST-TYPE_PLANS | plans_dispo = true | informational_only |
| FLD-CONST-MONTANT_DEVIS | devis_dispo = true | informational_only |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | devis_dispo = true | informational_only |
| FLD-CONST-FINANCEMENT_TYPE | financement_dispo = true | informational_only |
| FLD-CONST-BESOIN_INGENIEUR | 3+ étages or structure complexe | informational_only |
| FLD-CONST-BESOIN_GEOMETRE | terrain non borné | informational_only |
| FLD-CONST-PHOTOS_EXISTANT | renovation or extension | informational_only |
| FLD-CONST-PHOTOS_TERRAIN | construction on bare land | informational_only |
| FLD-CONST-NIVEAU_AVANCEMENT | renovation_partielle | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-CONST-CONTACT_TELEPHONE | Personal contact information |
| FLD-CONST-CONTACT_NOM | Personal identity |
| FLD-CONST-CONTACT_EMAIL | Personal contact |
| FLD-CONST-BUDGET_TOTAL | Financial information |
| FLD-CONST-BUDGET_CONSTRUCTION | Financial breakdown |
| FLD-CONST-BUDGET_MATERIAUX | Financial breakdown |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Financial breakdown |
| FLD-CONST-FINANCEMENT_TYPE | Financial information |
| FLD-CONST-LOCALISATION_ADRESSE | Exact address of property |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Legal land status |
| FLD-CONST-PERMIS_CONSTRUIRE | Legal permit status |
| FLD-CONST-NUMERO_PERMIS | Permit reference number |
| FLD-CONST-AUTORISATIONS | Legal authorizations |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-CONST-DERIVED-BUDGET_M2 | Budget au m² | budget_total / surface_construire |
| FLD-CONST-DERIVED-TERRAIN_CONSTRUCTIBLE | Constructibilité | statut_juridique + zone |
| FLD-CONST-DERIVED-PROJET_COMPLETUDE | Complétude | weighted fields |
| FLD-CONST-DERIVED-BUDGET_COHERENCE | Cohérence budget | vs marché local |
| FLD-CONST-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-CONST-DERIVED-COMPLEXITE | Complexité | type + étages + surface |
| FLD-CONST-DERIVED-NIVEAU_PREPARATION | Niveau préparation | plans + permis + devis |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Déduit des besoins, question trop directe |
| 2 | "Quel style ?" | Trop vague |
| 3 | "Avez-vous déjà construit ?" | Non pertinent |
| 4 | "Êtes-vous seul décideur ?" | Hors scope |
| 5 | "Pourquoi maintenant ?" | Hors scope |
| 6 | "Quels matériaux ?" | Déduit du budget/projet |
| 7 | "Combien de pièces ?" | Non canonique |
| 8 | "Quel est votre revenu ?" | Non pertinent |
| 9 | "Avez-vous un entrepreneur ?" | Proposé comme service |
| 10 | "Avez-vous visité d'autres constructions ?" | Hors scope |

---
## MATRIX 6: renovation_facade

### matrix_id
MATRIX-CONST-006

### canonical_name
Rénovation de Façade

### request_family
CONSTRUCTION_RENOVATION

### transaction_type
BUILD

### property_or_service_type
renovation_facade

### requester_typology
owner_or_project_owner

### journey_stage
PLANNING

### description
Rénovation extérieure: ravalement de façade, isolation extérieure, réfection toiture, menuiseries extérieures.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous le propriétaire, un promoteur ou un mandataire ?" | 10 |
| FLD-CONST-TYPE_PROJET | Type de projet | always | "Quel type de projet de construction/rénovation ?" | 20 |
| FLD-CONST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le projet ?" | 30 |
| FLD-CONST-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ou zone ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_CONSTRUIRE | Surface à construire/rénover | always | "Quelle surface est concernée (m²) ?" | 40 |
| FLD-CONST-DESCRIPTION | Description projet | always | "Décrivez votre projet en quelques phrases" | 45 |
| FLD-CONST-BUDGET_TOTAL | Budget total | always | "Quel est le budget total estimé du projet ?" | 50 |
| FLD-CONST-DATE_DEBUT | Date début | always | "Quand souhaitez-vous commencer les travaux ?" | 55 |
| FLD-CONST-DELAI | Délai souhaité | always | "Quel est votre délai souhaité ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_EXISTANTE | Surface existante | when renovation | "Quelle est la surface existante concernée ?" | 65 |
| FLD-CONST-NIVEAU_AVANCEMENT | Niveau avancement | when partial | "Quel est le niveau d'avancement actuel ?" | 70 |
| FLD-CONST-PLANS_DISPO | Plans disponibles | always | "Avez-vous des plans du bien ?" | 75 |
| FLD-CONST-PERMIS_CONSTRUIRE | Permis nécessaire | always | "Un permis est-il nécessaire ?" | 80 |
| FLD-CONST-BESOIN_ARCHITECTE | Besoin architecte | always | "Avez-vous besoin d'un architecte ?" | 85 |
| FLD-CONST-BESOIN_INGENIEUR | Besoin ingénieur | if structural | "Un ingénieur est-il nécessaire ?" | 90 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | always | "Pouvez-vous partager des photos de l'existant ?" | 95 |
| FLD-CONST-BUDGET_DEVISE | Devise | always | "Devise du budget ?" | 100 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-CONST-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-CONST-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-CONST-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-LOCALISATION_ADRESSE | Adresse chantier | always | "Adresse précise du chantier ?" | 130 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | when renovation | "Photos de l'état actuel ?" | 135 |
| FLD-CONST-PHOTOS_TERRAIN | Photos terrain | when terrain | "Photos du terrain ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-DUREE_ESTIMEE | Durée estimée | always | "Durée estimée des travaux ?" | 145 |
| FLD-CONST-DEVIS_DISPO | Devis disponibles | always | "Avez-vous déjà des devis ?" | 150 |
| FLD-CONST-FINANCEMENT_DISPO | Financement disponible | always | "Le financement est-il déjà disponible ?" | 155 |
| FLD-CONST-FINANCEMENT_TYPE | Type financement | when financed | "Type de financement ?" | 160 |
| FLD-CONST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 165 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-CONST-BUDGET_MATERIAUX | Budget matériaux | informational_only | 170 |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Budget main-d'oeuvre | informational_only | 175 |
| FLD-CONST-BUDGET_HONORAIRES | Budget honoraires | informational_only | 180 |
| FLD-CONST-BUDGET_NEGOCIABLE | Négociable | informational_only | 185 |
| FLD-CONST-TYPE_PLANS | Type de plans | informational_only | 190 |
| FLD-CONST-NUMERO_PERMIS | Numéro permis | verification_only | 195 |
| FLD-CONST-AUTORISATIONS | Autorisations | verification_only | 200 |
| FLD-CONST-MONTANT_DEVIS | Montant devis | informational_only | 205 |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | Maître d'oeuvre | informational_only | 210 |
| FLD-CONST-BESOIN_GEOMETRE | Besoin géomètre | informational_only | 215 |
| FLD-CONST-BESOIN_NOTAIRE | Besoin notaire | informational_only | 220 |
| FLD-CONST-PROFESSIONNELS_RECOMMANDES | Recommandations | informational_only | 225 |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références | informational_only | 230 |
| FLD-CONST-URGENCE | Urgence | informational_only | 235 |
| FLD-CONST-COMMENTAIRE | Commentaire | informational_only | 240 |
### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-CONST-BUDGET_CONSTRUCTION | Budget construction seul | informational_only |
| FLD-CONST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références visuels | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | terrain_dispo = true | verification_only |
| FLD-CONST-SURFACE_TERRAIN | terrain_dispo = true | informational_only |
| FLD-CONST-SURFACE_EXISTANTE | project type = renovation | informational_only |
| FLD-CONST-NUMERO_PERMIS | permis_construire = true | verification_only |
| FLD-CONST-AUTORISATIONS | copropriété or zone protégée | verification_only |
| FLD-CONST-TYPE_PLANS | plans_dispo = true | informational_only |
| FLD-CONST-MONTANT_DEVIS | devis_dispo = true | informational_only |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | devis_dispo = true | informational_only |
| FLD-CONST-FINANCEMENT_TYPE | financement_dispo = true | informational_only |
| FLD-CONST-BESOIN_INGENIEUR | 3+ étages or structure complexe | informational_only |
| FLD-CONST-BESOIN_GEOMETRE | terrain non borné | informational_only |
| FLD-CONST-PHOTOS_EXISTANT | renovation or extension | informational_only |
| FLD-CONST-PHOTOS_TERRAIN | construction on bare land | informational_only |
| FLD-CONST-NIVEAU_AVANCEMENT | renovation_partielle | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-CONST-CONTACT_TELEPHONE | Personal contact information |
| FLD-CONST-CONTACT_NOM | Personal identity |
| FLD-CONST-CONTACT_EMAIL | Personal contact |
| FLD-CONST-BUDGET_TOTAL | Financial information |
| FLD-CONST-BUDGET_CONSTRUCTION | Financial breakdown |
| FLD-CONST-BUDGET_MATERIAUX | Financial breakdown |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Financial breakdown |
| FLD-CONST-FINANCEMENT_TYPE | Financial information |
| FLD-CONST-LOCALISATION_ADRESSE | Exact address of property |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Legal land status |
| FLD-CONST-PERMIS_CONSTRUIRE | Legal permit status |
| FLD-CONST-NUMERO_PERMIS | Permit reference number |
| FLD-CONST-AUTORISATIONS | Legal authorizations |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-CONST-DERIVED-BUDGET_M2 | Budget au m² | budget_total / surface_construire |
| FLD-CONST-DERIVED-TERRAIN_CONSTRUCTIBLE | Constructibilité | statut_juridique + zone |
| FLD-CONST-DERIVED-PROJET_COMPLETUDE | Complétude | weighted fields |
| FLD-CONST-DERIVED-BUDGET_COHERENCE | Cohérence budget | vs marché local |
| FLD-CONST-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-CONST-DERIVED-COMPLEXITE | Complexité | type + étages + surface |
| FLD-CONST-DERIVED-NIVEAU_PREPARATION | Niveau préparation | plans + permis + devis |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Déduit des besoins, question trop directe |
| 2 | "Quel style ?" | Trop vague |
| 3 | "Avez-vous déjà construit ?" | Non pertinent |
| 4 | "Êtes-vous seul décideur ?" | Hors scope |
| 5 | "Pourquoi maintenant ?" | Hors scope |
| 6 | "Quels matériaux ?" | Déduit du budget/projet |
| 7 | "Combien de pièces ?" | Non canonique |
| 8 | "Quel est votre revenu ?" | Non pertinent |
| 9 | "Avez-vous un entrepreneur ?" | Proposé comme service |
| 10 | "Avez-vous visité d'autres constructions ?" | Hors scope |

---
## MATRIX 7: amenagement_interieur

### matrix_id
MATRIX-CONST-007

### canonical_name
Aménagement Intérieur

### request_family
CONSTRUCTION_RENOVATION

### transaction_type
BUILD

### property_or_service_type
amenagement_interieur

### requester_typology
owner_or_project_owner

### journey_stage
PLANNING

### description
Aménagement d'espaces intérieurs: cloisonnement, agencement cuisine/dressing, aménagement combles/sous-sol.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous le propriétaire, un promoteur ou un mandataire ?" | 10 |
| FLD-CONST-TYPE_PROJET | Type de projet | always | "Quel type de projet de construction/rénovation ?" | 20 |
| FLD-CONST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le projet ?" | 30 |
| FLD-CONST-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ou zone ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_CONSTRUIRE | Surface à construire/rénover | always | "Quelle surface est concernée (m²) ?" | 40 |
| FLD-CONST-DESCRIPTION | Description projet | always | "Décrivez votre projet en quelques phrases" | 45 |
| FLD-CONST-BUDGET_TOTAL | Budget total | always | "Quel est le budget total estimé du projet ?" | 50 |
| FLD-CONST-DATE_DEBUT | Date début | always | "Quand souhaitez-vous commencer les travaux ?" | 55 |
| FLD-CONST-DELAI | Délai souhaité | always | "Quel est votre délai souhaité ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_EXISTANTE | Surface existante | when renovation | "Quelle est la surface existante concernée ?" | 65 |
| FLD-CONST-NIVEAU_AVANCEMENT | Niveau avancement | when partial | "Quel est le niveau d'avancement actuel ?" | 70 |
| FLD-CONST-PLANS_DISPO | Plans disponibles | always | "Avez-vous des plans du bien ?" | 75 |
| FLD-CONST-PERMIS_CONSTRUIRE | Permis nécessaire | always | "Un permis est-il nécessaire ?" | 80 |
| FLD-CONST-BESOIN_ARCHITECTE | Besoin architecte | always | "Avez-vous besoin d'un architecte ?" | 85 |
| FLD-CONST-BESOIN_INGENIEUR | Besoin ingénieur | if structural | "Un ingénieur est-il nécessaire ?" | 90 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | always | "Pouvez-vous partager des photos de l'existant ?" | 95 |
| FLD-CONST-BUDGET_DEVISE | Devise | always | "Devise du budget ?" | 100 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-CONST-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-CONST-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-CONST-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-LOCALISATION_ADRESSE | Adresse chantier | always | "Adresse précise du chantier ?" | 130 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | when renovation | "Photos de l'état actuel ?" | 135 |
| FLD-CONST-PHOTOS_TERRAIN | Photos terrain | when terrain | "Photos du terrain ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-DUREE_ESTIMEE | Durée estimée | always | "Durée estimée des travaux ?" | 145 |
| FLD-CONST-DEVIS_DISPO | Devis disponibles | always | "Avez-vous déjà des devis ?" | 150 |
| FLD-CONST-FINANCEMENT_DISPO | Financement disponible | always | "Le financement est-il déjà disponible ?" | 155 |
| FLD-CONST-FINANCEMENT_TYPE | Type financement | when financed | "Type de financement ?" | 160 |
| FLD-CONST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 165 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-CONST-BUDGET_MATERIAUX | Budget matériaux | informational_only | 170 |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Budget main-d'oeuvre | informational_only | 175 |
| FLD-CONST-BUDGET_HONORAIRES | Budget honoraires | informational_only | 180 |
| FLD-CONST-BUDGET_NEGOCIABLE | Négociable | informational_only | 185 |
| FLD-CONST-TYPE_PLANS | Type de plans | informational_only | 190 |
| FLD-CONST-NUMERO_PERMIS | Numéro permis | verification_only | 195 |
| FLD-CONST-AUTORISATIONS | Autorisations | verification_only | 200 |
| FLD-CONST-MONTANT_DEVIS | Montant devis | informational_only | 205 |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | Maître d'oeuvre | informational_only | 210 |
| FLD-CONST-BESOIN_GEOMETRE | Besoin géomètre | informational_only | 215 |
| FLD-CONST-BESOIN_NOTAIRE | Besoin notaire | informational_only | 220 |
| FLD-CONST-PROFESSIONNELS_RECOMMANDES | Recommandations | informational_only | 225 |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références | informational_only | 230 |
| FLD-CONST-URGENCE | Urgence | informational_only | 235 |
| FLD-CONST-COMMENTAIRE | Commentaire | informational_only | 240 |
### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-CONST-BUDGET_CONSTRUCTION | Budget construction seul | informational_only |
| FLD-CONST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références visuels | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | terrain_dispo = true | verification_only |
| FLD-CONST-SURFACE_TERRAIN | terrain_dispo = true | informational_only |
| FLD-CONST-SURFACE_EXISTANTE | project type = renovation | informational_only |
| FLD-CONST-NUMERO_PERMIS | permis_construire = true | verification_only |
| FLD-CONST-AUTORISATIONS | copropriété or zone protégée | verification_only |
| FLD-CONST-TYPE_PLANS | plans_dispo = true | informational_only |
| FLD-CONST-MONTANT_DEVIS | devis_dispo = true | informational_only |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | devis_dispo = true | informational_only |
| FLD-CONST-FINANCEMENT_TYPE | financement_dispo = true | informational_only |
| FLD-CONST-BESOIN_INGENIEUR | 3+ étages or structure complexe | informational_only |
| FLD-CONST-BESOIN_GEOMETRE | terrain non borné | informational_only |
| FLD-CONST-PHOTOS_EXISTANT | renovation or extension | informational_only |
| FLD-CONST-PHOTOS_TERRAIN | construction on bare land | informational_only |
| FLD-CONST-NIVEAU_AVANCEMENT | renovation_partielle | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-CONST-CONTACT_TELEPHONE | Personal contact information |
| FLD-CONST-CONTACT_NOM | Personal identity |
| FLD-CONST-CONTACT_EMAIL | Personal contact |
| FLD-CONST-BUDGET_TOTAL | Financial information |
| FLD-CONST-BUDGET_CONSTRUCTION | Financial breakdown |
| FLD-CONST-BUDGET_MATERIAUX | Financial breakdown |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Financial breakdown |
| FLD-CONST-FINANCEMENT_TYPE | Financial information |
| FLD-CONST-LOCALISATION_ADRESSE | Exact address of property |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Legal land status |
| FLD-CONST-PERMIS_CONSTRUIRE | Legal permit status |
| FLD-CONST-NUMERO_PERMIS | Permit reference number |
| FLD-CONST-AUTORISATIONS | Legal authorizations |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-CONST-DERIVED-BUDGET_M2 | Budget au m² | budget_total / surface_construire |
| FLD-CONST-DERIVED-TERRAIN_CONSTRUCTIBLE | Constructibilité | statut_juridique + zone |
| FLD-CONST-DERIVED-PROJET_COMPLETUDE | Complétude | weighted fields |
| FLD-CONST-DERIVED-BUDGET_COHERENCE | Cohérence budget | vs marché local |
| FLD-CONST-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-CONST-DERIVED-COMPLEXITE | Complexité | type + étages + surface |
| FLD-CONST-DERIVED-NIVEAU_PREPARATION | Niveau préparation | plans + permis + devis |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Déduit des besoins, question trop directe |
| 2 | "Quel style ?" | Trop vague |
| 3 | "Avez-vous déjà construit ?" | Non pertinent |
| 4 | "Êtes-vous seul décideur ?" | Hors scope |
| 5 | "Pourquoi maintenant ?" | Hors scope |
| 6 | "Quels matériaux ?" | Déduit du budget/projet |
| 7 | "Combien de pièces ?" | Non canonique |
| 8 | "Quel est votre revenu ?" | Non pertinent |
| 9 | "Avez-vous un entrepreneur ?" | Proposé comme service |
| 10 | "Avez-vous visité d'autres constructions ?" | Hors scope |

---
## MATRIX 8: finition

### matrix_id
MATRIX-CONST-008

### canonical_name
Travaux de Finition

### request_family
CONSTRUCTION_RENOVATION

### transaction_type
BUILD

### property_or_service_type
finition

### requester_typology
owner_or_project_owner

### journey_stage
PLANNING

### description
Travaux de finition: peinture, carrelage, parquet, placo, plomberie finale, électricité finale, menuiseries intérieures.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous le propriétaire, un promoteur ou un mandataire ?" | 10 |
| FLD-CONST-TYPE_PROJET | Type de projet | always | "Quel type de projet de construction/rénovation ?" | 20 |
| FLD-CONST-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le projet ?" | 30 |
| FLD-CONST-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ou zone ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_CONSTRUIRE | Surface à construire/rénover | always | "Quelle surface est concernée (m²) ?" | 40 |
| FLD-CONST-DESCRIPTION | Description projet | always | "Décrivez votre projet en quelques phrases" | 45 |
| FLD-CONST-BUDGET_TOTAL | Budget total | always | "Quel est le budget total estimé du projet ?" | 50 |
| FLD-CONST-DATE_DEBUT | Date début | always | "Quand souhaitez-vous commencer les travaux ?" | 55 |
| FLD-CONST-DELAI | Délai souhaité | always | "Quel est votre délai souhaité ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-SURFACE_EXISTANTE | Surface existante | when renovation | "Quelle est la surface existante concernée ?" | 65 |
| FLD-CONST-NIVEAU_AVANCEMENT | Niveau avancement | when partial | "Quel est le niveau d'avancement actuel ?" | 70 |
| FLD-CONST-PLANS_DISPO | Plans disponibles | always | "Avez-vous des plans du bien ?" | 75 |
| FLD-CONST-PERMIS_CONSTRUIRE | Permis nécessaire | always | "Un permis est-il nécessaire ?" | 80 |
| FLD-CONST-BESOIN_ARCHITECTE | Besoin architecte | always | "Avez-vous besoin d'un architecte ?" | 85 |
| FLD-CONST-BESOIN_INGENIEUR | Besoin ingénieur | if structural | "Un ingénieur est-il nécessaire ?" | 90 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | always | "Pouvez-vous partager des photos de l'existant ?" | 95 |
| FLD-CONST-BUDGET_DEVISE | Devise | always | "Devise du budget ?" | 100 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-CONST-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-CONST-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-CONST-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-LOCALISATION_ADRESSE | Adresse chantier | always | "Adresse précise du chantier ?" | 130 |
| FLD-CONST-PHOTOS_EXISTANT | Photos existant | when renovation | "Photos de l'état actuel ?" | 135 |
| FLD-CONST-PHOTOS_TERRAIN | Photos terrain | when terrain | "Photos du terrain ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-CONST-DUREE_ESTIMEE | Durée estimée | always | "Durée estimée des travaux ?" | 145 |
| FLD-CONST-DEVIS_DISPO | Devis disponibles | always | "Avez-vous déjà des devis ?" | 150 |
| FLD-CONST-FINANCEMENT_DISPO | Financement disponible | always | "Le financement est-il déjà disponible ?" | 155 |
| FLD-CONST-FINANCEMENT_TYPE | Type financement | when financed | "Type de financement ?" | 160 |
| FLD-CONST-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 165 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-CONST-BUDGET_MATERIAUX | Budget matériaux | informational_only | 170 |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Budget main-d'oeuvre | informational_only | 175 |
| FLD-CONST-BUDGET_HONORAIRES | Budget honoraires | informational_only | 180 |
| FLD-CONST-BUDGET_NEGOCIABLE | Négociable | informational_only | 185 |
| FLD-CONST-TYPE_PLANS | Type de plans | informational_only | 190 |
| FLD-CONST-NUMERO_PERMIS | Numéro permis | verification_only | 195 |
| FLD-CONST-AUTORISATIONS | Autorisations | verification_only | 200 |
| FLD-CONST-MONTANT_DEVIS | Montant devis | informational_only | 205 |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | Maître d'oeuvre | informational_only | 210 |
| FLD-CONST-BESOIN_GEOMETRE | Besoin géomètre | informational_only | 215 |
| FLD-CONST-BESOIN_NOTAIRE | Besoin notaire | informational_only | 220 |
| FLD-CONST-PROFESSIONNELS_RECOMMANDES | Recommandations | informational_only | 225 |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références | informational_only | 230 |
| FLD-CONST-URGENCE | Urgence | informational_only | 235 |
| FLD-CONST-COMMENTAIRE | Commentaire | informational_only | 240 |
### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-CONST-BUDGET_CONSTRUCTION | Budget construction seul | informational_only |
| FLD-CONST-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-CONST-EXEMPLE_REFERENCES | Exemples / Références visuels | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | terrain_dispo = true | verification_only |
| FLD-CONST-SURFACE_TERRAIN | terrain_dispo = true | informational_only |
| FLD-CONST-SURFACE_EXISTANTE | project type = renovation | informational_only |
| FLD-CONST-NUMERO_PERMIS | permis_construire = true | verification_only |
| FLD-CONST-AUTORISATIONS | copropriété or zone protégée | verification_only |
| FLD-CONST-TYPE_PLANS | plans_dispo = true | informational_only |
| FLD-CONST-MONTANT_DEVIS | devis_dispo = true | informational_only |
| FLD-CONST-ENTREPRISE_MAITRE_OEUVRE | devis_dispo = true | informational_only |
| FLD-CONST-FINANCEMENT_TYPE | financement_dispo = true | informational_only |
| FLD-CONST-BESOIN_INGENIEUR | 3+ étages or structure complexe | informational_only |
| FLD-CONST-BESOIN_GEOMETRE | terrain non borné | informational_only |
| FLD-CONST-PHOTOS_EXISTANT | renovation or extension | informational_only |
| FLD-CONST-PHOTOS_TERRAIN | construction on bare land | informational_only |
| FLD-CONST-NIVEAU_AVANCEMENT | renovation_partielle | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-CONST-CONTACT_TELEPHONE | Personal contact information |
| FLD-CONST-CONTACT_NOM | Personal identity |
| FLD-CONST-CONTACT_EMAIL | Personal contact |
| FLD-CONST-BUDGET_TOTAL | Financial information |
| FLD-CONST-BUDGET_CONSTRUCTION | Financial breakdown |
| FLD-CONST-BUDGET_MATERIAUX | Financial breakdown |
| FLD-CONST-BUDGET_MAIN_OEUVRE | Financial breakdown |
| FLD-CONST-FINANCEMENT_TYPE | Financial information |
| FLD-CONST-LOCALISATION_ADRESSE | Exact address of property |
| FLD-CONST-STATUT_JURIDIQUE_TERRAIN | Legal land status |
| FLD-CONST-PERMIS_CONSTRUIRE | Legal permit status |
| FLD-CONST-NUMERO_PERMIS | Permit reference number |
| FLD-CONST-AUTORISATIONS | Legal authorizations |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-CONST-DERIVED-BUDGET_M2 | Budget au m² | budget_total / surface_construire |
| FLD-CONST-DERIVED-TERRAIN_CONSTRUCTIBLE | Constructibilité | statut_juridique + zone |
| FLD-CONST-DERIVED-PROJET_COMPLETUDE | Complétude | weighted fields |
| FLD-CONST-DERIVED-BUDGET_COHERENCE | Cohérence budget | vs marché local |
| FLD-CONST-DERIVED-URGENCE_REELLE | Urgence réelle | delai + message |
| FLD-CONST-DERIVED-COMPLEXITE | Complexité | type + étages + surface |
| FLD-CONST-DERIVED-NIVEAU_PREPARATION | Niveau préparation | plans + permis + devis |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Déduit des besoins, question trop directe |
| 2 | "Quel style ?" | Trop vague |
| 3 | "Avez-vous déjà construit ?" | Non pertinent |
| 4 | "Êtes-vous seul décideur ?" | Hors scope |
| 5 | "Pourquoi maintenant ?" | Hors scope |
| 6 | "Quels matériaux ?" | Déduit du budget/projet |
| 7 | "Combien de pièces ?" | Non canonique |
| 8 | "Quel est votre revenu ?" | Non pertinent |
| 9 | "Avez-vous un entrepreneur ?" | Proposé comme service |
| 10 | "Avez-vous visité d'autres constructions ?" | Hors scope |

---

# End of Document — Construction and Renovation Matrices
