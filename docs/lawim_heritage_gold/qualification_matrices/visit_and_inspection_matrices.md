# Visit and Inspection Qualification Matrices — LAWIM Heritage Gold

**Document ID:** LAWIM-GOLD-MATRICES-VISIT-INSPECTION-V1
**Mission:** LAWIM Heritage Gold — Qualification des demandes de visites et inspections
**Date:** 2026-07-15
**Statut:** CANONICAL — Reference document for architecture H1

---

# Table of Contents

| # | Service Type | Matrix ID | Category |
|---|-------------|-----------|----------|
| 1 | visite_simple | MATRIX-VISIT-001 | VISIT |
| 2 | visite_accompagnee | MATRIX-VISIT-002 | VISIT |
| 3 | contre_visite_technique | MATRIX-VISIT-003 | INSPECTION |
| 4 | inspection_etat_lieux | MATRIX-VISIT-004 | INSPECTION |
| 5 | inspection_technique | MATRIX-VISIT-005 | INSPECTION |
| 6 | evaluation_etat_bien | MATRIX-VISIT-006 | EVALUATION |

---

# Common Rules for All Visit and Inspection Matrices

## Qualification Order

| Order | Step | Field(s) |
|:-----:|------|----------|
| 1 | Identité demandeur | FLD-VISIT-IDENTITE_DEMANDEUR |
| 2 | Type de visite | FLD-VISIT-TYPE_VISITE |
| 3 | Objet de la visite | FLD-VISIT-OBJET |
| 4 | Localisation du bien | FLD-VISIT-LOCALISATION_VILLE, FLD-VISIT-LOCALISATION_QUARTIER |
| 5 | Type de bien | FLD-VISIT-TYPE_BIEN |
| 6 | Disponibilité | FLD-VISIT-DISPONIBILITE |
| 7 | Accompagnement | FLD-VISIT-NOMBRE_PERSONNES |
| 8 | Contact | FLD-VISIT-CONTACT_NOM, FLD-VISIT-CONTACT_TELEPHONE |
| 9 | Confirmation | Récapitulatif |
| 10 | Escalade | Planification visite / rapport |

## Matching Role Semantics

| Role | Description |
|------|-------------|
| hard_constraint | Must match exactly; otherwise excluded |
| soft_constraint | Strong preference but flexible |
| verification_only | For identity/authorization verification |
| informational_only | For display only |
| transaction_blocker | Must be resolved before execution |

## Source Status Definitions

| Status | Meaning |
|--------|---------|
| HERITAGE_VALIDATED | Explicit rule from LAWIM heritage documents |
| HERITAGE_NORMALIZED | Normalized from multiple heritage sources |
| EXPERT_PROPOSAL | Proposed by domain expert |

## Common Forbidden Questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Pourquoi voulez-vous visiter ?" | Hors scope, l'intention est déjà connue |
| 2 | "Quel est votre budget ?" | Déjà collecté en qualification recherche |
| 3 | "Avez-vous déjà visité d'autres biens ?" | Non pertinent |
| 4 | "Combien de pièces ?" | Terme non canonique |
| 5 | "Êtes-vous prêt à acheter ?" | Suggestif |
| 6 | "Quel est votre revenu ?" | Non pertinent pour une visite |
| 7 | "Avez-vous un agent immobilier ?" | Hors scope |
| 8 | "Pourquoi ce quartier ?" | Déjà connu |

---

## Master Field Catalog (Visit & Inspection)

