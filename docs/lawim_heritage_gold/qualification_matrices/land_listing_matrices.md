# LAND LISTING QUALIFICATION MATRICES — LAWIM Heritage Gold

**Document ID:** LAWIM-GOLD-MATRICES-LAND-LISTING-V1
**Mission:** LAWIM Heritage Gold — Qualification des demandes de mise en vente de terrains
**Date:** 2026-07-15
**Statut:** CANONICAL — Reference document for architecture H1

---

# Table of Contents

| # | Land Type | Matrix ID | Status |
|---|-----------|-----------|--------|
| 1 | terrain_titre_ferme | MATRIX-LAND-LIST-001 | TITRE |
| 2 | terrain_titre_constructible | MATRIX-LAND-LIST-002 | TITRE |
| 3 | terrain_titre_non_constructible | MATRIX-LAND-LIST-003 | TITRE |
| 4 | terrain_titre_agricole | MATRIX-LAND-LIST-004 | TITRE |
| 5 | terrain_titre_commercial | MATRIX-LAND-LIST-005 | TITRE |
| 6 | terrain_titre_industriel | MATRIX-LAND-LIST-006 | TITRE |
| 7 | terrain_titre_indivision | MATRIX-LAND-LIST-007 | TITRE |
| 8 | terrain_non_titre_ferme | MATRIX-LAND-LIST-008 | NON_TITRE |
| 9 | terrain_non_titre_constructible | MATRIX-LAND-LIST-009 | NON_TITRE |
| 10 | terrain_non_titre_non_constructible | MATRIX-LAND-LIST-010 | NON_TITRE |
| 11 | terrain_non_titre_agricole | MATRIX-LAND-LIST-011 | NON_TITRE |
| 12 | terrain_non_titre_commercial | MATRIX-LAND-LIST-012 | NON_TITRE |
| 13 | terrain_non_titre_industriel | MATRIX-LAND-LIST-013 | NON_TITRE |
| 14 | terrain_non_titre_indivision | MATRIX-LAND-LIST-014 | NON_TITRE |

---

# Common Rules for All Land Listing Matrices

## Global Principles

All land listing matrices follow the same qualification architecture as residential listings but are adapted for land-specific characteristics. The declarant may be the owner (propriétaire) or a mandate holder (mandataire). When the declarant is not the sole owner, additional mandate fields are required.

## Qualification Order

| Order | Step | Field(s) |
|:-----:|------|----------|
| 1 | Identité déclarant | FLD-LAND-IDENTITE_DECLARANT |
| 2 | Relation au bien | FLD-LAND-RELATION_BIEN |
| 3 | Autorisation / Mandat | FLD-LAND-AUTORISATION_MANDAT |
| 4 | Transaction | FLD-LAND-TRANSACTION |
| 5 | Statut foncier | FLD-LAND-STATUT_FONCIER |
| 6 | Localisation | FLD-LAND-LOCALISATION_VILLE, FLD-LAND-LOCALISATION_QUARTIER |
| 7 | Surface | FLD-LAND-SURFACE |
| 8 | Prix | FLD-LAND-PRIX_GLOBAL, FLD-LAND-PRIX_M2 |
| 9 | Usage | FLD-LAND-USAGE_PREVU |
| 10 | Documents fonciers | FLD-LAND-TITRE_FONCIER, FLD-LAND-DOCUMENTS |
| 11 | Caractéristiques terrain | FLD-LAND-ACCES, FLD-LAND-TOPGRAPHIE, FLD-LAND-VIABILISATION |
| 12 | Conditions vente | FLD-LAND-CONDITIONS |
| 13 | Photos / Vidéos | FLD-LAND-PHOTOS, FLD-LAND-VIDEOS |
| 14 | Contact | FLD-LAND-CONTACT_NOM, FLD-LAND-CONTACT_TELEPHONE |
| 15 | Règles de visite | FLD-LAND-REGLES_VISITE |
| 16 | Consentement publication | FLD-LAND-CONSENTEMENT_PUBLICATION |
| 17 | Confirmation | Récapitulatif |
| 18 | Escalade | Décision: publication, visite, transfert humain |

