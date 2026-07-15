# Property Management Qualification Matrices — LAWIM Heritage Gold

**Document ID:** LAWIM-GOLD-MATRICES-PROPERTY-MANAGEMENT-V1
**Mission:** LAWIM Heritage Gold — Qualification des demandes de gestion immobilière
**Date:** 2026-07-15
**Statut:** CANONICAL — Reference document for architecture H1

---

# Table of Contents

| # | Service Type | Matrix ID | Category |
|---|-------------|-----------|----------|
| 1 | gestion_locative_complete | MATRIX-PMGMT-001 | LOCATIVE |
| 2 | gestion_locative_partielle | MATRIX-PMGMT-002 | LOCATIVE |
| 3 | recouvrement_loyers | MATRIX-PMGMT-003 | FINANCIAL |
| 4 | gestion_entretien | MATRIX-PMGMT-004 | MAINTENANCE |
| 5 | gestion_sinistre | MATRIX-PMGMT-005 | DAMAGE |
| 6 | gestion_copropriete | MATRIX-PMGMT-006 | COPROPRIETE |
| 7 | syndic_benévole | MATRIX-PMGMT-007 | SYNDIC |
| 8 | syndic_professionnel | MATRIX-PMGMT-008 | SYNDIC |

---

# Common Rules for All Property Management Matrices

## Qualification Order

| Order | Step | Field(s) |
|:-----:|------|----------|
| 1 | Identité demandeur | FLD-PMGMT-IDENTITE_DEMANDEUR |
| 2 | Type de gestion | FLD-PMGMT-TYPE_GESTION |
| 3 | Description du besoin | FLD-PMGMT-DESCRIPTION |
| 4 | Localisation du/des biens | FLD-PMGMT-LOCALISATION_VILLE |
| 5 | Nombre de biens | FLD-PMGMT-NOMBRE_BIENS |
| 6 | Type de biens | FLD-PMGMT-TYPE_BIEN |
| 7 | Situation actuelle | FLD-PMGMT-SITUATION_ACTUELLE |
| 8 | Documents mandat | FLD-PMGMT-MANDAT_DISPO |
| 9 | Contact | FLD-PMGMT-CONTACT_NOM, FLD-PMGMT-CONTACT_TELEPHONE |
| 10 | Confirmation | Récapitulatif |
| 11 | Escalade | Proposition de service / mise en relation |

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
| EXTERNAL_CONFIRMED | Confirmed by non-LAWIM sources |
| EXPERT_PROPOSAL | Proposed by domain expert |

## Common Forbidden Questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien gagnez-vous ?" | Non pertinent |
| 2 | "Pourquoi ne gérez-vous pas vous-même ?" | Hors scope |
| 3 | "Avez-vous des problèmes avec vos locataires ?" | Trop intrusif |
| 4 | "Quel est votre emploi ?" | Non pertinent |
| 5 | "Avez-vous déjà eu des impayés ?" | À traiter dans le cadre du service |
| 6 | "Combien de pièces ?" | Terme non canonique |
| 7 | "Voulez-vous vendre ?" | Hors scope du service de gestion |
| 8 | "Avez-vous un autre bien ?" | Non pertinent pour la qualification |

---

## Master Field Catalog (Property Management)

| FIELD-ID | label | data_type | allowed_values | privacy | source | confidence |
|----------|-------|-----------|----------------|--------|--------|------------|
| FLD-PMGMT-IDENTITE_DEMANDEUR | Identité demandeur | enum | PROPRIETAIRE, COPROPRIETAIRE, SYNDIC, INVESTISSEUR, PROMOTEUR, ENTREPRISE | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-TYPE_GESTION | Type de gestion | enum | GESTION_COMPLETE, GESTION_PARTIELLE, RECOUVREMENT, ENTRETIEN, SINISTRE, COPROPRIETE, SYNDIC_BENEVOLE, SYNDIC_PROFESSIONNEL | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-DESCRIPTION | Description besoin | text | Free text (min 20 chars) | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-LOCALISATION_VILLE | Ville | string | LAWIM city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | string | Per-city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-LOCALISATION_ADRESSE | Adresse(s) bien(x) | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-NOMBRE_BIENS | Nombre de biens | integer | 1-1000 | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-TYPE_BIEN | Type de bien | enum[] | STUDIO, APPARTEMENT, MAISON, VILLA, COMMERCIAL, BUREAU, IMMEUBLE, RESIDENCE, LOTISSEMENT, AUTRE | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-SITUATION_ACTUELLE | Situation actuelle | enum | OCCUPE_AVEC_BAIL, OCCUPE_SANS_BAIL, LIBRE, EN_TRAVAUX, EN_LITIGE, MIXTE | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-NOMBRE_LOCATAIRES | Nombre locataires | integer | 0-1000 | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Loyer mensuel total | float | Positive float | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer mensuel moyen | float | Positive float | private | EXPERT_PROPOSAL | LOW |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | float | Positive float | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels locatifs | float | Positive float | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-TAUX_OCCUPATION | Taux d'occupation | enum | 100_PCT, 75_100_PCT, 50_75_PCT, MOINS_50_PCT, VARIABLE | private | EXPERT_PROPOSAL | MEDIUM |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés en cours | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-MONTANT_IMPAYES | Montant impayés | float | Positive float | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-NOMBRE_IMPAYES | Nombre impayés | integer | 0-100 | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-ANCIENNETE_IMPAYES | Ancienneté impayés | enum | MOINS_1_MOIS, 1_3_MOIS, 3_6_MOIS, PLUS_6_MOIS | confidential | EXPERT_PROPOSAL | LOW |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges en cours | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-LITIGES_DETAIL | Détail litiges | text | Free text | confidential | EXPERT_PROPOSAL | LOW |
| FLD-PMGMT-MANDAT_DISPO | Mandat de gestion disponible | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-MANDAT_TYPE | Type mandat | enum | MANDAT_GESTION, MANDAT_LOCATION, MANDAT_ENTRETIEN, MANDAT_SYNDIC, CONTRAT_PRESTATION | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-DUREE_MANDAT_SOUHAITEE | Durée mandat souhaitée | enum | 1_AN, 2_ANS, 3_ANS, 5_ANS, INDETERMINEE | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-PERIMETRE_GESTION | Périmètre gestion | enum | COMPLET, LOCATION_SEULE, ENTRETIEN_SEUL, RECOUVREMENT_SEUL, ADMINISTRATIF_SEUL, SUR_MESURE | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-FREQUENCE_REPORTING | Fréquence reporting | enum | HEBDOMADAIRE, MENSUELLE, TRIMESTRIELLE, SEMESTRIELLE, ANNUELLE, SUR_DEMANDE | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-BUDGET_PRESTATION | Budget prestation | float | Positive float | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-BUDGET_DEVISE | Devise | enum | XAF, EUR, USD | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-DATE_DEBUT_SOUHAITEE | Date début souhaitée | date | Valid date | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-URGENCE | Urgence | enum | URGENT, CETTE_SEMAINE, CE_MOIS, PAS_URGENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-TYPE_SINISTRE | Type de sinistre | enum | INCENDIE, DEGATS_EAU, VOL, VANDALISME, CATASTROPHE_NATURELLE, MOUVEMENT_TERRAIN, AUTRE | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-DATE_SINISTRE | Date sinistre | date | Valid date | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-DEGATS_ESTIMES | Dégâts estimés | enum | MINEURS, MODERES, MAJEURS, TRES_GRAVES, TOTAUX | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-ASSURANCE_DISPO | Assurance disponible | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-ASSURANCE_NOM | Nom assurance | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-ASSURANCE_NUMERO | Numéro contrat | string | Free text | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-ENTRETIEN_TYPE | Type d'entretien | enum | PREVENTIF, CURATIF, URGENT, PLANIFIE, SAISONNIER | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | Périodicité entretien | enum | PONCTUEL, MENSUEL, TRIMESTRIEL, SEMESTRIEL, ANNUEL | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-DERNIER_ENTRETIEN | Dernier entretien | date | Valid date | public | EXPERT_PROPOSAL | LOW |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | Nombre de lots | integer | 2-500 | public | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | Règlement copropriété | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | Syndic actuel | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Budget annuel copropriété | float | Positive float | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | PV d'AG disponibles | boolean | true, false | confidential | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | Fonds d'urgence | boolean | true, false | confidential | EXPERT_PROPOSAL | LOW |
| FLD-PMGMT-PIECE_IDENTITE | Pièce d'identité | string | URL | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-PIECE_PROPRIETE | Justificatif propriété | string | URL | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-CONTACT_NOM | Nom contact | string | Free text | private | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-CONTACT_TELEPHONE | Téléphone | string | Valid phone | private | HERITAGE_VALIDATED | HIGH |
| FLD-PMGMT-CONTACT_EMAIL | Email | string | Valid email | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-CONTACT_CANAL | Canal préféré | enum | WHATSAPP, TELEGRAM, SMS, EMAIL, APPEL | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-PMGMT-CONTACT_DISPO | Disponibilité contact | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-PMGMT-COMMENTAIRE | Commentaire | text | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-PMGMT-NIVEAU_VERIFICATION | Niveau vérification | enum | COMPLET, STANDARD, MINIMAL | confidential | HERITAGE_VALIDATED | HIGH |

