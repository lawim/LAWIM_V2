# Document and Legal Service Qualification Matrices — LAWIM Heritage Gold

**Document ID:** LAWIM-GOLD-MATRICES-DOCUMENT-LEGAL-V1
**Mission:** LAWIM Heritage Gold — Qualification des services documentaires et juridiques
**Date:** 2026-07-15
**Statut:** CANONICAL — Reference document for architecture H1

---

# Table of Contents

| # | Service Type | Matrix ID | Category |
|---|-------------|-----------|----------|
| 1 | verification_titre_foncier | MATRIX-DOC-LEGAL-001 | DOCUMENT_VERIFICATION |
| 2 | recherche_documentaire | MATRIX-DOC-LEGAL-002 | DOCUMENT_RESEARCH |
| 3 | constitution_dossier_permis | MATRIX-DOC-LEGAL-003 | PERMIT |
| 4 | aide_redaction_acte | MATRIX-DOC-LEGAL-004 | LEGAL_DRAFTING |
| 5 | mediation_immobiliere | MATRIX-DOC-LEGAL-005 | MEDIATION |
| 6 | conseil_juridique_immobilier | MATRIX-DOC-LEGAL-006 | LEGAL_ADVICE |
| 7 | verification_conformite | MATRIX-DOC-LEGAL-007 | COMPLIANCE |
| 8 | audit_documentaire | MATRIX-DOC-LEGAL-008 | DOCUMENT_AUDIT |

---

# Common Rules for All Document and Legal Service Matrices

## Qualification Order

| Order | Step | Field(s) |
|:-----:|------|----------|
| 1 | Identité demandeur | FLD-DOC-IDENTITE_DEMANDEUR |
| 2 | Type de service | FLD-DOC-TYPE_SERVICE |
| 3 | Objet de la demande | FLD-DOC-OBJET |
| 4 | Localisation du bien | FLD-DOC-LOCALISATION_VILLE |
| 5 | Documents disponibles | FLD-DOC-DOCUMENTS_DISPO |
| 6 | Urgence | FLD-DOC-URGENCE |
| 7 | Budget | FLD-DOC-BUDGET |
| 8 | Contact | FLD-DOC-CONTACT_NOM, FLD-DOC-CONTACT_TELEPHONE |
| 9 | Confirmation | Récapitulatif |
| 10 | Escalade | Mise en relation avec professionnel |

## Matching Role Semantics

| Role | Description |
|------|-------------|
| hard_constraint | Must match exactly; otherwise excluded |
| soft_constraint | Strong preference but flexible |
| verification_only | For verification purposes |
| informational_only | For display only |
| transaction_blocker | Must be resolved before execution |

---

## Master Field Catalog (Document & Legal Services)

| FIELD-ID | label | data_type | allowed_values | privacy | source | confidence |
|----------|-------|-----------|----------------|--------|--------|------------|
| FLD-DOC-IDENTITE_DEMANDEUR | Identité demandeur | enum | PARTICULIER, PROFESSIONNEL, ENTREPRISE, PROMOTEUR, NOTAIRE, AVOCAT | public | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-TYPE_SERVICE | Type de service | enum | VERIFICATION_TITRE, RECHERCHE_DOC, CONSTITUTION_PERMIS, REDACTION_ACTE, MEDIATION, CONSEIL_JURIDIQUE, VERIFICATION_CONFORMITE, AUDIT_DOC | public | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-OBJET | Objet de la demande | text | Free text | public | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-LOCALISATION_VILLE | Ville | string | LAWIM city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | string | Per-city list | public | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-LOCALISATION_ADRESSE | Adresse bien | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-TYPE_BIEN | Type de bien | enum | APPARTEMENT, MAISON, VILLA, TERRAIN, COMMERCIAL, INDUSTRIEL, IMMEUBLE, AUTRE | public | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-REFERENCE_CADASTRALE | Référence cadastrale | string | Alphanumeric | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-NUMERO_TITRE | Numéro titre foncier | string | Alphanumeric | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-DOCUMENTS_DISPO | Documents disponibles | enum[] | PIECE_IDENTITE, TITRE_FONCIER, ACTE_VENTE, CERTIFICAT_PROPRIETE, PLAN_BORNAGE, LOTISSEMENT, PERMIS_CONSTRUIRE, PROMESSE_VENTE, BAIL, REGLEMENT_COPROPRIETE, AUTRE | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents manquants | enum[] | Same as available | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-URGENCE | Urgence | enum | URGENT, 48H, CETTE_SEMAINE, CE_MOIS, PAS_URGENT | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-DATE_SOUHAITEE | Date souhaitée | date | Valid date | public | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-BUDGET | Budget | float | Positive float | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-BUDGET_DEVISE | Devise | enum | XAF, EUR, USD | public | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | text | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-DOC-PROFESSIONNEL_RECHERCHE | Professionnel recherché | enum | NOTAIRE, AVOCAT, GEOMETRE, ARCHITECTE, AGENT_IMMOBILIER, EXPERT_IMMOBILIER, HUISSIER | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-AUTORISATION_TIERS | Autorisation tiers | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-IDENTITE_TIERS | Identité tiers | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-PIECE_TIERS | Pièce tiers | string | URL | confidential | EXPERT_PROPOSAL | LOW |
| FLD-DOC-CONTACT_NOM | Nom contact | string | Free text | private | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-CONTACT_TELEPHONE | Téléphone | string | Valid phone | private | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-CONTACT_EMAIL | Email | string | Valid email | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-CONTACT_CANAL | Canal préféré | enum | WHATSAPP, TELEGRAM, SMS, EMAIL, APPEL | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-CONTACT_DISPO | Disponibilité contact | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-DOC-COMMENTAIRE | Commentaire | text | Free text | public | EXPERT_PROPOSAL | LOW |
| FLD-DOC-NIVEAU_VERIFICATION | Niveau vérification | enum | COMPLET, STANDARD, MINIMAL | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | text | Free text | confidential | EXPERT_PROPOSAL | LOW |
| FLD-DOC-LITIGES_CONNUS | Litiges connus | boolean | true, false | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-LITIGES_DETAIL | Détail litiges | text | Free text | confidential | EXPERT_PROPOSAL | LOW |
| FLD-DOC-NATURE_ACTE | Nature de l'acte | enum | ACTE_VENTE, ACTE_LOCATION, PROMESSE_VENTE, BAIL, MANDAT, DONATION, SUCCESSION, AUTRE | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-PARTIES_CONCERNEES | Parties concernées | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-DOC-MONTANT_TRANSACTION | Montant transaction | float | Positive float | private | EXPERT_PROPOSAL | LOW |
| FLD-DOC-CONTEXTE_MEDIATION | Contexte médiation | text | Free text | confidential | HERITAGE_VALIDATED | HIGH |
| FLD-DOC-PARTIE_ADVERSE | Partie adverse | string | Free text | private | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | Contact partie adverse | string | Free text | private | EXPERT_PROPOSAL | LOW |
| FLD-DOC-NORME_CONFORMITE | Norme de conformité | enum | URBANISME, CONSTRUCTION, ENVIRONNEMENT, SECURITE, ACCESSIBILITE, HYGIENE, AUTRE | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-PERIMETRE_AUDIT | Périmètre audit | enum | COMPLET, JURIDIQUE, TECHNIQUE, ADMINISTRATIF, FINANCIER | public | HERITAGE_NORMALIZED | MEDIUM |
| FLD-DOC-DATE_ACHAT | Date d'achat | date | Valid date | private | EXPERT_PROPOSAL | LOW |
| FLD-DOC-PRIX_ACHAT | Prix d'achat | float | Positive float | private | EXPERT_PROPOSAL | LOW |

---