| FIELD-ID | label | data_type | allowed_values | privacy | source | confidence |
|----------|-------|-----------|----------------|--------|--------|------------|
| FLD-VISIT-IDENTITE_DEMANDEUR | Identité demandeur | enum | ACHETEUR, LOCATAIRE, INVESTISSEUR, PROPRIETAIRE, AGENT, EXPERT, AUTRE | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-TYPE_VISITE | Type de visite | enum | VISITE_SIMPLE, VISITE_ACCOMPAGNEE, CONTRE_VISITE_TECHNIQUE, INSPECTION_ETAT_LIEUX, INSPECTION_TECHNIQUE, EVALUATION_ETAT | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-OBJET | Objet de la visite | text | Free text | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-LOCALISATION_VILLE | Ville | string | LAWIM city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-LOCALISATION_QUARTIER | Quartier | string | Per-city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-LOCALISATION_ADRESSE | Adresse bien | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-LOCALISATION_REPERE | Point de repère | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-VISIT-TYPE_BIEN | Type de bien | enum | STUDIO, APPARTEMENT, MAISON, VILLA, VILLA_BASSE, DUPLEX, TRIPLEX, TERRAIN, COMMERCIAL, BUREAU, LOCAL_PROFESSIONNEL, IMMEUBLE | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-REFERENCE_ANNONCE | Réf. annonce | string | Alphanumeric | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-SURFACE | Surface (m²) | float | Positive float | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-NOMBRE_CHAMBRES | Nombre chambres | integer | 0-20 | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-DISPONIBILITE_DATE | Date souhaitée | date | Valid date (future) | private | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-DISPONIBILITE_HEURE | Heure souhaitée | time | Valid time | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative date/heure | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-VISIT-DUREE_PREVUE | Durée prévue | enum | 15_MIN, 30_MIN, 1H, 2H, DEMI_JOURNEE, JOURNEE | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-NOMBRE_PERSONNES | Nombre de personnes | integer | 1-10 | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | Identité accompagnateur | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-VISIT-BESOIN_ACCOMPAGNATEUR | Accompagnateur souhaité | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-TYPE_ACCOMPAGNEMENT | Type accompagnement | enum | AGENT, PROPRIETAIRE, EXPERT, GEOMETRE, ARCHITECTE, INGENIEUR | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-MOTIF_INSPECTION | Motif inspection | text | Free text | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-PERIMETRE_INSPECTION | Périmètre inspection | enum | COMPLET, STRUCTURE, ELECTRICITE, PLOMBERIE, TOITURE, FACADE, INTERIEUR, EXTERIEUR, TOUS | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-EQUIPEMENT_INSPECTION | Équipement nécessaire | enum[] | CAMERA_THERMIQUE, ENDOSCOPE, HUMIDIMETRE, DETECTEUR_GAZ, NIVEAU_LASER, PERCHE_CAMERA, DRONE, AUTRE | public | EXPERT_PROPOSAL | LOW |
| FLD-VISIT-RAPPORT_SOUHAITE | Rapport souhaité | boolean | true, false | public | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-RAPPORT_TYPE | Type rapport | enum | SIMPLE, DETAILLE, AVEC_PHOTOS, AVEC_PRE_CONSTAT, EXPERTISE_COMPLETE | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-RAPPORT_DELAI | Délai rapport | enum | IMMEDIAT, 24H, 48H, 72H, 1_SEMAINE | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-VISIT-PRECISIONS | Précisions | text | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-VISIT-CONTACT_NOM | Nom contact | string | Free text | private | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-CONTACT_TELEPHONE | Téléphone | string | Valid phone | private | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-CONTACT_EMAIL | Email | string | Valid email | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-CONTACT_CANAL | Canal préféré | enum | WHATSAPP, TELEGRAM, SMS, EMAIL, APPEL | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Autorisation propriétaire | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Identité propriétaire | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Contact propriétaire | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-VISIT-PIECE_AUTORISATION | Pièce autorisation | string | URL | confidential | EXPERT_PROPOSAL | LOW |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Documents à fournir | enum[] | PIECE_IDENTITE, AUTORISATION, MANDAT, ORDRE_MISSION | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-NIVEAU_VERIFICATION | Niveau vérification | enum | COMPLET, STANDARD, MINIMAL | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-VISIT-URGENCE | Urgence | enum | URGENT, CETTE_SEMAINE, CE_MOIS, PAS_URGENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-VISIT-COMMENTAIRE | Commentaire | text | Free text | public | EXPERT_PROPOSAL | LOW |

---

## Derived Fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-VISIT-DERIVED-CONFIRMATION | Confirmation rendez-vous | planification + accord propriétaire |
| FLD-VISIT-DERIVED-COMPLETUDE_INSPECTION | Complétude inspection | périmètre + équipement |
| FLD-VISIT-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + motif |
| FLD-VISIT-DERIVED-PROFIL_VISITEUR | Profil visiteur | identite + historique |
| FLD-VISIT-DERIVED-RAPPORT_ATTENDU | Rapport attendu | type + délai |

---
## MATRIX 1: visite_simple

### matrix_id
MATRIX-VISIT-001

### canonical_name
Visite Simple

### request_family
VISIT_INSPECTION

### transaction_type
SERVICE

### property_or_service_type
visite_simple

### requester_typology
buyer_tenant_or_owner

### journey_stage
VISIT_OR_INSPECTION