---

## Derived Fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-PMGMT-DERIVED-REVENUS_MENSUELS | Revenus mensuels estimés | loyer_total * taux_occupation |
| FLD-PMGMT-DERIVED-RENTABILITE | Rentabilité estimée | revenus_annuels / valeur_bien |
| FLD-PMGMT-DERIVED-RISQUE_IMPAYES | Risque impayés | ancienneté + montant + nombre |
| FLD-PMGMT-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | weighted documents |
| FLD-PMGMT-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | nombre_biens + type + historique |
| FLD-PMGMT-DERIVED-URGENCE_SINISTRE | Urgence sinistre | type + degats + date |
| FLD-PMGMT-DERIVED-BESOIN_ENTRETIEN | Besoin entretien | periodicité + dernier + type |

---
## MATRIX 1: gestion_locative_complete

### matrix_id
MATRIX-PMGMT-001

### canonical_name
Gestion Locative Complète

### request_family
PROPERTY_MANAGEMENT

### transaction_type
SERVICE

### property_or_service_type
gestion_locative_complete

### requester_typology
owner_or_coowner

### journey_stage
SERVICE_REQUEST

### description
Prise en charge intégrale de la gestion locative: recherche de locataires, rédaction de baux, encaissement des loyers, gestion des impayés, entretien courant, régularisation des charges, état des lieux, gestion des litiges.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous propriétaire, copropriétaire ou syndic ?" | 10 |
| FLD-PMGMT-TYPE_GESTION | Type de gestion | always | "Quel type de gestion recherchez-vous ?" | 20 |
| FLD-PMGMT-DESCRIPTION | Description besoin | always | "Décrivez votre situation et vos besoins de gestion" | 25 |
| FLD-PMGMT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve(nt) le(s) bien(s) ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-NOMBRE_BIENS | Nombre de biens | always | "Combien de biens sont concernés ?" | 35 |
| FLD-PMGMT-TYPE_BIEN | Type de bien | always | "Quels types de biens ?" | 40 |
| FLD-PMGMT-SITUATION_ACTUELLE | Situation actuelle | always | "Quelle est la situation locative actuelle ?" | 45 |
| FLD-PMGMT-NOMBRE_LOCATAIRES | Nombre locataires | always | "Combien de locataires actuellement ?" | 50 |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Loyer mensuel total | always | "Quel est le montant total des loyers mensuels ?" | 55 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | always | "Y a-t-il des impayés actuellement ?" | 60 |
| FLD-PMGMT-PERIMETRE_GESTION | Périmètre gestion | always | "Quel périmètre de gestion souhaitez-vous ?" | 65 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer moyen | always | "Loyer moyen par bien ?" | 70 |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | always | "Charges mensuelles totales ?" | 75 |
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | always | "Revenus locatifs annuels estimés ?" | 80 |
| FLD-PMGMT-TAUX_OCCUPATION | Taux occupation | always | "Taux d'occupation actuel ?" | 85 |
| FLD-PMGMT-MANDAT_DISPO | Mandat disponible | always | "Avez-vous déjà un mandat de gestion ?" | 90 |
| FLD-PMGMT-DUREE_MANDAT_SOUHAITEE | Durée mandat | always | "Durée de mandat souhaitée ?" | 95 |
| FLD-PMGMT-FREQUENCE_REPORTING | Fréquence reporting | always | "Fréquence de reporting souhaitée ?" | 100 |
| FLD-PMGMT-DATE_DEBUT_SOUHAITEE | Date début | always | "Quand souhaitez-vous débuter ?" | 105 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 115 |
| FLD-PMGMT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 120 |
| FLD-PMGMT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 125 |
| FLD-PMGMT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 130 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_ADRESSE | Adresse(s) bien(s) | always | "Adresse(s) précise(s) du/des bien(s) ?" | 135 |
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier(s) ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat | when not provided | "Mandat de gestion à établir ?" | 145 |
| FLD-PMGMT-MANDAT_TYPE | Type mandat | when mandate needed | "Type de mandat souhaité ?" | 150 |
| FLD-PMGMT-PIECE_IDENTITE | Pièce identité | always | "Pièce d'identité à fournir ?" | 155 |
| FLD-PMGMT-PIECE_PROPRIETE | Justificatif propriété | always | "Justificatif de propriété ?" | 160 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget pour cette prestation ?" | 165 |
| FLD-PMGMT-BUDGET_DEVISE | Devise | always | "Devise ?" | 170 |
| FLD-PMGMT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 175 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only | 180 |
| FLD-PMGMT-TAUX_OCCUPATION | Taux occupation | informational_only | 185 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | informational_only | 190 |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | verification_only | 195 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | informational_only | 200 |
| FLD-PMGMT-URGENCE | Urgence | informational_only | 205 |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only | 210 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only |
| FLD-PMGMT-TAUX_OCCUPATION | Taux d'occupation | informational_only |
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer moyen | informational_only |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | informational_only |
| FLD-PMGMT-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-PMGMT-MANDAT_TYPE | mandat_dispo = false | verification_only |
| FLD-PMGMT-PIECE_IDENTITE | toujours | verification_only |
| FLD-PMGMT-PIECE_PROPRIETE | toujours | verification_only |
| FLD-PMGMT-MONTANT_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-NOMBRE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-ANCIENNETE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-LITIGES_DETAIL | litiges_en_cours = true | verification_only |
| FLD-PMGMT-ASSURANCE_NOM | assurance_dispo = true | informational_only |
| FLD-PMGMT-ASSURANCE_NUMERO | assurance_dispo = true | informational_only |
| FLD-PMGMT-TYPE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DATE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DEGATS_ESTIMES | gestion_sinistre | informational_only |
| FLD-PMGMT-ENTRETIEN_TYPE | gestion_entretien | informational_only |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | gestion_entretien | informational_only |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | copropriete or syndic | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-PMGMT-CONTACT_TELEPHONE | Personal contact |
| FLD-PMGMT-CONTACT_NOM | Personal identity |
| FLD-PMGMT-CONTACT_EMAIL | Personal contact |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Financial information |
| FLD-PMGMT-REVENUS_ANNUELS | Financial information |
| FLD-PMGMT-IMPAYES_EN_COURS | Financial difficulty |
| FLD-PMGMT-MONTANT_IMPAYES | Financial information |
| FLD-PMGMT-LITIGES_EN_COURS | Dispute information |
| FLD-PMGMT-LITIGES_DETAIL | Detailed dispute information |
| FLD-PMGMT-MANDAT_DISPO | Mandate terms |
| FLD-PMGMT-PIECE_IDENTITE | Identity document |
| FLD-PMGMT-PIECE_PROPRIETE | Property document |
| FLD-PMGMT-ASSURANCE_NUMERO | Insurance contract |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Financial coproperty data |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-PMGMT-DERIVED-REVENUS_MENSUELS | Revenus mensuels estimés | loyer_total * taux_occupation |
| FLD-PMGMT-DERIVED-RENTABILITE | Rentabilité estimée | revenus_annuels / valeur_bien |
| FLD-PMGMT-DERIVED-RISQUE_IMPAYES | Risque impayés | ancienneté + montant + nombre |
| FLD-PMGMT-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | weighted documents |
| FLD-PMGMT-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | nombre_biens + type |
| FLD-PMGMT-DERIVED-URGENCE_SINISTRE | Urgence sinistre | type + degats + date |
| FLD-PMGMT-DERIVED-BESOIN_ENTRETIEN | Besoin entretien | periodicité + dernier |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien gagnez-vous ?" | Non pertinent |
| 2 | "Pourquoi ne gérez-vous pas vous-même ?" | Hors scope |
| 3 | "Avez-vous des problèmes avec vos locataires ?" | Trop intrusif |
| 4 | "Quel est votre emploi ?" | Non pertinent |
| 5 | "Avez-vous déjà eu des impayés ?" | Déjà demandé dans le service |
| 6 | "Combien de pièces ?" | Non canonique |
| 7 | "Voulez-vous vendre ?" | Hors scope |
| 8 | "Avez-vous un autre bien ailleurs ?" | Non pertinent |