## Derived Fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DOC-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | documents_dispo vs documents_requis |
| FLD-DOC-DERIVED-RISQUE_JURIDIQUE | Risque juridique | litiges + titres + historique |
| FLD-DOC-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + date_souhaitee |
| FLD-DOC-DERIVED-PROFIL_DEMANDEUR | Profil demandeur | identite + historique |
| FLD-DOC-DERIVED-NOTARIAT_REQUIS | Notariat requis | type_service + objet |

---
## MATRIX 1: verification_titre_foncier

### matrix_id
MATRIX-DOC-LEGAL-001

### canonical_name
Vérification de Titre Foncier

### request_family
DOCUMENT_LEGAL_SERVICE

### transaction_type
SERVICE

### property_or_service_type
verification_titre_foncier

### requester_typology
individual_or_professional

### journey_stage
SERVICE_REQUEST

### description
Service de vérification de l'authenticité et de la validité d'un titre foncier auprès du conservatoire foncier. Inclut la recherche d'hypothèques, charges, servitudes et litiges.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous un particulier, un professionnel ou une entreprise ?" | 10 |
| FLD-DOC-TYPE_SERVICE | Type de service | always | "Quel service documentaire/juridique recherchez-vous ?" | 20 |
| FLD-DOC-OBJET | Objet demande | always | "Quel est l'objet précis de votre demande ?" | 25 |
| FLD-DOC-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se situe le bien concerné ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Quel type de bien est concerné ?" | 40 |
| FLD-DOC-DOCUMENTS_DISPO | Documents disponibles | always | "Quels documents avez-vous déjà en votre possession ?" | 45 |
| FLD-DOC-DATE_SOUHAITEE | Date souhaitée | always | "Pour quelle date souhaitez-vous ce service ?" | 50 |
| FLD-DOC-URGENCE | Urgence | always | "Quel est le niveau d'urgence ?" | 55 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-NUMERO_TITRE | Numéro titre foncier | always | "Quel est le numéro du titre foncier à vérifier ?" | 60 |
| FLD-DOC-REFERENCE_CADASTRALE | Référence cadastrale | if available | "Référence cadastrale ?" | 65 |
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | always | "Quartier où se situe le terrain ?" | 70 |
| FLD-DOC-LITIGES_CONNUS | Litiges connus | always | "Avez-vous connaissance de litiges ?" | 75 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | optional | "Connaissez-vous l'historique des propriétaires ?" | 80 |
| FLD-DOC-BUDGET | Budget | always | "Quel est votre budget pour cette vérification ?" | 85 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 100 |
| FLD-DOC-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 105 |
| FLD-DOC-CONTACT_EMAIL | Email | always | "Votre email ?" | 110 |
| FLD-DOC-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 115 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-LOCALISATION_ADRESSE | Adresse bien | if needed | "Adresse précise du bien ?" | 120 |
| FLD-DOC-DOCUMENTS_DISPO | Documents à fournir | always | "Documents à transmettre pour analyse ?" | 125 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-AUTORISATION_TIERS | Autorisation tiers | if acting for others | "Avez-vous l'autorisation du tiers concerné ?" | 130 |
| FLD-DOC-IDENTITE_TIERS | Identité tiers | when authorized | "Identité de la personne représentée ?" | 135 |
| FLD-DOC-PIECE_TIERS | Pièce tiers | when authorized | "Document d'autorisation signé ?" | 140 |
| FLD-DOC-BUDGET | Budget final | always | "Confirmation du budget ?" | 145 |
| FLD-DOC-BUDGET_DEVISE | Devise | always | "Devise ?" | 150 |
| FLD-DOC-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | informational_only | 160 |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | informational_only | 165 |
| FLD-DOC-PROFESSIONNEL_RECHERCHE | Professionnel recherché | soft_constraint | 170 |
| FLD-DOC-LITIGES_DETAIL | Détail litiges | verification_only | 175 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | informational_only | 180 |
| FLD-DOC-COMMENTAIRE | Commentaire | informational_only | 185 |
| FLD-DOC-CONTACT_DISPO | Disponibilité | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-DOC-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-DOC-COMMENTAIRE | Commentaire libre | informational_only |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents manquants | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-DOC-LITIGES_DETAIL | litiges_connus = true | verification_only |
| FLD-DOC-IDENTITE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PIECE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PARTIES_CONCERNEES | nature_acte provided | informational_only |
| FLD-DOC-MONTANT_TRANSACTION | nature_acte in (ACTE_VENTE, PROMESSE_VENTE) | informational_only |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | mediation | informational_only |
| FLD-DOC-HISTORIQUE_PROPRIETE | audit or verification | informational_only |
| FLD-DOC-DATE_ACHAT | audit_documentaire | informational_only |
| FLD-DOC-PRIX_ACHAT | audit_documentaire | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-DOC-CONTACT_TELEPHONE | Personal contact |
| FLD-DOC-CONTACT_NOM | Personal identity |
| FLD-DOC-CONTACT_EMAIL | Personal contact |
| FLD-DOC-NUMERO_TITRE | Legal property identifier |
| FLD-DOC-REFERENCE_CADASTRALE | Cadastral reference |
| FLD-DOC-DOCUMENTS_DISPO | Legal documents (originals) |
| FLD-DOC-LITIGES_CONNUS | Dispute information |
| FLD-DOC-LITIGES_DETAIL | Detailed dispute information |
| FLD-DOC-AUTORISATION_TIERS | Third-party authorization |
| FLD-DOC-IDENTITE_TIERS | Third-party identity |
| FLD-DOC-PIECE_TIERS | Third-party document |
| FLD-DOC-PARTIES_CONCERNEES | Party identities |
| FLD-DOC-MONTANT_TRANSACTION | Financial information |
| FLD-DOC-BUDGET | Financial information |
| FLD-DOC-CONTEXTE_MEDIATION | Sensitive context |
| FLD-DOC-PARTIE_ADVERSE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DOC-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | documents_dispo vs documents_requis |
| FLD-DOC-DERIVED-RISQUE_JURIDIQUE | Risque juridique | litiges + titres + historique |
| FLD-DOC-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + date |
| FLD-DOC-DERIVED-PROFIL_DEMANDEUR | Profil demandeur | identite + contexte |
| FLD-DOC-DERIVED-NOTARIAT_REQUIS | Notariat requis | type_service + objet |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un avocat ?" | Le service inclut l'orientation vers un professionnel |
| 2 | "Pourquoi avez-vous besoin de ce document ?" | Non pertinent, respect de la vie privée |
| 3 | "Le bien est-il en vente ?" | Hors scope du service documentaire |
| 4 | "Avez-vous un conflit avec votre voisin ?" | Trop intrusif |
| 5 | "Quel est votre revenu ?" | Non pertinent |
| 6 | "Avez-vous déjà fait appel à un notaire ?" | Proposé comme service |
| 7 | "Le bien est-il hypothéqué ?" | Vérifié via le service |
| 8 | "Avez-vous peur de perdre votre bien ?" | Inapproprié |

---
## MATRIX 2: recherche_documentaire

### matrix_id
MATRIX-DOC-LEGAL-002

### canonical_name
Recherche Documentaire

### request_family
DOCUMENT_LEGAL_SERVICE

### transaction_type
SERVICE

### property_or_service_type
recherche_documentaire

### requester_typology
individual_or_professional

### journey_stage
SERVICE_REQUEST

