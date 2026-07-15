# Professional Service Matrices

> **Request Family:** PROFESSIONAL_SEARCH
> **Transaction Type:** FIND
> **Version:** 1.0.0

---

## Table of Contents

1. [agent_immobilier](#1-agent_immobilier)
2. [agence_immobiliere](#2-agence_immobiliere)
3. [notaire](#3-notaire)
4. [geometre](#4-geometre)
5. [architecte](#5-architecte)
6. [ingenieur_genie_civil](#6-ingenieur_genie_civil)
7. [technicien_batiment](#7-technicien_batiment)
8. [macon](#8-macon)
9. [electricien](#9-electricien)
10. [plombier](#10-plombier)
11. [menuisier](#11-menuisier)
12. [peintre](#12-peintre)
13. [carreleur](#13-carreleur)
14. [couvreur](#14-couvreur)
15. [expert_immobilier](#15-expert_immobilier)
16. [evaluateur](#16-evaluateur)
17. [gestionnaire_immobilier](#17-gestionnaire_immobilier)
18. [syndic](#18-syndic)
19. [photographe_immobilier](#19-photographe_immobilier)
20. [videaste_drone](#20-videaste_drone)
21. [demenageur](#21-demenageur)
22. [entreprise_nettoyage](#22-entreprise_nettoyage)
23. [gardiennage](#23-gardiennage)
24. [assureur](#24-assureur)
25. [banque_microfinance](#25-banque_microfinance)
26. [courtier](#26-courtier)
27. [prestataire_administratif](#27-prestataire_administratif)

---

## Common Base Fields (All Professionals)

```yaml
common_base_fields:
  - field_name: type_prestation
    type: enum
    required: true
    description: Type of service requested from the professional
    values:
      - recherche_professionnel
      - mise_en_relation
      - devis_multiple
      - consultation
      - urgence

  - field_name: localisation
    type: object
    required: true
    description: Geographic location of the service need
    sub_fields:
      - field_name: ville
        type: string
        required: true
      - field_name: quartier
        type: string
        required: false
      - field_name: commune
        type: string
        required: false
      - field_name: departement
        type: string
        required: false
      - field_name: region
        type: string
        required: false
      - field_name: pays
        type: string
        required: true
      - field_name: code_postal
        type: string
        required: false
      - field_name: latitude
        type: float
        required: false
      - field_name: longitude
        type: float
        required: false
      - field_name: rayon_recherche_km
        type: integer
        required: false
        description: Search radius around the specified location

  - field_name: description_besoin
    type: text
    required: true
    description: Detailed description of the client's need
    max_length: 2000
    min_length: 20

  - field_name: urgence
    type: enum
    required: true
    description: Urgency level of the request
    values:
      - immediate
      - urgent_48h
      - cette_semaine
      - ce_mois
      - pas_urgent
      - planification

  - field_name: budget_fourchette
    type: object
    required: false
    description: Budget range for the service
    sub_fields:
      - field_name: devise
        type: string
        required: true
        default: XOF
      - field_name: minimum
        type: float
        required: true
      - field_name: maximum
        type: float
        required: true
      - field_name: negotiable
        type: boolean
        required: false
        default: true

  - field_name: date_souhaitee
    type: date
    required: true
    description: Desired date for service commencement or completion

  - field_name: type_bien_concerne
    type: enum
    required: false
    description: Type of property related to the service
    values:
      - appartement
      - maison
      - villa
      - terrain
      - immeuble
      - local_commercial
      - bureau
      - entrepot
      - hangar
      - ferme
      - plantation
      - copropriete
      - lotissement
      - patrimoine
      - monument
      - bien_industriel
      - hotel
      - residence_touristique
      - parking
      - autre

  - field_name: etendue_mission
    type: text
    required: false
    description: Scope of the mission or project

  - field_name: livrable_attendu
    type: array
    required: false
    description: Expected deliverables
    items:
      - rapport
      - devis
      - plan
      - certificat
      - attestation
      - contrat
      - facture
      - photographies
      - video
      - inspection_report
      - expertise_report
      - estimation
      - autre

  - field_name: qualification_agrement
    type: array
    required: false
    description: Required qualifications or certifications
    items:
      - agrement_professionnel
      - numero_contribuable
      - registre_commerce
      - assurance_pro
      - ordre_professionnel
      - certification_qualite
      - agrement_ministeriel
      - habilitation_specifique

  - field_name: experience_souhaitee
    type: integer
    required: false
    description: Minimum years of professional experience desired
    minimum: 0
    maximum: 50

  - field_name: disponibilite
    type: object
    required: false
    description: Availability schedule
    sub_fields:
      - field_name: jours_semaine
        type: array
        required: false
        items:
          - lundi
          - mardi
          - mercredi
          - jeudi
          - vendredi
          - samedi
          - dimanche
      - field_name: heures_ouvrables
        type: string
        required: false
      - field_name: intervention_weekend
        type: boolean
        required: false
        default: false
      - field_name: intervention_nuit
        type: boolean
        required: false
        default: false

  - field_name: langue
    type: array
    required: false
    description: Preferred languages
    items:
      - francais
      - anglais
      - arabe
      - bambara
      - dioula
      - peulh
      - soninke
      - senoufo
      - malinke
      - minianka
      - bete
      - baoule
      - agni
      - ewe
      - fon
      - yoruba
      - haoussa
      - wolof
      - serere
      - mandingue
      - soussou
      - kissi
      - swahili
      - portugais
      - espagnol
      - allemand

  - field_name: canal_contact
    type: array
    required: false
    description: Preferred contact channels
    items:
      - telephone
      - email
      - whatsapp
      - telegram
      - sms
      - plateforme_web
      - rendezvous_physique
      - visioconference
```

---
## 1. agent_immobilier
```yaml
matrix_id: PRO-AGENT-001
canonical_name: agent_immobilier
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un agent immobilier pour accompagner un client dans l'achat, la vente ou la location d'un bien immobilier.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_prestation
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_mandat
    required: true
    values:
      - mandat_vente
      - mandat_location
      - mandat_recherche
      - mandat_estimation

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: rayon_action
    weight: 0.25
  - field_name: specialite_bien
    weight: 0.20
  - field_name: experience_annees
    weight: 0.15

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: presentation
    required: true
  - field_name: tarifs_honoraires
    required: true
  - field_name: secteur_couverture
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: mandat_signe
    required: true
    type: document
  - field_name: assurance_professionnelle
    required: true
    type: document

recommended_fields:
  - field_name: avis_clients
  - field_name: portfolio_transactions
  - field_name: site_web

optional_fields:
  - field_name: partenaires_reseau
  - field_name: horaires_agence
  - field_name: equipement_vehicule
  - field_name: nombre_collaborateurs

conditional_fields:
  - field_name: carte_professionnelle
    condition: statut_exercice == titulaire_carte_pro
    type: document

sensitive_fields:
  - field_name: numero_carte_professionnelle
    pii: true
    sensitivity: high
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: situation_fiscale
    pii: true
    sensitivity: high
```

---
## 2. agence_immobiliere
```yaml
matrix_id: PRO-AGENC-002
canonical_name: agence_immobiliere
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'une agence immobiliere etablie disposant d'une structure physique et d'une equipe.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_prestation
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: taille_agence
    required: true
    values:
      - petite_moins_5
      - moyenne_5_20
      - grande_20_plus
      - reseau_national
      - franchise
  - field_name: specialites
    required: true
    values:
      - transaction
      - location
      - gestion_locative
      - syndic
      - expertise
      - estimation
      - promotion_immobiliere
      - multi_service

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_correspondance
    weight: 0.25
  - field_name: reputation_agence
    weight: 0.15
  - field_name: volume_annuel_transactions
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: raison_sociale
    required: true
  - field_name: siege_social
    required: true
  - field_name: portfolio_biens
    required: false

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_service
    required: true
    type: document
  - field_name: attestation_assurance
    required: true
    type: document
  - field_name: registre_commerce
    required: true
    type: document

recommended_fields:
  - field_name: site_web_agence
  - field_name: annuaire_biens
  - field_name: service_apres_vente
  - field_name: garanties_proposees

optional_fields:
  - field_name: nombre_succursales
  - field_name: pays_implantation
  - field_name: langues_equipe
  - field_name: service_juridique_interne
  - field_name: partenariat_assurance

conditional_fields:
  - field_name: franchise
    condition: taille_agence == franchise
    type: string
  - field_name: numero_carte_pro
    condition: agrements != sans_carte
    type: string

sensitive_fields:
  - field_name: registre_commerce_numero
    pii: true
    sensitivity: high
  - field_name: numero_contribuable
    pii: true
    sensitivity: high
  - field_name: identite_gerant
    pii: true
    sensitivity: high
  - field_name: bilan_financier
    pii: true
    sensitivity: high
```

---
## 3. notaire
```yaml
matrix_id: PRO-NOTAI-003
canonical_name: notaire
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un notaire pour l'authentification d'actes, la redaction de contrats immobiliers et les transactions foncieres.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: nature_operation
    required: true
  - field_name: type_bien
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: nature_operation
    required: true
  - field_name: stade_dossier
    required: true
    values:
      - preliminaire
      - compromis_signe
      - avant_contrat
      - acte_preparation
      - signature_imminente
      - post_signature
      - litige
  - field_name: specialite
    required: true
    values:
      - droit_immobilier
      - droit_foncier
      - droit_famille
      - droit_societe
      - generaliste

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: competence_territoriale
    weight: 0.25
  - field_name: specialite_juridique
    weight: 0.20
  - field_name: honoraires_estimes
    weight: 0.10
  - field_name: delai_traitement
    weight: 0.10
  - field_name: reputation
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: etude_notariale
    required: true
  - field_name: identite_notaire
    required: true
  - field_name: contact_etude
    required: true
  - field_name: horaires_audience
    required: true
  - field_name: tarifs_honoraires
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: pieces_identite_parties
    required: true
    type: document
  - field_name: titre_propriete
    required: true
    type: document
  - field_name: documents_fonciers
    required: true
    type: document
  - field_name: frais_notariaux
    required: true
    type: contract
  - field_name: calendrier_signature
    required: true
    type: schedule

recommended_fields:
  - field_name: service_consultation_en_ligne
  - field_name: repertoire_clientele
  - field_name: accompagnement_pret

optional_fields:
  - field_name: nombre_clercs
  - field_name: parking_client
  - field_name: accessibilite_pmr
  - field_name: permanence_samedi
  - field_name: visioconference

conditional_fields:
  - field_name: collaboration_avocat
    condition: nature_operation == litige
    type: boolean
  - field_name: expertise_comptable
    condition: nature_operation == succession || nature_operation == liquidation
    type: boolean

sensitive_fields:
  - field_name: identite_complete_parties
    pii: true
    sensitivity: high
  - field_name: montant_transaction
    pii: true
    sensitivity: high
  - field_name: clauses_contractuelles
    pii: true
    sensitivity: high
  - field_name: donnees_fiscales
    pii: true
    sensitivity: high
  - field_name: situation_matrimoniale
    pii: true
    sensitivity: high
  - field_name: numero_titre_foncier
    pii: true
    sensitivity: high
```

---
## 4. geometre
```yaml
matrix_id: PRO-GEOME-004
canonical_name: geometre
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un geometre expert foncier pour le bornage, lotissement, topographie et plans fonciers.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: nature_prestation
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: nature_terrain
    required: true
    values:
      - urbain
      - periurbain
      - rural
      - agricole
      - forestier
      - industriel
      - littoral
      - montagneux
  - field_name: surface_estimee
    required: true
    type: range
  - field_name: objectif_mission
    required: true
    values:
      - construction
      - vente
      - donation
      - succession
      - litige_voisinage
      - investissement
      - amenagement
      - projet_agricole

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_terrain
    weight: 0.25
  - field_name: experience_annees
    weight: 0.15
  - field_name: equipement_disponible
    weight: 0.10
  - field_name: certification_ordre
    weight: 0.15

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: identite_geometre
    required: true
  - field_name: cabine_etude
    required: true
  - field_name: numero_ordre
    required: true
  - field_name: assurance_professionnelle
    required: true
  - field_name: references_projets
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_prestation
    required: true
    type: document
  - field_name: titre_foncier
    required: true
    type: document
  - field_name: convention_honoraires
    required: true
    type: document
  - field_name: planning_intervention
    required: true
    type: schedule
  - field_name: acces_terrain
    required: true
    type: document

recommended_fields:
  - field_name: materiel_disponible
  - field_name: equipe_techniciens
  - field_name: zone_couverture_max
  - field_name: certifications_supplementaires

optional_fields:
  - field_name: logiciels_utilises
  - field_name: partenariat_notaire
  - field_name: service_archivage_plans
  - field_name: formation_continue

conditional_fields:
  - field_name: litige_en_cours
    condition: objectif_mission == litige_voisinage
    type: boolean
  - field_name: certificat_urbanisme
    condition: objectif_mission == construction
    type: document

sensitive_fields:
  - field_name: plan_propriete
    pii: true
    sensitivity: high
  - field_name: identification_proprietaire
    pii: true
    sensitivity: high
  - field_name: donnees_cadastrales
    pii: false
    sensitivity: medium
```

---
## 5. architecte
```yaml
matrix_id: PRO-ARCHI-005
canonical_name: architecte
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un architecte pour la conception, les plans, le permis de construire et la direction des travaux.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_projet
    required: true
  - field_name: surface
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_projet
    required: true
  - field_name: budget_travaux
    required: true
    type: range
  - field_name: budget_etudes
    required: false
    type: range
  - field_name: niveau_attendu
    required: true
    values:
      - esquisse
      - avant_projet_sommaire
      - avant_projet_definitif
      - dossier_permis_construire
      - projet_execution
      - direction_travaux
      - assistance_chantier
      - suivi_complet_operation
  - field_name: style_architectural
    required: false
    values:
      - moderne_contemporain
      - traditionnel
      - colonial
      - africain_moderne
      - minimaliste
      - industriel
      - bioclimatique_ecologique
      - rustique
      - luxe_prestige
      - tropical
      - libre

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_projet
    weight: 0.25
  - field_name: portfolio_realisations
    weight: 0.15
  - field_name: experience_annees
    weight: 0.10
  - field_name: inscription_ordre
    weight: 0.10
  - field_name: honoraires_estimes
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: identite_architecte
    required: true
  - field_name: agence_architecture
    required: true
  - field_name: portfolio
    required: true
  - field_name: numero_ordre
    required: true
  - field_name: assurance_rc_pro
    required: true
  - field_name: honoraires_pratiques
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_maitrise_oeuvre
    required: true
    type: document
  - field_name: programme_architectural
    required: true
    type: document
  - field_name: calendrier_prestations
    required: true
    type: schedule
  - field_name: conditions_financieres
    required: true
    type: contract
  - field_name: assurance_dommage_ouvrage
    required: true
    type: document

recommended_fields:
  - field_name: realisations_similaires
  - field_name: prix_concours
  - field_name: logiciels_mao_utilises
  - field_name: demarche_developpement_durable

optional_fields:
  - field_name: nombre_niveaux_projet
  - field_name: terrain_disponible_existant
  - field_name: documents_existants
  - field_name: contraintes_urbanisme
  - field_name: orientation_souhaitee
  - field_name: materiau_principal
  - field_name: performance_energetique_visee

conditional_fields:
  - field_name: permis_construire_depose
    condition: niveau_attendu == dossier_permis_construire || niveau_attendu == projet_execution || niveau_attendu == direction_travaux || niveau_attendu == suivi_complet_operation
    type: boolean
  - field_name: terrain_disponible
    condition: type_projet == construction_neuve || type_projet == lotissement_amenagement
    type: boolean

sensitive_fields:
  - field_name: plan_masse_projet
    pii: false
    sensitivity: medium
  - field_name: donnees_parcellaires
    pii: true
    sensitivity: high
  - field_name: identite_maitre_ouvrage
    pii: true
    sensitivity: high
  - field_name: budget_previsionnel_detail
    pii: true
    sensitivity: high
```

---
## 6. ingenieur_genie_civil
```yaml
matrix_id: PRO-INGEN-006
canonical_name: ingenieur_genie_civil
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un ingenieur en genie civil pour les etudes structurelles, le dimensionnement et le suivi technique de chantiers.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_mission
    required: true
  - field_name: description_projet
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_mission
    required: true
  - field_name: specialite_technique
    required: true
    values:
      - beton_arme
      - charpente_metallique
      - charpente_bois
      - structure_maconnerie
      - fondations_speciales
      - geotechnique
      - voirie_reseaux
      - hydraulique
      - thermique_acoustique
      - fluides_energie
      - structure_mixte
      - genie_parasismique
  - field_name: taille_projet
    required: true
    values:
      - petite_moins_200m2
      - moyenne_200_1000m2
      - grande_1000_5000m2
      - tres_grande_plus_5000m2

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_mission
    weight: 0.30
  - field_name: experience_similaire
    weight: 0.20
  - field_name: qualifications_techniques
    weight: 0.15
  - field_name: assurance_rc_decennale
    weight: 0.10
  - field_name: logiciels_maitrises
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: structure_professionnelle
    required: true
  - field_name: contacts_techniques
    required: true
  - field_name: references_projets
    required: true
  - field_name: assurance_decennale
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_prestation_ingenierie
    required: true
    type: document
  - field_name: cahier_charges_technique
    required: true
    type: document
  - field_name: plan_calendrier
    required: true
    type: schedule
  - field_name: budget_etudes_convenu
    required: true
    type: contract
  - field_name: attestation_assurance
    required: true
    type: document

recommended_fields:
  - field_name: publications_techniques
  - field_name: normes_maitrisees
  - field_name: partenaires_bureaux_etudes
  - field_name: certification_iso

optional_fields:
  - field_name: nombre_ingenieurs_equipe
  - field_name: logiciels_cao_bim
  - field_name: materiel_essais_in-situ
  - field_name: laboratoire_interne
  - field_name: zone_intervention_regionale

conditional_fields:
  - field_name: controle_technique_obligatoire
    condition: surface_batie > 500
    type: boolean
  - field_name: mission_sismique
    condition: zone_sismique == oui
    type: boolean
  - field_name: coordination_ssi
    condition: type_bien_concerne == immeuble || type_bien_concerne == hotel
    type: boolean

sensitive_fields:
  - field_name: notes_calculs_structure
    pii: false
    sensitivity: medium
  - field_name: plans_techniques
    pii: false
    sensitivity: medium
  - field_name: budget_travaux_estime
    pii: true
    sensitivity: high
  - field_name: identification_maitre_ouvrage
    pii: true
    sensitivity: high
```

---
## 7. technicien_batiment
```yaml
matrix_id: PRO-TECHN-007
canonical_name: technicien_batiment
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un technicien du batiment pour les diagnostics techniques, inspections et evaluations.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_mission_technique
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_mission_technique
    required: true
  - field_name: qualification_diagnostiqueur
    required: true
    values:
      - certifie_amiante
      - certifie_dpe
      - certifie_plomb
      - certifie_electrique
      - certifie_gaz
      - certifie_termite
      - certifie_multidiagnostic
      - technicien_batiment_general
      - inspecteur_batiment
      - assistant_maitrise_ouvrage
  - field_name: anciennete_bien
    required: false
    values:
      - moins_10_ans
      - 10_30_ans
      - 30_50_ans
      - plus_50_ans

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: certification_mission
    weight: 0.25
  - field_name: experience_diagnostics
    weight: 0.15
  - field_name: equipement_mesure
    weight: 0.10
  - field_name: assurance_rc_pro
    weight: 0.10
  - field_name: delai_rendu_rapport
    weight: 0.10
  - field_name: tarif_prestation
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: certifications_detenues
    required: true
  - field_name: references_diagnostics
    required: true
  - field_name: assurance_professionnelle
    required: true
  - field_name: zones_intervention
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_prestation_technique
    required: true
    type: document
  - field_name: acces_bien
    required: true
    type: document
  - field_name: calendrier_visite
    required: true
    type: schedule
  - field_name: conditions_tarifaires
    required: true
    type: contract
  - field_name: autorisation_proprietaire
    required: true
    type: document

recommended_fields:
  - field_name: logiciels_diagnostic
  - field_name: materiel_mesure_specifique
  - field_name: formation_continue_suivie
  - field_name: adhesion_organisme_qualite

optional_fields:
  - field_name: nombre_techniciens_equipe
  - field_name: vehicule_societe
  - field_name: disponibilite_weekend
  - field_name: rapport_digital_interactif

conditional_fields:
  - field_name: diagnostic_amiante_obligatoire
    condition: anciennete_bien == plus_50_ans || anciennete_bien == 30_50_ans
    type: boolean
  - field_name: crepis_obligatoire
    condition: type_mission_technique == diagnostic_plomb
    type: boolean

sensitive_fields:
  - field_name: rapport_diagnostic_complet
    pii: false
    sensitivity: medium
  - field_name: identification_proprietaire
    pii: true
    sensitivity: high
  - field_name: adresse_exacte_bien
    pii: true
    sensitivity: high
```

---
## 8. macon
```yaml
matrix_id: PRO-MACON-008
canonical_name: macon
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un macon pour le gros oeuvre, fondations, elevation de murs, dallage et ravalement.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: corps_metier
    required: true
  - field_name: description_travaux
    required: true
  - field_name: surface_concernee
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: corps_metier
    required: true
  - field_name: type_chantier
    required: true
    values:
      - construction_neuve
      - renovation_totale
      - renovation_partielle
      - extension
      - reparation_urgence
      - finition
  - field_name: budget
    required: true
  - field_name: delai
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_travaux
    weight: 0.25
  - field_name: assurance_decennale
    weight: 0.15
  - field_name: references_chantiers
    weight: 0.10
  - field_name: equipe_disponible
    weight: 0.10
  - field_name: tarif_m2
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: reference_chantiers
    required: true
  - field_name: assurance_decennale
    required: true
  - field_name: registre_commerce
    required: true
  - field_name: numero_contribuable
    required: true
  - field_name: equipe_disponible
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: devis_signe
    required: true
    type: document
  - field_name: contrat_travaux
    required: true
    type: document
  - field_name: planning_chantier
    required: true
    type: schedule
  - field_name: acces_chantier
    required: true
  - field_name: autorisation_travaux
    required: true
    type: document
  - field_name: etat_lieux_initial
    required: true
    type: document

recommended_fields:
  - field_name: photos_realisations
  - field_name: garantie_decennale_attestation
  - field_name: nombre_ouvriers
  - field_name: parc_materiel

optional_fields:
  - field_name: materiel_engins_disponibles
  - field_name: fourniture_materiaux_incluse
  - field_name: prestation_etude_incluse
  - field_name: nettoyage_chantier_inclus

conditional_fields:
  - field_name: permis_construire
    condition: type_chantier == construction_neuve || type_chantier == extension
    type: document
  - field_name: declaration_travaux
    condition: surface_concernee > 20
    type: document

sensitive_fields:
  - field_name: conditions_paiement_detail
    pii: true
    sensitivity: high
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: identite_client
    pii: true
    sensitivity: high
  - field_name: adresse_chantier
    pii: true
    sensitivity: medium
```

---
## 9. electricien
```yaml
matrix_id: PRO-ELECT-009
canonical_name: electricien
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un electricien pour l'installation, maintenance, renovation et depannage electrique.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: corps_metier
    required: true
  - field_name: description_travaux
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_travaux
    required: true
    values:
      - installation_complete
      - renovation_reseau
      - mise_aux_normes
      - depannage
      - extension_reseau
      - installation_domotique
      - installation_photovoltaique
      - installation_climatisation
      - installation_alarme
      - diagnostic_electrique
      - tableau_electrique
      - mise_terre_installation
  - field_name: qualification_requise
    required: true
    values:
      - qualifelec
      - consuel_habilité
      - agrement_enedis
      - certification_photovoltaique
      - habilitation_electrique
      - sans_qualification_specifique
  - field_name: budget
    required: true
  - field_name: delai
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_electrique
    weight: 0.25
  - field_name: habilitation_electrique
    weight: 0.15
  - field_name: assurance_professionnelle
    weight: 0.10
  - field_name: garantie_travaux
    weight: 0.10
  - field_name: disponibilite_urgence
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: contact_technique
    required: true
  - field_name: certification_qualification
    required: true
  - field_name: assurance_rc_pro
    required: true
  - field_name: references_travaux
    required: true
  - field_name: zones_intervention
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: devis_signe
    required: true
    type: document
  - field_name: schema_electrique_conforme
    required: true
    type: document
  - field_name: planning_intervention
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: attestation_conformite
    required: true
    type: document

recommended_fields:
  - field_name: materiel_utilise_marque
  - field_name: garantie_materiel_an
  - field_name: service_astreinte
  - field_name: devis_gratuit

optional_fields:
  - field_name: nombre_techniciens
  - field_name: vehicule_atelier
  - field_name: disponibilite_24h
  - field_name: intervention_urgence_tarif
  - field_name: partenariat_fournisseurs

conditional_fields:
  - field_name: consuel_obligatoire
    condition: type_travaux == installation_complete || type_travaux == renovation_reseau
    type: boolean
  - field_name: diagnostic_obligatoire
    condition: type_travaux == mise_aux_normes || type_travaux == renovation_reseau
    type: boolean

sensitive_fields:
  - field_name: plan_reseau_electrique
    pii: false
    sensitivity: high
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: identite_client
    pii: true
    sensitivity: high
  - field_name: code_alarme_securite
    pii: true
    sensitivity: high
```

---
## 10. plombier
```yaml
matrix_id: PRO-PLOMB-010
canonical_name: plombier
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un plombier pour l'installation, la reparation et la maintenance des reseaux d'eau et de chauffage.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: corps_metier
    required: true
  - field_name: description_travaux
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_travaux
    required: true
    values:
      - fuite_eau
      - debouchage_canalisation
      - installation_sanitaire
      - installation_chauffage
      - installation_chauffe_eau
      - installation_climatisation
      - renovation_plomberie
      - remplacement_ballon
      - installation_pompe_relevage
      - fosse_septique
      - depannage_urgence
  - field_name: qualification
    required: true
    values:
      - qualigaz
      - qualifelec_chauffage
      - agrement_installation_chauffage
      - certification_securite_gaz
      - sans_certification
  - field_name: budget
    required: true
  - field_name: delai
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_plomberie
    weight: 0.25
  - field_name: temps_reponse_urgence
    weight: 0.15
  - field_name: certification_qualification
    weight: 0.10
  - field_name: assurance_professionnelle
    weight: 0.10
  - field_name: garantie_travaux
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: contact_urgence
    required: true
  - field_name: qualifications
    required: true
  - field_name: assurance_pro
    required: true
  - field_name: references_travaux
    required: true
  - field_name: zone_intervention
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: devis_signe
    required: true
    type: document
  - field_name: diagnostic_etat_lieux
    required: true
    type: document
  - field_name: planning_intervention
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: garantie_pieces
    required: true
    type: document

recommended_fields:
  - field_name: garantie_main_oeuvre
  - field_name: service_astreinte_24h
  - field_name: devis_gratuit_sans_deplacement
  - field_name: vehicule_atelier

optional_fields:
  - field_name: stock_pieces_detachees
  - field_name: disponibilite_jour_ferie
  - field_name: intervention_nocturne
  - field_name: contrat_maintenance_propose

conditional_fields:
  - field_name: qualigaz_requis
    condition: type_travaux == installation_chauffage || type_travaux == installation_chauffe_eau || type_travaux == reseau_eau_chaude
    type: boolean

sensitive_fields:
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: identite_client
    pii: true
    sensitivity: high
  - field_name: plan_canalisation_bien
    pii: false
    sensitivity: medium
```

---
## 11. menuisier
```yaml
matrix_id: PRO-MENUI-011
canonical_name: menuisier
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un menuisier pour la fabrication et l'installation de meubles, menuiseries et agencements.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: corps_metier
    required: true
  - field_name: description_travaux
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_travaux
    required: true
    values:
      - fabrication_porte
      - fenetre_baie_vitree
      - escalier_main_courante
      - placard_dressing
      - cuisine_amenagee
      - agencement_sur_mesure
      - parquet_pose
      - terrasse_bois
      - veranda
      - porte_garage
      - cloture_bois
      - pergola
      - mobilier_sur_mesure
  - field_name: materiau
    required: true
    values:
      - bois_massif
      - bois_contreplaque
      - medium
      - stratifie
      - aluminium
      - pvc
      - mixte_bois_aluminium
      - metal
      - verre
      - composite
  - field_name: budget
    required: true
  - field_name: delai
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_metier
    weight: 0.25
  - field_name: materiau_maitrise
    weight: 0.15
  - field_name: portfolio_realisations
    weight: 0.15
  - field_name: assurance_professionnelle
    weight: 0.10
  - field_name: atelier_equipement
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: specialite_materiaux
    required: true
  - field_name: portfolio_photos
    required: true
  - field_name: assurance_pro
    required: true
  - field_name: registre_artisanat
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: devis_detail
    required: true
    type: document
  - field_name: plan_technique
    required: true
    type: document
  - field_name: planning_fabrication
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: garantie_ouvrage
    required: true
    type: document

recommended_fields:
  - field_name: echantillons_disponibles
  - field_name: showroom
  - field_name: service_pose_inclus
  - field_name: garantie_pose_5ans
  - field_name: conseil_personnalise

optional_fields:
  - field_name: finitions_proposees
  - field_name: quincaillerie_incluse
  - field_name: enlevement_ancien
  - field_name: traitement_bois
  - field_name: certification_bois_durable

conditional_fields:
  - field_name: prise_mesures_obligatoire
    condition: type_travaux == cuisine_amenagee || type_travaux == agencement_sur_mesure || type_travaux == veranda
    type: boolean

sensitive_fields:
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: identite_client
    pii: true
    sensitivity: high
  - field_name: plan_maison_interieur
    pii: false
    sensitivity: medium
  - field_name: adresse_intervention
    pii: true
    sensitivity: high
```

---
## 12. peintre
```yaml
matrix_id: PRO-PEINT-012
canonical_name: peintre
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un peintre pour la peinture interieure et exterieure, revetements muraux et finitions.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: corps_metier
    required: true
  - field_name: description_travaux
    required: true
  - field_name: surface_concernee
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_travaux
    required: true
    values:
      - peinture_murs_plafonds
      - peinture_exterieure
      - ravalement_facade
      - enduit_decoratif
      - revetement_mural_papier
      - revetement_mural_toile
      - peinture_boiseries
      - peinture_metal
      - lasure_bois_exterieur
      - peinture_sol
      - patine_decorative
      - fresque_murale
  - field_name: etat_actuel
    required: true
    values:
      - neuf
      - bon_etat
      - moyen
      - degrade
      - tres_degrade
  - field_name: budget
    required: true
  - field_name: delai
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_peinture
    weight: 0.25
  - field_name: references_chantiers
    weight: 0.15
  - field_name: garantie_travaux
    weight: 0.10
  - field_name: tarif_m2_moyen
    weight: 0.15
  - field_name: disponibilite
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: references_chantiers
    required: true
  - field_name: assurance_professionnelle
    required: true
  - field_name: portfolio_photos
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: devis_signe
    required: true
    type: document
  - field_name: nuancier_couleurs_choisi
    required: true
    type: document
  - field_name: preparation_surface_etat_lieux
    required: true
    type: document
  - field_name: planning_travaux
    required: true
    type: schedule
  - field_name: protection_mobilier
    required: true
    type: document

recommended_fields:
  - field_name: nuancier_disponible
  - field_name: devis_gratuit
  - field_name: garantie_decennale
  - field_name: produit_ecologique_disponible

optional_fields:
  - field_name: echantillon_couleur_gratuit
  - field_name: fourniture_peinture_incluse
  - field_name: sous_couche_incluse
  - field_name: protection_meubles_incluse
  - field_name: nettoyage_fin_chantier

conditional_fields:
  - field_name: traitement_moisissure
    condition: etat_actuel == degrade || etat_actuel == tres_degrade
    type: boolean
  - field_name: poncage_preparatoire
    condition: etat_actuel == moyen || etat_actuel == degrade
    type: boolean

sensitive_fields:
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: identite_client
    pii: true
    sensitivity: high
  - field_name: adresse_intervention
    pii: true
    sensitivity: high
  - field_name: budget_consacre
    pii: true
    sensitivity: medium
```

---
## 13. carreleur
```yaml
matrix_id: PRO-CARRE-013
canonical_name: carreleur
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un carreleur pour la pose de carrelage, faience, mosaique et pierre naturelle.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: corps_metier
    required: true
  - field_name: description_travaux
    required: true
  - field_name: surface_concernee
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_travaux
    required: true
    values:
      - carrelage_sol
      - faience_murale
      - mosaique_decorative
      - pierre_naturelle
      - dalle_exterieure
      - carrelage_grand_format
      - carrelage_chauffant
      - terrasse_carrelage
      - piscine_carrelage
  - field_name: materiaux_souhaites
    required: true
    values:
      - gre_cerame
      - porcelaine
      - faience
      - pierre_naturelle
      - marbre
      - granit
      - terre_cuite
      - ciment
      - resine
      - mosaique_verre
      - ardoise
      - travertin
      - beton_cire
      - quartz
  - field_name: budget
    required: true
  - field_name: delai
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_materiau
    weight: 0.25
  - field_name: references_realisations
    weight: 0.15
  - field_name: garantie_pose
    weight: 0.15
  - field_name: tarif_pose_m2
    weight: 0.10
  - field_name: outillage_specialise
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: references_chantiers
    required: true
  - field_name: catalogue_materiaux
    required: true
  - field_name: assurance_pro
    required: true
  - field_name: garantie_travaux
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: devis_signe
    required: true
    type: document
  - field_name: choix_carrelage_reference
    required: true
    type: document
  - field_name: plan_calepinage
    required: true
    type: document
  - field_name: planning_chantier
    required: true
    type: schedule
  - field_name: conditions_reglement
    required: true
    type: contract

recommended_fields:
  - field_name: showroom_carrelage
  - field_name: echantillons_disponibles
  - field_name: conseil_technique_pose
  - field_name: service_finition_inclus

optional_fields:
  - field_name: fourniture_carrelage_incluse
  - field_name: joint_epoxy
  - field_name: dalle_chauffante_integree
  - field_name: protection_sur_chantier
  - field_name: nettoyage_fin_chantier

conditional_fields:
  - field_name: preparation_sol_necessaire
    condition: type_travaux == carrelage_sol || type_travaux == dalle_exterieure || type_travaux == terrasse_carrelage
    type: boolean
  - field_name: ragreage_necessaire
    condition: type_pose == pose_collee
    type: boolean

sensitive_fields:
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: identite_client
    pii: true
    sensitivity: high
  - field_name: adresse_chantier
    pii: true
    sensitivity: high
  - field_name: budget_travaux
    pii: true
    sensitivity: medium
```

---
## 14. couvreur
```yaml
matrix_id: PRO-COUVR-014
canonical_name: couvreur
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un couvreur pour la pose, la reparation et l'entretien de toitures et charpentes.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: corps_metier
    required: true
  - field_name: description_travaux
    required: true
  - field_name: surface_concernee
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_travaux
    required: true
    values:
      - toiture_neuve
      - reparation_toiture
      - renovation_toiture
      - etancheite_toiture_terrasse
      - charpente_bois
      - charpente_metal
      - zinguerie_gouttiere
      - isolation_combles
      - velux_fenetre_toit
      - couverture_panneau_solaire
      - demoussage_traitement
      - infiltration_reparation
  - field_name: materiau_couverture
    required: true
    values:
      - tuile_terre_cuite
      - ardoise_naturelle
      - bac_acier
      - zinc
      - cuivre
      - shingle
      - bois_bardeau
      - chaume
      - toiture_vegetalisee
      - membrane_etancheite
  - field_name: budget
    required: true
  - field_name: delai
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_couverture
    weight: 0.25
  - field_name: materiau_maitrise
    weight: 0.15
  - field_name: assurance_decennale
    weight: 0.15
  - field_name: references_chantiers
    weight: 0.10
  - field_name: qualification_qualibat
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: qualifications_professionnelles
    required: true
  - field_name: assurance_decennale
    required: true
  - field_name: references_chantiers
    required: true
  - field_name: zone_intervention_max_km
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: devis_signe
    required: true
    type: document
  - field_name: inspection_prealable_etat_lieux
    required: true
    type: document
  - field_name: planning_chantier
    required: true
    type: schedule
  - field_name: conditions_securite_chantier
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: fiche_technique_materiaux
    required: true
    type: document
  - field_name: garantie_decennale_attestation
    required: true
    type: document

recommended_fields:
  - field_name: service_urgence_infiltration
  - field_name: devis_gratuit
  - field_name: inspection_thermique
  - field_name: conseil_isolation

optional_fields:
  - field_name: echafaudage_inclus
  - field_name: evacuation_dechets_incluse
  - field_name: traitement_bois_charpente
  - field_name: demoussage_inclus
  - field_name: fourniture_materiaux_incluse

conditional_fields:
  - field_name: permis_construire_toiture
    condition: type_travaux == toiture_neuve || type_travaux == renovation_toiture
    type: boolean
  - field_name: echafaudage_necessaire
    condition: type_chantier == immeuble_collectif || type_chantier == batiment_industriel || hauteur_batiment > 8
    type: boolean

sensitive_fields:
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: identite_client
    pii: true
    sensitivity: high
  - field_name: adresse_chantier
    pii: true
    sensitivity: high
  - field_name: budget_travaux_detail
    pii: true
    sensitivity: high
  - field_name: acces_hauteur_securite
    pii: false
    sensitivity: medium
```

---
## 15. expert_immobilier
```yaml
matrix_id: PRO-EXPER-015
canonical_name: expert_immobilier
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un expert immobilier pour les expertises techniques, evaluations et diagnostics approfondis.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_mission_expertise
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_mission_expertise
    required: true
  - field_name: specialite_expertise
    required: true
    values:
      - expertise_technique
      - expertise_juridique
      - expertise_financiere
      - expertise_assurance
      - expertise_copropriete
      - expertise_fonciere
      - expertise_thermique
      - expertise_structure
      - expertise_generaliste
  - field_name: qualification_expert
    required: true
    values:
      - expert_pres_tribunal
      - expert_agre_courtage
      - expert_compagnie_assurance
      - diagnostiqueur_certifie
      - ingenieur_conseil
      - architecte_expert
      - expert_immobilier_independant
  - field_name: experience_minimum_ans
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_expertise
    weight: 0.30
  - field_name: certifications_expertises
    weight: 0.15
  - field_name: references_missions_similaires
    weight: 0.10
  - field_name: honoraires_journaliers
    weight: 0.10
  - field_name: delai_rendu_rapport
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: titre_qualification
    required: true
  - field_name: assurance_professionnelle
    required: true
  - field_name: references_cabinet
    required: true
  - field_name: zone_intervention
    required: true
  - field_name: honoraires_pratiques
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: lettre_mission
    required: true
    type: document
  - field_name: contrat_expertise
    required: true
    type: document
  - field_name: acces_bien
    required: true
    type: document
  - field_name: calendrier_expertise
    required: true
    type: schedule
  - field_name: honoraires_convenus
    required: true
    type: contract
  - field_name: autorisation_proprietaire
    required: true
    type: document

recommended_fields:
  - field_name: liste_publications
  - field_name: appartenance_association_professionnelle
  - field_name: agrement_tribunal
  - field_name: formation_specialisee_continue

optional_fields:
  - field_name: equipe_pluridisciplinaire
  - field_name: laboratoire_analyse
  - field_name: materiel_mesure_specialise
  - field_name: archive_missions_anterieures
  - field_name: rapport_interactif

conditional_fields:
  - field_name: agrement_judiciaire
    condition: type_mission_expertise == expertise_contradictoire || type_mission_expertise == expertise_litige
    type: boolean
  - field_name: mission_judiciaire
    condition: type_mission_expertise == expertise_litige
    type: boolean

sensitive_fields:
  - field_name: rapport_expertise_complet
    pii: false
    sensitivity: high
  - field_name: evaluation_valeur_bien
    pii: true
    sensitivity: high
  - field_name: identification_proprietaire
    pii: true
    sensitivity: high
  - field_name: constatations_techniques
    pii: false
    sensitivity: medium
```

---
## 16. evaluateur
```yaml
matrix_id: PRO-EVALU-016
canonical_name: evaluateur
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un evaluateur agrees pour l'estimation de la valeur venale, locative ou patrimoniale de biens.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_evaluation
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_evaluation
    required: true
  - field_name: methode_evaluation
    required: true
    values:
      - comparative
      - par_revenu
      - par_cout
      - multicritere
      - actualisation_flux
  - field_name: qualification_evaluateur
    required: true
    values:
      - evaluateur_agre
      - expert_immobilier
      - mru_membre_chartered_surveyors
      - certified_appraiser
      - ingenieur_evaluateur
  - field_name: norme_evaluation
    required: true
    values:
      - norme_ivs
      - norme_anc
      - norme_fiscal
      - norme_bancaire
      - norme_assurance

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_evaluation
    weight: 0.30
  - field_name: marche_immobilier_local
    weight: 0.20
  - field_name: certification_evaluateur
    weight: 0.15
  - field_name: references_estimations
    weight: 0.10
  - field_name: tarif_prestation
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: titre_certification
    required: true
  - field_name: references_estimations
    required: true
  - field_name: secteur_expertise
    required: true
  - field_name: honoraires_estimation
    required: true
  - field_name: assurance_pro
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: mandat_evaluation
    required: true
    type: document
  - field_name: dossier_bien
    required: true
    type: document
  - field_name: acces_bien
    required: true
  - field_name: documentation_juridique
    required: true
    type: document
  - field_name: calendrier_visite
    required: true
    type: schedule
  - field_name: conditions_honoraires
    required: true
    type: contract

recommended_fields:
  - field_name: base_donnees_transactions
  - field_name: outils_sig_analyse
  - field_name: etudes_marche_locales
  - field_name: reseau_agents_immobiliers

optional_fields:
  - field_name: logiciel_evaluation
  - field_name: archive_estimations_similaires
  - field_name: veille_marche_immobilier
  - field_name: publication_etudes_sectorielles
  - field_name: membre_association_professionnelle

conditional_fields:
  - field_name: expertise_contradictoire
    condition: type_evaluation == evaluation_expropriation || type_evaluation == evaluation_partage
    type: boolean
  - field_name: norme_bancaire_applicable
    condition: type_evaluation == evaluation_pret_hypothecaire
    type: boolean

sensitive_fields:
  - field_name: rapport_evaluation_complet
    pii: true
    sensitivity: high
  - field_name: valeur_estimee_bien
    pii: true
    sensitivity: high
  - field_name: identite_proprietaire
    pii: true
    sensitivity: high
  - field_name: donnees_financieres_bien
    pii: true
    sensitivity: high
  - field_name: analyse_marche_confidentielle
    pii: false
    sensitivity: medium
```

---
## 17. gestionnaire_immobilier
```yaml
matrix_id: PRO-GESTI-017
canonical_name: gestionnaire_immobilier
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un gestionnaire immobilier pour la gestion locative, l'administration de biens et le suivi des locations.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_gestion
    required: true
  - field_name: nombre_biens
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_gestion
    required: true
  - field_name: portefeuille_gere
    required: true
    values:
      - moins_10_biens
      - 10_50_biens
      - 50_200_biens
      - plus_200_biens
  - field_name: agrement_gestionnaire
    required: true
    values:
      - carte_pro_g
      - agrement_sci
      - mandat_gerance
      - sans_agrement

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: portefeuille_similaire
    weight: 0.20
  - field_name: zone_couverture
    weight: 0.20
  - field_name: experience_annees
    weight: 0.15
  - field_name: taux_occupation
    weight: 0.10
  - field_name: taux_recouvrement
    weight: 0.10
  - field_name: honoraires_gestion
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: societe_gestion
    required: true
  - field_name: portefeuille_actuel
    required: true
  - field_name: references_bailleurs
    required: true
  - field_name: assurance_professionnelle
    required: true
  - field_name: grille_tarifaire
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_gestion
    required: true
    type: document
  - field_name: mandat_gerance
    required: true
    type: document
  - field_name: etat_lieux_bien
    required: true
    type: document
  - field_name: conditions_honoraires
    required: true
    type: contract
  - field_name: conditions_resiliation
    required: true
    type: contract
  - field_name: reporting_periodicite
    required: true
    type: document

recommended_fields:
  - field_name: legalite_contrats_locations
  - field_name: service_recouvrement_contentieux
  - field_name: assurance_loyers_impayes_proposee
  - field_name: suivi_comptable

optional_fields:
  - field_name: service_travaux_geres
  - field_name: mise_en_location_incluse
  - field_name: portail_bailleur_en_ligne
  - field_name: application_suivi_locataire

conditional_fields:
  - field_name: assurance_impayes
    condition: type_gestion == gestion_locative_complete
    type: boolean
  - field_name: gestion_travaux
    condition: type_gestion == gestion_locative_complete || type_gestion == gestion_travaux_location
    type: boolean

sensitive_fields:
  - field_name: contrat_bail_signe
    pii: true
    sensitivity: high
  - field_name: identite_locataires
    pii: true
    sensitivity: high
  - field_name: montant_loyers
    pii: true
    sensitivity: high
  - field_name: situation_financiere_bailleur
    pii: true
    sensitivity: high
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: dossier_locataire_complet
    pii: true
    sensitivity: high
```

---
## 18. syndic
```yaml
matrix_id: PRO-SYNDI-018
canonical_name: syndic
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un syndic de copropriete pour la gestion d'immeubles et l'administration des parties communes.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_mission_syndic
    required: true
  - field_name: nombre_lots
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_mission_syndic
    required: true
  - field_name: taille_copropriete
    required: true
    values:
      - petite_moins_10_lots
      - moyenne_10_50_lots
      - grande_50_200_lots
      - tres_grande_plus_200_lots
  - field_name: statut_syndic
    required: true
    values:
      - syndic_professionnel
      - syndic_benefice
      - syndic_cooperative
      - administrateur_providence
  - field_name: anciennete_cabinet
    required: true
    values:
      - moins_2_ans
      - 2_5_ans
      - 5_15_ans
      - plus_15_ans

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: taille_copropriete_correspondance
    weight: 0.25
  - field_name: honoraires_syndic
    weight: 0.15
  - field_name: experience_similaire
    weight: 0.15
  - field_name: taux_recouvrement_charges
    weight: 0.10
  - field_name: disponibilite_reunions
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: raison_sociale_syndic
    required: true
  - field_name: contact_cabinet
    required: true
  - field_name: nombre_coproprietes_geres
    required: true
  - field_name: references_coproprietes
    required: true
  - field_name: assurance_rc_pro
    required: true
  - field_name: conditions_honoraires
    required: true
  - field_name: garantie_financiere
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_syndic
    required: true
    type: document
  - field_name: reglement_copropriete
    required: true
    type: document
  - field_name: carnet_entretien_immeuble
    required: true
    type: document
  - field_name: budget_previsionnel
    required: true
    type: document
  - field_name: assurances_immeuble
    required: true
    type: document
  - field_name: planning_assemblee_generale
    required: true
    type: schedule

recommended_fields:
  - field_name: extranet_coproprietaires
  - field_name: application_mobile_suivi
  - field_name: service_recouvrement
  - field_name: partenariat_avocat

optional_fields:
  - field_name: audit_energetique_copro
  - field_name: diagnostic_technique_global
  - field_name: plan_pluriannuel_travaux
  - field_name: contrat_maintenance_ascenseur

conditional_fields:
  - field_name: fonds_travaux_obligatoire
    condition: taille_copropriete >= moyenne_10_50_lots
    type: boolean
  - field_name: diagnostic_technique_global_obligatoire
    condition: taille_copropriete >= grande_50_200_lots
    type: boolean

sensitive_fields:
  - field_name: identite_coproprietaires
    pii: true
    sensitivity: high
  - field_name: montant_charges_individuelles
    pii: true
    sensitivity: high
  - field_name: situation_financiere_copropriete
    pii: true
    sensitivity: high
  - field_name: contentieux_en_cours
    pii: true
    sensitivity: high
  - field_name: proces_verbaux_assemblees
    pii: false
    sensitivity: medium
```

---
## 19. photographe_immobilier
```yaml
matrix_id: PRO-PHOTO-019
canonical_name: photographe_immobilier
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un photographe specialise en photographie immobiliere pour les prises de vues professionnelles.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_prestation
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_prestation
    required: true
  - field_name: equipement_utilise
    required: true
    values:
      - reflex_professionnel
      - mirrorless_full_frame
      - objectif_grand_angle
      - drone_photographie
      - materiel_eclairage_pro
      - camera_360
  - field_name: delai_livraison
    required: true
    values:
      - 24h
      - 48h
      - 72h
      - 1_semaine
      - personnalise

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: portfolio_immobilier
    weight: 0.30
  - field_name: equipement_disponible
    weight: 0.20
  - field_name: delai_livraison_cliches
    weight: 0.15
  - field_name: tarif_prestation
    weight: 0.10
  - field_name: assurance_materiel
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: portfolio_immobilier
    required: true
  - field_name: equipement
    required: true
  - field_name: tarifs_prestations
    required: true
  - field_name: delai_livraison_standard
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_prestation_photo
    required: true
    type: document
  - field_name: brief_photographique
    required: true
    type: document
  - field_name: planning_seance
    required: true
    type: schedule
  - field_name: droits_utilisation_images
    required: true
    type: contract
  - field_name: conditions_paiement
    required: true
    type: contract

recommended_fields:
  - field_name: retouche_photo_incluse
  - field_name: visite_virtuelle_disponible
  - field_name: forfait_multiple_biens
  - field_name: photographie_aerienne
  - field_name: home_staging_conseil

optional_fields:
  - field_name: studio_retouche
  - field_name: materiel_eclairage_supplementaire
  - field_name: photographe_assistant
  - field_name: livraison_nuage_en_ligne
  - field_name: galerie_privee_client

conditional_fields:
  - field_name: drone_necessaire
    condition: type_prestation == photo_aerienne_drone || type_prestation == reportage_complet
    type: boolean
  - field_name: retouche_incluse
    condition: type_prestation == seance_photo_interieure || type_prestation == reportage_complet
    type: boolean

sensitive_fields:
  - field_name: photos_interieures_bien
    pii: false
    sensitivity: medium
  - field_name: identification_bien
    pii: true
    sensitivity: high
  - field_name: acces_propriete_privee
    pii: true
    sensitivity: high
  - field_name: droits_auteur_images
    pii: false
    sensitivity: medium
```

---
## 20. videaste_drone
```yaml
matrix_id: PRO-VIDEA-020
canonical_name: videaste_drone
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un videaste et telepilote de drone pour la realisation de videos immobilieres et aeriennes.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_prestation
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_prestation
    required: true
  - field_name: equipement_video
    required: true
    values:
      - drone_professionnel
      - drone_cinematique
      - camera_gopro_pro
      - camera_360_insta360
      - stabilisateur_gimbal
      - micro_professionnel
      - eclairage_video_pro
      - drone_thermique
  - field_name: certification_drone
    required: true
    values:
      - telepilote_dgac
      - brevet_drone_civil
      - assurance_drone_specifique
      - declaration_prefet
      - autorisation_survol
  - field_name: experience_video_immobiliere
    required: true
    values:
      - debutant_moins_1_an
      - intermediaire_1_3_ans
      - confirme_3_5_ans
      - expert_plus_5_ans
  - field_name: delai_livraison
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: portfolio_video
    weight: 0.30
  - field_name: equipement_maitrise
    weight: 0.15
  - field_name: certification_drone
    weight: 0.15
  - field_name: experience_immobiliere
    weight: 0.15
  - field_name: tarif_journee
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: portfolio_video
    required: true
  - field_name: equipement_technique
    required: true
  - field_name: certifications_drone
    required: true
  - field_name: assurance_professionnelle
    required: true
  - field_name: grille_tarifaire
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_production_video
    required: true
    type: document
  - field_name: brief_creatif_video
    required: true
    type: document
  - field_name: planning_tournage
    required: true
    type: schedule
  - field_name: autorisation_survol_drone
    required: true
    type: document
  - field_name: droits_diffusion_cedes
    required: true
    type: contract
  - field_name: format_livraison
    required: true
    type: document

recommended_fields:
  - field_name: montage_inclus
  - field_name: etalonnage_couleur
  - field_name: habillage_graphique
  - field_name: musique_libre_droit
  - field_name: voix_off_professionnelle
  - field_name: sous_titrage_multilingue

optional_fields:
  - field_name: storyboard_prealable
  - field_name: drone_nuit_autorisation
  - field_name: video_4k_8k
  - field_name: video_verticale_reseaux
  - field_name: livraison_raw_footage
  - field_name: nombre_revisions_incluses

conditional_fields:
  - field_name: autorisation_survol_urbain
    condition: type_prestation == video_aerienne_drone || type_prestation == video_survol_quartier
    type: document
  - field_name: post_production_longue
    condition: type_prestation == video_promotionnelle_complete || type_prestation == film_chantier_suivi
    type: boolean

sensitive_fields:
  - field_name: video_haute_resolution_bien
    pii: false
    sensitivity: medium
  - field_name: identification_exacte_bien
    pii: true
    sensitivity: high
  - field_name: donnees_gps_vol_drone
    pii: false
    sensitivity: medium
  - field_name: acces_spatial_aerien_prive
    pii: true
    sensitivity: high
```

---
## 21. demenageur
```yaml
matrix_id: PRO-DEMEN-021
canonical_name: demenageur
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'une entreprise de demenagement pour le transport de meubles et la logistique residentielle.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: localisation_depart
    required: true
  - field_name: localisation_arrivee
    required: true
  - field_name: type_demenagement
    required: true
  - field_name: volume_estime
    required: true

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_demenagement
    required: true
  - field_name: distance_km
    required: true
    values:
      - moins_50_km
      - 50_200_km
      - 200_500_km
      - plus_500_km
      - international
  - field_name: volume_estime
    required: true
  - field_name: services_souhaites
    required: true
    values:
      - demenagement_standard
      - demenagement_avec_emballage
      - demenagement_complet
      - montage_meubles
      - garde_meuble
      - assurance_transport
  - field_name: budget
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: couverture_itineraire
    weight: 0.20
  - field_name: capacite_transport
    weight: 0.20
  - field_name: services_inclus
    weight: 0.15
  - field_name: assurance_demenagement
    weight: 0.15
  - field_name: tarif_m3_km
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: raison_sociale_demenageur
    required: true
  - field_name: contact_logistique
    required: true
  - field_name: flotte_vehicules
    required: true
  - field_name: assurance_transport
    required: true
  - field_name: zones_desserte
    required: true
  - field_name: grille_tarifaire
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_demenagement
    required: true
    type: document
  - field_name: inventaire_mobilier
    required: true
    type: document
  - field_name: etat_lieux_logement_depart
    required: true
    type: document
  - field_name: planning_operation
    required: true
    type: schedule
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: autorisation_stationnement
    required: false
    type: document

recommended_fields:
  - field_name: service_emballage_fourni
  - field_name: monte_meuble_disponible
  - field_name: garde_meuble_propose
  - field_name: devis_gratuit_visite

optional_fields:
  - field_name: nombre_demenageurs_equipe
  - field_name: stock_cartons_inclus
  - field_name: deballage_reinstallation
  - field_name: nettoyage_ancien_logement
  - field_name: mise_en_meubles

conditional_fields:
  - field_name: demenagement_international_douane
    condition: distance_km == international
    type: boolean
  - field_name: monte_meuble_necessaire
    condition: etage_depart > 0 && ascenseur_depart == false
    type: boolean

sensitive_fields:
  - field_name: adresse_depart_exacte
    pii: true
    sensitivity: high
  - field_name: adresse_arrivee_exacte
    pii: true
    sensitivity: high
  - field_name: inventaire_objets_valeur
    pii: true
    sensitivity: high
  - field_name: date_absence_logement
    pii: true
    sensitivity: high
```

---
## 22. entreprise_nettoyage
```yaml
matrix_id: PRO-ENTRE-022
canonical_name: entreprise_nettoyage
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'une entreprise de nettoyage professionnel pour l'entretien regulier ou ponctuel de biens.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_nettoyage
    required: true
  - field_name: surface_nettoyer
    required: true
  - field_name: periodicite
    required: true
    values:
      - unique_ponctuel
      - hebdomadaire
      - bimensuel
      - mensuel
      - trimestriel
      - semestriel
      - annuel

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_nettoyage
    required: true
  - field_name: taille_entreprise
    required: true
    values:
      - individuel
      - petite_equipe_2_5
      - moyenne_equipe_5_20
      - grande_equipe_20_plus
  - field_name: budget_estime
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_nettoyage
    weight: 0.25
  - field_name: taille_equipe_disponible
    weight: 0.15
  - field_name: assurance_rc_pro
    weight: 0.10
  - field_name: tarif_m2
    weight: 0.10
  - field_name: references_clients
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: agrements_qualite
    required: false
  - field_name: assurance_professionnelle
    required: true
  - field_name: references_clients
    required: true
  - field_name: zone_intervention
    required: true
  - field_name: tarifs_indicatifs
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_prestation_nettoyage
    required: true
    type: document
  - field_name: cahier_charges_nettoyage
    required: true
    type: document
  - field_name: fiche_produits_utilises
    required: true
    type: document
  - field_name: planning_intervention
    required: true
    type: schedule
  - field_name: conditions_tarifaires
    required: true
    type: contract
  - field_name: etat_lieux_initial_proprete
    required: true
    type: document

recommended_fields:
  - field_name: produits_ecologiques
  - field_name: materiel_professionnel
  - field_name: personnel_forme
  - field_name: devis_gratuit
  - field_name: controle_qualite

optional_fields:
  - field_name: nombre_agents_nettoyage
  - field_name: vehicule_societe
  - field_name: fourniture_produits_incluse
  - field_name: machine_nettoyage_specialisee
  - field_name: desinfection_supplementaire

conditional_fields:
  - field_name: produit_specifique
    condition: type_nettoyage == nettoyage_industriel || type_nettoyage == nettoyage_cuisine_professionnelle
    type: boolean
  - field_name: habilitation_travail_hauteur
    condition: type_nettoyage == nettoyage_facade_vitres
    type: boolean

sensitive_fields:
  - field_name: acces_local_client
    pii: true
    sensitivity: high
  - field_name: planning_absence_client
    pii: true
    sensitivity: high
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: identite_client
    pii: true
    sensitivity: high
  - field_name: code_alarme_local
    pii: true
    sensitivity: high
```

---
## 23. gardiennage
```yaml
matrix_id: PRO-GARDI-023
canonical_name: gardiennage
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un service de gardiennage, surveillance et securite pour la protection de biens immobiliers.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_securisation
    required: true
  - field_name: duree_besoin
    required: true
    values:
      - ponctuel
      - journee
      - semaine
      - mois
      - trimestre
      - annee
      - indetermine

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_securisation
    required: true
  - field_name: taille_societe_securite
    required: true
    values:
      - independant
      - petite_equipe_2_10
      - moyenne_equipe_10_50
      - grande_societe_plus_50
  - field_name: agrement_securite
    required: true
    values:
      - cnaPS_agrement
      - agrement_prefectoral
      - carte_professionnelle_securite
      - ssi_ap_formation
      - sans_agrement
  - field_name: horaire_souhaite
    required: true
    values:
      - jour
      - nuit
      - 24h_24
      - week_end
      - personnalise

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_securisation
    weight: 0.25
  - field_name: agrement_securite
    weight: 0.20
  - field_name: personnel_disponible
    weight: 0.10
  - field_name: equipement_surveillance
    weight: 0.10
  - field_name: tarif_garde_horaire
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: raison_sociale_securite
    required: true
  - field_name: contact_urgence
    required: true
  - field_name: agrement_cNAPS
    required: true
  - field_name: assurance_professionnelle
    required: true
  - field_name: references_clients
    required: true
  - field_name: zone_couverture
    required: true
  - field_name: grille_tarifaire
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_prestation_securite
    required: true
    type: document
  - field_name: analyse_risques_site
    required: true
    type: document
  - field_name: plan_de_gardiennage
    required: true
    type: document
  - field_name: planning_effectif
    required: true
    type: schedule
  - field_name: consignes_securite_site
    required: true
    type: document
  - field_name: conditions_financieres
    required: true
    type: contract
  - field_name: assurance_rc_pro
    required: true
    type: document

recommended_fields:
  - field_name: centre_surveillance_24h
  - field_name: intervention_alerte
  - field_name: rapport_incidents_journalier
  - field_name: certification_qualite_securite

optional_fields:
  - field_name: equipement_video_surveillance
  - field_name: systeme_alarme_inclus
  - field_name: ronde_interactive
  - field_name: vehicule_patrouille
  - field_name: agent_cynophile

conditional_fields:
  - field_name: port_arme_autorise
    condition: type_securisation == gardiennage_permanent || type_securisation == garde_site_industriel
    type: boolean
  - field_name: surveillance_electronique
    condition: type_securisation == surveillance_electronique || type_securisation == gardiennage_permanent
    type: boolean

sensitive_fields:
  - field_name: plan_securite_site
    pii: false
    sensitivity: high
  - field_name: identification_agents_affectes
    pii: true
    sensitivity: high
  - field_name: code_acces_site
    pii: true
    sensitivity: high
  - field_name: systeme_alarme_code
    pii: true
    sensitivity: high
  - field_name: analyse_vulnerabilite
    pii: false
    sensitivity: high
```

---
## 24. assureur
```yaml
matrix_id: PRO-ASSUR-024
canonical_name: assureur
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un assureur ou courtier en assurance pour la souscription de contrats d'assurance immobiliere.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_assurance
    required: true
    values:
      - assurance_habitation
      - assurance_proprietaire_bailleur
      - assurance_copropriete
      - assurance_dommage_ouvrage
      - assurance_professionnelle_rc
      - assurance_multirisque_immeuble
      - assurance_pret_immobilier
      - assurance_sinistre

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_assurance
    required: true
  - field_name: specialite_assureur
    required: true
    values:
      - generaliste
      - specialiste_immobilier
      - specialiste_entreprise
      - specialiste_dommage_ouvrage
      - courtier_multicarte
  - field_name: statut_assureur
    required: true
    values:
      - courtier
      - agent_general
      - mandataire
      - compagnie_directe
      - bancassureur

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_correspondance
    weight: 0.25
  - field_name: offres_adaptees
    weight: 0.20
  - field_name: tarifs_competitifs
    weight: 0.15
  - field_name: garanties_proposees
    weight: 0.15
  - field_name: delai_etude_dossier
    weight: 0.10
  - field_name: accompagnement_sinistre
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: cabinet_assurance
    required: true
  - field_name: agrement_ORIAS
    required: true
  - field_name: compagnies_partenaires
    required: true
  - field_name: references_clients
    required: false

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: mandat_recherche
    required: true
    type: document
  - field_name: questionnaire_risques
    required: true
    type: document
  - field_name: donnees_bien_assurer
    required: true
    type: document
  - field_name: historique_sinistre
    required: false
    type: document
  - field_name: conditions_souscription
    required: true
    type: contract
  - field_name: proposition_contrat
    required: true
    type: document

recommended_fields:
  - field_name: comparateur_en_ligne
  - field_name: service_sinistre_dedie
  - field_name: simulation_gratuite
  - field_name: accompagnement_pret

optional_fields:
  - field_name: nombre_compagnies_partenaires
  - field_name: application_mobile
  - field_name: teleassistance_incluse
  - field_name: service_juridique
  - field_name: franchise_reduite_option

conditional_fields:
  - field_name: assurance_pret_obligatoire
    condition: type_assurance == assurance_pret_immobilier
    type: boolean
  - field_name: inspection_bien_requise
    condition: type_assurance == assurance_dommage_ouvrage || type_assurance == assurance_multirisque_immeuble
    type: boolean

sensitive_fields:
  - field_name: donnees_medicales
    pii: true
    sensitivity: high
  - field_name: situation_financiere
    pii: true
    sensitivity: high
  - field_name: historique_sinistres
    pii: true
    sensitivity: high
  - field_name: identite_assure
    pii: true
    sensitivity: high
  - field_name: valeur_biens_declaree
    pii: true
    sensitivity: high
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
```

---
## 25. banque_microfinance
```yaml
matrix_id: PRO-BANQU-025
canonical_name: banque_microfinance
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'une banque ou institution de microfinance pour le financement immobilier et le credit habitat.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_financement
    required: true
  - field_name: montant_souhaite
    required: true
  - field_name: apport_personnel
    required: false

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_financement
    required: true
  - field_name: type_etablissement
    required: true
    values:
      - banque_commerciale
      - banque_investissement
      - microfinance
      - cooperative_epargne_credit
      - societe_financiere
      - banque_islamique
  - field_name: montant_min_max
    required: true
    type: range
  - field_name: duree_souhaitee
    required: true
    type: range_months

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: taux_effectif
    weight: 0.25
  - field_name: conditions_octroi
    weight: 0.20
  - field_name: delai_traitement
    weight: 0.15
  - field_name: frais_dossier
    weight: 0.10
  - field_name: souplesse_caen
    weight: 0.10
  - field_name: presence_locale
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: raison_sociale_banque
    required: true
  - field_name: agence_proximite
    required: true
  - field_name: contact_conseiller
    required: true
  - field_name: conditions_generales
    required: true
  - field_name: grille_taux
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: dossier_complet_financement
    required: true
    type: document
  - field_name: justificatifs_revenus
    required: true
    type: document
  - field_name: offre_pret
    required: true
    type: document
  - field_name: garanties_hypothecaires
    required: true
    type: document
  - field_name: calendrier_versement
    required: true
    type: schedule
  - field_name: contrat_assurance
    required: true
    type: document

recommended_fields:
  - field_name: application_bancaire
  - field_name: service_conseil_gratuit
  - field_name: assurance_chomage_option
  - field_name: simulateur_en_ligne

optional_fields:
  - field_name: reseau_agences
  - field_name: service_en_ligne
  - field_name: credit_bail_option
  - field_name: pret_in_fine
  - field_name: regroupement_credit

conditional_fields:
  - field_name: garantie_hypothecaire
    condition: montant_souhaite > 50000
    type: boolean
  - field_name: assurance_emprunteur
    condition: type_financement == credit_acquisition || type_financement == credit_construction
    type: boolean

sensitive_fields:
  - field_name: identite_emprunteur_complet
    pii: true
    sensitivity: high
  - field_name: situation_financiere_detail
    pii: true
    sensitivity: high
  - field_name: bulletins_salaire
    pii: true
    sensitivity: high
  - field_name: avis_imposition
    pii: true
    sensitivity: high
  - field_name: contrat_pret_signe
    pii: true
    sensitivity: high
  - field_name: historique_credit
    pii: true
    sensitivity: high
```

---
## 26. courtier
```yaml
matrix_id: PRO-COURT-026
canonical_name: courtier
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un courtier en immobilier, financement ou assurance pour l'intermediation et le conseil.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_courtage
    required: true
    values:
      - courtier_pret_immobilier
      - courtier_assurance
      - courtier_immobilier
      - courtier_financement_professionnel
      - courtier_regroupement_credit
      - courtier_investissement
  - field_name: montant_souhaite
    required: false

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_courtage
    required: true
  - field_name: statut_courtier
    required: true
    values:
      - courtier_inscrit_ORIAS
      - courtier_salarie
      - courtier_mandataire
      - cabinet_courtage
      - reseau_courtier
  - field_name: partenaires_financeurs
    required: true
    values:
      - banques_partenaires
      - assureurs_partenaires
      - investisseurs_prives
      - fonds_investissement
      - multi_partenaires
  - field_name: honoraire_pratique
    required: true
    values:
      - honoraires_reussite
      - commission_banque
      - honoraires_fixes
      - mixte
      - gratuit

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_courtage
    weight: 0.25
  - field_name: reseau_partenaires
    weight: 0.20
  - field_name: taux_obtenu_moyen
    weight: 0.15
  - field_name: delai_moyen_obtention
    weight: 0.15
  - field_name: taux_satisfaction
    weight: 0.10
  - field_name: honoraires_pratiques
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: cabinet_courtage
    required: true
  - field_name: numero_ORIAS
    required: true
  - field_name: liste_partenaires
    required: true
  - field_name: references_clients
    required: true
  - field_name: conditions_honoraires
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: mandat_recherche_financement
    required: true
    type: document
  - field_name: dossier_financier_client
    required: true
    type: document
  - field_name: justificatifs_revenus_patrimoine
    required: true
    type: document
  - field_name: projet_immobilier_description
    required: true
    type: document
  - field_name: conditions_honoraires_contractuelles
    required: true
    type: contract
  - field_name: offres_recues
    required: true
    type: document

recommended_fields:
  - field_name: simulateur_en_ligne
  - field_name: suivi_dossier_personnalise
  - field_name: conseil_optimisation
  - field_name: accompagnement_juridique

optional_fields:
  - field_name: nombre_partenaires
  - field_name: application_suivi
  - field_name: service_renegociation
  - field_name: analyse_budgetaire
  - field_name: conseil_fiscal

conditional_fields:
  - field_name: honoraires_reussite
    condition: type_courtage == courtier_pret_immobilier || type_courtage == courtier_financement_professionnel
    type: boolean
  - field_name: exclusivite_mandat
    condition: type_courtage == courtier_immobilier
    type: boolean

sensitive_fields:
  - field_name: identite_client_complet
    pii: true
    sensitivity: high
  - field_name: dossier_financier_complet
    pii: true
    sensitivity: high
  - field_name: situation_endettement
    pii: true
    sensitivity: high
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: historique_credit_client
    pii: true
    sensitivity: high
```

---
## 27. prestataire_administratif
```yaml
matrix_id: PRO-PREST-027
canonical_name: prestataire_administratif
request_family: PROFESSIONAL_SEARCH
transaction_type: FIND
property_or_service_type: service_professionnel

description: >
  Recherche d'un prestataire administratif pour l'assistance dans les demarches immobilieres et la gestion documentaire.

minimum_intake_fields:
  - field_name: localisation
    required: true
  - field_name: description_besoin
    required: true
  - field_name: urgence
    required: true
  - field_name: date_souhaitee
    required: true
  - field_name: type_prestation_administrative
    required: true
    values:
      - assistance_demarches
      - redaction_contrats
      - montage_dossier_pret
      - suivi_administratif
      - declaration_fiscale
      - gestion_documentaire
      - transcription_actes
      - coordination_partenaires
  - field_name: volume_estime
    required: false

minimum_search_fields:
  - field_name: localisation
    required: true
  - field_name: type_prestation_administrative
    required: true
  - field_name: specialite_administrative
    required: true
    values:
      - droit_immobilier
      - droit_foncier
      - fiscalite_immobiliere
      - copropriete
      - succession
      - financement
      - generaliste
  - field_name: qualification
    required: true
    values:
      - assistant_juridique
      - clerc_notaire
      - comptable
      - conseiller_fiscal
      - assistant_de_gestion
      - secretaire_juridique
  - field_name: budget_estime
    required: true

minimum_matching_fields:
  - field_name: proximite_geographique
    weight: 0.20
  - field_name: specialite_administrative
    weight: 0.30
  - field_name: experience_annees
    weight: 0.20
  - field_name: qualification
    weight: 0.15
  - field_name: delai_traitement
    weight: 0.10
  - field_name: tarif_horaire
    weight: 0.10
  - field_name: langues_maitrisees
    weight: 0.10

minimum_introduction_fields:
  - field_name: identite_professionnel
    required: true
  - field_name: contact
    required: true
  - field_name: references
    required: true
  - field_name: cabinet_structure
    required: true
  - field_name: specialites_declarees
    required: true
  - field_name: assurance_professionnelle
    required: true
  - field_name: references_clients
    required: true
  - field_name: grille_tarifaire
    required: true

minimum_execution_fields:
  - field_name: contrat_service
    required: true
    type: document
  - field_name: conditions_paiement
    required: true
    type: contract
  - field_name: contrat_prestation_administrative
    required: true
    type: document
  - field_name: mandat_representation
    required: true
    type: document
  - field_name: documents_necessaires
    required: true
    type: document
  - field_name: calendrier_demarches
    required: true
    type: schedule
  - field_name: conditions_financieres
    required: true
    type: contract
  - field_name: confidentialite_engagement
    required: true
    type: document

recommended_fields:
  - field_name: service_urgence
  - field_name: logiciels_maitrises
  - field_name: accompagnement_physique
  - field_name: suivi_en_ligne

optional_fields:
  - field_name: horaires_flexibles
  - field_name: service_deplacement
  - field_name: partenariat_notaire
  - field_name: partenariat_banque
  - field_name: archive_numerique

conditional_fields:
  - field_name: representation_tiers
    condition: type_prestation_administrative == assistance_demarches || type_prestation_administrative == transcription_actes
    type: boolean
  - field_name: pouvoir_special
    condition: type_prestation_administrative == transcription_actes || type_prestation_administrative == coordination_partenaires
    type: boolean

sensitive_fields:
  - field_name: documents_clients_confidentiels
    pii: true
    sensitivity: high
  - field_name: identite_client_complet
    pii: true
    sensitivity: high
  - field_name: dossier_fiscal_client
    pii: true
    sensitivity: high
  - field_name: contrat_mandat
    pii: true
    sensitivity: high
  - field_name: coordonnees_bancaires
    pii: true
    sensitivity: high
  - field_name: copie_pieces_identite
    pii: true
    sensitivity: high
```

---