---
## MATRIX 2: gestion_locative_partielle

### matrix_id
MATRIX-PMGMT-002

### canonical_name
Gestion Locative Partielle

### request_family
PROPERTY_MANAGEMENT

### transaction_type
SERVICE

### property_or_service_type
gestion_locative_partielle

### requester_typology
owner_or_coowner

### journey_stage
SERVICE_REQUEST

### description
Gestion locative à la carte: le propriétaire choisit les services souhaités (encaissement seul, entretien seul, administrative seul). Service flexible adapté aux besoins spécifiques.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous propriétaire, copropriétaire ou syndic ?" | 10 |
| FLD-PMGMT-TYPE_GESTION | Type de gestion | always | "Quel type de gestion recherchez-vous ?" | 20 |
| FLD-PMGMT-DESCRIPTION | Description besoin | always | "Décrivez votre situation et vos besoins de gestion" | 25 |
| FLD-PMGMT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve(nt) le(s) bien(s) ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-NOMBRE_BIENS | Nombre de biens | always | "Combien de biens sont concernés ?" | 35 |
| FLD-PMGMT-TYPE_BIEN | Type de bien | always | "Quels types de biens ?" | 40 |
| FLD-PMGMT-SITUATION_ACTUELLE | Situation actuelle | always | "Quelle est la situation locative actuelle ?" | 45 |
| FLD-PMGMT-NOMBRE_LOCATAIRES | Nombre locataires | always | "Combien de locataires actuellement ?" | 50 |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Loyer mensuel total | always | "Quel est le montant total des loyers mensuels ?" | 55 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | always | "Y a-t-il des impayés actuellement ?" | 60 |
| FLD-PMGMT-PERIMETRE_GESTION | Périmètre gestion | always | "Quel périmètre de gestion souhaitez-vous ?" | 65 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat disponible | always | "Mandat de gestion disponible ?" | 70 |
| FLD-PMGMT-DUREE_MANDAT_SOUHAITEE | Durée mandat | always | "Durée de mandat souhaitée ?" | 75 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | always | "Fréquence reporting souhaitée ?" | 80 |
| FLD-PMGMT-DATE_DEBUT_SOUHAITEE | Date début | always | "Quand souhaitez-vous commencer ?" | 85 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 115 |
| FLD-PMGMT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 120 |
| FLD-PMGMT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 125 |
| FLD-PMGMT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 130 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_ADRESSE | Adresse(s) bien(s) | always | "Adresse(s) précise(s) du/des bien(s) ?" | 135 |
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier(s) ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat | when not provided | "Mandat de gestion à établir ?" | 145 |
| FLD-PMGMT-MANDAT_TYPE | Type mandat | when mandate needed | "Type de mandat souhaité ?" | 150 |
| FLD-PMGMT-PIECE_IDENTITE | Pièce identité | always | "Pièce d'identité à fournir ?" | 155 |
| FLD-PMGMT-PIECE_PROPRIETE | Justificatif propriété | always | "Justificatif de propriété ?" | 160 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget pour cette prestation ?" | 165 |
| FLD-PMGMT-BUDGET_DEVISE | Devise | always | "Devise ?" | 170 |
| FLD-PMGMT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 175 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only | 180 |
| FLD-PMGMT-TAUX_OCCUPATION | Taux occupation | informational_only | 185 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | informational_only | 190 |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | verification_only | 195 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | informational_only | 200 |
| FLD-PMGMT-URGENCE | Urgence | informational_only | 205 |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only | 210 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only |
| FLD-PMGMT-TAUX_OCCUPATION | Taux d'occupation | informational_only |
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer moyen | informational_only |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | informational_only |
| FLD-PMGMT-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-PMGMT-MANDAT_TYPE | mandat_dispo = false | verification_only |
| FLD-PMGMT-PIECE_IDENTITE | toujours | verification_only |
| FLD-PMGMT-PIECE_PROPRIETE | toujours | verification_only |
| FLD-PMGMT-MONTANT_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-NOMBRE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-ANCIENNETE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-LITIGES_DETAIL | litiges_en_cours = true | verification_only |
| FLD-PMGMT-ASSURANCE_NOM | assurance_dispo = true | informational_only |
| FLD-PMGMT-ASSURANCE_NUMERO | assurance_dispo = true | informational_only |
| FLD-PMGMT-TYPE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DATE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DEGATS_ESTIMES | gestion_sinistre | informational_only |
| FLD-PMGMT-ENTRETIEN_TYPE | gestion_entretien | informational_only |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | gestion_entretien | informational_only |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | copropriete or syndic | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-PMGMT-CONTACT_TELEPHONE | Personal contact |
| FLD-PMGMT-CONTACT_NOM | Personal identity |
| FLD-PMGMT-CONTACT_EMAIL | Personal contact |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Financial information |
| FLD-PMGMT-REVENUS_ANNUELS | Financial information |
| FLD-PMGMT-IMPAYES_EN_COURS | Financial difficulty |
| FLD-PMGMT-MONTANT_IMPAYES | Financial information |
| FLD-PMGMT-LITIGES_EN_COURS | Dispute information |
| FLD-PMGMT-LITIGES_DETAIL | Detailed dispute information |
| FLD-PMGMT-MANDAT_DISPO | Mandate terms |
| FLD-PMGMT-PIECE_IDENTITE | Identity document |
| FLD-PMGMT-PIECE_PROPRIETE | Property document |
| FLD-PMGMT-ASSURANCE_NUMERO | Insurance contract |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Financial coproperty data |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-PMGMT-DERIVED-REVENUS_MENSUELS | Revenus mensuels estimés | loyer_total * taux_occupation |
| FLD-PMGMT-DERIVED-RENTABILITE | Rentabilité estimée | revenus_annuels / valeur_bien |
| FLD-PMGMT-DERIVED-RISQUE_IMPAYES | Risque impayés | ancienneté + montant + nombre |
| FLD-PMGMT-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | weighted documents |
| FLD-PMGMT-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | nombre_biens + type |
| FLD-PMGMT-DERIVED-URGENCE_SINISTRE | Urgence sinistre | type + degats + date |
| FLD-PMGMT-DERIVED-BESOIN_ENTRETIEN | Besoin entretien | periodicité + dernier |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien gagnez-vous ?" | Non pertinent |
| 2 | "Pourquoi ne gérez-vous pas vous-même ?" | Hors scope |
| 3 | "Avez-vous des problèmes avec vos locataires ?" | Trop intrusif |
| 4 | "Quel est votre emploi ?" | Non pertinent |
| 5 | "Avez-vous déjà eu des impayés ?" | Déjà demandé dans le service |
| 6 | "Combien de pièces ?" | Non canonique |
| 7 | "Voulez-vous vendre ?" | Hors scope |
| 8 | "Avez-vous un autre bien ailleurs ?" | Non pertinent |

---
## MATRIX 3: recouvrement_loyers

### matrix_id
MATRIX-PMGMT-003

### canonical_name
Recouvrement de Loyers

### request_family
PROPERTY_MANAGEMENT

### transaction_type
SERVICE

### property_or_service_type
recouvrement_loyers

### requester_typology
owner_or_coowner

### journey_stage
SERVICE_REQUEST