### description
Service de recherche et collecte de documents fonciers et immobiliers: actes, plans, certificats, historique de propriété.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous un particulier, un professionnel ou une entreprise ?" | 10 |
| FLD-DOC-TYPE_SERVICE | Type de service | always | "Quel service documentaire/juridique recherchez-vous ?" | 20 |
| FLD-DOC-OBJET | Objet demande | always | "Quel est l'objet précis de votre demande ?" | 25 |
| FLD-DOC-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se situe le bien concerné ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Quel type de bien est concerné ?" | 40 |
| FLD-DOC-DOCUMENTS_DISPO | Documents disponibles | always | "Quels documents avez-vous déjà en votre possession ?" | 45 |
| FLD-DOC-DATE_SOUHAITEE | Date souhaitée | always | "Pour quelle date souhaitez-vous ce service ?" | 50 |
| FLD-DOC-URGENCE | Urgence | always | "Quel est le niveau d'urgence ?" | 55 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-NUMERO_TITRE | Numéro titre | if known | "Numéro de titre foncier (si connu) ?" | 60 |
| FLD-DOC-REFERENCE_CADASTRALE | Réf. cadastrale | if known | "Référence cadastrale ?" | 65 |
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | always | "Quartier précis ?" | 70 |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents recherchés | always | "Quels documents recherchez-vous précisément ?" | 75 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique | optional | "Recherchez-vous l'historique des propriétaires ?" | 80 |
| FLD-DOC-BUDGET | Budget | always | "Budget pour cette recherche ?" | 85 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 100 |
| FLD-DOC-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 105 |
| FLD-DOC-CONTACT_EMAIL | Email | always | "Votre email ?" | 110 |
| FLD-DOC-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 115 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-LOCALISATION_ADRESSE | Adresse bien | if needed | "Adresse précise du bien ?" | 120 |
| FLD-DOC-DOCUMENTS_DISPO | Documents à fournir | always | "Documents à transmettre pour analyse ?" | 125 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-AUTORISATION_TIERS | Autorisation tiers | if acting for others | "Avez-vous l'autorisation du tiers concerné ?" | 130 |
| FLD-DOC-IDENTITE_TIERS | Identité tiers | when authorized | "Identité de la personne représentée ?" | 135 |
| FLD-DOC-PIECE_TIERS | Pièce tiers | when authorized | "Document d'autorisation signé ?" | 140 |
| FLD-DOC-BUDGET | Budget final | always | "Confirmation du budget ?" | 145 |
| FLD-DOC-BUDGET_DEVISE | Devise | always | "Devise ?" | 150 |
| FLD-DOC-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | informational_only | 160 |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | informational_only | 165 |
| FLD-DOC-PROFESSIONNEL_RECHERCHE | Professionnel recherché | soft_constraint | 170 |
| FLD-DOC-LITIGES_DETAIL | Détail litiges | verification_only | 175 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | informational_only | 180 |
| FLD-DOC-COMMENTAIRE | Commentaire | informational_only | 185 |
| FLD-DOC-CONTACT_DISPO | Disponibilité | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-DOC-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-DOC-COMMENTAIRE | Commentaire libre | informational_only |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents manquants | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-DOC-LITIGES_DETAIL | litiges_connus = true | verification_only |
| FLD-DOC-IDENTITE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PIECE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PARTIES_CONCERNEES | nature_acte provided | informational_only |
| FLD-DOC-MONTANT_TRANSACTION | nature_acte in (ACTE_VENTE, PROMESSE_VENTE) | informational_only |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | mediation | informational_only |
| FLD-DOC-HISTORIQUE_PROPRIETE | audit or verification | informational_only |
| FLD-DOC-DATE_ACHAT | audit_documentaire | informational_only |
| FLD-DOC-PRIX_ACHAT | audit_documentaire | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-DOC-CONTACT_TELEPHONE | Personal contact |
| FLD-DOC-CONTACT_NOM | Personal identity |
| FLD-DOC-CONTACT_EMAIL | Personal contact |
| FLD-DOC-NUMERO_TITRE | Legal property identifier |
| FLD-DOC-REFERENCE_CADASTRALE | Cadastral reference |
| FLD-DOC-DOCUMENTS_DISPO | Legal documents (originals) |
| FLD-DOC-LITIGES_CONNUS | Dispute information |
| FLD-DOC-LITIGES_DETAIL | Detailed dispute information |
| FLD-DOC-AUTORISATION_TIERS | Third-party authorization |
| FLD-DOC-IDENTITE_TIERS | Third-party identity |
| FLD-DOC-PIECE_TIERS | Third-party document |
| FLD-DOC-PARTIES_CONCERNEES | Party identities |
| FLD-DOC-MONTANT_TRANSACTION | Financial information |
| FLD-DOC-BUDGET | Financial information |
| FLD-DOC-CONTEXTE_MEDIATION | Sensitive context |
| FLD-DOC-PARTIE_ADVERSE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DOC-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | documents_dispo vs documents_requis |
| FLD-DOC-DERIVED-RISQUE_JURIDIQUE | Risque juridique | litiges + titres + historique |
| FLD-DOC-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + date |
| FLD-DOC-DERIVED-PROFIL_DEMANDEUR | Profil demandeur | identite + contexte |
| FLD-DOC-DERIVED-NOTARIAT_REQUIS | Notariat requis | type_service + objet |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un avocat ?" | Le service inclut l'orientation vers un professionnel |
| 2 | "Pourquoi avez-vous besoin de ce document ?" | Non pertinent, respect de la vie privée |
| 3 | "Le bien est-il en vente ?" | Hors scope du service documentaire |
| 4 | "Avez-vous un conflit avec votre voisin ?" | Trop intrusif |
| 5 | "Quel est votre revenu ?" | Non pertinent |
| 6 | "Avez-vous déjà fait appel à un notaire ?" | Proposé comme service |
| 7 | "Le bien est-il hypothéqué ?" | Vérifié via le service |
| 8 | "Avez-vous peur de perdre votre bien ?" | Inapproprié |

---
## MATRIX 3: constitution_dossier_permis

### matrix_id
MATRIX-DOC-LEGAL-003

### canonical_name
Constitution de Dossier de Permis

### request_family
DOCUMENT_LEGAL_SERVICE

### transaction_type
SERVICE

### property_or_service_type
constitution_dossier_permis

### requester_typology
individual_or_professional

### journey_stage
SERVICE_REQUEST