## Cameroon Land Sensitivity Rules (Listing)

| Rule | Description |
|------|-------------|
| LL-R01 | Titre foncier status is the most critical field — determines legal security |
| LL-R02 | Surface must be collected in m² with precision |
| LL-R03 | Price can be expressed as global price OR price per m² |
| LL-R04 | Location must include both administrative (ville/quartier) and physical (axe, village, repère) |
| LL-R05 | Access quality (route type, distance) is a key valuation factor |
| LL-R06 | Viabilisation (water, electricity) significantly impacts price |
| LL-R07 | Topography affects land usability and price |
| LL-R08 | Flood zone status must be disclosed |
| LL-R09 | Occupation actuelle (current use) affects delivery timeline |
| LL-R10 | Litiges and servitudes must be declared |
| LL-R11 | Co-ownership (indivision) requires all co-owners' consent |
| LL-R12 | Succession lands require notarial verification |
| LL-R13 | Non-titre lands require additional documentation |
| LL-R14 | Professional verification (notaire/géomètre) is always recommended |

## Matching Role Semantics

| Role | Description |
|------|-------------|
| hard_constraint | Must match exactly; otherwise excluded |
| soft_constraint | Strong preference but flexible |
| ranking_preference | Used to rank results only |
| verification_only | For identity/authorization verification |
| transaction_blocker | Must be resolved before transaction |
| informational_only | For display only, does not affect matching |
| consent_required | Requires explicit user consent |

## Source Status Definitions

| Status | Meaning |
|--------|---------|
| HERITAGE_VALIDATED | Explicit rule from LAWIM heritage documents |
| HERITAGE_NORMALIZED | Normalized from multiple heritage sources |
| EXTERNAL_CONFIRMED | Confirmed by non-LAWIM sources |
| EXPERT_PROPOSAL | Proposed by domain expert |

## Common Forbidden Questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable pour terrain |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---

## Master Field Catalog (Land Listing)

