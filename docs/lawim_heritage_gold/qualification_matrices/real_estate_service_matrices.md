# Real Estate Service Matrices

> **Service Domain:** REAL_ESTATE_SERVICES
> **Version:** 1.0.0

---

## Table of Contents

1. [estimation_immobiliere](#1-estimation_immobiliere)
2. [expertise](#2-expertise)
3. [verification_documentaire](#3-verification_documentaire)
4. [visite_property](#4-visite_property)
5. [contre_visite](#5-contre_visite)
6. [gestion_locative](#6-gestion_locative)
7. [mise_en_location](#7-mise_en_location)
8. [mise_en_vente](#8-mise_en_vente)
9. [publication_service](#9-publication_service)
10. [photographie](#10-photographie)
11. [video_service](#11-video_service)
12. [drone_service](#12-drone_service)
13. [home_staging](#13-home_staging)
14. [renovation_service](#14-renovation_service)
15. [construction_service](#15-construction_service)
16. [entretien](#16-entretien)
17. [nettoyage](#17-nettoyage)
18. [securisation](#18-securisation)
19. [demenagement](#19-demenagement)
20. [assurance_service](#20-assurance_service)
21. [conseil_juridique](#21-conseil_juridique)
22. [conseil_fiscal](#22-conseil_fiscal)
23. [gestion_copropriete](#23-gestion_copropriete)
24. [recouvrement_locatif](#24-recouvrement_locatif)

---

## Structure

Each service matrix defines the minimum fields required at four stages:

1. **minimum_service_ready_fields** - Fields required before the service can be offered/listed
2. **minimum_provider_matching_ready_fields** - Fields required to match a provider to the service request
3. **minimum_quote_ready_fields** - Fields required to generate a quote/proposal
4. **minimum_execution_ready_fields** - Fields required to begin execution of the service

All fields are described in YAML format with metadata including type, required status, allowed values, and descriptions.

---

## 1. estimation_immobiliere
```yaml
service_id: SVC-ESTI-001
canonical_name: estimation_immobiliere
display_name: "Property Valuation"

description: >
  Service d'estimation de la valeur venale ou locative d'un bien immobilier base sur des methodes comparatives et des analyses de marche.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: surface_habitable
    required: true
    type: float
    unit: m2
  - field_name: terrain_surface
    required: false
    type: float
    unit: m2
  - field_name: description_bien
    required: true
    type: text
  - field_name: type_estimation
    required: true
    values:
      - estimation_vente
      - estimation_locative
      - estimation_assurance
      - estimation_pret
      - estimation_patrimoniale
  - field_name: urgence
    required: true
    values:
      - standard_72h
      - urgent_24h
      - express_4h
  - field_name: date_souhaitee
    required: true
    type: date
  - field_name: photos_bien
    required: false
    type: array
    format: image

minimum_provider_matching_ready_fields:
  - field_name: localisation_expertise
    required: true
  - field_name: type_bien
    required: true
  - field_name: surface_min_max
    required: true
    type: range
  - field_name: specialite_evaluateur
    required: true
    values:
      - evaluation_standard
      - evaluation_luxe
      - evaluation_commerciale
      - evaluation_industrielle
      - evaluation_agricole
      - evaluation_terrain
      - evaluation_copropriete
  - field_name: qualification
    required: true
    values:
      - expert_agree
      - evaluateur_certifie
      - agent_immobilier
      - ingenieur_evaluateur
      - mru_chartered
  - field_name: methode_evaluation
    required: false
    values:
      - comparative
      - par_revenu
      - par_cout
      - multicritere
      - actualisation
  - field_name: marche_connaissance
    required: true
    values:
      - local
      - regional
      - national
      - international
  - field_name: experience_minimum_ans
    required: true
    type: integer
  - field_name: assurance_professionnelle
    required: true
    type: boolean

minimum_quote_ready_fields:
  - field_name: rapport_estimation
    required: true
    type: document
    format: pdf
  - field_name: analyse_comparative
    required: true
    type: document
  - field_name: prix_m2_moyen_secteur
    required: true
    type: float
  - field_name: fourchette_estimation
    required: true
    type: object
    sub_fields:
      - field_name: valeur_basse
        type: float
      - field_name: valeur_haute
        type: float
      - field_name: valeur_retenue
        type: float
  - field_name: facteurs_influents
    required: true
    type: array
    items:
      - etat_general
      - emplacement
      - prestations
      - performance_energetique
      - travaux_necessaires
  - field_name: transactions_recentes
    required: true
    type: array
    description: Transactions comparables recentes dans le secteur
  - field_name: hypotheses_retention
    required: true
    type: text
  - field_name: date_validite_estimation
    required: true
    type: date
  - field_name: conditions_financieres
    required: true
    type: contract
  - field_name: signature_contractuelle
    required: true
    type: boolean

minimum_execution_ready_fields:
  - field_name: mandat_estimation_signe
    required: true
    type: document
  - field_name: visite_bien_effectuee
    required: true
    type: boolean
  - field_name: dossier_photographique
    required: true
    type: array
  - field_name: rapport_final_livre
    required: true
    type: document
  - field_name: paiement_honoraires
    required: true
    type: boolean
  - field_name: confirmation_reception_client
    required: true
    type: boolean
  - field_name: archive_dossier
    required: true
    type: boolean
  - field_name: satisfaction_client
    required: false
    type: integer
    minimum: 1
    maximum: 5
```

---
## 2. expertise
```yaml
service_id: SVC-EXPE-002
canonical_name: expertise
display_name: "Expertise/Inspection"

description: >
  Service d'expertise technique approfondie d'un bien immobilier pour evaluer son etat, sa conformite et identifier les desordres.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: description_bien
    required: true
  - field_name: type_expertise
    required: true
    values:
      - expertise_pre_achat
      - expertise_technique
      - expertise_structure
      - expertise_sinistre
      - expertise_conformite
      - expertise_copropriete
      - expertise_thermique
      - expertise_acoustique
  - field_name: objet_expertise
    required: true
    type: text
  - field_name: surface_concernee
    required: false
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: documents_existants
    required: false
    type: array
  - field_name: sinistre_description
    required: false
    condition: type_expertise == expertise_sinistre

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_expertise
    required: true
  - field_name: specialite_expert
    required: true
    values:
      - technique_general
      - structure
      - etancheite
      - electricite
      - plomberie
      - thermique
      - acoustique
      - amiante
      - termites
      - pluridisciplinaire
  - field_name: qualification_expert
    required: true
    values:
      - expert_pres_tribunal
      - ingenieur_conseil
      - architecte_dplg
      - diagnostiqueur_certifie
      - expert_assurance
  - field_name: assurance_rc_pro
    required: true
    type: boolean
  - field_name: equipement_specialise
    required: false
    values:
      - camera_thermique
      - endoscope
      - humidimetre
      - detecteur_gaz
      - sonomètre
      - test_etancheite
  - field_name: experience_minimum
    required: true
    type: integer
  - field_name: zone_intervention_km
    required: true
    type: integer
  - field_name: honoraires_journaliers
    required: true
    type: float
  - field_name: disponibilite
    required: true
  - field_name: references_expertises
    required: true
    type: array

minimum_quote_ready_fields:
  - field_name: rapport_expertise_provisoire
    required: true
    type: document
  - field_name: constatations_techniques
    required: true
    type: text
  - field_name: photos_anomalies
    required: true
    type: array
  - field_name: classification_desordres
    required: true
    type: object
    sub_fields:
      - field_name: urgence_haute
        type: array
      - field_name: urgence_moyenne
        type: array
      - field_name: urgence_basse
        type: array
  - field_name: estimation_travaux
    required: true
    type: object
  - field_name: conformite_normes
    required: true
    type: array
  - field_name: duree_validite_rapport
    required: true
    type: integer
    unit: mois
  - field_name: honoraires_convenus
    required: true
    type: float
  - field_name: delai_rendu
    required: true
    type: string
  - field_name: signature_expert
    required: true
    type: boolean

minimum_execution_ready_fields:
  - field_name: contrat_expertise_signe
    required: true
    type: document
  - field_name: acces_bien_obtenu
    required: true
    type: boolean
  - field_name: visite_effectuee
    required: true
    type: boolean
  - field_name: rapport_final_livre
    required: true
    type: document
  - field_name: paiement_effectue
    required: true
    type: boolean
  - field_name: accusé_reception_client
    required: true
    type: boolean
  - field_name: archive_conservation
    required: true
    type: boolean
    description: Archivage du rapport pour duree legale
```

---
## 3. verification_documentaire
```yaml
service_id: SVC-VERI-003
canonical_name: verification_documentaire
display_name: "Document Verification"

description: >
  Service de verification de la conformite et de l'authenticite des documents juridiques et fonciers d'un bien immobilier.

minimum_service_ready_fields:
  - field_name: type_verification
    required: true
    values:
      - verif_titre_foncier
      - verif_permis_construire
      - verif_reglement_copropriete
      - verif_contrat_bail
      - verif_acte_vente
      - verif_diagnostic_technique
      - verif_attestation_fiscale
      - verif_complete_due_diligence
  - field_name: documents_a_verifier
    required: true
    type: array
  - field_name: objectif_verification
    required: true
    values:
      - acquisition
      - location
      - financement
      - assurance
      - succession
      - litigation
      - conformite_reglementaire
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true

minimum_provider_matching_ready_fields:
  - field_name: specialite_juridique
    required: true
    values:
      - droit_immobilier
      - droit_foncier
      - droit_copropriete
      - droit_bail
      - droit_urbanisme
      - droit_fiscal_immobilier
      - generaliste
  - field_name: qualification_verificateur
    required: true
    values:
      - avocat
      - notaire
      - juriste_immobilier
      - clerc_notaire
      - conseiller_juridique
  - field_name: experience_annees
    required: true
  - field_name: assurance_rc_pro
    required: true
  - field_name: delai_traitement_moyen
    required: true
  - field_name: tarif_verification
    required: true
  - field_name: langues_maitrisees
    required: false
    values:
      - francais
      - anglais
      - arabe
      - portugais

minimum_quote_ready_fields:
  - field_name: rapport_verification
    required: true
    type: document
  - field_name: conformite_globale
    required: true
    type: boolean
  - field_name: anomalies_detectees
    required: false
    type: array
  - field_name: recommandations
    required: true
    type: text
  - field_name: risques_juridiques
    required: true
    type: array
  - field_name: actions_rectificatives
    required: false
    type: array
  - field_name: date_validite_verification
    required: true
    type: date
  - field_name: honoraires_convenus
    required: true
    type: float
  - field_name: signature_verificateur
    required: true
    type: boolean

minimum_execution_ready_fields:
  - field_name: mandat_verification_signe
    required: true
    type: document
  - field_name: documents_recus_complets
    required: true
    type: boolean
  - field_name: verification_effectuee
    required: true
    type: boolean
  - field_name: rapport_final_livre
    required: true
    type: document
  - field_name: paiement_honoraires
    required: true
    type: boolean
  - field_name: restitution_client
    required: true
    type: boolean
  - field_name: archive_securisee
    required: true
    type: boolean
```

---
## 4. visite_property
```yaml
service_id: SVC-VISI-004
canonical_name: visite_property
display_name: "Property Visit"

description: >
  Service d'organisation et de realisation de visites physiques d'un bien immobilier pour des clients potentiels.

minimum_service_ready_fields:
  - field_name: localisation_bien
    required: true
  - field_name: type_bien
    required: true
  - field_name: date_visite
    required: true
    type: date
  - field_name: creneau_horaire
    required: true
    type: string
  - field_name: duree_estimee
    required: true
    type: string
  - field_name: nombre_visiteurs
    required: true
    type: integer
  - field_name: type_visite
    required: true
    values:
      - visite_individuelle
      - visite_groupe
      - visite_libre
      - visite_virtuelle
      - porte_ouverte
  - field_name: accompagnateur
    required: false
  - field_name: acces_instructions
    required: false
  - field_name: documents_preparer
    required: false
    type: array

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: rayon_action_km
    required: true
    type: integer
  - field_name: disponibilite
    required: true
  - field_name: type_bien_maitrise
    required: true
    values:
      - tous_biens
      - residentiel
      - commercial
      - industriel
      - terrain
      - luxe
  - field_name: experience_visites
    required: true
    type: integer
  - field_name: vehicule_disponible
    required: false
    type: boolean
  - field_name: langue_parlee
    required: true
  - field_name: formation_commerciale
    required: false
    type: boolean
  - field_name: taux_conversion_visites
    required: false
    type: float

minimum_quote_ready_fields:
  - field_name: rapport_visite
    required: true
    type: document
  - field_name: feedback_visiteur
    required: true
    type: text
  - field_name: interet_exprime
    required: true
    values:
      - tres_interesse
      - interet_moyen
      - peu_interesse
      - aucun_interet
  - field_name: suivi_propose
    required: true
    type: boolean
  - field_name: remarques_techniques
    required: false
    type: text
  - field_name: photos_visite
    required: false
    type: array
  - field_name: conditions_honoraires_visite
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: planning_visite_confirme
    required: true
    type: boolean
  - field_name: acces_bien_organise
    required: true
    type: boolean
  - field_name: visite_realisee
    required: true
    type: boolean
  - field_name: compte_rendu_transmis
    required: true
    type: boolean
  - field_name: suivi_client_effectue
    required: true
    type: boolean
  - field_name: paiement_prestation
    required: true
    type: boolean
  - field_name: stockage_donnees
    required: true
    type: boolean
```

---
## 5. contre_visite
```yaml
service_id: SVC-CONT-005
canonical_name: contre_visite
display_name: "Counter-Visit"

description: >
  Service de seconde visite organisee pour des clients ayant deja visite un bien, afin d'approfondir leur connaissance ou finaliser une decision.

minimum_service_ready_fields:
  - field_name: localisation_bien
    required: true
  - field_name: type_bien
    required: true
  - field_name: date_contre_visite
    required: true
  - field_name: creneau_horaire
    required: true
  - field_name: duree_estimee
    required: true
  - field_name: nombre_visiteurs
    required: true
  - field_name: objectif_contre_visite
    required: true
    values:
      - accompagnement_technicien
      - mesure_complementaire
      - visite_familiale
      - expertise_conjointe
      - demonstration_equipement
      - signature_sur_place
  - field_name: accompagnateurs_supplementaires
    required: false
    type: array
  - field_name: documents_complementaires
    required: false
    type: array

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: specialite
    required: true
    values:
      - accompagnateur_technique
      - commercial_senior
      - negociation
      - expert_technique
  - field_name: disponibilite
    required: true
  - field_name: experience_contre_visites
    required: true
    type: integer
  - field_name: formation_technique
    required: false
    type: boolean
  - field_name: connaissance_secteur
    required: true
  - field_name: vehicule
    required: false
  - field_name: taux_reussite_contre_visite
    required: false
    type: float

minimum_quote_ready_fields:
  - field_name: rapport_contre_visite
    required: true
    type: document
  - field_name: avancement_decision
    required: true
    values:
      - decision_positive
      - besoin_reflexion
      - abandon
      - condition_suspensive
  - field_name: objections_levees
    required: false
    type: array
  - field_name: points_bloquants
    required: false
    type: array
  - field_name: prochaine_etape
    required: true
    values:
      - proposition_offre
      - signature_compromis
      - nouvelle_visite
      - fin_processus
  - field_name: honoraires_convenus
    required: true
    type: float

minimum_execution_ready_fields:
  - field_name: contre_visite_planifiee
    required: true
    type: boolean
  - field_name: acces_bien_confirme
    required: true
    type: boolean
  - field_name: contre_visite_realisee
    required: true
    type: boolean
  - field_name: compte_rendu_transmis
    required: true
    type: boolean
  - field_name: suivi_engage
    required: true
    type: boolean
  - field_name: paiement_effectue
    required: true
    type: boolean
```

---
## 6. gestion_locative
```yaml
service_id: SVC-GEST-006
canonical_name: gestion_locative
display_name: "Rental Management"

description: >
  Service de gestion locative complete incluant la recherche de locataire, la redaction de bail, le suivi des loyers et la gestion des relations locatives.

minimum_service_ready_fields:
  - field_name: localisation_bien
    required: true
  - field_name: type_bien
    required: true
  - field_name: surface
    required: true
  - field_name: description_bien
    required: true
  - field_name: nombre_pieces
    required: true
  - field_name: loyer_souhaite
    required: true
    type: float
  - field_name: charges_incluses
    required: false
    type: boolean
  - field_name: duree_mandat
    required: true
    values:
      - 6_mois
      - 1_an
      - 2_ans
      - 3_ans
      - indetermine
  - field_name: type_gestion
    required: true
    values:
      - gestion_complete
      - recherche_locataire
      - gestion_loyer
      - gestion_saisonnieres
  - field_name: meuble
    required: false
    type: boolean
  - field_name: inventaire_mobilier
    required: false
  - field_name: date_disponibilite
    required: true
  - field_name: diagnostics_disponibles
    required: false
    type: array
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: rayon_gestion
    required: true
    type: integer
  - field_name: portefeuille_actuel
    required: true
    values:
      - moins_5_biens
      - 5_20_biens
      - 20_50_biens
      - plus_50_biens
  - field_name: type_bien_maitrise
    required: true
    values:
      - residentiel
      - commercial
      - mixte
      - tous
  - field_name: logiciel_gestion
    required: false
    values:
      - immosquare
      - gestion_locative_pro
      - sage
      - city_spot
      - excel
      - autre
  - field_name: equipe_gestion
    required: true
    type: integer
  - field_name: assurance_professionnelle
    required: true
  - field_name: agrement_professionnel
    required: true
    values:
      - carte_pro_g
      - agrement_sci
      - mandat_gerance
  - field_name: experience_annees
    required: true
  - field_name: taux_occupation_moyen
    required: false
    type: float
  - field_name: taux_recouvrement
    required: false
    type: float

minimum_quote_ready_fields:
  - field_name: contrat_gestion_propose
    required: true
    type: document
  - field_name: honoraires_gestion
    required: true
    type: object
    sub_fields:
      - field_name: frais_mise_en_location
        type: string
      - field_name: frais_gestion_mensuelle
        type: string
      - field_name: frais_gestion_travaux
        type: string
      - field_name: frais_recouvrement
        type: string
  - field_name: conditions_resiliation
    required: true
    type: text
  - field_name: mandat_location
    required: true
    type: document
  - field_name: etat_des_lieux
    required: true
    type: document
  - field_name: diagnostic_technique
    required: true
    type: array
  - field_name: estimation_charges_annuelles
    required: false
    type: float
  - field_name: assurance_loyers_impayes_proposee
    required: false
    type: boolean
  - field_name: calendrier_prestations
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_gestion_signe
    required: true
    type: document
  - field_name: mandat_location_signe
    required: true
    type: document
  - field_name: etat_des_lieux_initial
    required: true
    type: document
  - field_name: annonce_publication
    required: true
    type: boolean
  - field_name: bail_signe
    required: true
    type: document
  - field_name: etat_des_lieux_entree
    required: true
    type: document
  - field_name: depot_garantie_encaisse
    required: true
    type: boolean
  - field_name: premier_loyer_percu
    required: true
    type: boolean
  - field_name: assurance_habitation_locataire
    required: true
    type: boolean
  - field_name: dossier_compte_rendu_bailleur
    required: true
    type: boolean
  - field_name: archive_comptable
    required: true
    type: boolean
```

---
## 7. mise_en_location
```yaml
service_id: SVC-MISE-007
canonical_name: mise_en_location
display_name: "Listing for Rent"

description: >
  Service de mise en location d'un bien immobilier incluant la publication d'annonces, la selection de locataires et la redaction du bail.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: surface
    required: true
  - field_name: loyer_demande
    required: true
  - field_name: charges
    required: false
  - field_name: depot_garantie
    required: false
  - field_name: description_bien
    required: true
  - field_name: photos_bien
    required: true
  - field_name: date_disponibilite
    required: true
  - field_name: duree_bail
    required: true
    values:
      - 1_an
      - 2_ans
      - 3_ans
      - mois_mois
      - saisonnier
  - field_name: meuble_non_meuble
    required: true
    values:
      - meuble
      - non_meuble
  - field_name: criteres_locataire
    required: false
  - field_name: conditions_specifiques
    required: false
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien_maitrise
    required: true
  - field_name: volume_location_annuel
    required: false
    type: integer
  - field_name: contrat_type_bail
    required: true
    type: document
  - field_name: delai_moyen_location
    required: false
    type: string
  - field_name: equipement_photo
    required: false
  - field_name: canaux_publication
    required: true
    values:
      - jumia_house
      - expat_dakar
      - lamudi
      - facebook_marketplace
      - site_agence_en_ligne
      - presse
      - affichage
  - field_name: service_juridique_bail
    required: false
  - field_name: honoraires_mise_location
    required: true
  - field_name: experience_location
    required: true
    type: integer

minimum_quote_ready_fields:
  - field_name: contrat_mandat_location
    required: true
    type: document
  - field_name: annonce_pret_a_publier
    required: true
    type: text
  - field_name: criteres_selection
    required: true
    type: array
  - field_name: honoraires_mandat
    required: true
    type: float
  - field_name: conditions_exclusivite
    required: false
    type: boolean
  - field_name: duree_mandat
    required: true
    type: string
  - field_name: visite_planification
    required: true
    type: boolean
  - field_name: modele_bail
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: mandat_location_signe
    required: true
    type: document
  - field_name: annonce_publiee
    required: true
    type: boolean
  - field_name: candidats_examines
    required: true
    type: boolean
  - field_name: dossier_locataire_retenu
    required: true
    type: document
  - field_name: bail_signe
    required: true
    type: document
  - field_name: etat_des_lieux_entree
    required: true
    type: document
  - field_name: depot_garantie_recu
    required: true
    type: boolean
  - field_name: honoraires_percus
    required: true
    type: boolean
  - field_name: archive_dossier
    required: true
    type: boolean
```

---
## 8. mise_en_vente
```yaml
service_id: SVC-MISE-008
canonical_name: mise_en_vente
display_name: "Listing for Sale"

description: >
  Service de mise en vente d'un bien immobilier incluant l'estimation, la publication d'annonces, les visites et l'accompagnement jusqu'a la vente.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: surface
    required: true
  - field_name: prix_demande
    required: true
  - field_name: description_bien
    required: true
  - field_name: photos_bien
    required: true
  - field_name: date_disponibilite
    required: true
  - field_name: type_mandat
    required: true
    values:
      - mandat_simple
      - mandat_exclusif
      - mandat_semi_exclusif
      - co_mandat
  - field_name: diagnostiques_obligatoires
    required: true
    type: array
  - field_name: dossier_technique_bien
    required: false
    type: document
  - field_name: frais_agence
    required: false
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: secteur_vente
    required: true
    values:
      - residentiel
      - commercial
      - industriel
      - terrain
      - luxe
      - tous
  - field_name: volume_vente_annuel
    required: true
    type: integer
  - field_name: prix_m2_moyen_pratique
    required: false
    type: float
  - field_name: canaux_diffusion
    required: true
    values:
      - jumia_house
      - expat_dakar
      - lamudi
      - facebook_marketplace
      - site_web
      - reseau_partenaire
      - presse
  - field_name: equipe_commerciale
    required: true
    type: integer
  - field_name: photographe_pro
    required: false
  - field_name: home_staging_service
    required: false
  - field_name: honoraires_vente
    required: true
  - field_name: experience_vente_annees
    required: true
  - field_name: taux_reussite_vente
    required: false
    type: float
  - field_name: delai_moyen_vente
    required: false

minimum_quote_ready_fields:
  - field_name: contrat_mandat_vente
    required: true
    type: document
  - field_name: estimation_prix_conseille
    required: true
    type: float
  - field_name: honoraires_convenus
    required: true
    type: float
  - field_name: plan_diffusion
    required: true
    type: array
  - field_name: conditions_exclusivite
    required: false
    type: boolean
  - field_name: diagnostics_fournis
    required: true
    type: boolean
  - field_name: calendrier_actions
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: mandat_vente_signe
    required: true
    type: document
  - field_name: annonce_publiee
    required: true
    type: boolean
  - field_name: visites_realisees
    required: true
    type: integer
  - field_name: offre_recue_examinee
    required: true
    type: boolean
  - field_name: compromis_signe
    required: true
    type: document
  - field_name: acte_vente_finalise
    required: true
    type: document
  - field_name: commission_percue
    required: true
    type: boolean
  - field_name: archive_dossier
    required: true
    type: boolean
```

---
## 9. publication_service
```yaml
service_id: SVC-PUBL-009
canonical_name: publication_service
display_name: "Listing Publication Service"

description: >
  Service de publication et de diffusion d'annonces immobilieres sur les plateformes et canaux appropries pour maximiser la visibilite.

minimum_service_ready_fields:
  - field_name: description_bien
    required: true
    type: text
  - field_name: photos
    required: true
    type: array
  - field_name: prix
    required: true
  - field_name: localisation
    required: true
  - field_name: type_transaction
    required: true
    values:
      - vente
      - location
      - viager
      - echange
  - field_name: type_bien
    required: true
  - field_name: surface
    required: true
  - field_name: nombre_pieces
    required: false
  - field_name: canaux_souhaites
    required: true
    type: array
    values:
      - jumia_house
      - expat_dakar
      - lamudi
      - facebook_marketplace
      - instagram
      - site_internet
      - presse_ecrite
      - affichage_physique
      - newsletter
  - field_name: duree_publication
    required: true
    values:
      - 7_jours
      - 14_jours
      - 30_jours
      - 60_jours
      - jusqua_vente
  - field_name: budget_publicite
    required: false
  - field_name: langues_annonce
    required: false
    values:
      - francais
      - anglais
      - bilingue
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: canaux_maitrises
    required: true
    type: array
  - field_name: audience_estimee
    required: false
    type: string
  - field_name: tarifs_publication
    required: true
    type: object
  - field_name: delai_mise_en_ligne
    required: true
  - field_name: service_redaction_annonce
    required: false
  - field_name: service_photo_inclus
    required: false
  - field_name: statistiques_visibilite
    required: false
  - field_name: experience_publications
    required: true
    type: integer
  - field_name: references_annonces
    required: false
    type: array

minimum_quote_ready_fields:
  - field_name: contrat_publication
    required: true
    type: document
  - field_name: redaction_annonce
    required: true
    type: text
  - field_name: visuels_prets
    required: true
    type: boolean
  - field_name: planning_diffusion
    required: true
    type: schedule
  - field_name: budget_publicitaire
    required: true
    type: float
  - field_name: canaux_selectionnes
    required: true
    type: array
  - field_name: indicateurs_performance
    required: true
    type: array
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: annonce_redigee_validee
    required: true
    type: boolean
  - field_name: publication_effective
    required: true
    type: boolean
  - field_name: rapport_diffusion
    required: true
    type: document
  - field_name: statistiques_consultations
    required: true
    type: object
  - field_name: paiement_effectue
    required: true
    type: boolean
  - field_name: archive_campagne
    required: true
    type: boolean
```

---
## 10. photographie
```yaml
service_id: SVC-PHOT-010
canonical_name: photographie
display_name: "Photography"

description: >
  Service de photographie immobiliere professionnelle pour mettre en valeur les biens a vendre ou a louer.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: surface_photographier
    required: true
  - field_name: type_prestation
    required: true
    values:
      - photo_interieure
      - photo_exterieure
      - reportage_complet
      - photo_hdr
      - photo_aerienne
      - visite_virtuelle_360
  - field_name: nombre_pieces
    required: true
  - field_name: exterieur_present
    required: false
  - field_name: nombre_photos_souhaite
    required: false
  - field_name: delai_livraison_souhaite
    required: true
  - field_name: retouche_photo
    required: false
    type: boolean
  - field_name: date_souhaitee
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: rayon_action_km
    required: true
  - field_name: equipement_photo
    required: true
    values:
      - reflex_pro
      - mirrorless_full_frame
      - objectif_grand_angle
      - flash_pro
      - pied_tres_qualite
  - field_name: experience_annees
    required: true
  - field_name: portfolio_immobilier
    required: true
  - field_name: delai_livraison_standard
    required: true
  - field_name: tarifs_prestations
    required: true
  - field_name: service_retouche_inclus
    required: false
  - field_name: assurance_materiel
    required: false
  - field_name: format_livraison
    required: false
    values:
      - jpg_hd
      - raw
      - tiff
      - png
      - webp
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: contrat_prestation_photo
    required: true
    type: document
  - field_name: nombre_photos_convenues
    required: true
    type: integer
  - field_name: format_livraison
    required: true
    type: string
  - field_name: retouche_incluse
    required: true
    type: boolean
  - field_name: droits_utilisation
    required: true
    type: contract
  - field_name: delai_livraison_contractuel
    required: true
    type: string
  - field_name: honoraires_convenus
    required: true
    type: float
  - field_name: planning_seance
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: seance_realisee
    required: true
    type: boolean
  - field_name: photos_livrees
    required: true
    type: boolean
  - field_name: droits_cedes_contractualises
    required: true
    type: boolean
  - field_name: paiement_effectue
    required: true
    type: boolean
  - field_name: validation_client
    required: true
    type: boolean
  - field_name: archive_images
    required: true
    type: boolean
```

---
## 11. video_service
```yaml
service_id: SVC-VIDE-011
canonical_name: video_service
display_name: "Video Service"

description: >
  Service de production video professionnelle pour la presentation dynamique de biens immobiliers.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: type_video
    required: true
    values:
      - video_visite
      - video_promotionnelle
      - video_chantier
      - video_temoignage
      - video_avant_apres
      - video_architecture
  - field_name: duree_souhaitee
    required: true
    type: string
  - field_name: style_souhaite
    required: false
  - field_name: date_tournage
    required: true
  - field_name: delai_livraison
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: equipement_video
    required: true
    values:
      - camera_cinema
      - mirrorless_video
      - drone_cinematique
      - stabilisateur_gimbal
      - son_externe_pro
      - eclairage_pro
  - field_name: experience_video_immobiliere
    required: true
  - field_name: portfolio_video
    required: true
  - field_name: logiciel_montage
    required: false
    values:
      - premiere_pro
      - final_cut
      - davinci_resolve
      - after_effects
  - field_name: delai_moyen_livraison
    required: true
  - field_name: tarifs_production
    required: true
  - field_name: service_post_production
    required: false
  - field_name: assurance_materiel
    required: false
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: contrat_production_video
    required: true
    type: document
  - field_name: storyboard_scenario
    required: true
    type: document
  - field_name: duree_video_convenue
    required: true
    type: string
  - field_name: format_livraison
    required: true
    values:
      - mp4_hd
      - mp4_4k
      - mov
      - vertical_reels
  - field_name: droits_diffusion
    required: true
    type: contract
  - field_name: nombre_revisions_incluses
    required: true
    type: integer
  - field_name: planning_tournage
    required: true
    type: schedule
  - field_name: honoraires_convenus
    required: true
    type: float
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: tournage_realise
    required: true
    type: boolean
  - field_name: video_montee
    required: true
    type: boolean
  - field_name: revisions_effectuees
    required: true
    type: boolean
  - field_name: video_finale_livree
    required: true
    type: boolean
  - field_name: droits_cedes
    required: true
    type: boolean
  - field_name: paiement_effectue
    required: true
    type: boolean
  - field_name: validation_client
    required: true
    type: boolean
  - field_name: archive_projet
    required: true
    type: boolean
```

---
## 12. drone_service
```yaml
service_id: SVC-DRON-012
canonical_name: drone_service
display_name: "Drone Service"

description: >
  Service de prise de vues aeriennes par drone pour les biens immobiliers, les terrains et les projets de construction.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: coordonnees_gps
    required: false
  - field_name: type_bien_terrain
    required: true
  - field_name: surface_survol
    required: true
  - field_name: objectif
    required: true
    values:
      - photo_aerienne
      - video_survol
      - inspection_toiture
      - topographie
      - suivi_chantier
      - visite_virtuelle_aerienne
      - vue_quartier
  - field_name: hauteur_vol_max
    required: false
  - field_name: contraintes_environnement
    required: false
  - field_name: date_souhaitee
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: certification_drone
    required: true
    values:
      - telepilote_dgac
      - brevet_drone
      - assurance_drone
      - autorisation_survol_urbain
  - field_name: type_drone
    required: true
    values:
      - drone_cinematique
      - drone_topographique_rtk
      - drone_thermique
      - drone_photogrammetrie
  - field_name: experience_drone_immobilier
    required: true
  - field_name: portfolio_aerien
    required: true
  - field_name: assurance_specifique_drone
    required: true
  - field_name: licence_telepilote
    required: true
  - field_name: zone_autorisation_prefectorale
    required: false
  - field_name: tarif_vol_horaire
    required: true
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: contrat_prestation_drone
    required: true
    type: document
  - field_name: plan_de_vol
    required: true
    type: document
  - field_name: duree_vol_estimee
    required: true
    type: string
  - field_name: autorisations_necessaires
    required: true
    type: array
  - field_name: format_livraison_souhaite
    required: true
    values:
      - photos_hd
      - video_4k
      - orthophoto
      - modele_3d
      - nuage_points
  - field_name: conditions_securite
    required: true
    type: document
  - field_name: honoraires_convenus
    required: true
    type: float
  - field_name: planning_vol
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: autorisations_obtenues
    required: true
    type: boolean
  - field_name: vol_realise
    required: true
    type: boolean
  - field_name: donnees_brutes_livrees
    required: true
    type: boolean
  - field_name: post_traitement_effectue
    required: true
    type: boolean
  - field_name: livrables_finaux_transmis
    required: true
    type: boolean
  - field_name: paiement_effectue
    required: true
    type: boolean
  - field_name: validation_client
    required: true
    type: boolean
  - field_name: archive_donnees_vol
    required: true
    type: boolean
```

---
## 13. home_staging
```yaml
service_id: SVC-HOME-013
canonical_name: home_staging
display_name: "Home Staging"

description: >
  Service de home staging pour valoriser un bien immobilier avant sa mise en vente ou en location, en optimisant sa presentation.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: surface
    required: true
  - field_name: pieces_concernees
    required: true
    type: array
  - field_name: etat_actuel
    required: true
    values:
      - vide
      - meuble
      - en_cours_travaux
      - degrade
      - bon_etat
  - field_name: objectif_staging
    required: true
    values:
      - vente
      - location
      - valorisation_prix
      - acceleration_vente
  - field_name: budget_staging
    required: false
  - field_name: contraintes_deco
    required: false
  - field_name: date_souhaitee
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: specialite_staging
    required: true
    values:
      - home_staging_residentiel
      - home_staging_luxe
      - home_staging_commercial
      - home_staging_location
  - field_name: portfolio_realisations
    required: true
  - field_name: stock_mobilier
    required: true
    type: boolean
  - field_name: equipe_decorateurs
    required: true
    type: integer
  - field_name: delai_moyen_intervention
    required: true
  - field_name: tarifs_staging_m2
    required: true
  - field_name: service_conseil_inclus
    required: false
  - field_name: forfaits_proposes
    required: false
    values:
      - essor_visibilite
      - home_staging_classique
      - home_staging_complet
      - home_staging_premium
  - field_name: references_avant_apres
    required: true
    type: array
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: contrat_prestation_staging
    required: true
    type: document
  - field_name: diagnostic_deco
    required: true
    type: document
  - field_name: proposition_staging
    required: true
    type: document
  - field_name: liste_interventions
    required: true
    type: array
  - field_name: calendrier_interventions
    required: true
    type: schedule
  - field_name: budget_staging_convenu
    required: true
    type: float
  - field_name: conditions_location_mobilier
    required: false
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: duree_location_mobilier
    required: false
  - field_name: reportage_photo_after
    required: false
    type: boolean

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: diagnostic_deco_realise
    required: true
    type: boolean
  - field_name: mobilier_installe
    required: true
    type: boolean
  - field_name: travaux_deco_realises
    required: true
    type: boolean
  - field_name: photos_after_livrees
    required: true
    type: boolean
  - field_name: mise_en_vente_location_effective
    required: true
    type: boolean
  - field_name: paiement_effectue
    required: true
    type: boolean
  - field_name: suivi_post_staging
    required: false
    type: boolean
```

---
## 14. renovation_service
```yaml
service_id: SVC-RENO-014
canonical_name: renovation_service
display_name: "Renovation Service"

description: >
  Service de renovation et de remise en etat de biens immobiliers incluant la coordination des corps de metier et le suivi de chantier.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: surface_concernee
    required: true
  - field_name: type_renovation
    required: true
    values:
      - renovation_complete
      - renovation_cuisine
      - renovation_salle_bain
      - ravalement_facade
      - mise_aux_normes
      - extension
      - amenagement_combles
      - renovation_energetique
      - rafraichissement
  - field_name: etat_actuel
    required: true
  - field_name: description_travaux
    required: true
  - field_name: budget_estime
    required: true
  - field_name: delai_souhaite
    required: true
  - field_name: occupation_site
    required: true
    type: boolean
  - field_name: photos_etat_lieux
    required: false
  - field_name: autorisations_necessaires
    required: false
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: specialite_renovation
    required: true
    values:
      - renovation_generale
      - renovation_luxe
      - renovation_energetique
      - renovation_apres_sinistre
      - renovation_copropriete
  - field_name: equipe_disponible
    required: true
    type: integer
  - field_name: qualifications
    required: true
    type: array
  - field_name: assurance_decennale
    required: true
  - field_name: references_chantiers
    required: true
  - field_name: delai_moyen_chantier
    required: true
  - field_name: garantie_travaux
    required: true
  - field_name: fournisseurs_partenaires
    required: false
  - field_name: tarif_m2_moyen
    required: true
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: contrat_renovation
    required: true
    type: document
  - field_name: cahier_charges_travaux
    required: true
    type: document
  - field_name: devis_detaille
    required: true
    type: document
  - field_name: planning_chantier
    required: true
    type: schedule
  - field_name: budget_materiaux
    required: true
    type: float
  - field_name: budget_main_oeuvre
    required: true
    type: float
  - field_name: echeancier_paiement
    required: true
    type: schedule
  - field_name: permis_autorisations
    required: false
    type: document
  - field_name: garantie_decennale_attestation
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: chantier_ouvert
    required: true
    type: boolean
  - field_name: travaux_realises
    required: true
    type: boolean
  - field_name: reception_travaux
    required: true
    type: document
  - field_name: factures_acquittees
    required: true
    type: boolean
  - field_name: etat_lieux_final
    required: true
    type: document
  - field_name: garantie_parfait_achevement
    required: true
    type: boolean
  - field_name: paiement_final_effectue
    required: true
    type: boolean
  - field_name: satisfaction_client
    required: false
    type: boolean
```

---
## 15. construction_service
```yaml
service_id: SVC-CONS-015
canonical_name: construction_service
display_name: "Construction Service"

description: >
  Service de construction neuve de biens immobiliers, de la conception a la livraison, incluant la gestion de projet et la coordination des intervenants.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: terrain_disponible
    required: true
    type: boolean
  - field_name: surface_terrain
    required: true
  - field_name: surface_construire
    required: true
  - field_name: type_construction
    required: true
    values:
      - maison_individuelle
      - villa
      - immeuble_collectif
      - batiment_commercial
      - batiment_industriel
      - lotissement
      - equipement_public
  - field_name: nombre_niveaux
    required: true
  - field_name: style_architectural
    required: false
  - field_name: budget_construction
    required: true
  - field_name: delai_souhaite
    required: true
  - field_name: terrain_viabilise
    required: false
  - field_name: permis_construire
    required: false
    type: boolean
  - field_name: etude_geotechnique
    required: false
    type: boolean
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: specialite_construction
    required: true
    values:
      - promoteur_immobilier
      - constructeur_maison
      - entreprise_batiment
      - maitre_oeuvre
      - lotisseur_amenageur
  - field_name: references_realisations
    required: true
  - field_name: equipe_projet
    required: true
    type: integer
  - field_name: annees_experience
    required: true
  - field_name: assurance_decennale
    required: true
  - field_name: garantie_financiere
    required: true
  - field_name: certifications_qualite
    required: false
  - field_name: capacite_production_annuelle
    required: false
  - field_name: partenaires_architectes
    required: false
  - field_name: fournisseurs_materiaux
    required: false
  - field_name: tarif_construction_m2
    required: true
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: contrat_construction
    required: true
    type: document
  - field_name: plans_architecte
    required: true
    type: document
  - field_name: permis_construire
    required: true
    type: document
  - field_name: etude_geotechnique
    required: true
    type: document
  - field_name: cahier_charges_technique
    required: true
    type: document
  - field_name: devis_quantitatif
    required: true
    type: document
  - field_name: planning_travaux
    required: true
    type: schedule
  - field_name: budget_total
    required: true
    type: float
  - field_name: echeancier_paiement
    required: true
    type: schedule
  - field_name: garanties_financieres
    required: true
    type: document
  - field_name: assurance_dommage_ouvrage
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: permis_construire_obtenu
    required: true
    type: boolean
  - field_name: fondations_realisees
    required: true
    type: boolean
  - field_name: structure_elevée
    required: true
    type: boolean
  - field_name: clos_couvert
    required: true
    type: boolean
  - field_name: reception_travaux
    required: true
    type: document
  - field_name: livraison_effective
    required: true
    type: boolean
  - field_name: paiements_effectues
    required: true
    type: boolean
  - field_name: garanties_activees
    required: true
    type: boolean
  - field_name: dossier_technique_remis
    required: true
    type: document
  - field_name: satisfaction_client
    required: false
    type: boolean
```

---
## 16. entretien
```yaml
service_id: SVC-ENTR-016
canonical_name: entretien
display_name: "Maintenance"

description: >
  Service d'entretien regulier et de maintenance preventive de biens immobiliers pour preserver leur etat et leur valeur.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: type_entretien
    required: true
    values:
      - entretien_courant
      - entretien_preventif
      - entretien_espaces_verts
      - entretien_piscine
      - entretien_facade
      - entretien_ascenseur
      - entretien_chauffage_clim
      - entretien_toiture
      - entretien_plomberie
      - entretien_electricite
  - field_name: periodicite
    required: true
    values:
      - hebdomadaire
      - bimensuel
      - mensuel
      - trimestriel
      - semestriel
      - annuel
      - ponctuel
  - field_name: surface_concernee
    required: false
  - field_name: description_besoin
    required: true
  - field_name: contrat_entretien
    required: false
    type: boolean
  - field_name: date_debut
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: specialite_entretien
    required: true
  - field_name: equipe_techniciens
    required: true
    type: integer
  - field_name: certifications
    required: true
  - field_name: assurance_professionnelle
    required: true
  - field_name: references_contrats
    required: true
  - field_name: delai_intervention_moyen
    required: true
  - field_name: tarif_horaire_forfait
    required: true
  - field_name: stock_pieces_detachees
    required: false
  - field_name: disponibilite_urgence
    required: false
  - field_name: outillage_specialise
    required: false
  - field_name: vehicule_atelier
    required: false

minimum_quote_ready_fields:
  - field_name: contrat_entretien_propose
    required: true
    type: document
  - field_name: programme_entretien
    required: true
    type: document
  - field_name: calendrier_passages
    required: true
    type: schedule
  - field_name: tarifs_annuels
    required: true
    type: float
  - field_name: conditions_resiliation
    required: true
    type: text
  - field_name: pieces_incluses
    required: false
    type: boolean
  - field_name: main_oeuvre_incluse
    required: true
    type: boolean
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: programme_entretien_etabli
    required: true
    type: boolean
  - field_name: interventions_realisees
    required: true
    type: boolean
  - field_name: rapports_intervention
    required: true
    type: array
  - field_name: facturation_effectuee
    required: true
    type: boolean
  - field_name: suivi_periodique
    required: true
    type: boolean
  - field_name: satisfaction_client
    required: false
    type: boolean
```

---
## 17. nettoyage
```yaml
service_id: SVC-NETT-017
canonical_name: nettoyage
display_name: "Cleaning"

description: >
  Service de nettoyage professionnel de biens immobiliers, ponctuel ou regulier, pour l'entretien et la remise en etat.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: type_nettoyage
    required: true
    values:
      - nettoyage_residentiel
      - nettoyage_bureau
      - nettoyage_commercial
      - nettoyage_chantier
      - nettoyage_location_vide
      - nettoyage_apres_travaux
      - nettoyage_facade_vitres
      - nettoyage_moquette_tapis
  - field_name: surface_nettoyer
    required: true
  - field_name: periodicite
    required: true
  - field_name: nombre_pieces
    required: false
  - field_name: description_taches
    required: true
  - field_name: produits_souhaites
    required: false
  - field_name: date intervention
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_nettoyage
    required: true
  - field_name: taille_equipe
    required: true
  - field_name: materiel_utilise
    required: true
  - field_name: produits_utilises
    required: false
  - field_name: agrements_qualite
    required: false
  - field_name: assurance_professionnelle
    required: true
  - field_name: references_clients
    required: true
  - field_name: tarif_m2
    required: true
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: contrat_prestation
    required: true
    type: document
  - field_name: cahier_charges
    required: true
    type: document
  - field_name: produits_utilises_liste
    required: true
    type: array
  - field_name: planning_intervention
    required: true
    type: schedule
  - field_name: tarifs_convenus
    required: true
    type: float
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: controle_qualite
    required: false
    type: document

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: intervention_realisee
    required: true
    type: boolean
  - field_name: fiche_produits_utilises
    required: true
    type: document
  - field_name: etat_lieux_apres_nettoyage
    required: true
    type: document
  - field_name: paiement_effectue
    required: true
    type: boolean
  - field_name: validation_client
    required: true
    type: boolean
  - field_name: satisfaction_qualite
    required: false
    type: boolean
```

---
## 18. securisation
```yaml
service_id: SVC-SECU-018
canonical_name: securisation
display_name: "Securing"

description: >
  Service de securisation temporaire ou permanente d'un bien immobilier incluant la mise en securite, le gardiennage et la surveillance.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: type_bien
    required: true
  - field_name: type_securisation
    required: true
    values:
      - securisation_temporaire
      - securisation_chantier
      - securisation_permanente
      - mise_en_securite_urgence
      - condamnation_acces
      - surveillance_electronique
      - gardiennage_site
  - field_name: surface_site
    required: true
  - field_name: duree_besoin
    required: true
  - field_name: niveau_securite
    required: true
    values:
      - standard
      - renforce
      - haute_securite
      - maximale
  - field_name: acces_existants
    required: false
  - field_name: equipements_presents
    required: false
  - field_name: horaire_couverture
    required: true
    values:
      - jour
      - nuit
      - 24h_24
      - week_end
      - personnalise
  - field_name: date_debut
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: specialite_securisation
    required: true
  - field_name: agrement_securite
    required: true
  - field_name: equipe_disponible
    required: true
  - field_name: equipements_surveillance
    required: false
    values:
      - camera_vision_nocturne
      - detecteur_mouvement
      - alarme_intrusion
      - barriere_infrarouge
      - controle_acces
  - field_name: assurance_professionnelle
    required: true
  - field_name: references_missions
    required: true
  - field_name: tarif_garde_horaire
    required: true
  - field_name: disponibilite_urgence
    required: true
  - field_name: centre_surveillance
    required: false
  - field_name: intervention_rapide
    required: false
    type: boolean

minimum_quote_ready_fields:
  - field_name: contrat_securisation
    required: true
    type: document
  - field_name: analyse_risques
    required: true
    type: document
  - field_name: plan_securisation
    required: true
    type: document
  - field_name: effectif_prevu
    required: true
    type: integer
  - field_name: equipements_deployes
    required: true
    type: array
  - field_name: calendrier_presence
    required: true
    type: schedule
  - field_name: procedures_urgence
    required: true
    type: document
  - field_name: budget_convenu
    required: true
    type: float
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: analyse_risques_realisee
    required: true
    type: boolean
  - field_name: equipement_installe
    required: true
    type: boolean
  - field_name: personnel_affecte
    required: true
    type: boolean
  - field_name: surveillance_active
    required: true
    type: boolean
  - field_name: rapports_periodiques
    required: true
    type: array
  - field_name: incidents_rapportes
    required: true
    type: array
  - field_name: paiement_effectue
    required: true
    type: boolean
  - field_name: levee_securisation
    required: false
    type: boolean
```

---
## 19. demenagement
```yaml
service_id: SVC-DEME-019
canonical_name: demenagement
display_name: "Moving"

description: >
  Service de demenagement complet pour particuliers et professionnels, incluant l'emballage, le transport et la remise en place.

minimum_service_ready_fields:
  - field_name: adresse_depart
    required: true
  - field_name: adresse_arrivee
    required: true
  - field_name: type_demenagement
    required: true
    values:
      - residentiel
      - professionnel
      - etudiant
      - local_commercial
      - bureau
      - industriel
  - field_name: volume_estime
    required: true
    description: Volume estime en metres cubes
  - field_name: etage_depart
    required: false
  - field_name: ascenseur_depart
    required: false
  - field_name: etage_arrivee
    required: false
  - field_name: ascenseur_arrivee
    required: false
  - field_name: distance_km
    required: true
  - field_name: services_souhaites
    required: true
    values:
      - transport_seul
      - emballage_inclus
      - demenagement_complet
      - montage_meubles
      - garde_meuble
      - assurance_transport
  - field_name: date_demenagement
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: type_demenagement
    required: true
  - field_name: capacite_transport
    required: true
  - field_name: flotte_vehicules
    required: true
  - field_name: equipe_demenageurs
    required: true
    type: integer
  - field_name: assurance_transport
    required: true
  - field_name: materiel_emballage
    required: false
  - field_name: garde_meuble_disponible
    required: false
  - field_name: monte_meuble_disponible
    required: false
  - field_name: experience_annees
    required: true
  - field_name: references_clients
    required: true
  - field_name: zones_desserte
    required: true
  - field_name: tarif_m3_km
    required: true
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: contrat_demenagement
    required: true
    type: document
  - field_name: inventaire_mobilier
    required: true
    type: document
  - field_name: volume_confirme
    required: true
    type: float
  - field_name: etat_lieux_depart
    required: true
    type: document
  - field_name: etat_lieux_arrivee
    required: true
    type: document
  - field_name: assurance_option
    required: true
    type: document
  - field_name: planning_jour_j
    required: true
    type: schedule
  - field_name: budget_total
    required: true
    type: float
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: conditions_annulation
    required: true
    type: text

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: inventaire_finalise
    required: true
    type: boolean
  - field_name: emballage_realise
    required: true
    type: boolean
  - field_name: transport_effectue
    required: true
    type: boolean
  - field_name: livraison_effectuee
    required: true
    type: boolean
  - field_name: montage_realise
    required: true
    type: boolean
  - field_name: etat_lieux_final
    required: true
    type: document
  - field_name: paiement_effectue
    required: true
    type: boolean
  - field_name: satisfaction_client
    required: false
    type: boolean
```

---
## 20. assurance_service
```yaml
service_id: SVC-ASSU-020
canonical_name: assurance_service
display_name: "Insurance Service"

description: >
  Service de souscription et de gestion de contrats d'assurance lies aux biens immobiliers.

minimum_service_ready_fields:
  - field_name: type_assurance
    required: true
    values:
      - assurance_habitation
      - assurance_proprietaire
      - assurance_copropriete
      - assurance_dommage_ouvrage
      - assurance_pret
      - assurance_multirisque
      - assurance_chantier
  - field_name: bien_concerne
    required: true
  - field_name: valeur_bien
    required: true
  - field_name: description_risques
    required: true
  - field_name: duree_souhaitee
    required: true
  - field_name: franchise_souhaitee
    required: false
  - field_name: garanties_souhaitees
    required: true
  - field_name: date_effet
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: specialite_assurance
    required: true
    values:
      - assurance_immobiliere
      - assurance_construction
      - assurance_copropriete
      - assurance_pret
      - multirisque_professionnelle
  - field_name: compagnies_representees
    required: true
  - field_name: agrement_ORIAS
    required: true
  - field_name: experience_annees
    required: true
  - field_name: taux_moyen_prime
    required: false
  - field_name: service_sinistre
    required: false
  - field_name: references_clients
    required: true
  - field_name: delai_etude_dossier
    required: true
  - field_name: honoraires_courtage
    required: true

minimum_quote_ready_fields:
  - field_name: mandat_recherche
    required: true
    type: document
  - field_name: questionnaire_risques
    required: true
    type: document
  - field_name: donnees_bien
    required: true
    type: document
  - field_name: historique_sinistres
    required: false
    type: document
  - field_name: offres_compagnies
    required: true
    type: array
  - field_name: comparatif_garanties
    required: true
    type: document
  - field_name: proposition_retenue
    required: true
    type: document
  - field_name: conditions_souscription
    required: true
    type: contract
  - field_name: honoraires_convenus
    required: true
    type: float

minimum_execution_ready_fields:
  - field_name: mandat_signe
    required: true
    type: document
  - field_name: questionnaire_rempli
    required: true
    type: boolean
  - field_name: comparatif_transmis
    required: true
    type: boolean
  - field_name: contrat_souscrit
    required: true
    type: boolean
  - field_name: attestation_delivree
    required: true
    type: document
  - field_name: paiement_prime
    required: true
    type: boolean
  - field_name: archive_contrat
    required: true
    type: boolean
  - field_name: suivi_annuel
    required: false
    type: boolean
```

---
## 21. conseil_juridique
```yaml
service_id: SVC-CONS-021
canonical_name: conseil_juridique
display_name: "Legal Advice"

description: >
  Service de conseil juridique en droit immobilier pour l'accompagnement dans les transactions, les baux, la copropriete et le foncier.

minimum_service_ready_fields:
  - field_name: domaine_conseil
    required: true
    values:
      - droit_immobilier
      - droit_foncier
      - droit_copropriete
      - droit_bail
      - droit_construction
      - droit_urbanisme
      - droit_fiscal_immobilier
      - contentieux_immobilier
  - field_name: objet_conseil
    required: true
    type: text
  - field_name: documents_juridiques
    required: false
    type: array
  - field_name: stade_dossier
    required: true
    values:
      - preliminaire
      - en_cours
      - contentieux
      - execution
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true

minimum_provider_matching_ready_fields:
  - field_name: specialite_juridique
    required: true
  - field_name: qualification_juriste
    required: true
    values:
      - avocat_specialise
      - juriste_immobilier
      - notaire_conseil
      - conseiller_juridique
  - field_name: barreau_inscription
    required: false
  - field_name: experience_annees
    required: true
  - field_name: assurance_rc_pro
    required: true
  - field_name: references_dossiers
    required: true
  - field_name: tarif_consultation
    required: true
  - field_name: delai_reponse
    required: true
  - field_name: langues_maitrisees
    required: false

minimum_quote_ready_fields:
  - field_name: contrat_conseil
    required: true
    type: document
  - field_name: lettre_mission
    required: true
    type: document
  - field_name: documents_examiner
    required: true
    type: array
  - field_name: questions_juridiques
    required: true
    type: array
  - field_name: honoraires_convenus
    required: true
    type: object
    sub_fields:
      - field_name: mode
        values:
          - forfait
          - horaire
          - resultat
          - abonnement
      - field_name: montant
        type: float
  - field_name: planning_consultation
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: mission_acceptee
    required: true
    type: boolean
  - field_name: documents_examines
    required: true
    type: boolean
  - field_name: consultation_delivree
    required: true
    type: boolean
  - field_name: note_conseil_transmise
    required: true
    type: document
  - field_name: honoraires_percus
    required: true
    type: boolean
  - field_name: suivi_dossier
    required: false
    type: boolean
  - field_name: satisfaction_client
    required: false
    type: boolean
```

---
## 22. conseil_fiscal
```yaml
service_id: SVC-CONS-022
canonical_name: conseil_fiscal
display_name: "Tax Advice"

description: >
  Service de conseil fiscal pour l'optimisation de la fiscalite immobiliere, les declarations et la planification patrimoniale.

minimum_service_ready_fields:
  - field_name: objet_conseil_fiscal
    required: true
    values:
      - fiscalite_acquisition
      - fiscalite_vente
      - fiscalite_locative
      - fiscalite_plus_value
      - fiscalite_succession
      - fiscalite_copropriete
      - optimisation_patrimoniale
      - declaration_fiscale
      - tva_immobiliere
  - field_name: situation_fiscale
    required: true
  - field_name: type_bien
    required: true
  - field_name: montant_transaction
    required: false
  - field_name: regime_fiscal
    required: false
  - field_name: documents_disponibles
    required: false
  - field_name: date_besoin
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: specialite_fiscale
    required: true
    values:
      - fiscalite_immobiliere
      - fiscalite_patrimoniale
      - fiscalite_entreprise
      - fiscalite_internationale
      - TVA_immobiliere
  - field_name: qualification_conseiller
    required: true
    values:
      - expert_comptable
      - avocat_fiscaliste
      - conseiller_fiscal
      - notaire_fiscaliste
      - inspecteur_fiscal
  - field_name: experience_fiscale_annees
    required: true
  - field_name: assurance_rc_pro
    required: true
  - field_name: references_dossiers
    required: true
  - field_name: tarif_consultation_horaire
    required: true
  - field_name: connaissance_legislation
    required: true
    values:
      - locale
      - nationale
      - ohada
      - internationale
  - field_name: langues
    required: false
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: contrat_conseil_fiscal
    required: true
    type: document
  - field_name: lettre_mission_fiscale
    required: true
    type: document
  - field_name: situation_fiscale_details
    required: true
    type: document
  - field_name: documents_a_examiner
    required: true
    type: array
  - field_name: honoraires_convenus
    required: true
    type: object
  - field_name: planning_prestations
    required: true
    type: schedule
  - field_name: confidentialite_engagement
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: mission_engagee
    required: true
    type: boolean
  - field_name: analyse_effectuee
    required: true
    type: boolean
  - field_name: note_conseil_fiscale
    required: true
    type: document
  - field_name: declaration_effectuee
    required: false
    type: boolean
  - field_name: optimisation_proposee
    required: true
    type: boolean
  - field_name: honoraires_percus
    required: true
    type: boolean
  - field_name: suivi_fiscal
    required: false
    type: boolean
  - field_name: archive_dossier
    required: true
    type: boolean
```

---
## 23. gestion_copropriete
```yaml
service_id: SVC-GEST-023
canonical_name: gestion_copropriete
display_name: "Condo Management"

description: >
  Service de gestion de copropriete incluant l'administration de l'immeuble, la comptabilite, l'organisation des AG et l'entretien des parties communes.

minimum_service_ready_fields:
  - field_name: localisation
    required: true
  - field_name: description_copropriete
    required: true
  - field_name: nombre_lots
    required: true
  - field_name: nombre_batiments
    required: false
  - field_name: type_gestion
    required: true
    values:
      - gestion_complete
      - gestion_comptable
      - gestion_technique
      - gestion_syndic
      - assistance_syndic_benevole
  - field_name: reglement_copropriete
    required: false
    type: boolean
  - field_name: budget_annuel_charges
    required: false
  - field_name: fonds_travaux_existant
    required: false
  - field_name: equipe_concierge
    required: false
  - field_name: date_debut_souhaitee
    required: true
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: localisation
    required: true
  - field_name: taille_copropriete_maitrisee
    required: true
    values:
      - petite_moins_10
      - moyenne_10_50
      - grande_50_200
      - tres_grande_plus_200
  - field_name: nombre_coproprietes_gerées
    required: true
    type: integer
  - field_name: equipe_gestion
    required: true
    type: integer
  - field_name: logiciel_gestion
    required: false
  - field_name: assurance_professionnelle
    required: true
  - field_name: garantie_financiere
    required: true
  - field_name: experience_syndic_annees
    required: true
  - field_name: references_coproprietes
    required: true
  - field_name: honoraires_syndic
    required: true
  - field_name: taux_recouvrement_moyen
    required: false
  - field_name: services_inclus
    required: false
    values:
      - comptabilite
      - convocation_AG
      - suivi_travaux
      - recouvrement
      - relation_fournisseurs

minimum_quote_ready_fields:
  - field_name: contrat_syndic
    required: true
    type: document
  - field_name: reglement_copropriete
    required: true
    type: document
  - field_name: etat_descriptif_division
    required: true
    type: document
  - field_name: carnet_entretien
    required: true
    type: document
  - field_name: budget_previsionnel
    required: true
    type: document
  - field_name: honoraires_gestion
    required: true
    type: object
  - field_name: conditions_resiliation
    required: true
    type: text
  - field_name: calendrier_assemblees
    required: true
    type: schedule
  - field_name: assurances_immeuble
    required: true
    type: array
  - field_name: conditions_paiement
    required: true
    type: contract

minimum_execution_ready_fields:
  - field_name: contrat_signe
    required: true
    type: document
  - field_name: reglement_recupere
    required: true
    type: boolean
  - field_name: budget_etabli
    required: true
    type: boolean
  - field_name: assemblee_tenue
    required: true
    type: boolean
  - field_name: comptabilite_en_place
    required: true
    type: boolean
  - field_name: fournisseurs_contractualises
    required: true
    type: boolean
  - field_name: recouvrement_engage
    required: true
    type: boolean
  - field_name: fonds_travaux_constitué
    required: false
    type: boolean
  - field_name: reporting_en_place
    required: true
    type: boolean
  - field_name: archive_documents
    required: true
    type: boolean
```

---
## 24. recouvrement_locatif
```yaml
service_id: SVC-RECO-024
canonical_name: recouvrement_locatif
display_name: "Rent Collection"

description: >
  Service de recouvrement de loyers impayes et de gestion contentieuse des impayes locatifs pour le compte de proprietaires bailleurs.

minimum_service_ready_fields:
  - field_name: localisation_bien
    required: true
  - field_name: montant_impaye
    required: true
  - field_name: duree_impaye
    required: true
  - field_name: type_bien
    required: true
  - field_name: identite_locataire
    required: false
    pii: true
  - field_name: contrat_bail
    required: true
  - field_name: historique_paiements
    required: true
  - field_name: depot_garantie_montant
    required: false
  - field_name: etat_des_lieux
    required: false
  - field_name: assurances_souscrites
    required: false
  - field_name: etapes_engagees
    required: false
    values:
      - relance_amiable
      - mise_en_demeure
      - commandement_payer
      - procedure_judiciaire
      - expulsion
  - field_name: urgence
    required: true

minimum_provider_matching_ready_fields:
  - field_name: specialite_recouvrement
    required: true
    values:
      - recouvrement_amiable
      - recouvrement_contentieux
      - recouvrement_judiciaire
      - gestion_impayes_locatifs
      - recouvrement_charges_copropriete
  - field_name: qualification
    required: true
    values:
      - huissier
      - avocat
      - societe_recouvrement
      - administrateur_biens
      - syndic
  - field_name: experience_recouvrement
    required: true
  - field_name: taux_recouvrement
    required: false
    type: float
  - field_name: assurance_professionnelle
    required: true
  - field_name: references_bailleurs
    required: true
  - field_name: honoraires_recouvrement
    required: true
    values:
      - pourcentage_percu
      - forfait_dossier
      - honoraire_resultat
      - mixte
  - field_name: delai_moyen_recouvrement
    required: false
  - field_name: partenariat_avocat
    required: false
  - field_name: disponibilite
    required: true

minimum_quote_ready_fields:
  - field_name: mandat_recouvrement
    required: true
    type: document
  - field_name: contrat_bail
    required: true
    type: document
  - field_name: historique_impayes
    required: true
    type: document
  - field_name: quittances_loyer
    required: false
    type: array
  - field_name: identite_debitrice
    required: true
    type: document
  - field_name: honoraires_convenus
    required: true
    type: object
  - field_name: strategie_recouvrement
    required: true
    type: text
  - field_name: calendrier_actions
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: clause_confidentialite
    required: true
    type: boolean

minimum_execution_ready_fields:
  - field_name: mandat_signe
    required: true
    type: document
  - field_name: dossier_constitué
    required: true
    type: boolean
  - field_name: relance_amiable_effectuee
    required: true
    type: boolean
  - field_name: mise_en_demeure_envoyee
    required: false
    type: boolean
  - field_name: procedure_engagee
    required: false
    type: boolean
  - field_name: paiement_recouvre
    required: true
    type: boolean
  - field_name: fonds_verses_bailleur
    required: true
    type: boolean
  - field_name: honoraires_preleves
    required: true
    type: boolean
  - field_name: archive_dossier
    required: true
    type: boolean
  - field_name: clôture_dossier
    required: true
    type: boolean
```

---
