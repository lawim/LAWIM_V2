# LAWIM

# 01-GLOSSAIRE.md

## Glossaire Officiel de LAWIM

Version 1.0

---

# 1. OBJECTIF

Le présent document constitue le dictionnaire officiel de LAWIM.

Il définit tous les termes métier utilisés dans :

* la Constitution ;
* les référentiels immobiliers ;
* le moteur conversationnel ;
* le moteur de matching ;
* les dashboards ;
* les API ;
* les tests ;
* la base de données.

Aucun terme ne peut être utilisé avec une autre signification.

---

# 2. PRINCIPES

Un terme possède :

* un seul nom officiel ;
* une seule définition officielle ;
* plusieurs synonymes éventuels.

Le code doit utiliser exclusivement le nom officiel.

---

# 3. PERSONNES

## Utilisateur

Toute personne utilisant LAWIM.

---

## Demandeur

Utilisateur recherchant un bien immobilier.

Synonymes

* Client
* Acheteur
* Locataire
* Investisseur

Selon le contexte.

---

## Propriétaire

Personne propriétaire du bien.

---

## Introduceur

Personne ayant introduit un propriétaire ou un bien dans LAWIM.

Il ne possède pas nécessairement le bien.

---

## Agent immobilier

Professionnel chargé d'intermédier des transactions.

---

## Agence immobilière

Entreprise exerçant une activité immobilière.

---

## Gestionnaire

Utilisateur chargé d'administrer un ensemble de biens.

---

## Administrateur

Utilisateur disposant des droits d'administration de LAWIM.

---

# 4. BIENS IMMOBILIERS

## Bien

Tout objet immobilier enregistré dans LAWIM.

---

## Bien résidentiel

Bien destiné principalement à l'habitation.

---

## Bien commercial

Bien destiné principalement à une activité économique.

---

## Bien industriel

Bien destiné principalement à une activité industrielle ou logistique.

---

## Bien agricole

Bien destiné principalement à une activité agricole.

---

## Bien hôtelier

Bien destiné principalement à l'hébergement.

---

## Bien mixte

Bien combinant plusieurs usages.

---

# 5. OPÉRATIONS

## Vente

Transfert définitif de propriété.

---

## Location

Mise à disposition temporaire contre paiement.

---

## Location meublée

Location comprenant le mobilier.

---

## Transaction

Aboutissement contractuel d'un dossier immobilier.

Selon le contexte, il peut s'agir d'une vente, d'une location ou d'un autre acte prévu par le référentiel.

---

## Visite

Déplacement organisé pour examiner un bien immobilier.

Une visite peut être physique ou préparée logistiquement par LAWIM.

---

## Détenteur

Personne habilitée à décider pour un bien.

Le détenteur peut être le propriétaire, une agence, un agent mandaté ou tout autre acteur autorisé.

---

## Lead

Résultat de matching formalisé entre une demande et un bien.

Le lead sert à tracer la compatibilité et à préparer la mise en relation.

---

## Notification

Message système généré par un événement identifié.

Une notification ne crée jamais la vérité métier.

---

## Service LAWIM

Service payant proposé par LAWIM.

Exemples :

* mise en relation payante ;
* accompagnement de visite ;
* accompagnement de transaction ;
* contrôle documentaire ;
* photographie ;
* vidéo ;
* vérification ;
* boost ;
* visibilité premium ;
* assistance.

---

## Recherche

Expression d'un besoin immobilier.

---

# 6. DOSSIERS

## Dossier

Ensemble des informations concernant un besoin immobilier.

Un utilisateur peut posséder plusieurs dossiers.

Chaque dossier possède son propre historique.

---

# 7. MOTEURS OFFICIELS

## Workflow Engine

Moteur qui orchestre les états, les transitions et les événements métier.

---

## Matching Engine

Moteur qui calcule la compatibilité entre un besoin et des biens.

---

## Conversation Engine

Moteur qui qualifie le besoin à partir des échanges avec l'utilisateur.

---

## Dashboard Engine

Moteur qui affiche les indicateurs, alertes et vues contextualisées.

---

## Notification Engine

Moteur qui diffuse les alertes et notifications officielles.

---

## Geo Engine

Moteur qui normalise la localisation et calcule les proximités.

---

## Role Engine

Moteur qui gère les rôles, permissions, comptes et responsabilités.

---

## Reporting Engine

Moteur qui calcule les indicateurs et les rapports officiels.

---

## Storage Lifecycle Manager

Moteur qui organise le stockage, l'archivage, les sauvegardes et la restauration.

---

## Security Engine

Moteur qui protège les accès, les secrets, les documents sensibles et les paiements.

---

## API Gateway

Point d'entrée officiel des API de LAWIM.

---

## Administration Engine

Moteur de supervision, de validation et d'administration interne.

---

## LAWIM AI

Assistant intelligent de recommandation, de synthèse et d'analyse.

---

## Continuous Learning Engine

Moteur qui prépare les apprentissages mensuels validés par l'humain.