### description
Visite standard d'un bien immobilier par un potentiel acquéreur ou locataire. Visite libre sans accompagnement technique particulier. Le visiteur se rend sur place selon les modalités définies.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Qui êtes-vous ? (acheteur, locataire, propriétaire, expert)" | 10 |
| FLD-VISIT-TYPE_VISITE | Type de visite | always | "Quel type de visite souhaitez-vous ?" | 20 |
| FLD-VISIT-OBJET | Objet de la visite | always | "Quel est l'objet de cette visite ?" | 25 |
| FLD-VISIT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le bien ?" | 30 |
| FLD-VISIT-TYPE_BIEN | Type de bien | always | "De quel type de bien s'agit-il ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ?" | 40 |
| FLD-VISIT-LOCALISATION_ADRESSE | Adresse | always | "Adresse précise du bien ?" | 45 |
| FLD-VISIT-DISPONIBILITE_DATE | Date souhaitée | always | "Quand souhaitez-vous faire la visite ?" | 50 |
| FLD-VISIT-DISPONIBILITE_HEURE | Heure souhaitée | always | "À quelle heure ?" | 55 |
| FLD-VISIT-NOMBRE_PERSONNES | Nombre de personnes | always | "Combien de personnes participeront à la visite ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-REFERENCE_ANNONCE | Réf. annonce | if known | "Avez-vous une référence d'annonce ?" | 65 |
| FLD-VISIT-DUREE_PREVUE | Durée prévue | always | "Durée prévue de la visite ?" | 70 |
| FLD-VISIT-CONTACT_CANAL | Canal contact | always | "Canal préféré pour confirmation ?" | 75 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-VISIT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-VISIT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-VISIT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative | if needed | "Date/heure alternative possible ?" | 130 |
| FLD-VISIT-PRECISIONS | Précisions | optional | "Avez-vous des précisions à apporter ?" | 135 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 140 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-VISIT-LOCALISATION_REPERE | Point de repère | informational_only | 160 |
| FLD-VISIT-REFERENCE_ANNONCE | Réf. annonce | informational_only | 165 |
| FLD-VISIT-SURFACE | Surface | informational_only | 170 |
| FLD-VISIT-NOMBRE_CHAMBRES | Chambres | informational_only | 175 |
| FLD-VISIT-DUREE_PREVUE | Durée | informational_only | 180 |
| FLD-VISIT-URGENCE | Urgence | informational_only | 185 |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | Nom accompagnateur | informational_only |
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative date | informational_only |
| FLD-VISIT-PRECISIONS | Précisions | informational_only |
| FLD-VISIT-URGENCE | Urgence | informational_only |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Documents à fournir | informational_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Contact propriétaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | visite_accompagnee or inspection | verification_only |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-PIECE_AUTORISATION | autorisation = true | verification_only |
| FLD-VISIT-RAPPORT_SOUHAITE | inspection or evaluation | informational_only |
| FLD-VISIT-RAPPORT_TYPE | rapport = true | informational_only |
| FLD-VISIT-RAPPORT_DELAI | rapport = true | informational_only |
| FLD-VISIT-EQUIPEMENT_INSPECTION | inspection technique | informational_only |
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | accompagnement personnalisé | informational_only |
| FLD-VISIT-TYPE_ACCOMPAGNEMENT | besoin_accompagnateur = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-VISIT-CONTACT_TELEPHONE | Personal contact |
| FLD-VISIT-CONTACT_NOM | Personal identity |
| FLD-VISIT-CONTACT_EMAIL | Personal contact |
| FLD-VISIT-LOCALISATION_ADRESSE | Exact address of property |
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Owner authorization |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Third-party identity |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Third-party contact |
| FLD-VISIT-PIECE_AUTORISATION | Legal authorization document |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Identity documents |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-VISIT-DERIVED-CONFIRMATION | Confirmation RDV | planification + accord |
| FLD-VISIT-DERIVED-COMPLETUDE_INSPECTION | Complétude | périmètre + équipement |
| FLD-VISIT-DERIVED-URGENCE_REELLE | Urgence | urgence + motif |
| FLD-VISIT-DERIVED-PROFIL_VISITEUR | Profil | identite + historique |
| FLD-VISIT-DERIVED-RAPPORT_ATTENDU | Rapport attendu | type + délai |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Pourquoi voulez-vous visiter ?" | Intention déjà connue |
| 2 | "Quel est votre budget ?" | Déjà collecté |
| 3 | "Avez-vous déjà visité d'autres biens ?" | Non pertinent |
| 4 | "Combien de pièces ?" | Non canonique |
| 5 | "Êtes-vous prêt à acheter ?" | Suggestif |
| 6 | "Quel est votre revenu ?" | Non pertinent |
| 7 | "Avez-vous un agent immobilier ?" | Hors scope |
| 8 | "Pourquoi ce quartier ?" | Déjà connu |

---
## MATRIX 2: visite_accompagnee

### matrix_id
MATRIX-VISIT-002

### canonical_name
Visite Accompagnée

### request_family
VISIT_INSPECTION

### transaction_type
SERVICE

### property_or_service_type
visite_accompagnee

### requester_typology
buyer_tenant_or_owner

### journey_stage
VISIT_OR_INSPECTION

### description
Visite d'un bien immobilier avec accompagnement par un agent, le propriétaire ou un expert. L'accompagnateur répond aux questions et fournit des informations détaillées.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Qui êtes-vous ? (acheteur, locataire, propriétaire, expert)" | 10 |
| FLD-VISIT-TYPE_VISITE | Type de visite | always | "Quel type de visite souhaitez-vous ?" | 20 |
| FLD-VISIT-OBJET | Objet de la visite | always | "Quel est l'objet de cette visite ?" | 25 |
| FLD-VISIT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le bien ?" | 30 |
| FLD-VISIT-TYPE_BIEN | Type de bien | always | "De quel type de bien s'agit-il ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ?" | 40 |
| FLD-VISIT-LOCALISATION_ADRESSE | Adresse | always | "Adresse précise du bien ?" | 45 |
| FLD-VISIT-DISPONIBILITE_DATE | Date souhaitée | always | "Quand souhaitez-vous faire la visite ?" | 50 |
| FLD-VISIT-DISPONIBILITE_HEURE | Heure souhaitée | always | "À quelle heure ?" | 55 |
| FLD-VISIT-NOMBRE_PERSONNES | Nombre de personnes | always | "Combien de personnes participeront à la visite ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-REFERENCE_ANNONCE | Réf. annonce | if known | "Référence de l'annonce ?" | 65 |
| FLD-VISIT-DUREE_PREVUE | Durée prévue | always | "Durée prévue ?" | 70 |
| FLD-VISIT-TYPE_ACCOMPAGNEMENT | Type accompagnement | always | "Qui souhaitez-vous comme accompagnateur ?" | 75 |
| FLD-VISIT-BESOIN_ACCOMPAGNATEUR | Accompagnateur | always | "Un accompagnateur (agent/expert) est-il nécessaire ?" | 80 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-VISIT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-VISIT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-VISIT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative | if needed | "Date/heure alternative possible ?" | 130 |
| FLD-VISIT-PRECISIONS | Précisions | optional | "Avez-vous des précisions à apporter ?" | 135 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Autorisation | always | "Avez-vous l'autorisation du propriétaire ?" | 140 |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Identité propriétaire | when authorized | "Nom du propriétaire ?" | 145 |
| FLD-VISIT-PIECE_AUTORISATION | Pièce autorisation | when needed | "Document d'autorisation ?" | 150 |
| FLD-VISIT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-VISIT-LOCALISATION_REPERE | Point de repère | informational_only | 160 |
| FLD-VISIT-REFERENCE_ANNONCE | Réf. annonce | informational_only | 165 |
| FLD-VISIT-SURFACE | Surface | informational_only | 170 |
| FLD-VISIT-NOMBRE_CHAMBRES | Chambres | informational_only | 175 |
| FLD-VISIT-DUREE_PREVUE | Durée | informational_only | 180 |
| FLD-VISIT-URGENCE | Urgence | informational_only | 185 |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | Nom accompagnateur | informational_only |
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative date | informational_only |
| FLD-VISIT-PRECISIONS | Précisions | informational_only |
| FLD-VISIT-URGENCE | Urgence | informational_only |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Documents à fournir | informational_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Contact propriétaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | visite_accompagnee or inspection | verification_only |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-PIECE_AUTORISATION | autorisation = true | verification_only |
| FLD-VISIT-RAPPORT_SOUHAITE | inspection or evaluation | informational_only |
| FLD-VISIT-RAPPORT_TYPE | rapport = true | informational_only |
| FLD-VISIT-RAPPORT_DELAI | rapport = true | informational_only |
| FLD-VISIT-EQUIPEMENT_INSPECTION | inspection technique | informational_only |
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | accompagnement personnalisé | informational_only |
| FLD-VISIT-TYPE_ACCOMPAGNEMENT | besoin_accompagnateur = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-VISIT-CONTACT_TELEPHONE | Personal contact |
| FLD-VISIT-CONTACT_NOM | Personal identity |
| FLD-VISIT-CONTACT_EMAIL | Personal contact |
| FLD-VISIT-LOCALISATION_ADRESSE | Exact address of property |
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Owner authorization |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Third-party identity |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Third-party contact |
| FLD-VISIT-PIECE_AUTORISATION | Legal authorization document |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Identity documents |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-VISIT-DERIVED-CONFIRMATION | Confirmation RDV | planification + accord |
| FLD-VISIT-DERIVED-COMPLETUDE_INSPECTION | Complétude | périmètre + équipement |
| FLD-VISIT-DERIVED-URGENCE_REELLE | Urgence | urgence + motif |
| FLD-VISIT-DERIVED-PROFIL_VISITEUR | Profil | identite + historique |
| FLD-VISIT-DERIVED-RAPPORT_ATTENDU | Rapport attendu | type + délai |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Pourquoi voulez-vous visiter ?" | Intention déjà connue |
| 2 | "Quel est votre budget ?" | Déjà collecté |
| 3 | "Avez-vous déjà visité d'autres biens ?" | Non pertinent |
| 4 | "Combien de pièces ?" | Non canonique |
| 5 | "Êtes-vous prêt à acheter ?" | Suggestif |
| 6 | "Quel est votre revenu ?" | Non pertinent |
| 7 | "Avez-vous un agent immobilier ?" | Hors scope |
| 8 | "Pourquoi ce quartier ?" | Déjà connu |