### description
Service d'aide à la constitution complète d'un dossier de permis de construire ou d'autorisation d'urbanisme.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous un particulier, un professionnel ou une entreprise ?" | 10 |
| FLD-DOC-TYPE_SERVICE | Type de service | always | "Quel service documentaire/juridique recherchez-vous ?" | 20 |
| FLD-DOC-OBJET | Objet demande | always | "Quel est l'objet précis de votre demande ?" | 25 |
| FLD-DOC-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se situe le bien concerné ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Quel type de bien est concerné ?" | 40 |
| FLD-DOC-DOCUMENTS_DISPO | Documents disponibles | always | "Quels documents avez-vous déjà en votre possession ?" | 45 |
| FLD-DOC-DATE_SOUHAITEE | Date souhaitée | always | "Pour quelle date souhaitez-vous ce service ?" | 50 |
| FLD-DOC-URGENCE | Urgence | always | "Quel est le niveau d'urgence ?" | 55 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Type de construction ?" | 60 |
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | always | "Quartier/zone ?" | 65 |
| FLD-DOC-DOCUMENTS_DISPO | Documents dispo | always | "Quels documents avez-vous déjà (plans, titre foncier…) ?" | 70 |
| FLD-DOC-LITIGES_CONNUS | Litiges | always | "Y a-t-il des litiges connus ?" | 75 |
| FLD-DOC-BUDGET | Budget | always | "Budget pour la constitution du dossier ?" | 80 |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | always | "Avez-vous des besoins spécifiques pour ce permis ?" | 85 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 100 |
| FLD-DOC-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 105 |
| FLD-DOC-CONTACT_EMAIL | Email | always | "Votre email ?" | 110 |
| FLD-DOC-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 115 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-LOCALISATION_ADRESSE | Adresse bien | if needed | "Adresse précise du bien ?" | 120 |
| FLD-DOC-DOCUMENTS_DISPO | Documents à fournir | always | "Documents à transmettre pour analyse ?" | 125 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-AUTORISATION_TIERS | Autorisation tiers | if acting for others | "Avez-vous l'autorisation du tiers concerné ?" | 130 |
| FLD-DOC-IDENTITE_TIERS | Identité tiers | when authorized | "Identité de la personne représentée ?" | 135 |
| FLD-DOC-PIECE_TIERS | Pièce tiers | when authorized | "Document d'autorisation signé ?" | 140 |
| FLD-DOC-BUDGET | Budget final | always | "Confirmation du budget ?" | 145 |
| FLD-DOC-BUDGET_DEVISE | Devise | always | "Devise ?" | 150 |
| FLD-DOC-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | informational_only | 160 |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | informational_only | 165 |
| FLD-DOC-PROFESSIONNEL_RECHERCHE | Professionnel recherché | soft_constraint | 170 |
| FLD-DOC-LITIGES_DETAIL | Détail litiges | verification_only | 175 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | informational_only | 180 |
| FLD-DOC-COMMENTAIRE | Commentaire | informational_only | 185 |
| FLD-DOC-CONTACT_DISPO | Disponibilité | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-DOC-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-DOC-COMMENTAIRE | Commentaire libre | informational_only |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents manquants | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-DOC-LITIGES_DETAIL | litiges_connus = true | verification_only |
| FLD-DOC-IDENTITE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PIECE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PARTIES_CONCERNEES | nature_acte provided | informational_only |
| FLD-DOC-MONTANT_TRANSACTION | nature_acte in (ACTE_VENTE, PROMESSE_VENTE) | informational_only |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | mediation | informational_only |
| FLD-DOC-HISTORIQUE_PROPRIETE | audit or verification | informational_only |
| FLD-DOC-DATE_ACHAT | audit_documentaire | informational_only |
| FLD-DOC-PRIX_ACHAT | audit_documentaire | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-DOC-CONTACT_TELEPHONE | Personal contact |
| FLD-DOC-CONTACT_NOM | Personal identity |
| FLD-DOC-CONTACT_EMAIL | Personal contact |
| FLD-DOC-NUMERO_TITRE | Legal property identifier |
| FLD-DOC-REFERENCE_CADASTRALE | Cadastral reference |
| FLD-DOC-DOCUMENTS_DISPO | Legal documents (originals) |
| FLD-DOC-LITIGES_CONNUS | Dispute information |
| FLD-DOC-LITIGES_DETAIL | Detailed dispute information |
| FLD-DOC-AUTORISATION_TIERS | Third-party authorization |
| FLD-DOC-IDENTITE_TIERS | Third-party identity |
| FLD-DOC-PIECE_TIERS | Third-party document |
| FLD-DOC-PARTIES_CONCERNEES | Party identities |
| FLD-DOC-MONTANT_TRANSACTION | Financial information |
| FLD-DOC-BUDGET | Financial information |
| FLD-DOC-CONTEXTE_MEDIATION | Sensitive context |
| FLD-DOC-PARTIE_ADVERSE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DOC-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | documents_dispo vs documents_requis |
| FLD-DOC-DERIVED-RISQUE_JURIDIQUE | Risque juridique | litiges + titres + historique |
| FLD-DOC-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + date |
| FLD-DOC-DERIVED-PROFIL_DEMANDEUR | Profil demandeur | identite + contexte |
| FLD-DOC-DERIVED-NOTARIAT_REQUIS | Notariat requis | type_service + objet |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un avocat ?" | Le service inclut l'orientation vers un professionnel |
| 2 | "Pourquoi avez-vous besoin de ce document ?" | Non pertinent, respect de la vie privée |
| 3 | "Le bien est-il en vente ?" | Hors scope du service documentaire |
| 4 | "Avez-vous un conflit avec votre voisin ?" | Trop intrusif |
| 5 | "Quel est votre revenu ?" | Non pertinent |
| 6 | "Avez-vous déjà fait appel à un notaire ?" | Proposé comme service |
| 7 | "Le bien est-il hypothéqué ?" | Vérifié via le service |
| 8 | "Avez-vous peur de perdre votre bien ?" | Inapproprié |

---
## MATRIX 4: aide_redaction_acte

### matrix_id
MATRIX-DOC-LEGAL-004

### canonical_name
Aide à la Rédaction d'Acte

### request_family
DOCUMENT_LEGAL_SERVICE

### transaction_type
SERVICE

### property_or_service_type
aide_redaction_acte

### requester_typology
individual_or_professional

### journey_stage
SERVICE_REQUEST

### description
Service d'assistance à la rédaction d'actes immobiliers: promesse de vente, acte de vente, bail, mandat, avenant.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous un particulier, un professionnel ou une entreprise ?" | 10 |
| FLD-DOC-TYPE_SERVICE | Type de service | always | "Quel service documentaire/juridique recherchez-vous ?" | 20 |
| FLD-DOC-OBJET | Objet demande | always | "Quel est l'objet précis de votre demande ?" | 25 |
| FLD-DOC-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se situe le bien concerné ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Quel type de bien est concerné ?" | 40 |
| FLD-DOC-DOCUMENTS_DISPO | Documents disponibles | always | "Quels documents avez-vous déjà en votre possession ?" | 45 |
| FLD-DOC-DATE_SOUHAITEE | Date souhaitée | always | "Pour quelle date souhaitez-vous ce service ?" | 50 |
| FLD-DOC-URGENCE | Urgence | always | "Quel est le niveau d'urgence ?" | 55 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-NATURE_ACTE | Nature de l'acte | always | "Quel type d'acte souhaitez-vous rédiger ?" | 60 |
| FLD-DOC-PARTIES_CONCERNEES | Parties concernées | always | "Qui sont les parties concernées ?" | 65 |
| FLD-DOC-MONTANT_TRANSACTION | Montant transaction | if sale/rent | "Montant de la transaction ?" | 70 |
| FLD-DOC-DOCUMENTS_DISPO | Documents dispo | always | "Quels documents de base avez-vous ?" | 75 |
| FLD-DOC-BUDGET | Budget | always | "Budget pour la rédaction ?" | 80 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 100 |
| FLD-DOC-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 105 |
| FLD-DOC-CONTACT_EMAIL | Email | always | "Votre email ?" | 110 |
| FLD-DOC-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 115 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-LOCALISATION_ADRESSE | Adresse bien | if needed | "Adresse précise du bien ?" | 120 |
| FLD-DOC-DOCUMENTS_DISPO | Documents à fournir | always | "Documents à transmettre pour analyse ?" | 125 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-AUTORISATION_TIERS | Autorisation tiers | if acting for others | "Avez-vous l'autorisation du tiers concerné ?" | 130 |
| FLD-DOC-IDENTITE_TIERS | Identité tiers | when authorized | "Identité de la personne représentée ?" | 135 |
| FLD-DOC-PIECE_TIERS | Pièce tiers | when authorized | "Document d'autorisation signé ?" | 140 |
| FLD-DOC-BUDGET | Budget final | always | "Confirmation du budget ?" | 145 |
| FLD-DOC-BUDGET_DEVISE | Devise | always | "Devise ?" | 150 |
| FLD-DOC-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | informational_only | 160 |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | informational_only | 165 |
| FLD-DOC-PROFESSIONNEL_RECHERCHE | Professionnel recherché | soft_constraint | 170 |
| FLD-DOC-LITIGES_DETAIL | Détail litiges | verification_only | 175 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | informational_only | 180 |
| FLD-DOC-COMMENTAIRE | Commentaire | informational_only | 185 |
| FLD-DOC-CONTACT_DISPO | Disponibilité | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-DOC-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-DOC-COMMENTAIRE | Commentaire libre | informational_only |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents manquants | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-DOC-LITIGES_DETAIL | litiges_connus = true | verification_only |
| FLD-DOC-IDENTITE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PIECE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PARTIES_CONCERNEES | nature_acte provided | informational_only |
| FLD-DOC-MONTANT_TRANSACTION | nature_acte in (ACTE_VENTE, PROMESSE_VENTE) | informational_only |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | mediation | informational_only |
| FLD-DOC-HISTORIQUE_PROPRIETE | audit or verification | informational_only |
| FLD-DOC-DATE_ACHAT | audit_documentaire | informational_only |
| FLD-DOC-PRIX_ACHAT | audit_documentaire | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-DOC-CONTACT_TELEPHONE | Personal contact |
| FLD-DOC-CONTACT_NOM | Personal identity |
| FLD-DOC-CONTACT_EMAIL | Personal contact |
| FLD-DOC-NUMERO_TITRE | Legal property identifier |
| FLD-DOC-REFERENCE_CADASTRALE | Cadastral reference |
| FLD-DOC-DOCUMENTS_DISPO | Legal documents (originals) |
| FLD-DOC-LITIGES_CONNUS | Dispute information |
| FLD-DOC-LITIGES_DETAIL | Detailed dispute information |
| FLD-DOC-AUTORISATION_TIERS | Third-party authorization |
| FLD-DOC-IDENTITE_TIERS | Third-party identity |
| FLD-DOC-PIECE_TIERS | Third-party document |
| FLD-DOC-PARTIES_CONCERNEES | Party identities |
| FLD-DOC-MONTANT_TRANSACTION | Financial information |
| FLD-DOC-BUDGET | Financial information |
| FLD-DOC-CONTEXTE_MEDIATION | Sensitive context |
| FLD-DOC-PARTIE_ADVERSE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DOC-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | documents_dispo vs documents_requis |
| FLD-DOC-DERIVED-RISQUE_JURIDIQUE | Risque juridique | litiges + titres + historique |
| FLD-DOC-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + date |
| FLD-DOC-DERIVED-PROFIL_DEMANDEUR | Profil demandeur | identite + contexte |
| FLD-DOC-DERIVED-NOTARIAT_REQUIS | Notariat requis | type_service + objet |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un avocat ?" | Le service inclut l'orientation vers un professionnel |
| 2 | "Pourquoi avez-vous besoin de ce document ?" | Non pertinent, respect de la vie privée |
| 3 | "Le bien est-il en vente ?" | Hors scope du service documentaire |
| 4 | "Avez-vous un conflit avec votre voisin ?" | Trop intrusif |
| 5 | "Quel est votre revenu ?" | Non pertinent |
| 6 | "Avez-vous déjà fait appel à un notaire ?" | Proposé comme service |
| 7 | "Le bien est-il hypothéqué ?" | Vérifié via le service |
| 8 | "Avez-vous peur de perdre votre bien ?" | Inapproprié |