### description
Service dédié au recouvrement des loyers impayés: relances amiables, mise en demeure, négociation d'échéanciers, procédures de recouvrement. Intervention progressive.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous propriétaire, copropriétaire ou syndic ?" | 10 |
| FLD-PMGMT-TYPE_GESTION | Type de gestion | always | "Quel type de gestion recherchez-vous ?" | 20 |
| FLD-PMGMT-DESCRIPTION | Description besoin | always | "Décrivez votre situation et vos besoins de gestion" | 25 |
| FLD-PMGMT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve(nt) le(s) bien(s) ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-NOMBRE_BIENS | Nombre de biens | always | "Combien de biens concernés par les impayés ?" | 35 |
| FLD-PMGMT-TYPE_BIEN | Type de bien | always | "Types de biens ?" | 40 |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Loyer mensuel | always | "Montant des loyers mensuels ?" | 45 |
| FLD-PMGMT-MONTANT_IMPAYES | Montant impayés | always | "Quel est le montant total des impayés ?" | 50 |
| FLD-PMGMT-NOMBRE_IMPAYES | Nombre impayés | always | "Nombre de mois d'impayés ?" | 55 |
| FLD-PMGMT-ANCIENNETE_IMPAYES | Ancienneté | always | "Depuis quand les impayés ont-ils commencé ?" | 60 |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | always | "Y a-t-il des litiges en cours ?" | 65 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat dispo | always | "Mandat de recouvrement disponible ?" | 70 |
| FLD-PMGMT-LITIGES_DETAIL | Détail litiges | if litiges | "Détail des litiges en cours ?" | 75 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | always | "Fréquence de reporting ?" | 80 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 115 |
| FLD-PMGMT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 120 |
| FLD-PMGMT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 125 |
| FLD-PMGMT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 130 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_ADRESSE | Adresse(s) bien(s) | always | "Adresse(s) précise(s) du/des bien(s) ?" | 135 |
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier(s) ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat | when not provided | "Mandat de gestion à établir ?" | 145 |
| FLD-PMGMT-MANDAT_TYPE | Type mandat | when mandate needed | "Type de mandat souhaité ?" | 150 |
| FLD-PMGMT-PIECE_IDENTITE | Pièce identité | always | "Pièce d'identité à fournir ?" | 155 |
| FLD-PMGMT-PIECE_PROPRIETE | Justificatif propriété | always | "Justificatif de propriété ?" | 160 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget pour cette prestation ?" | 165 |
| FLD-PMGMT-BUDGET_DEVISE | Devise | always | "Devise ?" | 170 |
| FLD-PMGMT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 175 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only | 180 |
| FLD-PMGMT-TAUX_OCCUPATION | Taux occupation | informational_only | 185 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | informational_only | 190 |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | verification_only | 195 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | informational_only | 200 |
| FLD-PMGMT-URGENCE | Urgence | informational_only | 205 |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only | 210 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only |
| FLD-PMGMT-TAUX_OCCUPATION | Taux d'occupation | informational_only |
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer moyen | informational_only |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | informational_only |
| FLD-PMGMT-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-PMGMT-MANDAT_TYPE | mandat_dispo = false | verification_only |
| FLD-PMGMT-PIECE_IDENTITE | toujours | verification_only |
| FLD-PMGMT-PIECE_PROPRIETE | toujours | verification_only |
| FLD-PMGMT-MONTANT_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-NOMBRE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-ANCIENNETE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-LITIGES_DETAIL | litiges_en_cours = true | verification_only |
| FLD-PMGMT-ASSURANCE_NOM | assurance_dispo = true | informational_only |
| FLD-PMGMT-ASSURANCE_NUMERO | assurance_dispo = true | informational_only |
| FLD-PMGMT-TYPE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DATE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DEGATS_ESTIMES | gestion_sinistre | informational_only |
| FLD-PMGMT-ENTRETIEN_TYPE | gestion_entretien | informational_only |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | gestion_entretien | informational_only |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | copropriete or syndic | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-PMGMT-CONTACT_TELEPHONE | Personal contact |
| FLD-PMGMT-CONTACT_NOM | Personal identity |
| FLD-PMGMT-CONTACT_EMAIL | Personal contact |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Financial information |
| FLD-PMGMT-REVENUS_ANNUELS | Financial information |
| FLD-PMGMT-IMPAYES_EN_COURS | Financial difficulty |
| FLD-PMGMT-MONTANT_IMPAYES | Financial information |
| FLD-PMGMT-LITIGES_EN_COURS | Dispute information |
| FLD-PMGMT-LITIGES_DETAIL | Detailed dispute information |
| FLD-PMGMT-MANDAT_DISPO | Mandate terms |
| FLD-PMGMT-PIECE_IDENTITE | Identity document |
| FLD-PMGMT-PIECE_PROPRIETE | Property document |
| FLD-PMGMT-ASSURANCE_NUMERO | Insurance contract |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Financial coproperty data |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-PMGMT-DERIVED-REVENUS_MENSUELS | Revenus mensuels estimés | loyer_total * taux_occupation |
| FLD-PMGMT-DERIVED-RENTABILITE | Rentabilité estimée | revenus_annuels / valeur_bien |
| FLD-PMGMT-DERIVED-RISQUE_IMPAYES | Risque impayés | ancienneté + montant + nombre |
| FLD-PMGMT-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | weighted documents |
| FLD-PMGMT-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | nombre_biens + type |
| FLD-PMGMT-DERIVED-URGENCE_SINISTRE | Urgence sinistre | type + degats + date |
| FLD-PMGMT-DERIVED-BESOIN_ENTRETIEN | Besoin entretien | periodicité + dernier |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien gagnez-vous ?" | Non pertinent |
| 2 | "Pourquoi ne gérez-vous pas vous-même ?" | Hors scope |
| 3 | "Avez-vous des problèmes avec vos locataires ?" | Trop intrusif |
| 4 | "Quel est votre emploi ?" | Non pertinent |
| 5 | "Avez-vous déjà eu des impayés ?" | Déjà demandé dans le service |
| 6 | "Combien de pièces ?" | Non canonique |
| 7 | "Voulez-vous vendre ?" | Hors scope |
| 8 | "Avez-vous un autre bien ailleurs ?" | Non pertinent |

---
## MATRIX 4: gestion_entretien

### matrix_id
MATRIX-PMGMT-004

### canonical_name
Gestion de l'Entretien

### request_family
PROPERTY_MANAGEMENT

### transaction_type
SERVICE

### property_or_service_type
gestion_entretien

### requester_typology
owner_or_coowner

### journey_stage
SERVICE_REQUEST