| FIELD-ID | label | data_type | allowed_values | privacy | source | confidence |
|----------|-------|-----------|----------------|--------|--------|------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | enum | PROPRIETAIRE, MANDATAIRE, COPROPRIETAIRE, HERITIER, AUTRE | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-RELATION_BIEN | Relation bien | enum | PROPRIETAIRE_UNIQUE, COPROPRIETAIRE, MANDATAIRE, HERITIER, USUFRUITIER | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-AUTORISATION_MANDAT | Autorisation mandat | enum | PLEINE_PROPRIETE, MANDAT_ECRIT, MANDAT_ORAL, PROCURATION, SUCCESSION | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-TRANSACTION | Transaction | enum | SELL | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-STATUT_FONCIER | Statut foncier | enum | TITRE_FONCIER, ATTESTATION, CONCESSION, CERTIFICAT_OCCUPATION, NON_DOCUMENTE, AUTRE | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-NUM_TITRE | Numéro titre foncier | string | Alphanumeric | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-LOCALISATION_VILLE | Ville | string | LAWIM city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-LOCALISATION_QUARTIER | Quartier | string | Per-city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-LOCALISATION_AXE | Axe principal | string | Free text | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-LOCALISATION_VILLAGE | Village | string | Free text | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-LOCALISATION_REPERE | Point de repère | string | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse complète | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-SURFACE | Surface (m²) | float | Positive float | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-SURFACE_MIN | Surface minimale | float | Positive float | public | EXPERT_PROPOSAL | LOW |
| FLD-LAND-PRIX_GLOBAL | Prix global | float | Positive float | private | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-PRIX_M2 | Prix au m² | float | Positive float | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-PRIX_DEVISE | Devise | enum | XAF, EUR, USD | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | date | Valid date | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | enum | IMMEDIATE, 1_MOIS, 3_MOIS, 6_MOIS, 1_AN, A_DEFINIR | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | enum | LIBRE, CULTIVE, BATI, EN_FRICHE, OCCUPE_ILLEGALEMENT | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-USAGE_PREVU | Usage prévu | enum | HABITATION, COMMERCE, INDUSTRIE, AGRICULTURE, MIXTE | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-CONSTRUCTIBLE | Constructible | boolean | true, false | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-LOTI | Terrain loti | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-ACCES_ROUTE | Accès route | enum | GOUDRONNEE, PISTE_PRATICABLE, PISTE_DIFFICILE, SENTIER, ENCLAVE | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-DISTANCE_ROUTE | Distance route (m) | float | Positive float | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-QUALITE_ACCES | Qualité accès | enum | EXCELLENTE, BONNE, MOYENNE, MEDIOCRE, DIFFICILE | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité disponible | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boolean | true, false | public | EXPERT_PROPOSAL | LOW |
| FLD-LAND-FORAGE | Forage | boolean | true, false | public | EXPERT_PROPOSAL | LOW |
| FLD-LAND-TOPGRAPHIE | Topographie | enum | PLAT, LEGERE_PENTE, FORTE_PENTE, VALLEE, COLLINE, ACCIDENTE | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-INONDABLE | Zone inondable | boolean | true, false | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-SERVITUDES | Servitudes | string | Free text | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-LITIGES_CONNUS | Litiges connus | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-LITIGES_DETAIL | Détail litiges | string | Free text | confidential | EXPERT_PROPOSAL | LOW |
| FLD-LAND-HYPOTHEQUE_CHARGE | Hypothèque / charge | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-SUCCESSION | Succession | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-INDIVISION | Indivision | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-PROCURATION | Procuration | boolean | true, false | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-BORNAGE | Bornage effectué | boolean | true, false | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-PV_BORNAGE | PV de bornage | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | string | Latitude, Longitude | public | EXPERT_PROPOSAL | LOW |
| FLD-LAND-PHOTOS | Photos terrain | array | URLs | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-VIDEOS | Vidéos terrain | array | URLs | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Document titre foncier | string | URL | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Acte de vente | string | URL | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Certificat propriété | string | URL | confidential | HERITAGE_NORMALIZED | HIGH |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | Plan de bornage | string | URL | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-DOCUMENT_LOTISSEMENT | Lotissement approuvé | string | URL | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-DOCUMENT_PROMESSE_VENTE | Promesse de vente | string | URL | confidential | EXPERT_PROPOSAL | MEDIUM |
| FLD-LAND-CONDITIONS | Conditions vente | string | Free text | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | integer | Positive integer | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | string | Free text | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | Disponibilité signataires | string | Free text | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-CONTACT_NOM | Nom contact | string | Free text | private | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | string | Valid phone | private | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-CONTACT_EMAIL | Email | string | Valid email | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-CONTACT_CANAL | Canal préféré | enum | WHATSAPP, TELEGRAM, SMS, EMAIL, APPEL | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-REGLES_VISITE | Règles visite | string | Free text | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires visite | string | Free text | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis visite | enum | 24H, 48H, 72H, SUR_RENDEZ_VOUS | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement publication | boolean | true, false | public | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | enum[] | LAWIM_SITE, PARTENAIRES, RESEAUX_SOCIAUX, TOUS | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | enum | 1_MOIS, 2_MOIS, 3_MOIS, 6_MOIS, JUSQU_A_VENTE | public | EXPERT_PROPOSAL | MEDIUM |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | enum | COMPLET, STANDARD, MINIMAL, NON_VERIFIE | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-VERIFICATION_DATE | Date vérification | date | Valid date | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-NATURE_MANDAT | Nature mandat | enum | MANDAT_SIMPLE, MANDAT_EXCLUSIF, MANDAT_COEXCLUSIF, PROCURATION | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-IDENTITE_TITULAIRE | Identité titulaire | string | Full name | private | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-PREUVE_MANDAT | Preuve mandat | string | URL | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-DUREE_MANDAT | Durée mandat | enum | 1_MOIS, 3_MOIS, 6_MOIS, 1_AN, DUREE_DETERMINEE, INDETERMINEE | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-DUREE_MANDAT_FIN | Fin mandat | date | Valid date | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-POUVOIRS_ACCORDS | Pouvoirs accordés | enum[] | PUBLIER_ANNONCE, NEGOCIER_PRIX, SIGNER_PROMESSE, SIGNER_ACTE, ENCAISSER_FONDS, FAIRE_VISITES, TOUS_POUVOIRS | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-NOMBRE_SIGNATAIRES_TITRE | Nombre signataires titre | integer | 1-20 | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-IDENTITE_SIGNATAIRES_TITRE | Identité signataires titre | string | Free text | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | enum | COMPTANT, CREDIT_BANCAIRE, TONTINE, DIASPORA, PRET_FAMILIAL | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | boolean | true, false | public | HERITAGE_NORMALIZED | MEDIUM |