---
## MATRIX 3: contre_visite_technique

### matrix_id
MATRIX-VISIT-003

### canonical_name
Contre-Visite Technique

### request_family
VISIT_INSPECTION

### transaction_type
SERVICE

### property_or_service_type
contre_visite_technique

### requester_typology
buyer_tenant_or_owner

### journey_stage
VISIT_OR_INSPECTION

### description
Seconde visite à caractère technique permettant à l'acheteur potentiel de faire examiner le bien par un expert (architecte, ingénieur, artisan) avant engagement.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Qui êtes-vous ? (acheteur, locataire, propriétaire, expert)" | 10 |
| FLD-VISIT-TYPE_VISITE | Type de visite | always | "Quel type de visite souhaitez-vous ?" | 20 |
| FLD-VISIT-OBJET | Objet de la visite | always | "Quel est l'objet de cette visite ?" | 25 |
| FLD-VISIT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le bien ?" | 30 |
| FLD-VISIT-TYPE_BIEN | Type de bien | always | "De quel type de bien s'agit-il ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ?" | 40 |
| FLD-VISIT-LOCALISATION_ADRESSE | Adresse | always | "Adresse précise du bien ?" | 45 |
| FLD-VISIT-DISPONIBILITE_DATE | Date souhaitée | always | "Quand souhaitez-vous faire la visite ?" | 50 |
| FLD-VISIT-DISPONIBILITE_HEURE | Heure souhaitée | always | "À quelle heure ?" | 55 |
| FLD-VISIT-NOMBRE_PERSONNES | Nombre de personnes | always | "Combien de personnes participeront à la visite ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-DUREE_PREVUE | Durée prévue | always | "Durée prévue ?" | 65 |
| FLD-VISIT-PERIMETRE_INSPECTION | Périmètre inspection | always | "Quels aspects souhaitez-vous examiner ?" | 70 |
| FLD-VISIT-EQUIPEMENT_INSPECTION | Équipement | if needed | "Équipement particulier nécessaire ?" | 75 |
| FLD-VISIT-TYPE_ACCOMPAGNEMENT | Accompagnement | always | "Quel expert vous accompagne ?" | 80 |
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | Expert accompagnant | always | "Nom de l'expert qui vous accompagne ?" | 85 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-VISIT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-VISIT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-VISIT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative | if needed | "Date/heure alternative possible ?" | 130 |
| FLD-VISIT-PRECISIONS | Précisions | optional | "Avez-vous des précisions à apporter ?" | 135 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Autorisation | always | "Avez-vous l'autorisation du propriétaire ?" | 140 |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Identité propriétaire | when authorized | "Nom du propriétaire ?" | 145 |
| FLD-VISIT-PIECE_AUTORISATION | Pièce autorisation | when needed | "Document d'autorisation ?" | 150 |
| FLD-VISIT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-VISIT-LOCALISATION_REPERE | Point de repère | informational_only | 160 |
| FLD-VISIT-REFERENCE_ANNONCE | Réf. annonce | informational_only | 165 |
| FLD-VISIT-SURFACE | Surface | informational_only | 170 |
| FLD-VISIT-NOMBRE_CHAMBRES | Chambres | informational_only | 175 |
| FLD-VISIT-DUREE_PREVUE | Durée | informational_only | 180 |
| FLD-VISIT-URGENCE | Urgence | informational_only | 185 |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | Nom accompagnateur | informational_only |
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative date | informational_only |
| FLD-VISIT-PRECISIONS | Précisions | informational_only |
| FLD-VISIT-URGENCE | Urgence | informational_only |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Documents à fournir | informational_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Contact propriétaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | visite_accompagnee or inspection | verification_only |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-PIECE_AUTORISATION | autorisation = true | verification_only |
| FLD-VISIT-RAPPORT_SOUHAITE | inspection or evaluation | informational_only |
| FLD-VISIT-RAPPORT_TYPE | rapport = true | informational_only |
| FLD-VISIT-RAPPORT_DELAI | rapport = true | informational_only |
| FLD-VISIT-EQUIPEMENT_INSPECTION | inspection technique | informational_only |
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | accompagnement personnalisé | informational_only |
| FLD-VISIT-TYPE_ACCOMPAGNEMENT | besoin_accompagnateur = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-VISIT-CONTACT_TELEPHONE | Personal contact |
| FLD-VISIT-CONTACT_NOM | Personal identity |
| FLD-VISIT-CONTACT_EMAIL | Personal contact |
| FLD-VISIT-LOCALISATION_ADRESSE | Exact address of property |
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Owner authorization |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Third-party identity |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Third-party contact |
| FLD-VISIT-PIECE_AUTORISATION | Legal authorization document |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Identity documents |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-VISIT-DERIVED-CONFIRMATION | Confirmation RDV | planification + accord |
| FLD-VISIT-DERIVED-COMPLETUDE_INSPECTION | Complétude | périmètre + équipement |
| FLD-VISIT-DERIVED-URGENCE_REELLE | Urgence | urgence + motif |
| FLD-VISIT-DERIVED-PROFIL_VISITEUR | Profil | identite + historique |
| FLD-VISIT-DERIVED-RAPPORT_ATTENDU | Rapport attendu | type + délai |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Pourquoi voulez-vous visiter ?" | Intention déjà connue |
| 2 | "Quel est votre budget ?" | Déjà collecté |
| 3 | "Avez-vous déjà visité d'autres biens ?" | Non pertinent |
| 4 | "Combien de pièces ?" | Non canonique |
| 5 | "Êtes-vous prêt à acheter ?" | Suggestif |
| 6 | "Quel est votre revenu ?" | Non pertinent |
| 7 | "Avez-vous un agent immobilier ?" | Hors scope |
| 8 | "Pourquoi ce quartier ?" | Déjà connu |