### description
Service de gestion et coordination des travaux d'entretien: diagnostic, recherche de prestataires, suivi des travaux, contrôle qualité. Entretien préventif et curatif.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous propriétaire, copropriétaire ou syndic ?" | 10 |
| FLD-PMGMT-TYPE_GESTION | Type de gestion | always | "Quel type de gestion recherchez-vous ?" | 20 |
| FLD-PMGMT-DESCRIPTION | Description besoin | always | "Décrivez votre situation et vos besoins de gestion" | 25 |
| FLD-PMGMT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve(nt) le(s) bien(s) ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-NOMBRE_BIENS | Nombre de biens | always | "Combien de biens nécessitent un entretien ?" | 35 |
| FLD-PMGMT-TYPE_BIEN | Type de bien | always | "Types de biens ?" | 40 |
| FLD-PMGMT-ENTRETIEN_TYPE | Type d'entretien | always | "Quel type d'entretien est nécessaire ?" | 45 |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | Périodicité | always | "Quelle périodicité d'entretien ?" | 50 |
| FLD-PMGMT-DERNIER_ENTRETIEN | Dernier entretien | always | "Quand a eu lieu le dernier entretien ?" | 55 |
| FLD-PMGMT-DESCRIPTION | Description travaux | always | "Description des travaux d'entretien nécessaires ?" | 60 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget prévu pour l'entretien ?" | 65 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat disponible | always | "Mandat de gestion disponible ?" | 70 |
| FLD-PMGMT-DUREE_MANDAT_SOUHAITEE | Durée mandat | always | "Durée de mandat souhaitée ?" | 75 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | always | "Fréquence reporting souhaitée ?" | 80 |
| FLD-PMGMT-DATE_DEBUT_SOUHAITEE | Date début | always | "Quand souhaitez-vous commencer ?" | 85 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 115 |
| FLD-PMGMT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 120 |
| FLD-PMGMT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 125 |
| FLD-PMGMT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 130 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_ADRESSE | Adresse(s) bien(s) | always | "Adresse(s) précise(s) du/des bien(s) ?" | 135 |
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier(s) ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat | when not provided | "Mandat de gestion à établir ?" | 145 |
| FLD-PMGMT-MANDAT_TYPE | Type mandat | when mandate needed | "Type de mandat souhaité ?" | 150 |
| FLD-PMGMT-PIECE_IDENTITE | Pièce identité | always | "Pièce d'identité à fournir ?" | 155 |
| FLD-PMGMT-PIECE_PROPRIETE | Justificatif propriété | always | "Justificatif de propriété ?" | 160 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget pour cette prestation ?" | 165 |
| FLD-PMGMT-BUDGET_DEVISE | Devise | always | "Devise ?" | 170 |
| FLD-PMGMT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 175 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only | 180 |
| FLD-PMGMT-TAUX_OCCUPATION | Taux occupation | informational_only | 185 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | informational_only | 190 |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | verification_only | 195 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | informational_only | 200 |
| FLD-PMGMT-URGENCE | Urgence | informational_only | 205 |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only | 210 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only |
| FLD-PMGMT-TAUX_OCCUPATION | Taux d'occupation | informational_only |
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer moyen | informational_only |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | informational_only |
| FLD-PMGMT-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-PMGMT-MANDAT_TYPE | mandat_dispo = false | verification_only |
| FLD-PMGMT-PIECE_IDENTITE | toujours | verification_only |
| FLD-PMGMT-PIECE_PROPRIETE | toujours | verification_only |
| FLD-PMGMT-MONTANT_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-NOMBRE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-ANCIENNETE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-LITIGES_DETAIL | litiges_en_cours = true | verification_only |
| FLD-PMGMT-ASSURANCE_NOM | assurance_dispo = true | informational_only |
| FLD-PMGMT-ASSURANCE_NUMERO | assurance_dispo = true | informational_only |
| FLD-PMGMT-TYPE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DATE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DEGATS_ESTIMES | gestion_sinistre | informational_only |
| FLD-PMGMT-ENTRETIEN_TYPE | gestion_entretien | informational_only |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | gestion_entretien | informational_only |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | copropriete or syndic | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-PMGMT-CONTACT_TELEPHONE | Personal contact |
| FLD-PMGMT-CONTACT_NOM | Personal identity |
| FLD-PMGMT-CONTACT_EMAIL | Personal contact |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Financial information |
| FLD-PMGMT-REVENUS_ANNUELS | Financial information |
| FLD-PMGMT-IMPAYES_EN_COURS | Financial difficulty |
| FLD-PMGMT-MONTANT_IMPAYES | Financial information |
| FLD-PMGMT-LITIGES_EN_COURS | Dispute information |
| FLD-PMGMT-LITIGES_DETAIL | Detailed dispute information |
| FLD-PMGMT-MANDAT_DISPO | Mandate terms |
| FLD-PMGMT-PIECE_IDENTITE | Identity document |
| FLD-PMGMT-PIECE_PROPRIETE | Property document |
| FLD-PMGMT-ASSURANCE_NUMERO | Insurance contract |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Financial coproperty data |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-PMGMT-DERIVED-REVENUS_MENSUELS | Revenus mensuels estimés | loyer_total * taux_occupation |
| FLD-PMGMT-DERIVED-RENTABILITE | Rentabilité estimée | revenus_annuels / valeur_bien |
| FLD-PMGMT-DERIVED-RISQUE_IMPAYES | Risque impayés | ancienneté + montant + nombre |
| FLD-PMGMT-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | weighted documents |
| FLD-PMGMT-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | nombre_biens + type |
| FLD-PMGMT-DERIVED-URGENCE_SINISTRE | Urgence sinistre | type + degats + date |
| FLD-PMGMT-DERIVED-BESOIN_ENTRETIEN | Besoin entretien | periodicité + dernier |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien gagnez-vous ?" | Non pertinent |
| 2 | "Pourquoi ne gérez-vous pas vous-même ?" | Hors scope |
| 3 | "Avez-vous des problèmes avec vos locataires ?" | Trop intrusif |
| 4 | "Quel est votre emploi ?" | Non pertinent |
| 5 | "Avez-vous déjà eu des impayés ?" | Déjà demandé dans le service |
| 6 | "Combien de pièces ?" | Non canonique |
| 7 | "Voulez-vous vendre ?" | Hors scope |
| 8 | "Avez-vous un autre bien ailleurs ?" | Non pertinent |

---
## MATRIX 5: gestion_sinistre

### matrix_id
MATRIX-PMGMT-005

### canonical_name
Gestion de Sinistre

### request_family
PROPERTY_MANAGEMENT

### transaction_type
SERVICE

### property_or_service_type
gestion_sinistre

### requester_typology
owner_or_coowner

### journey_stage
SERVICE_REQUEST

### description
Service de gestion des sinistres immobiliers: déclaration assurance, expertise, suivi des réparations, coordination des intervenants, accompagnement du propriétaire et du locataire.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous propriétaire, copropriétaire ou syndic ?" | 10 |
| FLD-PMGMT-TYPE_GESTION | Type de gestion | always | "Quel type de gestion recherchez-vous ?" | 20 |
| FLD-PMGMT-DESCRIPTION | Description besoin | always | "Décrivez votre situation et vos besoins de gestion" | 25 |
| FLD-PMGMT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve(nt) le(s) bien(s) ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-NOMBRE_BIENS | Nombre de biens | always | "Combien de biens sont sinistrés ?" | 35 |
| FLD-PMGMT-TYPE_BIEN | Type de bien | always | "Type de bien sinistré ?" | 40 |
| FLD-PMGMT-TYPE_SINISTRE | Type de sinistre | always | "Quel type de sinistre ?" | 45 |
| FLD-PMGMT-DATE_SINISTRE | Date sinistre | always | "Quand le sinistre est-il survenu ?" | 50 |
| FLD-PMGMT-DEGATS_ESTIMES | Dégâts estimés | always | "Quelle est l'ampleur des dégâts ?" | 55 |
| FLD-PMGMT-ASSURANCE_DISPO | Assurance | always | "Avez-vous une assurance couvrant ce sinistre ?" | 60 |
| FLD-PMGMT-URGENCE | Urgence | always | "Quel est le niveau d'urgence ?" | 65 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | always | "Litiges en cours liés à ce sinistre ?" | 70 |
| FLD-PMGMT-ASSURANCE_NOM | Assurance nom | if insurance | "Nom de votre assurance ?" | 75 |
| FLD-PMGMT-ASSURANCE_NUMERO | Contrat assurance | if insurance | "Numéro de contrat ?" | 80 |
| FLD-PMGMT-DESCRIPTION | Description | always | "Description détaillée du sinistre ?" | 85 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget pour la gestion du sinistre ?" | 90 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 115 |
| FLD-PMGMT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 120 |
| FLD-PMGMT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 125 |
| FLD-PMGMT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 130 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_ADRESSE | Adresse(s) bien(s) | always | "Adresse(s) précise(s) du/des bien(s) ?" | 135 |
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier(s) ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat | when not provided | "Mandat de gestion à établir ?" | 145 |
| FLD-PMGMT-MANDAT_TYPE | Type mandat | when mandate needed | "Type de mandat souhaité ?" | 150 |
| FLD-PMGMT-PIECE_IDENTITE | Pièce identité | always | "Pièce d'identité à fournir ?" | 155 |
| FLD-PMGMT-PIECE_PROPRIETE | Justificatif propriété | always | "Justificatif de propriété ?" | 160 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget pour cette prestation ?" | 165 |
| FLD-PMGMT-BUDGET_DEVISE | Devise | always | "Devise ?" | 170 |
| FLD-PMGMT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 175 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only | 180 |
| FLD-PMGMT-TAUX_OCCUPATION | Taux occupation | informational_only | 185 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | informational_only | 190 |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | verification_only | 195 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | informational_only | 200 |
| FLD-PMGMT-URGENCE | Urgence | informational_only | 205 |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only | 210 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only |
| FLD-PMGMT-TAUX_OCCUPATION | Taux d'occupation | informational_only |
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer moyen | informational_only |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | informational_only |
| FLD-PMGMT-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-PMGMT-MANDAT_TYPE | mandat_dispo = false | verification_only |
| FLD-PMGMT-PIECE_IDENTITE | toujours | verification_only |
| FLD-PMGMT-PIECE_PROPRIETE | toujours | verification_only |
| FLD-PMGMT-MONTANT_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-NOMBRE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-ANCIENNETE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-LITIGES_DETAIL | litiges_en_cours = true | verification_only |
| FLD-PMGMT-ASSURANCE_NOM | assurance_dispo = true | informational_only |
| FLD-PMGMT-ASSURANCE_NUMERO | assurance_dispo = true | informational_only |
| FLD-PMGMT-TYPE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DATE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DEGATS_ESTIMES | gestion_sinistre | informational_only |
| FLD-PMGMT-ENTRETIEN_TYPE | gestion_entretien | informational_only |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | gestion_entretien | informational_only |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | copropriete or syndic | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-PMGMT-CONTACT_TELEPHONE | Personal contact |
| FLD-PMGMT-CONTACT_NOM | Personal identity |
| FLD-PMGMT-CONTACT_EMAIL | Personal contact |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Financial information |
| FLD-PMGMT-REVENUS_ANNUELS | Financial information |
| FLD-PMGMT-IMPAYES_EN_COURS | Financial difficulty |
| FLD-PMGMT-MONTANT_IMPAYES | Financial information |
| FLD-PMGMT-LITIGES_EN_COURS | Dispute information |
| FLD-PMGMT-LITIGES_DETAIL | Detailed dispute information |
| FLD-PMGMT-MANDAT_DISPO | Mandate terms |
| FLD-PMGMT-PIECE_IDENTITE | Identity document |
| FLD-PMGMT-PIECE_PROPRIETE | Property document |
| FLD-PMGMT-ASSURANCE_NUMERO | Insurance contract |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Financial coproperty data |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-PMGMT-DERIVED-REVENUS_MENSUELS | Revenus mensuels estimés | loyer_total * taux_occupation |
| FLD-PMGMT-DERIVED-RENTABILITE | Rentabilité estimée | revenus_annuels / valeur_bien |
| FLD-PMGMT-DERIVED-RISQUE_IMPAYES | Risque impayés | ancienneté + montant + nombre |
| FLD-PMGMT-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | weighted documents |
| FLD-PMGMT-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | nombre_biens + type |
| FLD-PMGMT-DERIVED-URGENCE_SINISTRE | Urgence sinistre | type + degats + date |
| FLD-PMGMT-DERIVED-BESOIN_ENTRETIEN | Besoin entretien | periodicité + dernier |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien gagnez-vous ?" | Non pertinent |
| 2 | "Pourquoi ne gérez-vous pas vous-même ?" | Hors scope |
| 3 | "Avez-vous des problèmes avec vos locataires ?" | Trop intrusif |
| 4 | "Quel est votre emploi ?" | Non pertinent |
| 5 | "Avez-vous déjà eu des impayés ?" | Déjà demandé dans le service |
| 6 | "Combien de pièces ?" | Non canonique |
| 7 | "Voulez-vous vendre ?" | Hors scope |
| 8 | "Avez-vous un autre bien ailleurs ?" | Non pertinent |