---
## MATRIX 5: mediation_immobiliere

### matrix_id
MATRIX-DOC-LEGAL-005

### canonical_name
Médiation Immobilière

### request_family
DOCUMENT_LEGAL_SERVICE

### transaction_type
SERVICE

### property_or_service_type
mediation_immobiliere

### requester_typology
individual_or_professional

### journey_stage
SERVICE_REQUEST

### description
Service de médiation pour résoudre les conflits immobiliers entre parties: bailleur/locataire, vendeur/acheteur, copropriétaires.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous un particulier, un professionnel ou une entreprise ?" | 10 |
| FLD-DOC-TYPE_SERVICE | Type de service | always | "Quel service documentaire/juridique recherchez-vous ?" | 20 |
| FLD-DOC-OBJET | Objet demande | always | "Quel est l'objet précis de votre demande ?" | 25 |
| FLD-DOC-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se situe le bien concerné ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Quel type de bien est concerné ?" | 40 |
| FLD-DOC-DOCUMENTS_DISPO | Documents disponibles | always | "Quels documents avez-vous déjà en votre possession ?" | 45 |
| FLD-DOC-DATE_SOUHAITEE | Date souhaitée | always | "Pour quelle date souhaitez-vous ce service ?" | 50 |
| FLD-DOC-URGENCE | Urgence | always | "Quel est le niveau d'urgence ?" | 55 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-CONTEXTE_MEDIATION | Contexte médiation | always | "Quel est l'objet du conflit ?" | 60 |
| FLD-DOC-PARTIE_ADVERSE | Partie adverse | always | "Qui est l'autre partie ?" | 65 |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | Contact adverse | always | "Contact de l'autre partie ?" | 70 |
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Quel bien est concerné par le litige ?" | 75 |
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | always | "Quartier du bien ?" | 80 |
| FLD-DOC-DOCUMENTS_DISPO | Documents | always | "Quels documents relatifs au litige ?" | 85 |
| FLD-DOC-URGENCE | Urgence | always | "Urgence de la médiation ?" | 90 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 100 |
| FLD-DOC-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 105 |
| FLD-DOC-CONTACT_EMAIL | Email | always | "Votre email ?" | 110 |
| FLD-DOC-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 115 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-LOCALISATION_ADRESSE | Adresse bien | if needed | "Adresse précise du bien ?" | 120 |
| FLD-DOC-DOCUMENTS_DISPO | Documents à fournir | always | "Documents à transmettre pour analyse ?" | 125 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-AUTORISATION_TIERS | Autorisation tiers | if acting for others | "Avez-vous l'autorisation du tiers concerné ?" | 130 |
| FLD-DOC-IDENTITE_TIERS | Identité tiers | when authorized | "Identité de la personne représentée ?" | 135 |
| FLD-DOC-PIECE_TIERS | Pièce tiers | when authorized | "Document d'autorisation signé ?" | 140 |
| FLD-DOC-BUDGET | Budget final | always | "Confirmation du budget ?" | 145 |
| FLD-DOC-BUDGET_DEVISE | Devise | always | "Devise ?" | 150 |
| FLD-DOC-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | informational_only | 160 |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | informational_only | 165 |
| FLD-DOC-PROFESSIONNEL_RECHERCHE | Professionnel recherché | soft_constraint | 170 |
| FLD-DOC-LITIGES_DETAIL | Détail litiges | verification_only | 175 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | informational_only | 180 |
| FLD-DOC-COMMENTAIRE | Commentaire | informational_only | 185 |
| FLD-DOC-CONTACT_DISPO | Disponibilité | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-DOC-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-DOC-COMMENTAIRE | Commentaire libre | informational_only |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents manquants | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-DOC-LITIGES_DETAIL | litiges_connus = true | verification_only |
| FLD-DOC-IDENTITE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PIECE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PARTIES_CONCERNEES | nature_acte provided | informational_only |
| FLD-DOC-MONTANT_TRANSACTION | nature_acte in (ACTE_VENTE, PROMESSE_VENTE) | informational_only |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | mediation | informational_only |
| FLD-DOC-HISTORIQUE_PROPRIETE | audit or verification | informational_only |
| FLD-DOC-DATE_ACHAT | audit_documentaire | informational_only |
| FLD-DOC-PRIX_ACHAT | audit_documentaire | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-DOC-CONTACT_TELEPHONE | Personal contact |
| FLD-DOC-CONTACT_NOM | Personal identity |
| FLD-DOC-CONTACT_EMAIL | Personal contact |
| FLD-DOC-NUMERO_TITRE | Legal property identifier |
| FLD-DOC-REFERENCE_CADASTRALE | Cadastral reference |
| FLD-DOC-DOCUMENTS_DISPO | Legal documents (originals) |
| FLD-DOC-LITIGES_CONNUS | Dispute information |
| FLD-DOC-LITIGES_DETAIL | Detailed dispute information |
| FLD-DOC-AUTORISATION_TIERS | Third-party authorization |
| FLD-DOC-IDENTITE_TIERS | Third-party identity |
| FLD-DOC-PIECE_TIERS | Third-party document |
| FLD-DOC-PARTIES_CONCERNEES | Party identities |
| FLD-DOC-MONTANT_TRANSACTION | Financial information |
| FLD-DOC-BUDGET | Financial information |
| FLD-DOC-CONTEXTE_MEDIATION | Sensitive context |
| FLD-DOC-PARTIE_ADVERSE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DOC-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | documents_dispo vs documents_requis |
| FLD-DOC-DERIVED-RISQUE_JURIDIQUE | Risque juridique | litiges + titres + historique |
| FLD-DOC-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + date |
| FLD-DOC-DERIVED-PROFIL_DEMANDEUR | Profil demandeur | identite + contexte |
| FLD-DOC-DERIVED-NOTARIAT_REQUIS | Notariat requis | type_service + objet |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un avocat ?" | Le service inclut l'orientation vers un professionnel |
| 2 | "Pourquoi avez-vous besoin de ce document ?" | Non pertinent, respect de la vie privée |
| 3 | "Le bien est-il en vente ?" | Hors scope du service documentaire |
| 4 | "Avez-vous un conflit avec votre voisin ?" | Trop intrusif |
| 5 | "Quel est votre revenu ?" | Non pertinent |
| 6 | "Avez-vous déjà fait appel à un notaire ?" | Proposé comme service |
| 7 | "Le bien est-il hypothéqué ?" | Vérifié via le service |
| 8 | "Avez-vous peur de perdre votre bien ?" | Inapproprié |