---
## MATRIX 4: inspection_etat_lieux

### matrix_id
MATRIX-VISIT-004

### canonical_name
Inspection État des Lieux

### request_family
VISIT_INSPECTION

### transaction_type
SERVICE

### property_or_service_type
inspection_etat_lieux

### requester_typology
buyer_tenant_or_owner

### journey_stage
VISIT_OR_INSPECTION

### description
Inspection détaillée de l'état d'un bien dans le cadre d'un état des lieux d'entrée ou de sortie. Constat contradictoire de l'état du bien.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Qui êtes-vous ? (acheteur, locataire, propriétaire, expert)" | 10 |
| FLD-VISIT-TYPE_VISITE | Type de visite | always | "Quel type de visite souhaitez-vous ?" | 20 |
| FLD-VISIT-OBJET | Objet de la visite | always | "Quel est l'objet de cette visite ?" | 25 |
| FLD-VISIT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le bien ?" | 30 |
| FLD-VISIT-TYPE_BIEN | Type de bien | always | "De quel type de bien s'agit-il ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ?" | 40 |
| FLD-VISIT-LOCALISATION_ADRESSE | Adresse | always | "Adresse précise du bien ?" | 45 |
| FLD-VISIT-DISPONIBILITE_DATE | Date souhaitée | always | "Quand souhaitez-vous faire la visite ?" | 50 |
| FLD-VISIT-DISPONIBILITE_HEURE | Heure souhaitée | always | "À quelle heure ?" | 55 |
| FLD-VISIT-NOMBRE_PERSONNES | Nombre de personnes | always | "Combien de personnes participeront à la visite ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-PERIMETRE_INSPECTION | Périmètre | always | "Périmètre de l'état des lieux ?" | 65 |
| FLD-VISIT-DUREE_PREVUE | Durée prévue | always | "Durée estimée ?" | 70 |
| FLD-VISIT-RAPPORT_SOUHAITE | Rapport souhaité | always | "Souhaitez-vous un rapport écrit ?" | 75 |
| FLD-VISIT-RAPPORT_TYPE | Type rapport | when rapport | "Quel niveau de détail pour le rapport ?" | 80 |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Documents | always | "Quels documents pouvez-vous fournir ?" | 85 |
| FLD-VISIT-BESOIN_ACCOMPAGNATEUR | Accompagnateur | always | "Un accompagnateur (agent, huissier) ?" | 90 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-VISIT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-VISIT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-VISIT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative | if needed | "Date/heure alternative possible ?" | 130 |
| FLD-VISIT-PRECISIONS | Précisions | optional | "Avez-vous des précisions à apporter ?" | 135 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Autorisation | always | "Avez-vous l'autorisation du propriétaire ?" | 140 |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Identité propriétaire | when authorized | "Nom du propriétaire ?" | 145 |
| FLD-VISIT-PIECE_AUTORISATION | Pièce autorisation | when needed | "Document d'autorisation ?" | 150 |
| FLD-VISIT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-VISIT-LOCALISATION_REPERE | Point de repère | informational_only | 160 |
| FLD-VISIT-REFERENCE_ANNONCE | Réf. annonce | informational_only | 165 |
| FLD-VISIT-SURFACE | Surface | informational_only | 170 |
| FLD-VISIT-NOMBRE_CHAMBRES | Chambres | informational_only | 175 |
| FLD-VISIT-DUREE_PREVUE | Durée | informational_only | 180 |
| FLD-VISIT-URGENCE | Urgence | informational_only | 185 |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only | 190 |
| FLD-VISIT-EQUIPEMENT_INSPECTION | Équipement | informational_only | 195 |
| FLD-VISIT-RAPPORT_DELAI | Délai rapport | informational_only | 200 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | Nom accompagnateur | informational_only |
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative date | informational_only |
| FLD-VISIT-PRECISIONS | Précisions | informational_only |
| FLD-VISIT-URGENCE | Urgence | informational_only |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Documents à fournir | informational_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Contact propriétaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | visite_accompagnee or inspection | verification_only |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-PIECE_AUTORISATION | autorisation = true | verification_only |
| FLD-VISIT-RAPPORT_SOUHAITE | inspection or evaluation | informational_only |
| FLD-VISIT-RAPPORT_TYPE | rapport = true | informational_only |
| FLD-VISIT-RAPPORT_DELAI | rapport = true | informational_only |
| FLD-VISIT-EQUIPEMENT_INSPECTION | inspection technique | informational_only |
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | accompagnement personnalisé | informational_only |
| FLD-VISIT-TYPE_ACCOMPAGNEMENT | besoin_accompagnateur = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-VISIT-CONTACT_TELEPHONE | Personal contact |
| FLD-VISIT-CONTACT_NOM | Personal identity |
| FLD-VISIT-CONTACT_EMAIL | Personal contact |
| FLD-VISIT-LOCALISATION_ADRESSE | Exact address of property |
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Owner authorization |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Third-party identity |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Third-party contact |
| FLD-VISIT-PIECE_AUTORISATION | Legal authorization document |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Identity documents |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-VISIT-DERIVED-CONFIRMATION | Confirmation RDV | planification + accord |
| FLD-VISIT-DERIVED-COMPLETUDE_INSPECTION | Complétude | périmètre + équipement |
| FLD-VISIT-DERIVED-URGENCE_REELLE | Urgence | urgence + motif |
| FLD-VISIT-DERIVED-PROFIL_VISITEUR | Profil | identite + historique |
| FLD-VISIT-DERIVED-RAPPORT_ATTENDU | Rapport attendu | type + délai |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Pourquoi voulez-vous visiter ?" | Intention déjà connue |
| 2 | "Quel est votre budget ?" | Déjà collecté |
| 3 | "Avez-vous déjà visité d'autres biens ?" | Non pertinent |
| 4 | "Combien de pièces ?" | Non canonique |
| 5 | "Êtes-vous prêt à acheter ?" | Suggestif |
| 6 | "Quel est votre revenu ?" | Non pertinent |
| 7 | "Avez-vous un agent immobilier ?" | Hors scope |
| 8 | "Pourquoi ce quartier ?" | Déjà connu |