---
## MATRIX 6: gestion_copropriete

### matrix_id
MATRIX-PMGMT-006

### canonical_name
Gestion de Copropriété

### request_family
PROPERTY_MANAGEMENT

### transaction_type
SERVICE

### property_or_service_type
gestion_copropriete

### requester_typology
owner_or_coowner

### journey_stage
SERVICE_REQUEST

### description
Service de gestion d'une copropriété: administration courante, tenue de l'assemblée générale, gestion des parties communes, suivi des charges, relations avec les copropriétaires.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous propriétaire, copropriétaire ou syndic ?" | 10 |
| FLD-PMGMT-TYPE_GESTION | Type de gestion | always | "Quel type de gestion recherchez-vous ?" | 20 |
| FLD-PMGMT-DESCRIPTION | Description besoin | always | "Décrivez votre situation et vos besoins de gestion" | 25 |
| FLD-PMGMT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve(nt) le(s) bien(s) ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-NOMBRE_BIENS | Nombre de biens | always | "Combien de biens sont concernés ?" | 35 |
| FLD-PMGMT-TYPE_BIEN | Type de bien | always | "Types de biens ?" | 40 |
| FLD-PMGMT-SITUATION_ACTUELLE | Situation actuelle | always | "Situation actuelle ?" | 45 |
| FLD-PMGMT-PERIMETRE_GESTION | Périmètre | always | "Périmètre de gestion souhaité ?" | 50 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat disponible | always | "Mandat de gestion disponible ?" | 70 |
| FLD-PMGMT-DUREE_MANDAT_SOUHAITEE | Durée mandat | always | "Durée de mandat souhaitée ?" | 75 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | always | "Fréquence reporting souhaitée ?" | 80 |
| FLD-PMGMT-DATE_DEBUT_SOUHAITEE | Date début | always | "Quand souhaitez-vous commencer ?" | 85 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 115 |
| FLD-PMGMT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 120 |
| FLD-PMGMT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 125 |
| FLD-PMGMT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 130 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_ADRESSE | Adresse(s) bien(s) | always | "Adresse(s) précise(s) du/des bien(s) ?" | 135 |
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier(s) ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat | when not provided | "Mandat de gestion à établir ?" | 145 |
| FLD-PMGMT-MANDAT_TYPE | Type mandat | when mandate needed | "Type de mandat souhaité ?" | 150 |
| FLD-PMGMT-PIECE_IDENTITE | Pièce identité | always | "Pièce d'identité à fournir ?" | 155 |
| FLD-PMGMT-PIECE_PROPRIETE | Justificatif propriété | always | "Justificatif de propriété ?" | 160 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget pour cette prestation ?" | 165 |
| FLD-PMGMT-BUDGET_DEVISE | Devise | always | "Devise ?" | 170 |
| FLD-PMGMT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 175 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only | 180 |
| FLD-PMGMT-TAUX_OCCUPATION | Taux occupation | informational_only | 185 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | informational_only | 190 |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | verification_only | 195 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | informational_only | 200 |
| FLD-PMGMT-URGENCE | Urgence | informational_only | 205 |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only | 210 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only |
| FLD-PMGMT-TAUX_OCCUPATION | Taux d'occupation | informational_only |
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer moyen | informational_only |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | informational_only |
| FLD-PMGMT-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-PMGMT-MANDAT_TYPE | mandat_dispo = false | verification_only |
| FLD-PMGMT-PIECE_IDENTITE | toujours | verification_only |
| FLD-PMGMT-PIECE_PROPRIETE | toujours | verification_only |
| FLD-PMGMT-MONTANT_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-NOMBRE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-ANCIENNETE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-LITIGES_DETAIL | litiges_en_cours = true | verification_only |
| FLD-PMGMT-ASSURANCE_NOM | assurance_dispo = true | informational_only |
| FLD-PMGMT-ASSURANCE_NUMERO | assurance_dispo = true | informational_only |
| FLD-PMGMT-TYPE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DATE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DEGATS_ESTIMES | gestion_sinistre | informational_only |
| FLD-PMGMT-ENTRETIEN_TYPE | gestion_entretien | informational_only |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | gestion_entretien | informational_only |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | copropriete or syndic | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-PMGMT-CONTACT_TELEPHONE | Personal contact |
| FLD-PMGMT-CONTACT_NOM | Personal identity |
| FLD-PMGMT-CONTACT_EMAIL | Personal contact |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Financial information |
| FLD-PMGMT-REVENUS_ANNUELS | Financial information |
| FLD-PMGMT-IMPAYES_EN_COURS | Financial difficulty |
| FLD-PMGMT-MONTANT_IMPAYES | Financial information |
| FLD-PMGMT-LITIGES_EN_COURS | Dispute information |
| FLD-PMGMT-LITIGES_DETAIL | Detailed dispute information |
| FLD-PMGMT-MANDAT_DISPO | Mandate terms |
| FLD-PMGMT-PIECE_IDENTITE | Identity document |
| FLD-PMGMT-PIECE_PROPRIETE | Property document |
| FLD-PMGMT-ASSURANCE_NUMERO | Insurance contract |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Financial coproperty data |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-PMGMT-DERIVED-REVENUS_MENSUELS | Revenus mensuels estimés | loyer_total * taux_occupation |
| FLD-PMGMT-DERIVED-RENTABILITE | Rentabilité estimée | revenus_annuels / valeur_bien |
| FLD-PMGMT-DERIVED-RISQUE_IMPAYES | Risque impayés | ancienneté + montant + nombre |
| FLD-PMGMT-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | weighted documents |
| FLD-PMGMT-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | nombre_biens + type |
| FLD-PMGMT-DERIVED-URGENCE_SINISTRE | Urgence sinistre | type + degats + date |
| FLD-PMGMT-DERIVED-BESOIN_ENTRETIEN | Besoin entretien | periodicité + dernier |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien gagnez-vous ?" | Non pertinent |
| 2 | "Pourquoi ne gérez-vous pas vous-même ?" | Hors scope |
| 3 | "Avez-vous des problèmes avec vos locataires ?" | Trop intrusif |
| 4 | "Quel est votre emploi ?" | Non pertinent |
| 5 | "Avez-vous déjà eu des impayés ?" | Déjà demandé dans le service |
| 6 | "Combien de pièces ?" | Non canonique |
| 7 | "Voulez-vous vendre ?" | Hors scope |
| 8 | "Avez-vous un autre bien ailleurs ?" | Non pertinent |