---
## MATRIX 6: conseil_juridique_immobilier

### matrix_id
MATRIX-DOC-LEGAL-006

### canonical_name
Conseil Juridique Immobilier

### request_family
DOCUMENT_LEGAL_SERVICE

### transaction_type
SERVICE

### property_or_service_type
conseil_juridique_immobilier

### requester_typology
individual_or_professional

### journey_stage
SERVICE_REQUEST

### description
Service de conseil juridique spécialisé en droit immobilier camerounais: questions foncières, locatives, copropriété, fiscales.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous un particulier, un professionnel ou une entreprise ?" | 10 |
| FLD-DOC-TYPE_SERVICE | Type de service | always | "Quel service documentaire/juridique recherchez-vous ?" | 20 |
| FLD-DOC-OBJET | Objet demande | always | "Quel est l'objet précis de votre demande ?" | 25 |
| FLD-DOC-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se situe le bien concerné ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Quel type de bien est concerné ?" | 40 |
| FLD-DOC-DOCUMENTS_DISPO | Documents disponibles | always | "Quels documents avez-vous déjà en votre possession ?" | 45 |
| FLD-DOC-DATE_SOUHAITEE | Date souhaitée | always | "Pour quelle date souhaitez-vous ce service ?" | 50 |
| FLD-DOC-URGENCE | Urgence | always | "Quel est le niveau d'urgence ?" | 55 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-OBJET | Objet conseil | always | "Quel est le domaine juridique concerné ?" | 60 |
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Type de bien concerné ?" | 65 |
| FLD-DOC-LOCALISATION_VILLE | Ville | always | "Ville du bien ?" | 70 |
| FLD-DOC-LITIGES_CONNUS | Litiges | always | "Y a-t-il un litige en cours ?" | 75 |
| FLD-DOC-DOCUMENTS_DISPO | Documents | always | "Documents disponibles pour analyse ?" | 80 |
| FLD-DOC-URGENCE | Urgence | always | "Niveau d'urgence ?" | 85 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 100 |
| FLD-DOC-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 105 |
| FLD-DOC-CONTACT_EMAIL | Email | always | "Votre email ?" | 110 |
| FLD-DOC-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 115 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-LOCALISATION_ADRESSE | Adresse bien | if needed | "Adresse précise du bien ?" | 120 |
| FLD-DOC-DOCUMENTS_DISPO | Documents à fournir | always | "Documents à transmettre pour analyse ?" | 125 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-AUTORISATION_TIERS | Autorisation tiers | if acting for others | "Avez-vous l'autorisation du tiers concerné ?" | 130 |
| FLD-DOC-IDENTITE_TIERS | Identité tiers | when authorized | "Identité de la personne représentée ?" | 135 |
| FLD-DOC-PIECE_TIERS | Pièce tiers | when authorized | "Document d'autorisation signé ?" | 140 |
| FLD-DOC-BUDGET | Budget final | always | "Confirmation du budget ?" | 145 |
| FLD-DOC-BUDGET_DEVISE | Devise | always | "Devise ?" | 150 |
| FLD-DOC-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | informational_only | 160 |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | informational_only | 165 |
| FLD-DOC-PROFESSIONNEL_RECHERCHE | Professionnel recherché | soft_constraint | 170 |
| FLD-DOC-LITIGES_DETAIL | Détail litiges | verification_only | 175 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | informational_only | 180 |
| FLD-DOC-COMMENTAIRE | Commentaire | informational_only | 185 |
| FLD-DOC-CONTACT_DISPO | Disponibilité | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-DOC-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-DOC-COMMENTAIRE | Commentaire libre | informational_only |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents manquants | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-DOC-LITIGES_DETAIL | litiges_connus = true | verification_only |
| FLD-DOC-IDENTITE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PIECE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PARTIES_CONCERNEES | nature_acte provided | informational_only |
| FLD-DOC-MONTANT_TRANSACTION | nature_acte in (ACTE_VENTE, PROMESSE_VENTE) | informational_only |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | mediation | informational_only |
| FLD-DOC-HISTORIQUE_PROPRIETE | audit or verification | informational_only |
| FLD-DOC-DATE_ACHAT | audit_documentaire | informational_only |
| FLD-DOC-PRIX_ACHAT | audit_documentaire | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-DOC-CONTACT_TELEPHONE | Personal contact |
| FLD-DOC-CONTACT_NOM | Personal identity |
| FLD-DOC-CONTACT_EMAIL | Personal contact |
| FLD-DOC-NUMERO_TITRE | Legal property identifier |
| FLD-DOC-REFERENCE_CADASTRALE | Cadastral reference |
| FLD-DOC-DOCUMENTS_DISPO | Legal documents (originals) |
| FLD-DOC-LITIGES_CONNUS | Dispute information |
| FLD-DOC-LITIGES_DETAIL | Detailed dispute information |
| FLD-DOC-AUTORISATION_TIERS | Third-party authorization |
| FLD-DOC-IDENTITE_TIERS | Third-party identity |
| FLD-DOC-PIECE_TIERS | Third-party document |
| FLD-DOC-PARTIES_CONCERNEES | Party identities |
| FLD-DOC-MONTANT_TRANSACTION | Financial information |
| FLD-DOC-BUDGET | Financial information |
| FLD-DOC-CONTEXTE_MEDIATION | Sensitive context |
| FLD-DOC-PARTIE_ADVERSE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DOC-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | documents_dispo vs documents_requis |
| FLD-DOC-DERIVED-RISQUE_JURIDIQUE | Risque juridique | litiges + titres + historique |
| FLD-DOC-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + date |
| FLD-DOC-DERIVED-PROFIL_DEMANDEUR | Profil demandeur | identite + contexte |
| FLD-DOC-DERIVED-NOTARIAT_REQUIS | Notariat requis | type_service + objet |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un avocat ?" | Le service inclut l'orientation vers un professionnel |
| 2 | "Pourquoi avez-vous besoin de ce document ?" | Non pertinent, respect de la vie privée |
| 3 | "Le bien est-il en vente ?" | Hors scope du service documentaire |
| 4 | "Avez-vous un conflit avec votre voisin ?" | Trop intrusif |
| 5 | "Quel est votre revenu ?" | Non pertinent |
| 6 | "Avez-vous déjà fait appel à un notaire ?" | Proposé comme service |
| 7 | "Le bien est-il hypothéqué ?" | Vérifié via le service |
| 8 | "Avez-vous peur de perdre votre bien ?" | Inapproprié |