---
## MATRIX 5: inspection_technique

### matrix_id
MATRIX-VISIT-005

### canonical_name
Inspection Technique

### request_family
VISIT_INSPECTION

### transaction_type
SERVICE

### property_or_service_type
inspection_technique

### requester_typology
buyer_tenant_or_owner

### journey_stage
VISIT_OR_INSPECTION

### description
Inspection technique approfondie d'un bien immobilier pour évaluer son état structurel, ses installations et identifier d'éventuels désordres ou vices.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Qui êtes-vous ? (acheteur, locataire, propriétaire, expert)" | 10 |
| FLD-VISIT-TYPE_VISITE | Type de visite | always | "Quel type de visite souhaitez-vous ?" | 20 |
| FLD-VISIT-OBJET | Objet de la visite | always | "Quel est l'objet de cette visite ?" | 25 |
| FLD-VISIT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le bien ?" | 30 |
| FLD-VISIT-TYPE_BIEN | Type de bien | always | "De quel type de bien s'agit-il ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ?" | 40 |
| FLD-VISIT-LOCALISATION_ADRESSE | Adresse | always | "Adresse précise du bien ?" | 45 |
| FLD-VISIT-DISPONIBILITE_DATE | Date souhaitée | always | "Quand souhaitez-vous faire la visite ?" | 50 |
| FLD-VISIT-DISPONIBILITE_HEURE | Heure souhaitée | always | "À quelle heure ?" | 55 |
| FLD-VISIT-NOMBRE_PERSONNES | Nombre de personnes | always | "Combien de personnes participeront à la visite ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-MOTIF_INSPECTION | Motif inspection | always | "Quel est le motif de l'inspection ?" | 65 |
| FLD-VISIT-PERIMETRE_INSPECTION | Périmètre | always | "Périmètre de l'inspection ?" | 70 |
| FLD-VISIT-EQUIPEMENT_INSPECTION | Équipement | always | "Équipement nécessaire ?" | 75 |
| FLD-VISIT-DUREE_PREVUE | Durée prévue | always | "Durée estimée ?" | 80 |
| FLD-VISIT-RAPPORT_SOUHAITE | Rapport | always | "Rapport détaillé souhaité ?" | 85 |
| FLD-VISIT-RAPPORT_TYPE | Type rapport | when rapport | "Type de rapport ?" | 90 |
| FLD-VISIT-RAPPORT_DELAI | Délai rapport | when rapport | "Délai souhaité pour le rapport ?" | 95 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-VISIT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-VISIT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-VISIT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative | if needed | "Date/heure alternative possible ?" | 130 |
| FLD-VISIT-PRECISIONS | Précisions | optional | "Avez-vous des précisions à apporter ?" | 135 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Autorisation | always | "Avez-vous l'autorisation du propriétaire ?" | 140 |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Identité propriétaire | when authorized | "Nom du propriétaire ?" | 145 |
| FLD-VISIT-PIECE_AUTORISATION | Pièce autorisation | when needed | "Document d'autorisation ?" | 150 |
| FLD-VISIT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-VISIT-LOCALISATION_REPERE | Point de repère | informational_only | 160 |
| FLD-VISIT-REFERENCE_ANNONCE | Réf. annonce | informational_only | 165 |
| FLD-VISIT-SURFACE | Surface | informational_only | 170 |
| FLD-VISIT-NOMBRE_CHAMBRES | Chambres | informational_only | 175 |
| FLD-VISIT-DUREE_PREVUE | Durée | informational_only | 180 |
| FLD-VISIT-URGENCE | Urgence | informational_only | 185 |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only | 190 |
| FLD-VISIT-EQUIPEMENT_INSPECTION | Équipement | informational_only | 195 |
| FLD-VISIT-RAPPORT_DELAI | Délai rapport | informational_only | 200 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | Nom accompagnateur | informational_only |
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative date | informational_only |
| FLD-VISIT-PRECISIONS | Précisions | informational_only |
| FLD-VISIT-URGENCE | Urgence | informational_only |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Documents à fournir | informational_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Contact propriétaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | visite_accompagnee or inspection | verification_only |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-PIECE_AUTORISATION | autorisation = true | verification_only |
| FLD-VISIT-RAPPORT_SOUHAITE | inspection or evaluation | informational_only |
| FLD-VISIT-RAPPORT_TYPE | rapport = true | informational_only |
| FLD-VISIT-RAPPORT_DELAI | rapport = true | informational_only |
| FLD-VISIT-EQUIPEMENT_INSPECTION | inspection technique | informational_only |
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | accompagnement personnalisé | informational_only |
| FLD-VISIT-TYPE_ACCOMPAGNEMENT | besoin_accompagnateur = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-VISIT-CONTACT_TELEPHONE | Personal contact |
| FLD-VISIT-CONTACT_NOM | Personal identity |
| FLD-VISIT-CONTACT_EMAIL | Personal contact |
| FLD-VISIT-LOCALISATION_ADRESSE | Exact address of property |
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Owner authorization |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Third-party identity |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Third-party contact |
| FLD-VISIT-PIECE_AUTORISATION | Legal authorization document |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Identity documents |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-VISIT-DERIVED-CONFIRMATION | Confirmation RDV | planification + accord |
| FLD-VISIT-DERIVED-COMPLETUDE_INSPECTION | Complétude | périmètre + équipement |
| FLD-VISIT-DERIVED-URGENCE_REELLE | Urgence | urgence + motif |
| FLD-VISIT-DERIVED-PROFIL_VISITEUR | Profil | identite + historique |
| FLD-VISIT-DERIVED-RAPPORT_ATTENDU | Rapport attendu | type + délai |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Pourquoi voulez-vous visiter ?" | Intention déjà connue |
| 2 | "Quel est votre budget ?" | Déjà collecté |
| 3 | "Avez-vous déjà visité d'autres biens ?" | Non pertinent |
| 4 | "Combien de pièces ?" | Non canonique |
| 5 | "Êtes-vous prêt à acheter ?" | Suggestif |
| 6 | "Quel est votre revenu ?" | Non pertinent |
| 7 | "Avez-vous un agent immobilier ?" | Hors scope |
| 8 | "Pourquoi ce quartier ?" | Déjà connu |