---
## MATRIX 7: syndic_benévole

### matrix_id
MATRIX-PMGMT-007

### canonical_name
Syndic Bénévole

### request_family
PROPERTY_MANAGEMENT

### transaction_type
SERVICE

### property_or_service_type
syndic_benévole

### requester_typology
owner_or_coowner

### journey_stage
SERVICE_REQUEST

### description
Accompagnement et outils pour le syndic bénévole: modèles de documents, assistance juridique, plateforme de gestion, mise en relation avec prestataires. Solution pour petites copropriétés.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous propriétaire, copropriétaire ou syndic ?" | 10 |
| FLD-PMGMT-TYPE_GESTION | Type de gestion | always | "Quel type de gestion recherchez-vous ?" | 20 |
| FLD-PMGMT-DESCRIPTION | Description besoin | always | "Décrivez votre situation et vos besoins de gestion" | 25 |
| FLD-PMGMT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve(nt) le(s) bien(s) ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier de la copropriété ?" | 35 |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | Nombre de lots | always | "Combien de lots dans la copropriété ?" | 40 |
| FLD-PMGMT-TYPE_BIEN | Type de bien | always | "Type de la copropriété (résidentielle, mixte) ?" | 45 |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | Règlement copropriété | always | "Existe-t-il un règlement de copropriété ?" | 50 |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | Syndic actuel | always | "Y a-t-il un syndic actuellement en place ?" | 55 |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Budget annuel | if budget known | "Budget annuel de la copropriété ?" | 60 |
| FLD-PMGMT-DATE_DEBUT_SOUHAITEE | Date début | always | "À partir de quand souhaitez-vous le service ?" | 65 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | PV AG | always | "Procès-verbaux d'AG disponibles ?" | 70 |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | Fonds urgence | always | "Fonds d'urgence constitués ?" | 75 |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Budget annuel | always | "Budget annuel prévisionnel ?" | 80 |
| FLD-PMGMT-MANDAT_DISPO | Mandat | always | "Mandat du syndic actuel disponible ?" | 85 |
| FLD-PMGMT-DUREE_MANDAT_SOUHAITEE | Durée mandat | always | "Durée du mandat souhaitée ?" | 90 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | always | "Fréquence reporting souhaitée ?" | 95 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 115 |
| FLD-PMGMT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 120 |
| FLD-PMGMT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 125 |
| FLD-PMGMT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 130 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_ADRESSE | Adresse(s) bien(s) | always | "Adresse(s) précise(s) du/des bien(s) ?" | 135 |
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier(s) ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat | when not provided | "Mandat de gestion à établir ?" | 145 |
| FLD-PMGMT-MANDAT_TYPE | Type mandat | when mandate needed | "Type de mandat souhaité ?" | 150 |
| FLD-PMGMT-PIECE_IDENTITE | Pièce identité | always | "Pièce d'identité à fournir ?" | 155 |
| FLD-PMGMT-PIECE_PROPRIETE | Justificatif propriété | always | "Justificatif de propriété ?" | 160 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget pour cette prestation ?" | 165 |
| FLD-PMGMT-BUDGET_DEVISE | Devise | always | "Devise ?" | 170 |
| FLD-PMGMT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 175 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only | 180 |
| FLD-PMGMT-TAUX_OCCUPATION | Taux occupation | informational_only | 185 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | informational_only | 190 |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | verification_only | 195 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | informational_only | 200 |
| FLD-PMGMT-URGENCE | Urgence | informational_only | 205 |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only | 210 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only |
| FLD-PMGMT-TAUX_OCCUPATION | Taux d'occupation | informational_only |
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer moyen | informational_only |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | informational_only |
| FLD-PMGMT-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-PMGMT-MANDAT_TYPE | mandat_dispo = false | verification_only |
| FLD-PMGMT-PIECE_IDENTITE | toujours | verification_only |
| FLD-PMGMT-PIECE_PROPRIETE | toujours | verification_only |
| FLD-PMGMT-MONTANT_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-NOMBRE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-ANCIENNETE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-LITIGES_DETAIL | litiges_en_cours = true | verification_only |
| FLD-PMGMT-ASSURANCE_NOM | assurance_dispo = true | informational_only |
| FLD-PMGMT-ASSURANCE_NUMERO | assurance_dispo = true | informational_only |
| FLD-PMGMT-TYPE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DATE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DEGATS_ESTIMES | gestion_sinistre | informational_only |
| FLD-PMGMT-ENTRETIEN_TYPE | gestion_entretien | informational_only |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | gestion_entretien | informational_only |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | copropriete or syndic | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-PMGMT-CONTACT_TELEPHONE | Personal contact |
| FLD-PMGMT-CONTACT_NOM | Personal identity |
| FLD-PMGMT-CONTACT_EMAIL | Personal contact |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Financial information |
| FLD-PMGMT-REVENUS_ANNUELS | Financial information |
| FLD-PMGMT-IMPAYES_EN_COURS | Financial difficulty |
| FLD-PMGMT-MONTANT_IMPAYES | Financial information |
| FLD-PMGMT-LITIGES_EN_COURS | Dispute information |
| FLD-PMGMT-LITIGES_DETAIL | Detailed dispute information |
| FLD-PMGMT-MANDAT_DISPO | Mandate terms |
| FLD-PMGMT-PIECE_IDENTITE | Identity document |
| FLD-PMGMT-PIECE_PROPRIETE | Property document |
| FLD-PMGMT-ASSURANCE_NUMERO | Insurance contract |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Financial coproperty data |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-PMGMT-DERIVED-REVENUS_MENSUELS | Revenus mensuels estimés | loyer_total * taux_occupation |
| FLD-PMGMT-DERIVED-RENTABILITE | Rentabilité estimée | revenus_annuels / valeur_bien |
| FLD-PMGMT-DERIVED-RISQUE_IMPAYES | Risque impayés | ancienneté + montant + nombre |
| FLD-PMGMT-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | weighted documents |
| FLD-PMGMT-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | nombre_biens + type |
| FLD-PMGMT-DERIVED-URGENCE_SINISTRE | Urgence sinistre | type + degats + date |
| FLD-PMGMT-DERIVED-BESOIN_ENTRETIEN | Besoin entretien | periodicité + dernier |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien gagnez-vous ?" | Non pertinent |
| 2 | "Pourquoi ne gérez-vous pas vous-même ?" | Hors scope |
| 3 | "Avez-vous des problèmes avec vos locataires ?" | Trop intrusif |
| 4 | "Quel est votre emploi ?" | Non pertinent |
| 5 | "Avez-vous déjà eu des impayés ?" | Déjà demandé dans le service |
| 6 | "Combien de pièces ?" | Non canonique |
| 7 | "Voulez-vous vendre ?" | Hors scope |
| 8 | "Avez-vous un autre bien ailleurs ?" | Non pertinent |

---
## MATRIX 8: syndic_professionnel

### matrix_id
MATRIX-PMGMT-008

### canonical_name
Syndic Professionnel

### request_family
PROPERTY_MANAGEMENT

### transaction_type
SERVICE

### property_or_service_type
syndic_professionnel

### requester_typology
owner_or_coowner

### journey_stage
SERVICE_REQUEST