---

## Campay Payment Engine

Module officiel de paiement Mobile Money via Campay pour les services LAWIM.

---

# 8. PAIEMENT CAMPAY

## Campay

Prestataire de paiement Mobile Money utilisé par LAWIM pour les services payants.

---

## Webhook

Appel serveur à serveur reçu après un événement externe, notamment la confirmation d'un paiement.

---

## Mobile Money

Mode de paiement électronique lié au portefeuille mobile de l'utilisateur.

---

## Rapprochement

Contrôle entre les opérations enregistrées dans LAWIM et les confirmations externes du prestataire de paiement.

---

## Qualification

Transformation d'une conversation en informations immobilières structurées.

---

## Matching

Recherche des biens compatibles avec un dossier.

---

## Rematching

Nouvelle recherche automatique après un échec du matching précédent.

---

## Trust Score

Score de confiance associé à un compte, un acteur ou une entité métier selon les règles du référentiel.

Le Trust Score complète l'identité. Il ne remplace jamais le rôle.

---

## Mandat

Autorisation donnée à un tiers d'agir pour le compte d'un propriétaire ou d'un détenteur.

---

## Procuration

Acte ou document permettant à une personne d'agir au nom d'une autre dans le cadre autorisé.

---

## Notaire

Professionnel du droit chargé d'authentifier certains actes immobiliers.

---

# 7. CONVERSATION

## Conversation

Suite chronologique des échanges entre LAWIM et un utilisateur.

---

## Mémoire conversationnelle

Ensemble des informations déjà connues.

---

## Champ critique

Information indispensable pour lancer le matching.

---

## Champ obligatoire

Information nécessaire pour qualifier correctement un bien.

---

## Champ recommandé

Information améliorant le matching.

---

## Champ facultatif

Information utile mais non indispensable.

---

## Champ interdit

Information qui ne doit jamais être demandée pour un type de bien.

---

# 8. MATCHING

## Score

Indice de compatibilité entre un besoin et un bien.

---

## Compatibilité

Mesure de la correspondance entre les critères du dossier et les caractéristiques du bien.

---

## Priorité

Poids attribué à un critère dans le calcul du score.

---

## Matching Engine

Moteur chargé d'évaluer la compatibilité entre un besoin et un bien.

---

# 9. GÉOGRAPHIE

## Ville

Commune officielle.

---

## Quartier

Subdivision d'une ville.

---

## Localité

Lieu ne correspondant pas forcément à une commune.

Exemple :

Village.

---

## Coordonnées GPS

Latitude et longitude d'un bien.

---

## Distance

Écart géographique entre deux positions.

---

## Zone LAWIM

Bassin immobilier cohérent utilisé pour la recherche, le matching et l'analyse territoriale.

---

# 10. DONNÉES

## Attribut

Caractéristique d'un bien.

Exemple :

Parking.

Forage.

Piscine.

---

## Valeur normalisée

Valeur appartenant au catalogue officiel.

---

## Synonyme

Terme accepté mais automatiquement converti vers le nom officiel.

---

# 11. STATUTS

## Disponible

Bien pouvant être proposé.

---

## Réservé

Bien momentanément indisponible.

---

## Loué

Bien actuellement loué.

---

## Vendu

Bien définitivement vendu.

---

## Archivé

Bien retiré des propositions.

---

# 12. GÉOLOCALISATION

## OpenStreetMap

Référentiel cartographique officiel de LAWIM.

---

## Géocodage

Transformation d'une adresse en coordonnées GPS.

---

## Géocodage inverse

Transformation de coordonnées GPS en adresse.

---

# 13. TABLEAUX DE BORD

## Dashboard

Interface dynamique, contextualisée et adaptée au rôle qui affiche les informations utiles au moment utile.

Le Dashboard ne décide pas. Il projette l'état de LAWIM.

---

# 14. IA

## Assistant LAWIM

Assistant conversationnel officiel de LAWIM.

Il applique exclusivement les règles définies dans la Constitution.

---

# 15. NORMALISATION

Tout terme rencontré dans une conversation est converti vers son terme officiel.

Exemple :

TF

↓

Titre foncier

---

Ydé

↓

Yaoundé

---

Deux chambres

↓

Appartement
Nombre de chambres = 2

---

# 16. INTERDICTION

Deux définitions officielles d'un même terme sont interdites.

Deux noms officiels pour un même concept sont interdits.

Toute ambiguïté doit être supprimée avant implémentation.

---

# FIN DU DOCUMENT

## 17. SUPPORT MULTILINGUE

Le glossaire officiel doit pouvoir être décliné en Français, English et Pidgin English.

Chaque concept peut posséder des libellés multilingues, des synonymes régionaux et des variantes contrôlées.

Les définitions canoniques restent uniques ; seules les formes d'expression changent selon la langue.

Le présent Glossaire constitue le dictionnaire officiel de LAWIM.

Tous les documents de la Constitution doivent utiliser exclusivement les définitions qu'il contient.