---

## Derived Fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix m² calculé | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local par type |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut_foncier + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | weighted(acces_route, distance, qualite) |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | weighted(eau, electricite, forage) |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie + zone |
| FLD-LAND-DERIVED-URBANISATION | Urbanisation | ville + quartier |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + vérification conservatoire |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree_mandat + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE_ANNONCE | Complétude annonce | weighted(fields, photos, documents) |

---
## MATRIX 1: terrain_titre_ferme

### matrix_id
MATRIX-LAND-LIST-001

### canonical_name
Terrain avec titre foncier — Ferme/Agricole

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_titre_ferme

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain avec titre foncier — ferme/agricole. This land dispose d'un titre foncier valide et enregistré. Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier |  | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 2: terrain_titre_constructible

### matrix_id
MATRIX-LAND-LIST-002

### canonical_name
Terrain avec titre foncier — Constructible

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_titre_constructible

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain avec titre foncier — constructible. This land dispose d'un titre foncier valide et enregistré. Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier |  | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 3: terrain_titre_non_constructible

### matrix_id
MATRIX-LAND-LIST-003

### canonical_name
Terrain avec titre foncier — Non constructible

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_titre_non_constructible

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain avec titre foncier — non constructible. This land dispose d'un titre foncier valide et enregistré. Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier |  | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 4: terrain_titre_agricole

### matrix_id
MATRIX-LAND-LIST-004

### canonical_name
Terrain avec titre foncier — Agricole

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_titre_agricole

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain avec titre foncier — agricole. This land dispose d'un titre foncier valide et enregistré. Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier |  | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 5: terrain_titre_commercial

### matrix_id
MATRIX-LAND-LIST-005

### canonical_name
Terrain avec titre foncier — Commercial

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_titre_commercial

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain avec titre foncier — commercial. This land dispose d'un titre foncier valide et enregistré. Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier |  | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 6: terrain_titre_industriel

### matrix_id
MATRIX-LAND-LIST-006

### canonical_name
Terrain avec titre foncier — Industriel

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_titre_industriel

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain avec titre foncier — industriel. This land dispose d'un titre foncier valide et enregistré. Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier |  | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 7: terrain_titre_indivision

### matrix_id
MATRIX-LAND-LIST-007

### canonical_name
Terrain avec titre foncier — Indivision

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_titre_indivision

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain avec titre foncier — indivision. This land dispose d'un titre foncier valide et enregistré. Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier |  | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 8: terrain_non_titre_ferme

### matrix_id
MATRIX-LAND-LIST-008

### canonical_name
Terrain sans titre foncier — Ferme/Agricole

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_non_titre_ferme

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain sans titre foncier — ferme/agricole. This land ne dispose pas de titre foncier (documents alternatifs possibles). Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier | if statut = TITRE_FONCIER | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 9: terrain_non_titre_constructible

### matrix_id
MATRIX-LAND-LIST-009

### canonical_name
Terrain sans titre foncier — Constructible

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_non_titre_constructible

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain sans titre foncier — constructible. This land ne dispose pas de titre foncier (documents alternatifs possibles). Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier | if statut = TITRE_FONCIER | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 10: terrain_non_titre_non_constructible

### matrix_id
MATRIX-LAND-LIST-010

