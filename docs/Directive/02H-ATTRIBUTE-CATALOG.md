# LAWIM

# 02H-ATTRIBUTE-CATALOG.md

# Catalogue officiel des attributs et valeurs normalisées

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit le catalogue officiel des attributs utilisés par LAWIM pour :

* la conversation ;
* la qualification ;
* le matching ;
* la base de données ;
* les dashboards ;
* les notifications ;
* les tests ;
* les exports et contrôles.

Il constitue la référence de normalisation pour toutes les valeurs libres rencontrées dans la plateforme.

---

# CHAPITRE 2 — PRINCIPE FONDAMENTAL

Un attribut officiel possède :

* un nom canonique ;
* une signification unique ;
* des synonymes autorisés ;
* des valeurs autorisées quand l'attribut est énuméré.

Aucune équipe ne doit inventer une variante locale si l'attribut existe déjà dans ce catalogue.

---

# CHAPITRE 3 — ATTRIBUTS D'IDENTITÉ ET D'ACTEURS

Les attributs suivants servent à identifier les personnes et les organisations.

| Attribut canonique | Usage |
| --- | --- |
| `user` | Utilisateur générique de LAWIM |
| `demandeur` | Personne recherchant un bien |
| `proprietaire` | Personne propriétaire du bien |
| `introduceur` | Personne ayant mis le bien en relation avec LAWIM |
| `detenteur` | Personne habilitée à décider pour le bien |
| `agent_immobilier` | Professionnel immobilier |
| `agence_immobiliere` | Organisation immobilière |
| `gestionnaire` | Gestionnaire de biens ou d'organisation |
| `partenaire` | Prestataire ou intervenant associé |
| `membre_lawim` | Membre de l'équipe LAWIM |
| `administrateur` | Utilisateur disposant des droits d'administration |
| `notaire` | Professionnel juridique intervenant dans la transaction |

Synonymes autorisés :

* client -> demandeur ;
* locataire -> demandeur selon le contexte ;
* acheteur -> demandeur selon le contexte ;
* propriétaire mandaté -> détenteur si la décision lui appartient ;
* agence -> agence_immobiliere.

---

# CHAPITRE 4 — ATTRIBUTS MÉTIER IMMOBILIERS

Les attributs ci-dessous sont utilisés pour décrire les biens, les besoins et les offres.

| Attribut canonique | Valeurs principales |
| --- | --- |
| `famille_bien` | residentiel, commercial, industriel, agricole, hotelier, mixte |
| `type_bien_residentiel` | chambre, chambre_moderne, studio, studio_meuble, appartement, appartement_meuble, duplex, maison, villa, immeuble_residentiel, mini_cite, residence |
| `operation` | vente, location, location_meublee, bail_professionnel, bail_commercial |
| `standing` | standard, good, premium, vip, exclusive, luxury |
| `disponibilite` | immediate, aujourd_hui, cette_semaine, ce_mois, date_precise |
| `statut_bien` | created, qualified, published, deactivated, sold, archived |
| `statut_demande` | draft, active, paused, converted, archived |

Synonymes autorisés :

* location meublée -> `location_meublee` ;
* bail pro -> `bail_professionnel` ;
* bail commercial -> `bail_commercial` ;
* publié -> `published` ;
* archivé -> `archived`.

---

# CHAPITRE 5 — ATTRIBUTS GÉOGRAPHIQUES

Les attributs de localisation sont normalisés pour toutes les couches de LAWIM.

| Attribut canonique | Usage |
| --- | --- |
| `pays` | Pays de référence |
| `ville` | Commune ou ville de référence |
| `quartier` | Unité géographique privilégiée |
| `secteur` | Sous-zone de proximité |
| `point_de_repere` | Repère local reconnu |
| `gps_latitude` | Latitude |
| `gps_longitude` | Longitude |
| `distance` | Écart entre deux positions |
| `zone_lawim` | Bassin immobilier cohérent |

Synonymes autorisés :

* yaounde / yde -> Yaoundé ;
* douala centre / centre ville -> quartier ou zone selon le contexte ;
* carrefour / rond-point / station-service -> point de repère si le contexte le justifie.

---

# CHAPITRE 6 — ATTRIBUTS IMMOBILIERS COMPLÉMENTAIRES

Les attributs suivants complètent la description d'un bien ou d'un besoin.

| Attribut canonique | Exemples de valeurs |
| --- | --- |
| `budget_min` | valeur numérique |
| `budget_max` | valeur numérique |
| `superficie` | m² |
| `chambres` | entier |
| `salles_de_bain` | entier |
| `parking` | aucun, moto, 1_vehicule, 2_vehicules, 3_plus |
| `securite` | aucune, gardien, barriere, cloture, videosurveillance |
| `amenity` | forage, compteur_eneo, compteur_camwater, balcon, jardin, piscine, climatisation, internet |
| `type_douche` | interne, externe, partagee |
| `type_cuisine` | interne, externe, kitchenette |
| `acces` | independant, partagé |
| `mobilier` | meuble, non_meuble |
| `source_origine` | annonce, saisie_directe, import, relation, partenaire, autre |