---
## MATRIX 6: evaluation_etat_bien

### matrix_id
MATRIX-VISIT-006

### canonical_name
Évaluation de l'État du Bien

### request_family
VISIT_INSPECTION

### transaction_type
SERVICE

### property_or_service_type
evaluation_etat_bien

### requester_typology
buyer_tenant_or_owner

### journey_stage
VISIT_OR_INSPECTION

### description
Évaluation complète de l'état général d'un bien immobilier incluant structure, finitions, installations techniques et conformité. Produit un rapport d'évaluation détaillé.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Qui êtes-vous ? (acheteur, locataire, propriétaire, expert)" | 10 |
| FLD-VISIT-TYPE_VISITE | Type de visite | always | "Quel type de visite souhaitez-vous ?" | 20 |
| FLD-VISIT-OBJET | Objet de la visite | always | "Quel est l'objet de cette visite ?" | 25 |
| FLD-VISIT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le bien ?" | 30 |
| FLD-VISIT-TYPE_BIEN | Type de bien | always | "De quel type de bien s'agit-il ?" | 35 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-LOCALISATION_QUARTIER | Quartier | always | "Quel quartier ?" | 40 |
| FLD-VISIT-LOCALISATION_ADRESSE | Adresse | always | "Adresse précise du bien ?" | 45 |
| FLD-VISIT-DISPONIBILITE_DATE | Date souhaitée | always | "Quand souhaitez-vous faire la visite ?" | 50 |
| FLD-VISIT-DISPONIBILITE_HEURE | Heure souhaitée | always | "À quelle heure ?" | 55 |
| FLD-VISIT-NOMBRE_PERSONNES | Nombre de personnes | always | "Combien de personnes participeront à la visite ?" | 60 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-PERIMETRE_INSPECTION | Périmètre | always | "Évaluation complète ou partielle ?" | 65 |
| FLD-VISIT-MOTIF_INSPECTION | Motif | always | "Motif de l'évaluation ?" | 70 |
| FLD-VISIT-DUREE_PREVUE | Durée prévue | always | "Durée estimée ?" | 75 |
| FLD-VISIT-RAPPORT_SOUHAITE | Rapport | always | "Rapport d'évaluation souhaité ?" | 80 |
| FLD-VISIT-RAPPORT_TYPE | Type rapport | always | "Quel type de rapport ?" | 85 |
| FLD-VISIT-RAPPORT_DELAI | Délai rapport | always | "Délai pour le rapport ?" | 90 |
| FLD-VISIT-SURFACE | Surface | always | "Surface du bien (m²) ?" | 95 |
| FLD-VISIT-NOMBRE_CHAMBRES | Nombre chambres | always | "Nombre de pièces principales ?" | 100 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 110 |
| FLD-VISIT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 115 |
| FLD-VISIT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 120 |
| FLD-VISIT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 125 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative | if needed | "Date/heure alternative possible ?" | 130 |
| FLD-VISIT-PRECISIONS | Précisions | optional | "Avez-vous des précisions à apporter ?" | 135 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Autorisation | always | "Avez-vous l'autorisation du propriétaire ?" | 140 |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Identité propriétaire | when authorized | "Nom du propriétaire ?" | 145 |
| FLD-VISIT-PIECE_AUTORISATION | Pièce autorisation | when needed | "Document d'autorisation ?" | 150 |
| FLD-VISIT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-VISIT-LOCALISATION_REPERE | Point de repère | informational_only | 160 |
| FLD-VISIT-REFERENCE_ANNONCE | Réf. annonce | informational_only | 165 |
| FLD-VISIT-SURFACE | Surface | informational_only | 170 |
| FLD-VISIT-NOMBRE_CHAMBRES | Chambres | informational_only | 175 |
| FLD-VISIT-DUREE_PREVUE | Durée | informational_only | 180 |
| FLD-VISIT-URGENCE | Urgence | informational_only | 185 |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only | 190 |
| FLD-VISIT-EQUIPEMENT_INSPECTION | Équipement | informational_only | 195 |
| FLD-VISIT-RAPPORT_DELAI | Délai rapport | informational_only | 200 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | Nom accompagnateur | informational_only |
| FLD-VISIT-DISPONIBILITE_ALTERNATIVE | Alternative date | informational_only |
| FLD-VISIT-PRECISIONS | Précisions | informational_only |
| FLD-VISIT-URGENCE | Urgence | informational_only |
| FLD-VISIT-COMMENTAIRE | Commentaire | informational_only |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Documents à fournir | informational_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Contact propriétaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | visite_accompagnee or inspection | verification_only |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-CONTACT_PROPRIETAIRE | autorisation = true | verification_only |
| FLD-VISIT-PIECE_AUTORISATION | autorisation = true | verification_only |
| FLD-VISIT-RAPPORT_SOUHAITE | inspection or evaluation | informational_only |
| FLD-VISIT-RAPPORT_TYPE | rapport = true | informational_only |
| FLD-VISIT-RAPPORT_DELAI | rapport = true | informational_only |
| FLD-VISIT-EQUIPEMENT_INSPECTION | inspection technique | informational_only |
| FLD-VISIT-IDENTITE_ACCOMPAGNATEUR | accompagnement personnalisé | informational_only |
| FLD-VISIT-TYPE_ACCOMPAGNEMENT | besoin_accompagnateur = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-VISIT-CONTACT_TELEPHONE | Personal contact |
| FLD-VISIT-CONTACT_NOM | Personal identity |
| FLD-VISIT-CONTACT_EMAIL | Personal contact |
| FLD-VISIT-LOCALISATION_ADRESSE | Exact address of property |
| FLD-VISIT-AUTORISATION_PROPRIETAIRE | Owner authorization |
| FLD-VISIT-IDENTITE_PROPRIETAIRE | Third-party identity |
| FLD-VISIT-CONTACT_PROPRIETAIRE | Third-party contact |
| FLD-VISIT-PIECE_AUTORISATION | Legal authorization document |
| FLD-VISIT-DOCUMENTS_A_FOURNIR | Identity documents |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-VISIT-DERIVED-CONFIRMATION | Confirmation RDV | planification + accord |
| FLD-VISIT-DERIVED-COMPLETUDE_INSPECTION | Complétude | périmètre + équipement |
| FLD-VISIT-DERIVED-URGENCE_REELLE | Urgence | urgence + motif |
| FLD-VISIT-DERIVED-PROFIL_VISITEUR | Profil | identite + historique |
| FLD-VISIT-DERIVED-RAPPORT_ATTENDU | Rapport attendu | type + délai |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Pourquoi voulez-vous visiter ?" | Intention déjà connue |
| 2 | "Quel est votre budget ?" | Déjà collecté |
| 3 | "Avez-vous déjà visité d'autres biens ?" | Non pertinent |
| 4 | "Combien de pièces ?" | Non canonique |
| 5 | "Êtes-vous prêt à acheter ?" | Suggestif |
| 6 | "Quel est votre revenu ?" | Non pertinent |
| 7 | "Avez-vous un agent immobilier ?" | Hors scope |
| 8 | "Pourquoi ce quartier ?" | Déjà connu |

---

# End of Document — Visit and Inspection Matrices