### canonical_name
Terrain sans titre foncier — Non constructible

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_non_titre_non_constructible

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain sans titre foncier — non constructible. This land ne dispose pas de titre foncier (documents alternatifs possibles). Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier | if statut = TITRE_FONCIER | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 11: terrain_non_titre_agricole

### matrix_id
MATRIX-LAND-LIST-011

### canonical_name
Terrain sans titre foncier — Agricole

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_non_titre_agricole

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain sans titre foncier — agricole. This land ne dispose pas de titre foncier (documents alternatifs possibles). Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier | if statut = TITRE_FONCIER | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 12: terrain_non_titre_commercial

### matrix_id
MATRIX-LAND-LIST-012

### canonical_name
Terrain sans titre foncier — Commercial

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_non_titre_commercial

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain sans titre foncier — commercial. This land ne dispose pas de titre foncier (documents alternatifs possibles). Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier | if statut = TITRE_FONCIER | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 13: terrain_non_titre_industriel

### matrix_id
MATRIX-LAND-LIST-013

### canonical_name
Terrain sans titre foncier — Industriel

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_non_titre_industriel

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain sans titre foncier — industriel. This land ne dispose pas de titre foncier (documents alternatifs possibles). Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier | if statut = TITRE_FONCIER | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---
## MATRIX 14: terrain_non_titre_indivision

### matrix_id
MATRIX-LAND-LIST-014

### canonical_name
Terrain sans titre foncier — Indivision

### request_family
LAND_LISTING

### transaction_type
SELL

### property_or_service_type
terrain_non_titre_indivision

### requester_typology
owner_or_mandate

### journey_stage
LISTING