### description
Service complet de syndic professionnel: gestion administrative, financière et technique de la copropriété. Tenue des comptes, organisation AG, suivi des travaux, relations fournisseurs.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous propriétaire, copropriétaire ou syndic ?" | 10 |
| FLD-PMGMT-TYPE_GESTION | Type de gestion | always | "Quel type de gestion recherchez-vous ?" | 20 |
| FLD-PMGMT-DESCRIPTION | Description besoin | always | "Décrivez votre situation et vos besoins de gestion" | 25 |
| FLD-PMGMT-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se trouve(nt) le(s) bien(s) ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier de la copropriété ?" | 35 |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | Nombre de lots | always | "Combien de lots dans la copropriété ?" | 40 |
| FLD-PMGMT-TYPE_BIEN | Type de bien | always | "Type de la copropriété (résidentielle, mixte) ?" | 45 |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | Règlement copropriété | always | "Existe-t-il un règlement de copropriété ?" | 50 |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | Syndic actuel | always | "Y a-t-il un syndic actuellement en place ?" | 55 |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Budget annuel | if budget known | "Budget annuel de la copropriété ?" | 60 |
| FLD-PMGMT-DATE_DEBUT_SOUHAITEE | Date début | always | "À partir de quand souhaitez-vous le service ?" | 65 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | PV AG | always | "Procès-verbaux d'AG disponibles ?" | 70 |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | Fonds urgence | always | "Fonds d'urgence constitués ?" | 75 |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Budget annuel | always | "Budget annuel prévisionnel ?" | 80 |
| FLD-PMGMT-MANDAT_DISPO | Mandat | always | "Mandat du syndic actuel disponible ?" | 85 |
| FLD-PMGMT-DUREE_MANDAT_SOUHAITEE | Durée mandat | always | "Durée du mandat souhaitée ?" | 90 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | always | "Fréquence reporting souhaitée ?" | 95 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 115 |
| FLD-PMGMT-CONTACT_TELEPHONE | Téléphone | always | "Votre numéro de téléphone ?" | 120 |
| FLD-PMGMT-CONTACT_EMAIL | Email | always | "Votre adresse email ?" | 125 |
| FLD-PMGMT-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 130 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-LOCALISATION_ADRESSE | Adresse(s) bien(s) | always | "Adresse(s) précise(s) du/des bien(s) ?" | 135 |
| FLD-PMGMT-LOCALISATION_QUARTIER | Quartier | always | "Quartier(s) ?" | 140 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-PMGMT-MANDAT_DISPO | Mandat | when not provided | "Mandat de gestion à établir ?" | 145 |
| FLD-PMGMT-MANDAT_TYPE | Type mandat | when mandate needed | "Type de mandat souhaité ?" | 150 |
| FLD-PMGMT-PIECE_IDENTITE | Pièce identité | always | "Pièce d'identité à fournir ?" | 155 |
| FLD-PMGMT-PIECE_PROPRIETE | Justificatif propriété | always | "Justificatif de propriété ?" | 160 |
| FLD-PMGMT-BUDGET_PRESTATION | Budget | always | "Budget pour cette prestation ?" | 165 |
| FLD-PMGMT-BUDGET_DEVISE | Devise | always | "Devise ?" | 170 |
| FLD-PMGMT-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification souhaité ?" | 175 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only | 180 |
| FLD-PMGMT-TAUX_OCCUPATION | Taux occupation | informational_only | 185 |
| FLD-PMGMT-IMPAYES_EN_COURS | Impayés | informational_only | 190 |
| FLD-PMGMT-LITIGES_EN_COURS | Litiges | verification_only | 195 |
| FLD-PMGMT-FREQUENCE_REPORTING | Reporting | informational_only | 200 |
| FLD-PMGMT-URGENCE | Urgence | informational_only | 205 |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only | 210 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-PMGMT-REVENUS_ANNUELS | Revenus annuels | informational_only |
| FLD-PMGMT-TAUX_OCCUPATION | Taux d'occupation | informational_only |
| FLD-PMGMT-LOYER_MENSUEL_MOYEN | Loyer moyen | informational_only |
| FLD-PMGMT-CHARGES_MENSUELLES | Charges mensuelles | informational_only |
| FLD-PMGMT-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-PMGMT-COMMENTAIRE | Commentaire | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-PMGMT-MANDAT_TYPE | mandat_dispo = false | verification_only |
| FLD-PMGMT-PIECE_IDENTITE | toujours | verification_only |
| FLD-PMGMT-PIECE_PROPRIETE | toujours | verification_only |
| FLD-PMGMT-MONTANT_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-NOMBRE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-ANCIENNETE_IMPAYES | impayes_en_cours = true | informational_only |
| FLD-PMGMT-LITIGES_DETAIL | litiges_en_cours = true | verification_only |
| FLD-PMGMT-ASSURANCE_NOM | assurance_dispo = true | informational_only |
| FLD-PMGMT-ASSURANCE_NUMERO | assurance_dispo = true | informational_only |
| FLD-PMGMT-TYPE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DATE_SINISTRE | gestion_sinistre | informational_only |
| FLD-PMGMT-DEGATS_ESTIMES | gestion_sinistre | informational_only |
| FLD-PMGMT-ENTRETIEN_TYPE | gestion_entretien | informational_only |
| FLD-PMGMT-ENTRETIEN_PERIODICITE | gestion_entretien | informational_only |
| FLD-PMGMT-COPROPRIETE_NOMBRE_LOTS | syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_REGLEMENT | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_SYNDIC_ACTUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | copropriete or syndic | informational_only |
| FLD-PMGMT-COPROPRIETE_PROCES_VERBAUX | copropriete or syndic | verification_only |
| FLD-PMGMT-COPROPRIETE_FONDS_URGENCE | copropriete or syndic | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-PMGMT-CONTACT_TELEPHONE | Personal contact |
| FLD-PMGMT-CONTACT_NOM | Personal identity |
| FLD-PMGMT-CONTACT_EMAIL | Personal contact |
| FLD-PMGMT-LOYER_MENSUEL_TOTAL | Financial information |
| FLD-PMGMT-REVENUS_ANNUELS | Financial information |
| FLD-PMGMT-IMPAYES_EN_COURS | Financial difficulty |
| FLD-PMGMT-MONTANT_IMPAYES | Financial information |
| FLD-PMGMT-LITIGES_EN_COURS | Dispute information |
| FLD-PMGMT-LITIGES_DETAIL | Detailed dispute information |
| FLD-PMGMT-MANDAT_DISPO | Mandate terms |
| FLD-PMGMT-PIECE_IDENTITE | Identity document |
| FLD-PMGMT-PIECE_PROPRIETE | Property document |
| FLD-PMGMT-ASSURANCE_NUMERO | Insurance contract |
| FLD-PMGMT-COPROPRIETE_BUDGET_ANNUEL | Financial coproperty data |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-PMGMT-DERIVED-REVENUS_MENSUELS | Revenus mensuels estimés | loyer_total * taux_occupation |
| FLD-PMGMT-DERIVED-RENTABILITE | Rentabilité estimée | revenus_annuels / valeur_bien |
| FLD-PMGMT-DERIVED-RISQUE_IMPAYES | Risque impayés | ancienneté + montant + nombre |
| FLD-PMGMT-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | weighted documents |
| FLD-PMGMT-DERIVED-PROFIL_PROPRIETAIRE | Profil propriétaire | nombre_biens + type |
| FLD-PMGMT-DERIVED-URGENCE_SINISTRE | Urgence sinistre | type + degats + date |
| FLD-PMGMT-DERIVED-BESOIN_ENTRETIEN | Besoin entretien | periodicité + dernier |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Combien gagnez-vous ?" | Non pertinent |
| 2 | "Pourquoi ne gérez-vous pas vous-même ?" | Hors scope |
| 3 | "Avez-vous des problèmes avec vos locataires ?" | Trop intrusif |
| 4 | "Quel est votre emploi ?" | Non pertinent |
| 5 | "Avez-vous déjà eu des impayés ?" | Déjà demandé dans le service |
| 6 | "Combien de pièces ?" | Non canonique |
| 7 | "Voulez-vous vendre ?" | Hors scope |
| 8 | "Avez-vous un autre bien ailleurs ?" | Non pertinent |

---

# End of Document — Property Management Matrices