---
## MATRIX 7: verification_conformite

### matrix_id
MATRIX-DOC-LEGAL-007

### canonical_name
Vérification de Conformité

### request_family
DOCUMENT_LEGAL_SERVICE

### transaction_type
SERVICE

### property_or_service_type
verification_conformite

### requester_typology
individual_or_professional

### journey_stage
SERVICE_REQUEST

### description
Service de vérification de la conformité d'un bien immobilier aux normes en vigueur: urbanisme, construction, sécurité, environnement.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous un particulier, un professionnel ou une entreprise ?" | 10 |
| FLD-DOC-TYPE_SERVICE | Type de service | always | "Quel service documentaire/juridique recherchez-vous ?" | 20 |
| FLD-DOC-OBJET | Objet demande | always | "Quel est l'objet précis de votre demande ?" | 25 |
| FLD-DOC-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se situe le bien concerné ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Quel type de bien est concerné ?" | 40 |
| FLD-DOC-DOCUMENTS_DISPO | Documents disponibles | always | "Quels documents avez-vous déjà en votre possession ?" | 45 |
| FLD-DOC-DATE_SOUHAITEE | Date souhaitée | always | "Pour quelle date souhaitez-vous ce service ?" | 50 |
| FLD-DOC-URGENCE | Urgence | always | "Quel est le niveau d'urgence ?" | 55 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-NORME_CONFORMITE | Norme de conformité | always | "Quel type de conformité recherchez-vous ?" | 60 |
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Type de bien ?" | 65 |
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | always | "Quartier ?" | 70 |
| FLD-DOC-LOCALISATION_ADRESSE | Adresse | always | "Adresse précise du bien ?" | 75 |
| FLD-DOC-DOCUMENTS_DISPO | Documents | always | "Documents disponibles ?" | 80 |
| FLD-DOC-BUDGET | Budget | always | "Budget pour la vérification ?" | 85 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 100 |
| FLD-DOC-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 105 |
| FLD-DOC-CONTACT_EMAIL | Email | always | "Votre email ?" | 110 |
| FLD-DOC-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 115 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-LOCALISATION_ADRESSE | Adresse bien | if needed | "Adresse précise du bien ?" | 120 |
| FLD-DOC-DOCUMENTS_DISPO | Documents à fournir | always | "Documents à transmettre pour analyse ?" | 125 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-AUTORISATION_TIERS | Autorisation tiers | if acting for others | "Avez-vous l'autorisation du tiers concerné ?" | 130 |
| FLD-DOC-IDENTITE_TIERS | Identité tiers | when authorized | "Identité de la personne représentée ?" | 135 |
| FLD-DOC-PIECE_TIERS | Pièce tiers | when authorized | "Document d'autorisation signé ?" | 140 |
| FLD-DOC-BUDGET | Budget final | always | "Confirmation du budget ?" | 145 |
| FLD-DOC-BUDGET_DEVISE | Devise | always | "Devise ?" | 150 |
| FLD-DOC-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | informational_only | 160 |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | informational_only | 165 |
| FLD-DOC-PROFESSIONNEL_RECHERCHE | Professionnel recherché | soft_constraint | 170 |
| FLD-DOC-LITIGES_DETAIL | Détail litiges | verification_only | 175 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | informational_only | 180 |
| FLD-DOC-COMMENTAIRE | Commentaire | informational_only | 185 |
| FLD-DOC-CONTACT_DISPO | Disponibilité | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-DOC-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-DOC-COMMENTAIRE | Commentaire libre | informational_only |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents manquants | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-DOC-LITIGES_DETAIL | litiges_connus = true | verification_only |
| FLD-DOC-IDENTITE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PIECE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PARTIES_CONCERNEES | nature_acte provided | informational_only |
| FLD-DOC-MONTANT_TRANSACTION | nature_acte in (ACTE_VENTE, PROMESSE_VENTE) | informational_only |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | mediation | informational_only |
| FLD-DOC-HISTORIQUE_PROPRIETE | audit or verification | informational_only |
| FLD-DOC-DATE_ACHAT | audit_documentaire | informational_only |
| FLD-DOC-PRIX_ACHAT | audit_documentaire | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-DOC-CONTACT_TELEPHONE | Personal contact |
| FLD-DOC-CONTACT_NOM | Personal identity |
| FLD-DOC-CONTACT_EMAIL | Personal contact |
| FLD-DOC-NUMERO_TITRE | Legal property identifier |
| FLD-DOC-REFERENCE_CADASTRALE | Cadastral reference |
| FLD-DOC-DOCUMENTS_DISPO | Legal documents (originals) |
| FLD-DOC-LITIGES_CONNUS | Dispute information |
| FLD-DOC-LITIGES_DETAIL | Detailed dispute information |
| FLD-DOC-AUTORISATION_TIERS | Third-party authorization |
| FLD-DOC-IDENTITE_TIERS | Third-party identity |
| FLD-DOC-PIECE_TIERS | Third-party document |
| FLD-DOC-PARTIES_CONCERNEES | Party identities |
| FLD-DOC-MONTANT_TRANSACTION | Financial information |
| FLD-DOC-BUDGET | Financial information |
| FLD-DOC-CONTEXTE_MEDIATION | Sensitive context |
| FLD-DOC-PARTIE_ADVERSE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DOC-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | documents_dispo vs documents_requis |
| FLD-DOC-DERIVED-RISQUE_JURIDIQUE | Risque juridique | litiges + titres + historique |
| FLD-DOC-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + date |
| FLD-DOC-DERIVED-PROFIL_DEMANDEUR | Profil demandeur | identite + contexte |
| FLD-DOC-DERIVED-NOTARIAT_REQUIS | Notariat requis | type_service + objet |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un avocat ?" | Le service inclut l'orientation vers un professionnel |
| 2 | "Pourquoi avez-vous besoin de ce document ?" | Non pertinent, respect de la vie privée |
| 3 | "Le bien est-il en vente ?" | Hors scope du service documentaire |
| 4 | "Avez-vous un conflit avec votre voisin ?" | Trop intrusif |
| 5 | "Quel est votre revenu ?" | Non pertinent |
| 6 | "Avez-vous déjà fait appel à un notaire ?" | Proposé comme service |
| 7 | "Le bien est-il hypothéqué ?" | Vérifié via le service |
| 8 | "Avez-vous peur de perdre votre bien ?" | Inapproprié |

---
## MATRIX 8: audit_documentaire

### matrix_id
MATRIX-DOC-LEGAL-008

### canonical_name
Audit Documentaire

### request_family
DOCUMENT_LEGAL_SERVICE

### transaction_type
SERVICE

### property_or_service_type
audit_documentaire

### requester_typology
individual_or_professional

### journey_stage
SERVICE_REQUEST

### description
Service d'audit complet de la documentation d'un bien immobilier: titres, actes, plans, autorisations, historique.

### minimum_intake_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-IDENTITE_DEMANDEUR | Identité demandeur | always | "Êtes-vous un particulier, un professionnel ou une entreprise ?" | 10 |
| FLD-DOC-TYPE_SERVICE | Type de service | always | "Quel service documentaire/juridique recherchez-vous ?" | 20 |
| FLD-DOC-OBJET | Objet demande | always | "Quel est l'objet précis de votre demande ?" | 25 |
| FLD-DOC-LOCALISATION_VILLE | Ville | always | "Dans quelle ville se situe le bien concerné ?" | 30 |