### description
Qualification matrix for listing terrain sans titre foncier — indivision. This land ne dispose pas de titre foncier (documents alternatifs possibles). Covers complete listing process from declarant identification through property characteristics, legal documentation, and publication consent. Applicable for owners and mandate holders.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-IDENTITE_DECLARANT | Identité déclarant | always | "Êtes-vous propriétaire ou mandataire ?" | 10 |
| FLD-LAND-RELATION_BIEN | Relation bien | always | "Quelle est votre relation avec ce terrain ?" | 20 |
| FLD-LAND-TRANSACTION | Transaction | always | Derived (SELL) | 30 |
| FLD-LAND-STATUT_FONCIER | Statut foncier | always | "Le terrain a-t-il un titre foncier ?" | 40 |
| FLD-LAND-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve le terrain ?" | 50 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-LOCALISATION_QUARTIER | Quartier / Axe | always | "Quartier ou axe principal ?" | 60 |
| FLD-LAND-LOCALISATION_ADRESSE | Adresse / Repère | always | "Adresse ou point de repère ?" | 65 |
| FLD-LAND-SURFACE | Surface | always | "Surface du terrain en m² ?" | 70 |
| FLD-LAND-PRIX_GLOBAL | Prix global | always | "Prix de vente ?" | 75 |
| FLD-LAND-DISPONIBILITE_DATE | Date disponibilité | always | "À partir de quand le terrain est-il disponible ?" | 80 |
| FLD-LAND-OCCUPATION_ACTUELLE | Occupation actuelle | always | "Le terrain est-il actuellement occupé ou exploité ?" | 85 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-PRIX_NEGOCIABLE | Négociable | always | "Le prix est-il négociable ?" | 90 |
| FLD-LAND-USAGE_PREVU | Usage prévu | always | "Quel est l'usage prévu ou autorisé ?" | 95 |
| FLD-LAND-CONSTRUCTIBLE | Constructible | always | "Le terrain est-il constructible ?" | 100 |
| FLD-LAND-ACCES_ROUTE | Accès route | always | "Quel est le type d'accès routier ?" | 105 |
| FLD-LAND-TOPGRAPHIE | Topographie | always | "Quelle est la topographie du terrain ?" | 110 |
| FLD-LAND-INONDABLE | Zone inondable | always | "Le terrain est-il en zone inondable ?" | 115 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-CONTACT_NOM | Nom | always | "Votre nom ?" | 120 |
| FLD-LAND-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 125 |
| FLD-LAND-CONTACT_EMAIL | Email | always | "Votre email ?" | 130 |
| FLD-LAND-CONSENTEMENT_PUBLICATION | Consentement | always | "Acceptez-vous la publication de l'annonce ?" | 140 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-REGLES_VISITE | Règles visite | always | "Modalités de visite du terrain ?" | 150 |
| FLD-LAND-REGLES_VISITE_HORAIRES | Horaires | always | "Horaires disponibles ?" | 155 |
| FLD-LAND-REGLES_VISITE_PREAVIS | Préavis | always | "Préavis nécessaire ?" | 160 |
| FLD-LAND-LOCALISATION_REPERE | Point repère | always | "Point de repère pour retrouver le terrain ?" | 165 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-LAND-NUM_TITRE | Numéro titre foncier | if statut = TITRE_FONCIER | "Numéro du titre foncier ?" | 170 |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Document foncier | always | "Document de propriété disponible ?" | 175 |
| FLD-LAND-CONDITIONS | Conditions vente | always | "Conditions particulières de vente ?" | 180 |
| FLD-LAND-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 185 |
| FLD-LAND-BESOIN_NOTAIRE | Besoin notaire | always | "Souhaitez-vous l'intervention d'un notaire ?" | 190 |
| FLD-LAND-BESOIN_GEOMETRE | Besoin géomètre | when land not borné | "Un géomètre est-il nécessaire ?" | 195 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-LAND-LOTI | Terrain loti | soft_constraint | 200 |
| FLD-LAND-QUALITE_ACCES | Qualité accès | ranking_preference | 205 |
| FLD-LAND-DISTANCE_ROUTE | Distance route | ranking_preference | 210 |
| FLD-LAND-VIABILISATION_EAU | Eau disponible | soft_constraint | 215 |
| FLD-LAND-VIABILISATION_ELECTRICITE | Électricité | soft_constraint | 220 |
| FLD-LAND-GROUPE_ELECTROGENE | Groupe électrogène | boost (+10) | 225 |
| FLD-LAND-FORAGE | Forage | boost (+15) | 230 |
| FLD-LAND-SERVITUDES | Servitudes | verification_only | 235 |
| FLD-LAND-BORNAGE | Bornage effectué | informational_only | 240 |
| FLD-LAND-CERTIFICAT_URBANISME | Certificat urbanisme | informational_only | 245 |
| FLD-LAND-PHOTOS | Photos | informational_only | 250 |
| FLD-LAND-VIDEOS | Vidéos | informational_only | 255 |
| FLD-LAND-COORDONNEES_GPS | Coordonnées GPS | informational_only | 260 |
| FLD-LAND-PRIX_DEVISE | Devise | informational_only | 265 |
| FLD-LAND-PRIX_M2 | Prix au m² | informational_only | 270 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-LAND-LOCALISATION_AXE | Axe principal | informational_only |
| FLD-LAND-LOCALISATION_VILLAGE | Village | informational_only |
| FLD-LAND-SURFACE_MIN | Surface minimale | informational_only |
| FLD-LAND-DISPONIBILITE_DELAI | Délai disponibilité | informational_only |
| FLD-LAND-CONTACT_CANAL | Canal préféré | informational_only |
| FLD-LAND-CONSENTEMENT_CANAUX | Canaux publication | informational_only |
| FLD-LAND-CONSENTEMENT_DUREE | Durée publication | informational_only |
| FLD-LAND-PV_BORNAGE | PV de bornage | verification_only |
| FLD-LAND-SOURCE_FINANCEMENT | Source financement | informational_only |
| FLD-LAND-CONDITION_NOMBRE_SIGNATAIRES | Nombre signataires | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | Identité signataires | verification_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-LAND-NATURE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-IDENTITE_TITULAIRE | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-PREUVE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-DUREE_MANDAT | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-POUVOIRS_ACCORDS | relation_bien != PROPRIETAIRE_UNIQUE | verification_only |
| FLD-LAND-NUM_TITRE | statut = TITRE_FONCIER | verification_only |
| FLD-LAND-HYPOTHEQUE_CHARGE | num_titre provided | verification_only |
| FLD-LAND-LITIGES_CONNUS | any legal concern | verification_only |
| FLD-LAND-LITIGES_DETAIL | litiges = true | verification_only |
| FLD-LAND-SUCCESSION | if héritage | verification_only |
| FLD-LAND-INDIVISION | usage = co-ownership | verification_only |
| FLD-LAND-PROCURATION | if mandate | verification_only |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | statut != TITRE_FONCIER | verification_only |
| FLD-LAND-DOCUMENT_PLAN_BORNAGE | bornage = true | verification_only |
| FLD-LAND-DOCUMENT_LOTISSEMENT | loti = true | verification_only |
| FLD-LAND-CONDITION_IDENTITE_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONDITION_DISPO_SIGNATAIRES | nombre_signataires > 1 | verification_only |
| FLD-LAND-CONSENTEMENT_CANAUX | consent = true | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-LAND-CONTACT_TELEPHONE | Personal contact information |
| FLD-LAND-CONTACT_NOM | Personal identity |
| FLD-LAND-CONTACT_EMAIL | Personal contact |
| FLD-LAND-PRIX_GLOBAL | Financial - owner pricing |
| FLD-LAND-LOCALISATION_ADRESSE | Exact location |
| FLD-LAND-NUM_TITRE | Legal property identifier |
| FLD-LAND-DOCUMENT_TITRE_FONCIER | Legal document |
| FLD-LAND-DOCUMENT_ACTE_VENTE | Legal sale document |
| FLD-LAND-DOCUMENT_CERTIFICAT_PROPRIETE | Legal ownership document |
| FLD-LAND-LITIGES_CONNUS | Legal dispute information |
| FLD-LAND-HYPOTHEQUE_CHARGE | Encumbrance information |
| FLD-LAND-LITIGES_DETAIL | Detailed dispute information |
| FLD-LAND-IDENtITE_SIGNATAIRES_TITRE | Third-party identity |
| FLD-LAND-PREUVE_MANDAT | Legal mandate document |
| FLD-LAND-IDENTITE_TITULAIRE | Third-party identity |
| FLD-LAND-NATURE_MANDAT | Mandate terms |
| FLD-LAND-DUREE_MANDAT | Mandate duration |
| FLD-LAND-POUVOIRS_ACCORDS | Mandate powers |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-LAND-DERIVED-PRIX_M2_CALCULE | Prix au m² | prix_global / surface |
| FLD-LAND-DERIVED-PRIX_COHERENCE | Cohérence prix | prix vs marché local |
| FLD-LAND-DERIVED-CONSTRUCTIBILITE | Constructibilité | statut + zone + documents |
| FLD-LAND-DERIVED-SCORE_ACCES | Score accès | acces_route + distance + qualite |
| FLD-LAND-DERIVED-SCORE_VIABILISATION | Score viabilisation | eau + electricite + forage |
| FLD-LAND-DERIVED-RISQUE_INONDATION | Risque inondation | inondable + topographie |
| FLD-LAND-DERIVED-TITRE_VALIDE | Titre valide | num_titre + verification |
| FLD-LAND-DERIVED-MANDAT_ACTIF | Mandat actif | duree + date_fin |
| FLD-LAND-DERIVED-COMPLETUDE | Complétude annonce | weighted fields |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien de chambres ?" | Terrain — pas de chambres |
| 2 | "Combien de douches ?" | Non applicable |
| 3 | "Combien de salons ?" | Non applicable |
| 4 | "Quel standing résidentiel ?" | Non applicable |
| 5 | "À quel étage ?" | Non applicable |
| 6 | "Y a-t-il un ascenseur ?" | Non applicable |
| 7 | "Quel est votre revenu ?" | Non pertinent |
| 8 | "Pourquoi vendez-vous ?" | Hors scope |
| 9 | "Combien de pièces ?" | Terme non canonique |

---

# End of Document — Land Listing Matrices