Attributs de prix :

| Attribut canonique | Usage |
| --- | --- |
| `prix_vente` | Prix demandé pour une vente |
| `loyer` | Montant locatif récurrent |
| `caution` | Dépôt de garantie |
| `avance_loyer` | Avance demandée pour la location |
| `mensualite` | Paiement périodique |
| `frais_service` | Frais liés aux services LAWIM |
| `devise` | Monnaie utilisée |
| `taxe_estimee` | Charge fiscale éventuelle |
| `estimation_prix` | Valeur estimée par le moteur ou un acteur habilité |
| `fourchette_marche` | Intervalle de prix observé sur le marché |
| `historique_prix` | Série de variations historiques |
| `variation_prix` | Écart entre deux valeurs de prix |

---

# CHAPITRE 7 — ATTRIBUTS JURIDIQUES ET DOCUMENTAIRES

Les attributs juridiques sont utilisés pour les biens, les détenteurs et les transactions.

| Attribut canonique | Usage |
| --- | --- |
| `mandat` | Autorisation d'agir pour un propriétaire |
| `procuration` | Pouvoir donné à un tiers |
| `titre_foncier` | Référence de propriété foncière |
| `rccm` | Identifiant d'enregistrement d'entreprise |
| `numero_contribuable` | Identifiant fiscal |
| `piece_identite` | CNI, passeport, titre de séjour |
| `contrôle_documentaire` | Vérification des pièces |
| `visite` | Visite physique du bien |
| `transaction` | Vente, location ou autre aboutissement contractuel |

Synonymes autorisés :

* TF -> titre_foncier ;
* dossier juridique -> contrôle_documentaire selon le contexte ;
* rendez-vous sur site -> visite ;
* procuration légale -> procuration.

---

# CHAPITRE 8 — ATTRIBUTS DE SERVICES ET DE MONÉTISATION

LAWIM utilise ces attributs pour les services facturables.

| Attribut canonique | Usage |
| --- | --- |
| `mise_en_relation` | Mise en relation payante |
| `accompagnement_visite` | Accompagnement physique ou logistique |
| `accompagnement_transaction` | Assistance jusqu'à la clôture |
| `photographie` | Production de photos |
| `video` | Production de vidéos |
| `verification` | Vérification humaine ou assistée |
| `boost` | Accélération de visibilité |
| `visibilite_premium` | Mise en avant payante |
| `assistance` | Assistance opérationnelle |

Règle absolue :

LAWIM ne prélève aucune commission sur les ventes ou locations immobilières.

---

# CHAPITRE 9 — ATTRIBUTS D'ENGAGEMENT ET DE QUALITÉ

| Attribut canonique | Usage |
| --- | --- |
| `lead` | Opportunité issue du matching |
| `relationship` | Relation active entre parties |
| `notification` | Message système lié à un événement |
| `trust_score` | Score de confiance |
| `score_snapshot` | Historique d'un score calculé |
| `qualite_donnee` | Niveau de complétude ou de fiabilité |
| `fraicheur` | Actualité d'une donnée |

---

# CHAPITRE 10 — NORMALISATION ET CONTRÔLE

Toute valeur saisie par un utilisateur ou reçue d'un canal externe doit être :

* comparée au catalogue officiel ;
* rapprochée de ses synonymes ;
* convertie vers une valeur canonique ;
* historisée si la valeur d'origine doit être conservée.

Les valeurs libres ne sont acceptées que si aucune valeur canonique n'existe déjà.

---

# CHAPITRE 11 — RÈGLES ABSOLUES

Le catalogue doit toujours :

* éviter les doublons de sens ;
* utiliser une seule valeur canonique par concept ;
* rester compatible avec la Constitution ;
* rester compatible avec la base de données ;
* rester compatible avec les tests ;
* rester compatible avec les moteurs de LAWIM.

Il est interdit :

* de créer deux noms pour le même attribut ;
* de créer deux valeurs canoniques concurrentes ;
* d'utiliser un synonyme comme valeur stockée définitive.

---

# CHAPITRE 12 — OBJECTIF FINAL

Le catalogue d'attributs permet à LAWIM de parler un langage métier unique, compréhensible par les humains, exploitable par les moteurs et stable dans le temps.

Il constitue la base commune de la conversation, du matching, de la base de données, des dashboards et des tests.

---

# FIN DU DOCUMENT

Le présent **02H-ATTRIBUTE-CATALOG.md** constitue la référence officielle de normalisation des attributs de LAWIM.