### minimum_search_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Quel type de bien est concerné ?" | 40 |
| FLD-DOC-DOCUMENTS_DISPO | Documents disponibles | always | "Quels documents avez-vous déjà en votre possession ?" | 45 |
| FLD-DOC-DATE_SOUHAITEE | Date souhaitée | always | "Pour quelle date souhaitez-vous ce service ?" | 50 |
| FLD-DOC-URGENCE | Urgence | always | "Quel est le niveau d'urgence ?" | 55 |

### minimum_matching_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-PERIMETRE_AUDIT | Périmètre audit | always | "Quel périmètre d'audit souhaitez-vous ?" | 60 |
| FLD-DOC-TYPE_BIEN | Type de bien | always | "Type de bien ?" | 65 |
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | always | "Quartier ?" | 70 |
| FLD-DOC-DOCUMENTS_DISPO | Documents | always | "Quels documents avez-vous ?" | 75 |
| FLD-DOC-DATE_ACHAT | Date achat | optional | "Quand le bien a-t-il été acquis ?" | 80 |
| FLD-DOC-PRIX_ACHAT | Prix achat | optional | "Prix d'acquisition ?" | 85 |
| FLD-DOC-BUDGET | Budget | always | "Budget pour l'audit ?" | 90 |

### minimum_introduction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-CONTACT_NOM | Nom | always | "Quel est votre nom ?" | 100 |
| FLD-DOC-CONTACT_TELEPHONE | Téléphone | always | "Votre téléphone ?" | 105 |
| FLD-DOC-CONTACT_EMAIL | Email | always | "Votre email ?" | 110 |
| FLD-DOC-CONTACT_CANAL | Canal préféré | always | "Canal de communication préféré ?" | 115 |

### minimum_visit_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-LOCALISATION_ADRESSE | Adresse bien | if needed | "Adresse précise du bien ?" | 120 |
| FLD-DOC-DOCUMENTS_DISPO | Documents à fournir | always | "Documents à transmettre pour analyse ?" | 125 |

### minimum_transaction_fields

| FIELD-ID | label | mandatory_when | question_template | question_priority |
|----------|-------|----------------|-------------------|-------------------|
| FLD-DOC-AUTORISATION_TIERS | Autorisation tiers | if acting for others | "Avez-vous l'autorisation du tiers concerné ?" | 130 |
| FLD-DOC-IDENTITE_TIERS | Identité tiers | when authorized | "Identité de la personne représentée ?" | 135 |
| FLD-DOC-PIECE_TIERS | Pièce tiers | when authorized | "Document d'autorisation signé ?" | 140 |
| FLD-DOC-BUDGET | Budget final | always | "Confirmation du budget ?" | 145 |
| FLD-DOC-BUDGET_DEVISE | Devise | always | "Devise ?" | 150 |
| FLD-DOC-NIVEAU_VERIFICATION | Niveau vérification | always | "Niveau de vérification ?" | 155 |

### recommended_fields

| FIELD-ID | label | matching_role | question_priority |
|----------|-------|---------------|-------------------|
| FLD-DOC-LOCALISATION_QUARTIER | Quartier | informational_only | 160 |
| FLD-DOC-BESOIN_SPECIFIQUE | Besoin spécifique | informational_only | 165 |
| FLD-DOC-PROFESSIONNEL_RECHERCHE | Professionnel recherché | soft_constraint | 170 |
| FLD-DOC-LITIGES_DETAIL | Détail litiges | verification_only | 175 |
| FLD-DOC-HISTORIQUE_PROPRIETE | Historique propriété | informational_only | 180 |
| FLD-DOC-COMMENTAIRE | Commentaire | informational_only | 185 |
| FLD-DOC-CONTACT_DISPO | Disponibilité | informational_only | 190 |

### optional_fields

| FIELD-ID | label | matching_role |
|----------|-------|---------------|
| FLD-DOC-CONTACT_DISPO | Disponibilité contact | informational_only |
| FLD-DOC-COMMENTAIRE | Commentaire libre | informational_only |
| FLD-DOC-DOCUMENTS_MANQUANTS | Documents manquants | informational_only |

### conditional_fields

| FIELD-ID | condition | matching_role |
|----------|-----------|---------------|
| FLD-DOC-LITIGES_DETAIL | litiges_connus = true | verification_only |
| FLD-DOC-IDENTITE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PIECE_TIERS | autorisation_tiers = true | verification_only |
| FLD-DOC-PARTIES_CONCERNEES | nature_acte provided | informational_only |
| FLD-DOC-MONTANT_TRANSACTION | nature_acte in (ACTE_VENTE, PROMESSE_VENTE) | informational_only |
| FLD-DOC-CONTACT_PARTIE_ADVERSE | mediation | informational_only |
| FLD-DOC-HISTORIQUE_PROPRIETE | audit or verification | informational_only |
| FLD-DOC-DATE_ACHAT | audit_documentaire | informational_only |
| FLD-DOC-PRIX_ACHAT | audit_documentaire | informational_only |

### sensitive_fields

| FIELD-ID | reason |
|----------|--------|
| FLD-DOC-CONTACT_TELEPHONE | Personal contact |
| FLD-DOC-CONTACT_NOM | Personal identity |
| FLD-DOC-CONTACT_EMAIL | Personal contact |
| FLD-DOC-NUMERO_TITRE | Legal property identifier |
| FLD-DOC-REFERENCE_CADASTRALE | Cadastral reference |
| FLD-DOC-DOCUMENTS_DISPO | Legal documents (originals) |
| FLD-DOC-LITIGES_CONNUS | Dispute information |
| FLD-DOC-LITIGES_DETAIL | Detailed dispute information |
| FLD-DOC-AUTORISATION_TIERS | Third-party authorization |
| FLD-DOC-IDENTITE_TIERS | Third-party identity |
| FLD-DOC-PIECE_TIERS | Third-party document |
| FLD-DOC-PARTIES_CONCERNEES | Party identities |
| FLD-DOC-MONTANT_TRANSACTION | Financial information |
| FLD-DOC-BUDGET | Financial information |
| FLD-DOC-CONTEXTE_MEDIATION | Sensitive context |
| FLD-DOC-PARTIE_ADVERSE | Third-party identity |

### derived_fields

| FIELD-ID | label | derived_from |
|----------|-------|-------------|
| FLD-DOC-DERIVED-COMPLETUDE_DOSSIER | Complétude dossier | documents_dispo vs documents_requis |
| FLD-DOC-DERIVED-RISQUE_JURIDIQUE | Risque juridique | litiges + titres + historique |
| FLD-DOC-DERIVED-URGENCE_REELLE | Urgence réelle | urgence + date |
| FLD-DOC-DERIVED-PROFIL_DEMANDEUR | Profil demandeur | identite + contexte |
| FLD-DOC-DERIVED-NOTARIAT_REQUIS | Notariat requis | type_service + objet |

### forbidden_questions

| # | Question interdite | Raison |
|---|-------------------|--------|
| 1 | "Avez-vous un avocat ?" | Le service inclut l'orientation vers un professionnel |
| 2 | "Pourquoi avez-vous besoin de ce document ?" | Non pertinent, respect de la vie privée |
| 3 | "Le bien est-il en vente ?" | Hors scope du service documentaire |
| 4 | "Avez-vous un conflit avec votre voisin ?" | Trop intrusif |
| 5 | "Quel est votre revenu ?" | Non pertinent |
| 6 | "Avez-vous déjà fait appel à un notaire ?" | Proposé comme service |
| 7 | "Le bien est-il hypothéqué ?" | Vérifié via le service |
| 8 | "Avez-vous peur de perdre votre bien ?" | Inapproprié |

---

# End of Document — Document and Legal Service Matrices
